---
id: std-ui-ux-quality-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - user-facing-web-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-08-15
review_due: 2027-02-15
---

# UI/UX Quality Baseline

## Purpose

Define the minimum product-quality bar for user-facing web interfaces without prescribing a visual style, component library, CSS framework, layout grammar, or brand system.

This Standard is a **quality floor, not a creative ceiling**. Product identity, art direction, density, composition, motion language, typography, color, shape, and component choices remain repo-local unless another applicable Standard or decision constrains them.

A technically functional interface can still fail this Standard when its hierarchy, interaction, accessibility, responsive behavior, states, or visual execution make the product materially harder to use or materially weaker than its intended product/brand quality.

## Applicability

This Standard applies to user-facing web surfaces, including:

- public/marketing sites;
- authenticated product/admin interfaces;
- forms, wizards, configurators, dashboards and workspaces;
- installable web-app/PWA surfaces;
- touch-oriented, kiosk or field-operation interfaces.

The depth of visual polish and evidence is proportional to the surface. A public sales experience, an operations desk and a maintenance console do not need the same art direction, but all must meet applicable usability/accessibility requirements.

## 1. Preserve product intent and creative freedom

The implementation MUST derive its visual/interaction direction from the repository's real product, brand, users and existing decisions before defaulting to framework or template conventions.

This Standard MUST NOT be interpreted as requiring:

- Material, shadcn, Radix, Bootstrap or another component system;
- cards as the default container;
- a sidebar/topbar dashboard composition;
- a particular border radius, shadow, palette, grid or typography system;
- Tailwind, CSS Modules or another styling mechanism;
- a particular animation library;
- visual sameness across unrelated products.

When distinctive visual quality is part of the scope, framework defaults or a generic generated-SaaS composition are not, by themselves, a finished design decision.

Consistency means coherent product rules, not identical composition everywhere.

## 2. Information hierarchy and decision support

Each meaningful screen MUST make its primary purpose understandable without requiring the user to reverse-engineer the layout.

For task-oriented surfaces:

- the current context/state MUST be clear;
- the primary action or next decision SHOULD be visually dominant when one exists;
- secondary actions SHOULD not compete with the primary action without a product reason;
- related information SHOULD be grouped by user intent, not merely by data model;
- repeated labels/copy/chrome SHOULD be removed when they do not improve orientation or decision-making;
- empty visual volume MUST NOT push frequent work out of the practical viewport without purpose.

A component exists to support understanding, navigation, input, comparison or action. Decorative containers SHOULD NOT proliferate solely to make the interface look "designed".

## 3. Interaction states

Interactive flows MUST handle the states that can materially occur, not only the happy path.

As applicable, define and verify:

- initial/empty;
- loading/pending;
- populated;
- validation;
- error/failure;
- success/confirmation;
- disabled/unavailable;
- partial or stale data;
- destructive confirmation/recovery;
- offline/network-required state when `std-web-pwa-baseline` applies.

State transitions MUST preserve enough context for the user to understand what happened and what they can do next.

Errors MUST be associated with the affected control/content and SHOULD explain a useful recovery action. Important asynchronous feedback SHOULD be exposed accessibly, for example through appropriate live-region behavior when semantic HTML alone is insufficient.

## 4. Accessibility baseline

Applicable user-facing web content MUST target WCAG 2.2 Level AA unless an explicit external obligation requires a different/higher target or a documented exception is permitted.

At minimum:

- interactive functionality MUST be operable without relying solely on a mouse;
- focus MUST be visible and MUST NOT be fully obscured by author-created sticky/fixed UI;
- DOM/focus order MUST follow a meaningful interaction order;
- controls MUST have programmatic names that match visible intent;
- information MUST NOT rely on color alone;
- non-exempt content MUST reflow without loss of information/functionality at the WCAG 320 CSS-pixel equivalent;
- pointer targets MUST meet WCAG 2.2 Target Size (Minimum), including its documented exceptions;
- drag interactions MUST expose a non-drag single-pointer alternative unless dragging is essential;
- authentication/input flows MUST avoid unnecessary cognitive barriers covered by applicable WCAG criteria.

For frequent primary controls on touch-heavy, field, kiosk or mobile operational surfaces, prefer approximately **44×44 CSS px or larger** even though the WCAG AA minimum can be smaller. This is an internal quality recommendation, not a replacement for WCAG's normative criteria.

Use semantic HTML before adding ARIA. When implementing an ARIA composite/pattern, use the applicable WAI-ARIA APG pattern as interaction guidance and verify the actual browser/assistive-technology behavior; an APG example is not production code to copy blindly.

## 5. Responsive and zoom behavior

Responsive quality is behavioral, not a set of fashionable breakpoints.

User-facing surfaces MUST:

- avoid losing required information/actions at narrow/reflowed widths;
- avoid page-level horizontal overflow for content that does not intrinsically require two-dimensional interaction;
- preserve readable hierarchy when text wraps or content grows;
- allow browser/user zoom rather than disabling it to protect a layout;
- adapt fixed/sticky UI so it does not consume or obscure an unreasonable share of the visible viewport;
- keep critical actions reachable with keyboard, touch and pointer input as applicable.

