---
id: pb-frontend-quality-review
kind: playbook
status: active
owner: engineering
version: "0.15"
applies_to:
  - user-facing-web-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
  - src-w3c-css-font-loading
  - src-chrome-devtools-rendered-fonts
  - src-whatwg-html-animation-frame-callbacks
  - src-w3c-event-timing-observer-threshold
  - src-wicg-layout-instability-input-exclusion
  - src-w3c-high-resolution-time
  - src-awesome-design-md
  - src-emil-ui-skills
  - src-ecc
  - src-unslop
  - src-modern-web-guidance
last_verified: 2026-11-22
review_due: 2027-02-22
---

# Frontend Quality Review

## Purpose

Turn a functional frontend change into a deliberately designed product. This is the Handbook's operational Unslop method, materially adapted and strengthened from `src-unslop`; [UI/UX Quality Baseline §1](../standards/ui-ux-quality-baseline.md#1-product-specific-design-and-reconstruction) makes diagnosis, direction, applicable passes and real visual acceptance mandatory for material design work. It is not a second skill or a shared visual skin.

Use this Playbook for:

- new product/public screens;
- meaningful redesign/polish;
- responsive/mobile work;
- forms/wizards;
- interaction/motion changes;
- PWA/installable surfaces;
- visual acceptance/release work.

For trivial copy/layout changes, apply only the relevant portions.

Identify the action boundary first: **audit**, **bounded fix**, or **authorized redesign**. An audit produces findings, not edits. A redesign can replace the visual system within its scope without asking again about every aesthetic choice; it does not authorize new business facts, external effects or release. Keep known-good behavior and data invariants, not arbitrary old visual decisions.

## 1. Classify the surface

Before designing, identify what kind of surface this is and therefore what quality should optimize for.

### Public / commercial / storytelling

Optimize for:

- brand recognition;
- trust;
- conversion hierarchy;
- editorial rhythm;
- memorable composition;
- meaningful media/motion.

Creative latitude: **high**.

### Editorial / reference / training

Optimize for finding a source, sustained reading, citation, returning to the right place and accurate print or copy output when needed. Start with the document and its status. Provide orientation in proportion to the document's complexity. Use [Editorial Reading and Navigation](../patterns/editorial-reading-navigation.md) for long documents, live contents and learning sequences.

### Operational / B2B workspace

Optimize for:

- information hierarchy;
- next-action clarity;
- density appropriate to repeated work;
- scanning/comparison;
- predictable state/action grammar;
- mobile/field operability if applicable.

Creative latitude: **medium**, but "operational" does not mean generic SaaS.

### Form / wizard / intake

Optimize for:

- low cognitive load;
- progress/orientation;
- validation/recovery;
- optional-vs-required clarity;
- interruption/resume semantics;
- mobile keyboard behavior.

Creative latitude: **medium** around a strong interaction contract.

### Kiosk / camera / field / touch-heavy

Optimize for:

- physical ergonomics;
- large/obvious targets;
- recovery and permission states;
- device orientation/environment;
- minimal dependence on precise pointer input.

Creative latitude: product-dependent; physical truth outranks desktop aesthetics.

### Internal utility

Optimize for task completion and maintainability. Do not spend visual complexity without user/product value, but still respect the applicable quality/accessibility floor.

## 2. Read product evidence before choosing composition

For meaningful visual work, inspect the smallest set of inputs that can materially affect the design:

- existing brand/visual decisions, separating current explicit constraints from replaceable historical choices;
- current screenshots/rendered product;
- real business/user workflow;
- existing components/tokens;
- adjacent screens that establish product grammar;
- known UX defects/acceptance criteria.

Do not begin by choosing a library component or cloning a generic dashboard.

Capture the rendered starting point and one representative journey in a safe environment before changing it. If there is no implementation, record that no baseline exists. A screenshot-only reconstruction or live-page snapshot is a prototype, not proof of functional equivalence or a change to the live site. Inspect content, states and interaction, not only the attractive first viewport.

For cross-repository quality-sensitive work, `pol-reuse-first` permits comparing mature internal donor implementations when they are likely to contain stronger validated practice.

