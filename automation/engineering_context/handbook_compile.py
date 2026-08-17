from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import tempfile
from typing import Any

from .canonical import canonical_json, estimate_tokens, stable_hash, sha256_text
from .handbook_source import AgentContextError, KnowledgeUnit, extract_agent_context, extract_source_id

COMPILED_SCHEMA = "handbook-compiled/v1"
COMPILER_SCHEMA = 1
OUTPUT_FILES = ("manifest.json", "graph.json", "routing.json", "planning.json", "implementation.json", "verification.json")
CANONICAL_DIRS = ("governance", "policies", "standards", "patterns", "playbooks", "references")


@dataclass(frozen=True)
class CompileResult:
    changed_files: tuple[str, ...]
    skipped_sources: tuple[str, ...]
    handbook_hash: str


def _discover_markdown(root: Path) -> list[Path]:
    roots = [root / name for name in CANONICAL_DIRS if (root / name).is_dir()]
    if not roots:
        roots = [root]
    files: list[Path] = []
    for base in roots:
        files.extend(p for p in base.rglob("*.md") if "machine-readable/compiled" not in p.as_posix())
    return sorted(set(files), key=lambda p: p.relative_to(root).as_posix())


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _previous_units(output_dir: Path) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for name in ("planning.json", "implementation.json", "verification.json"):
        payload = _load_json(output_dir / name, {})
        for unit in payload.get("units", []) if isinstance(payload, dict) else []:
            existing = merged.get(unit.get("id"))
            if existing is None:
                merged[unit["id"]] = unit
            else:
                sources = sorted(set(existing.get("sources", [])) | set(unit.get("sources", [])))
                existing["sources"] = sources
    return merged


def _unit_record(unit: KnowledgeUnit) -> dict[str, Any]:
    record = unit.as_dict()
    record["estimated_tokens"] = estimate_tokens(unit.text)
    return record


def _phase_match(unit: dict[str, Any], phase: str) -> bool:
    phases = unit.get("phase", [])
    return not phases or phase in phases


