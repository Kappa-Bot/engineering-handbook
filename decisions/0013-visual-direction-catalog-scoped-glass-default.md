---
id: adr-0013-visual-direction-catalog-scoped-glass-default
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to: [engineering-handbook, internal-operator-consoles, user-facing-surfaces]
sources: [src-w3c-wcag-22, src-w3c-aria-apg]
last_verified: 2026-11-19
review_due: 2027-02-19
---

# Selectable visual directions and a scoped Glassmorphism default

## Owner decision — 2026-11-19

The owner explicitly selected **approach A: product-level visual-direction catalog** for MelodIQ Systems. **Approach B: a live user-facing material selector is deferred to a separate future project**. Glassmorphism is one catalog option alongside first-class Neumorphism and solid/editorial directions; further entries may be added under validated catalog ownership.

For **new or explicitly authorized material redesigns of internal authenticated operator/admin consoles only**, Glassmorphism is the **starting default when the product has no current explicit applicable direction**. It must survive real task/visual/accessibility/performance evidence; failing contexts can choose another direction. Public marketing, self-service, field, kiosk, clinical data and editorial surfaces have no inherited portfolio material default. The current local `DESIGN.md`, explicit current product constraints and an owner-authorized task decision take precedence; tenant identity and business/data/security contracts remain protected.

This **amends the 2026-11-16 optional-only/no-preference conclusion** in `pat-operator-glass-surface-material` and related general Unslop text **for that limited console scope**. The earlier decision remains historical context: glass is still optional on other surfaces and not guaranteed to be retained during an authorized redesign. No particular sidebar, palette, typeface, hero, card style or cross-product component architecture is prescribed. The quality baseline and reconstruction contract remain active.

## Implementation and boundaries

- Canonical human owner: `pat-visual-direction-catalog`. Canonical structured inventory: `machine-readable/visual-directions.v1.json`, validated by `automation/engineering_context/visual_directions.py` and exposed via the `visual-directions` CLI.
- Material detail: `pat-operator-glass-surface-material` and `pat-operator-neumorphic-surface-material`. The task router adds **selection** context to material console-design work; it adds a specific material implementation gate **only for explicit requested adoption**, never because the default exists.
- Current product-owned design contracts, real UI and release processes are not edited retroactively. A result from the resolver is a recommendation/trace, **not an authorization token**. No runtime user preference, hot style switch, migration of existing products, installation, external deployment or paid dependency follows from this change.
- Entry aliases, references and defaults are schema-validated; a new direction is added as a catalog entry and owned Pattern, not as competing prose mappings. Discovery, source registration and the distributed skill bundle expose the new contract without changing the four-file stable discovery registry.

## Acceptance

Verify positive/negated/bilingual style recognition; design-versus-micro/public/backend task separation; explicit task, local and scoped-default precedence; search/graph/context selection; zero implied rollout; compiled freshness, catalog integrity and all existing Handbook tests. Real browser/assistive-tech adoption must be independently verified in each authorized product repository before production claims.
