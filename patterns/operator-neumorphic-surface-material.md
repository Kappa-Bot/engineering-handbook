---
id: pat-operator-neumorphic-surface-material
kind: pattern
status: active
owner: engineering
version: "1.0"
applies_to:
  - authenticated-operational-consoles
  - admin-workspaces
  - selected-product-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-11-19
review_due: 2027-02-19
---

# Accessible Neumorphism: selective tactile depth

## Selection and authority

Neumorphism (also called *neomorphism*, *neumorfismo* or *soft UI*) is a **selectable visual direction**, not the default for MelodIQ's internal consoles. Its raised/inset light-and-shadow language can make a few controls feel tactile; it is unsuitable when it makes actual interaction targets, text, focus or state ambiguous. [The visual-direction catalog](visual-direction-catalog.md) owns selection and precedence. `std-ui-ux-quality-baseline` owns the accessibility/quality floor; `pat-design-context-layering` keeps product and tenant identity local.

A chosen direction never authorizes re-skinning a product, changing data/permission logic or publishing. Record the decision in the current product's existing `DESIGN.md` only within an authorized material redesign. An audit remains read-only. Neumorphism is **not a synonym for round cards, beige backgrounds or no borders**; blind use creates generic, inaccessible AI slop.

## A functional material hierarchy

| Plane | Suitable treatment | Reject |
| --- | --- | --- |
| Navigation/context | A restrained raised or inset region only where it clarifies grouping or location | Every tab, chip and side panel embossed simultaneously |
| Primary controls | A clearly bounded pressable shape; optional shadow gives *secondary* depth | Shadows as the only clue that a button exists or is pressed |
| Data/form workspace | Opaque, flat-to-solid, high-contrast reading and input plane | Inset spreadsheet cells, clinical readings or form fields with illegible edges |
| Focus/selection/errors | Explicit outline, semantic color plus text/icon where needed, accessible state announcement | A subtle dark shadow as the only focus, selected, invalid or disabled signal |
| Elevated context | Clearly separated popover/dialog with stable foreground and focus handling | Nested soft shadow tunnels that conceal the active layer |

Choose task hierarchy, density and geometry **before** decorative depth. A dense operations, treasury or clinical screen can remain almost entirely solid under a Neumorphic product direction. A functional fallback is a coherent design, not a degraded failure mode.

## Semantic token projection

Use existing product tokens where possible. These are roles, not mandated CSS variable names or copied colors:

| Role | Responsibility |
| --- | --- |
| `surface.base` / `surface.data` | Stable opaque canvases, independently readable |
| `surface.control` | Touchable control fill distinguishable from its surroundings |
| `edge.control` / `edge.focus` / `edge.selected` | Perceptible boundaries, keyboard focus and selection without relying on shadow |
| `depth.raised` / `depth.inset` | Optional, limited light/shadow cue after semantics are satisfied |
| `text.primary` / `text.secondary` | Readable over each actual surface/theme |
| `status.*` / `selected` / `disabled` | Truthful and redundant state signals |

Resolve light/dark separately; do not invert one light-source recipe mechanically. The light-source direction, shadow polarity and border/focus system must be coherent within the selected product and tenant palette. Density and typography stay product-owned. Do not copy a demonstration token set into all MelodIQ products.

### Progressive enhancement sketch

CSS pseudocode, **not** a cross-repo dependency:

```css
.soft-control {
  color: var(--text-primary);
  background: var(--surface-control);
  border: 1px solid var(--edge-control);
  box-shadow: var(--depth-raised);
}
.soft-control:focus-visible {
  outline: 2px solid var(--edge-focus);
  outline-offset: 2px;
}
.soft-control[aria-pressed="true"] {
  border-color: var(--edge-selected);
  box-shadow: var(--depth-inset);
}
@media (forced-colors: active) {
  .soft-control {
    color: ButtonText;
    background: ButtonFace;
    border-color: ButtonText;
    box-shadow: none;
  }
  .soft-control:focus-visible { outline-color: Highlight; }
}
```

Actual state and action semantics come from the proper native element/ARIA pattern; visual depth does not create interaction. Test with CSS shadows removed, with forced colors and at 200% zoom. WCAG 2.2 non-text contrast applies to visual information required to identify a control/state; text/essential data retain their own contrast requirements. See `src-w3c-wcag-22` for the normative criterion rather than treating a CSS swatch as proof.

## Critical failure modes

- **Invisible affordance:** a button appears to be part of the background. Add an explicit edge, label, hit area and focus state; measure the actual composite.
- **State by shadow:** raised versus inset is too subtle or unavailable. Pair with `aria-pressed`/selected state, label/icon/text, clear focus and an error/disabled contract. Never use shadow polarity as the sole status cue.
- **Low-contrast form:** inset fields hide labels, placeholders, validation or autofill content. Keep real labels, readable borders, actual errors and recovery actions.
- **Decorative proliferation:** large soft cards push frequent tasks below the fold and make density worse. Reduce layers and preserve a common reading plane.
- **Theme/brand leakage:** a platform shadow palette is copied into tenant colors, public marketing or a clinical product without approval. Resolve the product's `DESIGN.md` and identity boundaries first.
- **Motion/render cost:** animated shadows or endless elevation changes degrade input/scroll responsiveness. Measure on realistic low-end devices, disable gratuitous motion, and provide a solid no-shadow fallback.

## Acceptance and evidence

For an authorized Neumorphic implementation, inspect a real dense screen, a form, an interactive control, open/closed overlay states, empty/error/disabled/selected/focused states and narrow/mobile usage. Verify keyboard, touch, focus return, screen-reader naming and actual state truth. Compare light/dark only where supported; test forced-colors, no-shadow fallback, 320 CSS px and 200% zoom. Measure paint/scroll and interaction where depth effects are substantial. Record exact build and unrun device/assistive-tech gates rather than promoting a prototype to production evidence.

For MelodIQ Core, Ops OS, DentalOS and Church OS, inspect the *current* product contract; no previous prototype or this Pattern is evidence that any product has already adopted Neumorphism. Financial/clinical data, tenant permissions, audit trails and existing operational behaviors remain protected.

## Agent context projection

```json agent-context
{
  "units": [
    {
      "id": "operator-neumorphic-material-decision",
      "type": "decision-question",
      "text": "For explicit Neumorphism in an authorized operator console, verify local DESIGN.md and the catalog precedence; preserve solid data, identifiable control edges and semantic state without shadow. A style request never grants migration or production release, and the scoped internal default remains only a candidate where no local choice exists.",
      "source": "pat-operator-neumorphic-surface-material",
      "covers": ["neumorphic-material-fidelity"],
      "activate_when": ["archetype:operator-neumorphic-material-change"],
      "phase": ["planning", "implementation"],
      "priority": 80
    },
    {
      "id": "operator-neumorphic-material-acceptance",
      "type": "verification",
      "text": "If an authorized internal-console direction explicitly selects Neumorphism, verify identifiable controls without shadows, focus/pressed/selected/error/disabled states, semantic labels, opaque dense-data planes, actual text/non-text contrast, 320px/200% zoom, touch/keyboard, forced-colors/no-shadow fallback, product/tenant isolation and measured render cost. Disclose all unrun device/assistive-tech gates; never treat a soft UI prototype as production adoption.",
      "source": "pat-operator-neumorphic-surface-material",
      "covers": ["neumorphic-material-fidelity", "accessibility", "performance", "compatibility"],
      "activate_when": ["archetype:operator-neumorphic-material-change"],
      "phase": ["verification"],
      "priority": 82
    }
  ]
}
```
