# MelodIQ Systems — OpenDesign starter kit

This directory is a **distribution/prototype kit**, not the corporate source of truth. Source authority remains `../DESIGN.md`, `../tokens.json`, and the restricted v8 logo provenance in the parent directory.

## Contents

| Resource | Use | Authority |
|---|---|---|
| `system/manifest.json`, `system/DESIGN.md`, `system/tokens.css` | Corporate design-system package for local OpenDesign import | Derived, nonauthoritative |
| `demo/alcance-del-servicio.html` | Offline, editable, printable A4 commercial one-pager | **Draft/demo**, not the approved Gmail master |
| `check.py` | Lightweight package consistency and offline-safety checks | Local verification helper |

**No protected logo, real client data, private Gmail template, login credential or font file is shipped.** The demo deliberately uses ordinary text for the company name, not an approximation of the approved logo.

## Safe usage on Windows

1. Read `playbooks/open-design-local-adoption.md` in the Handbook. OpenDesign's Codex adapter uses `danger-full-access` on Windows/WSL. Do **not** run Codex *from OpenDesign* against your normal repositories.
2. Install the official signed/stable Windows build only after inspecting its release, integrity and permissions. OpenDesign does not need API billing to import and preview these local files. Do not set up OpenDesign AMR, Cloud credits or paid media providers for this pilot.
3. On first launch, choose **Don't share** for optional analytics/conversation data and check Settings → Privacy. Note that optional telemetry control does not disable configured reliability telemetry.
4. In OpenDesign, import the `system/` directory as a **local design system** using its Design Systems import-from-folder surface. Confirm the imported name is "MelodIQ Systems · Corporate" and the rendered tokens match the canonical brand contract. If the importer rejects the current package, record the exact error rather than weakening its validation.
5. Open `demo/alcance-del-servicio.html` locally in a normal browser or add an isolated copy as an OpenDesign project artifact. Edit the left-hand form fields; use **Imprimir / PDF** to print. The HTML deliberately has no HTTP requests, third-party scripts or persistence. Use **demo data only** for the pilot.
6. Confirm one-page A4 print preview, keyboard focus, text wrap, mobile behavior and contrast. A visual review is still required; the script check alone is not visual acceptance.
7. Keep product-specific ChurchOS/JobOps/Agurto systems separate from this corporate package. Adapted product packages must be derived from *their own* design authority, not from MelodIQ corporate colors.

### CLI and MCP boundary

OpenDesign advertises `od mcp install codex --print` to **preview** an MCP configuration. Do not follow it with `od mcp install codex` automatically. The actual OpenDesign MCP includes write/create/delete-style project tools; "local" is not synonymous with "read-only".

For this first pilot, the supported boundary is **local folder import/export**, not a privileged live MCP.

A future read-only MCP configuration may be adopted only after listing actual tool names, proving a working client-side allowlist against the installed Codex version and verifying unauthorized write tools are absent. Never trust `enabled_tools` merely because the TOML parses; known Codex releases have had allowlist registration regressions. Keep write operations behind explicit permissions.

## Corporate logo

The restricted `assets.pack.v8.json` describes two approved production roots and their checksums. Do not infer an approved SVG, use an arbitrary generated brand symbol or copy the private ZIP into this public repository. For a production artifact, validate the local canonical pack/root checksums and use only approved derivatives under the canonical DESIGN contract. Until then, the starter remains marked **BORRADOR · DEMO**.

## Refresh and verification

Run:

```powershell
python brands/melodiq-systems/open-design/check.py
```

After changing canonical `tokens.json` or `DESIGN.md`, reconcile this derived package and rerun the check; it deliberately fails when locked palette values drift. Do not silently edit a design token in OpenDesign and claim the corporate standard changed.

The offline one-pager is only a reusable seed; it does not replace previously approved ChurchOS proposal or Gmail signature templates. No sending, deployment or publishing is authorized by this kit.
