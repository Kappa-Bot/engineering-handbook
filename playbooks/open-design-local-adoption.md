---
id: pb-open-design-local-adoption
kind: playbook
status: active
owner: engineering
version: "1.0"
applies_to:
  - developer-workstations
  - design-production
  - all-repositories
sources:
  - src-open-design
  - src-openai-codex-agents
last_verified: 2026-10-08
review_due: 2027-01-08
---

# OpenDesign — local design and production workflow

## Purpose and limits

Use OpenDesign to explore, preview and iteratively refine visual work that has a clear canonical owner. OpenDesign is a production/preview **workspace**, not Kappa-Bot engineering governance, a new agent hierarchy or a replacement design-system authority.

The safest first integration on Windows is **local-file exchange** between a trusted Codex session and an isolated OpenDesign project. Only expand to live MCP/agent execution after proving the effective permission boundary.

## Authority and content ownership

```text
Handbook governance + security/cost controls
→ product/brand repo's canonical DESIGN contract
→ task-specific approved scope and acceptance
→ derived OpenDesign package / isolated project
→ reviewed exported artifact
→ implementation or separately authorized delivery
```

- Corporate MelodIQ tokens apply only to corporate surfaces; ChurchOS, JobOps, Platform Admin and tenant branding retain separate authorities.
- Use real approved logo/root asset bytes and verified provenance; never generate substitute marks or publish restricted packs.
- Import only public/synthetic examples during the initial pilot. Do not ingest congregant, customer, credentials, restricted contact lists or private commercial correspondence.
- A generated prototype is not proof of deployed functionality, access controls, backend behavior, product maturity or customer results.
- Preserve all copyright/licensing and attribution obligations for imported templates, design systems, images, fonts and generated assets.

## Installation and permissions

1. Use a current official stable OpenDesign release and verify the platform, publisher, release notes and expected installer digest where published. Do not install by executing an arbitrary URL piped into a shell.
2. Disable optional product analytics and conversation/tool-content sharing in Settings → Privacy before importing nontrivial work. OpenDesign documents a separate configured safety/reliability channel that cannot be disabled by those optional controls; use only non-sensitive pilot data.
3. Use a dedicated local workspace directory outside actual product checkouts. Do not point OpenDesign's agent at a repo containing secrets or credentials.
4. OpenDesign's **Codex adapter on Windows/WSL** can invoke Codex with `danger-full-access`, and the app-server path uses a noninteractive approval policy. Do not use that launcher against company repos for this pilot. If a later release changes this, verify the actual launch arguments and effective sandbox rather than relying on release notes alone.
5. Reuse the user's normal Codex session for authorized engineering. Preserve its `CODEX_HOME`, MCPs, model routing, agent catalog, approval mode and included-cost limits.
6. Preview `od mcp install codex --print` only. Do not install the live OpenDesign MCP as read-only by assumption; its actual server includes write tools. A future restricted MCP must prove effective tool visibility and deny unauthorized operations on the real installed client before enabling it against sensitive files.

## Deriving a design package

Use the product/brand's existing design contract, not a random OpenDesign skin. The minimal compatible package is:

```text
manifest.json
DESIGN.md
tokens.css
```

For richer packages, add usage, components, previews and assets only when real consumers justify them; OpenDesign applies additional guard requirements to rich manifests. Preserve provenance and valid licensing.

The MelodIQ corporate pilot lives in `brands/melodiq-systems/open-design/system/`. Its 56-slot CSS includes OpenDesign compatibility tokens but must preserve the canonical corporate identity values. The package is a distribution snapshot, not a new authority.

Products/tenants require distinct derivations and owner-approved acceptance. Never blindly recolor a vertical to corporate violet.

## First artifact: an editable commercial one-pager

`brands/melodiq-systems/open-design/demo/alcance-del-servicio.html` is the isolated pilot. It:

- works offline without network calls, persistence, third-party scripts or external model providers;
- edits client, project, date, situation, proposal, included/excluded work and next step;
- reflects changes safely via text nodes rather than HTML injection;
- prints as an A4 draft;
- labels itself **BORRADOR · DEMO** until real copy, approved logo and visual acceptance are complete.

It does **not** overwrite or replace an existing approved Gmail proposal/template.

## Acceptance sequence

| Gate | Evidence | If unavailable |
|---|---|---|
| Source integrity | Corporate token values and package manifest agree with canonical sources | Block package import |
| Local import | OpenDesign recognizes the design package and resolves the assets/tokens | Preserve package; report importer error |
| Privacy | Optional telemetry off; demo workspace isolated | Do not load confidential data |
| Security | No privileged OpenDesign-launched Codex; no untested write-capable MCP | Keep local-file exchange only |
| Demo interaction | Offline editing, reset, no persistence, print preview | Do not mark template accepted |
| Visual QA | Actual responsive/reflow/A4 output, contrast and official logo review when applicable | Do not claim production-ready |
| Delivery | Source/identity/claims/permissions checked and expressly approved | Keep **BORRADOR · DEMO** |

Use the repository's risk-based verification policy: no invented screenshots, no user/customer claims inferred from a mockup, no mandatory agent per stage.

## Ownership and updates

The product repo owns its implementation; OpenDesign is a disposable projection/iteration environment. Promote validated results back through normal repository review and tests. Do not create automatic community/theme updates that rewrite active design contracts or silently install paid model providers.

When a new OpenDesign release changes imports, MCP permissions, privacy or Codex launch behavior, verify those contracts before updating this playbook. A README that says "read-only" is not sufficient evidence when the live tool surface includes write operations.
