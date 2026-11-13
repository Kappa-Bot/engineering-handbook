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

For an explicitly authorized translucent material treatment, consult `pat-operator-glass-surface-material` for the distinction between glass navigation, opaque data and elevated context. The shell behavior documented here does **not** require Glassmorphism or override existing product visual authority.

### Evidence and precedents

- **Verified internal donor — theme and route continuity:** `Kappa-Bot/MelodIQ-Core` commit `4777ee0bbfc46a5c3df32ad2b21f9823799316ef`. Study `apps/platform/app/components/ui1/theme-locale-controls.tsx`, `workspace-shell.tsx`, `apps/platform/app/orbit.css` and `test/ui1/shells.spec.ts`. The curtain switch, header placement and route-stage behavior were observed in the authenticated production shell on 2026-10-30.
- **Internal donor — compact hover/focus rail:** `Kappa-Bot/MelodIQ-Core` commit `6283c8387a1c74f53fb741e61a305397e2302a7a`. Study `apps/platform/app/components/ui1/primary-navigation.tsx`, `apps/platform/app/orbit.css` and `test/ui1/shells.spec.ts`. The rail now starts compact, reveals on hover or keyboard focus and offers a distinct pin/unpin preference. A previous donor opened expanded by default and retained pointer focus after an unpin click, making the interaction appear inert; **do not copy that legacy behavior**. Automated full-suite and mobile/200%-zoom acceptance remain separate gates.
- **Curtain interaction:** `src-21st-curtain-theme-toggle` is a visual/behavioral reference (icon toggle and approximately 600 ms reveal), not an automatically approved runtime dependency or licensed source-code transplant.
- **Expandable sidebar:** `src-21st-manual-sidebar` links to the original `src-aceternity-sidebar` implementation: hover expansion on desktop, responsive mobile composition and dark support. Its stock demo links, logo, user, spacing and color choices are **not** MelodIQ product requirements.
- **Browser API:** `src-mdn-start-view-transition` describes same-document view transitions and compatibility; feature-detect and provide a no-animation fallback.

## 1. Theme control: header-owned, persistent and honest

