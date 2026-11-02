---
id: pb-frontend-quality-review
kind: playbook
status: active
owner: engineering
version: "0.7"
applies_to:
  - user-facing-web-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
  - src-awesome-design-md
  - src-emil-ui-skills
last_verified: 2026-11-02
review_due: 2027-04-29
---

# Frontend Quality Review

## Purpose

Turn a functional frontend change into a product-quality result without forcing every product into the same visual system.

Use this Playbook for:

- new product/public screens;
- meaningful redesign/polish;
- responsive/mobile work;
- forms/wizards;
- interaction/motion changes;
- PWA/installable surfaces;
- visual acceptance/release work.

For trivial copy/layout changes, apply only the relevant portions.

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

- existing brand/visual decisions;
- current screenshots/rendered product;
- real business/user workflow;
- existing components/tokens;
- adjacent screens that establish product grammar;
- known UX defects/acceptance criteria.

Do not begin by choosing a library component or cloning a generic dashboard.

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

## 3. Establish three short theses

Before material implementation, be able to state:

### Visual thesis

What should this surface feel like and why is that appropriate to the product/brand?

### UX thesis

What should the user understand/do with the least unnecessary cognitive work?

### Interaction thesis

Which behaviors materially improve orientation, feedback or character?

These theses can be one sentence each. They are a thinking tool, not mandatory permanent documentation for every task.

If there is no defensible visual thesis for a visually important surface, framework defaults are likely driving the design.

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

Use only skills whose expertise can materially change this task:

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

Do not invoke the full set performatively. `pol-agent-operating-model` owns the cross-repository routing rule.

## 5. Design hierarchy before decoration

Resolve:

1. page/screen purpose;
2. primary action/decision;
3. information grouping;
4. navigation/context;
5. states and recovery;
6. responsive priority;
7. only then decorative/material details.

Challenge:

- redundant headings/labels;
- multiple competing conversion CTAs;
- card proliferation and cards nested inside cards;
- oversized containers with low information value;
- repeated chrome;
- excessive helper copy;
- decorative icon tiles/badges/pills used as default structure;
- decorative gradients, glass, blur, glow and shadow without product meaning;
- generic dashboard shells inherited from framework defaults;
- low-value KPI cards/charts where direct values or tables communicate better;
- arbitrary hard-coded colors/radii/spacing that fork established tokens;
- uniform `transition: all` or animation added to every interaction;
- decorative effects used to compensate for weak hierarchy.

A screen can be visually rich and still pass this review. The question is whether richness supports product identity/meaning rather than obscuring it.

### Public lead-generation journey (when that is the actual product goal)

Resolve the content jobs before styling individual sections:

- The first viewport should answer **who is offering what, for whom/where, why it matters, and what to do next**; use expressive brand language as a complement to a concrete proposition, not as its only substitute.
- Make a coherent path from the offer to the relevant service detail, authentic proof (if available), how the engagement works, meaningful price/budget context (if authorized), likely objections, and contact. These are *information needs*, not a mandatory quota of cards, pages, icons, badges or FAQs.
- Distinguish a fast direct-contact route (phone/WhatsApp) from a structured enquiry form when the latter is in scope. Validate that every CTA reaches a functioning, truthful destination and does not promise an unavailable capability.
- Use high-quality, rights-cleared imagery with intentional subject, lighting, text-safe areas and responsive crops. Generated/conceptual images must not masquerade as completed client work.
- In mobile layouts, ensure navigation, readable hero copy, contact actions and any sticky bar/floating widget do not overlap one another or obscure primary content/focus. An autoplay carousel, visual disclaimer or animation must not dominate the enquiry path.

### Photographic hero craft for client marketing websites

For MelodIQ-produced **public client/business landing pages** where the available, rights-cleared photography genuinely supports the offer, treat the **edge-to-edge, near/full-viewport photographic hero** as the preferred starting point rather than a small image inside an ordinary content block:

