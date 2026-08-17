---
id: pat-mobile-responsive-interaction
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - mobile-web
  - touch-heavy-web-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-cssom-view
  - src-w3c-css-env
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Mobile Responsive Interaction

## Intent

Use this Pattern when mobile quality depends on more than CSS breakpoints: virtual keyboards, bottom navigation, overlays/sheets, gestures, edge safe areas, cameras/scanners or installed-app chrome.

The central idea is that **mobile is a physical interaction environment**, not a narrow desktop screenshot.

## 1. Reflow before breakpoint decoration

Start from the content/workflow and preserve required information/actions down to the applicable reflow floor.

For ordinary vertically scrolling content, use 320 CSS px as an accessibility verification floor because WCAG 2.2 Reflow defines that equivalent width for non-exempt content.

Project test matrices MAY add representative product/device widths (for example 360, ~390/412, tablet, landscape) based on actual users. Do not turn a donor repository's exact device matrix into a universal list.

Do not disable zoom to protect layout.

## 2. Find geometry defects; do not hide them

A root-level `overflow-x: hidden` can conceal symptoms while focusable/meaningful content remains clipped or transformed outside the visual viewport.

Prefer:

1. identify the offending element;
2. fix min-width/flex/grid/transform/content wrapping;
3. constrain overflow locally only where the component intentionally owns it;
4. verify meaningful descendants remain reachable/visible.

`document.scrollWidth <= innerWidth` is useful but not sufficient: transforms can visually displace an element without increasing layout overflow. Critical responsive tests SHOULD assert bounding-box containment/visibility for elements whose placement is part of acceptance.

## 3. Virtual keyboard is product behavior

If the workflow includes editable fields plus fixed/sticky UI, overlays or bottom navigation, treat the virtual keyboard as a first-class state.

Where supported and relevant, use `window.visualViewport` resize/scroll information to reason about the actually visible area rather than assuming the layout viewport equals the usable viewport.

Typical outcomes:

- hide or reposition bottom navigation that would compete with focused editing;
- keep the focused field and its error/help/action visible;
- size bottom sheets to the visible viewport rather than a stale full-screen height;
- avoid fixed footers covering form actions.

Provide a sensible fallback for user agents where the API/behavior differs.

## 4. Safe areas

Controls anchored to viewport edges SHOULD incorporate `env(safe-area-inset-*)` when display geometry can overlap essential content.

Safe-area padding is not a universal decoration. Apply it at the component/shell that owns the edge.

## 5. Bottom navigation and horizontal strips

Bottom navigation MUST NOT cause document-level horizontal overflow.

When the number/width of destinations cannot fit:

- simplify based on product priorities; or
- allow the navigation strip itself to scroll horizontally when that remains understandable.

For horizontal tabs/chips/filters, prefer local horizontal scrolling/scroll snapping over making the whole page wider.

Keep the vertical page scroll and horizontal strip scroll ownership unambiguous.

## 6. Gestures and direct manipulation

A gesture surface MUST have explicit ownership.

For draggable sheets/carousels/etc.:

- start drag only from an intentional handle/surface when child content needs its own scrolling or tapping;
- do not steal vertical page/list interaction from ordinary content;
- use pointer/touch behavior appropriate to the interaction;
- keep per-frame interaction work out of expensive application state when direct transform/animation state is more appropriate;
- expose a non-drag alternative when WCAG requires it.

A drag affordance is not permission to make the rest of the sheet a gesture trap.

## 7. Camera/scanner flows

When camera/scanner behavior is part of the product, design for the physical context:

- choose front/rear camera based on the workflow rather than a single global default;
- account for whether preview mirroring matches the operator/user context;
- preserve/recover the camera session across expected background/foreground transitions when feasible;
- provide a truthful fallback when browser detection APIs/camera access are unavailable;
- keep permission/error/retry states usable on the target device.

Desktop emulation cannot prove camera ergonomics.

## 8. Touch targets and focus

Use the `std-ui-ux-quality-baseline` target-size/accessibility floor.

For frequent mobile operational controls, prefer generous targets (roughly 44 CSS px or larger) and spacing even when the WCAG minimum can technically be met with less.

Visible focus/keyboard navigation still matter on mobile/tablet because users can attach keyboards, use switch/speech input, or encounter hybrid devices.

## 9. Verification matrix

Choose evidence by risk, not device-count vanity.

A material mobile interaction change SHOULD cover:

- 320 CSS px reflow/accessibility floor where applicable;
- one or more representative phone widths;
- orientation/tablet when the product supports or benefits from them;
- long/localized content;
- focused editable field + real/emulated keyboard behavior;
- safe-area anchored UI;
- gesture alternative and child scrolling;
- camera/permissions when relevant.

Use a real device when the acceptance condition is inherently native/physical (installed PWA, keyboard feel/layout, camera ergonomics). Report missing real-device verification honestly.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "mobile-physical-interaction-state",
      "type": "decision-question",
      "text": "Does the affected mobile workflow depend on virtual keyboard, safe-area, fixed-edge UI, gestures, camera/scanner, or installed-app behavior that changes the actually usable viewport or interaction?",
      "source": "pat-mobile-responsive-interaction",
      "covers": ["accessibility", "compatibility"],
      "activate_when": ["surface:frontend", "capability:pwa"],
      "phase": ["planning"],
      "priority": 76
    },
    {
      "id": "mobile-focused-content-visible",
      "type": "constraint",
      "text": "Keep focused editable content and required actions reachable and visible when virtual keyboards, fixed navigation, sheets, or safe areas reduce the usable viewport.",
      "source": "pat-mobile-responsive-interaction",
      "covers": ["accessibility"],
      "activate_when": ["surface:frontend", "capability:pwa"],
      "phase": ["implementation", "verification"],
      "priority": 82
    },
    {
      "id": "mobile-native-physical-verification",
      "type": "verification",
      "text": "Use representative real-device verification when acceptance depends on installed-PWA, virtual-keyboard feel/layout, safe-area geometry, or camera ergonomics; otherwise record that physical gate as not run.",
      "source": "pat-mobile-responsive-interaction",
      "covers": ["accessibility", "compatibility"],
      "activate_when": ["capability:pwa", "surface:frontend"],
      "phase": ["verification"],
      "priority": 88
    }
  ]
}
```
