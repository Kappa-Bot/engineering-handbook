#!/usr/bin/env python3
"""Stable, dependency-free Handbook bootstrap. Never execute a downloaded validator.

Trust boundary: the owner-authorized canonical HTTPS repository and this locally
installed bootstrap. Fast-forward and hashes detect drift, not a compromised
maintainer or same-user attacker. Bootstrap upgrades require explicit install.
"""
from __future__ import annotations

import argparse
import errno
import base64
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unicodedata
import uuid

CANONICAL_REMOTE = "https://github.com/Kappa-Bot/engineering-handbook.git"
BOOTSTRAP_API = 2
SKILL_SOURCE = "agent-config/codex/skills/engineering-handbook/SKILL.md"
BUNDLE_SOURCE = "agent-config/codex/skills/engineering-handbook/bundle.json"
MAX_FILES = 2000
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_BUNDLE_BYTES = 64 * 1024 * 1024
CACHE_CONFIG = b"[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = true\n"
RUNTIME_MODULES = {"__init__", "__main__", "canonical", "cli", "conformance", "context_solver", "discovery", "discovery_rules", "handbook_compile", "handbook_source", "planning_ir", "repo_profile", "task_descriptor", "visual_directions"}
REGISTRIES = {"rules.v1.json": "discovery-rules/v1", "routes.v1.json": "discovery-routes/v1", "landmarks.v1.json": "discovery-landmarks/v1", "taxonomy.v1.json": "discovery-taxonomy/v1"}


class UpdateBlocked(RuntimeError):
    pass


class NetworkUnavailable(RuntimeError):
    pass


