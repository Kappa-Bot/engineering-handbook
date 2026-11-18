"""Versioned, non-executable task/landmark registry and bounded language grammar.

Rules describe evidence, never grant permission. Complex visual recognizers in
task_descriptor remain feature extractors; generic intent/risk/path mappings live
in the registry. No eval, imports or arbitrary callbacks are accepted from data.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import unicodedata

REGISTRY_DIR = Path(__file__).resolve().parents[2] / "machine-readable/discovery"
PREFIXES = {"intent", "surface", "operation", "capability", "risk", "archetype", "state", "boundary", "delivery"}
CLAUSE_ACTION = r"(?:fix|correct|corrig\w*|revis\w*|review|audit\w*|inspect|design|diseñ\w*|disen\w*|redesign\w*|rediseñ\w*|redisen\w*|migr\w*|despl\w*|deploy(?:s|ed|ing)?|implement\w*|actualiz\w*|update|crea\w*|add|añad\w*|anad\w*|apply|aplica\w*|polish|pule|refine|remove|elimina\w*)"


def normalize(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold()) if not unicodedata.combining(c))


def positive_text(text: str) -> str:
    """Separate affirmative clauses before dropping prohibited actions.

    This is conservative lexical scope, not a natural-language authorization
    solver. Contradictions/implicit scope still need agent judgement.
    """
    primary = re.split(r"[;\n]|\b(?:but|pero|then|luego)\b", text, flags=re.I)
    clauses = []
    for clause in primary:
        clause = re.sub(r"^\s*(?:please|por favor)\s*,?\s+", "", clause, flags=re.I)
        explanation = re.match(
            r"\s*(?:how|what|why|when|where|which|can|could|would|should|c[oó]mo|qu[eé]|explain|explica\w*)\b",
            clause, re.I,
        )
        if not explanation:
            parts = re.split(rf"[,.](?=\s+(?:no\s|do not|don't|{CLAUSE_ACTION}\b))", clause, flags=re.I)
        else:
            parts = [clause]
        for part in parts:
            # A leading question or prohibition scopes coordinated verbs until an
            # explicit clause boundary; they do not become new instructions.
            if explanation or re.match(r"\s*(?:do not|don['’]t|never|no|without|sin)\b", part, re.I):
                clauses.append(part)
            else:
                clauses.extend(re.split(rf"\b(?:and|y)\s+(?=(?:no\s|do not|{CLAUSE_ACTION}\b))", part, flags=re.I))
    result = []
    negative = re.compile(
        r"\b(?:do not|don['’]t|never|without|no(?!\s+(?:solo|s[oó]lo|only)\b)|sin)\s+"
        r"(?:(?:un|una|a|any|el|la|the|hagas?|hacer)\s+){0,2}"
        r"(?:cambi\w*|chang\w*|migr\w*|deploy\w*|despl\w*|release\w*|"
        r"execut\w*|ejecut\w*|modif\w*|edit\w*|rediseñ\w*|redesign\w*|"
        r"touch\w*|toqu\w*|toc\w*|instal\w*|crea\w*|borr\w*|delet\w*|"
        r"apli\w*|apply|unslop\w*|alter\w*|actualiz\w*|updat\w*|rotat\w*)\b.*",
        re.I,
    )
    for clause in clauses:
        clause = negative.sub("", clause).strip()
        if clause:
            result.append(clause)
    return "; ".join(result)


def _validate_condition(condition: dict) -> None:
    if not isinstance(condition, dict) or len(condition) != 1:
        raise ValueError("rule condition must have exactly one operator")
    operator, value = next(iter(condition.items()))
    if operator in {"all", "any", "none"}:
        if not isinstance(value, list) or not value:
            raise ValueError(f"{operator} requires nonempty conditions")
        for child in value:
            _validate_condition(child)
    elif operator in {"text", "path"}:
        if not isinstance(value, str) or not value or len(value) > 2500:
            raise ValueError("regex must be a bounded nonempty string")
        re.compile(value)
    else:
        raise ValueError(f"unknown discovery operator: {operator}")


def validate_registry(registry: dict) -> None:
    if not isinstance(registry, dict) or registry.get("schema") != "discovery-rules/v1" or not isinstance(registry.get("rules"), list):
        raise ValueError("unsupported discovery rule registry")
    ids = set()
    for rule in registry["rules"]:
        rid = rule.get("id")
        if not isinstance(rid, str) or not rid or rid in ids:
            raise ValueError(f"invalid or duplicate rule id: {rid}")
        ids.add(rid)
        _validate_condition(rule.get("when"))
        outputs = rule.get("emit")
        if not isinstance(outputs, list) or not outputs:
            raise ValueError(f"rule {rid} needs outputs")
        for output in outputs:
            if not isinstance(output, str) or not re.fullmatch(r"[a-z]+:[a-z][a-z0-9-]*", output) or output.split(":")[0] not in PREFIXES:
                raise ValueError(f"invalid output in rule {rid}: {output}")


def load_registry(name: str = "rules.v1.json") -> dict:
    registry = json.loads((REGISTRY_DIR / name).read_text(encoding="utf-8"))
    if name == "rules.v1.json":
        validate_registry(registry)
    return registry


def _matches(condition: dict, text: str, paths: tuple[str, ...]) -> bool:
    operator, value = next(iter(condition.items()))
    if operator == "text":
        return bool(re.search(value, text))
    if operator == "path":
        return any(re.search(value, path) for path in paths)
    outcomes = [_matches(child, text, paths) for child in value]
    if operator == "all":
        return all(outcomes)
    if operator == "any":
        return any(outcomes)
    return not any(outcomes)


def evaluate_rules(task: str, changed_paths: tuple[str, ...] = (), registry: dict | None = None) -> tuple[set[str], list[dict]]:
    registry = registry if registry is not None else load_registry()
    validate_registry(registry)
    text = normalize(positive_text(task))
    raw = normalize(task)
    paths = tuple(normalize(path.replace("\\", "/").removeprefix("./")) for path in changed_paths)
    tags: set[str] = set()
    evidence = []
    for rule in registry["rules"]:
        matched = _matches(rule["when"], text, paths)
        if matched:
            tags.update(rule["emit"])
            # A path rule needs an actual path-only match, not just a nonempty
            # changed list, before it receives the higher evidence rank.
            path_match = bool(paths) and _matches(rule["when"], "", paths)
            source = "change-structure" if path_match else "text-signal"
            evidence.extend({"source": source, "rank": 350 if path_match else 200,
                             "signal": tag, "value": tag.split(":", 1)[1],
                             "rule_id": rule["id"], "decision": "matched"} for tag in rule["emit"])
        elif text != raw and _matches(rule["when"], raw, paths):
            evidence.append({"source": "text-signal", "rank": 200, "signal": "excluded",
                             "value": "negated-clause", "rule_id": rule["id"], "decision": "excluded"})
    return tags, evidence


def discover_landmarks(paths: list[str]) -> dict[str, list[str]]:
    registry = load_registry("landmarks.v1.json")
    if registry.get("schema") != "discovery-landmarks/v1":
        raise ValueError("unsupported landmarks registry")
    result = {}
    for label, patterns in registry["landmarks"].items():
        if not isinstance(patterns, list) or not all(isinstance(p, str) for p in patterns):
            raise ValueError(f"invalid landmark {label}")
        result[label] = [p for p in paths if any(re.search(pattern, normalize(p)) for pattern in patterns)]
    return result
