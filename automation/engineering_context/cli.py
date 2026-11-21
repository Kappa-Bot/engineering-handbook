from __future__ import annotations

import argparse
import codecs
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import tempfile

from .canonical import canonical_json, stable_hash
from .context_solver import build_repo_route, solve_context
from .handbook_compile import COMPILED_SCHEMA, OUTPUT_FILES, _compare_compiled, check_compiled_fresh, compile_handbook
from .planning_ir import ValidationIssue, capsule_delta, new_planning_ir, planning_ir_from_dict, validate_planning_ir
from .repo_profile import InvalidRepositoryRoot, profile_repo, write_repo_profile
from .task_descriptor import describe_task
from .discovery import SCHEMA as DISCOVERY_SCHEMA, check_integrity, knowledge_tree, search
from .discovery_rules import load_registry
from .visual_directions import CATALOG_PATH as VISUAL_CATALOG_PATH, load_visual_catalog, resolve_visual_direction

MODE_TO_PHASE = {"plan": "planning", "implement": "implementation", "verify": "verification"}
ROUTING_REGISTRIES = ("rules.v1.json", "landmarks.v1.json", "routes.v1.json")
# The portable CLI has no dependency on the checkout-only bootstrap.
SKILL_SOURCE = "agent-config/codex/skills/engineering-handbook/SKILL.md"
SKILL_REPOSITORY = "Kappa-Bot/engineering-handbook"
SKILL_REMOTE = f"https://github.com/{SKILL_REPOSITORY}.git"
BUNDLE_FILE_LIMIT = 16 * 1024 * 1024


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _local_file(root: Path, relative: str) -> Path | None:
    path = Path(relative)
    if not path.parts or path.anchor or ".." in path.parts or "\\" in relative or ":" in relative:
        return None
    target = root
    try:
        for part in path.parts:
            target = target / part
            info = target.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                return None
    except (OSError, ValueError):
        return None
    return target if stat.S_ISREG(info.st_mode) else None


def _relocated_skill(root: Path) -> bool:
    if root.name != "references":
        return False
    manifest_file = _local_file(root.parent, "install-manifest.json")
    skill = _local_file(root.parent, "SKILL.md")
    if manifest_file is None or skill is None:
        return False
    try:
        if max(manifest_file.stat().st_size, skill.stat().st_size) > BUNDLE_FILE_LIMIT:
            return False
        manifest = _read_json(manifest_file)
        if not isinstance(manifest, dict) or manifest.get("skill_name") != "engineering-handbook":
            return False
        version = manifest.get("schema_version")
        repository = manifest.get("source_repository")
        if type(version) is not int or version not in (1, 2):
            return False
        if version == 1 and repository not in (SKILL_REPOSITORY, SKILL_REMOTE):
            return False
        if version == 2:
            revision = manifest.get("revision")
            if (repository != SKILL_REMOTE or type(manifest.get("bootstrap_api")) is not int
                    or manifest["bootstrap_api"] != 2 or not isinstance(revision, str)
                    or not re.fullmatch(r"[0-9a-f]{40}", revision)):
                return False
        files = manifest.get("files")
        if not isinstance(files, list) or not all(
            isinstance(row, dict) and all(isinstance(row.get(key), str) for key in ("install_path", "source_path", "sha256"))
            for row in files
        ):
            return False
        entries = [row for row in files if row["install_path"].casefold() == "skill.md"
                   or row["source_path"].casefold() == SKILL_SOURCE.casefold()]
        return len(entries) == 1 and entries[0] == {
            "source_path": SKILL_SOURCE, "install_path": "SKILL.md",
            "sha256": hashlib.sha256(skill.read_bytes()).hexdigest(),
        }
    except (OSError, ValueError, RecursionError):
        return False


