"""Catalog-wide local search and typed discovery graph (no hosted index)."""
from __future__ import annotations

from collections import Counter
from datetime import date
import json
import math
from pathlib import Path
import re

from .canonical import stable_hash
from .discovery_rules import normalize, validate_registry
from .visual_directions import CATALOG_PATH as VISUAL_CATALOG_PATH, load_visual_catalog

SCHEMA = "handbook-discovery/v1"
GOVERNED_KINDS = {"governance", "policy", "standard", "pattern", "playbook", "reference"}
INDEXED_KINDS = GOVERNED_KINDS | {"decision", "template", "entrypoint", "contribution-guide", "brand-contract"}
HISTORICAL = {"superseded", "retired", "archived", "proposed", "draft"}
EDGE_TYPES = {"requires", "related", "supersedes", "amends", "conflicts", "contains", "projects", "activates", "selects"}
STOPWORDS = set("a an and or of the to for in on with is as by all de del la el las los un una unos unas para por con y o en al que como this este esta".split())


def _inline_list(value: str) -> list[str]:
    return [v.strip().strip('"\'') for v in value[1:-1].split(",") if v.strip()]


def read_catalog(root: Path) -> list[dict]:
    """Parse the deliberately small catalog YAML subset, refusing other syntax."""
    path = root / "machine-readable/catalog.yaml"
    if not path.exists():
        return []
    result, current = [], None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#") or line.startswith(("version:", "documents:")):
            continue
        start = re.fullmatch(r"  - id: ([a-z0-9-]+)", line)
        if start:
            current = {"id": start[1]}; result.append(current); continue
        match = re.fullmatch(r"    (kind|path|status|applies_to): (.+)", line)
        if not current or not match:
            raise ValueError(f"unsupported catalog syntax at line {number}")
        key, value = match.groups()
        if key in current:
            raise ValueError(f"duplicate catalog field at line {number}")
        if key == "applies_to":
            if not value.startswith("[") or not value.endswith("]"):
                raise ValueError("catalog applies_to must be an inline list")
            value = _inline_list(value)
        else:
            value = value.strip('"\'')
        current[key] = value
    ids, paths = set(), set()
    for item in result:
        if not {"id", "kind", "path", "status", "applies_to"}.issubset(item):
            raise ValueError(f"incomplete catalog record: {item['id']}")
        if item["id"] in ids or item["path"] in paths:
            raise ValueError(f"duplicate catalog identity: {item['id']}")
        ids.add(item["id"]); paths.add(item["path"])
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts or "\\" in item["path"]:
            raise ValueError(f"unsafe catalog path: {relative}")
    return result


def require_visual_bundle(bundle: dict) -> None:
    """Keep the standalone visual registry in portable Codex skill snapshots."""
    if "machine-readable/visual-directions.v1.json" not in bundle.get("include", []):
        raise ValueError("portable bundle omits visual-direction catalog")


def _source_references(value: str, items: str) -> list[str] | None:
    value = value.strip()
    if items:
        if value:
            return None
        members = re.findall(r"^[ \t]*-[ \t]+(.+)$", items, re.M)
    elif value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        members = inner.removesuffix(",").split(",") if inner else []
    elif value:
        members = [value]
    else:
        return None
    references = []
    for member in members:
        member = member.strip()
        if len(member) >= 2 and member[0] in "\"'" and member[-1] == member[0]:
            member = member[1:-1]
        if not re.fullmatch(r"[^\s\x22\x27\[\]{},:]+", member):
            return None
        references.append(member)
    return references


def document_metadata(text: str) -> dict[str, str | list[str]]:
    front = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not front:
        return {}
    fields = {}
    for key, value, items in re.findall(r"^([a-z_]+):[ \t]*([^\n]*)((?:\n[ \t]*-[ \t]+[^\n]+)*)", front[1], re.M):
        if key == "applies_to" and value.strip().startswith("[") and value.strip().endswith("]"):
            fields[key] = _inline_list(value.strip())
        elif key == "applies_to" and not value.strip() and items:
            fields[key] = [item.strip().strip('"\'') for item in re.findall(r"^[ \t]*-[ \t]+(.+)$", items, re.M)]
        elif key == "sources":
            references = None if key in fields else _source_references(value, items)
            fields[key] = references if references is not None else value
        else:
            fields[key] = value
    return fields


def _is_decision(item: dict) -> bool:
    return item["kind"] == "decision" or item["path"].startswith("decisions/")


