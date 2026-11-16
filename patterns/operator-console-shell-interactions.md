---
id: pat-operator-console-shell-interactions
kind: pattern
status: active
owner: engineering
version: "0.2"
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
last_verified: 2026-11-16
review_due: 2027-02-16
---

# Operator Console Shell: Theme, Sidebar and Continuity

## Intent, authority and scope

This Pattern provides **optional shell mechanics**: persistent theme preferences, expandable navigation and route continuity. Choose the shell composition from the actual operator tasks and the direction established under [UI/UX Quality Baseline §1](../standards/ui-ux-quality-baseline.md#1-product-specific-design-and-reconstruction). A compact rail, curtain reveal, right-edge toggle or animated route entry is not a portfolio default.

Use it when relevant to a new operator console or an authorized shell change, not as a mandatory layout or CSS dependency. Within an authorized redesign, replace inadequate shell composition and supersede the affected `DESIGN.md` decisions; prior approval alone does not protect a weak design. Explicit current theme constraints, release freezes, clinical/privacy requirements and authorization boundaries still apply. Public marketing, patient/member self-service, kiosk and print surfaces choose their own composition.

The result should look **native to the product**, not like a copied SaaS demo. Reuse behavior and state contracts where useful; resolve or deliberately reconstruct typography, contrast, density, geometry and color through the current direction and `pat-design-context-layering`. Preserve legal identity and authentic brand assets unless their alteration is separately authorized.

If the direction selects a translucent material treatment, consult `pat-operator-glass-surface-material` for glass navigation, opaque data and elevated context. The shell behavior here does **not** require Glassmorphism.

**Supersession, 2026-11-16:** the earlier portfolio preference for a compact first-render rail, far-right curtain toggle and animated route entry is retired. The donor records below remain historical evidence; chosen interactions retain their functional and accessibility contracts.

### Evidence and precedents

- **Verified internal donor — theme and route continuity:** `Kappa-Bot/MelodIQ-Core` commit `4777ee0bbfc46a5c3df32ad2b21f9823799316ef`. Study `apps/platform/app/components/ui1/theme-locale-controls.tsx`, `workspace-shell.tsx`, `apps/platform/app/orbit.css` and `test/ui1/shells.spec.ts`. The curtain switch, header placement and route-stage behavior were observed in the authenticated production shell on 2026-10-30.
- **Internal donor — compact hover/focus rail:** `Kappa-Bot/MelodIQ-Core` commit `6283c8387a1c74f53fb741e61a305397e2302a7a`. Study `apps/platform/app/components/ui1/primary-navigation.tsx`, `apps/platform/app/orbit.css` and `test/ui1/shells.spec.ts`. In that design, the rail starts compact, reveals on hover or keyboard focus and offers a distinct pin/unpin preference. Its earlier expanded initial state contradicted that local contract; pointer focus retained after unpin also made the interaction appear inert. These are state-contract lessons, **not a ban on deliberately expanded navigation in another direction**. Automated full-suite and mobile/200%-zoom acceptance remain separate gates.
- **Curtain interaction:** `src-21st-curtain-theme-toggle` is a visual/behavioral reference (icon toggle and approximately 600 ms reveal), not an automatically approved runtime dependency or licensed source-code transplant.
- **Expandable sidebar:** `src-21st-manual-sidebar` links to the original `src-aceternity-sidebar` implementation: hover expansion on desktop, responsive mobile composition and dark support. Its stock demo links, logo, user, spacing and color choices are **not** MelodIQ product requirements.
- **Browser API:** `src-mdn-start-view-transition` describes same-document view transitions and compatibility; feature-detect and provide a no-animation fallback.

## 1. Theme control: header-owned, persistent and honest

1. When the product supports user-selectable themes, place the control in a stable, discoverable location appropriate to the chosen shell. The donor's rightmost-header sun/moon button is one option, not a required composition. Do not duplicate inconsistent controls on every page. An authentication shell may expose the same preference through its own navigation.
2. Give the control a native `button`, meaningful accessible name for the **next action**, visible focus and a truthful selected/pressed state. The language selector (if supported) is a separate native control. Keep usable pointer/touch targets and never rely on a decorative icon alone.
3. The product's current, authoritative preference must set the **initial server-rendered theme** (cookie or authenticated server preference where appropriate) and the semantic document color scheme. An optimistic client update can improve perceived speed, but must reconcile with the persisted value and visibly recover if saving fails. Do not silently claim persistence when it does not exist.
4. Map semantic roles across light/dark (canvas, elevated surface, text, muted text, border, focus, selected, success, warning, danger); resolve tenant branding within the existing safe token contract. Do not invert the page using global CSS filters or introduce pure-black body copy/illegible status colors.
5. For a curtain reveal, apply [Interaction Continuity § Theme changes](interaction-continuity.md#theme-changes). Verify the live controls during capture and animation. The earlier console donor's ~600 ms reveal of the captured new root is visual precedent. Reuse it only where the target has demonstrated hit testing, interruption, and focus continuity.
6. Use the same immediate, readable theme update on reduced-motion, unsupported and failed capture paths. Keep the console's authoritative preference and recovery contract in all paths.
7. If the product supports a system preference, define its precedence and switching rules explicitly. Do **not** present a system option or sync behavior that the app has not implemented.

Keep sensitive content within the authorized rendering boundary during capture. The console donor also illustrates SSR preference propagation and persistence recovery.

## 2. Sidebar, when selected: deliberate and keyboard-safe

Choose persistent expanded navigation, a compact expandable rail or another clear navigation composition according to task frequency, label ambiguity, density and viewport. Do not force icon-only navigation to resemble the donor. The following mechanics apply **when an expandable rail is selected**.

### Desktop / pointer-fine

- Give a compact rail legible iconography and a current-destination indicator; its expanded state reveals useful labels and groups. The donor's 72–80 px compact width, 216–240 px expanded width and 220–320 ms treatment are historical examples, not acceptance thresholds. Derive dimensions and optional motion from the current design. Do not hide essential navigation behind ambiguous icons.
- Prefer a slight **hover-intent delay** and exit grace where necessary to prevent jitter as the pointer crosses the rail boundary. Hover-only expansion is an enhancement; a keyboard user must be able to reveal the same labels with focus and use every destination. Keep expanded while its descendants have focus.
- The first desktop render must match the **chosen initial-state contract** and explicit saved preference without hydration jank. If the direction chooses compact-first behavior, hover/focus reveal must work without requiring a prior collapse click. If it chooses expanded navigation, expanded first paint is correct. Treat **pin/unpin** as distinct from transient hover; do not reinterpret an obsolete default as a user's pin decision.
- Provide an accessible **pin/unpin control** when a dense/frequent operator workflow benefits from a permanently open sidebar. Name the **next action** ("Pin navigation" / "Unpin navigation"), expose `aria-pressed` for whether it is pinned, and make click feedback truthful. Pointer-activated buttons must not leave `:focus-within` latched after unpin and pointer exit; keyboard-activated buttons **must retain keyboard focus** and keep expanded labels visible while focus is inside.
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
- Keep real route changes immediately intelligible and usable. A static update or a modest entry can satisfy this; the Core donor's ~360 ms fade and 10 px settling is not required. Never animate a blank full page, block an available action, or re-run entry motion on every text/data refresh.
- Preserve or deliberately reconcile filters, selections, return path and focus after navigation. Loading skeletons reflect actual pending work; avoid fake delays, duplicate page headings and empty space that pushes routine work below the fold.
- Reduced-motion, browser history, slow data, authorization failures, hard refresh and theme changes must keep truthful content and operable controls. Do not let transitions capture stale or unauthorized tenant information.

## 4. Adoption workflow for any console

1. **Establish scope and direction:** read `AGENTS.md`, `DESIGN.md`, the current brief, theme/navigation model and privacy constraints. Apply `std-ui-ux-quality-baseline` §1; supersede inadequate aesthetics within delegated redesign authority, while recording explicit current theme restrictions and independent release freezes. An external demo alone grants no authority.
2. **Inventory the real shell:** header controls, sidebar states, login/auth shell, route boundaries, desktop/mobile/zoom, source of preferences, loading/error paths and existing accessibility.
3. **Choose integration:** retain useful primitives without preserving an inadequate composition. Use the donor only for selected mechanics. Decide navigation form and initial state, persistence, any collapsed/expanded widths, SSR preference channel, supported themes and breakpoints. Keep one canonical implementation per app.
4. **Implement the selected design:** cover theme semantics/persistence if themes are supported, the chosen navigation on desktop/keyboard/mobile, and route continuity. A curtain or rail is optional. Do not migrate protected domain screens, public sites or unrelated CSS as collateral work.
5. **Verify with real rendering:** record desktop, 320 px and 200% zoom; contrast, hard refresh, keyboard/focus, mobile navigation, route/history continuity and authorization. Exercise light/dark, hover/exit, drawer/Escape, curtain interruption and preference-save failure where those mechanics exist. Check reduced motion, console errors and unwanted layout shift; mark irrelevant mechanics inapplicable rather than adding them to satisfy the matrix.
6. **Ship and report evidence by layer:** local tests/build, deployed exact SHA, live authenticated smoke and visual review are distinct. Report `NOT RUN`/`BLOCKED` explicitly; a Handbook Pattern does not mean DentalOS/ChurchOS has implemented or accepted it.

### Acceptance matrix (adapt to the product)

| Scenario | Minimum observed result |
|---|---|
| First render and reload (light/dark) | Correct persisted theme, no wrong-theme flash, header control reflects state |
| Toggle with optional curtain selected | Curtain moves smoothly; next-theme content and controls remain usable |
| Toggle with reduced motion/API missing | Immediate safe switch; no invisible/competing layers |
| Preference-save rejection | Truthful error and visual rollback/reconciliation |
| First desktop visit without explicit pin | Chosen initial navigation state already visible; if compact-first is selected, hover/focus reveal works without a prior click |
| Desktop rail: pointer enter/leave | Smooth expansion/retraction, no flicker or unintended content reflow |
| Keyboard tab/focus inside rail | Labels reachable, focus remains visible, no hover dependence |
| Pinned rail or active route | Stable state, correct `aria-current`, no stale user/tenant scope |
| Mobile, 320 px, zoom 200% | Named open/close, Escape and focus return, no blocked controls or horizontal overflow |
| Route change/back/forward/loading | Context persists or resets intentionally; no blank flicker; focus meaningful |
| Role/tenant and error scenarios | No permission leakage, misleading states or raw backend diagnostics |

## 5. Historical portfolio observations

These dated records do not establish today's consumer state or prescribe its next design. Re-read the current product brief before implementation; this Handbook update deploys nothing.

- **MelodIQ Core (2026-10-30):** curtain header toggle, preference persistence, route-stage motion and footer removal were in place. Sidebar regression corrected in `6283c838`: compact first render, temporary hover/focus reveal, explicit pin/unpin and no stuck pointer focus. The mobile dialog was retained. Authenticated production smoke on 2026-10-30 confirmed the resting 78 px rail, hover/focus expansion to 252 px, no content-column movement, and shrinking on pointer exit after unpin. That audit did not establish automated full-suite or mobile/zoom acceptance because its CI runner was blocked; this is not a statement about today's runner or release state.
- **DentalOS:** the MD-1 contract inspected for the original Pattern specified light-only operation and limited motion. Verify its current status; an authorized redesign may supersede aesthetics, but do not silently override an explicit current light-only constraint or clinical/privacy/release gate. Public Uribe Villa and patient surfaces are not implicitly in scope.
- **Church OS / Ops OS / future Verticals:** evaluate these mechanics only when they serve the next authorized direction. Preserve roles, authentic tenant identity, accessibility, performance and active release gates; do not inherit Core's layout by default. No cross-repo deployment is asserted here.

## Sources and reuse

Material external precedents are registered in `machine-readable/sources.yaml`. The 21st.dev and Aceternity examples are design evidence; do not paste their demo implementation or add dependencies merely because they appear there. Where an external implementation is copied or materially adapted, verify the exact source/package license and comply with attribution/notice obligations. See `gov-source-authority`, `gov-knowledge-promotion` and `pat-design-context-layering`.

## Agent-context routing

The deterministic context router must surface this pattern for new operator-console shells and targeted sidebar, theme or route-continuity changes. The canonical prose above controls the implementation; these small units make it discoverable without requiring an agent to remember the page name.

```json agent-context
{
  "units": [
    {
      "id": "operator-console-shell-scope-and-donor",
      "type": "decision-question",
      "text": "For an operator shell change, apply std-ui-ux-quality-baseline section 1 to the current brief, tasks and DESIGN.md. Within authorized redesign, replace inadequate composition; preserve current explicit constraints, release freezes, roles and tenant boundaries. Select useful theme/navigation/continuity mechanics; Core and 21st.dev donors do not mandate a compact rail, curtain or header placement.",
      "source": "pat-operator-console-shell-interactions",
      "covers": [
        "accessibility",
        "console-shell-fidelity",
        "compatibility"
      ],
      "activate_when": [
        "archetype:operator-console-shell-change"
      ],
      "phase": [
        "planning"
      ],
      "priority": 79
    },
    {
      "id": "operator-console-shell-integrated-interactions",
      "type": "pattern",
      "text": "Implement the chosen shell, not a prescribed rail or curtain. Where themes exist, use semantic tokens, authoritative first paint and persistence recovery. For optional curtains apply pat-interaction-continuity. If navigation expands, separate hover/focus from pinning and avoid table reflow. Provide keyboard-safe mobile navigation with focus recovery. Preserve meaningful route and tenant context, functional invariants and authorization boundaries.",
      "source": "pat-operator-console-shell-interactions",
      "covers": [
        "accessibility",
        "compatibility",
        "console-shell-fidelity",
        "performance"
      ],
      "activate_when": [
        "archetype:operator-console-shell-change"
      ],
      "phase": [
        "implementation"
      ],
      "priority": 84
    },
    {
      "id": "operator-console-shell-live-acceptance",
      "type": "verification",
      "text": "Verify the chosen initial navigation state, keyboard/current destination, authorized routes, mobile 320px and 200% zoom. Exercise hover/focus/pin only when selected, and theme first paint, persistence failure and curtain interruption only where supported. Check route/history continuity against the current direction. Record exact-build authenticated smoke where available and label unrun or inapplicable gates.",
      "source": "pat-operator-console-shell-interactions",
      "covers": [
        "accessibility",
        "compatibility",
        "console-shell-fidelity",
        "performance"
      ],
      "activate_when": [
        "archetype:operator-console-shell-change"
      ],
      "phase": [
        "verification"
      ],
      "priority": 89
    }
  ]
}
```
