---
id: pat-operator-console-shell-interactions
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - authenticated-operational-consoles
  - admin-workspaces
  - vertical-products
sources:
  - src-21st-curtain-theme-toggle
  - src-21st-manual-sidebar
  - src-aceternity-sidebar
  - src-mdn-start-view-transition
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-10-30
review_due: 2027-01-30
---

# Operator Console Shell: Theme, Sidebar and Continuity

## Intent, authority and scope

MelodIQ Systems' preferred **interaction direction** for its authenticated operator consoles is a compact, legible shell: an accessible curtain-style light/dark switch at the far right of the header; a calm, expandable navigation rail; and route changes that feel continuous instead of abruptly replacing the screen.

This is an owner-selected reusable **Pattern**, not a company-wide CSS framework, dependency, palette, brand, or permission to override each product's active `DESIGN.md`. Use it when designing a new MelodIQ admin console or performing an expressly authorized shell transformation in MelodIQ Core, DentalOS, Church OS, Ops OS or a future Vertical. Existing release freezes, clinical/privacy requirements and deliberate light-only product contracts remain in force until that product's migration is separately authorized and verified. Public marketing, patient/member self-service, kiosk and print surfaces choose their own composition.

The result should look **native to the product**, not like a copied SaaS demo. Reuse behavior and state contracts; resolve typography, contrast, density, geometry, color and brand from the owning repository and `pat-design-context-layering`.

### Evidence and precedents

- **Verified internal donor — theme and route continuity:** `Kappa-Bot/MelodIQ-Core` commit `4777ee0bbfc46a5c3df32ad2b21f9823799316ef`. Study `apps/platform/app/components/ui1/theme-locale-controls.tsx`, `workspace-shell.tsx`, `apps/platform/app/orbit.css` and `test/ui1/shells.spec.ts`. The curtain switch, header placement and route-stage behavior were observed in the authenticated production shell on 2026-10-30.
- **Verified internal donor — compact hover/focus rail:** `Kappa-Bot/MelodIQ-Core` commit `3b35d775d52727f5061abb518344bd9541fa9ff3`. Study `apps/platform/app/components/ui1/primary-navigation.tsx`, `apps/platform/app/orbit.css` and `test/ui1/shells.spec.ts`. The production shell was observed expanding the compact rail on pointer hover and keyboard focus while retaining the content column; mobile/200%-zoom acceptance and the automated full test gate were not run for this increment.
- **Curtain interaction:** `src-21st-curtain-theme-toggle` is a visual/behavioral reference (icon toggle and approximately 600 ms reveal), not an automatically approved runtime dependency or licensed source-code transplant.
- **Expandable sidebar:** `src-21st-manual-sidebar` links to the original `src-aceternity-sidebar` implementation: hover expansion on desktop, responsive mobile composition and dark support. Its stock demo links, logo, user, spacing and color choices are **not** MelodIQ product requirements.
- **Browser API:** `src-mdn-start-view-transition` describes same-document view transitions and compatibility; feature-detect and provide a no-animation fallback.

## 1. Theme control: header-owned, persistent and honest

1. Place a compact sun/moon button at the **rightmost end of the persistent top bar**, adjacent to any language/account controls. Do not bury theme preferences in a footer or duplicate them on every page. An authentication shell may expose the same control in its own header.
2. Give the control a native `button`, meaningful accessible name for the **next action**, visible focus and a truthful selected/pressed state. The language selector (if supported) is a separate native control. Keep usable pointer/touch targets and never rely on a decorative icon alone.
3. The product's current, authoritative preference must set the **initial server-rendered theme** (cookie or authenticated server preference where appropriate) and the semantic document color scheme. An optimistic client update can improve perceived speed, but must reconcile with the persisted value and visibly recover if saving fails. Do not silently claim persistence when it does not exist.
4. Map semantic roles across light/dark (canvas, elevated surface, text, muted text, border, focus, selected, success, warning, danger); resolve tenant branding within the existing safe token contract. Do not invert the page using global CSS filters or introduce pure-black body copy/illegible status colors.
5. Prefer a short curtain reveal using `document.startViewTransition(updateTheme)` and feature detection. Apply the real DOM theme update inside the callback, never behind a long delay. The donor uses a ~600 ms decelerated `clip-path` reveal of the new root view, without blocking input or adding a motion library solely for this effect.
6. When the API is unavailable, errors, or `prefers-reduced-motion: reduce` is active, switch immediately without the curtain. Clean up transition flags on both success and rejection. Do not make the user wait for the animation to finish before the theme can be used.
7. If the product supports a system preference, define its precedence and switching rules explicitly. Do **not** present a system option or sync behavior that the app has not implemented.

