---
id: pat-operator-glass-surface-material
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - authenticated-operational-consoles
  - admin-workspaces
  - vertical-products
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-11-08
review_due: 2027-02-08
---

# Operator Glass: restrained depth, solid data

## Intent and authority

The MelodIQ owner prefers a **restrained Glassmorphism direction for CRM and internal operator surfaces**. The objective is a product that feels refined and alive while remaining faster to scan and operate than a decorative dashboard. The material is a hierarchy tool, not a background effect applied to every rectangle.

This is an **active, optional implementation Pattern**, not an organization-wide palette, CSS package or automatic redesign instruction. It describes *how to evaluate and implement* a glass treatment **when the product owner and the product's current design authority authorize it**. The owner preference makes it a candidate for future, specifically scoped operator work; it does not itself amend a consumer repository's `DESIGN.md`, its release freeze or its approved theme. `pat-design-context-layering` and `std-ui-ux-quality-baseline` remain controlling. For header theme switch, sidebar and route transitions, use `pat-operator-console-shell-interactions`; this Pattern owns only the **material and elevation model**.

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

Implement through the **consumer's existing semantic theme system**, never through a hard-coded MelodIQ Core violet or an imported prototype stylesheet. The following are *roles*, not an instruction to add these exact names to every repository:

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

The initial MelodIQ Core prototype explored lilac/violet, DM Sans, Phosphor icons and translucent panel tokens. **None of those trial values, fonts or icon families are approved as portfolio-wide defaults.** Retain each product's authentic logo, typography, geometry, statuses and density. In MelodIQ Core, use the owner-approved v8 M–Q raster assets: a generated approximation from a mockup is not a production logo.

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

- **Navigation shell:** a restrained glass top bar/rail can distinguish global context. Preserve the existing header-toggle, navigation, keyboard, focus, tenant and route-state contracts from `pat-operator-console-shell-interactions`. No decorative footer or global glass-on-glass shell multiplication.
- **Search and filters:** use a stable field background, explicit applied filters, truthful count, visible selected/unselected state and quick clear/reset. When there is no useful filter, do not add a glass chip to suggest one.
- **Tables and lists:** keep the actual reading plane solid. Strong primary column, predictable row actions, numeric alignment, stable sticky headers where useful; semantic text/icon states. At narrow widths, select an honest reflow/scroll strategy by task, not a decorative card conversion by default.
- **Jobs, scheduling and repeated tasks:** prioritize next action, status changes and one-to-three-click safe routines. Density and operability take precedence over large soft panels or animations. Avoid asking for superadmin intervention when a properly authorized operator action exists.
- **Forms, dialogs and inspectors:** field labels, validation, unsaved changes and recovery remain readable. Manage opening and closing focus, keyboard Escape and focus return. Prefer an inline/child route for long tasks or nested operations rather than stacking frosted drawers and modals.
- **Treasury/finance and clinical data:** opaque ledger cells, amounts, totals, period labels, uncertainty, periodontograms, appointment data and audit evidence. Convey negative/pending/unknown/confirmed states with explicit text and non-color cues. Do not hide critical data in blurred backgrounds, hover-only details or decorative charts.
- **Feedback:** pressed, pending, success, error, disabled, empty, partial, loading, stale and permission states must describe the real operation. Visual shine is not evidence that a write succeeded.

## Per-product adoption boundaries

| Product | Candidate usage | Boundary before implementation |
| --- | --- | --- |
| **MelodIQ Core** | Restrained chrome around customer/runtime operations; opaque searchable data workspace | Honor `design-system/platform-core/DESIGN.md`, its current Manrope/Inter tokens and verified v8 M–Q mark. Do not silently replace the existing operator layout, security/tenant context or shipped palette. |
| **Ops OS / Agurto OS** | Navigation and lightweight context panels around Jobs, agenda, budgets and operational actions | Preserve Agurto tenant identity, authorised workflows, existing data separation and field/mobile usability. Demo-only decisions do not modify production Agurto or the public website. |
| **DentalOS** | Limited, calm chrome with fully solid clinical workspace | Current `DESIGN.md` MD-1 is **light-only**, uses Manrope/green and compact geometry. No dark mode, purple theme or frosted chart/periodontogram without a separate product-owned design-contract change and clinical acceptance. Public Uribe Villa is out of scope. |
| **Church OS** | Quiet header/sidebar/context accents around People, Agenda and other operator work | Its current `DESIGN.md` governs tenant branding, single visible truth and non-nested task flows. **Tesorería** and audit-related values remain opaque and precise; Local/tenant authorization is never presentation-derived. |

These are proposed **adoption profiles**, not assertions that any product has implemented or accepted the glass system. A `DESIGN.md` update and scoped owner approval are required before shipping material changes in an existing product. Approval of this Handbook Pattern is **not** release approval.

## Adoption sequence and evidence

1. Read the consumer's current `AGENTS.md`, `DESIGN.md`, tokens, tenant boundaries, known freezes and real deployed screenshots. Classify the operator task and its visual density; compare a *no-glass* baseline to the proposed material treatment.
2. Decide whether glass improves **orientation or perceived continuity** without degrading scanning, input, contrast, speed or trust. If the answer is no, use solid surfaces. Record the choice in the existing product design contract; no second source of truth.
3. Prototype the narrowest valuable slice: global shell, one realistic dense data screen, one form/overlay, both real empty/error states, and a narrow/mobile state. Use realistic synthetic data in demos; do not invent production customer, clinical or financial facts.
4. Review and accept a product-specific material map and token projection. Reuse existing primitives and test the opaque fallback before adding blur. Keep demo/product/public-site isolation intact.
5. Implement only on an explicitly authorized product branch/release scope. Keep domain logic, API behavior, permissions and persistence unchanged unless separately requested and verified.
6. Verify with actual rendered evidence and disclose missing gates. Only then consider widening the adoption or changing the canonical product contract.

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

This Pattern may be strengthened into a more prescriptive design-system contract **only after scoped product adoption and real cross-Vertical evidence**. Until then, `pat-design-context-layering` keeps the visual decision local and this page provides a repeatable, deliberately limited method.

## Agent context projection

```json agent-context
{
  "units": [
    {
      "id": "operator-glass-material-adoption-decision",
      "type": "decision-question",
      "text": "When designing a MelodIQ operator console, inspect the current product DESIGN.md, approved theme, user tasks, tenant scope and visual evidence. The owner favors restrained Glassmorphism, but it is a candidate only: does this product authorize it and does it improve task orientation without harming data clarity, accessibility, speed or density? Do not import a shared color/font/logo or automatically re-theme a production app.",
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
