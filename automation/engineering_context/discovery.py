"""Catalog-wide local search and typed discovery graph (no hosted index)."""
from __future__ import annotations

from collections import Counter
from datetime import date
import json
import math
from pathlib import Path
import re
from string import ascii_lowercase, ascii_uppercase

from .canonical import stable_hash
from .discovery_rules import normalize, read_registry, validate_landmarks, validate_registry, validate_routes
from .handbook_source import AGENT_CONTEXT_OPEN
from .visual_directions import CATALOG_PATH as VISUAL_CATALOG_PATH, load_visual_catalog, parse_visual_catalog

_ASCII_CASE_FOLD = str.maketrans(ascii_uppercase, ascii_lowercase)

SCHEMA = "handbook-discovery/v1"
GOVERNED_KINDS = {"governance", "policy", "standard", "pattern", "playbook", "reference"}
INDEXED_KINDS = GOVERNED_KINDS | {"decision", "template", "entrypoint", "contribution-guide", "brand-contract"}
HISTORICAL = {"superseded", "retired", "archived", "proposed", "draft"}
GOVERNED_STATUSES = HISTORICAL | {"active", "deprecated"}
EDGE_TYPES = {"requires", "related", "supersedes", "amends", "conflicts", "contains", "projects", "activates", "selects"}
STOPWORDS = set("a an and or of the to for in on with is as by all de del la el las los un una unos unas para por con y o en al que como this este esta".split())


def _inline_list(value: str) -> list[str]:
    return [v.strip().strip('"\'') for v in value[1:-1].split(",") if v.strip()]


def read_catalog_snapshot(root: Path) -> tuple[list[dict], str | None]:
    """Parse the supported catalog YAML and hash the same source text."""
    path = root / "machine-readable/catalog.yaml"
    if not path.exists():
        return [], None
    text = path.read_text(encoding="utf-8")
    result, current = [], None
    headers: set[str] = set()
    rows_closed = False
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(("version:", "documents:")):
            key, _, value = line.partition(":")
            if key in headers:
                raise ValueError(f"duplicate catalog header {key} at line {number}")
            if key == "documents":
                if result:
                    raise ValueError(f"catalog documents header follows records at line {number}")
                value = re.split(r"[ \t]+#", value, maxsplit=1)[0].strip()
                if value and not re.fullmatch(r"\[[ \t]*\]", value):
                    raise ValueError(f"unsupported catalog documents value at line {number}")
                rows_closed = bool(value)
            else:
                rows_closed = "documents" in headers or bool(result)
            headers.add(key)
            current = None
            continue
        start = re.fullmatch(r"  - id: ([a-z0-9-]+)", line)
        if start:
            if rows_closed:
                raise ValueError(f"catalog record outside documents at line {number}")
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
    ids: set[str] = set()
    paths: dict[str, str] = {}
    for item in result:
        if not {"id", "kind", "path", "status", "applies_to"}.issubset(item):
            raise ValueError(f"incomplete catalog record: {item['id']}")
        path = item["path"]
        # Fold ASCII aliases without conflating distinct Unicode file names.
        path_identity = path.translate(_ASCII_CASE_FOLD)
        if item["id"] in ids or paths.get(path_identity) == path:
            raise ValueError(f"duplicate catalog identity: {item['id']}")
        if path_identity in paths:
            raise ValueError(f"case-colliding catalog paths: {paths[path_identity]} and {path}")
        ids.add(item["id"])
        paths[path_identity] = path
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts or "\\" in path:
            raise ValueError(f"unsafe catalog path: {relative}")
        if relative.as_posix() != path:
            raise ValueError(f"noncanonical catalog path: {path}")
        if item["kind"] in GOVERNED_KINDS and item["status"] not in GOVERNED_STATUSES:
            raise ValueError(f"invalid governed catalog status: {item['id']}: {item['status']}")
    return result, stable_hash(text)


def read_catalog(root: Path) -> list[dict]:
    rows, _ = read_catalog_snapshot(root)
    return rows


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


def _parse_document_metadata(text: str, artifact_id: str) -> tuple[dict[str, str | list[str]], list[str]]:
    front = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not front:
        return {}, []
    fields = {}
    repeated_identity = set()
    for key, value, items in re.findall(r"^([a-z_]+):[ \t]*([^\n]*)((?:\n[ \t]*-[ \t]+[^\n]+)*)", front[1], re.M):
        if key in ("id", "kind", "status") and key in fields:
            repeated_identity.add(key)
        if key == "applies_to" and value.strip().startswith("[") and value.strip().endswith("]"):
            fields[key] = _inline_list(value.strip())
        elif key == "applies_to" and not value.strip() and items:
            fields[key] = [item.strip().strip('"\'') for item in re.findall(r"^[ \t]*-[ \t]+(.+)$", items, re.M)]
        elif key == "sources":
            references = None if key in fields else _source_references(value, items)
            fields[key] = references if references is not None else value
        else:
            fields[key] = value
    problems = [f"duplicate-frontmatter-identity:{artifact_id}:{key}" for key in sorted(repeated_identity)]
    return fields, problems


