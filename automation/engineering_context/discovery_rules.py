"""Versioned, non-executable task/landmark registry and bounded language grammar.

Rules describe evidence, never grant permission. Complex visual recognizers in
task_descriptor remain feature extractors; generic intent/risk/path mappings live
in the registry. No eval, imports or arbitrary callbacks are accepted from data.
"""
from __future__ import annotations

from pathlib import Path
import re
import unicodedata
from typing import Any

from .canonical import load_json_with_finite_numbers

REGISTRY_DIR = Path(__file__).resolve().parents[2] / "machine-readable/discovery"
PREFIXES = {"intent", "surface", "operation", "capability", "risk", "archetype", "state", "boundary", "delivery"}
CLAUSE_ACTION = r"(?:fix|correct|corrig\w*|revis\w*|review|audit\w*|inspect|check|analiz\w*|analy[sz]\w*|assess|measure|mide|medir|benchmark|verific\w*|verify|design|diseñ\w*|disen\w*|redesign\w*|rediseñ\w*|redisen\w*|migr\w*|despl\w*|deploy(?:s|ed|ing)?|implement\w*|actualiz\w*|update|crea\w*|add|añad\w*|anad\w*|apply|aplica\w*|polish|pule|refine|remove|elimina\w*|refactor\w*|rename\w*|renombr\w*|reorgan\w*|restructur\w*|reestructur\w*|limpi\w*|escrib\w*|write|replace|sustitu\w*|clean(?:\s+up)?|simplif\w*|split|extract)"

# The registry remains the only domain-to-owner router. This vocabulary only
# identifies which *affirmative object* a declarative quality rule may inspect.
QUALITY_REVIEW_NOUN = r"(?:audit|auditoria|review|revision|analysis|analisis|assessment|evaluacion|inspeccion)"
QUALITY_DOMAIN_HEAD = r"(?:security|seguridad|privacy|privacidad|performance|rendimiento|accessibility|accesibilidad|reliability|fiabilidad|ux|ui|quality|calidad|global|integral|holistic|overall|full|engineering|comprehensive)"
QUALITY_ACTION = r"(?:review|revis\w*|audit\w*|inspeccion\w*|inspect|check|comprueba|verific\w*|verify|evalu\w*|assess|diagnos\w*|diagnost\w*|analy[sz]\w*|analiz\w*|measure|mide|medir|benchmark|profil\w*|test|prueba\w*|scan|escane\w*|fix|correct|corrig\w*|repair|repara\w*|mejora\w*|improve|optimiza\w*|optimize|mitiga\w*|reduce|harden|refuerza\w*|implement\w*)"
QUALITY_MUTATING_ACTION = r"(?:fix|correct|corrig\w*|repair|repara\w*|mejora\w*|improve|optimiza\w*|optimize|mitiga\w*|reduce|harden|refuerza\w*|implement\w*)"
QUALITY_WRAPPER = r"(?:realiza\w*|haz|hacer|efectua\w*|lleva a cabo|carry out|conduct|perform|complete|completa\w*|termina\w*|finish|do|run)"
QUALITY_HEADER = re.compile(
    rf"^(?:(?:please|por favor|necesito que|quiero que)\s+)?"
    rf"(?:{QUALITY_ACTION}\b|"
    rf"{QUALITY_WRAPPER}\s+(?:(?:una?|an?|the|el|la)\s+)?(?:{QUALITY_DOMAIN_HEAD}\s+){{0,5}}{QUALITY_REVIEW_NOUN}\b|"
    rf"(?:{QUALITY_DOMAIN_HEAD}\s+){{1,4}}{QUALITY_REVIEW_NOUN}\b|"
    rf"{QUALITY_REVIEW_NOUN}\b)",
    re.I,
)
DOCUMENT_PRIMARY = re.compile(
    r"^(?:(?:the|this|our|my|el|la|los|las|esta|este|de|del)\s+)?"
    r"(?:(?:api|security|seguridad|privacy|privacidad|performance|rendimiento|"
    r"accessibility|accesibilidad|ux|ui|quality|calidad|reliability|fiabilidad|"
    r"internal|public|website|web|product|release|deployment|policy|politica|the|la|el)\s+){0,4}"
    r"(?:readme(?:\.md)?|handbook|docs?|documentation|documentacion|guia|guide|"
    r"manual|instructions|instrucciones|policy|politica)(?:\b|\.md\b)",
    re.I,
)
QUALITY_NOMINAL = r"(?:security|seguridad|privacy|privacidad|performance|rendimiento|accessibility|accesibilidad|reliability|fiabilidad|ux|ui)"
NOMINAL_EXCLUSION = re.compile(
    rf"\b(?:not(?!\s+only\b)|excluding|exclude|except(?:\s+for)?|excepto|without|sin)\s+"
    rf"(?:(?:the|la|el|a|la|los|las)\s+)?{QUALITY_NOMINAL}\b"
    rf"(?:\s*(?:,|\band\b|\bor\b|\by\b|\bni\b|\bnor\b|\be\b)\s*{QUALITY_NOMINAL}\b)*",
    re.I,
)


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.casefold())
    if normalized.isascii():
        return normalized
    marks = {ord(char): None for char in set(normalized) if unicodedata.combining(char)}
    return normalized.translate(marks) if marks else normalized


