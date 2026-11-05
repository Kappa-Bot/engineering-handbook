---
id: pat-public-service-gallery-selector
kind: pattern
status: active
owner: engineering
version: "0.2"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - product-vertical-public-pages
  - demos
sources:
  - src-21st-minhxthanh-interactive-selector
  - src-w3c-wcag-22
  - src-w3c-aria-apg
last_verified: 2026-11-05
review_due: 2027-02-05
---

# Public Service Gallery: Interactive Image Selector

## Scope and decision

Use this Pattern when a public service website has **three to five visually distinctive categories, spaces or real projects** worth exploring. The active photo expands while other choices remain visible. It is a reusable interaction option, **not a requirement to add a gallery, an animation or four fake projects to every website**. Flat grids are better for many equally important images; before/after comparisons need their own truthful consent and image semantics.

The reference is [Interactive Selector by @minhxthanh](https://21st.dev/@minhxthanh/components/interactive-selector). Its public page documents a premium-camping React/Tailwind selector; its component source requires an account and its reuse license was not verified. Rebuild the observed **interaction grammar**, never reproduce the camping wording/assets, assume its source is licensed or force a React dependency onto a static site. The first independently implemented reference is **Pinturas García**: `Kappa-Bot/pinturas-garcia` at commit `ea4f3ac408a5aa4ee52394bbaf0f8a0289691304` (gallery and responsive fix). It is an implementation example, not a global visual theme.

## 1. Content and image contract

1. Plan the categories and labels from the site's *actual* service offer (e.g. interiors, façades, commercial premises, details). Each photo must have a useful one-sentence explanation and a truthful image provenance. **Conceptual, licensed stock or AI-generated work must never be described as a completed client commission**; use "inspiración", "escena ilustrativa" or other accurate context where appropriate.
2. Source a distinct and intentional composition for **each desktop landscape image and its corresponding mobile portrait image**. A dedicated ~9:16 mobile rendition often preserves the subject more convincingly than an automatic center crop. Record the original, rights, intended focal point, sizes and optimization in a local media manifest.
3. Keep labels visible even when panels are inactive. Each compact panel needs enough legible text or a persistent short caption to reveal its choice; do not hide every title behind hover. On expansion show category, short explanatory sentence and optional direct service CTA.
4. Prepare a no-JavaScript fallback: the first item stays legible and each category's meaningful content exists in the DOM. Do not gate the site's service proposition on an animation or an image-loading race.

## 2. Desktop interaction grammar

- Four panels are a strong starting point **when there really are four categories**. Lay them out in a clipped flex row with an intentional gap and stable section height. Illustrative García geometry: inactive `flex: 1`, active approximately `flex: 3.4`, gap ~11px, height `clamp(455px, 48vw, 660px)`. Treat these as starting measurements, not brand tokens.
- On pointer/keyboard selection, change one active index. Animate flex-basis/grow and a subtle internal image scale with eased CSS, roughly 650–900ms. Keep image decoding, text and panel sizes stable. Never set every card to absolute positioning or remount the entire gallery on selection.
- Use one semantic control model consistently. When selection reveals an associated description panel, native buttons in a `tablist` with `role="tab"`, `aria-selected`, roving `tabindex` and matched `role="tabpanel"` can work. Only claim that pattern when Arrow Left/Right, Home/End, focus, panel identity and accessible names actually work. Alternatively, use ordinary labeled buttons if the interaction is not truly tabs.
- Clicking an already selected panel does not trigger an unnecessary reload; inactive panels remain discoverable. Focus indicators must remain visible over both pale and dark images. State changes are not announced redundantly or on every transition frame.
- Preserve a direct route to each service in surrounding static page content for indexing and no-JS access. Gallery exploration is **not** the only navigation.

## 3. Small screens and reduced motion

- At mobile widths, retain agency with a **horizontal scroll-snap photo rail**; use roughly 79vw for the active card and 65vw for inactive cards as an optional starting point. Keep horizontal overflow *inside* the rail, never on the document. An adjacent non-overlapping detail panel can carry the active title/description/CTA.
- Support tap, swipe/scroll, and keyboard selection. If a user scrolls between cards, reconcile the selected index with the nearest meaningful card—do not fight touch scrolling with repeated forced `scrollIntoView` calls or autoplay.
- Recheck imagery, headings, portrait focal points and captions at 320px/390px, short viewport height, text enlargement and 200% zoom. Inactive labels must neither crop awkwardly nor make the panel impossible to identify.
- With `prefers-reduced-motion: reduce`, remove width/scale animation and keep all interactions functional; do not delay the detail update for a transition end. If layout reflow is expensive, prefer a shorter/simpler transition.
- Do not autoplay gallery selection by default. If a product genuinely needs autoplay, re-evaluate user control, stop conditions and WCAG 2.2.2 rather than inheriting the hero's timer.

## 4. Implementation and acceptance

1. Read repository `AGENTS.md`, `DESIGN.md`, content plan and approved imagery. Inspect the exact external source before adopting anything beyond the documented mechanics. Reuse compatible components already in the project.
2. Establish a working static, semantic item list first. Add active-index state, desktop expansion, mobile scroll-snap, selected details and reduced-motion rules. Set a useful source-order and accessible image alternatives; decorative duplicates may be hidden from assistive technology.
3. Verify all items are selectable with pointer, keyboard and touch; test Left/Right and Home/End if using tabs. Confirm the selected detail matches the image and that layout remains stable after repeated selection and resizing.
4. Capture desktop and 390px/320px browser views, a narrow viewport with long labels, enlarged text, keyboard focus and reduced-motion. Confirm no cut-off inactive title, horizontal *page* scroll, missing mobile photo, broken source, console errors or blank first load. Mark unrun tests `NOT RUN`.

## 5. Before/after controls and standalone results (separate gallery variant)

An expanding-category selector, a before/after comparison and a grid of single result images are **different controls**. Pick only what helps the visitor. Do not force every result image into an artificial pair or manufacture a clinical 'before' photograph to satisfy a template. If a public page is called “Resultados”, factual clinical cases need patient authorization and accurate context; demo-only images must be described nearby as **generated conceptual images, not patient or treatment outcomes**. Do not imply one smile predicts or guarantees a particular treatment result.

For a before/after comparator:

1. The **visible divider handle is the real pointer hit target**. Press or touch the handle to start, capture that pointer, update solely on movement with the active pointer, release on pointer up/cancel/lost capture. Do **not** move the divider on plain mouse hover or mere pointer entry, and do not reset its position on pointer leave or blur. A transparent full-image input that captures arbitrary clicks is not equivalent to dragging a visible handle.
2. Give the handle a meaningful accessible name, `role="slider"`, focus, `aria-valuemin/max/now` and accurate value text. Support Arrow Left/Right (also Up/Down), Home/End and optionally Shift for larger increments. The handle must work with mouse, touch and keyboard. Keep a stable no-JS comparison fallback.
3. In drag mode, remove the divider's delayed positional animation: the boundary should track the finger/cursor immediately and not lag behind. Ensure the 'Antes' label corresponds to the actual before image and 'Después' to the after image. Use enough drag margin to keep the handle visible at both ends on 320px screens.
4. Test three **independent** modes: move the mouse across the image without pressing (value unchanged); press/drag/release the actual handle (value changes and persists after leaving); focus the handle and use arrows/Home/End (value changes and persists after blur). Include real touch drag, reduced-motion and 200% zoom checks. An automated responsive count alone does not verify this.

For standalone visual results: choose distinct, realistic source photographs with healthy natural variation and authentic skin/enamel detail. Label each photo clearly, optimize and lazy-load it, keep associated text short, and disclose provenance where the gallery is first understood. Real clinical outcomes require separate consent, provenance and claims review; conceptual demo photographs can illustrate **variation and aesthetics**, never treatment efficacy.

This pattern complements `pat-public-marketing-hero-motion` for the first viewport and `pat-public-client-reviews-marquee` for testimonial presentation. In a new commercial site, follow `pb-public-client-website-delivery` for whether and where the gallery belongs.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "public-gallery-content-and-media",
      "type": "decision-question",
      "force": "must",
      "text": "For a public service gallery, first check whether distinct real categories justify an interactive image selector; source truthful desktop/mobile images with rights and avoid presenting illustrative scenes as completed work. Use pat-public-service-gallery-selector, not a copied generic demo.",
      "source": "pat-public-service-gallery-selector",
      "covers": ["accessibility", "hero-fidelity"],
      "activate_when": ["archetype:public-client-website", "archetype:public-site-gallery"],
      "phase": ["planning"],
      "priority": 70
    },
    {
      "id": "public-gallery-responsive-selector",
      "type": "pattern",
      "force": "must",
      "text": "When a gallery is warranted, implement a semantic selectable expanding-photo row on desktop with discoverable inactive labels and a mobile scroll-snap rail plus matching detail panel. Support pointer/touch/keyboard, no-JS and reduced-motion; use site-specific images and titles.",
      "source": "pat-public-service-gallery-selector",
      "covers": ["accessibility", "compatibility", "hero-fidelity"],
      "activate_when": ["archetype:public-client-website", "archetype:public-site-gallery"],
      "phase": ["implementation"],
      "priority": 77
    },
    {
      "id": "public-gallery-live-interaction-check",
      "type": "verification",
      "force": "must",
      "text": "Inspect each gallery panel on desktop, 390px/320px, keyboard tab/arrow/Home/End, touch swipe, zoom and reduced motion; check captions are readable, mobile portrait images load, selected details match and no page overflow or clipped inactive titles remain.",
      "source": "pat-public-service-gallery-selector",
      "covers": ["accessibility", "performance", "hero-fidelity"],
      "activate_when": ["archetype:public-client-website", "archetype:public-site-gallery"],
      "phase": ["verification"],
      "priority": 81
    },
    {
      "id": "public-comparison-drag-handle-contract",
      "type": "pattern",
      "force": "must",
      "text": "When implementing before/after, only a pressed visible handle may start pointer-captured drag. Never follow unpressed mouse hover, use an invisible full-frame input or reset the value on leave. Provide a real focusable slider with touch and Arrow/Home/End controls, no lagging divider transitions, truthful before/after sides and accessible static fallback. Standalone generated smiles are allowed only as explicitly conceptual images, never claimed clinical results.",
      "source": "pat-public-service-gallery-selector",
      "covers": ["accessibility", "compatibility", "hero-fidelity"],
      "activate_when": ["archetype:public-client-website", "archetype:public-site-gallery"],
      "phase": ["implementation"],
      "priority": 86
    },
    {
      "id": "public-comparison-drag-verification",
      "type": "verification",
      "force": "must",
      "text": "Test hover-without-press keeps a comparator unchanged, handle-only mouse and real touch drag capture and persist, keyboard arrows/Home/End work, labels match the layers, and generated standalone portraits load with honest demo provenance; verify at 320px, zoom 200% and reduced motion.",
      "source": "pat-public-service-gallery-selector",
      "covers": ["accessibility", "compatibility", "hero-fidelity"],
      "activate_when": ["archetype:public-client-website", "archetype:public-site-gallery"],
      "phase": ["verification"],
      "priority": 87
    }
  ]
}
```