- Compose the image, foreground contrast, **real service proposition**, locality/fit when relevant, and primary conversion action as one first-viewport experience. A transparent header may overlay the photograph; if it remains sticky, it must gain a readable surface over following sections.
- Prefer a restrained, visible camera movement (for example, a small slow zoom), staggered headline/body/CTA entrances using eased opacity and short directional movement, and a deliberate fade-out/fade-in when scenes change. Text can enter from above and CTA groups from their nearer horizontal side, but they must remain understandable without waiting for motion.
- Avoid competing carousel controls, captions, menus, sticky bars and messaging widgets. Keep controls operable, preserve reading time, and **stop autoplay while the navigation is open**. Apply the visible pause/independent-timer contract from `pat-public-marketing-hero-motion` when scenes advance automatically. Motion must respect reduced-motion settings and avoid blank content or delayed interactions.
- Test first and later scroll checkpoints on mobile and desktop, including short viewports, crop/contrast in every visual scene, menu-open and scrolled-header states, 320px reflow and zoom. A screenshot during an entrance animation is a checkpoint, not proof of final legibility.
- Keep image provenance truthful. If there are no verified finished works, creative conceptual photos can express style but cannot be represented as the client's portfolio; disclose that clearly without letting disclosure overwhelm the selling message.

**Reusable hero execution:** consult `pat-public-marketing-hero-motion` when this task is a public marketing hero, full-screen photo/CTA composition, or rotating-word headline. Decide first whether the words add value. When a specific 21st.dev reference is supplied, inspect its **exact page and underlying original source** before translating the mechanic. The Tommy Jepsen `Animated Hero` swaps one complete word on a timer; it is **not** magnetic hover on individual letters. Keep a readable static H1, stable word slot, repo-local wording, separate word/scene clocks, visible pause for autoplay, responsive crops, reduced-motion behavior and a real primary CTA. Do not combine this automatically with all other animations on every website.

This is a **scope-specific default, not a universal layout or animation quota**. A content-first hero can be better when photography lacks rights, is irrelevant, slows the initial experience, compromises accessibility or conflicts with a deliberate repo-local brand decision. Record the reason for a different composition; do not force full-screen photos onto dashboards, operational screens, or content where they hinder the user. The observations and trade-offs are illustrated in `ref-public-service-commercial-benchmark-vizcaya-2026-10-29`.

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

### Collection truth and completion loops

When the surface filters a collection, inspect the actual predicate rather than trusting the control label:

- does every visible row satisfy the selected state/criterion/range?
- do counts, cursor/pagination, empty state, and exact-data output use that same predicate?
- does a changed predicate clear or explicitly reconcile a now-out-of-scope selection?

For repeated entry/capture work, inspect the complete loop: select → required continuation → submit → success/failure → next ready action. A success state that strands the operator, or a failure that discards recoverable context, is incomplete interaction design.

### Navigation continuity and perceived response

For route or major-view changes, verify that relevant context (such as the active record, filters, selection, scroll position and return path) is preserved or deliberately reset, and that keyboard focus lands somewhere meaningful. Do not restore stale or unauthorized context. Treat transitions as feedback for a real state change: they must not hide initial content, delay an available action, or outlast the task they explain. Loading placeholders should reflect actual pending work; reserve known space and avoid flashing an artificial loading state for work that has already completed. See `ref-internal-ui-pwa-donor-audit` for internal examples and limits.

### Semantic visual review

Before approving a graphic, state the question it answers. Verify that its unit, scope/period, comparison/reference, and unknown/partial/zero conditions are visible. Ask whether a table is instead the primary task surface for exact lookup, audit, dense comparison, or row action. If both are needed, keep the overview graphic and make exact values reachable through a keyboard-safe disclosure or equivalent non-tooltip path.

## 7. Apply the quality Standards/Patterns

Always apply the relevant sections of:

- `std-ui-ux-quality-baseline`.

Additionally:

- platform/Vertical/tenant/surface design resolution → `pat-design-context-layering`;
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

For materially visual work, run the product and inspect the actual result when tooling permits.

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

If a product is supposed to look premium, branded, editorial, physical, playful or otherwise distinctive, explicitly ask during review:

> Does this look like this product, or like a generic generated template?

If it is generic because the product has no reason to be distinctive, that may be acceptable. If distinctive quality is part of the intended outcome, treat generic composition as a real quality defect and iterate hierarchy/art direction—not merely shadows/gradients.

Also ask:

> Which visual decisions came from product intent, and which appeared merely because an AI/framework commonly generates them?

Remove the latter unless they survive an explicit product/usefulness rationale.

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

## 12. Handoff

Report:

- what user/product outcome improved;
- Standards/Patterns applied;
- functional/accessibility/visual checks actually run;
- representative viewports/states inspected;
- native-device checks actually run;
- unresolved visual/accessibility defects;
- gates not run.

Do not declare UI/PWA quality complete based solely on build/lint/unit success.