def positive_text(text: str) -> str:
    """Separate affirmative clauses before dropping prohibited actions.

    This is conservative lexical scope, not a natural-language authorization
    solver. Contradictions/implicit scope still need agent judgement.
    """
    primary = re.split(r"[;\n]|\b(?:but|pero|then|luego)\b", text, flags=re.I)
    # A repeated explicit material verb starts a new affirmative instruction:
    # "Do not apply X and apply Y" differs from "do not deploy and migrate".
    # Keep this narrow; coordinated negations without a repeated action stay
    # conservatively prohibited by the general grammar below.
    expanded = []
    material_verb = r"(?:apply|apli\w*|use\w*|usa\w*|switch|set|adopt|adopta\w*)"
    for clause in primary:
        if re.match(rf"\s*(?:do not|don['’]t|never|no)\s+{material_verb}\b", clause, re.I):
            expanded.extend(re.split(rf"\b(?:and|y)\s+(?={material_verb}\b)", clause, maxsplit=1, flags=re.I))
        else:
            expanded.append(clause)
    primary = expanded
    # A leading prohibition can be followed by a distinct affirmative
    # instruction after a comma ("do not redesign X, redesign Y"), but a
    # bare list of banned verbs ("do not refactor, rename or reorganize")
    # remains one negated scope. Accept only clear independent action heads.
    separated = []
    affirmative_after_negation = (
        r"(?:fix|corrig\w*|correct|review|revis\w*|audit\w*|inspect|"
        r"redesign\w*|rediseñ\w*|redisen\w*|deploy\w*|despl\w*)"
    )
    for clause in primary:
        if re.match(r"\s*(?:do not|don['’]t|never|no|without|sin)\b", clause, re.I):
            separated.extend(re.split(rf",(?=\s*{affirmative_after_negation}\b)", clause, maxsplit=1, flags=re.I))
        else:
            separated.append(clause)
    primary = separated
    clauses = []
    for clause in primary:
        clause = re.sub(r"^\s*(?:please|por favor)\s*,?\s+", "", clause, flags=re.I)
        explanation = re.match(
            r"\s*[¿?]?\s*(?:how|what|why|when|where|which|can|could|would|should|c[oó]mo|qu[eé]|explain|explica\w*)\b",
            clause, re.I,
        )
        # An enumeration after a leading prohibition stays prohibited; a
        # descriptive review/question does not become an embedded edit order.
        prohibited = re.match(r"\s*(?:do not|don['’]t|never|no|without|sin)\b", clause, re.I)
        review_of_procedure = re.match(r"\s*(?:review|revisa\w*|audit\w*|audita\w*|inspect|inspecciona\w*)\b", clause, re.I) and re.search(
            r"\b(?:how\s+to|c[oó]mo|to\s+(?:refactor\w*|renam\w*|renombr\w*|split|extract|reorgan\w*|restructur\w*|reestructur\w*))\b|"
            r"\b(?:without|sin)\s+(?:edit\w*|modif\w*|cambi\w*|editar|hacer cambios)\b(?:\s+(?:anything|nada))?\s*[.!?]?$",
            clause, re.I,
        )
        protected = bool(explanation or prohibited or review_of_procedure)
        if protected:
            parts = [clause]
        else:
            parts = re.split(rf"[,.](?=\s+(?:no\s|do not|don't|{CLAUSE_ACTION}\b))", clause, flags=re.I)
        for part in parts:
            # A leading question or prohibition scopes coordinated verbs until an
            # explicit clause boundary; they do not become new instructions.
            if protected or re.match(r"\s*(?:do not|don['’]t|never|no|without|sin)\b", part, re.I):
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
        r"apli\w*|apply|unslop\w*|alter\w*|actualiz\w*|updat\w*|rotat\w*|"
        r"refactor\w*|renam\w*|renombr\w*|reorgan\w*|restructur\w*|reestructur\w*|limpi\w*|"
        r"clean(?:\s+up)?|replace|sustitu\w*|escrib\w*|write|simplif\w*|split|extract|"
        r"audit\w*|revis\w*|review|inspect|verifi[cq]\w*|verify|measure|mide|medir|benchmark)\b.*",
        re.I,
    )
    for clause in clauses:
        # "Review UX, excluding privacy and security" is a review of UX,
        # not permission to load the expressly excluded domain playbooks.
        clause = NOMINAL_EXCLUSION.sub("", clause)
        clause = negative.sub("", clause).strip(" ,")
        if clause:
            # A provenance review names an observation even when its label begins with "release".
            clause = re.sub(r"^(release|deployment) provenance (review|audit|check)\b", r"\2 \1 provenance", clause, flags=re.I)
            result.append(clause)
    return "; ".join(result)


