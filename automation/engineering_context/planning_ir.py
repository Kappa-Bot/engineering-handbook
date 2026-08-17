from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .context_solver import ContextCapsule
from .task_descriptor import TaskDescriptor


@dataclass(frozen=True)
class Decision:
    id: str
    choice: str | None = None
    reason: str | None = None
    source: str | None = None

    def to_dict(self):
        return {key: value for key, value in {"id": self.id, "choice": self.choice, "reason": self.reason, "source": self.source}.items() if value is not None}


@dataclass(frozen=True)
class Invariant:
    id: str
    text: str = ""
    source: str | None = None

    def to_dict(self):
        return {key: value for key, value in {"id": self.id, "text": self.text, "source": self.source}.items() if value not in (None, "")}


@dataclass(frozen=True)
class VerificationRequirement:
    id: str
    evidence_class: str | None = None
    source: str | None = None

    def to_dict(self):
        return {key: value for key, value in {"id": self.id, "evidence_class": self.evidence_class, "source": self.source}.items() if value is not None}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class PlanningIR:
    context_id: str
    task: dict[str, Any]
    affected: dict[str, Any]
    decisions: tuple[Decision, ...] = ()
    invariants: tuple[Invariant, ...] = ()
    state_transitions: tuple[dict[str, Any], ...] = ()
    risks: tuple[str, ...] = ()
    implementation_units: tuple[dict[str, Any], ...] = ()
    verification: tuple[VerificationRequirement, ...] = ()
    unresolved: tuple[dict[str, Any], ...] = ()
    provenance: tuple[str, ...] = ()
    state: dict[str, Any] = field(default_factory=dict)
    operations: tuple[str, ...] = ()
    delivery: dict[str, Any] = field(default_factory=dict)
    uncovered: tuple[str, ...] = ()
    schema: str = "planning-ir/v1"

    def to_dict(self) -> dict[str, Any]:
        return {"schema": self.schema, "context_id": self.context_id, "task": self.task, "affected": self.affected, "decisions": [item.to_dict() for item in self.decisions], "invariants": [item.to_dict() for item in self.invariants], "state_transitions": [dict(item) for item in self.state_transitions], "risks": list(self.risks), "implementation_units": [dict(item) for item in self.implementation_units], "verification": [item.to_dict() for item in self.verification], "unresolved": [dict(item) for item in self.unresolved], "provenance": list(self.provenance), "state": self.state, "operations": list(self.operations), "delivery": self.delivery, "uncovered": list(self.uncovered)}

    @classmethod
    def for_test(cls, risks: tuple[str, ...] = (), decisions: tuple[Any, ...] = (), migration: bool = False, verification: tuple[Any, ...] = (), operations: tuple[str, ...] = (), production: bool = False):
        decision_items = tuple(item if isinstance(item, Decision) else Decision(str(item)) for item in decisions)
        verification_items = tuple(item if isinstance(item, VerificationRequirement) else VerificationRequirement(str(item)) for item in verification)
        return cls(context_id="test", task={"objective": "test", "scope": [], "exclusions": []}, affected={"capabilities": [], "boundaries": []}, decisions=decision_items, risks=risks, verification=verification_items, state={"migration": migration}, operations=operations, delivery={"production_effect": production})


def new_planning_ir(descriptor: TaskDescriptor, capsule: ContextCapsule) -> PlanningIR:
    invariants: list[Invariant] = []; verification: list[VerificationRequirement] = []; unresolved: list[dict[str, Any]] = []; implementation: list[dict[str, Any]] = []
    for unit in capsule.units:
        source = (unit.get("sources") or [unit.get("source")])[0]
        if unit.get("type") == "constraint":
            invariants.append(Invariant(unit["id"], unit.get("text", ""), source))
        elif unit.get("type") == "verification":
            verification.append(VerificationRequirement(unit["id"], unit.get("text"), source))
        elif unit.get("type") == "decision-question":
            unresolved.append({"id": unit["id"], "question": unit.get("text", ""), "source": source})
        elif unit.get("type") in {"pattern", "anti-pattern"}:
            implementation.append({"id": unit["id"], "source": source})
    for risk in capsule.uncovered:
        unresolved.append({"id": f"uncovered:{risk}", "risk": risk, "reason": "no compiled unit covered required risk"})
    return PlanningIR(context_id=capsule.id, task={"objective": descriptor.task_text, "scope": [], "exclusions": []}, affected={"capabilities": list(descriptor.capabilities), "boundaries": [key for key, value in descriptor.boundaries.items() if value]}, invariants=tuple(invariants), risks=descriptor.risks, implementation_units=tuple(implementation), verification=tuple(verification), unresolved=tuple(unresolved), provenance=capsule.provenance, state=dict(descriptor.state), operations=descriptor.operations, delivery=dict(descriptor.delivery), uncovered=capsule.uncovered)