def _decision_metadata_problems(item: dict, text: str) -> list[str]:
    if item["kind"] != "decision":
        return [f"metadata mismatch: {item['id']}:kind"]
    fields = document_metadata(text)
    return [
        f"metadata mismatch: {item['id']}:{key}"
        for key in ("id", "kind", "status")
        if (key == "status" or key in fields) and fields.get(key) != item[key]
    ]


def _source_review_date(value: str) -> date | None:
    # The registry accepts plain scalars and a matching pair of YAML quotes.
    match = re.fullmatch(r'''(["']?)([0-9]{4}-[0-9]{2}-[0-9]{2})\1''', value.strip())
    if match:
        try:
            return date.fromisoformat(match[2])
        except ValueError:
            pass
    return None


def check_integrity(root: Path) -> list[str]:
    """Portable canonical-repository integrity checks; not an installed-file audit."""
    problems = []
    try:
        catalog = read_catalog(root)
        source_text = (root / "machine-readable/sources.yaml").read_text(encoding="utf-8")
        source_ids = re.findall(r"^  - id: (\S+)\s*$", source_text, re.M)
        registered_source_ids = set(source_ids)
        if len(source_ids) != len(registered_source_ids):
            problems.append("duplicate source id")
        source_sections = re.split(r"^  - id: ", source_text, flags=re.M)[1:]
        required_source_fields = {"title", "tier", "kind", "url", "canonical_language", "applies_to", "status", "last_verified", "review_due", "volatility", "reuse"}
        for section in source_sections:
            source_id = section.splitlines()[0]
            fields = dict(re.findall(r"^    ([a-z_]+):[ \t]*(.+)$", section, re.M))
            missing = required_source_fields - fields.keys()
            if missing:
                problems.append("source missing fields: " + source_id + ": " + ", ".join(sorted(missing)))
            if fields.get("tier") not in {"A", "B", "C", "D"}:
                problems.append("invalid source tier: " + source_id)
            dates = {key: _source_review_date(fields[key]) for key in ("last_verified", "review_due") if key in fields}
            for key, value in dates.items():
                if value is None:
                    problems.append(f"invalid-source-date:{source_id}:{key}")
            verified, due = dates.get("last_verified"), dates.get("review_due")
            if verified and due and due < verified:
                problems.append(f"source-review-precedes-verification:{source_id}")
        for item in catalog:
            path = root / item["path"]
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                problems.append("missing or unsafe catalog path: " + item["path"]); continue
            if path.suffix != ".md":
                continue
            text = path.read_text(encoding="utf-8")
            is_governed = item["kind"] in GOVERNED_KINDS
            is_decision = _is_decision(item)
            fields = document_metadata(text) if is_governed or is_decision else {}
            if is_governed:
                required = {"id", "kind", "status", "owner", "version", "applies_to", "sources", "last_verified", "review_due"}
                if not required.issubset(fields):
                    problems.append("missing normative metadata: " + item["id"])
                for key in ("id", "kind", "status"):
                    if fields.get(key) != item[key]:
                        problems.append("metadata mismatch: " + item["id"] + ":" + key)
                if item["status"] == "active":
                    scope = fields.get("applies_to")
                    if not isinstance(scope, list) or set(scope) != set(item["applies_to"]):
                        problems.append(f"metadata mismatch: {item['id']}:applies_to")
            if is_decision:
                problems.extend(_decision_metadata_problems(item, text))
            if is_governed or is_decision:
                references = set(re.findall(r"\bsrc-[a-z0-9][a-z0-9-]*\b", text))
                if "sources" in fields:
                    declared = fields["sources"]
                    if isinstance(declared, list):
                        references.update(declared)
                    else:
                        problems.append(f"invalid-source-references:{item['id']}")
                problems.extend("unknown source: " + item["id"] + ":" + uid for uid in sorted(references - registered_source_ids))
        bundle = json.loads((root / "agent-config/codex/skills/engineering-handbook/bundle.json").read_text(encoding="utf-8"))
        if bundle.get("schema_version") != 1 or bundle.get("skill_name") != "engineering-handbook":
            problems.append("unsupported skill bundle")
        require_visual_bundle(bundle)
        for include in bundle.get("include", []):
            path = root / include
            if Path(include).is_absolute() or ".." in Path(include).parts or not path.exists():
                problems.append("missing or unsafe bundle include: " + include)
        load_visual_catalog(root)
    except (ValueError, OSError, KeyError) as exc:
        problems.append(str(exc))
    return problems


