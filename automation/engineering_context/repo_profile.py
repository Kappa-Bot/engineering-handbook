from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from .canonical import canonical_json, stable_hash

LOCKFILES = {"pnpm-lock.yaml":"pnpm","package-lock.json":"npm","yarn.lock":"yarn","bun.lockb":"bun"}
MIGRATION_HINTS = ("supabase/migrations", "migrations", "prisma/migrations")
TEST_HINTS = ("tests", "test", "__tests__", "e2e")
PWA_HINTS = ("manifest.webmanifest", "manifest.json", "service-worker.js", "sw.js")
EXCLUDED_DIRS = {".git", "node_modules", "dist", "build", ".next"}


def _exists_any(root: Path, hints: tuple[str, ...]) -> bool:
    return any((root / hint).exists() for hint in hints)


def _walk_files(root: Path, start: Path, max_depth: int | None = None) -> list[Path]:
    if not start.exists():
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
        dirs[:] = sorted(directory for directory in dirs if directory not in EXCLUDED_DIRS)
        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []
        for name in sorted(names):
            path = current_path / name
            try:
                relative_depth = len(path.relative_to(root).parts)
            except ValueError:
                continue
            if max_depth is None or relative_depth <= max_depth:
                files.append(path)
    return files


def _tree_markers(root: Path, max_depth: int = 4) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in _walk_files(root, root, max_depth))


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _segment_hash(root: Path, paths: list[Path]) -> str:
    entries: dict[str, str] = {}
    for path in sorted(paths, key=lambda value: value.as_posix()):
        if path.is_file():
            entries[path.relative_to(root).as_posix()] = _file_sha256(path)
        elif path.is_dir():
            directory_key = path.relative_to(root).as_posix().rstrip("/") + "/"
            entries.setdefault(directory_key, "<dir>")
            for child in _walk_files(root, path):
                entries[child.relative_to(root).as_posix()] = _file_sha256(child)
    return stable_hash(sorted(entries.items()))


def _package_info(root: Path) -> tuple[dict[str, str], dict[str, Any]]:
    package = root / "package.json"
    scripts: dict[str, str] = {}
    dependencies: dict[str, Any] = {}
    if package.exists():
        try:
            payload = json.loads(package.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
        scripts = {str(k): str(v) for k, v in payload.get("scripts", {}).items() if isinstance(k, str) and isinstance(v, str)}
        dependencies = {**payload.get("dependencies", {}), **payload.get("devDependencies", {})}
    return scripts, dependencies


def _detect_package_manager(root: Path) -> str | None:
    for lockfile, manager in LOCKFILES.items():
        if (root / lockfile).exists():
            return manager
    return None


def _declared(root: Path) -> dict[str, Any]:
    path = root / ".engineering/context.json"
    if not path.exists():
        return {"schema": "repo-context/v1", "decisions": {}, "landmarks": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") not in (None, "repo-context/v1"):
        raise ValueError("unsupported repo context schema")
    return {
        "schema": "repo-context/v1",
        "decisions": payload.get("decisions", {}),
        "landmarks": payload.get("landmarks", {}),
        "routes": payload.get("routes", {}),
    }


def profile_repo(root: Path, previous: dict | None = None) -> dict:
    root = root.resolve()
    scripts, dependencies = _package_info(root)
    markers = _tree_markers(root)
    package_manager = _detect_package_manager(root)
    persistence = _exists_any(root, MIGRATION_HINTS)
    pwa = any(any(marker.endswith(hint) or marker == hint for hint in PWA_HINTS) for marker in markers)
    ci = any(marker.startswith(".github/workflows/") for marker in markers)
    tests = any(marker.split("/", 1)[0] in TEST_HINTS or "/tests/" in f"/{marker}/" or marker.startswith("tests/") for marker in markers)
    auth = any(key.lower() in {"@clerk/nextjs", "clerk", "next-auth", "@auth/core", "supabase", "@supabase/supabase-js"} or "auth" in key.lower() for key in dependencies)
    declared = _declared(root)

    segment_inputs = {
        "runtime": [path for path in [root / "package.json", *(root / name for name in LOCKFILES)] if path.exists()],
        "delivery": [root / ".github/workflows"] if (root / ".github/workflows").exists() else [],
        "persistence": [root / hint for hint in MIGRATION_HINTS if (root / hint).exists()],
        "verification": [root / hint for hint in TEST_HINTS if (root / hint).exists()] + ([root / "package.json"] if (root / "package.json").exists() else []),
        "declared": [root / ".engineering/context.json"] if (root / ".engineering/context.json").exists() else [],
    }
    hashes = {key: _segment_hash(root, value) for key, value in segment_inputs.items()}
    previous_hashes = ((previous or {}).get("meta") or {}).get("segment_hashes", {})
    reused = sorted(key for key, value in hashes.items() if previous_hashes.get(key) == value)
    detected = {
        "package_manager": package_manager,
        "commands": scripts,
        "capabilities": {"persistence": persistence, "pwa": pwa, "auth": auth},
        "delivery": {"ci": ci},
        "verification": {"tests": tests},
        "landmarks": {
            "migrations": [hint for hint in MIGRATION_HINTS if (root / hint).exists()],
            "tests": [hint for hint in TEST_HINTS if (root / hint).exists()],
            "ci": [".github/workflows"] if ci else [],
        },
    }
    profile = {"schema": "repo-profile/v1", "detected": detected, "declared": declared, "meta": {"segment_hashes": hashes, "reused_segments": reused}}
    profile["profile_hash"] = stable_hash({"detected": detected, "declared": declared, "segment_hashes": hashes})
    return profile


def write_repo_profile(root: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    previous = None
    target = output_dir / "repo.json"
    if target.exists():
        try:
            previous = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = None
    profile = profile_repo(root, previous)
    target.write_text(canonical_json(profile), encoding="utf-8")
    return profile