def _has_decision(ir: PlanningIR, *needles: str) -> bool:
    ids = " ".join(decision.id.lower() for decision in ir.decisions)
    return any(needle in ids for needle in needles)


def _has_verification(ir: PlanningIR, *needles: str) -> bool:
    ids = " ".join(requirement.id.lower() for requirement in ir.verification)
    return any(needle in ids for needle in needles)


def validate_planning_ir(ir: PlanningIR) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []; risks = set(ir.risks)
    if ir.schema != "planning-ir/v1":
        issues.append(ValidationIssue("unsupported-planning-ir-schema", f"Unsupported Planning IR schema: {ir.schema}."))
    if risks & {"tenant-isolation", "privilege"} and not _has_decision(ir, "authorization", "authz"):
        issues.append(ValidationIssue("missing-authorization-decision", "Tenant/privilege risk requires an authorization boundary decision."))
    if "credential" in risks and not _has_decision(ir, "credential-lifecycle", "token-lifecycle", "credential"):
        issues.append(ValidationIssue("missing-credential-lifecycle-decision", "Credential risk requires lifecycle/expiration/revocation semantics."))
    if ir.state.get("migration") and not _has_verification(ir, "migration"):
        issues.append(ValidationIssue("missing-migration-verification", "Migration changes require migration verification evidence."))
    if "integration" in ir.operations and not _has_decision(ir, "retry", "failure", "integration"):
        issues.append(ValidationIssue("missing-integration-failure-semantics", "Integration work requires failure/retry semantics."))
    if ir.delivery.get("production_effect") and "deployment" in ir.operations and not _has_verification(ir, "release-identity", "release-target", "deployment-identity"):
        issues.append(ValidationIssue("missing-release-identity-verification", "Production deployment requires release identity/target verification."))
    unresolved_risks = {item.get("risk") for item in ir.unresolved if item.get("risk")}
    for risk in ir.uncovered:
        if risk not in unresolved_risks:
            issues.append(ValidationIssue("missing-uncovered-risk-entry", f"Uncovered risk {risk} must remain explicit in unresolved state."))
    return tuple(issues)


def capsule_delta(previous_id: str | None, previous_unit_ids: set[str], current: ContextCapsule) -> dict[str, Any]:
    current_by_id = {unit["id"]: unit for unit in current.units}; current_ids = set(current_by_id)
    if previous_id is None:
        return {"base_context_id": None, "current_context_id": current.id, "added_units": [current_by_id[uid] for uid in sorted(current_ids)], "removed_unit_ids": [], "unchanged_unit_count": 0}
    return {"base_context_id": previous_id, "current_context_id": current.id, "added_units": [current_by_id[uid] for uid in sorted(current_ids - previous_unit_ids)], "removed_unit_ids": sorted(previous_unit_ids - current_ids), "unchanged_unit_count": len(current_ids & previous_unit_ids)}


def _render(ir: PlanningIR, title: str) -> str:
    lines = [f"# {title}", "", f"Context: `{ir.context_id}`", ""]
    if ir.task.get("objective"):
        lines += ["## Objective", ir.task["objective"], ""]
    if ir.decisions:
        lines += ["## Decisions", *[f"- `{decision.id}`" + (f": {decision.choice}" if decision.choice else "") for decision in ir.decisions], ""]
    if ir.invariants:
        lines += ["## Invariants", *[f"- `{item.id}` ({item.source or 'local'})" for item in ir.invariants], ""]
    if ir.unresolved:
        lines += ["## Unresolved", *[f"- `{item.get('id')}`" + (f": {item.get('question')}" if item.get("question") else "") for item in ir.unresolved], ""]
    if ir.verification:
        lines += ["## Verification", *[f"- `{item.id}`" for item in ir.verification], ""]
    return "\n".join(lines).rstrip() + "\n"


def render_plan_view(ir: PlanningIR) -> str:
    return _render(ir, "Implementation Plan Context")


def render_spec_view(ir: PlanningIR) -> str:
    return _render(ir, "Specification Context")


def planning_ir_from_dict(payload: dict[str, Any]) -> PlanningIR:
    return PlanningIR(schema=payload.get("schema", "planning-ir/v1"), context_id=payload.get("context_id", ""), task=payload.get("task", {}), affected=payload.get("affected", {}), decisions=tuple(Decision(**item) for item in payload.get("decisions", [])), invariants=tuple(Invariant(**item) for item in payload.get("invariants", [])), state_transitions=tuple(payload.get("state_transitions", [])), risks=tuple(payload.get("risks", [])), implementation_units=tuple(payload.get("implementation_units", [])), verification=tuple(VerificationRequirement(**item) for item in payload.get("verification", [])), unresolved=tuple(payload.get("unresolved", [])), provenance=tuple(payload.get("provenance", [])), state=payload.get("state", {}), operations=tuple(payload.get("operations", [])), delivery=payload.get("delivery", {}), uncovered=tuple(payload.get("uncovered", [])))