Minimal CSS interaction contract (adapt token and naming conventions to the target app):

```css
html[data-theme-transition="curtain"]::view-transition-old(root) {
  animation: none;
}
html[data-theme-transition="curtain"]::view-transition-new(root) {
  animation: console-theme-curtain 600ms cubic-bezier(.16, 1, .3, 1) both;
}
@keyframes console-theme-curtain {
  from { clip-path: inset(0 0 0 100%); }
  to { clip-path: inset(0 0 0 0); }
}
@media (prefers-reduced-motion: reduce) {
  html[data-theme-transition="curtain"]::view-transition-old(root),
  html[data-theme-transition="curtain"]::view-transition-new(root) {
    animation: none !important;
  }
}
```

This is an interaction sketch, **not a complete implementation**; see the internal donor for lifecycle, error rollback, SSR preference propagation and tests. Do not animate or duplicate sensitive page content through external screenshots or third-party effects.

## 2. Sidebar: expandable, deliberate, keyboard-safe

### Desktop / pointer-fine

- Start from a **recognizable compact navigation rail** (indicatively 72–80 px) with legible iconography and a current-destination indicator. On pointer hover, temporarily reveal labels and groups in an expanded surface (indicatively 216–240 px), with a **decelerated 220–320 ms** width/opacity treatment. Do not hide essential navigation behind icons with ambiguous meaning.
- Prefer a slight **hover-intent delay** and exit grace where necessary to prevent jitter as the pointer crosses the rail boundary. Hover-only expansion is an enhancement; a keyboard user must be able to reveal the same labels with focus and use every destination. Keep expanded while its descendants have focus.
- Provide an **explicit expand/pin control** where a dense/frequent operator workflow benefits from a permanently open sidebar. If a preference is saved, restore it without hydration jank; do not make persistence a requirement to navigate.
- Avoid shifting, shrinking or reflowing a dense table whenever the pointer merely grazes the rail. Temporary expansion may overlay the content with appropriate elevation; an explicitly pinned width may reserve layout space. Never cover focused controls without recovery.
- Primary links are real links, current destination uses `aria-current="page"`, grouping reflects the owning product's information architecture, and permission-sensitive entries derive from verified navigation state. A pretty sidebar cannot replace server-side authorization.
- The top slot carries approved product/tenant identity; the bottom may carry useful profile/exit actions **inside the rail**. Do not add an always-visible decorative global footer to operational screens.

### Touch / narrow viewport

- Do not imitate hover. Use an explicit, named menu button opening a mobile drawer or equivalent product-approved navigation pattern, with `aria-expanded` and correct `aria-controls`.
- On open, manage focus and scroll containment; close with Escape, a visible close button, route selection and appropriate outside interaction; restore focus to the trigger. Respect safe areas, virtual keyboard and 320 CSS-px reflow at 200% zoom.
- Do not duplicate independent navigation DOMs with inconsistent active state, authorization or labels. Keep one source of navigation truth even if desktop and mobile render differently.

### Visual quality

- Animate only the properties that explain expansion (width/transform/label opacity), with one consistent easing curve; **never** use `transition: all` as a shortcut.
- Suppress nonessential motion under reduced-motion settings; links must remain visible/readable and usable during and after a transition.
- Use semantic theme tokens rather than shipping Aceternity's neutral/black demo palette. No copied "Acet Labs" logo, avatar, placeholder KPI blocks or unapproved imagery.
- Prefer existing app primitives and CSS when they satisfy the contract. Add `motion`/`framer-motion` or a sidebar package only with a documented user-facing need, compatibility, license and bundle assessment.

## 3. Navigation between screens

Treat route changes as state transitions with consistent shell, not page flashes:

