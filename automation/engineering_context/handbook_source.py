from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any

AGENT_CONTEXT_OPEN = "```json agent-context"
ALLOWED_TYPES = {
    "constraint", "decision-question", "risk", "pattern",
    "anti-pattern", "verification", "escalation", "route-hint",
}
ALLOWED_PHASES = {"planning", "implementation", "verification"}
ALLOWED_FORCE = {"must", "must-not", "should", "may"}


class AgentContextError(ValueError):
    pass


@dataclass(frozen=True)
class KnowledgeUnit:
    id: str
    type: str
    text: str
    source: str
    covers: tuple[str, ...]
    activate_when: tuple[str, ...]
    activate_all: tuple[str, ...] = ()
    force: str | None = None
    phase: tuple[str, ...] = ()
    priority: int = 50
    requires: tuple[str, ...] = ()
    excludes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "text": self.text,
            "source": self.source,
            "sources": [self.source],
            "covers": list(self.covers),
            "activate_when": list(self.activate_when),
            "activate_all": list(self.activate_all),
            "phase": list(self.phase),
            "priority": self.priority,
            "requires": list(self.requires),
            "excludes": list(self.excludes),
        }
        if self.force is not None:
            result["force"] = self.force
        return result


def extract_source_id(markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        raise AgentContextError("missing frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise AgentContextError("unterminated frontmatter") from exc
    found = []
    pattern = re.compile(r"^id:\s*([^\s]+)\s*$")
    for line in lines[1:end]:
        match = pattern.match(line)
        if match:
            found.append(match.group(1))
    if len(found) != 1:
        raise AgentContextError("frontmatter must contain exactly one scalar id")
    return found[0]


def _string_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        raise AgentContextError(f"{field} must be a list of non-empty strings")
    return tuple(value)


def _validate_unit(raw: Any, source_id: str) -> KnowledgeUnit:
    if not isinstance(raw, dict):
        raise AgentContextError("unit must be an object")
    required = ("id", "type", "text", "source", "covers", "activate_when")
    missing = [key for key in required if key not in raw]
    if missing:
        raise AgentContextError("unit missing fields: " + ", ".join(missing))
    if not isinstance(raw["id"], str) or not raw["id"]:
        raise AgentContextError("unit id must be non-empty string")
    if raw["type"] not in ALLOWED_TYPES:
        raise AgentContextError(f"unknown unit type: {raw['type']}")
    if not isinstance(raw["text"], str) or not raw["text"].strip():
        raise AgentContextError("unit text must be non-empty string")
    if raw["source"] != source_id:
        raise AgentContextError(f"unit {raw['id']} source mismatch")
    force = raw.get("force")
    if force is not None and force not in ALLOWED_FORCE:
        raise AgentContextError(f"invalid force: {force}")
    phase = _string_tuple(raw.get("phase", []), "phase")
    unknown_phase = set(phase) - ALLOWED_PHASES
    if unknown_phase:
        raise AgentContextError("invalid phase: " + ", ".join(sorted(unknown_phase)))
    priority = raw.get("priority", 50)
    if not isinstance(priority, int) or not 0 <= priority <= 100:
        raise AgentContextError("priority must be integer from 0 to 100")
    return KnowledgeUnit(
        id=raw["id"], type=raw["type"], text=raw["text"].strip(), source=source_id,
        covers=_string_tuple(raw["covers"], "covers"),
        activate_when=_string_tuple(raw["activate_when"], "activate_when"),
        activate_all=_string_tuple(raw.get("activate_all", []), "activate_all"),
        force=force, phase=phase, priority=priority,
        requires=_string_tuple(raw.get("requires", []), "requires"),
        excludes=_string_tuple(raw.get("excludes", []), "excludes"),
    )


def extract_agent_context(markdown: str, path: str) -> list[KnowledgeUnit]:
    if AGENT_CONTEXT_OPEN not in markdown:
        return []
    source_id = extract_source_id(markdown)
    lines = markdown.splitlines()
    units: list[KnowledgeUnit] = []
    seen: set[str] = set()
    i = 0
    while i < len(lines):
        if lines[i].strip() != AGENT_CONTEXT_OPEN:
            i += 1
            continue
        i += 1
        body: list[str] = []
        while i < len(lines) and lines[i].strip() != "```":
            body.append(lines[i])
            i += 1
        if i >= len(lines):
            raise AgentContextError(f"{path}: unterminated agent-context block")
        try:
            payload = json.loads("\n".join(body))
        except json.JSONDecodeError as exc:
            raise AgentContextError(f"{path}: malformed agent-context JSON: {exc}") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("units"), list):
            raise AgentContextError(f"{path}: agent-context payload must contain units list")
        for raw in payload["units"]:
            unit = _validate_unit(raw, source_id)
            if unit.id in seen:
                raise AgentContextError(f"{path}: duplicate unit id {unit.id}")
            seen.add(unit.id)
            units.append(unit)
        i += 1
    return units