def document_metadata(text: str, *, artifact_id: str = "document") -> dict[str, str | list[str]]:
    fields, problems = _parse_document_metadata(text, artifact_id)
    if problems:
        raise ValueError("; ".join(problems))
    return fields


def _is_decision(item: dict) -> bool:
    return item["kind"] == "decision" or item["path"].startswith("decisions/")


def _decision_metadata_problems(item: dict, fields: dict) -> list[str]:
    if item["kind"] != "decision":
        return [f"metadata mismatch: {item['id']}:kind"]
    return [
        f"metadata mismatch: {item['id']}:{key}"
        for key in ("id", "kind", "status")
        if (key == "status" or key in fields) and fields.get(key) != item[key]
    ]


def _governed_declared_identity_problems(item: dict, fields: dict, text: str) -> list[str]:
    prose_only = AGENT_CONTEXT_OPEN not in text
    problems = []
    for key in ("id", "kind", "status"):
        if key not in fields:
            continue
        expected = item[key]
        value = fields[key]
        if value == expected:
            continue
        # Indexed prose can use surrounding whitespace or one matching pair of scalar quotes.
        if prose_only and value.strip() in (expected, f'"{expected}"', f"'{expected}'"):
            continue
        problems.append(f"metadata mismatch: {item['id']}:{key}")
    return problems


def _review_date(value: str) -> date | None:
    # Accept plain scalars and a matching pair of YAML quotes.
    match = re.fullmatch(r'''(["']?)([0-9]{4}-[0-9]{2}-[0-9]{2})\1''', value.strip())
    if match:
        try:
            return date.fromisoformat(match[2])
        except ValueError:
            pass
    return None


def _review_date_problems(fields: dict, subject: str, identity: str) -> list[str]:
    dates = {key: _review_date(fields[key]) for key in ("last_verified", "review_due") if key in fields}
    problems = [f"invalid-{subject}-date:{identity}:{key}" for key, value in dates.items() if value is None]
    verified, due = dates.get("last_verified"), dates.get("review_due")
    if verified and due and due < verified:
        problems.append(f"{subject}-review-precedes-verification:{identity}")
    return problems


def _catalog_spelling_matches(root: Path, relative: str, directory_names: dict[str, set[str]]) -> bool:
    # Compare lexical entries so a correctly named, confined directory alias still works.
    parent = root
    for part in relative.split("/"):
        key = str(parent)
        if key not in directory_names:
            directory_names[key] = {entry.name for entry in parent.iterdir()}
        if part not in directory_names[key]:
            return False
        parent = parent / part
    return True


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
        known_source_fields = required_source_fields | {"id", "license", "revision", "version"}
        for section in source_sections:
            source_id = section.splitlines()[0]
            # Repeated declarations are ambiguous even if one value is blank.
            declarations = Counter(key.lower() for key in re.findall(r"^    ([A-Za-z_]+):", section, re.M))
            declarations["id"] += 1
            problems.extend(
                f"duplicate-source-field:{source_id}:{key}"
                for key in sorted(known_source_fields) if declarations[key] > 1
            )
            fields = dict(re.findall(r"^    ([a-z_]+):[ \t]*(.+)$", section, re.M))
            missing = required_source_fields - fields.keys()
            if missing:
                problems.append("source missing fields: " + source_id + ": " + ", ".join(sorted(missing)))
            if fields.get("tier") not in {"A", "B", "C", "D"}:
                problems.append("invalid source tier: " + source_id)
            problems.extend(_review_date_problems(fields, "source", source_id))
        directory_names: dict[str, set[str]] = {}
        for item in catalog:
            path = root / item["path"]
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                problems.append("missing or unsafe catalog path: " + item["path"]); continue
            if not _catalog_spelling_matches(root, item["path"], directory_names):
                problems.append("catalog path spelling differs from disk: " + item["path"])
                continue
            if path.suffix.lower() != ".md":
                continue
            text = path.read_text(encoding="utf-8")
            is_governed = item["kind"] in GOVERNED_KINDS
            is_decision = _is_decision(item)
            fields, identity_problems = (
                _parse_document_metadata(text, item["id"]) if is_governed or is_decision else ({}, [])
            )
            problems.extend(identity_problems)
            if is_governed:
                required = {"id", "kind", "status", "owner", "version", "applies_to", "sources", "last_verified", "review_due"}
                if not required.issubset(fields):
                    problems.append("missing normative metadata: " + item["id"])
                for key in ("id", "kind", "status"):
                    if fields.get(key) != item[key]:
                        problems.append("metadata mismatch: " + item["id"] + ":" + key)
                if item["status"] == "active":
                    problems.extend(_review_date_problems(fields, "document", item["id"]))
                    scope = fields.get("applies_to")
                    if not isinstance(scope, list) or set(scope) != set(item["applies_to"]):
                        problems.append(f"metadata mismatch: {item['id']}:applies_to")
            if is_decision:
                problems.extend(_decision_metadata_problems(item, fields))
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