def document_is_review_object(clause: str) -> bool:
    """Documentation named as the direct object is not the product under audit.

    References later in the clause ("use README as evidence") do not veto
    a real application review. This is deliberately bounded lexical scoping.
    """
    candidate = normalize(clause.strip())
    header = QUALITY_HEADER.match(candidate)
    return bool(header and DOCUMENT_PRIMARY.match(candidate[header.end():].lstrip()))


def quality_action_clauses(positive: str) -> tuple[str, ...]:
    """Normalize an affirmative review/change head without deciding its domain.

    Rule scope `quality-clause` receives one `quality-review` or
    `quality-change` marker per clause; topical vocabulary remains data-driven.
    """
    clauses = []
    for candidate in normalize(positive).split(";"):
        candidate = candidate.strip()
        header = QUALITY_HEADER.match(candidate)
        if header is None or document_is_review_object(candidate):
            continue
        mutating = bool(re.match(rf"^(?:please\s+|por favor\s+)?{QUALITY_MUTATING_ACTION}\b", candidate))
        marker = "quality-change" if mutating else "quality-review"
        clauses.append(f"{marker} {candidate}")
    return tuple(clauses)


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
        try:
            re.compile(value)
        except (re.error, OverflowError, RecursionError) as error:
            raise ValueError(f"invalid discovery {operator} regex: {error}") from error
    else:
        raise ValueError(f"unknown discovery operator: {operator}")


def _has_path_condition(condition: dict) -> bool:
    operator, value = next(iter(condition.items()))
    if operator == "path":
        return True
    return operator in {"all", "any", "none"} and any(_has_path_condition(child) for child in value)


def validate_registry(registry: dict) -> None:
    if not isinstance(registry, dict) or registry.get("schema") != "discovery-rules/v1" or not isinstance(registry.get("rules"), list):
        raise ValueError("unsupported discovery rule registry")
    ids = set()
    for index, rule in enumerate(registry["rules"]):
        if not isinstance(rule, dict):
            raise ValueError(f"rules.v1.json: rules[{index}] must be an object")
        rid = rule.get("id")
        if not isinstance(rid, str) or not rid or rid in ids:
            raise ValueError(f"invalid or duplicate rule id: {rid}")
        ids.add(rid)
        _validate_condition(rule.get("when"))
        scope = rule.get("scope", "task")
        if not isinstance(scope, str) or scope not in {"task", "clause", "quality-clause"}:
            raise ValueError(f"invalid rule scope: {rid}")
        if scope in {"clause", "quality-clause"} and _has_path_condition(rule["when"]):
            raise ValueError(f"clause-scoped rule cannot inspect unrelated paths: {rid}")
        outputs = rule.get("emit")
        if not isinstance(outputs, list) or not outputs:
            raise ValueError(f"rule {rid} needs outputs")
        for output in outputs:
            if not isinstance(output, str) or not re.fullmatch(r"[a-z]+:[a-z][a-z0-9-]*", output) or output.split(":")[0] not in PREFIXES:
                raise ValueError(f"invalid output in rule {rid}: {output}")