1. Place a compact sun/moon button at the **rightmost end of the persistent top bar**, adjacent to any language/account controls. Do not bury theme preferences in a footer or duplicate them on every page. An authentication shell may expose the same control in its own header.
2. Give the control a native `button`, meaningful accessible name for the **next action**, visible focus and a truthful selected/pressed state. The language selector (if supported) is a separate native control. Keep usable pointer/touch targets and never rely on a decorative icon alone.
3. The product's current, authoritative preference must set the **initial server-rendered theme** (cookie or authenticated server preference where appropriate) and the semantic document color scheme. An optimistic client update can improve perceived speed, but must reconcile with the persisted value and visibly recover if saving fails. Do not silently claim persistence when it does not exist.
4. Map semantic roles across light/dark (canvas, elevated surface, text, muted text, border, focus, selected, success, warning, danger); resolve tenant branding within the existing safe token contract. Do not invert the page using global CSS filters or introduce pure-black body copy/illegible status colors.
5. For a curtain reveal, apply [Interaction Continuity § Theme changes](interaction-continuity.md#theme-changes). Verify the live controls during capture and animation. The earlier console donor's ~600 ms reveal of the captured new root is visual precedent. Reuse it only where the target has demonstrated hit testing, interruption, and focus continuity.
6. Use the same immediate, readable theme update on reduced-motion, unsupported and failed capture paths. Keep the console's authoritative preference and recovery contract in all paths.
7. If the product supports a system preference, define its precedence and switching rules explicitly. Do **not** present a system option or sync behavior that the app has not implemented.

Keep sensitive content within the authorized rendering boundary during capture. The console donor also illustrates SSR preference propagation and persistence recovery.

## 2. Sidebar: expandable, deliberate, keyboard-safe

### Desktop / pointer-fine

- Start from a **recognizable compact navigation rail** (indicatively 72–80 px) with legible iconography and a current-destination indicator. On pointer hover, temporarily reveal labels and groups in an expanded surface (indicatively 216–240 px), with a **decelerated 220–320 ms** width/opacity treatment. Do not hide essential navigation behind icons with ambiguous meaning.
- Prefer a slight **hover-intent delay** and exit grace where necessary to prevent jitter as the pointer crosses the rail boundary. Hover-only expansion is an enhancement; a keyboard user must be able to reveal the same labels with focus and use every destination. Keep expanded while its descendants have focus.
- The **first desktop render must start compact** when no explicit pin preference exists. Initial expanded state is a functional regression, even if manually collapsing reveals hover later. Treat **pin/unpin** as distinct from pointer hover: hover is transient; pin reserves the expanded layout after pointer exit. If saved, restore the explicit pin without hydration jank; do not reuse an old "expanded by default" preference as a pin decision.
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
| First desktop visit without explicit pin | 72–80 px compact rail already visible, hover expands directly without needing a prior click |
| Desktop rail: pointer enter/leave | Smooth expansion/retraction, no flicker or unintended content reflow |
| Keyboard tab/focus inside rail | Labels reachable, focus remains visible, no hover dependence |
| Pinned rail or active route | Stable state, correct `aria-current`, no stale user/tenant scope |
| Mobile, 320 px, zoom 200% | Named open/close, Escape and focus return, no blocked controls or horizontal overflow |
| Route change/back/forward/loading | Context persists or resets intentionally; no blank flicker; focus meaningful |
| Role/tenant and error scenarios | No permission leakage, misleading states or raw backend diagnostics |

## 5. Portfolio adoption status

- **MelodIQ Core (2026-10-30):** curtain header toggle, preference persistence, route-stage motion and footer removal in place. Sidebar regression corrected in `6283c838`: compact first render, temporary hover/focus reveal, explicit pin/unpin and no stuck pointer focus. The mobile dialog is retained. Authenticated production smoke on 2026-10-30 confirmed the resting 78 px rail, hover/focus expansion to 252 px, no content-column movement, and shrinking on pointer exit after unpin. Automated full-suite and mobile/zoom acceptance have not been established by the current blocked CI runner.
- **DentalOS:** current MD-1 contract explicitly specifies light-only operation and limited motion. This Pattern records the owner's desired future console direction; a separate authorized design-contract amendment, token work and clinical/privacy/visual acceptance must precede a dark-mode or sidebar rollout. Public Uribe Villa and patient surfaces are not implicitly in scope.
- **Church OS / Ops OS / future Verticals:** use this Pattern as a candidate for the next authorized operational shell design, preserving their specific roles, tenant branding, accessibility, performance and active release gates. No cross-repo deployment is asserted here.

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
      "text": "For an authenticated operator console or a shell change, inspect the product's active DESIGN.md, release freeze, roles, tenant context and navigation map. Confirm this is an operator/admin surface, not a public, patient/member, kiosk or print surface. Study the verified MelodIQ Core theme/sidebar/route donors and the named 21st.dev references before adapting the behavior; do not imply approval to override product-specific contracts.",
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
      "text": "Use semantic light/dark tokens and render the authoritative saved theme from the server. Put the accessible switch at the far right of the persistent header. For a curtain, use pat-interaction-continuity and preserve immediate fallback and persistence recovery. Start the desktop rail at 72–80px unless pinned. Keep hover/focus reveal separate from pinning and avoid table reflow. Use a named mobile drawer with Escape and focus return. Preserve header, rail and tenant state on navigation. Follow local DESIGN.md and authorization boundaries.",
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
      "text": "Verify compact first desktop render, hover/focus expansion, pin/unpin and pointer-exit, keyboard and aria-current, authorized navigation, and mobile drawer at 320px and 200% zoom. Check theme first paint, persistence failure, input during any curtain, reduced-motion fallback and route/history continuity. Check shell structure against the approved design. Record exact-build authenticated smoke where available and label unrun gates.",
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