def _validate_dependency_graph(kind: str, graph: dict[str, list[str]]) -> None:
    done: set[str] = set()
    active: set[str] = set()
    for start in graph:
        if start in done:
            continue
        active.add(start)
        stack = [(start, iter(graph[start]))]
        while stack:
            node, children = stack[-1]
            target = next(children, None)
            if target is None:
                stack.pop()
                active.remove(node)
                done.add(node)
            elif target in active:
                raise ValueError(f"cyclic {kind} dependency: {target}")
            elif target not in done:
                active.add(target)
                stack.append((target, iter(graph.get(target, ()))))


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
    for edge in edges:
        source, target, kind = edge["from"], edge["to"], edge["type"]
        if kind == "requires" and ((source, target, "conflicts") in relations or (target, source, "conflicts") in relations):
            raise ValueError(f"conflicting required dependency: {source} -> {target}")
    for kind, graph in dependencies.items():
        _validate_dependency_graph(kind, graph)


def _terms(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", normalize(text)) if len(t) > 1 and t not in STOPWORDS]


_FRONTMATTER = re.compile(r"^---.*?---", re.S)
_LIST_OR_ROOT_HEADING = re.compile(
    r"^(?:(?P<heading>#{1,6})(?=[ \t]|$)|[ \t]*(?:[-+*]|[0-9]{1,9}[.)])(?:[ \t]+|$)(?P<fence>`{3,}|~{3,})?)",
    re.M,
)


def _markdown_text_views(text: str) -> tuple[str, str]:
    """Return excerpt prose and the source for local related-link discovery."""
    spans: list[tuple[int, int]] = []
    start = 0
    fence = ""
    for match in re.finditer(r"^ {0,3}(`{3,}|~{3,})([^\n]*)$", text, re.M):
        marker, trailing = match.groups()
        if fence:
            if marker.startswith(fence) and not trailing.strip():
                fence = ""
                start = match.end()
        elif marker.startswith("~") or "`" not in trailing:
            spans.append((start, match.start()))
            fence = marker
    if not fence:
        spans.append((start, len(text)))

    chunks = [text[start:end] for start, end in spans]
    prose = _FRONTMATTER.sub("", "".join(chunks), count=1)
    if "](" in text:
        frontmatter = _FRONTMATTER.match(text)
        body_start = frontmatter.end() if frontmatter else 0
        saw_list = False
        for index, (start, end) in enumerate(spans):
            direct_fence = False
            for item in _LIST_OR_ROOT_HEADING.finditer(text, max(start, body_start), end):
                if item["heading"]:
                    saw_list = False
                    continue
                saw_list = True
                if item["fence"]:
                    direct_fence = True
                    break
            if direct_fence or (saw_list and text[end:end + 1] == " "):
                # A standalone-fence scan can mask visible links past a list fence.
                # Keep its known prefix, then recover source links from the ambiguous span.
                links = "".join(chunks[:index]) + text[start:]
                return prose, _FRONTMATTER.sub("", links, count=1)
    return prose, prose


def _taxonomy_edges(taxonomy: dict) -> list[dict]:
    edges = taxonomy.get("edges", [])
    if not isinstance(edges, list):
        raise ValueError("taxonomy.v1.json: edges must be a list")
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise ValueError(f"taxonomy.v1.json: edges[{index}] must be an object")
        for field in ("from", "to", "type"):
            if not isinstance(edge.get(field), str):
                raise ValueError(f"taxonomy.v1.json: edges[{index}].{field} must be a string")
    return edges


def _taxonomy_topics(taxonomy: dict) -> list[dict]:
    topics = taxonomy.get("topics", [])
    if not isinstance(topics, list):
        raise ValueError("taxonomy.v1.json: topics must be a list")
    for index, topic in enumerate(topics):
        location = f"taxonomy.v1.json: topics[{index}]"
        if not isinstance(topic, dict):
            raise ValueError(f"{location} must be an object")
        for field in ("id", "title"):
            value = topic.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{location}.{field} must be a nonblank string")
        for field, values in (("artifacts", topic.get("artifacts")), ("aliases", topic.get("aliases", []))):
            if not isinstance(values, list):
                raise ValueError(f"{location}.{field} must be a list")
            for member_index, value in enumerate(values):
                if not isinstance(value, str):
                    raise ValueError(f"{location}.{field}[{member_index}] must be a string")
    return [topic | {"artifacts": list(dict.fromkeys(topic["artifacts"]))} for topic in topics]


def build_discovery(
    root: Path,
    units: dict | None = None,
    *,
    catalog_snapshot: tuple[list[dict], str | None] | None = None,
) -> dict:
    if catalog_snapshot is None:
        catalog_snapshot = read_catalog_snapshot(root)
    catalog, catalog_source_hash = catalog_snapshot
    resolved_root = root.resolve()
    registry_dir = root / "machine-readable/discovery"
    registries = {p.name: read_registry(p) for p in sorted(registry_dir.glob("*.json"))}
    if "rules.v1.json" in registries:
        validate_registry(registries["rules.v1.json"])
    if "landmarks.v1.json" in registries:
        validate_landmarks(registries["landmarks.v1.json"])
    taxonomy = registries.get("taxonomy.v1.json", {"topics": [], "edges": []})
    if not isinstance(taxonomy, dict):
        raise ValueError("taxonomy.v1.json must be an object")
    if "schema" in taxonomy and taxonomy["schema"] != "discovery-taxonomy/v1":
        raise ValueError("taxonomy.v1.json: unsupported schema (expected discovery-taxonomy/v1)")
    declared_edges = _taxonomy_edges(taxonomy)
    topics = _taxonomy_topics(taxonomy)
    documents, nodes, edges = [], [], list(declared_edges)
    related_links: list[tuple[str, Path, str]] = []
    aliases = {}
    for topic in topics:
        nodes.append({"id": "topic:" + topic["id"], "type": "topic", "title": topic["title"]})
        for artifact in topic["artifacts"]:
            aliases.setdefault(artifact, []).extend([topic["title"], *topic.get("aliases", [])])
            edges.append({"from": "topic:" + topic["id"], "to": artifact, "type": "contains"})
    directory_names: dict[str, set[str]] = {}
    for item in sorted(catalog, key=lambda item: item["id"]):
        text = ""
        source_hash = None
        path = root / item["path"]
        is_decision = _is_decision(item)
        is_markdown = path.suffix.lower() == ".md" and (is_decision or item["kind"] in INDEXED_KINDS)
        is_source_registry = (
            item["path"] in {"machine-readable/sources.yaml", VISUAL_CATALOG_PATH.as_posix()}
            or (item["path"] == "machine-readable/discovery/routes.v1.json" and "routes.v1.json" in registries)
        )
        if is_markdown or is_source_registry:
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(resolved_root):
                raise ValueError(f"missing or unsafe catalog source: {item['path']}")
            if not _catalog_spelling_matches(root, item["path"], directory_names):
                raise ValueError(f"catalog path spelling differs from disk: {item['path']}")
            content = path.read_text(encoding="utf-8")
            if item["path"] == VISUAL_CATALOG_PATH.as_posix():
                parse_visual_catalog(content, resolved_root=resolved_root)
            source_hash = stable_hash(content) if content or is_source_registry else None
            if is_markdown:
                text = content
            if is_decision or (is_markdown and item["kind"] in GOVERNED_KINDS):
                fields = document_metadata(text, artifact_id=item["id"])
                if is_decision:
                    problems = _decision_metadata_problems(item, fields)
                else:
                    problems = _governed_declared_identity_problems(item, fields, text)
                if problems:
                    raise ValueError("; ".join(problems))
        heading = re.search(r"^#(?![ \t]+#+[ \t]*$)[ \t][^\S\r\n]*(\S.*)$", text, re.M)
        title = heading[1] if heading else item["id"].replace("-", " ")
        keywords = " ".join([item["id"], item["path"], title, *item["applies_to"], *aliases.get(item["id"], [])])
        terms = Counter(_terms(text))
        terms.update({key: value * 7 for key, value in Counter(_terms(keywords)).items()})
        plain, link_source = _markdown_text_views(text)
        excerpt = re.sub(r"\s+", " ", plain).strip()[:260]
        amended_by = sorted({
            edge["from"] for edge in declared_edges
            if edge["to"] == item["id"] and edge["type"] == "amends"
        })
        documents.append({**item, "title": title, "amended_by": amended_by, "terms": dict(sorted(terms.items())), "length": sum(terms.values()),
                          "excerpt": excerpt, "source_hash": source_hash})
        nodes.append({"id": item["id"], "type": item["kind"], "path": item["path"], "status": item["status"]})
        if is_markdown:
            for link in re.findall(r"\]\(([^)]+)\)", link_source):
                local = link.split("#", 1)[0]
                if local and "://" not in local:
                    related_links.append((item["id"], path.parent, local))
    # Links are navigation, not implicit normative dependencies.
    by_path = {str((root / item["path"]).resolve()): item["id"] for item in catalog}
    for source, parent, local in related_links:
        target = by_path.get(str((parent / local).resolve()))
        if target and target != source:
            edges.append({"from": source, "to": target, "type": "related"})
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
    # Topic memberships point to catalog documents, even when another graph node exists.
    catalog_ids = {item["id"] for item in catalog}
    for topic in topics:
        for artifact in topic["artifacts"]:
            if artifact not in catalog_ids:
                edge = {"from": "topic:" + topic["id"], "to": artifact, "type": "contains"}
                raise ValueError(f"invalid discovery edge: {edge}")
    result = {"schema": SCHEMA, "catalog_hash": stable_hash(catalog),
              "catalog_source_hash": catalog_source_hash,
              "registry_hashes": {k: stable_hash(v) for k, v in registries.items()},
              "documents": documents, "topics": topics, "nodes": sorted(nodes, key=lambda n: n["id"]), "edges": edges}
    if "routes.v1.json" in registries:
        routes = validate_routes(registries["routes.v1.json"])
        # JSON object keys are sorted by stable_hash, but route priority is ordered.
        result["route_order"] = list(routes)
    result["index_hash"] = stable_hash(result)
    return result


def search(index: dict, query: str, *, limit: int = 8, historical: bool = False) -> list[dict]:
    exact_id = query.strip().translate(_ASCII_CASE_FOLD)
    query_terms = set(_terms(query))
    all_documents = index["documents"]
    hidden = set() if historical else {doc["id"] for doc in all_documents if doc["status"] in HISTORICAL}
    documents = [doc for doc in all_documents if doc["id"] not in hidden]
    avg = sum(doc["length"] for doc in documents) / max(1, len(documents))
    frequencies = {term: sum(term in doc["terms"] for doc in documents) for term in query_terms}
    results = []
    for doc in documents:
        matched = sorted(query_terms & doc["terms"].keys())
        if not matched and doc["id"] != exact_id:
            continue
        score = 0.0
        for term in matched:
            frequency = doc["terms"][term]
            idf = math.log(1 + (len(documents) - frequencies[term] + 0.5) / (frequencies[term] + 0.5))
            score += idf * frequency * 2.2 / (frequency + 1.2 * (0.25 + 0.75 * doc["length"] / max(1, avg)))
        # Prefer satisfying a multi-word query over one ubiquitous term.
        score *= len(matched) / max(1, len(query_terms))
        hit = {key: doc[key] for key in ("id", "title", "path", "kind", "status", "excerpt")}
        hit["amended_by"] = [artifact for artifact in doc["amended_by"] if artifact not in hidden]
        results.append(hit | {"score": round(score, 6), "matched_terms": matched, "method": "local-lexical-bm25"})
    # A complete catalog ID takes precedence without changing its lexical score.
    results.sort(key=lambda result: (result["id"] != exact_id, -result["score"], result["id"]))
    return results[:max(0, min(limit, 100))]


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
    # Allocate against the full index so the current and historical views share IDs.
    topic_ids = {group["id"] for group in groups}
    kinds = {doc["kind"] for doc in index["documents"]}
    reserved = topic_ids | kinds
    fallback_ids = {}
    for kind in sorted(topic_ids & kinds):
        group_id = f"kind:{kind}"
        while group_id in reserved:
            group_id = f"kind:{group_id}"
        reserved.add(group_id)
        fallback_ids[kind] = group_id
    groups.extend({"id": fallback_ids.get(kind, kind), "title": kind, "children": children}
                  for kind, children in sorted(remainder.items()))
    return {"kind": "knowledge", "children": groups, "count": len(documents)}
