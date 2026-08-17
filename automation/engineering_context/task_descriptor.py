from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import stable_hash

EVIDENCE_RANK = {"explicit-structured": 600, "declared-decision": 500, "repo-structure": 400, "change-structure": 350, "text-signal": 200, "agent-resolution": 150}


@dataclass(frozen=True)
class TaskDescriptor:
    intent: tuple[str, ...] = ()
    surfaces: tuple[str, ...] = ()
    operations: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    state: dict[str, Any] | None = None
    boundaries: dict[str, Any] | None = None
    delivery: dict[str, Any] | None = None
    archetypes: tuple[str, ...] = ()
    uncertain: tuple[dict[str, Any], ...] = ()
    evidence: tuple[dict[str, Any], ...] = ()
    task_text: str = ""
    id: str = ""

    def __post_init__(self):
        if self.state is None:
            object.__setattr__(self, "state", {})
        if self.boundaries is None:
            object.__setattr__(self, "boundaries", {})
        if self.delivery is None:
            object.__setattr__(self, "delivery", {})
        if not self.id:
            object.__setattr__(self, "id", stable_hash(self.to_dict(include_id=False)))

    def to_dict(self, include_id: bool = True) -> dict[str, Any]:
        data = {
            "intent": list(self.intent), "surfaces": list(self.surfaces), "operations": list(self.operations),
            "capabilities": list(self.capabilities), "risks": list(self.risks), "state": self.state,
            "boundaries": self.boundaries, "delivery": self.delivery, "archetypes": list(self.archetypes),
            "uncertain": [dict(item) for item in self.uncertain], "evidence": [dict(item) for item in self.evidence],
            "task_text": self.task_text,
        }
        if include_id:
            data["id"] = self.id
        return data

    @classmethod
    def for_test(cls, risks: tuple[str, ...] = (), surfaces: tuple[str, ...] = (), operations: tuple[str, ...] = (), capabilities: tuple[str, ...] = (), migration: bool = False, **kwargs):
        return cls(intent=("modify",), surfaces=surfaces, operations=operations, capabilities=capabilities, risks=risks, state={"migration": migration}, boundaries={}, delivery={}, task_text="test", **kwargs)

    def predicates(self) -> set[str]:
        output = {f"intent:{item}" for item in self.intent} | {f"surface:{item}" for item in self.surfaces} | {f"operation:{item}" for item in self.operations} | {f"capability:{item}" for item in self.capabilities} | {f"risk:{item}" for item in self.risks} | {f"archetype:{item}" for item in self.archetypes}
        if self.state.get("migration"):
            output.add("state:migration")
        if self.boundaries.get("privileged"):
            output.add("boundary:privileged")
        if self.boundaries.get("external"):
            output.add("boundary:external")
        if self.delivery.get("production_effect"):
            output.add("delivery:production")
        return output


def _sorted(items: set[str]) -> tuple[str, ...]:
    return tuple(sorted(items))


def _evidence(bucket: list[dict[str, Any]], source: str, signal: str, value: str):
    bucket.append({"source": source, "rank": EVIDENCE_RANK[source], "signal": signal, "value": value})


