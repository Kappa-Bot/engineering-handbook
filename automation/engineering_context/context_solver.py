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
        return {"id": self.id, "phase": self.phase, "units": [dict(item) for item in self.units], "covered": list(self.covered), "uncovered": list(self.uncovered), "estimated_tokens": self.estimated_tokens, "escalations": [dict(item) for item in self.escalations], "provenance": list(self.provenance), "required_evidence": list(self.required_evidence), "candidate_count": self.candidate_count}


def _unit_matches(unit: dict[str, Any], tags: set[str], phase: str) -> bool:
    phases = set(unit.get("phase", []))
    if phases and phase not in phases:
        return False
    if set(unit.get("excludes", [])) & tags:
        return False
    activates = set(unit.get("activate_when", []))
    return not activates or bool(activates & tags)


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
    tags = descriptor.predicates()
    if routing:
        ids: set[str] = set()
        for tag in tags:
            ids.update(routing.get(tag, []))
        by_id = {unit["id"]: unit for unit in units}
        candidates = [by_id[uid] for uid in sorted(ids) if uid in by_id]
    else:
        candidates = list(units)
    return _dedupe([unit for unit in candidates if _unit_matches(unit, tags, phase)])


def solve_context(compiled: dict[str, Any], descriptor: TaskDescriptor, phase: str, budget: ContextBudget = DEFAULT_BUDGET) -> ContextCapsule:
    if phase not in {"planning", "implementation", "verification"}:
        raise ValueError("invalid phase")
    candidates = _candidate_units(compiled, descriptor, phase)
    required = set(descriptor.risks)
    covered: set[str] = set(); selected: list[dict[str, Any]] = []; escalations: list[dict[str, Any]] = []; total = 0
    by_id = {unit["id"]: unit for unit in candidates}

    dependency_ids: set[str] = set()
    for unit in candidates:
        dependency_ids.update(unit.get("requires", []))
    all_units = {unit["id"]: unit for unit in compiled.get("units", [])}
    for required_id in sorted(dependency_ids):
        unit = all_units.get(required_id)
        if unit and _unit_matches(unit, descriptor.predicates(), phase) and required_id not in by_id:
            candidates.append(unit); by_id[required_id] = unit

    remaining = list(candidates)
    while required - covered:
        best = None; best_key = None
        for unit in remaining:
            newly_covered = set(unit.get("covers", [])) & (required - covered)
            if not newly_covered:
                continue
            cost = max(1, int(unit.get("estimated_tokens", 1))); priority = max(1, int(unit.get("priority", 50)))
            score = (len(newly_covered) * priority) / cost
            key = (score, -cost, unit["id"])
            if best is None or key > best_key:
                best = unit; best_key = key
        if best is None:
            break
        cost = int(best.get("estimated_tokens", 0)); projected = total + cost
        if projected > budget.hard_max and best.get("force") not in {"must", "must-not"}:
            break
        if projected > budget.hard_max:
            escalations.append({"type": "hard-budget-crossed", "unit": best["id"], "estimated_tokens": projected})
        selected.append(best); total = projected; covered.update(set(best.get("covers", [])) & required); remaining = [unit for unit in remaining if unit["id"] != best["id"]]

    optional_limit = max(0, budget.soft_max - budget.reserve)
    for unit in sorted(remaining, key=lambda item: (-int(item.get("priority", 50)), int(item.get("estimated_tokens", 1)), item["id"])):
        if unit.get("type") not in {"decision-question", "constraint", "anti-pattern", "pattern", "verification", "route-hint"}:
            continue
        cost = int(unit.get("estimated_tokens", 0))
        if total + cost > optional_limit:
            continue
        selected.append(unit); total += cost

    uncovered = tuple(sorted(required - covered))
    if uncovered:
        escalations.append({"type": "uncovered-required", "risks": list(uncovered), "action": "load canonical guidance or resolve explicitly"})
    selected = _dedupe(selected)
    provenance = tuple(sorted({source for unit in selected for source in unit.get("sources", [unit.get("source")]) if source}))
    evidence = tuple(sorted(unit["id"] for unit in selected if unit.get("type") == "verification"))
    capsule_id = context_id(phase, descriptor.id, [unit["id"] for unit in selected], uncovered)
    return ContextCapsule(capsule_id, phase, tuple(selected), tuple(sorted(covered)), uncovered, total, tuple(escalations), provenance, evidence, len(candidates))


ARCHETYPE_ROUTE = {
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
    inspect: list[str] = []; avoid: list[str] = []
    for archetype in descriptor.archetypes:
        spec = ARCHETYPE_ROUTE.get(archetype, {})
        inspect.extend(spec.get("inspect_first", [])); avoid.extend(spec.get("avoid", []))
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