When platform/Vertical/tenant boundaries or multiple surface types are involved, apply `pat-design-context-layering` before deciding which design rules are actually authoritative for the surface.

### Public commercial-site benchmark (where relevant)

For a public business website whose purpose includes qualified enquiries, do a **market-and-current-site comparison before settling the page design**. The reference is evidence of user expectations and content coverage, not a design system to copy:

1. Inspect the actual current/approved site or preview, plus one to three materially relevant live examples, at representative desktop and mobile widths. Check beyond the hero: services, service areas, process, prices/conditions where applicable, genuine work, reputation, FAQs, navigation, contact and footer. Record which pages are real, proposed, preview-only or intentionally excluded.
2. Write a small **commercial coverage and journey matrix**: visitor question/intent → current answer and route → reference observation → proposed answer/route → factual source/owner approval → disposition (`adopt`, `adapt`, `defer`, `not applicable`). A visually appealing landing with no convincing service or next-step path is not automatically ready to sell.
3. For the **first viewport**, compare message clarity, specific offering and real service geography, composition/crop and contrast, primary CTA, optional secondary exploration path, and credible proof. Test the full scroll journey too: attractive hero photography does not make up for missing answers below it.
4. Separate **design quality** from **truth and authorized scope**. Never import another site's photos, logo, reviews, claims, prices, metrics or location pages without confirmed rights and client-specific evidence. If a demo has an approved noindex/contact/backend restriction, mark the commercial gap as deferred or out of scope; do not silently enable production capabilities.
5. Keep what the existing implementation does better. Capture negative patterns in otherwise stronger references (obstructive sticky widgets, fragile reveal animations, inconsistent forms, thin location pages, distracting carousel chrome) as explicit **anti-patterns**, not prescriptions.

An observational example and reusable acceptance matrix are in `ref-public-service-commercial-benchmark-vizcaya-2026-10-29`. Its single-site findings are evidence, not organization-wide mandates.

## 3. Diagnose and set the direction

### Diagnosis and transformation depth

