from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any

from .canonical import canonical_json, load_json_with_unique_members, stable_hash
from .discovery_rules import discover_landmarks

LOCKFILES = {
    "pnpm-lock.yaml": "pnpm",
    "package-lock.json": "npm",
    "yarn.lock": "yarn",
    "bun.lockb": "bun",
    "bun.lock": "bun",
}
MIGRATION_HINTS = ("supabase/migrations", "migrations", "prisma/migrations")
TEST_HINTS = ("tests", "test", "__tests__", "e2e")
COMMERCIAL_CONTEXT_HINTS = (
    ".agents/product-marketing.md", ".claude/product-marketing.md",
    ".agents/product-marketing-context.md", ".claude/product-marketing-context.md",
    "docs/product-marketing.md", "docs/marketing-context.md",
)
EXCLUDED_DIRS = {".git", "node_modules", "dist", "build", ".next", ".venv", "venv", "__pycache__", ".cache", ".pytest_cache"}


class InvalidRepositoryRoot(ValueError):
    """An explicitly selected repository root is missing or is not a directory."""


def _repository_directory(root: Path) -> Path:
    root = root.resolve()
    if not root.is_dir():
        raise InvalidRepositoryRoot(f"Repository root must be an existing directory ({root}).")
    return root


def _contained_path(root: Path, path: Path) -> Path | None:
    try:
        target = path.resolve(strict=True)
    except (FileNotFoundError, NotADirectoryError, RuntimeError):
        return None
    return target if target.is_relative_to(root) else None


def _walk_entry_in_root(root: Path, path: Path) -> bool:
    try:
        info = path.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return False
    if stat.S_ISLNK(info.st_mode):
        return False
    # Junctions are reparse points, but Windows does not report them as symlinks.
    if getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        target = _contained_path(root, path)
        if target is None:
            return False
        if stat.S_ISDIR(info.st_mode):
            return all(
                target != _contained_path(root, ancestor)
                for ancestor in path.parents if ancestor.is_relative_to(root)
            )
    return True


def _has_migration_directory(root: Path) -> bool:
    for hint in MIGRATION_HINTS:
        directory = _contained_path(root, root / hint)
        if directory is not None and directory.is_dir():
            return True
    return False


def _walk_files(root: Path, start: Path, max_depth: int | None = None) -> list[Path]:
    if not _walk_entry_in_root(root, start) or (start != root and _contained_path(root, start) is None):
        return []
    if start.is_file():
        return [start]
    files: list[Path] = []
    for current, dirs, names in os.walk(start, topdown=True):
        current_path = Path(current)
        try:
            current_depth = len(current_path.relative_to(root).parts)
        except ValueError:
            continue
        dirs[:] = sorted(directory for directory in dirs if directory not in EXCLUDED_DIRS
                         and _walk_entry_in_root(root, current_path / directory))
        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []
        for name in sorted(names):
            path = current_path / name
            if not _walk_entry_in_root(root, path) or name.startswith(".env") or name.endswith((".pyc", ".pyo")):
                continue
            try:
                relative_depth = len(path.relative_to(root).parts)
            except ValueError:
                continue
            if max_depth is None or relative_depth <= max_depth:
                files.append(path)
    return files


def _tree_markers(root: Path, max_depth: int | None = None, *, excluded_file: Path | None = None) -> list[str]:
    paths = _walk_files(root, root, max_depth)
    return sorted(path.relative_to(root).as_posix() for path in paths if path != excluded_file)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _optional_file_sha256(path: Path) -> str | None:
    try:
        return _file_sha256(path)
    except OSError:
        # Keep the discovered path, but do not mark unreadable contents as reused.
        return None


def _segment_hash(
    root: Path, paths: list[Path], *, excluded_file: Path | None = None,
    observed_files: dict[str, str] | None = None,
) -> str:
    entries = dict(observed_files or {})
    for path in sorted(paths, key=lambda value: value.as_posix()):
        if path == excluded_file:
            continue
        target = _contained_path(root, path)
        if target is None:
            continue
        if target.is_file():
            entries[path.relative_to(root).as_posix()] = _file_sha256(target)
        elif target.is_dir():
            directory_key = path.relative_to(root).as_posix().rstrip("/") + "/"
            entries.setdefault(directory_key, "<dir>")
            for child in _walk_files(root, path):
                if child != excluded_file:
                    entries[child.relative_to(root).as_posix()] = _file_sha256(child)
    return stable_hash(sorted(entries.items()))


