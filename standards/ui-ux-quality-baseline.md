---
id: std-ui-ux-quality-baseline
kind: standard
status: active
owner: engineering
version: "0.13"
applies_to:
  - user-facing-web-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-wcag-accessible-authentication-minimum
  - src-w3c-html-language-declarations
  - src-whatwg-html-form-submission
  - src-whatwg-html-number-input
  - src-whatwg-html-language-inheritance
  - src-w3c-css-language-pseudo-class
  - src-w3c-css-forced-colors
  - src-w3c-aria-apg
  - src-w3c-html-aria-disabled-controls
  - src-unslop
  - src-modern-web-guidance
last_verified: 2026-11-21
review_due: 2027-02-19
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

### Modern platform and browser contract

Before materially adding/replacing HTML, CSS or browser-side behavior, agents MUST assess the applicable current platform guidance through [Modern Web Platform Workflow](../playbooks/modern-web-platform-workflow.md). This applies to forms, overlays, tables, responsive layout, input, rendering and browser defense/interaction changes, including internal CRMs; it does not mandate a new API, a repository-wide scan, an external executable or redesign for a copy fix.

The choice MUST fit the product's actual browser/device/assistive-technology contract, essential-versus-enhancement distinction, framework DOM ownership, SSR/hydration and security constraints. Baseline status and a guide's support date are evidence, not a substitute for that contract. Preserve a usable tested fallback for essential behavior where support is insufficient; unsupported optional effects may degrade without hiding content or actions. No automatic experimental opt-in, blanket type escape, unpinned CDN polyfill or change to the browser floor is permitted by source adoption.

Native elements still require verified semantics, focus, keyboard, announcements and failure states. Client-side simplification MUST NOT replace server validation, authorization, tenant isolation or data integrity. Keep performance and legal/privacy claims with their existing canonical owners. Verify the affected behavior, compatibility/fallback and representative rendered states; missing required evidence remains incomplete.

The [attributed assessment](../references/modern-web-ponytail-adoption-assessment.md) records source versions and deliberate adaptations. `pol-reuse-first` controls minimum-complete implementation; the design reconstruction contract below still controls authorized material redesign.

## 1. Product-specific design and reconstruction

The implementation MUST derive its visual/interaction direction from the real product, users, task, verified business facts and current brief. Existing designs and local contracts are evidence to assess, not a presumption that yesterday's composition is the right answer. Material visual creation, redesign and anti-slop work MUST apply the diagnosis, direction and nine-pass method in [Frontend Quality Review](../playbooks/frontend-quality-review.md#3-diagnose-and-set-the-direction), with explicit dispositions for inapplicable passes.

The owner-authorized [Unslop decision](../decisions/0009-unslop-design-reconstruction.md) establishes **reconstruction over cosmetic preservation when the design problem is systemic**. Within an authorized redesign, agents MUST replace inadequate hierarchy, section order, navigation composition, palette, typography, spacing, material, component grammar, imagery or motion instead of preserving them solely because they already exist or were once approved. Supersede the affected local design decisions coherently; do not keep two active visual contracts. There is no universal preference for a photographic hero, muted typography, a card grid or the previous brand treatment. **One limited default is defined by the [visual-direction catalog](../patterns/visual-direction-catalog.md): Glassmorphism is a starting candidate for new or already-authorized material redesigns of internal operator/admin consoles without an explicit current product direction.** Other surfaces inherit no material default; local design and successful quality evidence outrank that candidate.

This changes design authority, not action permissions. A design audit remains read-only; a bounded fix remains bounded; a redesign is not permission to change business capabilities, legal identity, authorization, data, publication state or third-party brand rights. Explicit current constraints and independently scoped release freezes still apply. Do not seek repeated aesthetic confirmation when the owner already delegated the direction; ask only for a missing decision that materially changes scope, rights, facts or external effects.

The following are acceptance requirements, not optional styling advice:

- State a concrete audience/task, visual character, product world, meaningful focal content and recognizable product detail before material implementation. "Modern", "clean" or "premium" alone is not a direction.
- Reject interchangeable generated-template composition and unsupported promotional copy. A restrained utility can be excellent, but its hierarchy, terms, data and actions MUST express its actual work; austerity is not an exemption from design fit.
- Remove or replace repeated containers, badges, effects, generic images and motion that cannot justify their contribution to comprehension, task completion or product recognition. A technically usable but indiscriminate skin is not finished design.
- Evaluate an expressive treatment on its result, not a blanket ban on gradients, bold type, color or animation. Do not replace one generic style with a universal neutral Unslop skin.
- Preserve functional/domain invariants and truthful states while changing their presentation. Fixture data MUST remain distinguishable from real claims, testimonials, metrics or completed work.