def _ranked_reading(root: Path, index: dict, query: str, *, limit: int = 8, historical: bool = False) -> list[dict]:
    hits = search(index, query, limit=limit, historical=historical)
    root = root.resolve()
    for hit in hits:
        path = hit["path"]
        if _local_file(root, path) is not None:
            availability = {"status": "present", "relative_to": "handbook-root", "path": path}
        elif path == SKILL_SOURCE and _relocated_skill(root):
            availability = {"status": "relocated", "relative_to": "skill-root", "path": "SKILL.md"}
        else:
            availability = {"status": "unavailable"}
        hit["local_availability"] = availability
    return hits


def _load_compiled(path: Path, phase: str) -> dict:
    if phase not in {"planning", "implementation", "verification"}:
        raise ValueError(f"invalid compiled phase {phase}")
    view = _read_json(path / f"{phase}.json")
    routing = _read_json(path / "routing.json")
    manifest = _read_json(path / "manifest.json")
    if not isinstance(view, dict) or view.get("schema") != COMPILED_SCHEMA or not isinstance(view.get("units"), list):
        raise ValueError(f"invalid compiled phase artifact: {phase}.json")
    if not isinstance(routing, dict) or not all(isinstance(key, str) and isinstance(value, list) and all(isinstance(uid, str) for uid in value) for key, value in routing.items()):
        raise ValueError("invalid compiled routing artifact")
    if not isinstance(manifest, dict) or manifest.get("schema") != COMPILED_SCHEMA or not isinstance(manifest.get("handbook_hash"), str) or not manifest.get("handbook_hash"):
        raise ValueError("invalid compiled manifest artifact")
    return {"units": view["units"], "routing": routing, "handbook_hash": manifest["handbook_hash"]}


def _emit(payload: dict, pretty: bool = False):
    encoding = getattr(sys.stdout, "encoding", None)
    ascii_only = encoding is not None and codecs.lookup(encoding).name != "utf-8"
    if not pretty and not ascii_only:
        sys.stdout.write(canonical_json(payload))
        return
    # Escapes keep the JSON readable across legacy ASCII-compatible pipes.
    indent = 2 if pretty else None
    separators = None if pretty else (",", ":")
    print(json.dumps(payload, sort_keys=True, indent=indent, separators=separators, ensure_ascii=ascii_only))


def cmd_compile(args) -> int:
    result = compile_handbook(args.root, args.output)
    _emit({"changed_files": list(result.changed_files), "skipped_sources": list(result.skipped_sources), "handbook_hash": result.handbook_hash}, args.pretty)
    return 0


def cmd_profile(args) -> int:
    profile = write_repo_profile(args.repo, args.output) if args.output else profile_repo(args.repo)
    _emit(profile, args.pretty)
    return 0


def _read_base_context(path: Path) -> tuple[str, set[str], dict[str, dict]]:
    base = _read_json(path)
    if not isinstance(base, dict):
        raise ValueError("base context must be a JSON object")
    capsule = base.get("capsule")
    if capsule is None:
        capsule = base
    if not isinstance(capsule, dict):
        raise ValueError("base context capsule must be a JSON object")

    context_ids = [base[key] for key in ("context_id", "id") if key in base]
    if capsule is not base and "id" in capsule:
        context_ids.append(capsule["id"])
    if not context_ids or any(not isinstance(value, str) or not value.strip() for value in context_ids):
        raise ValueError("base context requires a nonempty string ID")
    if len(set(context_ids)) != 1:
        raise ValueError("base context ID does not match its capsule")
    base_id = context_ids[0]

    raw_ids = base.get("unit_ids", [])
    if not isinstance(raw_ids, list) or not all(isinstance(uid, str) and uid for uid in raw_ids):
        raise ValueError("base context unit_ids must be an array of nonempty strings")
    unit_ids = set(raw_ids)
    previous_units = {}
    if "units" not in capsule:
        if "unit_ids" not in base:
            raise ValueError("base context requires capsule units or a unit_ids array")
        return base_id, unit_ids, previous_units

    raw_units = capsule["units"]
    if not isinstance(raw_units, list):
        raise ValueError("base context units must be an array of records")
    for unit in raw_units:
        if not isinstance(unit, dict) or not isinstance(unit.get("id"), str) or not unit["id"]:
            raise ValueError("base context unit records require nonempty string IDs")
        uid = unit["id"]
        if uid in previous_units and canonical_json(previous_units[uid]) != canonical_json(unit):
            raise ValueError(f"base context has conflicting records for unit {uid}")
        previous_units[uid] = unit
    if unit_ids and unit_ids != previous_units.keys():
        raise ValueError("base context unit_ids do not match its capsule units")
    return base_id, set(previous_units), previous_units


