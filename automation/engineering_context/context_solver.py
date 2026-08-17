from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import context_id
from .task_descriptor import TaskDescriptor


@dataclass(frozen=True)
class ContextBudget:
    target: int = 600
    soft_max: int = 900
    hard_max: int = 1400
    reserve: int = 250


DEFAULT_BUDGET = ContextBudget()


@dataclass(frozen=True)
class ContextCapsule:
    id: str
    phase: str
    units: tuple[dict[str, Any], ...]
    covered: tuple[str, ...]
    uncovered: tuple[str, ...]
    estimated_tokens: int
    escalations: tuple[dict[str, Any], ...]
    provenance: tuple[str, ...]
    required_evidence: tuple[str, ...] = ()
    candidate_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "phase": self.phase, "units": [dict(x) for x in self.units], "covered": list(self.covered), "uncovered": list(self.uncovered), "estimated_tokens": self.estimated_tokens, "escalations": [dict(x) for x in self.escalations], "provenance": list(self.provenance), "required_evidence": list(self.required_evidence), "candidate_count": self.candidate_count}


def _descriptor_tags(descriptor: TaskDescriptor) -> set[str]:
    return descriptor.predicates()


def _unit_matches(unit: dict[str, Any], tags: set[str], phase: str) -> bool:
    phases = set(unit.get("phase", []))
    if phases and phase not in phases:
        return False
    if set(unit.get("excludes", [])) & tags:
        return False
    activates = set(unit.get("activate_when", []))
    activate_all = set(unit.get("activate_all", []))
    any_ok = not activates or bool(activates & tags)
    all_ok = not activate_all or activate_all.issubset(tags)
    return any_ok and all_ok


