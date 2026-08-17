from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile

from .canonical import canonical_json
from .context_solver import build_repo_route, solve_context
from .handbook_compile import COMPILED_SCHEMA, OUTPUT_FILES, check_compiled_fresh, compile_handbook
from .planning_ir import capsule_delta, new_planning_ir, planning_ir_from_dict, validate_planning_ir
from .repo_profile import profile_repo, write_repo_profile
from .task_descriptor import describe_task

MODE_TO_PHASE = {"plan": "planning", "implement": "implementation", "verify": "verification"}


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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
    if pretty:
        print(json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(canonical_json(payload))


def cmd_compile(args) -> int:
    result = compile_handbook(args.root, args.output)
    _emit({"changed_files": list(result.changed_files), "skipped_sources": list(result.skipped_sources), "handbook_hash": result.handbook_hash}, args.pretty)
    return 0


def cmd_profile(args) -> int:
    profile = write_repo_profile(args.repo, args.output) if args.output else profile_repo(args.repo)
    _emit(profile, args.pretty)
    return 0


def cmd_context(args) -> int:
    phase = MODE_TO_PHASE[args.mode]
    compiled_dir = args.handbook.resolve()
    canonical_root = compiled_dir.parent.parent
    freshness_problems = check_compiled_fresh(canonical_root, compiled_dir)
    if freshness_problems:
        raise RuntimeError("compiled handbook context is stale: " + "; ".join(freshness_problems))
    compiled = _load_compiled(compiled_dir, phase)
    profile = profile_repo(args.repo)
    descriptor = describe_task(args.task, profile, tuple(args.changed or ()))
    capsule = solve_context(compiled, descriptor, phase)
    route = build_repo_route(profile, descriptor)
    ir = new_planning_ir(descriptor, capsule)
    capsule_dict = capsule.to_dict()
    if args.base_context:
        base = _read_json(args.base_context)
        base_id = base.get("context_id") or base.get("id")
        unit_ids = set(base.get("unit_ids", []))
        if not unit_ids:
            unit_ids = {unit.get("id") for unit in base.get("capsule", {}).get("units", []) if unit.get("id")}
        capsule_dict["delta"] = capsule_delta(base_id, unit_ids, capsule)
    payload = {"schema": "agent-context/v1", "mode": args.mode, "context_id": capsule.id, "descriptor": descriptor.to_dict(), "repo_route": route, "capsule": capsule_dict, "uncertain": [dict(item) for item in descriptor.uncertain], "planning_ir_seed": ir.to_dict()}
    if args.metrics:
        payload["metrics"] = {"candidate_units": capsule.candidate_count, "selected_units": len(capsule.units), "estimated_tokens": capsule.estimated_tokens, "full_source_reads": 0, "uncovered_required": len(capsule.uncovered), "repo_profile_segment_reuse": len(profile.get("meta", {}).get("reused_segments", [])), "context_delta": capsule_dict.get("delta", {}).get("unchanged_unit_count", 0) if "delta" in capsule_dict else 0}
    _emit(payload, args.pretty)
    return 0


def cmd_validate(args) -> int:
    payload = _read_json(args.input)
    ir = planning_ir_from_dict(payload)
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
        problems.extend(check_compiled_fresh(root, output))
    except Exception as exc:
        problems.append(str(exc))
    _emit({"ok": not problems, "problems": problems}, args.pretty)
    return 0 if not problems else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="engineering-context", description="Deterministic Engineering Handbook context compiler and agent runtime router")
    sub = parser.add_subparsers(dest="command", required=True)
    compile_cmd = sub.add_parser("compile-handbook"); compile_cmd.add_argument("--root", type=Path, required=True); compile_cmd.add_argument("--output", type=Path, required=True); compile_cmd.add_argument("--pretty", action="store_true"); compile_cmd.set_defaults(func=cmd_compile)
    profile_cmd = sub.add_parser("profile-repo"); profile_cmd.add_argument("--repo", type=Path, required=True); profile_cmd.add_argument("--output", type=Path); profile_cmd.add_argument("--pretty", action="store_true"); profile_cmd.set_defaults(func=cmd_profile)
    context_cmd = sub.add_parser("context"); context_cmd.add_argument("--repo", type=Path, required=True); context_cmd.add_argument("--handbook", type=Path, required=True); context_cmd.add_argument("--mode", choices=tuple(MODE_TO_PHASE), required=True); context_cmd.add_argument("--task", required=True); context_cmd.add_argument("--changed", action="append", default=[]); context_cmd.add_argument("--base-context", type=Path); context_cmd.add_argument("--metrics", action="store_true"); context_cmd.add_argument("--pretty", action="store_true"); context_cmd.set_defaults(func=cmd_context)
    validate_cmd = sub.add_parser("validate-plan"); validate_cmd.add_argument("--input", type=Path, required=True); validate_cmd.add_argument("--pretty", action="store_true"); validate_cmd.set_defaults(func=cmd_validate)
    check_cmd = sub.add_parser("check"); check_cmd.add_argument("--root", type=Path, required=True); check_cmd.add_argument("--pretty", action="store_true"); check_cmd.set_defaults(func=cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