def _legacy_web_manifest_hash(path: Path) -> str | None:
    try:
        data = path.read_bytes()
        payload = json.loads(data.decode("utf-8-sig"))
    except (OSError, ValueError, RecursionError):
        return None
    if not isinstance(payload, dict):
        return None

    start_url = payload.get("start_url")
    has_name = any(isinstance(payload.get(key), str) and payload[key].strip() for key in ("name", "short_name"))
    display = payload.get("display")
    icons = payload.get("icons")
    has_icon = isinstance(icons, list) and any(
        isinstance(icon, dict) and isinstance(icon.get("src"), str) and icon["src"].strip() for icon in icons
    )
    if isinstance(start_url, str) and start_url.strip() or has_name and (
        display in ("browser", "minimal-ui", "standalone", "fullscreen") or has_icon
    ):
        return hashlib.sha256(data).hexdigest()
    return None


def _pwa_evidence(root: Path, markers: list[str]) -> tuple[list[str], dict[str, str | None]]:
    paths = []
    manifest_hashes = {}
    for marker in markers:
        name = marker.rsplit("/", 1)[-1].lower()
        if not (name.endswith(".webmanifest") or name in ("manifest.json", "service-worker.js", "sw.js")):
            continue
        path = root / marker
        try:
            if path.is_symlink():
                continue
            target = path.resolve(strict=True)
            if not target.is_relative_to(root) or not target.is_file():
                continue
        except (OSError, RuntimeError):
            continue
        if name == "manifest.json":
            digest = _legacy_web_manifest_hash(target)
            if digest is None:
                continue
            manifest_hashes[marker] = digest
        elif name.endswith(".webmanifest"):
            manifest_hashes[marker] = _optional_file_sha256(target)
        paths.append(marker)
    return paths, manifest_hashes


def _package_info(root: Path) -> tuple[dict[str, str], dict[str, Any], str | None, str | None]:
    package = _contained_path(root, root / "package.json")
    scripts: dict[str, str] = {}
    dependencies: dict[str, Any] = {}
    digest = None
    if package is not None:
        data = package.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        try:
            payload = json.loads(data.decode("utf-8").removeprefix("\ufeff"))
        except json.JSONDecodeError:
            return scripts, dependencies, "invalid JSON in package.json", digest
        if not isinstance(payload, dict):
            raise ValueError("package.json must be a JSON object")
        for field in ("scripts", "dependencies", "devDependencies"):
            if field in payload and not isinstance(payload[field], dict):
                raise ValueError(f"package.json {field} must be a JSON object")
        scripts = {str(k): str(v) for k, v in payload.get("scripts", {}).items() if isinstance(k, str) and isinstance(v, str)}
        dependencies = {**payload.get("dependencies", {}), **payload.get("devDependencies", {})}

        for field in ("dependencies", "devDependencies"):
            if any(not isinstance(specification, str) for specification in payload.get(field, {}).values()):
                return scripts, dependencies, f"package.json {field} values must be strings", digest
    return scripts, dependencies, None, digest


def _package_lockfiles(root: Path) -> list[Path]:
    lockfiles = []
    for name in LOCKFILES:
        path = root / name
        target = _contained_path(root, path)
        if target is not None and target.is_file():
            lockfiles.append(path)
    return lockfiles


def _declared_snapshot(root: Path, *, excluded_file: Path | None = None) -> tuple[dict[str, Any], str]:
    key = ".engineering/context.json"
    source = root / key
    path = _contained_path(root, source)
    if path is None:
        return {"schema": "repo-context/v1", "decisions": {}, "landmarks": {}}, stable_hash([])
    data = path.read_bytes()
    # Keep universal newlines for JSON diagnostics and original bytes for the segment hash.
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    payload = load_json_with_unique_members(text, label="Repository context")
    if not isinstance(payload, dict):
        raise ValueError("repo context must be a JSON object")
    if payload.get("schema") not in (None, "repo-context/v1"):
        raise ValueError("unsupported repo context schema")
    # UTF-8 decoding covers literal text; JSON escapes can introduce an unpaired surrogate.
    if "\\u" in text:
        try:
            canonical_json(payload).encode("utf-8")
        except UnicodeEncodeError:
            raise ValueError("Repository context contains an unpaired Unicode surrogate.") from None
    landmarks = payload.get("landmarks", {})
    if not isinstance(landmarks, dict):
        raise ValueError("repo landmarks must be an object of path lists")
    valid, invalid = {}, []
    for label, paths in landmarks.items():
        if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
            raise ValueError(f"landmark {label} must contain a list of paths")
        valid[label] = []
        for value in paths:
            path = root / value
            safe = bool(value) and "\\" not in value and ":" not in value and not Path(value).is_absolute() and ".." not in Path(value).parts
            if safe and path == excluded_file:
                continue
            safe = safe and path.exists()
            safe = safe and path.resolve().is_relative_to(root)
            if safe and all(
                _walk_entry_in_root(root, part) for part in (path, *path.parents)
                if part != root and part.is_relative_to(root)
            ):
                valid[label].append(value)
            else:
                invalid.append({"label": label, "path": value, "reason": "missing-or-unsafe-path"})
    entries = [] if source == excluded_file else [(key, hashlib.sha256(data).hexdigest())]
    return {
        "schema": "repo-context/v1",
        "decisions": payload.get("decisions", {}),
        "landmarks": valid,
        "invalid_landmarks": invalid,
        "routes": payload.get("routes", {}),
    }, stable_hash(entries)


