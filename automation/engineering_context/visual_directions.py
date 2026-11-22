"""Versioned MelodIQ material directions; deterministic selection, not UI authority.

The local product contract and an authorized task decide the actual direction.
This module never modifies a product, writes a preference or selects a theme
for a user at runtime.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import re

from .canonical import load_json_with_unique_members, stable_hash
from .discovery_rules import normalize

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = Path("machine-readable/visual-directions.v1.json")


def _alias_key(value: str) -> str:
    return normalize(value).strip()


def load_visual_catalog(root: Path = DEFAULT_ROOT, *, expected_source_hash: str | None = None) -> dict:
    """Reject ambiguous aliases, unsafe references and invalid scoped defaults."""
    root = Path(root).resolve()
    catalog_file = root / CATALOG_PATH
    if catalog_file.is_symlink() or not catalog_file.is_file() or not catalog_file.resolve().is_relative_to(root):
        raise ValueError("missing or unsafe visual-direction catalog")
    source = catalog_file.read_text(encoding="utf-8")
    if expected_source_hash is not None and stable_hash(source) != expected_source_hash:
        raise ValueError("visual-direction catalog differs from the verified discovery index")
    return parse_visual_catalog(source, resolved_root=root)


def parse_visual_catalog(source: str, *, resolved_root: Path) -> dict:
    """Validate captured catalog text and its references in the selected Handbook."""
    catalog = load_json_with_unique_members(
        source, label=CATALOG_PATH.name, require_finite_numbers=False,
    )
    if not isinstance(catalog, dict) or catalog.get("schema") != "melodiq-visual-directions/v1":
        raise ValueError("unsupported visual-direction catalog")
    surfaces, defaults, entries = catalog.get("surfaces"), catalog.get("default_by_surface"), catalog.get("directions")
    if (not isinstance(surfaces, list) or not surfaces or not all(isinstance(s, str) and re.fullmatch(r"[a-z]+(?:-[a-z]+)*", s) for s in surfaces)
            or len(surfaces) != len(set(surfaces)) or not isinstance(defaults, dict) or not isinstance(entries, list) or not entries):
        raise ValueError("invalid visual-direction surfaces or entries")
    ids, aliases = set(), {}
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("invalid visual-direction entry")
        identity, title, status = item.get("id"), item.get("title"), item.get("status")
        if (not isinstance(identity, str) or not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", identity)
                or identity in ids or not isinstance(title, str) or not title.strip() or status != "active"):
            raise ValueError("invalid or duplicate visual-direction identity")
        ids.add(identity)
        words = item.get("aliases")
        if not isinstance(words, list) or not words or not all(isinstance(word, str) and word.strip() for word in words):
            raise ValueError("invalid visual-direction aliases")
        for word in words:
            key = _alias_key(word)
            if not key or key in aliases:
                raise ValueError("ambiguous visual-direction alias: " + word)
            aliases[key] = identity
        reference = item.get("reference")
        if not isinstance(reference, str) or not reference.endswith(".md") or "\\" in reference or ":" in reference:
            raise ValueError("invalid visual-direction reference")
        relative = PurePosixPath(reference)
        path = resolved_root / reference
        if (relative.is_absolute() or relative.as_posix() != reference or ".." in relative.parts
                or not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(resolved_root)):
            raise ValueError("missing or unsafe visual-direction reference: " + reference)
        for key in ("best_for", "avoid"):
            if not isinstance(item.get(key), list) or not all(isinstance(value, str) and value.strip() for value in item[key]):
                raise ValueError("invalid visual-direction guidance: " + key)
    if any(not isinstance(surface, str) or surface not in surfaces or not isinstance(style, str) or style not in ids for surface, style in defaults.items()):
        raise ValueError("invalid visual-direction default mapping")
    if any(normalize(identity) in aliases and aliases[normalize(identity)] != identity for identity in ids):
        raise ValueError("visual-direction alias shadows a canonical ID")
    if defaults != {"internal-console": "glassmorphism"}:
        raise ValueError("unexpected visual-direction default scope")
    return catalog


def resolve_visual_direction(root: Path, surface: str, task_style: str | None = None, local_style: str | None = None) -> dict:
    """Surface default applies only in the absence of explicit local/task direction."""
    catalog = load_visual_catalog(root)
    if surface not in catalog["surfaces"]:
        raise ValueError("unknown visual surface: " + str(surface))
    entries = {item["id"]: item for item in catalog["directions"]}
    aliases = {_alias_key(alias): item["id"] for item in catalog["directions"] for alias in item["aliases"]}
    aliases.update({normalize(item["id"]): item["id"] for item in catalog["directions"]})
    task_style = aliases.get(_alias_key(task_style), task_style) if task_style is not None else None
    local_style = aliases.get(_alias_key(local_style), local_style) if local_style is not None else None
    for choice in (task_style, local_style):
        if choice is not None and choice not in entries:
            raise ValueError("unknown visual direction: " + str(choice))
    selected, source = (task_style, "explicit-task") if task_style is not None else ((local_style, "local-design") if local_style is not None else (catalog["default_by_surface"].get(surface), "default" if surface in catalog["default_by_surface"] else "product-owned"))
    return {"schema": "visual-direction-selection/v1", "surface": surface, "selected": selected, "source": source,
            "reference": entries[selected]["reference"] if selected else None,
            "reason": "Task-scoped design selection, never authorization or automatic product migration" if source == "explicit-task" else
                      "Current explicit product design contract" if source == "local-design" else
                      "Scoped starting candidate for an internal console, subject to product/rendered evidence" if source == "default" else
                      "No portfolio default: establish the product-owned direction",
            "authorizes_ui_change": False, "runtime_user_toggle": False}


def detect_visual_styles(text: str, root: Path = DEFAULT_ROOT, *, catalog: dict | None = None) -> tuple[str, ...]:
    """Find positive mentions; a comparison can return multiple candidates."""
    if catalog is None:
        catalog = load_visual_catalog(root)
    normalized = normalize(text)
    clauses = re.split(
        r"[;,\.\n]|\b(?:but|pero|then|luego)\b|"
        r"\b(?:and|y)\s+(?=(?:usa|usar|use|apply|aplica|elige|choose|"
        r"prefiero|quiero|no|do not|avoid|evita)\b)",
        normalized,
    )
    matched = set()
    negative = re.compile(r"\b(?:no|sin|without|avoid|evita|descarta|reject|never|do not|don['’]t)\b")
    rejected_after = re.compile(r"^\s+(?:no|descartad[oa]|rejected|never)\b")
    replaced_by = re.compile(r"\b(?:frente a|en lugar de|instead of|rather than|antes que)\s*$")
    for clause in clauses:
        for item in catalog["directions"]:
            for alias in item["aliases"]:
                for occurrence in re.finditer(r"(?<!\w)" + re.escape(_alias_key(alias)) + r"(?!\w)", clause):
                    if (not negative.search(clause[:occurrence.start()])
                            and not rejected_after.search(clause[occurrence.end():])
                            and not replaced_by.search(clause[:occurrence.start()])):
                        matched.add(item["id"])
    return tuple(item["id"] for item in catalog["directions"] if item["id"] in matched)