For a material anti-slop request, merely changing colors, radii or shadows MUST NOT count as completion while the diagnosed composition/content problem remains. The operational procedure and scoped defect record live in the Playbook, not a second Standard.

This Standard MUST NOT be interpreted as requiring:

- Material, shadcn, Radix, Bootstrap or another component system;
- cards as the default container;
- a sidebar/topbar dashboard composition;
- a particular border radius, shadow, palette, grid or typography system;
- Tailwind, CSS Modules or another styling mechanism;
- a particular animation library;
- visual sameness across unrelated products.

Framework defaults or a generic generated-SaaS composition are not, by themselves, a finished design decision. A good existing solution may survive the review on evidence; novelty and churn are not acceptance criteria.

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

### Task hierarchy for data and graphics

Choose the representation from the user question, not from a component catalog.

- use a graphic when spatial comparison, trend, range, distribution, or relationship is the decision task;
- use a table when exact lookup, audit, dense comparison, export, or row-level action is the decision task;
- when both are necessary, the graphic SHOULD answer the overview question and exact values MUST remain reachable without relying on a tooltip;
- a chart MUST name its question, measure/unit, scope/period, and any material unknown, partial, excluded, or confirmed-zero state;
- a decorative chart, a duplicate default table, or a generic KPI-card wall is not evidence of decision support.

This rule is semantic rather than stylistic: it does not prescribe a chart library, visual language, or product art direction.

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

When a button uses `aria-disabled` to remain discoverable while unavailable,
verify its intended keyboard focus behavior. The ARIA state communicates that
the action is unavailable to assistive technology. The application also
needs to make the action inactive. Exercise keyboard and pointer activation
as supported and check that the button's action has no effect while disabled.
Verify that activation works again when the flow enables the button. See
`src-w3c-html-aria-disabled-controls` §4.2 and the focusability guidance
in `src-w3c-aria-apg`.

### Filters, collections and retained selection

A visible filter/control MUST correspond to a real predicate over the visible collection. Labels such as state, status, cohort, date range, or initial MUST not merely seek, sort, or cosmetically highlight matching rows while retaining out-of-predicate content.

Pagination, cursors, counts, empty states, and exact-data export for a filtered collection MUST use the same predicate. When a changed predicate excludes a retained selection, the UI MUST clear or explicitly reconcile that selection before presenting the new collection. A user must not appear to be acting on an item that is no longer in scope.

Errors MUST be associated with the affected control/content and SHOULD explain a useful recovery action. Important asynchronous feedback SHOULD be exposed accessibly, for example through appropriate live-region behavior when semantic HTML alone is insufficient.

### Human-safe error presentation

User-facing product surfaces MUST NOT render raw transport, backend, provider or internal diagnostic text as ordinary product copy.

This includes, unless a repo-local product requirement deliberately defines a safe exception:

- raw JSON or serialized exception bodies;
- stack traces or exception class names;
- machine-oriented `snake_case`/internal error codes;
- database, table, RPC, queue, framework or provider implementation names;
- capabilities, policy internals or authorization implementation terminology;
- UUIDs/record identifiers that have no user-facing meaning;
- HTTP/network terminology that does not help the user recover.

The user-facing layer SHOULD map internal failures to a stable product message that explains what happened at the level the user needs and gives a useful recovery action when one exists. A deliberately safe support/request reference MAY be shown when it materially helps support without exposing privileged internals.

Detailed diagnostic context belongs in appropriate internal observability: server-side logs, traces, structured error telemetry or engineering tools, subject to privacy/security rules. The UI should retain enough correlation to diagnose the event without copying the diagnostic payload into the product surface.

Human-safe presentation MUST NOT turn a security, authorization, integrity or persistence failure into a successful-looking fallback. The underlying operation still fails safely and truthfully.

For operator/admin surfaces where users can encounter backend mutations directly, representative failure-path tests SHOULD assert both the intended recovery copy and the absence of raw technical diagnostics.

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

An accessibility **audit** must report actual user-operable behavior and relevant unrun manual/assistive-technology checks; a linter, static axe-like scan or a WCAG badge does not establish full compliance. Fixing a keyboard/focus defect does not by itself authorize a whole visual reconstruction.