def json_bytes(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stable_hash(value) -> str:
    return "sha256:" + digest(json_bytes(value))


def read_json(path: Path) -> dict:
    try:
        result = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise UpdateBlocked(f"invalid or missing JSON: {path.name}") from exc
    if not isinstance(result, dict):
        raise UpdateBlocked(f"JSON object required: {path.name}")
    return result


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        raise UpdateBlocked(f"unsafe bundle path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value or any(p in {".", ".."} for p in path.parts):
        raise UpdateBlocked(f"unsafe bundle path: {value!r}")
    for part in path.parts:
        if part.endswith((".", " ")) or re.search(r'[<>"|?*\x00-\x1f]', part) or re.match(r"^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)", part, re.I):
            raise UpdateBlocked(f"nonportable bundle path: {value!r}")
    return value


def no_links(path: Path) -> None:
    for candidate in (path, *path.parents):
        if candidate.is_symlink() or (candidate.exists() and getattr(candidate.lstat(), "st_file_attributes", 0) & 0x400):
            raise UpdateBlocked(f"symlink/reparse point is not allowed: {candidate}")


def generated(path: str) -> bool:
    return "__pycache__" in PurePosixPath(path).parts or path.endswith((".pyc", ".pyo"))


def validate_files(files: dict[str, bytes]) -> None:
    if not files or len(files) > MAX_FILES or "SKILL.md" not in files:
        raise UpdateBlocked("invalid bundle file count or missing SKILL.md")
    identities = set()
    total = 0
    for name, content in files.items():
        safe_relative(name)
        if name == "install-manifest.json" or not isinstance(content, bytes) or len(content) > MAX_FILE_BYTES:
            raise UpdateBlocked("invalid bundle entry")
        identity = name.casefold()
        if identity in identities or any(parent.as_posix().casefold() in identities for parent in PurePosixPath(name).parents if parent.as_posix() != "."):
            raise UpdateBlocked("bundle path collision")
        identities.add(identity); total += len(content)
    # Detect parent-file collisions regardless of input order.
    for name in files:
        if any(parent.as_posix().casefold() in identities for parent in PurePosixPath(name).parents if parent.as_posix() != "."):
            raise UpdateBlocked("bundle file/directory collision")
    if total > MAX_BUNDLE_BYTES:
        raise UpdateBlocked("bundle exceeds size limit")


def make_manifest(files: dict[str, bytes], revision: str) -> dict:
    validate_files(files)
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise UpdateBlocked("invalid source revision")
    return {"schema_version": 2, "skill_name": "engineering-handbook", "source_repository": CANONICAL_REMOTE,
            "revision": revision, "bootstrap_api": BOOTSTRAP_API,
            "files": [{"install_path": name, "source_path": SKILL_SOURCE if name == "SKILL.md" else name.removeprefix("references/"), "sha256": digest(files[name])} for name in sorted(files)]}


def atomic_write(path: Path, content: bytes) -> None:
    no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        with temporary.open("xb") as stream:
            stream.write(content); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def snapshot_files(root: Path) -> dict[str, bytes]:
    no_links(root)
    result = {}
    if not root.is_dir():
        raise UpdateBlocked("installed snapshot is missing")
    for current, dirs, names in os.walk(root, followlinks=False):
        for name in [*dirs, *names]:
            no_links(Path(current) / name)
        for name in names:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            if relative == "install-manifest.json" or generated(relative):
                continue
            if not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > MAX_FILE_BYTES:
                raise UpdateBlocked("unexpected installed file type or size")
            result[relative] = path.read_bytes()
    return result


def verify_snapshot(root: Path, expected_manifest_hash: str) -> dict:
    manifest_path = root / "install-manifest.json"
    no_links(manifest_path)
    if not manifest_path.is_file() or digest(manifest_path.read_bytes()) != expected_manifest_hash:
        raise UpdateBlocked("installed manifest drift or missing trusted manifest")
    manifest = read_json(manifest_path)
    files = snapshot_files(root)
    expected = make_manifest(files, manifest.get("revision", ""))
    if manifest != expected:
        raise UpdateBlocked("installed file drift; preserve edits and reconcile explicitly")
    return manifest


def verify_installed(config: dict) -> dict:
    bootstrap = Path(config["bootstrap"])
    no_links(bootstrap)
    state = read_json(bootstrap / "state.json")
    if state.get("schema") != "handbook-state/v2":
        raise UpdateBlocked("unsupported installed state")
    manifest = verify_snapshot(Path(config["target"]), state.get("manifest_sha256", ""))
    if state.get("revision") != manifest["revision"]:
        raise UpdateBlocked("revision drift in installed state")
    snapshot = Path(state.get("snapshot", ""))
    if not snapshot.is_absolute() or snapshot.parent != bootstrap / "snapshots" or ".." in snapshot.parts:
        raise UpdateBlocked("invalid immutable snapshot location")
    verify_snapshot(snapshot, state["manifest_sha256"])
    return state


LOCK_FORMAT = "handbook-os-lock/v1"
LOCK_WAIT_SECONDS = 10


@contextmanager
def update_lock(bootstrap: Path):
    """Kernel-owned cross-process lock: an abnormal exit releases ownership.

    Keep the inode on disk after unlock. Unlinking it creates a race in which
    two different processes may hold locks on different replacement inodes.
    Legacy create-exclusive locks must be reconciled rather than stolen.
    """
    no_links(bootstrap)
    bootstrap.mkdir(parents=True, exist_ok=True)
    path = bootstrap / "update.lock"
    no_links(path)
    was_present = path.exists()
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_BINARY", 0)
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "r+b") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise UpdateBlocked("update lock is not a regular file")
        acquired = False
        deadline = time.monotonic() + LOCK_WAIT_SECONDS
        try:
            while not acquired:
                try:
                    stream.seek(0)
                    if os.name == "nt":
                        import msvcrt
                        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                except OSError as exc:
                    if exc.errno not in {errno.EACCES, errno.EAGAIN}:
                        raise
                    if time.monotonic() >= deadline:
                        raise UpdateBlocked("update lock held by another root preflight; retry session start") from exc
                    time.sleep(0.15)

            stream.seek(0)
            existing = stream.read(4097)
            if len(existing) > 4096:
                raise UpdateBlocked("invalid update lock metadata; manual recovery required")
            if existing:
                try:
                    metadata = json.loads(existing)
                except (ValueError, UnicodeDecodeError) as exc:
                    raise UpdateBlocked("invalid or interrupted legacy update lock; preserve and reconcile it") from exc
                if not isinstance(metadata, dict) or metadata.get("schema") != LOCK_FORMAT:
                    raise UpdateBlocked("legacy update.lock requires verified process shutdown and manual migration")
            elif was_present:
                raise UpdateBlocked("empty pre-existing update.lock requires manual recovery")

            stream.seek(0)
            stream.truncate(0)
            stream.write(json_bytes({"schema": LOCK_FORMAT, "pid": os.getpid(), "created": int(time.time())}))
            stream.flush()
            os.fsync(stream.fileno())
            yield
        finally:
            if acquired:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def write_snapshot(path: Path, files: dict[str, bytes], manifest: dict) -> None:
    no_links(path)
    path.mkdir(parents=True, exist_ok=False)
    for relative, content in files.items():
        target = path / safe_relative(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    (path / "install-manifest.json").write_bytes(json_bytes(manifest))
    verify_snapshot(path, digest(json_bytes(manifest)))


def recover_activation(config: dict) -> None:
    """Under update_lock, finish a committed activation or restore verified old state."""
    bootstrap = Path(config["bootstrap"]); journal_path = bootstrap / "activation.json"
    if not journal_path.exists():
        return
    journal = read_json(journal_path)
    target = Path(config["target"])
    backup = Path(journal["backup"]) if journal.get("backup") else None
    stage = Path(journal["stage"])
    if journal.get("target") != str(target) or stage.parent != target.parent or not stage.name.startswith(".handbook-stage-") or (backup and (backup.parent != bootstrap / "backups")):
        raise UpdateBlocked("invalid activation journal; manual recovery required")
    no_links(stage)
    if backup:
        no_links(backup)
    state_path = bootstrap / "state.json"
    current = read_json(state_path) if state_path.exists() else None
    if current == journal["new_state"] and target.exists():
        verify_installed(config)
        journal_path.unlink(); return
    old = journal.get("old_state")
    if backup and backup.exists():
        verify_snapshot(backup, old["manifest_sha256"])
        if target.exists():
            verify_snapshot(target, journal["new_state"]["manifest_sha256"])
            quarantined = bootstrap / "backups" / ("interrupted-" + uuid.uuid4().hex)
            os.replace(target, quarantined)
        os.replace(backup, target)
    elif old:
        verify_snapshot(target, old["manifest_sha256"])
    elif target.exists():
        verify_snapshot(target, journal["new_state"]["manifest_sha256"])
        quarantined = bootstrap / "backups" / ("interrupted-" + uuid.uuid4().hex)
        quarantined.parent.mkdir(parents=True, exist_ok=True)
        os.replace(target, quarantined)
    if old:
        atomic_write(state_path, json_bytes(old))
    elif state_path.exists():
        raise UpdateBlocked("unexpected state during first-install recovery")
    journal_path.unlink()


def activate(config: dict, files: dict[str, bytes], manifest: dict) -> dict:
    """Caller holds update_lock. Keep immutable per-task snapshots and recoverable old copy."""
    validate_files(files)
    if manifest != make_manifest(files, manifest.get("revision", "")):
        raise UpdateBlocked("candidate manifest mismatch")
    bootstrap = Path(config["bootstrap"]); target = Path(config["target"])
    no_links(bootstrap); no_links(target)
    recover_activation(config)
    state_path = bootstrap / "state.json"
    old_state = verify_installed(config) if target.exists() or state_path.exists() else None
    target.parent.mkdir(parents=True, exist_ok=True)
    bootstrap.mkdir(parents=True, exist_ok=True)
    if target.parent.stat().st_dev != bootstrap.stat().st_dev:
        raise UpdateBlocked("bootstrap and skill must share a filesystem for recoverable activation")
    mh = digest(json_bytes(manifest))
    snapshot = bootstrap / "snapshots" / (manifest["revision"] + "-" + mh[:12])
    if snapshot.exists():
        verify_snapshot(snapshot, mh)
    else:
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        # A crash while constructing this copy must not poison the deterministic
        # published name. Unpublished stages can be retained for recovery.
        snapshot_stage = snapshot.parent / (".handbook-snapshot-stage-" + uuid.uuid4().hex)
        write_snapshot(snapshot_stage, files, manifest)
        os.rename(snapshot_stage, snapshot)
    stage = target.parent / (".handbook-stage-" + uuid.uuid4().hex)
    write_snapshot(stage, files, manifest)
    backup = bootstrap / "backups" / ((old_state["revision"] if old_state else "initial") + "-" + uuid.uuid4().hex)
    backup.parent.mkdir(parents=True, exist_ok=True)
    new_state = {"schema": "handbook-state/v2", "revision": manifest["revision"], "manifest_sha256": mh, "snapshot": str(snapshot)}
    journal = {"target": str(target), "stage": str(stage), "backup": str(backup) if old_state else None, "old_state": old_state, "new_state": new_state}
    atomic_write(bootstrap / "activation.json", json_bytes(journal))
    try:
        if old_state:
            os.replace(target, backup)
        os.replace(stage, target)
        verify_snapshot(target, mh)
        atomic_write(state_path, json_bytes(new_state))
        verify_installed(config)
        (bootstrap / "activation.json").unlink()
    except Exception:
        recover_activation(config)
        raise
    return new_state


def git_environment(bootstrap: Path) -> dict[str, str]:
    environment = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k not in {"SSH_ASKPASS", "SSH_ASKPASS_REQUIRE"}}
    environment.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "", "GIT_ALLOW_PROTOCOL": "https", "GIT_NO_REPLACE_OBJECTS": "1", "GIT_ATTR_NOSYSTEM": "1", "LC_ALL": "C"})
    return environment