Use the [anti-slop review](../patterns/design-context-layering.md#anti-slop-review) on the actual screen. Record each actionable finding as **route/state + element → observed symptom → user/design cost → proposed correction → acceptance evidence**. Include generic but tidy composition, filler copy, absent product identity and broken states; do not equate slop with a purple palette.

Choose the depth from the failure, not from attachment to the current UI:

| Diagnosis | Execution |
| --- | --- |
| Systemic: template drives several sections, hierarchy or product identity | **Reconstruct.** Rebuild the composition and relevant visual system. Reorder/merge sections, replace layout, tokens, type, components, media and motion as required by the task. This is the default for material anti-slop work with systemic defects. |
| Local: coherent direction, isolated defects | **Refine.** Fix the cause and shared instances. No automatic palette/type/layout freeze: replace any of them if that is the coherent fix. |
| Strong: current evidence supports the design | **Retain.** Explain why it works and correct only real gaps. Do not manufacture novelty to demonstrate activity. |

For a bounded request that exposes a systemic problem, complete only the authorized fix and record the wider issue; do not pretend a micro-edit solved it. For audit-only work, report the recommended depth without implementing it.

### Product direction

Write five short, testable lines in the existing task/design record:

1. **Product and task:** audience, real offer/work and first useful decision.
2. **Character:** a few concrete traits tied to that audience; generic adjectives alone do not decide anything.
3. **World:** product-specific material, imagery, terminology or domain logic that will guide composition and color.
4. **Focal content:** the one or two places that deserve the most attention and what verified information they communicate. An operational screen can use an exceptionally clear schedule or work queue instead of ornamental media.
5. **Signature:** a recognizable detail or interaction derived from the work, used consistently rather than pasted on every section.

Add the critical journey, invariant/permission boundaries and acceptance criteria next to those lines. Reuse the existing local contract; this is not a demand for another template file. If the owner delegated direction, state the choice and implement. Stop only for unresolved material authority, rights, facts or a choice the owner reserved.

For systemic redesign, compare the old composition against a genuinely different structural alternative before committing to the treatment. A sketch or small prototype is enough to resolve the decision; do not require a gallery of cosmetic variants. Record what the new structure improves. Do not preserve section order just to make an animated before/after easier to produce.

## 4. Route design intelligence selectively

External design references are useful only when they answer a specific unresolved question.

Use this order:

1. current product evidence and repo-local design contract;
2. existing internal primitives and mature internal implementations;
3. `pat-design-context-layering` and `ref-external-design-intelligence-corpus`;
4. one to three focused external precedents when additional evidence can change the decision;
5. new design.

Do not load an entire design corpus into routine task context. Do not average named brands or use "make it like X" as the final design rationale. Extract the principle, then make a product-owned decision.

### Skill routing

The integrated Unslop procedure below is the default method for material design work, not an optional external inspiration. Use additional available skills only for a capability the task still needs:

- `ui-ux-pro-max`, `taste`, `impeccable`: material visual/UX composition and refinement;
- `emil-design-eng`: interaction craft and design-engineering review;
- `find-animation-opportunities`: decide where motion is worth adding;
- `animate` / `animate-expo`: implement motion for the applicable platform;
- `animation-vocabulary`: specify motion precisely;
- `apple-design`: when its interaction/physical-motion principles are relevant, not as an Apple skin;
- `improve-animations` / `review-animations`: audit implemented motion;
- `pick-ui-library`: only when a library choice is genuinely open;
- `prototype`: when materially different alternatives should be compared;
- `ask-sonner`: only for Sonner-specific work;
- `write-swift`: only for Swift work.

Do not invoke the full set performatively or install upstream Unslop beside the router merely to consume this method. `pol-agent-operating-model` owns cross-repository routing; source/tool evaluation is recorded in `ref-unslop-adoption-assessment`.

## 5. Design hierarchy before decoration

Resolve:

1. page/screen purpose;
2. primary action/decision;
3. information grouping;
4. navigation/context;
5. states and recovery;
6. responsive priority;
7. only then decorative/material details.

Use the [anti-slop review](../patterns/design-context-layering.md#anti-slop-review) to identify the user cost of a repeated or decorative treatment. Compare the actual render against a deliberate alternative using the same content. Ask what the page is for, where the first action leads, and what information or state becomes harder to see with the chosen treatment.

### Nine-pass reconstruction

Resolve structure in the direction first, then apply these passes across the affected surface in this order. Copy can change layout needs: revisit earlier passes when later evidence invalidates them. A coherent rewrite may implement several passes together; neither nine commits nor nine artificial renders are required. Give every pass a **changed**, **retained with evidence**, or **not applicable with reason** disposition in the existing review record.

| Pass | Required design work | Acceptance question |
| --- | --- | --- |
| **1. Spacing** | Establish a deliberate rhythm, grouping, alignment and task-appropriate density. Replace inconsistent values; size touch targets independently of decorative spacing. | Do groups, repeated rows and numbers align, including long content and narrow/short screens? |
| **2. Color** | Rebuild semantic surface, text, action, state and focus roles. Allocate emphasis to meaning, not every rectangle. Verify the actual composite in each supported theme. | Can users distinguish priority, selection, focus and status without relying on color alone? |
| **3. Icons** | Remove decorative duplication; use a coherent family, optical size and stroke appropriate to the interface. Keep labels and accessible names where meaning requires them. | Does each icon improve recognition or action rather than echo its heading? |
| **4. Copy** | Replace interchangeable headlines, hype, redundant labels and invented proof with the product's concrete task, offer, limits and next action. Use the current locale and truthful data. | Could the same copy sell an unrelated product after changing its name? If so, what is missing? |
| **5. Typography** | Choose hierarchy, reading face, emphasis, line length and numeric treatment from the direction. Replace a weak type system coherently; test locale, zoom and real wrapping. | Is the reading order clear and the text usable, not merely thin, fashionable or uniform? |
| **6. Layout** | Implement the structural alternative: section order, navigation, proportions, table/chart choice, progressive disclosure and mobile priority. Remove template card walls and dead bands. | Does the complete journey expose the right information/action sooner without losing necessary capability? |
| **7. Details** | Reconcile component geometry, boundaries, states, controls, charts and the signature. Remove orphan badges, inconsistent radii and decorative metrics. | Do repeated components follow the new contract and communicate real state? |
| **8. Visuals** | Use rights-cleared real material, a truthful product view, purposeful generated artwork or a finished typographic composition. Optimize crops, dimensions and delivery. | Does the visual explain this product, and is its provenance clear? |
| **9. Motion** | Remove purposeless loops and delayed content. Design feedback/orientation with explicit properties, interruptibility, stable targets and reduced-motion behavior. | Is the first frame useful, the transition legible and the next action immediately available? |

Do not import upstream numerical recipes or stylistic prohibitions as universal tokens. A gradient, strong weight, icon color, second chart or expressive transition can be correct when its job, accessibility and cost are demonstrated. The [visual-direction catalog](../patterns/visual-direction-catalog.md) makes Glassmorphism the **starting candidate only for new/authorized material design of internal consoles lacking a current product direction** and offers Neumorphism and solid/editorial alternatives. That candidate still needs this diagnosis; photographic heroes and particular shell layouts have no portfolio default.

Do not leave an empty media slot as a finished result when generation is unavailable. Choose a complete composition using available truthful assets, or identify the blocked deliverable and leave acceptance incomplete. Paid tools, external uploads and generated imagery follow the actual task's authority and cost boundary. A richer image cannot fabricate a feature, testimonial or completed client job.

### Public lead-generation journey (when that is the actual product goal)

Resolve the content jobs before styling individual sections:

- The first viewport should answer **who is offering what, for whom/where, why it matters, and what to do next**; use expressive brand language as a complement to a concrete proposition, not as its only substitute.
- Make a coherent path from the offer to the relevant service detail, authentic proof (if available), how the engagement works, meaningful price/budget context (if authorized), likely objections, and contact. These are *information needs*, not a mandatory quota of cards, pages, icons, badges or FAQs.
- Distinguish a fast direct-contact route (phone/WhatsApp) from a structured enquiry form when the latter is in scope. Validate that every CTA reaches a functioning, truthful destination and does not promise an unavailable capability.
- Use high-quality, rights-cleared imagery with intentional subject, lighting, text-safe areas and responsive crops. Generated/conceptual images must not masquerade as completed client work.
- In mobile layouts, ensure navigation, readable hero copy, contact actions and any sticky bar/floating widget do not overlap one another or obscure primary content/focus. An autoplay carousel, visual disclaimer or animation must not dominate the enquiry path.

### Photographic hero craft for client marketing websites

For MelodIQ-produced **public client/business landing pages**, choose between photographic, product-led, editorial/typographic or other justified first-viewport compositions from the direction. The previous portfolio preference for a near/full-viewport photograph is superseded: a full-height image must earn its space against a stronger alternative, not win by inheritance. When photography genuinely supports the offer:

- Compose the image, foreground contrast, **real service proposition**, locality/fit when relevant, and primary conversion action as one first-viewport experience. A transparent header may overlay the photograph; if it remains sticky, it must gain a readable surface over following sections.
- Use camera movement or scene transitions only when they improve the approved story and pass the motion/interaction checks. Static imagery is a complete choice; never hide the proposition or CTA to stage an entrance.
- Avoid competing carousel controls, captions, menus, sticky bars and messaging widgets. Keep controls operable, preserve reading time, and **stop autoplay while the navigation is open**. For timed scenes, use the current control contract, independent timers and WCAG acceptance in [the hero pattern §2.1](../patterns/public-marketing-hero-motion.md#21-scene-controls-autoplay-and-scoped-design-authority). Respect reduced motion and keep content and interaction available.
- Test first and later scroll checkpoints on mobile and desktop, including short viewports, crop/contrast in every visual scene, menu-open and scrolled-header states, 320px reflow and zoom. A screenshot during an entrance animation is a checkpoint, not proof of final legibility.
- Keep image provenance truthful. If there are no verified finished works, creative conceptual photos can express style but cannot be represented as the client's portfolio; disclose that clearly without letting disclosure overwhelm the selling message.

Consult `pat-public-marketing-hero-motion` for a public marketing hero, full-screen photo/CTA composition, or rotating-word headline. Decide first whether the words add value. When a specific 21st.dev reference is supplied, inspect its exact page and original source. The Tommy Jepsen `Animated Hero` swaps one complete word on a timer. Keep a readable static H1, stable word slot, repo-local wording, separate word and scene clocks, responsive crops, reduced-motion behavior and a real primary CTA. Apply the pattern's control and WCAG contract when autoplay is in scope.

There is **no preferred portfolio layout or animation quota**. Judge media-led and content-led alternatives on the same user, truth, accessibility and performance criteria. Do not force full-screen photos onto dashboards or preserve them on websites solely because a donor used them. Historical observations and trade-offs remain in `ref-public-service-commercial-benchmark-vizcaya-2026-10-29` as evidence, not a style mandate.

## 6. Define states and content stress

Before accepting the component/screen, exercise realistic variations:

- empty/loading/error/success;
- long names/addresses/labels;
- optional data absent;
- one item vs many;
- validation;
- permission denied/retry where applicable;
- theme variants;
- resume/draft state for interruptible workflows.

Prefer real/representative product copy and data over repeated lorem/placeholder shapes when visual density matters.

For content-sensitive components, check optical alignment of icons and labels, heading/paragraph wrapping, truncation at the actual density, and comparable number alignment (such as tabular figures for changing numeric columns). Reuse suitable tokens or deliberately replace the inadequate system and its affected consumers together; neither arbitrary values nor automatic preservation is a design method. Specify the properties that should transition rather than `transition: all`, and verify that motion does not obscure content or interfere with input/reduced-motion behavior.

### Collection truth and completion loops

When the surface filters a collection, inspect the actual predicate rather than trusting the control label:

- does every visible row satisfy the selected state/criterion/range?
- do counts, cursor/pagination, empty state, and exact-data output use that same predicate?
- does a changed predicate clear or explicitly reconcile a now-out-of-scope selection?

For repeated entry/capture work, inspect the complete loop: select → required continuation → submit → success/failure → next ready action. A success state that strands the operator, or a failure that discards recoverable context, is incomplete interaction design.

Trace **action → operation state → authoritative result → visible and accessible feedback → next action**. Start with any filter or draft already active. After confirmed creation, reconcile the collection deliberately. Offer a link to the new item or move to a compatible filter with the change explained. Preserve the predicate and show where to find the item when it legitimately belongs elsewhere. Announce success once and choose a stable, useful focus target. Use loading and retry cues for actual work. Distinguish a validated empty result, disabled action, pending request and failed read.

For rejection, retry, cancellation or conflict, check draft/selection retention and the actual persisted result. When a write may already have committed, reconcile its status before implying cancellation or allowing a blind duplicate retry. Keep reversible deactivation distinct from confirmed irreversible deletion where both exist. Use synthetic outcomes to test these branches and record the integration boundary separately.

### Navigation continuity and perceived response

For route or major-view changes, verify that relevant context (such as the active record, filters, selection, scroll position and return path) is preserved or deliberately reset, and that keyboard focus lands somewhere meaningful. Do not restore stale or unauthorized context. Treat transitions as feedback for a real state change: they must not hide initial content, delay an available action, or outlast the task they explain. Loading placeholders should reflect actual pending work; reserve known space and avoid flashing an artificial loading state for work that has already completed. See `ref-internal-ui-pwa-donor-audit` for internal examples and limits.

### Semantic visual review

Before approving a graphic, state the question it answers. Verify that its unit, scope/period, comparison/reference, and unknown/partial/zero conditions are visible. Ask whether a table is instead the primary task surface for exact lookup, audit, dense comparison, or row action. If both are needed, keep the overview graphic and make exact values reachable through a keyboard-safe disclosure or equivalent non-tooltip path.

## 7. Apply the quality Standards/Patterns

Always apply the relevant sections of:

- `std-ui-ux-quality-baseline`.

Additionally:

- material HTML/CSS/browser behavior, native components or compatibility/fallback choices → `pb-modern-web-platform-workflow`, as required by the UI Standard; coordinate with `pol-reuse-first` without weakening an authorized reconstruction;
- website/API/CRM/custom-product-agent boundaries → `ref-connected-product-resource-map` to locate the existing owners, not to infer a new architecture;
- platform/Vertical/tenant/surface design resolution → `pat-design-context-layering`;
- long-form reading, live contents and sequenced learning → `pat-editorial-reading-navigation`;
- transitions, disclosures, search selection or theme continuity → `pat-interaction-continuity`;
- authenticated MelodIQ console shell work (theme, navigation rail, route continuity) → `pat-operator-console-shell-interactions` when repo-local design authority permits it;
- complete public client/marketing website build → `pb-public-client-website-delivery`, orchestrating the hero, gallery, reviews, CTA and live release;
- public client/marketing photographic or animated hero work → `pat-public-marketing-hero-motion`, after local `DESIGN.md` and truth checks;
- interactive category/service gallery → `pat-public-service-gallery-selector`; demo or live testimonials → `pat-public-client-reviews-marquee`;
- public website SEO/search/brand previews → `std-public-web-discoverability-baseline` and `pb-public-web-discoverability-launch`;
- install/PWA work → `std-web-pwa-baseline`;
- mobile keyboard/overlay/gesture/camera work → `pat-mobile-responsive-interaction`;
- retained visual acceptance evidence → `pat-visual-evidence-integrity`.

Use APG patterns only when the interaction semantics actually match the pattern; prefer native semantic elements where they already solve the problem.

## 8. Render and inspect

For materially visual work, run the product and inspect the actual result. Under the UI Standard, missing required rendering capability leaves visual acceptance incomplete, not assumed. There is no three-render limit or substitute iteration quota; close the observed failure classes and required states.

When a journey promises a particular typeface, inspect the fonts that rendered
representative text in the intended element, state and language. Record any
glyphs supplied by fallback and compare them with the design's expected coverage.
`document.fonts.ready` can resolve and `document.fonts.check()` can return `true`
even when the named family is absent. A downloaded face can also go unused by
that element. In Chrome DevTools, inspect the element's Rendered Fonts and
compare with the same text using fallback. See `src-w3c-css-font-loading`
and `src-chrome-devtools-rendered-fonts`.

When an existing interaction uses `requestAnimationFrame` and its timing is under
review, record the callback's frame timestamp separately from its actual entry
and exit. Callbacks in the same document's frame can receive the same timestamp
even when an earlier callback delays a later one. Use `performance.now()` or
marks in the same document to measure the elapsed interval. Confirm the expected
state through the affected control or next user action. Use separate rendered
evidence for a claim about when that state was painted or became useful. See
`src-whatwg-html-animation-frame-callbacks` and `src-w3c-high-resolution-time`.

When a browser timing check uses Event Timing `event` entries, record the
observer's `durationThreshold` and which trusted interactions reached the
handler. Compare default collection with a supported lower threshold and
include a control that both observers report. A click can run and change
the expected state while appearing only in the lower-threshold stream.
Check the reported event duration separately from handler time and keep
the tested collection boundary with the result. See
`src-w3c-event-timing-observer-threshold` §§2.1 and 3.4.

When a frontend review uses `layout-shift` entries to assess movement,
start from a settled layout. Compare the observed element geometry with
each entry's `value` and `hadRecentInput`. Where relevant, exercise a
trusted action, a delayed update beyond the recent-input window, and a
settled no-input control. A positive shift can still carry the input
exclusion flag. Verify which entries the measurement uses and separately
observe what the user can see or operate. Record viewport changes when
they can affect the baseline. See `src-wicg-layout-instability-input-exclusion` §§2.4 and 3.

### Establish a safe QA boundary

Identify the environment, account/role and side effects before acting. Live exploration is read-only unless the task explicitly authorizes the mutation. Use isolated test accounts/data in an approved local or preview environment for submissions, deletes, billing, notifications or other consequential actions; preview alone does not guarantee that its integrations are harmless. Disable/stub external effects only in that authorized test scope. A request to audit a flow does not authorize sending real enquiries, WhatsApps, emails or charges, changing customer records, or bypassing approval.

Redact secrets and personal/customer data in retained screenshots, network captures and logs. If safe execution is unavailable, report the affected step as blocked rather than completing it against real users.

For meaningful flows, use a compact journey record: **route + initial state/role → user action → expected result/recovery → observed result + evidence**. Include the affected loading, validation, error/retry and completion transitions, not only static pages. Inspect console errors and failed network requests for those journeys; classify unrelated pre-existing noise with a reason instead of either ignoring everything or treating every warning as a new blocker.

### Select representative evidence

At minimum select evidence by risk:

- representative desktop;
- narrow/reflow floor and representative mobile;
- critical semantic states;
- applicable theme;
- focus/keyboard for interactive UI;
- motion checkpoints when animation can create overlap/clipping;
- long/realistic content.
- filter predicate/selection coherence and repeated-task completion where applicable;
- chart-question fit versus table-first work, plus exact-data reachability where graphics are used.

For public commercial sites, add a **side-by-side acceptance pass** against the recorded benchmark: same viewport and comparable scroll checkpoints (first viewport, service discovery, evidence/process, contact, footer); complete one representative enquiry journey from each major route and from a mobile sticky action if present. Compare what the visitor can learn and do, not just how photogenic the hero is. Document every material reference advantage as implemented, deliberately excluded, or deferred with a reason. Check that scroll reveals never hide already-available content and that fixed affordances remain non-obstructive.

Do not infer "looks good" from clean JSX/CSS.

For every material design task, explicitly ask during review:

> Does this look like this product, or like a generic generated template?

A quiet internal utility may use familiar controls, but its composition must still express the real task. Interchangeable content, indiscriminate cards and ornamental metrics do not become acceptable by calling the product a utility. Iterate hierarchy, content and art direction, not merely shadows or gradients.

Also ask:

> Which visual decisions came from product intent, and which appeared merely because an AI/framework commonly generates them?

Remove the latter unless they survive an explicit product/usefulness rationale.

For each original finding, record **resolved with evidence**, **retained with product reason**, **outside authorized scope**, or **unverified/blocked**. Do not hide an unresolved acceptance defect in a deferred list and call the redesign complete. Compare representative before/after states with the same data, and complete the critical journey after the final visual pass. Use `pat-performance-budgeting` when media, fonts, effects, data density or motion can change loading, interaction or scrolling cost; do not claim faster or higher-converting output without comparable observations.

When issue creation is authorized, reuse the existing issue for the same route/component and failure class. Include the exact build/state, reproduction, impact, acceptance condition and redacted evidence. An audit schedules nothing and publishes nothing by itself.

## 9. Accessibility and interaction review

Verify applicable:

- semantic controls/labels;
- keyboard reachability/order;
- visible/unobscured focus;
- pointer/touch target size;
- drag alternative;
- reflow/zoom;
- reduced-motion behavior;
- live status/errors;
- dialog/tab/combobox/grid keyboard behavior when those ARIA patterns are used.

Automated Axe-like checks are valuable but do not replace keyboard/use-flow inspection or semantic reasoning.

## 10. PWA/native review

If the surface is installable:

- verify only intended routes advertise/install;
- verify manifest identity/scope/launch;
- verify installed shell responsive behavior;
- verify service-worker/offline/update features only if actually present;
- separate browser-emulated evidence from real-device launcher/keyboard/camera checks.

Do not add service worker/offline/push as polish unless the product requirement justifies it.

## 11. Visual evidence quality

When acceptance depends on screenshots, use `pat-visual-evidence-integrity`.

A large screenshot directory is not evidence of coverage unless semantic states, provenance and scenario isolation are trustworthy.

Separate a new-design review from a regression comparison. A missing or incomparable baseline cannot establish "no regressions"; follow the Pattern's baseline and intentional-update contract. Fixed device lists, pixel tolerances or automated accessibility scores from an external recipe are not universal acceptance criteria.

## 12. Handoff

Report:

- what user/product outcome improved;
- diagnosis, five-line direction, transformation depth and nine-pass dispositions;
- visual decisions superseded, intentional baseline changes and the current local contract;
- Standards/Patterns applied;
- functional/accessibility/visual checks actually run;
- representative viewports/states inspected;
- native-device checks actually run;
- unresolved visual/accessibility defects;
- gates not run.

Do not declare UI/PWA quality complete based solely on build/lint/unit success.

For a material design comparison, keep a compact decision trail from the observed symptom through the hypothesis, change, representative evidence and decision. Include useful rejected variants, scope limits and the next unresolved risk. A repeat of the same test confirms that observation. Scores or iteration counts are optional summaries and do not establish coverage.

Optional before/after videos are presentation assets, not release evidence or a reason to retain the old DOM structure. Do not import the upstream snapshot/story scripts or their dependencies automatically. Use redacted or synthetic content, preserve applicable attribution, and keep presentation code out of the shipped application.

## Attribution

The direction framework and nine-pass workflow materially adapt **Unslop by Damir Sokolovsky (@heydamir)** under **CC BY 4.0**. This adaptation changes preservation rules, structural freedom, tokens, media selection and acceptance. [Pinned source, license and modification record](../references/unslop-adoption-assessment.md#attribution-and-reuse).

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "ux-journey-audit",
      "type": "decision-question",
      "text": "For a UI/UX quality review, inspect actual user journeys, hierarchy, navigation/focus continuity, pending/empty/error/success states, content stress, responsive and product-specific art direction. Follow the rendered Frontend Quality Review; an audit does not authorize Unslop reconstruction or a new material choice.",
      "source": "pb-frontend-quality-review",
      "covers": ["ux-quality"],
      "activate_when": ["archetype:ui-quality-review", "risk:ux-quality"],
      "force": "must",
      "phase": ["planning", "implementation"],
      "priority": 96
    },
    {
      "id": "ux-journey-evidence",
      "type": "verification",
      "text": "Audit the actual rendered journey across representative desktop/mobile, meaningful states, keyboard/focus, reduced motion and applicable themes. Include realistic content and observed failure recovery; code/screenshots alone are not proof. Record unrun browser/native evidence and no implied edit authority.",
      "source": "pb-frontend-quality-review",
      "covers": ["ux-quality"],
      "activate_when": ["archetype:ui-quality-review", "risk:ux-quality"],
      "force": "must",
      "phase": ["verification"],
      "priority": 96
    },
    {
      "id": "frontend-design-fit-review",
      "type": "verification",
      "text": "Verify direction, nine-pass dispositions, supersessions and real critical journeys; compare before/after when a baseline exists. Close slop/access/performance defects. Cosmetics/tests/video alone cannot pass.",
      "source": "pb-frontend-quality-review",
      "covers": ["design-fit"],
      "activate_when": ["risk:design-fit"],
      "phase": ["verification"],
      "requires": ["visual-evidence-bind-provenance"],
      "priority": 94
    },
    {
      "id": "frontend-operation-feedback",
      "type": "pattern",
      "text": "Identify who can act and what confirms the write. Trace pending state, authoritative result, accessible feedback and next action. Reconcile filters after confirmed creation. Preserve drafts on conflict and avoid duplicate announcements or retries of uncertain writes.",
      "source": "pb-frontend-quality-review",
      "covers": ["operation-feedback"],
      "activate_when": ["risk:operation-feedback"],
      "phase": ["planning", "implementation"],
      "priority": 94
    },
    {
      "id": "frontend-operation-feedback-verification",
      "type": "verification",
      "text": "Start with a filter or draft active. Exercise pending, confirmed creation, empty result, failure and conflict. Assert the real outcome, useful focus, one accessible confirmation, correct filter and preserved recovery. Scope synthetic evidence to the UI/contract tested.",
      "source": "pb-frontend-quality-review",
      "covers": ["operation-feedback"],
      "activate_when": ["risk:operation-feedback"],
      "phase": ["verification"],
      "priority": 94
    }
  ]
}
```