### Language of the page and passages

For a language semantics review, apply WCAG 2.2 3.1.1 to the page default and 3.1.2 to the human language of its passages and phrases. On rendered HTML, compare the language of the actual text with the `lang` on the `html` and the programmatically identified language of affected passages and phrases. Check the root again after an in-page locale switch. Use valid BCP 47 tags on the root and on elements that declare genuine passage-level changes. The 3.1.2 exceptions cover proper names, technical terms, words whose language cannot be determined, and borrowings in ordinary use in the surrounding language. Treat translated copy and `hreflang` as separate checks. Record the markup check separately from any representative browser and assistive-technology behavior required by the acceptance scope. Report unrun checks and observed limitations. Inspect the rendered markup even when speech sounds correct.

For a rendered passage, trace `lang` on the element and its ancestors. A
missing attribute can inherit the parent language. An explicit `lang=""` sets
the language to unknown for that element and descendants that inherit it. A
concrete `:lang(es)` check on a target in the browser can confirm language
matching, including an inherited `es-MX`. Direct `[lang]` and `.lang` readings
show only a local declaration. Check the tag and visible text separately
from selector matching and assistive-technology behavior. See
`src-whatwg-html-language-inheritance` and `src-w3c-css-language-pseudo-class`.

### Accessible authentication

WCAG 2.2 SC 3.3.8 (Level AA) applies to each step used to authenticate an existing user. If a step requires remembering, transcribing or solving something, document how it meets the criterion. The step can offer another authentication method that avoids cognitive tests or a mechanism that helps the user complete the test. The criterion also allows a test that consists of recognizing objects or identifying non-text content the user previously supplied to the site.

For example, where a password manager or copy and paste supplies the assistance, check the affected fields with a representative manager or paste a complete one-time code in an authorized test flow. Record the step, the mechanism or alternative observed, and any untested steps. One working field supplies evidence for that step. Preserve identity verification and existing security controls.

### Forced colors and state visibility

When reviewing affected web controls in forced colors, check rendered keyboard focus and the applicable selected or checked states with the user's palette. Under `forced-colors: active` and default `forced-color-adjust: auto`, CSS system colors can replace author colors and box/text shadows are suppressed. Verify that meaningful state cues remain visible through suitable system-color borders, outlines, check marks or other non-color-only indicators. Record any narrow `forced-color-adjust` opt-out and its benefit to the user's color and contrast needs. Apply WCAG 2.2 SC 1.4.11 to relevant author-controlled non-text cues against adjacent colors, including its exceptions for inactive controls and unmodified user-agent appearance. Record build, control states and browser with the native OS contrast theme or emulation used. Keep those observations distinct, and mark unrun native, emulated or separate assistive-technology checks `NOT RUN`.

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

When an existing HTML form submits from script, compare that path with activating
the intended submit button. With native validation enabled, try a missing required
value and valid input. Check whether the form fires a `submit` event and which
control appears in `event.submitter`. If a named button selects the action, check
its name and value at the receiver. `requestSubmit(button)` uses that button as
the submitter. Direct `form.submit()` skips interactive validation and the
`submit` event and supplies no submit button. Verify server-side validation,
authorization and any claimed durable result separately. See
`src-whatwg-html-form-submission` §§4.10.3 and 4.10.22.3–4.

When an existing number input distinguishes an omitted quantity from zero,
inspect the named field in `FormData` before conversion. An absent field has
no entry. An enabled, named number input left empty contributes an empty
string. A control value spelled `0` contributes `"0"`. Other valid spellings
of zero can remain distinct strings, such as `"0.00"`. The control's
`valueAsNumber` is `NaN` for an empty value and numeric zero for each of
these spellings.
Check whether native submission proceeds with optional and required inputs.
If fractions matter, try values against the field's actual step and step
base. Constructing `FormData` alone does not exercise constraint validation.
Verify the receiving application's interpretation separately. See
`src-whatwg-html-number-input` §§4.10.5.1.12, 4.10.5.3.8 and 4.10.5.4
and `src-whatwg-html-form-submission` §4.10.22.4.

When mobile virtual keyboards change the usable viewport, apply `pat-mobile-responsive-interaction`.

Completion is a state transition, not only a successful request. After a successful repeated task, restore a truthful next-action-ready state (for example, the next search/result/input) or make the completed state and safe next action explicit. On failure, preserve enough input/context for recovery.

