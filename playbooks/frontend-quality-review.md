---
id: pb-frontend-quality-review
kind: playbook
status: active
owner: engineering
version: "0.2"
applies_to:
  - user-facing-web-surfaces
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
  - src-awesome-design-md
  - src-emil-ui-skills
last_verified: 2026-08-31
review_due: 2027-02-28
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

## 7. Apply the quality Standards/Patterns

Always apply the relevant sections of:

- `std-ui-ux-quality-baseline`.

Additionally:

- platform/Vertical/tenant/surface design resolution → `pat-design-context-layering`;
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
