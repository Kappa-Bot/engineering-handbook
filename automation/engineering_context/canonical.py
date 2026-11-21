from __future__ import annotations

import hashlib
import json
import math
from typing import Any, NoReturn


def load_json_with_unique_members(text: str, *, label: str) -> Any:
    def unique_members(pairs: list[tuple[str, object]]) -> dict[str, object]:
        members: dict[str, object] = {}
        for name, value in pairs:
            if name in members:
                raise ValueError(f"{label} has duplicate JSON member {name!r}.")
            members[name] = value
        return members

    def invalid_number(value: str) -> NoReturn:
        raise ValueError(f"{label} has invalid JSON number {value!r}.")

    def finite_float(value: str) -> float:
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{label} JSON number is outside the supported finite range.")
        return result

    return json.loads(text, object_pairs_hook=unique_members, parse_constant=invalid_number, parse_float=finite_float)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def stable_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def estimate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text.encode("utf-8")) / 4)) if text else 0


def context_id(*parts: Any) -> str:
    return stable_hash(list(parts))