def _dedupe(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for unit in units:
        uid = unit["id"]
        if uid not in merged:
            merged[uid] = dict(unit)
            continue
        merged[uid]["sources"] = sorted(set(merged[uid].get("sources", [])) | set(unit.get("sources", [])))
    return [merged[key] for key in sorted(merged)]


def _candidate_units(compiled: dict[str, Any], descriptor: TaskDescriptor, phase: str) -> list[dict[str, Any]]:
    units = compiled.get("units", [])
    routing = compiled.get("routing", {})
    tags = _descriptor_tags(descriptor)
    if routing:
        ids: set[str] = set()
        for tag in tags:
            ids.update(routing.get(tag, []))
        by_id = {unit["id"]: unit for unit in units}
        candidates = [by_id[uid] for uid in sorted(ids) if uid in by_id]
    else:
        candidates = list(units)
    return _dedupe([unit for unit in candidates if _unit_matches(unit, tags, phase)])


def _direct_risk_coverage(unit: dict[str, Any], required: set[str]) -> set[str]:
    activations = set(unit.get("activate_when", [])) | set(unit.get("activate_all", []))
    if activations and all(item.startswith("intent:") for item in activations):
        return set()
    return set(unit.get("covers", [])) & required


def solve_context(compiled: dict[str, Any], descriptor: TaskDescriptor, phase: str, budget: ContextBudget = DEFAULT_BUDGET) -> ContextCapsule:
    if phase not in {"planning", "implementation", "verification"}:
        raise ValueError("invalid phase")

    tags = _descriptor_tags(descriptor)
    candidates = _candidate_units(compiled, descriptor, phase)
    all_units = {unit["id"]: unit for unit in compiled.get("units", [])}
    required = set(descriptor.risks)
    covered: set[str] = set()
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    escalations: list[dict[str, Any]] = []
    total = 0

    def closure_for(unit: dict[str, Any]) -> list[dict[str, Any]]:
        ordered: list[dict[str, Any]] = []
        seen: set[str] = set()
        visiting: set[str] = set()

        def visit(current: dict[str, Any]) -> None:
            uid = current["id"]
            if uid in selected_ids or uid in seen:
                return
            if uid in visiting:
                raise ValueError(f"cyclic requires dependency at {uid}")
            visiting.add(uid)
            for required_id in sorted(current.get("requires", [])):
                dependency = all_units.get(required_id)
                if dependency is None:
                    raise ValueError(f"unit {uid} requires unknown unit {required_id}")
                if not _unit_matches(dependency, tags, phase):
                    raise ValueError(f"required unit {required_id} is not applicable for selected unit {uid}")
                visit(dependency)
            visiting.remove(uid)
            seen.add(uid)
            ordered.append(current)

        visit(unit)
        return ordered

    def closure_cost(closure: list[dict[str, Any]]) -> int:
        return sum(int(unit.get("estimated_tokens", 0)) for unit in closure if unit["id"] not in selected_ids)

    def append_closure(closure: list[dict[str, Any]], escalation_type: str) -> None:
        nonlocal total
        for unit in closure:
            uid = unit["id"]
            if uid in selected_ids:
                continue
            cost = int(unit.get("estimated_tokens", 0))
            projected = total + cost
            if projected > budget.hard_max:
                escalations.append({"type": escalation_type, "unit": uid, "estimated_tokens": projected})
            selected.append(unit)
            selected_ids.add(uid)
            total = projected
            covered.update(_direct_risk_coverage(unit, required))

    remaining = list(candidates)
    force_weight = {"must": 4.0, "must-not": 4.0, "should": 1.5, "may": 1.0, None: 1.0}

    while required - covered:
        best = None
        best_closure: list[dict[str, Any]] = []
        best_key = None
        for unit in remaining:
            newly_covered = _direct_risk_coverage(unit, required - covered)
            if not newly_covered:
                continue
            closure = closure_for(unit)
            cost = max(1, closure_cost(closure))
            projected = total + cost
            if projected > budget.hard_max and unit.get("force") not in {"must", "must-not"}:
                continue
            priority = max(1, int(unit.get("priority", 50)))
            score = ((len(newly_covered) ** 2) * priority * force_weight.get(unit.get("force"), 1.0)) / cost
            key = (score, -cost, unit["id"])
            if best is None or key > best_key:
                best = unit
                best_closure = closure
                best_key = key
        if best is None:
            break
        append_closure(best_closure, "hard-budget-crossed")
        remaining = [unit for unit in remaining if unit["id"] not in selected_ids]

    # Include every matching mandatory requirement after minimum direct risk coverage.
    # Pure intent activation does not count as direct risk coverage, but authority still applies.
    for unit in sorted(remaining, key=lambda item: (-int(item.get("priority", 50)), int(item.get("estimated_tokens", 1)), item["id"])):
        if unit.get("force") not in {"must", "must-not"}:
            continue
        closure = closure_for(unit)
        append_closure(closure, "normative-budget-crossed")

    uncovered = tuple(sorted(required - covered))
    if uncovered:
        escalations.append({"type": "uncovered-required", "risks": list(uncovered), "action": "load canonical guidance or resolve explicitly"})
    selected = _dedupe(selected)
    provenance = tuple(sorted({source for unit in selected for source in unit.get("sources", [unit.get("source")]) if source}))
    evidence = tuple(sorted(unit["id"] for unit in selected if unit.get("type") == "verification"))
    capsule_id = context_id(phase, descriptor.id, [unit["id"] for unit in selected], uncovered)
    return ContextCapsule(capsule_id, phase, tuple(selected), tuple(sorted(covered)), uncovered, total, tuple(escalations), provenance, evidence, len(candidates))


ARCTYPE_ROUTE = {
    "authenticated-mutation": {"inspect_first": ["domain-mutation", "authorization-boundary", "persistence-owner", "nearest-tests"], "avoid": ["pwa"]},
    "schema-change": {"inspect_first": ["persistence-owner", "migrations", "nearest-tests"], "avoid": ["pwa"]},
    "external-integration": {"inspect_first": ["integration-boundary", "domain-owner", "nearest-tests"], "avoid": []},
    "ui-flow-change": {"inspect_first": ["ui-surface", "design-primitives", "nearest-tests"], "avoid": ["database"]},
    "visual-regression-fix": {"inspect_first": ["ui-surface", "design-primitives", "nearest-tests"], "avoid": ["database", "pwa"]},
    "pwa-capability-change": {"inspect_first": ["pwa", "ui-surface", "nearest-tests"], "avoid": []},
    "production-release": {"inspect_first": ["ci", "release-config", "verification"], "avoid": []},
    "background-job": {"inspect_first": ["domain-owner", "persistence-owner", "nearest-tests"], "avoid": ["pwa"]},
    "modify-domain-state": {"inspect_first": ["domain-owner", "persistence-owner", "nearest-tests"], "avoid": ["pwa"]},
    "add-crud-capability": {"inspect_first": ["domain-owner", "persistence-owner", "nearest-tests"], "avoid": []},
}


def build_repo_route(profile: dict, descriptor: TaskDescriptor) -> dict[str, Any]:
    inspect: list[str] = []
    avoid: list[str] = []
    for archetype in descriptor.archetypes:
        spec = ARCTYPE_ROUTE.get(archetype, {})
        inspect.extend(spec.get("inspect_first", []))
        avoid.extend(spec.get("avoid", []))
    if "authorization" in descriptor.risks:
        inspect.append("authorization-boundary")
    if descriptor.state.get("migration"):
        inspect.extend(["persistence-owner", "migrations"])
    landmarks = {**profile.get("detected", {}).get("landmarks", {}), **profile.get("declared", {}).get("landmarks", {})}
    resolved = {label: landmarks.get(label, []) for label in sorted(set(inspect))}
    commands = profile.get("detected", {}).get("commands", {})
    verification: list[str] = []
    if "authorization" in descriptor.risks:
        verification.append("authorization-negative")
    if "tenant-isolation" in descriptor.risks:
        verification.append("cross-tenant-negative")
    if "credential" in descriptor.risks:
        verification.append("credential-lifecycle")
    if descriptor.state.get("migration"):
        verification.append("migration-validation")
    return {"inspect_first": sorted(set(inspect)), "resolved": resolved, "inspect_if": [], "avoid_by_default": sorted(set(avoid)), "commands": commands, "verification": verification}
