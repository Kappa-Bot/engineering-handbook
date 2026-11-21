from __future__ import annotations

from copy import deepcopy
from itertools import chain
from typing import Any

ALLOWED_STATUS = {"passed", "failed", "not-run", "blocked", "not-applicable"}


def _get(obj: Any, key: str, default):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def project_conformance(capsule: Any, ir: Any, evidence: tuple[dict, ...], exceptions: tuple[dict, ...] = ()) -> dict:
    """Project a snapshot of the supplied evidence and exception records.

    The caller owns exception approval and scope decisions.
    """
    required = set()
    requirements = chain(_get(capsule, "required_evidence", []), _get(ir, "verification", []))
    for item in requirements:
        requirement_id = item if isinstance(item, str) else _get(item, "id", None)
        if requirement_id:
            required.add(requirement_id)
    exception_records = list(exceptions)
    exception_ids = {record["id"] for record in exception_records}
    demonstrated: list[str] = []; failed: list[str] = []; not_run: list[str] = []; not_applicable: list[str] = []; records: dict[str, dict] = {}
    blocked: list[str] = []
    for record in evidence:
        status = record.get("status")
        if not isinstance(status, str):
            raise ValueError("invalid evidence status: expected a string")
        if status not in ALLOWED_STATUS:
            raise ValueError(f"invalid evidence status {status}")
        evidence_id = record.get("id")
        if not evidence_id:
            raise ValueError("evidence id required")
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            raise ValueError("evidence id must be a nonblank string")
        if evidence_id in records:
            raise ValueError(f"duplicate evidence id {evidence_id}")
        if status == "not-applicable" and evidence_id not in exception_ids:
            reason = record.get("reason")
            if not reason or (
                evidence_id in required
                and (type(reason) in (bool, int, float) or (isinstance(reason, str) and not reason.strip()))
            ):
                raise ValueError("not-applicable requires reason or exception")
        records[evidence_id] = record
        if status == "passed":
            demonstrated.append(evidence_id)
        elif status == "failed":
            failed.append(evidence_id)
        elif status == "not-run":
            not_run.append(evidence_id)
        elif status == "blocked":
            blocked.append(evidence_id)
        else:
            not_applicable.append(evidence_id)
    gaps = sorted(required.difference(demonstrated, not_applicable, exception_ids))
    return {
        "required": sorted(required),
        "demonstrated": sorted(demonstrated),
        "failed": sorted(failed),
        "not_run": sorted(not_run),
        "blocked": sorted(blocked),
        "not_applicable": sorted(not_applicable),
        "exceptions": sorted(exception_ids),
        "exception_records": deepcopy(exception_records),
        "gaps": gaps,
        "evidence": deepcopy(records),
    }
