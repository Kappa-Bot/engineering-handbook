# MelodIQ visual-direction catalog — approved design

Date: 2026-11-19. Owner choice: **approach A**, visual direction selected per product. The user explicitly deferred approach B (a runtime/per-user theme selector).

## Intent

Make Glassmorphism the **scoped starting direction** for new or explicitly authorized material redesigns of MelodIQ's authenticated internal operator/admin consoles, while making Neumorphism a first-class, discoverable alternative in an expandable visual-direction catalog. Preserve each product's identity, accessibility and functional truth. Correct Handbook routing, governance and stale visual claims that currently contradict this choice.

## Approaches considered

1. **Product-level catalog (selected):** one versioned machine-readable inventory, canonical material guidance, a deterministic selection interface and project-owned `DESIGN.md` decisions. No shared runtime dependency.
2. **User-facing live selector (deferred):** per-user style changes, persistence and all-state dual-render verification. Future separate project; not silently implemented by this catalog.
3. **Cross-repository component package (not selected):** potential reuse, but premature shared UI ownership and coupling across different product/tenant identities.

## Scope and precedence

- A visual direction is a **candidate material language**, not a generic dashboard layout, component library, brand palette, UI quality standard or license to redesign.
- For a *new* internal operator/admin console, or material redesign already authorized, with no applicable explicit current product direction: default to `glassmorphism` **as the starting candidate**, then validate actual tasks/rendering. If it fails access/contrast/performance/density, choose a suitable alternative and record why. Existing screens are not retroactively re-skinned by a Handbook update.
- Current explicit `DESIGN.md`/product constraint wins over the catalog default. An owner-authorized new design request can replace an earlier aesthetic within its approved scope, with a recorded supersession. Tenant branding, clinical/financial semantics, permissions, persistence, public-facing brand and release freezes do not follow the style choice.
- A public/marketing, patient/member, field, kiosk, editorial or other non-console surface has **no inherited portfolio default**. A material can be explicitly selected when its local direction warrants it; operator-console-specific mechanics are not imported solely from a shared material name.
- `neumorphism` is selectable for any expressly suitable local design, including an internal console; `solid-editorial` is a deliberate accessible alternative and functional fallback. Catalog entries can grow without changing the selection API.
- No end-user runtime switch, preference storage, automatic tenant-wide theme propagation, new product UI implementation, provider install or paid dependency in this phase.

## Catalog and selection contract

- Source `machine-readable/visual-directions.v1.json`: schema `melodiq-visual-directions/v1`, unique lower-kebab IDs, active entries, aliases, canonical reference paths, applicable surface hints and exactly one default mapping `internal-console -> glassmorphism`. Initial IDs: `glassmorphism`, `neumorphism`, `solid-editorial`.
- Standard-library resolver `automation/engineering_context/visual_directions.py`: validate schema/IDs/references/safe paths; resolve `(surface, explicit_task_choice, local_design_choice)` with precedence **explicit authorized task choice > local current design choice > scoped default > product-owned undecided**. An unknown choice blocks instead of silently replacing it; the resolver does not grant authorization. Keep result source/choice/why observable.
- CLI `visual-directions --root ... [--surface ...] [--style ...] [--local-style ...]` lists options or returns the resolved choice. The existing `search`/knowledge tree discover the human-facing catalog via canonical document and bilingual topic aliases.
- Descriptor routes `archetype:operator-visual-direction-choice` only for materially visual internal-console tasks (new design/redesign, not ordinary backend work, copy edits or public sites). Explicit Glass/Neumorphism material requests get their own material predicates **only within relevant operator scope**; public explicit style requests may discover the catalog but never inherit the internal default. Negated/rejected styles cannot become selected evidence. Classification is guidance, not mutation authority.
- Context compiler includes a small catalog-selection planning unit and conditional material acceptance units. Do not add a fifth `machine-readable/discovery/*.json` registry: the already-installed stable updater expects that directory's explicit four-file contract. Add the independent catalog file to the bundled includes instead.

## Visual and verification contract

- **Glassmorphism:** limited translucent navigation/context, solid data reading plane and clear elevated overlays; actual composite contrast, focus, opaque/forced-colors fallback, narrow/zoomed layout, blur performance, reduced motion and tenant/brand isolation. No glass-on-glass card wall.
- **Neumorphism:** selective raised/inset affordances where tactile/metaphoric depth genuinely clarifies control roles. Never encode interactive, selected, pressed, invalid or disabled meaning by shadows alone. Keep identifiable control edges/focus rings, readable solid data, keyboard/touch behavior, high-contrast/forced-colors and reduced-motion/fallback paths. Avoid fake embossed inputs and low-contrast soft shadows.
- **Solid/editorial:** full first-class direction for dense/critical reading, forms, clinical/financial records, print and performance-constrained contexts. It is not an accessibility exemption from the same UI quality floor.
- Light/dark, brand, density and motion remain **orthogonal** to material selection; a material ID never imposes a palette, typography family or runtime toggle. Existing UI/UX Standard, Unslop nine-pass workflow and browser compatibility requirements remain the acceptance authority.
- Tests cover valid/default/override/unknown catalog choices; operator/public/negative/mixed routing; catalog search/context; future entry extensibility; integrity of distributed bundle; preservation of unrelated visual and context regressions. No claim that actual products have adopted the catalog absent product-repo evidence.

## Ownership and reconciliation

- Canonical owner: new `patterns/visual-direction-catalog.md`. Deep material execution stays in `patterns/operator-glass-surface-material.md` and new `patterns/operator-neumorphic-surface-material.md`. A new ADR records the explicit 2026-11-19 owner reversal of the 2026-11-16 optional-only glass position without erasing history.
- Amend only conflicting scoped sentences in `standards/ui-ux-quality-baseline.md`, `patterns/design-context-layering.md`, `patterns/operator-console-shell-interactions.md`, `playbooks/frontend-quality-review.md`, global baseline/skill and README. Register artifacts in `machine-readable/catalog.yaml`, taxonomy and skill bundle; regenerate compiled corpus.
- Existing `DESIGN.md` files in product repositories remain their owners; don't mass-rewrite them or launch unrequested releases. The future runtime picker will need its own design, state, accessibility and migration plan.