- Keep sidebar, top bar, tenant context and focus affordances stable while the **route content region** updates.
- For real route changes, use a modest entry (the verified Core donor uses ~360 ms decelerated fade and 10 px vertical settling), or the app's existing equivalent. Never animate a blank full page, block an available action, or re-run entry motion on every text/data refresh.
- Preserve or deliberately reconcile filters, selections, return path and focus after navigation. Loading skeletons reflect actual pending work; avoid fake delays, duplicate page headings and empty space that pushes routine work below the fold.
- Reduced-motion, browser history, slow data, authorization failures, hard refresh and theme changes must keep truthful content and operable controls. Do not let transitions capture stale or unauthorized tenant information.

## 4. Adoption workflow for any console

1. **Read local authority:** `AGENTS.md`, `DESIGN.md`, current surface contract, theme tokens, navigation model and privacy constraints. Record any conflicting freeze/light-only intent; an external demo alone cannot override it.
2. **Inventory the real shell:** header controls, sidebar states, login/auth shell, route boundaries, desktop/mobile/zoom, source of preferences, loading/error paths and existing accessibility.
3. **Choose integration:** adapt existing components first; use the MelodIQ Core donor only for relevant mechanics. Decide product-owned collapsed/expanded widths, persistence, SSR preference channel, theme token coverage and breakpoints. Keep one canonical implementation per app.
4. **Implement in bounded slices:** (a) theme semantics/persistence, (b) header toggle and curtain, (c) sidebar desktop/keyboard/mobile, (d) route continuity. Do not migrate protected domain screens, public sites or unrelated CSS as collateral work.
5. **Verify with real rendering:** record desktop, 320 px and 200% zoom; light/dark contrast and hard refresh; keyboard/focus; mouse hover/exit; touch drawer/Escape; reduced motion; route transitions/back-forward; pending/failed preference save; current route and authorization; no console errors or unwanted layout shift.
6. **Ship and report evidence by layer:** local tests/build, deployed exact SHA, live authenticated smoke and visual review are distinct. Report `NOT RUN`/`BLOCKED` explicitly; a Handbook Pattern does not mean DentalOS/ChurchOS has implemented or accepted it.

### Acceptance matrix (adapt to the product)

| Scenario | Minimum observed result |
|---|---|
| First render and reload (light/dark) | Correct persisted theme, no wrong-theme flash, header control reflects state |
| Toggle with motion enabled | Curtain moves smoothly; next-theme content and controls remain usable |
| Toggle with reduced motion/API missing | Immediate safe switch; no invisible/competing layers |
| Preference-save rejection | Truthful error and visual rollback/reconciliation |
| Desktop rail: pointer enter/leave | Smooth expansion/retraction, no flicker or unintended content reflow |
| Keyboard tab/focus inside rail | Labels reachable, focus remains visible, no hover dependence |
| Pinned rail or active route | Stable state, correct `aria-current`, no stale user/tenant scope |
| Mobile, 320 px, zoom 200% | Named open/close, Escape and focus return, no blocked controls or horizontal overflow |
| Route change/back/forward/loading | Context persists or resets intentionally; no blank flicker; focus meaningful |
| Role/tenant and error scenarios | No permission leakage, misleading states or raw backend diagnostics |

## 5. Portfolio adoption status

- **MelodIQ Core (2026-10-30):** curtain header toggle, preference persistence, route-stage motion and footer removal implemented and observed live. The compact/pinned sidebar also expands smoothly on desktop pointer hover and keyboard focus without moving the main column (production `3b35d775`); mobile dialog is retained from the preceding implementation. The current CI runner could not start its steps, so this is live interaction evidence, not a green full-suite or mobile/zoom acceptance receipt.
- **DentalOS:** current MD-1 contract explicitly specifies light-only operation and limited motion. This Pattern records the owner's desired future console direction; a separate authorized design-contract amendment, token work and clinical/privacy/visual acceptance must precede a dark-mode or sidebar rollout. Public Uribe Villa and patient surfaces are not implicitly in scope.
- **Church OS / Ops OS / future Verticals:** use this Pattern as a candidate for the next authorized operational shell design, preserving their specific roles, tenant branding, accessibility, performance and active release gates. No cross-repo deployment is asserted here.

## Sources and reuse

Material external precedents are registered in `machine-readable/sources.yaml`. The 21st.dev and Aceternity examples are design evidence; do not paste their demo implementation or add dependencies merely because they appear there. Where an external implementation is copied or materially adapted, verify the exact source/package license and comply with attribution/notice obligations. See `gov-source-authority`, `gov-knowledge-promotion` and `pat-design-context-layering`.
