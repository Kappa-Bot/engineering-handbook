from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canonical import canonical_json, stable_hash

LOCKFILES = {"pnpm-lock.yaml":"pnpm","package-lock.json":"npm","yarn.lock":"yarn","bun.lockb":"bun"}
MIGRATION_HINTS = ("supabase/migrations", "migrations", "prisma/migrations")
TEST_HINTS = ("tests", "test", "__tests__", "e2e")
PWA_HINTS = ("manifest.webmanifest", "manifest.json", "service-worker.js", "sw.js")


def _exists_any(root: Path, hints: tuple[str, ...]) -> bool:
    return any((root / hint).exists() for hint in hints)


def _tree_markers(root: Path, max_depth: int = 4) -> list[str]:
    markers: list[str] = []
    if not root.exists():
        return markers
    for path in root.rglob("*"):
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if len(rel.parts) > max_depth:
            continue
        if any(part in {".git", "node_modules", "dist", "build", ".next"} for part in rel.parts):
            continue
        if path.is_file():
            markers.append(rel.as_posix())
    return sorted(markers)


def _segment_hash(root: Path, paths: list[Path]) -> str:
    entries = []
    for path in sorted(paths, key=lambda value: value.as_posix()):
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = f"<binary:{path.stat().st_size}>"
            entries.append((path.relative_to(root).as_posix(), content))
        elif path.is_dir():
            entries.append((path.relative_to(root).as_posix(), [item.relative_to(root).as_posix() for item in path.rglob("*") if item.is_file()]))
    return stable_hash(entries)


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