def _checked_routing_registries(index: dict, names: tuple[str, ...] = ROUTING_REGISTRIES) -> dict[str, dict]:
    verified_hashes = index["registry_hashes"]
    checked = {}
    for name in names:
        expected = verified_hashes.get(name)
        if expected is None:
            path = f"machine-readable/discovery/{name}"
            if any(document["path"] == path for document in index["documents"]):
                raise RuntimeError(f"{name} is missing from the selected Handbook routing registries.")
            # Minimal corpora can use executing defaults for undeclared registries.
        registry = load_registry(name)
        if expected is not None and (
            expected != stable_hash(registry)
            or (name == "routes.v1.json" and index["route_order"] != list(registry["routes"]))
        ):
            raise RuntimeError(
                f"{name} differs from the selected Handbook routing registry. "
                "Run this command from the selected Handbook root."
            )
        checked[name] = registry
    return checked


def _selected_visual_catalog(root: Path, index: dict) -> dict | None:
    for document in index["documents"]:
        if document["path"] == VISUAL_CATALOG_PATH.as_posix():
            source_hash = document.get("source_hash")
            if not isinstance(source_hash, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", source_hash):
                raise RuntimeError("Recompile the selected Handbook to bind its declared visual catalog.")
            return load_visual_catalog(root, expected_source_hash=source_hash)
    # Catalog-free or undeclared fixtures retain the executing runtime default.
    return None


def cmd_context(args) -> int:
    phase = MODE_TO_PHASE[args.mode]
    compiled_dir = args.handbook.resolve()
    canonical_root = compiled_dir.parent.parent
    freshness_problems = check_compiled_fresh(canonical_root, compiled_dir)
    if freshness_problems:
        raise RuntimeError("compiled handbook context is stale: " + "; ".join(freshness_problems))
    index = _read_json(compiled_dir / "discovery.json")
    routes = _checked_routing_registries(index)["routes.v1.json"]["routes"]
    compiled = _load_compiled(compiled_dir, phase)
    profile = profile_repo(args.repo)
    descriptor = describe_task(
        args.task, profile, tuple(args.changed or ()), visual_catalog=_selected_visual_catalog(canonical_root, index),
    )
    capsule = solve_context(compiled, descriptor, phase)
    route = build_repo_route(profile, descriptor, routes=routes)
    ir = new_planning_ir(descriptor, capsule)
    capsule_dict = capsule.to_dict()
    if args.base_context:
        base_id, unit_ids, previous_units = _read_base_context(args.base_context)
        capsule_dict["delta"] = capsule_delta(base_id, unit_ids, capsule, previous_units=previous_units)
    payload = {"schema": "agent-context/v1", "mode": args.mode, "context_id": capsule.id, "descriptor": descriptor.to_dict(), "repo_route": route, "capsule": capsule_dict, "uncertain": [dict(item) for item in descriptor.uncertain], "planning_ir_seed": ir.to_dict()}
    payload["discovery"] = {"index_hash": index["index_hash"], "suggested_reading": _ranked_reading(canonical_root, index, args.task, limit=5), "absence_of_matches_is_not_clearance": True}
    if args.metrics:
        payload["metrics"] = {
            "candidate_units": capsule.candidate_count,
            "selected_units": len(capsule.units),
            "estimated_tokens": capsule.estimated_tokens,
            "estimated_tokens_scope": "selected-unit-text",
            "canonical_capsule_utf8_bytes": len(canonical_json(capsule_dict).encode("utf-8")),
            "full_source_reads": 0,
            "full_source_reads_scope": "capsule",
            "freshness_verification": "local_recompile",
            "uncovered_required": len(capsule.uncovered),
            "repo_profile_segment_reuse": len(profile.get("meta", {}).get("reused_segments", [])),
            "context_delta": capsule_dict.get("delta", {}).get("unchanged_unit_count", 0),
        }
    _emit(payload, args.pretty)
    return 0


def cmd_validate(args) -> int:
    try:
        ir = planning_ir_from_dict(_read_json(args.input))
    except ValueError as exc:
        issues = (ValidationIssue("invalid-planning-ir-shape", str(exc)),)
    else:
        issues = validate_planning_ir(ir)
    _emit({"valid": not issues, "issues": [{"code": issue.code, "message": issue.message, "severity": issue.severity} for issue in issues]}, args.pretty)
    return 0 if not issues else 1


def cmd_check(args) -> int:
    root = args.root.resolve(); output = root / "machine-readable/compiled"; problems: list[str] = []
    try:
        with tempfile.TemporaryDirectory() as tmp:
            temp_output = Path(tmp) / "compiled"
            compile_handbook(root, temp_output)
            snapshot = {name: (temp_output / name).read_bytes() for name in OUTPUT_FILES}
            second = compile_handbook(root, temp_output)
            if second.changed_files:
                problems.append("compiled output is not byte-stable on second compile")
            if snapshot != {name: (temp_output / name).read_bytes() for name in OUTPUT_FILES}:
                problems.append("compiled output changed without source changes")
        problems.extend(_compare_compiled(output, snapshot.items()))
    except Exception as exc:
        problems.append(str(exc))
    _emit({"ok": not problems, "problems": problems}, args.pretty)
    return 0 if not problems else 1


def _discovery_index(root: Path) -> dict:
    problems = check_compiled_fresh(root, root / "machine-readable/compiled")
    if problems:
        raise RuntimeError("stale discovery index: " + "; ".join(problems))
    index = _read_json(root / "machine-readable/compiled/discovery.json")
    if index.get("schema") != DISCOVERY_SCHEMA:
        raise ValueError("unsupported discovery index")
    return index


def cmd_search(args) -> int:
    index = _discovery_index(args.root)
    results = _ranked_reading(args.root, index, args.query, limit=args.limit, historical=args.historical)
    _emit({"query": args.query, "results": results, "status": "found" if results else "no-match-needs-discovery", "index_hash": index["index_hash"]}, args.pretty)
    return 0


def cmd_tree(args) -> int:
    index = _discovery_index(args.root)
    if args.kind == "knowledge":
        result = knowledge_tree(index, historical=args.historical)
    elif args.kind == "execution":
        routes = _checked_routing_registries(index, ("routes.v1.json",))["routes.v1.json"]["routes"]
        types = {"trigger", "predicate", "context-unit"}
        nodes = [n for n in index["nodes"] if n["type"] in types]
        ids = {node["id"] for node in nodes}
        result = {"kind": "execution", "nodes": nodes, "edges": [e for e in index["edges"] if e["from"] in ids and e["to"] in ids], "routes": routes, "route_order": list(routes)}
    else:
        if args.repo is None:
            raise ValueError("repository tree requires --repo")
        routes = _checked_routing_registries(index)["routes.v1.json"]["routes"]
        profile = profile_repo(args.repo)
        descriptor = describe_task(
            args.task or "", profile, visual_catalog=_selected_visual_catalog(args.root, index),
        )
        result = {"kind": "repository", "landmarks": profile["detected"]["landmarks"], "task_route": build_repo_route(profile, descriptor, routes=routes), "profile_hash": profile["profile_hash"]}
    _emit(result, args.pretty)
    return 0


def cmd_explain(args) -> int:
    index = _discovery_index(args.root)
    routes = _checked_routing_registries(index)["routes.v1.json"]["routes"]
    phase = MODE_TO_PHASE[args.mode]
    profile = profile_repo(args.repo)
    descriptor = describe_task(
        args.task, profile, tuple(args.changed), visual_catalog=_selected_visual_catalog(args.root, index),
    )
    compiled = _load_compiled(args.root / "machine-readable/compiled", phase)
    capsule = solve_context(compiled, descriptor, phase)
    selected = {unit["id"] for unit in capsule.units}
    tags = descriptor.predicates()
    decisions = []
    for unit in compiled["units"]:
        any_tags = set(unit.get("activate_when", []))
        all_tags = set(unit.get("activate_all", []))
        exclusion = sorted(set(unit.get("excludes", [])) & tags)
        missing = sorted(all_tags - tags)
        if unit["id"] in selected:
            reason = "mandatory-or-direct-risk-coverage-or-required-dependency"
        elif exclusion:
            reason = "excluded-by-task-predicate"
        elif missing or (any_tags and not any_tags & tags):
            reason = "trigger-not-satisfied"
        else:
            reason = "not-needed-for-current-minimum-coverage-or-budget"
        decisions.append({"id": unit["id"], "source": unit["source"], "selected": unit["id"] in selected, "reason": reason,
                          "matched": sorted((any_tags | all_tags) & tags), "missing_all": missing, "excluded_by": exclusion})
    _emit({"schema": "discovery-explanation/v1", "descriptor": descriptor.to_dict(), "rules": list(descriptor.evidence),
           "unit_decisions": decisions, "phase_scope": phase, "capsule": capsule.to_dict(), "repo_route": build_repo_route(profile, descriptor, routes=routes),
           "reading": _ranked_reading(args.root, index, args.task), "authority": "classification is evidence, not permission to modify, spawn or release"}, args.pretty)
    return 0


def cmd_doctor(args) -> int:
    problems = []
    try:
        index = _discovery_index(args.root)
        runtime = _read_json(args.root / "machine-readable/agent-runtime-routing.v1.json")
        if any(route.get("model") == "gpt-6-luna" for route in runtime["model_routing"]["routes"]):
            problems.append("blocked model remains in active route")
        if args.repo:
            _checked_routing_registries(index, ("landmarks.v1.json",))
            profile = profile_repo(args.repo)
            problems.extend("invalid landmark: " + item["path"] for item in profile["declared"].get("invalid_landmarks", []))
        counts = {"catalog_documents": len(index["documents"]), "graph_nodes": len(index["nodes"]), "typed_edges": len(index["edges"])}
    except (ValueError, OSError, KeyError, RuntimeError) as exc:
        problems.append(str(exc)); counts = {}
    _emit({"ok": not problems, "problems": problems, "counts": counts, "scope": "local configuration and discovery; no remote access, model availability or workstation adoption claim"}, args.pretty)
    return 0 if not problems else 1


def cmd_integrity(args) -> int:
    problems = check_integrity(args.root)
    _emit({"ok": not problems, "problems": problems, "scope": "canonical-repository"}, args.pretty)
    return 0 if not problems else 1


def cmd_visual_directions(args) -> int:
    if args.style is not None or args.local_style is not None or args.surface is not None:
        if args.surface is None:
            raise ValueError("--surface is required when resolving a visual direction")
        payload = resolve_visual_direction(args.root, args.surface, args.style, args.local_style)
    else:
        catalog = load_visual_catalog(args.root)
        payload = {"schema": catalog["schema"], "directions": catalog["directions"], "default_by_surface": catalog["default_by_surface"],
                   "runtime_user_toggle": False, "authorizes_ui_change": False}
    _emit(payload, args.pretty)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="engineering-context", description="Deterministic Engineering Handbook context compiler and agent runtime router")
    sub = parser.add_subparsers(dest="command", required=True)
    compile_cmd = sub.add_parser("compile-handbook"); compile_cmd.add_argument("--root", type=Path, required=True); compile_cmd.add_argument("--output", type=Path, required=True); compile_cmd.add_argument("--pretty", action="store_true"); compile_cmd.set_defaults(func=cmd_compile)
    profile_cmd = sub.add_parser("profile-repo"); profile_cmd.add_argument("--repo", type=Path, required=True); profile_cmd.add_argument("--output", type=Path); profile_cmd.add_argument("--pretty", action="store_true"); profile_cmd.set_defaults(func=cmd_profile)
    context_cmd = sub.add_parser("context"); context_cmd.add_argument("--repo", type=Path, required=True); context_cmd.add_argument("--handbook", type=Path, required=True); context_cmd.add_argument("--mode", choices=tuple(MODE_TO_PHASE), required=True); context_cmd.add_argument("--task", required=True); context_cmd.add_argument("--changed", action="append", default=[]); context_cmd.add_argument("--base-context", type=Path); context_cmd.add_argument("--metrics", action="store_true"); context_cmd.add_argument("--pretty", action="store_true"); context_cmd.set_defaults(func=cmd_context)
    validate_cmd = sub.add_parser("validate-plan"); validate_cmd.add_argument("--input", type=Path, required=True); validate_cmd.add_argument("--pretty", action="store_true"); validate_cmd.set_defaults(func=cmd_validate)
    check_cmd = sub.add_parser("check"); check_cmd.add_argument("--root", type=Path, required=True); check_cmd.add_argument("--pretty", action="store_true"); check_cmd.set_defaults(func=cmd_check)
    search_cmd = sub.add_parser("search"); search_cmd.add_argument("--root", type=Path, required=True); search_cmd.add_argument("--query", required=True); search_cmd.add_argument("--limit", type=int, default=8); search_cmd.add_argument("--historical", action="store_true"); search_cmd.add_argument("--pretty", action="store_true"); search_cmd.set_defaults(func=cmd_search)
    tree_cmd = sub.add_parser("tree"); tree_cmd.add_argument("--root", type=Path, required=True); tree_cmd.add_argument("--kind", choices=("knowledge", "execution", "repository"), default="knowledge"); tree_cmd.add_argument("--repo", type=Path); tree_cmd.add_argument("--task"); tree_cmd.add_argument("--historical", action="store_true"); tree_cmd.add_argument("--pretty", action="store_true"); tree_cmd.set_defaults(func=cmd_tree)
    explain_cmd = sub.add_parser("explain"); explain_cmd.add_argument("--root", type=Path, required=True); explain_cmd.add_argument("--repo", type=Path, required=True); explain_cmd.add_argument("--task", required=True); explain_cmd.add_argument("--mode", choices=tuple(MODE_TO_PHASE), default="plan"); explain_cmd.add_argument("--changed", action="append", default=[]); explain_cmd.add_argument("--pretty", action="store_true"); explain_cmd.set_defaults(func=cmd_explain)
    doctor_cmd = sub.add_parser("doctor"); doctor_cmd.add_argument("--root", type=Path, required=True); doctor_cmd.add_argument("--repo", type=Path); doctor_cmd.add_argument("--pretty", action="store_true"); doctor_cmd.set_defaults(func=cmd_doctor)
    integrity_cmd = sub.add_parser("integrity"); integrity_cmd.add_argument("--root", type=Path, required=True); integrity_cmd.add_argument("--pretty", action="store_true"); integrity_cmd.set_defaults(func=cmd_integrity)
    visual_cmd = sub.add_parser("visual-directions"); visual_cmd.add_argument("--root", type=Path, required=True); visual_cmd.add_argument("--surface"); visual_cmd.add_argument("--style"); visual_cmd.add_argument("--local-style"); visual_cmd.add_argument("--pretty", action="store_true"); visual_cmd.set_defaults(func=cmd_visual_directions)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except InvalidRepositoryRoot as exc:
        print(str(exc), file=sys.stderr)
        return 2