def git_command(config: dict, args: list[str], *, input_bytes: bytes | None = None, timeout: float = 15, check: bool = True) -> subprocess.CompletedProcess:
    bootstrap = Path(config["bootstrap"])
    command = [config.get("git_executable", "git"), "--no-replace-objects", "-c", "core.hooksPath=" + str(bootstrap / "empty-hooks"),
               "-c", "credential.helper=", "-c", "http.sslVerify=true", "-c", "http.followRedirects=false", "-c", "protocol.allow=never", "-c", "protocol.https.allow=always",
               "-c", "gc.auto=0", "-c", "maintenance.auto=false", "-c", "fetch.fsckObjects=true", "-c", "transfer.fsckObjects=true", *args]
    remaining = config.get("_deadline", time.monotonic() + timeout) - time.monotonic()
    if remaining <= 0:
        raise UpdateBlocked("preflight time budget exhausted; retry before starting work")
    kwargs = {"capture_output": True, "env": git_environment(bootstrap), "cwd": str(bootstrap), "timeout": min(timeout, remaining)}
    if input_bytes is None:
        kwargs["stdin"] = subprocess.DEVNULL
    else:
        kwargs["input"] = input_bytes
    result = subprocess.run(command, **kwargs)
    if check and result.returncode:
        raise UpdateBlocked("Git verification failed (no credentials, hooks or prompt contents were forwarded)")
    return result


def prepare_cache(config: dict) -> Path:
    bootstrap = Path(config["bootstrap"]); cache = bootstrap / "cache.git"
    no_links(cache)
    empty = bootstrap / "empty-hooks"
    no_links(empty)
    empty.mkdir(exist_ok=True)
    if any(empty.iterdir()):
        raise UpdateBlocked("bootstrap empty hook/template directory was modified")
    if not cache.exists():
        git_command(config, ["init", "--bare", "--template=" + str(empty), str(cache)])
        atomic_write(cache / "config", CACHE_CONFIG)
    no_links(cache / "config")
    if (cache / "config").read_bytes() != CACHE_CONFIG:
        raise UpdateBlocked("dedicated Git cache configuration drift")
    for current, dirs, names in os.walk(cache, followlinks=False):
        for name in [*dirs, *names]:
            no_links(Path(current) / name)
    for path in (cache / "objects", cache / "refs", cache / "HEAD", cache / "objects/info/alternates", cache / "objects/info/http-alternates"):
        no_links(path)
    if any((cache / p).exists() for p in ("objects/info/alternates", "objects/info/http-alternates", "shallow")):
        raise UpdateBlocked("unsupported alternate or shallow Git cache")
    return cache


def fetch_revision(config: dict) -> tuple[str, Path]:
    if config.get("remote") != CANONICAL_REMOTE:
        raise UpdateBlocked("only the canonical HTTPS remote is allowed")
    cache = prepare_cache(config)
    try:
        result = git_command(config, ["--git-dir=" + str(cache), "fetch", "--no-tags", "--no-recurse-submodules", CANONICAL_REMOTE, "refs/heads/main"], check=False)
    except subprocess.TimeoutExpired as exc:
        # A whole-process timeout could be local object verification, not just
        # transport. Only explicit transport errors qualify as offline below.
        raise UpdateBlocked("canonical fetch exceeded its verification time budget") from exc
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").casefold()
        integrity_failure = re.search(r"certificate|ssl|tls|authentication|unauthorized|forbidden|fsck|corrupt|invalid|remote ref|repository not found", message)
        network_failure = re.search(r"could not resolve (?:host|proxy)|failed to connect|couldn't connect|connection (?:timed out|refused|reset)|network is unreachable|operation timed out", message)
        if network_failure and not integrity_failure:
            raise NetworkUnavailable("canonical HTTPS transport unavailable")
        raise UpdateBlocked("canonical fetch failed verification, authorization or configuration; not an offline fallback")
    revision = git_command(config, ["--git-dir=" + str(cache), "rev-parse", "--verify", "FETCH_HEAD^{commit}"]).stdout.decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise UpdateBlocked("invalid fetched commit")
    return revision, cache


