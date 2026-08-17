from __future__ import annotations

from typing import Any

ALLOWED_STATUS = {"passed", "failed", "not-run", "not-applicable"}


def _get(obj: Any, key: str, default):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def project_conformance(capsule: Any, ir: Any, evidence: tuple[dict, ...], exceptions: tuple[dict, ...] = ()) -> dict:
    required = set(_get(capsule, "required_evidence", [])) | set(_get(ir, "verification", []))
    normalized = set()
    for item in required:
        if isinstance(item, str):
            normalized.add(item)
        elif isinstance(item, dict):
            normalized.add(item.get("id"))
        else:
            normalized.add(getattr(item, "id", None))
    required = {item for item in normalized if item}
    exception_map = {item["id"]: item for item in exceptions}
    demonstrated: list[str] = []; failed: list[str] = []; not_run: list[str] = []; not_applicable: list[str] = []; gaps: list[str] = []; records: dict[str, dict] = {}
    for record in evidence:
        status = record.get("status")
        if status not in ALLOWED_STATUS:
            raise ValueError(f"invalid evidence status {status}")
        evidence_id = record.get("id")
        if not evidence_id:
            raise ValueError("evidence id required")
        if evidence_id in records:
            raise ValueError(f"duplicate evidence id {evidence_id}")
        if status == "not-applicable" and not (record.get("reason") or evidence_id in exception_map):
            raise ValueError("not-applicable requires reason or exception")
        records[evidence_id] = record
        if status == "passed":
            demonstrated.append(evidence_id)
        elif status == "failed":
            failed.append(evidence_id)
        elif status == "not-run":
            not_run.append(evidence_id)
        else:
            not_applicable.append(evidence_id)
    for requirement in sorted(required):
        if requirement in demonstrated or requirement in not_applicable or requirement in exception_map:
            continue
        gaps.append(requirement)
    return {"required": sorted(required), "demonstrated": sorted(demonstrated), "failed": sorted(failed), "not_run": sorted(not_run), "not_applicable": sorted(not_applicable), "exceptions": sorted(exception_map), "gaps": gaps, "evidence": records}
