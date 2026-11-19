---
id: pat-operator-glass-surface-material
kind: pattern
status: active
owner: engineering
version: "0.3"
applies_to:
  - authenticated-operational-consoles
  - admin-workspaces
  - vertical-products
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-11-19
review_due: 2027-02-19
---

# Operator Glass: restrained depth, solid data

## Intent and authority

Glass is **one selectable material technique** in the [MelodIQ visual-direction catalog](visual-direction-catalog.md), not a universal product skin. As of the owner's [2026-11-19 decision](../decisions/0013-visual-direction-catalog-scoped-glass-default.md), it is the **starting default for new or already-authorized material redesigns of authenticated internal operator/admin consoles** only when the product has no explicit applicable direction. Test that candidate against rendered task evidence; a solid, Neumorphic, editorial or other direction remains appropriate when it serves the actual work better. Existing production consoles are not automatically re-skinned.

This **active, conditional Pattern** describes how to evaluate and implement glass when the selected direction warrants it. [UI/UX Quality Baseline §1](../standards/ui-ux-quality-baseline.md#1-product-specific-design-and-reconstruction) controls reconstruction and acceptance: a material redesign may remove previously approved glass, replace its palette and typography, or select another material without preserving an obsolete aesthetic. The local design contract and current authorized task outrank the scoped starting default. Respect explicit current constraints and independent release freezes. `pat-design-context-layering` governs product boundaries. For independent theme/sidebar/route mechanics use `pat-operator-console-shell-interactions`; this Pattern owns only the **material and elevation model**.

**Decision history:** on 2026-11-16, the earlier broad owner preference for glass across operator products was retired; experiments remained historical evidence, not automatic adoption. On 2026-11-19 the owner [restored only a scoped starting default for new/authorized internal consoles](../decisions/0013-visual-direction-catalog-scoped-glass-default.md), **not** the broad portfolio rule. Both dates matter; a current explicit product choice still wins.

Public marketing sites, patient/member self-service, kiosk, print and field interfaces require their own design decision. Do not style Agurto's marketing website, the Uribe Villa public site, or any tenant brand merely because it belongs to the portfolio.

## Three material layers

| Layer | Appropriate use | Visual treatment | Avoid |
| --- | --- | --- | --- |
| **Glass chrome** | Top bar, navigation rail, secondary toolbar, contextual filter container | Limited translucency, fine visible boundary, restrained shadow, optional blur on a quiet background | Rows of nested glass cards, floating decoration, text over busy imagery |
| **Solid data** | Tables, search fields, jobs, calendars, forms, clinical records, financial values, audit trails | Opaque or near-opaque surface; predictable contrast; row/column alignment and strong active/focus state | Reading through an image, color-only statuses, pale text, decorative floating KPIs |
| **Elevated context** | Bounded menu, popover, inspector, dialog or single contextual drawer | Stronger separation from the parent surface, stable backdrop, obvious context and focus | Translucent modal over a translucent form, nested routine overlays, visually hidden close/return path |

**The hierarchy is functional:** depth differentiates persistent navigation from the active workspace and an elevated task. It must never determine which business facts are true, permitted or actionable. User task, information density, filters and action placement are decided *before* material effects.

### Screen composition rule

Prefer one coherent reading plane with carefully chosen glass boundaries. Avoid a grid of shiny cards inside a shiny page with more frosted badges on top. Empty space, blur, borders, shadows and gradients each spend the same attention budget; every simultaneous effect needs a reason. A simple solid panel can be more elegant than glass when the screen is dense.

## Token contract: semantic roles, not copied colors

Implement through a **coherent product semantic theme system**, adapting useful existing primitives without inheriting their visual values by default. Never copy a MelodIQ Core violet or import a prototype stylesheet as portfolio authority. The following are *roles*, not an instruction to add these exact names to every repository:

| Semantic role | Intent |
| --- | --- |
| `surface.canvas` | Calm page backdrop; never the sole contrast source for data |
| `surface.chrome` | Translucent operator navigation/toolbar, with an opaque fallback |
| `surface.data` | Stable opaque reading and input surface |
| `surface.elevated` | Dialog/drawer/popover surface, usually more opaque than chrome |
| `border.subtle` / `border.strong` | Quiet grouping versus control/focus separation |
| `text.primary` / `text.secondary` | Verified readable foreground over each material and theme |
| `focus`, `selected`, `status.*` | Semantically distinct state roles, not a single brand-accent wash |
| `shadow.elevated`, `blur.chrome` | Context-sensitive elevation; disabled when unsupported or too expensive |

Resolve light and dark **separately** where the product supports both; a blanket opacity inversion is not a theme. The actual underlay, gradients, imagery, window size, browser and backdrop state can all change perceived contrast. Measure text and essential UI-state contrast against the **worst visible composite**, not the nominal RGBA swatch. `std-ui-ux-quality-baseline` owns applicable WCAG 2.2 AA acceptance; this Pattern does not invent different thresholds.

The initial MelodIQ Core prototype explored lilac/violet, DM Sans, Phosphor icons and translucent panel tokens. **None of those trial values, fonts or icon families are portfolio-wide defaults.** Choose typography, geometry, density and material for the current direction, and preserve the meaning of statuses. Preserve authentic product/tenant logos and legal identity unless changing them is separately authorized; a generated approximation from a mockup is not an approved production logo. The original Core exercise referenced v8 M–Q raster assets; verify the current asset owner instead of treating this historical identifier as a perpetual requirement.

### Progressive enhancement sketch

This is CSS **pseudocode adapted to local tokens**, not a drop-in file or cross-product component dependency:

```css
.operator-chrome {
  background: var(--chrome-opaque-fallback);
  border: 1px solid var(--border-chrome);
  box-shadow: var(--shadow-chrome);
}

@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .operator-chrome[data-glass-enabled="true"] {
    background: var(--chrome-translucent);
    backdrop-filter: blur(var(--chrome-blur));
    -webkit-backdrop-filter: blur(var(--chrome-blur));
  }
}

.operator-data { background: var(--surface-data-opaque); }

@media (forced-colors: active) {
  .operator-chrome {
    background: Canvas;
    border-color: CanvasText;
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

If blur is unsupported, disabled, dropped under load or visually harmful, the **opaque fallback remains a complete usable design**. Reduced-motion disables unnecessary movement, but is not itself proof that blur is disabled. Avoid `transition: all`, expensive continuously animated blur and heavy full-viewport backdrop filters without measured justification.

## Operational component behavior

- **Navigation shell:** restrained glass can distinguish global context where the chosen shell benefits from it. Apply the functional, keyboard, focus, tenant and route-state contracts of the selected mechanics in `pat-operator-console-shell-interactions`; do not inherit a rail or header-toggle placement merely to match that donor. No decorative footer or glass-on-glass shell multiplication.
- **Search and filters:** use a stable field background, explicit applied filters, truthful count, visible selected/unselected state and quick clear/reset. When there is no useful filter, do not add a glass chip to suggest one.
- **Tables and lists:** keep the actual reading plane solid. Strong primary column, predictable row actions, numeric alignment, stable sticky headers where useful; semantic text/icon states. At narrow widths, select an honest reflow/scroll strategy by task, not a decorative card conversion by default.
- **Jobs, scheduling and repeated tasks:** prioritize next action, status changes and one-to-three-click safe routines. Density and operability take precedence over large soft panels or animations. Avoid asking for superadmin intervention when a properly authorized operator action exists.
- **Forms, dialogs and inspectors:** field labels, validation, unsaved changes and recovery remain readable. Manage opening and closing focus, keyboard Escape and focus return. Prefer an inline/child route for long tasks or nested operations rather than stacking frosted drawers and modals.
- **Treasury/finance and clinical data:** opaque ledger cells, amounts, totals, period labels, uncertainty, periodontograms, appointment data and audit evidence. Convey negative/pending/unknown/confirmed states with explicit text and non-color cues. Do not hide critical data in blurred backgrounds, hover-only details or decorative charts.
- **Feedback:** pressed, pending, success, error, disabled, empty, partial, loading, stale and permission states must describe the real operation. Visual shine is not evidence that a write succeeded.

## Product contexts and protected invariants

| Product | Context if glass is selected | Boundary before implementation |
| --- | --- | --- |
| **MelodIQ Core** | Navigation/context around customer/runtime operations; opaque searchable data workspace | Inspect `design-system/platform-core/DESIGN.md` and current assets. Supersede inadequate layout, palette and typography within authorized redesign; retain security/tenant context and authentic identity. |
| **Ops OS / Agurto OS** | Navigation and lightweight context panels around Jobs, agenda, budgets and operational actions | Preserve Agurto tenant identity, authorised workflows, existing data separation and field/mobile usability. Demo-only decisions do not modify production Agurto or the public website. |
| **DentalOS** | Limited material accents around a fully solid clinical workspace, if useful | The originally inspected MD-1 used light-only Manrope/green; recheck current constraints rather than inheriting its aesthetic. Do not silently override an explicit current light-only restriction, clinical acceptance or privacy gate. Clinical charts must remain readable and precise. Public Uribe Villa is out of scope. |
| **Church OS** | Context accents around People, Agenda and operator tasks, if useful | Review current `DESIGN.md` for tenant identity and task/state invariants; reconstruct presentation when authorized. **Tesorería** and audit-related values remain opaque and precise; Local/tenant authorization is never presentation-derived. |

These are **context examples**, not adoption claims or preferred styles. Record the selected material and superseded decisions in the product's existing `DESIGN.md`; delegated redesign authority is sufficient for aesthetic choices within that scope, without another glass-specific approval ceremony. Publication and changes to protected invariants require their own valid authority. Approval of this Handbook Pattern is **not** release approval.

## Adoption sequence and evidence

1. Apply the current direction under `std-ui-ux-quality-baseline` §1 after reading `AGENTS.md`, `DESIGN.md`, tokens, tenant boundaries, known freezes and rendered evidence. Classify task and density. Treat the existing glass treatment as a candidate to replace, not a protected baseline; compare it with a complete no-glass alternative when material choice is in scope.
2. Decide whether glass improves **orientation or perceived continuity** without degrading scanning, input, contrast, speed or trust. If the answer is no, use solid surfaces. Record the choice in the existing product design contract; no second source of truth.
3. Validate a representative slice before propagating the chosen design: shell where relevant, a realistic dense data screen, a form/overlay, empty/error states and narrow/mobile behavior. The slice is evidence for reconstruction, not a ceiling on an authorized redesign. Use clearly identified synthetic data in demos; do not invent production customer, clinical or financial facts.
4. Review and accept a product-specific material map and token projection. Reuse existing primitives and test the opaque fallback before adding blur. Keep demo/product/public-site isolation intact.
5. Implement only on an explicitly authorized product branch/release scope. Keep domain logic, API behavior, permissions and persistence unchanged unless separately requested and verified.
6. Verify the complete authorized scope with actual rendered evidence and disclose missing gates. Keep the canonical product contract in step with the selected design and observed acceptance; do not represent a prototype as production adoption.

### Minimum acceptance matrix

| Check | Evidence required before calling an implementation done |
| --- | --- |
| Reading | Text/input/status contrast on the weakest real composite in light/dark **where supported**, focused/selected/error/disabled states and realistic dense data |
| Operation | Keyboard/focus order, screen-reader names, filter predicates/counts, quick actions, dialog or route recovery, no misleading success |
| Mobile and zoom | 320 CSS px reflow, 200% zoom, touch targets, virtual keyboard, long content, no hidden actions or unintended page overflow |
| Motion and fallback | Reduced-motion state, no-blur fallback, browser without `backdrop-filter`, no overlapping unreadable layers |
| Performance | Scroll, sticky header/rail, data-heavy list, lower-powered mobile/PWA device; check rendering cost, not just Lighthouse startup score |
| Provenance | Product/tenant/brand separation, source-of-truth contract, actual commit/build and environment, explicit unrun or blocked gates |

## Maturity and decision boundary

The initial self-contained Core-oriented prototype established a **visual direction**, not production readiness. Desktop visual exploration and in-memory interactions are not proof of WCAG, assistive technology, mobile/200%-zoom, data-integrity, low-end-device performance or live product adoption. Do not cite that experiment as a verified donor implementation or claim Core/Ops/Dental/Church are already migrated.

Evidence may improve these material mechanics, but the limited internal-console default does not make glass the portfolio's visual identity. Product-specific art direction and the reconstruction requirements of `std-ui-ux-quality-baseline` remain controlling.

## Agent context projection

```json agent-context
{
  "units": [
    {
      "id": "operator-glass-material-adoption-decision",
      "type": "decision-question",
      "text": "For explicit Glassmorphism adoption in an authorized operator design, apply pat-visual-direction-catalog precedence and the current DESIGN.md, task and rendered evidence. Glass is only the starting default for new or already-authorized material-redesign internal consoles lacking an explicit product choice, not a broad portfolio skin or a reason to re-theme existing production. Replace it with a better material if readability, accessibility, density, performance or task orientation require. Preserve tenant/brand identity and independent release/permission gates.",
      "source": "pat-operator-glass-surface-material",
      "covers": ["glass-material-fidelity", "accessibility", "performance"],
      "activate_when": ["archetype:operator-glass-material-change"],
      "phase": ["planning"],
      "priority": 76
    },
    {
      "id": "operator-glass-material-conditional-acceptance",
      "type": "verification",
      "text": "If an operator-console change explicitly adopts Glassmorphism, verify a translucent chrome/opaque data/elevated-context hierarchy; actual-composite contrast, semantic focus and state, mobile 320px/200%-zoom, touch/keyboard, opaque blur fallback, reduced motion, data-dense scroll performance and tenant/brand isolation. Report all unrun visual/device/accessibility/performance gates rather than declaring the prototype production-ready.",
      "source": "pat-operator-glass-surface-material",
      "covers": ["glass-material-fidelity", "accessibility", "performance", "compatibility"],
      "activate_when": ["archetype:operator-glass-material-change"],
      "phase": ["verification"],
      "priority": 80
    }
  ]
}
```