def validate_edges(nodes: set[str], edges: list[dict]) -> None:
    dependencies = {kind: {} for kind in ("requires", "supersedes")}
    relations = set()
    for edge in edges:
        source, target, kind = edge.get("from"), edge.get("to"), edge.get("type")
        if source not in nodes or target not in nodes or kind not in EDGE_TYPES or source == target:
            raise ValueError(f"invalid discovery edge: {edge}")
        relations.add((source, target, kind))
        if kind in dependencies:
            dependencies[kind].setdefault(source, []).append(target)
    for source, target, kind in relations:
        if kind == "requires" and ((source, target, "conflicts") in relations or (target, source, "conflicts") in relations):
            raise ValueError(f"conflicting required dependency: {source} -> {target}")
    for kind, graph in dependencies.items():
        done, visiting = set(), set()
        def visit(node):
            if node in visiting:
                raise ValueError(f"cyclic {kind} dependency: {node}")
            if node in done:
                return
            visiting.add(node)
            for child in graph.get(node, []):
                visit(child)
            visiting.remove(node); done.add(node)
        for node in graph:
            visit(node)


def _terms(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", normalize(text)) if len(t) > 1 and t not in STOPWORDS]


def build_discovery(root: Path, units: dict | None = None) -> dict:
    catalog = read_catalog(root)
    registry_dir = root / "machine-readable/discovery"
    registries = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in sorted(registry_dir.glob("*.json"))}
    if "rules.v1.json" in registries:
        validate_registry(registries["rules.v1.json"])
    taxonomy = registries.get("taxonomy.v1.json", {"topics": [], "edges": []})
    documents, nodes, edges = [], [], list(taxonomy.get("edges", []))
    aliases = {}
    for topic in taxonomy.get("topics", []):
        nodes.append({"id": "topic:" + topic["id"], "type": "topic", "title": topic["title"]})
        for artifact in topic["artifacts"]:
            aliases.setdefault(artifact, []).extend([topic["title"], *topic.get("aliases", [])])
            edges.append({"from": "topic:" + topic["id"], "to": artifact, "type": "contains"})
    for item in sorted(catalog, key=lambda item: item["id"]):
        text = ""
        source_hash = None
        path = root / item["path"]
        is_decision = _is_decision(item)
        is_markdown = path.suffix == ".md" and (is_decision or item["kind"] in INDEXED_KINDS)
        is_source_registry = (
            item["path"] in {"machine-readable/sources.yaml", VISUAL_CATALOG_PATH.as_posix()}
            or (item["path"] == "machine-readable/discovery/routes.v1.json" and "routes.v1.json" in registries)
        )
        if is_markdown or is_source_registry:
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError(f"missing or unsafe catalog source: {item['path']}")
            content = path.read_text(encoding="utf-8")
            source_hash = stable_hash(content) if content or is_source_registry else None
            if is_markdown:
                text = content
            if is_decision:
                problems = _decision_metadata_problems(item, text)
                if problems:
                    raise ValueError("; ".join(problems))
        heading = re.search(r"^#\s+(.+)$", text, re.M)
        title = heading[1] if heading else item["id"].replace("-", " ")
        keywords = " ".join([item["id"], item["path"], title, *item["applies_to"], *aliases.get(item["id"], [])])
        terms = Counter(_terms(text))
        terms.update({key: value * 7 for key, value in Counter(_terms(keywords)).items()})
        plain = re.sub(r"```.*?```", "", text, flags=re.S)
        plain = re.sub(r"^---.*?---", "", plain, count=1, flags=re.S)
        excerpt = re.sub(r"\s+", " ", plain).strip()[:260]
        amended_by = sorted(e["from"] for e in taxonomy.get("edges", []) if e["to"] == item["id"] and e["type"] == "amends")
        documents.append({**item, "title": title, "amended_by": amended_by, "terms": dict(sorted(terms.items())), "length": sum(terms.values()),
                          "excerpt": excerpt, "source_hash": source_hash})
        nodes.append({"id": item["id"], "type": item["kind"], "path": item["path"], "status": item["status"]})
    # Links are navigation, not implicit normative dependencies.
    by_path = {str((root / item["path"]).resolve()): item["id"] for item in catalog}
    for item in documents:
        path = root / item["path"]
        if item["source_hash"] is None or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            local = link.split("#", 1)[0]
            target = by_path.get(str((path.parent / local).resolve())) if local and "://" not in local else None
            if target and target != item["id"]:
                edges.append({"from": item["id"], "to": target, "type": "related"})
    predicates = set()
    for rule in registries.get("rules.v1.json", {}).get("rules", []):
        rid = "rule:" + rule["id"]
        nodes.append({"id": rid, "type": "trigger", "condition": rule["when"]})
        for tag in rule["emit"]:
            predicates.add(tag)
            edges.append({"from": rid, "to": "predicate:" + tag, "type": "activates"})
    for uid, unit in sorted((units or {}).items()):
        nodes.append({"id": "unit:" + uid, "type": "context-unit", "phase": unit.get("phase", [])})
        if unit.get("source") in {doc["id"] for doc in documents}:
            edges.append({"from": unit["source"], "to": "unit:" + uid, "type": "projects"})
        for tag in [*unit.get("activate_when", []), *unit.get("activate_all", [])]:
            predicates.add(tag)
            edges.append({"from": "predicate:" + tag, "to": "unit:" + uid, "type": "selects"})
        for dependency in unit.get("requires", []):
            edges.append({"from": "unit:" + uid, "to": "unit:" + dependency, "type": "requires"})
    nodes.extend({"id": "predicate:" + p, "type": "predicate"} for p in sorted(predicates))
    edges = [dict(zip(("from", "to", "type"), value)) for value in sorted({(e["from"], e["to"], e["type"]) for e in edges})]
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate discovery node")
    validate_edges(set(ids), edges)
    catalog_path = root / "machine-readable/catalog.yaml"
    result = {"schema": SCHEMA, "catalog_hash": stable_hash(catalog),
              "catalog_source_hash": stable_hash(catalog_path.read_text(encoding="utf-8")) if catalog_path.is_file() else None,
              "registry_hashes": {k: stable_hash(v) for k, v in registries.items()},
              "documents": documents, "topics": taxonomy.get("topics", []), "nodes": sorted(nodes, key=lambda n: n["id"]), "edges": edges}
    if "routes.v1.json" in registries:
        routes = registries["routes.v1.json"].get("routes")
        if not isinstance(routes, dict):
            raise ValueError("invalid discovery route map")
        # JSON object keys are sorted by stable_hash, but route priority is ordered.
        result["route_order"] = list(routes)
    result["index_hash"] = stable_hash(result)
    return result