def describe_task(task_text: str, repo_profile: dict, changed_paths: tuple[str, ...] = ()) -> TaskDescriptor:
    text = task_text.lower()
    intent = {"modify"}; surfaces: set[str] = set(); operations: set[str] = set(); capabilities: set[str] = set(); risks: set[str] = set(); archetypes: set[str] = set(); evidence: list[dict[str, Any]] = []; uncertain: list[dict[str, Any]] = []
    state = {"durable_change": False, "migration": False}; boundaries = {"external": False, "privileged": False}; delivery = {"production_effect": False}
    detected = repo_profile.get("detected", {}); repo_caps = detected.get("capabilities", {})
    for capability, enabled in repo_caps.items():
        if enabled:
            capabilities.add(capability); _evidence(evidence, "repo-structure", f"capability:{capability}", "true")

    if any(word in text for word in ("spacing", "layout", "visual", "screen", "button", "card", "ux", "ui")):
        surfaces.add("frontend"); archetypes.add("ui-flow-change"); _evidence(evidence, "text-signal", "surface", "frontend")
    if any(word in text for word in ("backend", "server", "mutation", "update", "create", "delete", "archive")):
        surfaces.add("backend")
    if any(word in text for word in ("authenticated", "permission", "role", "tenant")):
        operations.add("authorization"); risks.add("authorization"); boundaries["privileged"] = True
    if "tenant" in text:
        risks.add("tenant-isolation")
    if any(word in text for word in ("integration", "webhook", "api provider", "external")):
        operations.add("integration"); boundaries["external"] = True; archetypes.add("external-integration")
    if any(word in text for word in ("deploy", "release", "production")):
        operations.add("deployment"); delivery["production_effect"] = True; archetypes.add("production-release")
    if any(word in text for word in ("schema", "column", "migration", "archived_at")):
        operations.add("migration"); surfaces.add("database"); state["migration"] = True; state["durable_change"] = True; archetypes.add("schema-change")
    if any(word in text for word in ("create", "update", "archive", "delete", "mutation")):
        operations.add("mutation"); state["durable_change"] = bool(repo_caps.get("persistence"))
    if any(word in text for word in ("authenticated", "tenant")) and "mutation" in operations:
        archetypes.add("authenticated-mutation")
    if "invitation" in text or "invite" in text:
        operations.add("mutation"); risks.update(("authorization", "tenant-isolation")); archetypes.add("authenticated-mutation")
        if any(word in text for word in ("expiring", "expiration", "expiry", "token", "link")):
            risks.add("credential")
        else:
            uncertain.append({"field": "risks", "question": "Does this invitation act as a bearer credential?", "allowed": ["credential", "not-credential", "unknown"]})
    if any(word in text for word in ("token", "secret", "credential")):
        risks.add("credential")
    if "pwa" in text or "service worker" in text:
        capabilities.add("pwa"); archetypes.add("pwa-capability-change"); surfaces.add("frontend")
    if any(word in text for word in ("background job", "cron", "queue")):
        archetypes.add("background-job"); surfaces.add("backend")

    for raw_path in changed_paths:
        path = raw_path.lower().replace("\\", "/")
        if "migrations/" in path or path.endswith(".sql"):
            surfaces.add("database"); operations.add("migration"); state["migration"] = True; state["durable_change"] = True; archetypes.add("schema-change"); _evidence(evidence, "change-structure", "migration", raw_path)
        if path.startswith(".github/workflows/"):
            surfaces.add("ci"); _evidence(evidence, "change-structure", "surface", raw_path)
        if any(key in path for key in ("policy", "policies", "permission", "authz", "rls")):
            risks.add("authorization"); operations.add("authorization"); boundaries["privileged"] = True; _evidence(evidence, "change-structure", "risk:authorization", raw_path)
        if any(key in path for key in ("token", "secret", "invite", "credential")):
            risks.add("credential"); _evidence(evidence, "change-structure", "risk:credential", raw_path)
        if any(key in path for key in ("manifest.webmanifest", "service-worker", "sw.js")):
            capabilities.add("pwa"); surfaces.add("frontend")

    if "mutation" in operations and "authorization" in operations:
        archetypes.add("authenticated-mutation")
    if "mutation" in operations and state["durable_change"] and not archetypes:
        archetypes.add("modify-domain-state")
    if surfaces == {"frontend"} and any(word in text for word in ("spacing", "visual")):
        archetypes.add("visual-regression-fix")

    return TaskDescriptor(intent=_sorted(intent), surfaces=_sorted(surfaces), operations=_sorted(operations), capabilities=_sorted(capabilities), risks=_sorted(risks), state=state, boundaries=boundaries, delivery=delivery, archetypes=_sorted(archetypes), uncertain=tuple(uncertain), evidence=tuple(evidence), task_text=task_text)


def merge_agent_resolution(descriptor: TaskDescriptor, resolution: dict) -> TaskDescriptor:
    allowed_fields = {item["field"] for item in descriptor.uncertain}
    if not set(resolution).issubset(allowed_fields):
        raise ValueError("agent resolution may only fill declared uncertain fields")
    risks = set(descriptor.risks); uncertain = list(descriptor.uncertain); evidence = list(descriptor.evidence)
    if "risks" in resolution:
        values = resolution["risks"]
        if not isinstance(values, list):
            raise ValueError("risks resolution must be a list")
        allowed_values: set[str] = set()
        for item in uncertain:
            if item["field"] == "risks":
                allowed_values.update(item.get("allowed", []))
        for value in values:
            if value in ("not-credential", "unknown"):
                continue
            if value not in allowed_values:
                raise ValueError(f"invalid risk resolution {value}")
            risks.add(value); _evidence(evidence, "agent-resolution", "risk", value)
        uncertain = [item for item in uncertain if item["field"] != "risks"]
    return TaskDescriptor(intent=descriptor.intent, surfaces=descriptor.surfaces, operations=descriptor.operations, capabilities=descriptor.capabilities, risks=_sorted(risks), state=dict(descriptor.state), boundaries=dict(descriptor.boundaries), delivery=dict(descriptor.delivery), archetypes=descriptor.archetypes, uncertain=tuple(uncertain), evidence=tuple(evidence), task_text=descriptor.task_text)