def profile_repo(
    root: Path, previous: dict | None = None, *, excluded_file: Path | None = None,
    landmark_registry: dict | None = None,
) -> dict:
    root = _repository_directory(root)
    scripts, dependencies, package_problem, package_digest = _package_info(root)
    markers = _tree_markers(root, excluded_file=excluded_file)
    lockfiles = _package_lockfiles(root)
    package_manager = LOCKFILES[lockfiles[0].name] if lockfiles else None
    persistence = _has_migration_directory(root)
    pwa_paths, runtime_file_hashes = _pwa_evidence(root, markers)
    pyproject = root / "pyproject.toml"
    if pyproject != excluded_file and not pyproject.is_symlink():
        target = _contained_path(root, pyproject)
        if target is not None and target.is_file():
            runtime_file_hashes[pyproject.name] = _optional_file_sha256(target)
    ci = any(marker.startswith(".github/workflows/") for marker in markers)
    tests = any(marker.split("/", 1)[0] in TEST_HINTS or "/tests/" in f"/{marker}/" or marker.startswith("tests/") for marker in markers)
    auth = any(key.lower() in {"@clerk/nextjs", "clerk", "next-auth", "@auth/core", "supabase", "@supabase/supabase-js"} or "auth" in key.lower() for key in dependencies)
    declared, declared_hash = _declared_snapshot(root, excluded_file=excluded_file)
    discovered_landmarks = discover_landmarks(markers, registry=landmark_registry)
    if pwa_paths:
        discovered_landmarks["pwa"] = sorted(set(discovered_landmarks.get("pwa", [])).union(pwa_paths))

    package_files = {}
    if package_digest is not None and root / "package.json" != excluded_file:
        package_files["package.json"] = package_digest
    segment_inputs = {
        "runtime": ([root / "pnpm-workspace.yaml"] if (root / "pnpm-workspace.yaml").exists() else []) + lockfiles,
        "delivery": [root / ".github/workflows"] if (root / ".github/workflows").exists() else [],
        "persistence": [root / hint for hint in MIGRATION_HINTS if (root / hint).exists()],
        "verification": [root / hint for hint in TEST_HINTS if (root / hint).exists()],
    }
    hashes = {
        key: _segment_hash(
            root, paths, excluded_file=excluded_file,
            observed_files=package_files if key in ("runtime", "verification") else None,
        )
        for key, paths in segment_inputs.items()
    }
    hashes["declared"] = declared_hash
    if runtime_file_hashes:
        hashes["runtime"] = stable_hash([hashes["runtime"], sorted(runtime_file_hashes.items())])
    hashes["discovery-tree"] = stable_hash(markers)
    previous_meta = previous.get("meta") if isinstance(previous, dict) else None
    previous_hashes = previous_meta.get("segment_hashes") if isinstance(previous_meta, dict) else None
    reused = []
    if isinstance(previous_hashes, dict):
        reused = sorted(
            key for key, value in hashes.items()
            if previous_hashes.get(key) == value and (key != "runtime" or None not in runtime_file_hashes.values())
        )
    detected = {
        "package_manager": package_manager,
        "commands": scripts,
        "capabilities": {"persistence": persistence, "pwa": bool(pwa_paths), "auth": auth},
        "delivery": {"ci": ci},
        "verification": {"tests": tests},
        "landmarks": {
            **discovered_landmarks,
            # Paths only: discovery must not copy confidential commercial facts
            # into a context profile. Declared landmarks remain authoritative.
            "commercial-context": [
                hint for hint in COMMERCIAL_CONTEXT_HINTS
                if (target := _contained_path(root, root / hint)) is not None and target.is_file()
            ],
        },
    }
    profile = {"schema": "repo-profile/v1", "detected": detected, "declared": declared, "meta": {"segment_hashes": hashes, "reused_segments": reused}}
    if package_problem:
        profile["meta"]["input_problems"] = [package_problem]
    profile["profile_hash"] = stable_hash({"detected": detected, "declared": declared, "segment_hashes": hashes})
    return profile


def write_repo_profile(root: Path, output_dir: Path) -> dict:
    root = _repository_directory(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    previous = None
    target = output_dir.resolve() / "repo.json"
    if target.exists():
        try:
            previous = load_json_with_unique_members(
                target.read_text(encoding="utf-8"),
                label="Previous repository profile",
                require_finite_numbers=False,
            )
        except ValueError:
            previous = None
    profile = profile_repo(root, previous, excluded_file=target)
    target.write_text(canonical_json(profile), encoding="utf-8")
    return profile