def search(index: dict, query: str, *, limit: int = 8, historical: bool = False) -> list[dict]:
    query_terms = set(_terms(query))
    documents = [doc for doc in index["documents"] if historical or doc["status"] not in HISTORICAL]
    avg = sum(doc["length"] for doc in documents) / max(1, len(documents))
    frequencies = {term: sum(term in doc["terms"] for doc in documents) for term in query_terms}
    results = []
    for doc in documents:
        matched = sorted(query_terms & doc["terms"].keys())
        if not matched:
            continue
        score = 0.0
        for term in matched:
            frequency = doc["terms"][term]
            idf = math.log(1 + (len(documents) - frequencies[term] + 0.5) / (frequencies[term] + 0.5))
            score += idf * frequency * 2.2 / (frequency + 1.2 * (0.25 + 0.75 * doc["length"] / max(1, avg)))
        # Prefer satisfying a multi-word query over one ubiquitous term.
        score *= len(matched) / max(1, len(query_terms))
        results.append({key: doc[key] for key in ("id", "title", "path", "kind", "status", "excerpt", "amended_by")} | {"score": round(score, 6), "matched_terms": matched, "method": "local-lexical-bm25"})
    return sorted(results, key=lambda result: (-result["score"], result["id"]))[:max(0, min(limit, 100))]


def knowledge_tree(index: dict, *, historical: bool = False) -> dict:
    documents = {doc["id"]: {k: doc[k] for k in ("id", "title", "kind", "path", "status")} for doc in index["documents"] if historical or doc["status"] not in HISTORICAL}
    assigned = set()
    groups = []
    for topic in index["topics"]:
        members = [documents[uid] for uid in topic["artifacts"] if uid in documents]
        assigned.update(item["id"] for item in members)
        groups.append({"id": topic["id"], "title": topic["title"], "children": members})
    remainder = {}
    for uid, doc in documents.items():
        if uid not in assigned:
            remainder.setdefault(doc["kind"], []).append(doc)
    groups.extend({"id": kind, "title": kind, "children": children} for kind, children in sorted(remainder.items()))
    return {"kind": "knowledge", "children": groups, "count": len(documents)}
