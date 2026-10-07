#!/usr/bin/env python3
"""Offline structure/source checks for the corporate OpenDesign starter.

This is NOT browser visual QA or a substitute for the canonical brand contract.
Run from any directory: python brands/melodiq-systems/open-design/check.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
BRAND = KIT.parent
SYSTEM = KIT / "system"
DEMO = KIT / "demo" / "alcance-del-servicio.html"

# OpenDesign upstream token-schema v1, observed 2026-10-08.
REQUIRED = set(
    "--bg --surface --surface-warm --fg --fg-2 --muted --meta --border "
    "--border-soft --accent --accent-on --accent-hover --accent-active "
    "--success --warn --danger --font-display --font-body --font-mono "
    "--text-xs --text-sm --text-base --text-lg --text-xl --text-2xl "
    "--text-3xl --text-4xl --leading-body --leading-tight "
    "--tracking-display --space-1 --space-2 --space-3 --space-4 "
    "--space-5 --space-6 --space-8 --space-12 --section-y-desktop "
    "--section-y-tablet --section-y-phone --radius-sm --radius-md "
    "--radius-lg --radius-pill --elev-flat --elev-ring --elev-raised "
    "--focus-ring --motion-fast --motion-base --ease-standard "
    "--container-max --container-gutter-desktop --container-gutter-tablet "
    "--container-gutter-phone"
    .split()
)


def main() -> int:
    failures: list[str] = []
    def require(ok: bool, label: str) -> None:
        if not ok:
            failures.append(label)

    source = json.loads((BRAND / "tokens.json").read_text(encoding="utf-8"))
    contract = (BRAND / "DESIGN.md").read_text(encoding="utf-8")
    manifest = json.loads((SYSTEM / "manifest.json").read_text(encoding="utf-8"))
    design = (SYSTEM / "DESIGN.md").read_text(encoding="utf-8")
    css = (SYSTEM / "tokens.css").read_text(encoding="utf-8")
    demo = DEMO.read_text(encoding="utf-8")

    require(manifest.get("schemaVersion") == "od-design-system-project/v1",
            "OpenDesign manifest schema")
    require(manifest.get("id") == SYSTEM.parent.name.replace("open-design", "melodiq-systems-corporate")
            or manifest.get("id") == "melodiq-systems-corporate", "OpenDesign package id")
    require(manifest.get("files") == {"design": "DESIGN.md", "tokens": "tokens.css"},
            "OpenDesign declared files")
    require(manifest.get("source", {}).get("type") == "github",
            "OpenDesign source provenance")
    require(source.get("scope") == "melodiq-corporate-surfaces-only",
            "brand scope unchanged")
    require(f'v{source["version"]}' in design, "tokens provenance version")
    version = re.search(r'^version:\s*"([^"]+)"', contract, re.M)
    require(bool(version and f"v{version.group(1)}" in design),
            "DESIGN provenance version")
    require(len(re.findall(r"^## ", design, flags=re.M)) >= 7,
            "substantive OpenDesign design sections")

    root_match = re.search(r":root\s*\{([^}]*)\}", css, re.S)
    require(root_match is not None, "CSS :root")
    root = root_match.group(1) if root_match else ""
    slots = dict(re.findall(r"^\s*(--[a-z0-9-]+):\s*([^;]+);", root, re.M))
    require(set(slots) == REQUIRED, f"56 OD token slots (found {len(slots)})")
    colors = source["color"]
    mapping = {
        "--bg": "paper", "--surface": "white", "--fg": "ink",
        "--muted": "muted", "--border": "border", "--accent": "primary",
        "--accent-on": "white", "--accent-hover": "hover"
    }
    for token, key in mapping.items():
        require(slots.get(token) == colors[key], f"canonical color {token}")
    require(slots.get("--container-max") == str(source["layout"]["contentMaxRem"]) + "rem",
            "canonical max container")
    require(slots.get("--radius-sm") == str(source["radius"]["control"]) + "px",
            "canonical control radius")
    require(slots.get("--motion-fast") == str(source["motion"]["feedbackMs"]) + "ms",
            "canonical feedback motion")
    require("[data-theme=\"dark\"]" in css, "dark semantic mapping")

    # Static, conservative offline checks; these do not replace runtime tests.
    for term in ("fetch(", "XMLHttpRequest", "sendBeacon", "localStorage",
                 "sessionStorage", "navigator.clipboard", "<script src=", "http://",
                 "https://", "innerHTML", "eval("):
        require(term not in demo, f"demo must be offline/static: {term}")
    for term in ('BORRADOR · DEMO', "window.print()", "textContent",
                 "form.addEventListener", "@page{size:A4", "lang=\"es\""):
        require(term in demo, f"demo contract: {term}")

    require(not (SYSTEM / "assets").exists(),
            "restricted corporate logo assets must not be distributed")
    if failures:
        for issue in failures:
            print("FAIL:", issue)
        return 1
    print("PASS: OpenDesign package; 56 token slots; corporate source parity; offline demo structure")
    print("NOT RUN: visual QA, browser interactivity, OpenDesign import, OS sandbox permissions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