See [Frontend Quality Review §6](../playbooks/frontend-quality-review.md#6-define-states-and-content-stress) for feedback and recovery when an operation changes a filtered collection.

## 7. Motion and direct manipulation

Motion MUST support orientation, causality, hierarchy or product character rather than compensate for weak composition.

- Required information/actions MUST remain understandable when reduced motion is requested.
- Motion MUST NOT create intervals where two competing text/state layers are simultaneously unreadable.
- Direct-manipulation gestures SHOULD feel responsive and MUST preserve a non-gesture alternative where accessibility requires it.
- Hover-only affordances MUST NOT be the sole way to discover or operate required functionality.

A highly expressive public experience MAY use substantially more motion/3D/editorial composition than an operational workspace. The quality criterion is deliberate fit, not minimal animation.

See [Interaction Continuity](../patterns/interaction-continuity.md) for transient layers, capture-based theme changes and mixed input that can affect focus, hit testing or available content.

## 8. Theme and visual semantics

If multiple themes are supported:

- semantic roles (surface, text, action, status, focus, border/elevation where relevant) SHOULD remain equivalent across themes;
- selection and focus MUST remain distinguishable;
- theme controls MUST have clear title/description/selected semantics;
- system/light/dark behavior MUST be tested as distinct states when the product claims them.

Do not hardcode a donor product's palette into another product merely because its theme model was reusable.

## 9. Visual verification

For materially visual changes, code review alone is insufficient.

Material visual acceptance MUST be based on the rendered product at the viewports/states that can materially change the decision. Verification MUST cover the applicable items below, or explicitly record a gate as not run with its consequence:

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

Do not declare visual acceptance complete while required rendered evidence is missing. A build, a design score, a marked checklist, a static reconstruction or a before/after presentation video is not that evidence. There is **no fixed render-count ceiling**: iterate until the diagnosed defects and risk-relevant states are resolved, or stop with an explicit blocker/incomplete result. More renders alone do not prove quality.

For material redesign, compare the same content and semantic states before/after and identify what the new hierarchy enables. Record intended baseline changes separately from unintended regressions. Verify critical journeys, accessible interaction and representative performance after the visual changes; a more attractive first viewport cannot compensate for a broken or slower core task.

## 10. Definition of done for UI work

A user-facing visual change is complete only when:

- the intended user decision/task is clearer or at least not degraded;
- for material design work, the product-specific direction is visible in the actual result, all nine passes have a disposition, and systemic slop was corrected at its cause rather than cosmetically covered;
- where visual decisions or baselines are deliberately replaced, their supersession is recorded in the owning product's existing contract; a bounded fix does not require inventing a new design contract;
- applicable states are implemented;
- representative user-facing failure states do not expose raw internal diagnostics as ordinary product copy;
- applicable WCAG 2.2 AA requirements are respected;
- responsive behavior is verified at risk-relevant widths;
- material visual output has been inspected; unavailable required evidence leaves visual acceptance incomplete rather than implicitly passed;
- no known high-severity client-visible defect remains in the tested scope;
- unrun browser/device/accessibility/visual gates are disclosed;
- filtered collections, retained selection, and repeated-task completion are verified as state transitions where they are in scope;
- repo-specific visual identity remains repo-specific rather than being replaced by handbook aesthetics.

## Adoption and attribution

Apply the reconstruction contract to new and materially redesigned surfaces through the normal Handbook refresh. Do not grandfather weak visual choices into future work, but do not mutate unrelated products or silently expand a small fix. Audit-only or scheduled reviews may record actionable, deduplicated findings when issue creation is authorized; they do not gain implementation authority from this Standard.

The design method materially adapts Unslop by Damir Sokolovsky (@heydamir), CC BY 4.0. [Source, attribution, changes and evidence limits](../references/unslop-adoption-assessment.md#attribution-and-reuse) identify the adapted portions; this does not relicense the entire Handbook.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "web-platform-compatibility",
      "type": "constraint",
      "text": "Use pb-modern-web-platform-workflow and its pinned guide locators before material browser changes. Fit actual browser/AT support, essential fallbacks, React/SSR ownership and typed boundaries; verify real behavior. No automatic CLI/hooks, experimental opt-ins, safety removal or API-for-novelty rewrite.",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["browser-compatibility"],
      "activate_when": ["archetype:web-platform-change"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 100
    },
    {
      "id": "ui-design-reconstruction",
      "type": "constraint",
      "text": "For read-only visual audits, use the Unslop quality rubric and report evidence without changing the product. For explicitly authorized redesigns, apply pb-frontend-quality-review, superseding weak composition/tokens but never truth, capabilities or access/release boundaries; update affected contracts only within the authorized scope.",
      "source": "std-ui-ux-quality-baseline",
      "covers": [],
      "activate_when": ["risk:design-fit"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 100
    },
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
      "id": "ui-accessibility-functional-verification",
      "type": "verification",
      "text": "For a focused accessibility audit, test actual keyboard, focus order/occlusion, semantic names, zoom/reflow, touch targets, reduced motion, form errors and relevant assistive-technology interaction in representative rendered states. A scanner-only pass is not WCAG 2.2 AA acceptance; report unavailable device/AT gates honestly.",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["accessibility"],
      "activate_when": ["archetype:accessibility-review"],
      "force": "must",
      "phase": ["verification"],
      "priority": 99
    },
    {
      "id": "ui-language-semantics-evidence",
      "type": "verification",
      "force": "should",
      "text": "For page, passage and phrase language, compare visible text with the rendered HTML root lang and programmatic language of non-exempt passages or phrases, including affected locale switches. Check valid language tags and applicable WCAG 3.1.2 exceptions. Translation and hreflang are separate evidence. Record representative browser and assistive-technology behavior when in scope, and mark unrun checks NOT RUN. Inspect the rendered markup even when speech sounds correct.",
      "source": "std-ui-ux-quality-baseline",
      "covers": [
        "language-semantics"
      ],
      "activate_when": [
        "archetype:accessibility-language-markup-review"
      ],
      "phase": [
        "planning",
        "verification"
      ],
      "priority": 94
    },
    {
      "id": "ui-accessible-authentication-evidence",
      "type": "verification",
      "force": "should",
      "text": "For each authentication step that requires a cognitive test, record the applicable SC 3.3.8 condition. The step may offer a method that avoids cognitive tests or assistance completing the test, or ask the user to recognize objects or identify non-text content they supplied to the site. Where relevant, verify password-manager autofill or whole-code paste in an authorized test flow. Record observed and untested steps and preserve identity and security controls.",
      "source": "std-ui-ux-quality-baseline",
      "covers": [
        "accessible-authentication"
      ],
      "activate_when": [
        "archetype:accessible-authentication-review"
      ],
      "phase": [
        "planning",
        "verification"
      ],
      "priority": 94
    },
    {
      "id": "ui-forced-colors-state-evidence",
      "type": "verification",
      "force": "should",
      "text": "Check rendered keyboard focus and applicable selected or checked states under forced colors. Preserve the user palette and verify system-color cues survive suppressed box/text shadows. Check applicable WCAG 2.2 SC 1.4.11 non-text contrast against adjacent colors, honoring inactive and unmodified user-agent exceptions. Record build/browser and state with native OS contrast-theme or emulated results identified separately. Record scoped palette opt-outs and mark unrun checks NOT RUN.",
      "source": "std-ui-ux-quality-baseline",
      "covers": [
        "forced-colors-visibility"
      ],
      "activate_when": [
        "archetype:accessibility-forced-colors-review"
      ],
      "phase": [
        "planning",
        "verification"
      ],
      "priority": 94
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
      "text": "Material visual acceptance needs rendered states/viewports matched to risk. Missing evidence is incomplete; disclose unrun gates.",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["accessibility"],
      "activate_when": ["surface:frontend", "archetype:ui-flow-change", "archetype:visual-regression-fix"],
      "force": "must",
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
    },
    {
      "id": "ui-filter-selection-truth",
      "type": "constraint",
      "text": "Visible collection filters must be real predicates across rows, pagination, counts, and exports; clear or reconcile retained selection when a new predicate excludes it.",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["data-integrity", "accessibility"],
      "activate_all": ["surface:frontend"],
      "activate_when": ["archetype:collection-filter-change"],
      "force": "must",
      "phase": ["implementation", "verification"],
      "priority": 88
    },
    {
      "id": "ui-semantic-representation",
      "type": "decision-question",
      "text": "Is the user task best served by a graphic for spatial comparison/trend/range/distribution or by a table for exact lookup/audit/action, and are any secondary exact values reachable without tooltip-only meaning?",
      "source": "std-ui-ux-quality-baseline",
      "covers": ["accessibility"],
      "activate_when": ["surface:frontend", "archetype:visual-regression-fix"],
      "phase": ["planning", "verification"],
      "priority": 72
    }
  ]
}
```
