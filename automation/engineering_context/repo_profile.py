from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from .canonical import canonical_json, stable_hash
from .discovery_rules import discover_landmarks

LOCKFILES = {"pnpm-lock.yaml":"pnpm","package-lock.json":"npm","yarn.lock":"yarn","bun.lockb":"bun"}
MIGRATION_HINTS = ("supabase/migrations", "migrations", "prisma/migrations")
TEST_HINTS = ("tests", "test", "__tests__", "e2e")
PWA_HINTS = ("manifest.webmanifest", "manifest.json", "service-worker.js", "sw.js")
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


def _exists_any(root: Path, hints: tuple[str, ...]) -> bool:
    return any((root / hint).exists() for hint in hints)


def _walk_files(root: Path, start: Path, max_depth: int | None = None) -> list[Path]:
    if not start.exists() or start.is_symlink():
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
        dirs[:] = sorted(directory for directory in dirs if directory not in EXCLUDED_DIRS and not (current_path / directory).is_symlink())
        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []
        for name in sorted(names):
            path = current_path / name
            if path.is_symlink() or name.startswith(".env") or name.endswith((".pyc", ".pyo")):
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


def _segment_hash(root: Path, paths: list[Path], *, excluded_file: Path | None = None) -> str:
    entries: dict[str, str] = {}
    for path in sorted(paths, key=lambda value: value.as_posix()):
        if path == excluded_file:
            continue
        if path.is_file():
            entries[path.relative_to(root).as_posix()] = _file_sha256(path)
        elif path.is_dir():
            directory_key = path.relative_to(root).as_posix().rstrip("/") + "/"
            entries.setdefault(directory_key, "<dir>")
            for child in _walk_files(root, path):
                if child != excluded_file:
                    entries[child.relative_to(root).as_posix()] = _file_sha256(child)
    return stable_hash(sorted(entries.items()))


def _package_info(root: Path) -> tuple[dict[str, str], dict[str, Any]]:
    package = root / "package.json"
    scripts: dict[str, str] = {}
    dependencies: dict[str, Any] = {}
    if package.exists():
        try:
            payload = json.loads(package.read_text(encoding="utf-8").removeprefix("\ufeff"))
        except json.JSONDecodeError:
            payload = {}
        if not isinstance(payload, dict):
            raise ValueError("package.json must be a JSON object")
        for field in ("scripts", "dependencies", "devDependencies"):
            if field in payload and not isinstance(payload[field], dict):
                raise ValueError(f"package.json {field} must be a JSON object")
        scripts = {str(k): str(v) for k, v in payload.get("scripts", {}).items() if isinstance(k, str) and isinstance(v, str)}
        dependencies = {**payload.get("dependencies", {}), **payload.get("devDependencies", {})}
    return scripts, dependencies


def _detect_package_manager(root: Path) -> str | None:
    for lockfile, manager in LOCKFILES.items():
        if (root / lockfile).exists():
            return manager
    return None


def _declared(root: Path, *, excluded_file: Path | None = None) -> dict[str, Any]:
    path = root / ".engineering/context.json"
    if not path.exists():
        return {"schema": "repo-context/v1", "decisions": {}, "landmarks": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("repo context must be a JSON object")
    if payload.get("schema") not in (None, "repo-context/v1"):
        raise ValueError("unsupported repo context schema")
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
            if safe and not any(part.is_symlink() for part in [path, *path.parents] if part != root and part.is_relative_to(root)):
                valid[label].append(value)
            else:
                invalid.append({"label": label, "path": value, "reason": "missing-or-unsafe-path"})
    return {
        "schema": "repo-context/v1",
        "decisions": payload.get("decisions", {}),
        "landmarks": valid,
        "invalid_landmarks": invalid,
        "routes": payload.get("routes", {}),
    }


def profile_repo(root: Path, previous: dict | None = None, *, excluded_file: Path | None = None) -> dict:
    root = _repository_directory(root)
    scripts, dependencies = _package_info(root)
    markers = _tree_markers(root, excluded_file=excluded_file)
    package_manager = _detect_package_manager(root)
    persistence = _exists_any(root, MIGRATION_HINTS)
    pwa = any(any(marker.endswith(hint) or marker == hint for hint in PWA_HINTS) for marker in markers)
    ci = any(marker.startswith(".github/workflows/") for marker in markers)
    tests = any(marker.split("/", 1)[0] in TEST_HINTS or "/tests/" in f"/{marker}/" or marker.startswith("tests/") for marker in markers)
    auth = any(key.lower() in {"@clerk/nextjs", "clerk", "next-auth", "@auth/core", "supabase", "@supabase/supabase-js"} or "auth" in key.lower() for key in dependencies)
    declared = _declared(root, excluded_file=excluded_file)
    discovered_landmarks = discover_landmarks(markers)

    segment_inputs = {
        "runtime": [path for path in [root / "package.json", root / "pnpm-workspace.yaml", *(root / name for name in LOCKFILES)] if path.exists()],
        "delivery": [root / ".github/workflows"] if (root / ".github/workflows").exists() else [],
        "persistence": [root / hint for hint in MIGRATION_HINTS if (root / hint).exists()],
        "verification": [root / hint for hint in TEST_HINTS if (root / hint).exists()] + ([root / "package.json"] if (root / "package.json").exists() else []),
        "declared": [root / ".engineering/context.json"] if (root / ".engineering/context.json").exists() else [],
    }
    hashes = {key: _segment_hash(root, paths, excluded_file=excluded_file) for key, paths in segment_inputs.items()}
    hashes["discovery-tree"] = stable_hash(markers)
    previous_hashes = ((previous or {}).get("meta") or {}).get("segment_hashes", {})
    reused = sorted(key for key, value in hashes.items() if previous_hashes.get(key) == value)
    detected = {
        "package_manager": package_manager,
        "commands": scripts,
        "capabilities": {"persistence": persistence, "pwa": pwa, "auth": auth},
        "delivery": {"ci": ci},
        "verification": {"tests": tests},
        "landmarks": {
            **discovered_landmarks,
            # Paths only: discovery must not copy confidential commercial facts
            # into a context profile. Declared landmarks remain authoritative.
            "commercial-context": [hint for hint in COMMERCIAL_CONTEXT_HINTS if (root / hint).is_file()],
        },
    }
    profile = {"schema": "repo-profile/v1", "detected": detected, "declared": declared, "meta": {"segment_hashes": hashes, "reused_segments": reused}}
    profile["profile_hash"] = stable_hash({"detected": detected, "declared": declared, "segment_hashes": hashes})
    return profile


def write_repo_profile(root: Path, output_dir: Path) -> dict:
    root = _repository_directory(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    previous = None
    target = output_dir.resolve() / "repo.json"
    if target.exists():
        try:
            previous = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = None
    profile = profile_repo(root, previous, excluded_file=target)
    target.write_text(canonical_json(profile), encoding="utf-8")
    return profile