def validate_routes(registry: object) -> dict:
    routes = registry.get("routes") if isinstance(registry, dict) else None
    if not isinstance(routes, dict):
        raise ValueError("invalid discovery route map")
    if "schema" in registry and registry["schema"] != "discovery-routes/v1":
        raise ValueError("routes.v1.json: unsupported schema (expected discovery-routes/v1)")
    for name, route in routes.items():
        location = f"routes.v1.json: routes[{name!r}]"
        if not isinstance(route, dict):
            raise ValueError(f"{location} must be an object")
        for field in ("inspect_first", "avoid"):
            labels = route.get(field, [])
            if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
                raise ValueError(f"{location}.{field} must be an array of strings")
    return routes


def validate_landmarks(registry: object) -> dict:
    if not isinstance(registry, dict) or registry.get("schema") != "discovery-landmarks/v1":
        raise ValueError("unsupported landmarks registry")
    landmarks = registry.get("landmarks")
    if not isinstance(landmarks, dict):
        raise ValueError("landmarks.v1.json: landmarks must be an object")
    for label, patterns in landmarks.items():
        if not isinstance(patterns, list) or not all(isinstance(pattern, str) for pattern in patterns):
            raise ValueError(f"invalid landmark {label}")
        for index, pattern in enumerate(patterns):
            try:
                re.compile(pattern)
            except (re.error, OverflowError, RecursionError) as error:
                raise ValueError(f"invalid landmark regex {label}[{index}]: {error}") from error
    return landmarks


def read_registry(path: Path) -> Any:
    """Read one discovery registry without collapsing repeated JSON members."""
    def unique_members(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        members = {}
        for name, value in pairs:
            if name in members:
                raise ValueError(f"{path.name}: duplicate discovery registry JSON member {name!r}")
            members[name] = value
        return members

    return load_json_with_finite_numbers(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique_members,
        label=f"Discovery registry {path.name}",
    )


def load_registry(name: str = "rules.v1.json") -> dict:
    registry = read_registry(REGISTRY_DIR / name)
    if name == "rules.v1.json":
        validate_registry(registry)
    elif name == "routes.v1.json":
        validate_routes(registry)
    elif name == "landmarks.v1.json":
        validate_landmarks(registry)
    return registry


def _matches(condition: dict, text: str, paths: tuple[str, ...]) -> bool:
    operator, value = next(iter(condition.items()))
    if operator == "text":
        return bool(re.search(value, text))
    if operator == "path":
        return any(re.search(value, path) for path in paths)
    outcomes = (_matches(child, text, paths) for child in value)
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
    quality = quality_action_clauses(text)
    paths = tuple(normalize(path.replace("\\", "/").removeprefix("./")) for path in changed_paths)
    tags: set[str] = set()
    evidence = []

    def matched(rule: dict, candidate: str) -> bool:
        if rule.get("scope") == "quality-clause":
            return any(_matches(rule["when"], clause, ()) for clause in quality if clause)
        if rule.get("scope") == "clause":
            # Each action must satisfy its own positive target AND exclusions.
            # Combining one clause's verb with another's target/negative check
            # creates both false refactors and silently missed code changes.
            return any(_matches(rule["when"], clause.strip(), ()) for clause in candidate.split(";") if clause.strip())
        return _matches(rule["when"], candidate, paths)

    for rule in registry["rules"]:
        is_match = matched(rule, text)
        if is_match:
            tags.update(rule["emit"])
            # A path rule needs an actual path-only match, not just a nonempty
            # changed list, before it receives the higher evidence rank.
            path_match = rule.get("scope") != "clause" and bool(paths) and _matches(rule["when"], "", paths)
            source = "change-structure" if path_match else "text-signal"
            evidence.extend({"source": source, "rank": 350 if path_match else 200,
                             "signal": tag, "value": tag.split(":", 1)[1],
                             "rule_id": rule["id"], "decision": "matched"} for tag in rule["emit"])
        elif text != raw and matched(rule, raw):
            evidence.append({"source": "text-signal", "rank": 200, "signal": "excluded",
                             "value": "negated-clause", "rule_id": rule["id"], "decision": "excluded"})
    return tags, evidence


def discover_landmarks(paths: list[str], *, registry: dict | None = None) -> dict[str, list[str]]:
    if registry is None:
        landmarks = load_registry("landmarks.v1.json")["landmarks"]
    else:
        landmarks = validate_landmarks(registry)
    result = {}
    for label, patterns in landmarks.items():
        result[label] = [p for p in paths if any(re.search(pattern, normalize(p)) for pattern in patterns)]
    return result