Do not use global `overflow-x: hidden` or equivalent clipping as a substitute for finding the element that actually breaks layout. Local clipping may be legitimate when it is part of the intended component behavior and does not hide required content/focus.

Transforms can move meaningful UI outside the visual viewport without changing document `scrollWidth`; material responsive QA SHOULD therefore include element-containment/visibility checks in addition to overflow checks.

Use `pat-mobile-responsive-interaction` when virtual keyboards, bottom navigation, overlays, gestures, cameras or edge-anchored controls materially affect the mobile experience.

## 6. Forms and data entry

Forms MUST distinguish required from optional information and SHOULD request only information necessary for the current decision/workflow.

- Labels and instructions MUST remain understandable without placeholder text alone.
- Validation SHOULD occur at a point where it helps recovery rather than surprising the user only after a long flow.
- Optional enhancements such as photos, precise location, secondary metadata or preferred channels MUST NOT become accidental blockers unless the product requirement makes them mandatory.
- Multi-step flows MUST preserve/communicate progress and SHOULD permit safe correction without unnecessary re-entry.
- Destructive reset/cancel actions SHOULD be proportionately protected based on consequence.

When mobile virtual keyboards change the usable viewport, apply `pat-mobile-responsive-interaction`.

## 7. Motion and direct manipulation

Motion MUST support orientation, causality, hierarchy or product character rather than compensate for weak composition.

- Required information/actions MUST remain understandable when reduced motion is requested.
- Motion MUST NOT create intervals where two competing text/state layers are simultaneously unreadable.
- Direct-manipulation gestures SHOULD feel responsive and MUST preserve a non-gesture alternative where accessibility requires it.
- Hover-only affordances MUST NOT be the sole way to discover or operate required functionality.

A highly expressive public experience MAY use substantially more motion/3D/editorial composition than an operational workspace. The quality criterion is deliberate fit, not minimal animation.

## 8. Theme and visual semantics

If multiple themes are supported:

- semantic roles (surface, text, action, status, focus, border/elevation where relevant) SHOULD remain equivalent across themes;
- selection and focus MUST remain distinguishable;
- theme controls MUST have clear title/description/selected semantics;
- system/light/dark behavior MUST be tested as distinct states when the product claims them.

Do not hardcode a donor product's palette into another product merely because its theme model was reusable.

## 9. Visual verification

For materially visual changes, code review alone is insufficient.

The change SHOULD be rendered and inspected at the viewports/states that can materially change the decision. Verification SHOULD cover:

- intended hierarchy and composition;
- content wrapping/realistic content;
- required interaction states;
- narrow/mobile and representative desktop conditions;
- applicable theme states;
- focus/keyboard behavior;
- reduced-motion behavior when motion is material;
- no hidden/clipped critical content;
- product/brand fit.

When visual evidence is retained or used to make acceptance claims, apply `pat-visual-evidence-integrity`.

If tooling cannot render/inspect the UI or required native-device behavior, report that visual/native gate as **not run** instead of inferring quality from code.

## 10. Definition of done for UI work

A user-facing visual change is complete only when:

- the intended user decision/task is clearer or at least not degraded;
- applicable states are implemented;
- applicable WCAG 2.2 AA requirements are respected;
- responsive behavior is verified at risk-relevant widths;
- material visual output has been inspected when tooling permits;
- no known high-severity client-visible defect remains in the tested scope;
- unrun browser/device/accessibility/visual gates are disclosed;
- repo-specific visual identity remains repo-specific rather than being replaced by handbook aesthetics.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "ui-accessibility-baseline",
      "type": "constraint",
      "text": "Target applicable user-facing web content to WCAG 2.2 AA and preserve keyboard operation, visible focus, meaningful naming/order, reflow, and non-color-only semantics.",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["accessibility"],
      "activate_when": ["surface:frontend", "risk:accessibility"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 100
    },
    {
      "id": "ui-responsive-integrity",
      "type": "constraint",
      "text": "Preserve required information and actions at narrow widths and do not hide real layout defects with global overflow clipping.",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["accessibility"],
      "activate_when": ["surface:frontend"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 75
    },
    {
      "id": "ui-visual-verification",
      "type": "verification",
      "text": "Render and inspect materially visual changes at risk-relevant states and viewports, and report browser, device, accessibility, or visual gates that were not run.",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["accessibility"],
      "activate_when": ["surface:frontend", "archetype:ui-flow-change", "archetype:visual-regression-fix"],
      "force": "should",
      "phase": ["verification"],
      "priority": 90
    },
    {
      "id": "ui-quality-floor-not-style",
      "type": "constraint",
      "text": "Use the handbook as a quality floor, not as a shared art direction, component system, or visual template for unrelated products.",
      "source": "std-ui-ux-quality-baseline",
      "covers": [],
      "activate_when": ["surface:frontend"],
      "force": "must-not",
      "phase": ["planning"],
      "priority": 25
    }
  ]
}
```