def require_fast_forward(config: dict, cache: Path, previous: str, candidate: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", previous) or not re.fullmatch(r"[0-9a-f]{40}", candidate):
        raise UpdateBlocked("invalid revision for history check")
    result = git_command(config, ["--git-dir=" + str(cache), "merge-base", "--is-ancestor", previous, candidate], check=False)
    if result.returncode:
        raise UpdateBlocked("remote history is divergent, rewound or cannot be verified; no automatic replacement")


def validate_candidate(files: dict[str, bytes]) -> None:
    validate_files(files)
    prefix = "references/"
    required_files = {prefix + "automation/engineering_context/" + name + ".py" for name in RUNTIME_MODULES}
    required_files.update({prefix + "machine-readable/catalog.yaml", prefix + "agent-config/codex/AGENTS.global.md"})
    required_files.add(prefix + "machine-readable/visual-directions.v1.json")
    required_files.update(prefix + "machine-readable/discovery/" + name for name in REGISTRIES)
    if not required_files.issubset(files) or not files["SKILL.md"].strip():
        raise UpdateBlocked("candidate lacks the minimum runtime, catalog, registries or skill contract")
    def payload(path):
        try:
            value = json.loads(files[prefix + path])
        except (KeyError, ValueError) as exc:
            raise UpdateBlocked(f"missing or invalid candidate artifact: {path}") from exc
        if not isinstance(value, dict):
            raise UpdateBlocked(f"candidate JSON object required: {path}")
        return value
    manifest = payload("machine-readable/compiled/manifest.json")
    if manifest.get("schema") != "handbook-compiled/v1" or manifest.get("compiler_schema") != 3:
        raise UpdateBlocked("unsupported compiled contract; explicit bootstrap upgrade required")
    hashes = manifest.get("artifact_hashes", {})
    required = {"graph.json", "routing.json", "planning.json", "implementation.json", "verification.json", "discovery.json"}
    if not isinstance(hashes, dict) or set(hashes) != required:
        raise UpdateBlocked("candidate artifact hash inventory is incomplete")
    artifacts = {}
    for name, expected in hashes.items():
        artifacts[name] = payload("machine-readable/compiled/" + name)
        if stable_hash(artifacts[name]) != expected:
            raise UpdateBlocked("candidate compiled artifact hash mismatch")
    for name in ("planning.json", "implementation.json", "verification.json"):
        view = artifacts[name]
        if view.get("schema") != "handbook-compiled/v1" or not isinstance(view.get("units"), list) or not all(isinstance(unit, dict) for unit in view["units"]):
            raise UpdateBlocked("invalid candidate compiled units")
    graph = artifacts["graph.json"]
    if graph.get("schema") != "handbook-compiled/v1" or not isinstance(graph.get("edges"), dict):
        raise UpdateBlocked("invalid candidate compiled graph")
    for mapping in (graph["edges"], artifacts["routing.json"]):
        if not all(isinstance(key, str) and isinstance(value, list) and all(isinstance(item, str) for item in value) for key, value in mapping.items()):
            raise UpdateBlocked("invalid candidate compiled routing/dependencies")
    index = artifacts["discovery.json"]
    if index.get("schema") != "handbook-discovery/v1" or not all(isinstance(index.get(key), list) and all(isinstance(item, dict) for item in index[key]) for key in ("documents", "nodes", "edges", "topics")) or not index["documents"]:
        raise UpdateBlocked("invalid candidate discovery collections")
    index_body = {k: v for k, v in index.items() if k != "index_hash"}
    if index.get("index_hash") != stable_hash(index_body) or manifest.get("discovery_hash") != index["index_hash"]:
        raise UpdateBlocked("candidate discovery index hash mismatch")
    if stable_hash(files[prefix + "machine-readable/catalog.yaml"].decode("utf-8")) != index.get("catalog_source_hash"):
        raise UpdateBlocked("candidate catalog/index drift")
    for doc in index["documents"]:
        if not all(isinstance(doc.get(key), str) and doc[key] for key in ("id", "path", "kind", "status")):
            raise UpdateBlocked("invalid candidate discovery document")
        if doc.get("source_hash") is not None:
            path = prefix + safe_relative(doc["path"])
            if path not in files or stable_hash(files[path].decode("utf-8")) != doc["source_hash"]:
                raise UpdateBlocked("candidate canonical source/index drift")
    registry_hashes = index.get("registry_hashes")
    if not isinstance(registry_hashes, dict) or set(registry_hashes) != set(REGISTRIES):
        raise UpdateBlocked("candidate discovery registry inventory is incomplete")
    for name, expected in registry_hashes.items():
        registry = payload("machine-readable/discovery/" + name)
        if registry.get("schema") != REGISTRIES[name] or stable_hash(registry) != expected:
            raise UpdateBlocked("candidate routing registry drift")
    # This stable bootstrap validates downloaded data without importing or
    # executing downloaded Python. The four-file discovery API remains intact.
    visual = payload("machine-readable/visual-directions.v1.json")
    surfaces, defaults, directions = visual.get("surfaces"), visual.get("default_by_surface"), visual.get("directions")
    if (visual.get("schema") != "melodiq-visual-directions/v1"
            or not isinstance(surfaces, list) or not surfaces
            or not all(isinstance(surface, str) and re.fullmatch(r"[a-z]+(?:-[a-z]+)*", surface) for surface in surfaces)
            or len(set(surfaces)) != len(surfaces)
            or "internal-console" not in surfaces
            or defaults != {"internal-console": "glassmorphism"}
            or not isinstance(directions, list) or not directions):
        raise UpdateBlocked("invalid candidate visual-direction scope or schema")
    ids, aliases = set(), {}
    for item in directions:
        if not isinstance(item, dict):
            raise UpdateBlocked("invalid candidate visual-direction item")
        identity, title, words, reference = (item.get(key) for key in ("id", "title", "aliases", "reference"))
        if (not isinstance(identity, str) or not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", identity)
                or identity in ids or not isinstance(title, str) or not title.strip()
                or item.get("status") != "active" or not isinstance(words, list) or not words):
            raise UpdateBlocked("invalid candidate visual-direction identity")
        ids.add(identity)
        if not isinstance(reference, str) or not reference.endswith(".md"):
            raise UpdateBlocked("invalid candidate visual-direction reference")
        source_path = prefix + safe_relative(reference)
        if source_path not in files or not files[source_path].strip():
            raise UpdateBlocked("missing candidate visual-direction reference")
        for guidance in ("best_for", "avoid"):
            values = item.get(guidance)
            if not isinstance(values, list) or not all(isinstance(value, str) and value.strip() for value in values):
                raise UpdateBlocked("invalid candidate visual-direction guidance")
        for word in words:
            if not isinstance(word, str) or not word.strip():
                raise UpdateBlocked("invalid candidate visual-direction alias")
            key = "".join(char for char in unicodedata.normalize("NFKD", word.casefold()) if not unicodedata.combining(char)).strip()
            if not key or key in aliases:
                raise UpdateBlocked("ambiguous candidate visual-direction alias")
            aliases[key] = identity
    if "glassmorphism" not in ids or any(identity in aliases and aliases[identity] != identity for identity in ids):
        raise UpdateBlocked("invalid candidate visual-direction default/alias mapping")
    runtime = payload("machine-readable/agent-runtime-routing.v1.json")
    if runtime.get("schema") != "agent-runtime-routing/v1" or not all(isinstance(runtime.get(key), dict) for key in ("cheap_implementer", "model_routing", "spawn_configuration")):
        raise UpdateBlocked("invalid candidate model-routing contract")
    choices = runtime["model_routing"]
    if not isinstance(choices.get("current_tiers"), dict) or not all(isinstance(model, str) for model in choices["current_tiers"].values()) or not isinstance(choices.get("routes"), list) or not all(isinstance(route, dict) and isinstance(route.get("case"), str) and ("model" not in route or isinstance(route["model"], str)) for route in choices["routes"]):
        raise UpdateBlocked("invalid candidate model-routing selectors")
    if not isinstance(runtime["cheap_implementer"].get("current_preferred_model"), str) or not isinstance(runtime["spawn_configuration"].get("backstop_model"), str):
        raise UpdateBlocked("invalid candidate preferred/backstop selectors")
    def enables_luna(value):
        if isinstance(value, dict):
            return any(enables_luna(item) for item in value.values())
        if isinstance(value, list):
            return any(enables_luna(item) for item in value)
        return isinstance(value, str) and value.casefold() == "gpt-6-luna"
    if enables_luna(runtime):
        raise UpdateBlocked("candidate re-enables prohibited GPT-6 Luna routing")
    if not files[prefix + "agent-config/codex/AGENTS.global.md"].strip():
        raise UpdateBlocked("candidate lacks fresh global baseline")


def bundle_from_git(config: dict, cache: Path, revision: str) -> dict[str, bytes]:
    listing = git_command(config, ["--git-dir=" + str(cache), "ls-tree", "-rlz", revision]).stdout
    entries = {}
    for record in listing.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, oid, size = metadata.decode("ascii").split()
        name = raw_path.decode("utf-8")
        entries[name] = (mode, kind, oid, int(size) if size != "-" else -1)
    def read_blob(name):
        entry = entries.get(name)
        if entry is None or entry[0] not in {"100644", "100755"} or entry[1] != "blob" or not 0 <= entry[3] <= MAX_FILE_BYTES:
            raise UpdateBlocked("unsafe, oversized or missing Git bundle entry: " + name)
        return git_command(config, ["--git-dir=" + str(cache), "cat-file", "blob", entry[2]]).stdout
    try:
        bundle = json.loads(read_blob(BUNDLE_SOURCE))
    except ValueError as exc:
        raise UpdateBlocked("invalid bundle declaration") from exc
    if not isinstance(bundle, dict) or bundle.get("required_bootstrap_api") != BOOTSTRAP_API:
        raise UpdateBlocked("bundle requires an explicit stable-bootstrap upgrade")
    includes = bundle.get("include")
    if not isinstance(includes, list) or not includes:
        raise UpdateBlocked("invalid bundle includes")
    for include in includes:
        safe_relative(include)
        if not any(path == include or path.startswith(include + "/") for path in entries):
            raise UpdateBlocked("bundle include has no tracked source: " + include)
    selected = [path for path in entries if not generated(path) and any(path == include or path.startswith(include + "/") for include in includes)]
    if len(selected) > MAX_FILES or sum(max(0, entries[p][3]) for p in selected) > MAX_BUNDLE_BYTES:
        raise UpdateBlocked("remote bundle exceeds size limits")
    files = {"SKILL.md": read_blob(SKILL_SOURCE)}
    for path in selected:
        safe_relative(path)
        files["references/" + path] = read_blob(path)
    validate_candidate(files)
    return files


def refresh(config: dict) -> dict:
    config = {**config, "_deadline": time.monotonic() + 45}
    with update_lock(Path(config["bootstrap"])):
        if has_global_override(config):
            raise UpdateBlocked("AGENTS.override.md shadows global instructions; reconcile before preflight")
        recover_activation(config)
        previous = verify_installed(config)
        try:
            revision, cache = fetch_revision(config)
        except NetworkUnavailable:
            # Drift is checked before the network call; never bless a broken
            # installation merely because remote verification is unavailable.
            return {"status": "STALE_OFFLINE", **previous, "remote_checked": False}
        require_fast_forward(config, cache, previous["revision"], revision)
        if revision == previous["revision"]:
            return {"status": "CURRENT", **previous, "remote_checked": True}
        files = bundle_from_git(config, cache, revision)
        state = activate(config, files, make_manifest(files, revision))
        return {"status": "UPDATED", **state, "remote_checked": True}


def is_owned_hook_group(group: dict, event: str) -> bool:
    """Recognize only Handbook-owned hooks, including the old per-prompt one."""
    if not isinstance(group, dict) or len(group.get("hooks", [])) != 1:
        return False
    handler = group["hooks"][0]
    if not isinstance(handler, dict) or handler.get("type") != "command":
        return False
    try:
        args = shlex.split(handler.get("command", ""))
    except (ValueError, TypeError):
        return False
    return (len(args) >= 5
            and args[-4:] == ["preflight", "--hook", "--event", event]
            and args[-5].replace("\\", "/").split("/")[-1] == "handbook_update.py")


def merge_hooks(existing: dict, script: Path) -> dict:
    if not isinstance(existing, dict) or not isinstance(existing.get("hooks", {}), dict):
        raise UpdateBlocked("invalid existing hooks.json; not replaced")
    hooks = existing.setdefault("hooks", {})
    # Remove the legacy per-prompt updater; never affect unrelated prompt hooks.
    for event in ("UserPromptSubmit", "SessionStart"):
        groups = hooks.get(event, [])
        if not isinstance(groups, list) or not all(
            isinstance(g, dict) and isinstance(g.get("hooks"), list) for g in groups
        ):
            raise UpdateBlocked("invalid existing hook groups; not replaced")
        remaining = [group for group in groups if not is_owned_hook_group(group, event)]
        if remaining:
            hooks[event] = remaining
        else:
            hooks.pop(event, None)

    # Codex emits SessionStart only for root sessions; a spawned agent emits
    # SubagentStart instead. Startup/resume/clear are macro-execution boundaries,
    # not every user prompt or worker invocation.
    event = "SessionStart"
    argv = [sys.executable, "-I", str(script), "preflight", "--hook", "--event", event]
    command = shlex.join(argv)
    ps = "& " + " ".join("'" + value.replace("'", "''") + "'" for value in argv) + "; exit $LASTEXITCODE"
    windows = "powershell.exe -NoProfile -NonInteractive -EncodedCommand " + base64.b64encode(ps.encode("utf-16-le")).decode("ascii")
    owned = {"type": "command", "command": command, "commandWindows": windows,
             "timeout": 60, "statusMessage": "Refreshing Engineering Handbook", "additionalContextLimit": 6000}
    hooks.setdefault(event, []).append({"matcher": "startup|resume|clear", "hooks": [owned]})
    return existing


def has_global_override(config: dict) -> bool:
    override = Path(config["codex_home"]) / "AGENTS.override.md"
    no_links(override)
    return override.is_file() and bool(override.read_text(encoding="utf-8").strip())


def doctor(config: dict) -> dict:
    state = verify_installed(config)
    baseline = Path(state["snapshot"]) / "references/agent-config/codex/AGENTS.global.md"
    baseline_status = "PRESENT" if baseline.is_file() and baseline.read_bytes().strip() else "MISSING"
    hooks_path = Path(config["codex_home"]) / "hooks.json"
    no_links(hooks_path)
    existing = read_json(hooks_path) if hooks_path.is_file() else {}
    if not isinstance(existing.get("hooks", {}), dict):
        raise UpdateBlocked("invalid hooks.json; no execution claimed")
    expected = merge_hooks({}, Path(config["bootstrap"]) / "handbook_update.py")["hooks"]
    definitions = {}
    for event, expected_groups in expected.items():
        groups = existing.get("hooks", {}).get(event, [])
        if not isinstance(groups, list):
            raise UpdateBlocked("invalid hook definitions; no execution claimed")
        definitions[event] = "PRESENT" if expected_groups[0] in groups else "MISSING_OR_CHANGED" if groups else "MISSING"
    prompt_groups = existing.get("hooks", {}).get("UserPromptSubmit", [])
    if not isinstance(prompt_groups, list):
        raise UpdateBlocked("invalid UserPromptSubmit hook definitions")
    definitions["UserPromptSubmit"] = "STALE_OWNED_HOOK" if any(
        is_owned_hook_group(group, "UserPromptSubmit") for group in prompt_groups
    ) else "REMOVED"
    shadowed = has_global_override(config)
    status = "SHADOWED" if shadowed else "BASELINE_MISSING" if baseline_status == "MISSING" else "HOOKS_INCOMPLETE" if definitions.get("SessionStart") != "PRESENT" or definitions["UserPromptSubmit"] != "REMOVED" else "READY_FOR_CLIENT_VERIFICATION"
    return {"status": "VERIFIED_LOCAL", **state, "global_instruction_status": status,
            "global_baseline": baseline_status, "global_override": "PRESENT" if shadowed else "ABSENT",
            "hook_definitions": definitions, "hook_execution": "NOT_OBSERVED",
            "hook_trust_and_client_support": "NOT_OBSERVED", "remote_checked": False}


def hook_output(result: dict, event: str) -> dict:
    root = Path(result["snapshot"])
    context = (f"Engineering Handbook preflight: {result['status']}; revision {result['revision']}. "
               f"For this task use the immutable snapshot {root}. Read {root / 'references/agent-config/codex/AGENTS.global.md'} "
               f"and {root / 'SKILL.md'} before substantive work. The installed skill directory may refresh for another session; keep using this pinned snapshot. "
               "Global startup instructions are not claimed to have reloaded. Higher-priority instructions and repository authority still apply. "
               "GPT-6 Luna is prohibited; bounded/visual delegates use available GPT-6.1 Terra. Resolve current client capabilities, do not invent them.")
    if result["status"] == "STALE_OFFLINE":
        context += " Remote freshness could not be checked; this is a verified last-known-good copy, not a claim of being current. Report that limitation where relevant."
    return {"continue": True, "hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}


def local_bundle(source: Path) -> dict[str, bytes]:
    """Explicit manual distribution only; does not enroll a checkout in auto-update."""
    source = source.resolve()
    bundle = read_json(source / BUNDLE_SOURCE)
    files = {"SKILL.md": (source / SKILL_SOURCE).read_bytes()}
    for include in bundle.get("include", []):
        safe_relative(include)
        path = source / include
        no_links(path)
        if not path.exists():
            raise UpdateBlocked("missing bundle include: " + include)
        candidates = sorted(path.rglob("*")) if path.is_dir() else [path]
        for candidate in candidates:
            no_links(candidate)
            if candidate.is_file() and not generated(candidate.relative_to(source).as_posix()):
                files["references/" + candidate.relative_to(source).as_posix()] = candidate.read_bytes()
    validate_files(files)
    return files


def manual_bundle(source: Path, skills_home: Path, *, check: bool = False, backup_existing: bool = False) -> dict:
    """Portable counterpart of the manual PowerShell bundle installer (v1 manifest)."""
    files = local_bundle(source)
    full_manifest = make_manifest(files, "0" * 40)
    manifest = {"schema_version": 1, "skill_name": "engineering-handbook", "source_repository": CANONICAL_REMOTE, "files": full_manifest["files"]}
    target = skills_home.resolve() / "engineering-handbook"
    no_links(target)
    matches = False
    if target.exists():
        existing_manifest_path = target / "install-manifest.json"
        if existing_manifest_path.exists() and read_json(existing_manifest_path).get("schema_version") == 2:
            raise UpdateBlocked("enrolled target must use preflight; explicit unenrollment is required before manual replacement")
        try:
            current = read_json(target / "install-manifest.json")
            matches = current.get("files") == manifest["files"] and snapshot_files(target) == files
        except UpdateBlocked:
            matches = False
    if check:
        return {"status": "IN_SYNC" if matches else "OUT_OF_SYNC", "target": str(target), "auto_update": False}
    if matches:
        return {"status": "IN_SYNC", "target": str(target), "auto_update": False}
    if target.exists() and not backup_existing:
        raise UpdateBlocked("existing skill differs; explicit --backup-existing is required for manual replacement")
    skills_home.mkdir(parents=True, exist_ok=True)
    stage = target.parent / (".handbook-stage-" + uuid.uuid4().hex)
    # Write with the v2 verifier, then retain the established v1 manual manifest.
    write_snapshot(stage, files, full_manifest)
    atomic_write(stage / "install-manifest.json", json_bytes(manifest))
    backup = None
    if target.exists():
        backup = skills_home.parent / "skill-backups" / ("engineering-handbook.backup-" + uuid.uuid4().hex)
        no_links(backup); backup.parent.mkdir(parents=True, exist_ok=True)
        os.replace(target, backup)
    try:
        os.replace(stage, target)
    except Exception:
        if backup:
            os.replace(backup, target)
        raise
    return {"status": "INSTALLED", "target": str(target), "backup": str(backup) if backup else None, "auto_update": False}


def install(codex_home: Path, skills_home: Path, *, backup_existing: bool = False) -> dict:
    codex_home = codex_home.absolute(); skills_home = skills_home.absolute()
    no_links(codex_home); no_links(skills_home)
    bootstrap = codex_home / "handbook-bootstrap"
    bootstrap.mkdir(parents=True, exist_ok=True)
    script = bootstrap / "handbook_update.py"
    hooks_path = codex_home / "hooks.json"
    no_links(hooks_path)
    prior_hooks = hooks_path.read_bytes() if hooks_path.exists() else None
    merged = merge_hooks(read_json(hooks_path) if prior_hooks is not None else {}, script)
    override = codex_home / "AGENTS.override.md"
    no_links(override)
    if override.exists() and override.read_text(encoding="utf-8").strip():
        raise UpdateBlocked("AGENTS.override.md shadows global instructions; reconcile it explicitly before enrollment")
    config_path = bootstrap / "config.json"
    config = {"schema": "handbook-install/v2", "remote": CANONICAL_REMOTE, "bootstrap": str(bootstrap),
              "target": str(skills_home / "engineering-handbook"), "codex_home": str(codex_home),
              "git_executable": shutil.which("git")}
    if not config["git_executable"]:
        raise UpdateBlocked("Git is required")
    if config_path.exists():
        prior = read_json(config_path)
        if any(prior.get(key) != config[key] for key in ("schema", "remote", "bootstrap", "target", "codex_home")):
            raise UpdateBlocked("existing bootstrap configuration differs; no automatic relocation")
    with update_lock(bootstrap):
        recover_activation(config)
        revision, cache = fetch_revision(config)
        files = bundle_from_git(config, cache, revision)
        target = Path(config["target"])
        unmanaged_backup = None
        if (bootstrap / "state.json").exists():
            previous = verify_installed(config)
            require_fast_forward(config, cache, previous["revision"], revision)
        elif target.exists():
            if not backup_existing:
                raise UpdateBlocked("existing unmanaged skill; use --backup-existing once to retain and replace it")
            unmanaged_backup = bootstrap / "backups" / ("unenrolled-" + uuid.uuid4().hex)
            no_links(target); unmanaged_backup.parent.mkdir(exist_ok=True)
            os.replace(target, unmanaged_backup)
        try:
            state = activate(config, files, make_manifest(files, revision))
        except Exception:
            if unmanaged_backup and unmanaged_backup.exists() and not target.exists():
                os.replace(unmanaged_backup, target)
            raise
        bootstrap_code = Path(__file__).read_bytes()
        config["bootstrap_sha256"] = digest(bootstrap_code)
        if script.exists() and script.read_bytes() != bootstrap_code:
            backup_code = bootstrap / "backups" / ("bootstrap-" + uuid.uuid4().hex + ".py")
            atomic_write(backup_code, script.read_bytes())
        atomic_write(script, bootstrap_code)
        atomic_write(config_path, json_bytes(config))
        # Refuse to overwrite a concurrent human edit made during the fetch.
        now_hooks = hooks_path.read_bytes() if hooks_path.exists() else None
        if now_hooks != prior_hooks:
            raise UpdateBlocked("hooks.json changed during installation; bundle retained, hooks not replaced")
        if prior_hooks is not None and prior_hooks != json_bytes(merged):
            atomic_write(bootstrap / "backups" / ("hooks-" + uuid.uuid4().hex + ".json"), prior_hooks)
        atomic_write(hooks_path, json_bytes(merged))
    return {"status": "INSTALLED", **state, "hooks": str(hooks_path), "bootstrap": str(script),
            "hook_trust_and_client_support": "REQUIRES_CLIENT_VERIFICATION", "existing_AGENTS_md": "PRESERVED",
            "next": "Review/trust the hooks in Codex, start a fresh session and run doctor; old startup instructions are not retroactively reloaded."}


def load_config(path: Path) -> dict:
    no_links(path)
    config = read_json(path)
    if config.get("schema") != "handbook-install/v2" or config.get("remote") != CANONICAL_REMOTE:
        raise UpdateBlocked("unsupported installed bootstrap configuration")
    bootstrap = Path(config["bootstrap"])
    if path.absolute() != bootstrap / "config.json" or not bootstrap.is_absolute():
        raise UpdateBlocked("bootstrap configuration location mismatch")
    no_links(bootstrap)
    script = bootstrap / "handbook_update.py"
    if not script.is_file() or digest(script.read_bytes()) != config.get("bootstrap_sha256"):
        raise UpdateBlocked("installed bootstrap drift; reinstall explicitly")
    for key in ("target", "codex_home"):
        if not Path(config[key]).is_absolute() or ".." in Path(config[key]).parts:
            raise UpdateBlocked("installed paths must be absolute and normalized")
        no_links(Path(config[key]))
    if Path(config["target"]).name != "engineering-handbook" or bootstrap.parent != Path(config["codex_home"]):
        raise UpdateBlocked("invalid installed target")
    return config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe Engineering Handbook distribution and pre-task refresh")
    sub = parser.add_subparsers(dest="command", required=True)
    install_parser = sub.add_parser("install")
    install_parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    install_parser.add_argument("--skills-home", type=Path, default=Path.home() / ".agents/skills")
    install_parser.add_argument("--backup-existing", action="store_true")
    for name in ("preflight", "doctor"):
        command = sub.add_parser(name)
        command.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "config.json")
        if name == "preflight":
            command.add_argument("--hook", action="store_true")
            command.add_argument("--event", choices=("SessionStart", "UserPromptSubmit"), default="UserPromptSubmit")
    bundle_parser = sub.add_parser("bundle")
    bundle_parser.add_argument("--source", type=Path, required=True)
    bundle_parser.add_argument("--skills-home", type=Path, required=True)
    bundle_parser.add_argument("--check", action="store_true")
    bundle_parser.add_argument("--backup-existing", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "install":
            result = install(args.codex_home, args.skills_home, backup_existing=args.backup_existing)
        elif args.command == "bundle":
            result = manual_bundle(args.source, args.skills_home, check=args.check, backup_existing=args.backup_existing)
        elif args.command == "preflight" and args.hook and args.event == "UserPromptSubmit":
            # Old installed prompt hooks are deliberately inert until explicitly
            # reinstalled; no file, network, transcript or configuration read.
            print(json.dumps({"continue": True, "suppressOutput": True}))
            return 0
        else:
            config = load_config(args.config)
            result = refresh(config) if args.command == "preflight" else doctor(config)
        if getattr(args, "hook", False):
            # No stdin or transcript is read, logged, or forwarded. Event is a
            # fixed installer-owned argument, never derived from prompt text.
            print(json.dumps(hook_output(result, args.event), ensure_ascii=False))
        else:
            print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return 2 if result.get("status") == "OUT_OF_SYNC" else 0
    except (UpdateBlocked, NetworkUnavailable, OSError, ValueError, TypeError, KeyError, RecursionError, subprocess.TimeoutExpired) as exc:
        reason = "Engineering Handbook preflight blocked: " + str(exc)
        if getattr(args, "hook", False):
            output = {"continue": False, "stopReason": reason, "systemMessage": reason}
            if args.event == "UserPromptSubmit":
                output.update({"decision": "block", "reason": reason})
            print(json.dumps(output, ensure_ascii=False))
            return 0  # Structured stop is the documented hook control protocol.
        print(json.dumps({"status": "BLOCKED", "reason": reason}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