def compile_handbook(root: Path, output_dir: Path) -> CompileResult:
    root = root.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    previous_manifest = _load_json(output_dir / "manifest.json", {})
    previous_sources = previous_manifest.get("sources", {}) if isinstance(previous_manifest, dict) else {}
    prev_units = _previous_units(output_dir)

    units_by_source: dict[str, list[dict[str, Any]]] = {}
    source_meta: dict[str, dict[str, Any]] = {}
    skipped: list[str] = []

    for path in _discover_markdown(root):
        text = path.read_text(encoding="utf-8")
        if "```json agent-context" not in text:
            continue
        rel = path.relative_to(root).as_posix()
        source_id = extract_source_id(text)
        source_hash = sha256_text(text)
        prev = previous_sources.get(source_id, {}) if isinstance(previous_sources, dict) else {}
        can_reuse = prev.get("source_hash") == source_hash and prev.get("compiler_schema", COMPILER_SCHEMA) == COMPILER_SCHEMA
        reused: list[dict[str, Any]] = []
        if can_reuse:
            ids = prev.get("unit_ids", [])
            if ids and all(uid in prev_units for uid in ids):
                reused = [dict(prev_units[uid]) for uid in ids]
        if reused:
            units_by_source[source_id] = reused
            skipped.append(source_id)
        else:
            parsed = extract_agent_context(text, rel)
            units_by_source[source_id] = [_unit_record(unit) for unit in parsed]
        source_meta[source_id] = {"path": rel, "source_hash": source_hash}

    all_units: dict[str, dict[str, Any]] = {}
    for source_id in sorted(units_by_source):
        for unit in units_by_source[source_id]:
            uid = unit["id"]
            if uid in all_units:
                raise AgentContextError(f"duplicate global unit id {uid}")
            record = dict(unit)
            record["source"] = source_id
            record["sources"] = sorted(set(record.get("sources", [source_id])))
            record["covers"] = sorted(set(record.get("covers", [])))
            record["activate_when"] = sorted(set(record.get("activate_when", [])))
            record["phase"] = sorted(set(record.get("phase", [])))
            record["requires"] = sorted(set(record.get("requires", [])))
            record["excludes"] = sorted(set(record.get("excludes", [])))
            record["estimated_tokens"] = int(record.get("estimated_tokens", estimate_tokens(record.get("text", ""))))
            all_units[uid] = record

    for unit in all_units.values():
        missing = [uid for uid in unit.get("requires", []) if uid not in all_units]
        if missing:
            raise AgentContextError(f"unit {unit['id']} requires unknown units: {', '.join(missing)}")

    graph = {uid: all_units[uid].get("requires", []) for uid in sorted(all_units) if all_units[uid].get("requires")}
    routing: dict[str, list[str]] = {}
    for uid in sorted(all_units):
        for predicate in all_units[uid].get("activate_when", []):
            routing.setdefault(predicate, []).append(uid)
    routing = {key: sorted(value) for key, value in sorted(routing.items())}

    for source_id, units in units_by_source.items():
        req_records: list[dict[str, Any]] = []
        for unit in units:
            for req in unit.get("requires", []):
                if req in all_units:
                    req_records.append(all_units[req])
        dependency_hash = stable_hash(req_records)
        unit_records = [all_units[u["id"]] for u in units]
        output_hash = stable_hash(unit_records)
        source_meta[source_id].update({
            "compiler_schema": COMPILER_SCHEMA,
            "dependency_hash": dependency_hash,
            "output_hash": output_hash,
            "unit_ids": sorted(u["id"] for u in units),
        })

    handbook_hash = stable_hash({sid: meta["output_hash"] for sid, meta in sorted(source_meta.items())})
    manifest = {
        "schema": COMPILED_SCHEMA,
        "compiler_schema": COMPILER_SCHEMA,
        "handbook_hash": handbook_hash,
        "sources": {sid: source_meta[sid] for sid in sorted(source_meta)},
    }
    payloads: dict[str, Any] = {
        "manifest.json": manifest,
        "graph.json": {"schema": COMPILED_SCHEMA, "edges": graph},
        "routing.json": routing,
        "planning.json": {"schema": COMPILED_SCHEMA, "units": [all_units[uid] for uid in sorted(all_units) if _phase_match(all_units[uid], "planning")]},
        "implementation.json": {"schema": COMPILED_SCHEMA, "units": [all_units[uid] for uid in sorted(all_units) if _phase_match(all_units[uid], "implementation")]},
        "verification.json": {"schema": COMPILED_SCHEMA, "units": [all_units[uid] for uid in sorted(all_units) if _phase_match(all_units[uid], "verification")]},
    }

    changed: list[str] = []
    for filename in OUTPUT_FILES:
        target = output_dir / filename
        new_text = canonical_json(payloads[filename])
        old_text = target.read_text(encoding="utf-8") if target.exists() else None
        if old_text != new_text:
            target.write_text(new_text, encoding="utf-8")
            changed.append(filename)

    return CompileResult(tuple(changed), tuple(sorted(skipped)), handbook_hash)


def check_compiled_fresh(root: Path, output_dir: Path) -> list[str]:
    root = root.resolve()
    output_dir = output_dir.resolve()
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "compiled"
        compile_handbook(root, temp_out)
        problems: list[str] = []
        for filename in OUTPUT_FILES:
            actual = output_dir / filename
            expected = temp_out / filename
            if not actual.exists():
                problems.append(f"missing {actual}")
            elif actual.read_bytes() != expected.read_bytes():
                problems.append(f"stale {actual}")
        return problems


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    result = compile_handbook(args.root, args.output)
    print(json.dumps({"changed_files": list(result.changed_files), "skipped_sources": list(result.skipped_sources), "handbook_hash": result.handbook_hash}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
