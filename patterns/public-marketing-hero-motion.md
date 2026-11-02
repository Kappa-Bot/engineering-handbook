---
id: pat-public-marketing-hero-motion
kind: pattern
status: active
owner: engineering
version: "0.3"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - product-vertical-public-pages
sources:
  - src-21st-tommy-animated-hero
  - src-tommy-twblocks-hero5
  - src-w3c-wcag-22
last_verified: 2026-11-02
review_due: 2027-02-02
---

# Public Marketing Hero: Photo, Story and Rotating-Word Motion

## Scope and authority

This Pattern turns a repeated commercial-site design decision into a discoverable, testable starting point. It complements `std-ui-ux-quality-baseline` and `pb-frontend-quality-review`; **it is not a mandatory hero template, motion-library requirement or portfolio-wide visual skin**. For public marketing pages that deliberately use an autoplay scene selector, the accessible pause and independent-motion behavior in §2.1 is the portfolio default. Brand, wording, color, imagery, privacy, service geography and conversion destination remain owned by the implementing repository and client approval. It does not govern authenticated CRM/clinical/operator screens. Read `pb-public-client-website-delivery` for end-to-end website composition.

Read `pat-design-context-layering` first when platform/vertical/tenant boundaries differ. When a named external component is specified, inspect the **exact component page and actual source**. Do not infer behavior from a library search result, a title containing 'interactive', a still image or an unrelated demo.

## Observed precedent: what Tommy Jepsen actually built

- `src-21st-tommy-animated-hero` points to the exact 21st.dev community page; its listed dependencies are `lucide-react` and `framer-motion`.
- `src-tommy-twblocks-hero5` points to the original MIT-licensed TWBlocks `Hero5`: **a permanent lead phrase with one complete word changing automatically** (roughly every two seconds), each word sliding vertically with opacity and a spring. The donor also has supporting text and two call-to-action buttons.
- This is **not** an effect where glyphs repel/attract the mouse, scatter, glow on hover or change independently. Those are different patterns requiring separate intent and evidence.
- We can reproduce the **interaction grammar** rather than copy its placeholder wording, colors, layout, CSS framework, shadcn buttons or package imports. The donor does not establish a universally acceptable accessibility implementation, pause UI, mobile crop or brand system.

## 1. Decide the hero before designing its animation

| Situation | Preferred design route |
| --- | --- |
| Public service/client business, useful rights-cleared photography | Consider a full-bleed or near/full-viewport photographic hero, with image/overlay/type/CTA composed as one first-viewport experience. |
| No good/authorized imagery; content is more important than spectacle | Prefer a crisp typography-led first screen, not a synthetic stock photograph. |
| Several genuinely different approved service scenes | A manual scene selector may help discovery; do not add autoplay simply to fill the screen. |
| A short claim has several truthful, grammatical interchangeable endings | Consider a restrained rotating *complete word* beneath an unchanging phrase. |
| Operational, clinical, data-dense or repeated-task UI | Prefer clarity, immediate feedback and low motion; this public marketing pattern is normally inapplicable. |

First-view check: Does the visitor learn **what is offered, by whom/where if material, why it matters and what to do next**? Brand poetry may support the claim but cannot replace the service proposition. Keep primary and secondary CTAs distinguishable and pointing to real, working destinations; do not introduce a second quote flow or change an approved conversion route for visual polish.

## 2. Photographic hero composition and choreography

1. Start with the actual approved image(s): focal subject, safe space for copy, mobile crop, lighting, contrast, rights/provenance and image budget. If an editorial/AI image is used, never present it as documentary proof of a completed job. Avoid visible per-photo 'AI' noise when a truthful site-level disclosure already exists and no local law requires another treatment.
2. Compose the navigation overlay, heading, useful supporting sentence, CTA and optional scene controls within the intended viewport. Transparent header at scroll top may be appropriate; sticky/scrolled state must regain an opaque/legible surface and a clear focus ring.
3. If motion adds value, sequence it rather than activating everything at once: slow, small photographic zoom; a title arriving with gentle opacity/directional movement; supporting copy; then CTA buttons from nearby horizontal sides. Crossfade scenes without a blank stage. Keep text/actions usable immediately regardless of the animation lifecycle.
4. **Illustrative ranges, not mandatory tokens:** title/CTA entrances around 700–1200 ms with decelerated easing; crossfades around 800–1200 ms; subtle zoom from about 1.01–1.06 over 10–15 seconds. Prefer the owning site's existing motion language; visible quality and device measurements decide the actual values.
5. Separate motion layers: **scene transition**, **first-entry content reveal**, and **rotating word** are independent. Do not replay all entrance animations every time a keyword changes. A manual scene change must not force the H1 to remount or lose focus.
6. Header dropdowns, dots/arrows, navigation, scroll targets and WhatsApp/contact affordances need predictable pointer/keyboard/touch feedback. If a carousel auto-advances, follow the explicit pause and lifecycle contract in §2.1; suspend while navigation is open and when hidden/offscreen; respect reading time.

## 2.1. Accessible scene controls and independent timers (public websites)

For **public client/business hero carousels that intentionally auto-advance**, use the following shared interaction grammar. The 2026-11-02 Pinturas García build demonstrated that a compact visible pause/play affordance can coexist with a quiet hero and independent headline words. This updates the earlier Agurto manual-takeover/no-visible-pause precedent. Never add a carousel to a page that does not need one.

1. **Visible, accessible pause/play.** Keep the controls quiet but explicit: previous/next arrows near the side edges, compact dots and a recognizable pause/play button. Add a distinct round down-arrow only where there is meaningful content below. Use the **client's** tokens, not Agurto's palette. The pause control needs a real accessible name and state reflecting its effect.
2. **Independent scene and word clocks.** A useful García-style example uses an approximately 7.6-second scene interval and a separately scheduled ~2.8-second whole-word interval. A manual dot/arrow/swipe/keyboard scene selection changes the photo and may reschedule **only the scene clock**; it must not remount the heading or reset the word's independent phase. Starting, stopping and resuming must never create duplicated intervals. A pause action stops **all automatically advancing hero content** (photos and words) until an explicit resume; do not silently restart when hover/focus ends.
3. **User control and focus.** Arrow/dot/swipe/keyboard changes remain operable while paused. If focus or navigation requires temporarily suspending autoplay, do so without erasing explicit paused state. Manual-only or permanent manual takeover is an acceptable simpler variant if clearly disclosed and verified, but it is no longer the universal default. On return from focus, background or a scrolled-away state, resume only when the user's setting permits.
4. **Lifecycle and accessibility:** stop automatic updates while the hero is offscreen, the tab is hidden or a navigation overlay is open; show a readable static first scene/word under `prefers-reduced-motion`. WCAG 2.2 SC 2.2.2 requires a mechanism to pause, stop or hide ongoing automatic moving/updating content. An invisible shortcut or screen-reader-only button is insufficient if ordinary visitors cannot discover the mechanism. Without JavaScript, a real first image, H1, support text and CTA still exist.
5. **Responsive placement:** touch-friendly targets and visible focus rings must not collide with H1/CTAs/sticky header. Move arrows lower on narrow screens if desktop centering intersects the copy; keep dots, pause and next-section arrow within reachable safe areas, with no horizontal document scroll.

### Required tests for this control grammar

- Initial scene is visible before JS; autoplay runs only when motion is enabled, the page/hero is visible and navigation is closed.
- Manually choose a scene (arrow, dot, swipe and keyboard): verify the chosen photo, accessible selected state, rescheduled scene timing and **uninterrupted word schedule**. Wait beyond the scene interval; check only permitted autoplay runs.
- Activate the visible pause button, wait beyond both intervals and confirm **neither scene nor word advances**; manually navigate a scene while paused; explicitly resume and verify both clocks run once. Check focus/blur and return from background do not silently override pause.
- Verify reduced-motion, hidden tab, offscreen, menu-open, 320px and 390px, desktop, zoom and focus/contrast. Do not mark these passes without observing them.
- Confirm visible pause/play placement, readable accessible name and state. If no credible pause/stop mechanism can be tested, use manual-only scenes instead.

## 3. Rotating-word title contract

Use the original Hero5 **structure and purpose**, not its site styling:

- **Stable lead:** a short phrase that never moves when the keyword changes (e.g., 'Mover, con').
- **Whole-word states:** two to four approved, grammatical words, not a stream of individual glyphs (e.g., 'cuidado.', 'precisión.', 'confianza.'). Preserve accents and punctuation; the longest translated word must fit.
- **Single slot:** center a fixed-width/height, overflow-clipped second line; reserve its dimensions before hydration and font load so swapping cannot move the CTA or create CLS. Measure/size for the **longest** state, including on 320px screens, 200% zoom and large text.
- **Motion:** a gentle upward/downward enter/exit with fade and a damped spring; about 2–4 seconds of reading between changes, tuned to actual copy. At most one word is prominent/readable at once. Never leave a moment with both words illegible or layer two fully opaque words.
- **Semantics:** maintain **one real H1** in the server-rendered HTML, with a meaningful stable accessible phrase. When alternates are decorative synonyms, keep them out of repetitive screen-reader announcements; when they convey distinct essential claims, render those claims elsewhere as real accessible text rather than silently hiding meaning.
- **SSR/no JS:** the first approved word and CTA are visible without hydration, timers or an external API. Do not render an empty heading or defer SEO text to client effects.
- **Lifecycle:** use one managed timer per independent concern with cleanup, never overlapping duplicates during rerenders. Stop updates while explicitly paused, out of view/inactive tab, menu-open and under `prefers-reduced-motion`. Word changes should not be accidentally coupled to scene selection; WCAG 2.2.2 applies to both moving concerns.
- **Interaction:** this timer does **not** depend on hover. Do not silently substitute a mouse-magnetic effect; mobile/touch receives the same rotating words when motion is enabled or a truthful static fallback when not.
- **Dependencies:** reuse an existing compatible `motion/react`/Framer Motion integration where already present and licensed. Plain CSS or Web Animations may be enough for a simple phrase. Evaluate dependency weight/version/licensing before adding a new animation package; do not transplant the whole donor component merely for one word.

### Implementation sketch (adapt, not copy verbatim)

~~~tsx
// Pseudocode for a product-local React component; lifecycle and accessibility are required.
const words = ['cuidado.', 'precisión.', 'confianza.'] as const;
const [active, setActive] = useState(0);
// Resolve prefers-reduced-motion, explicit pause, menu/visibility state; scene and word timers remain independent.
// Register one 3-second interval with cleanup, and show word[0] without JS.

<h1 aria-label="Mover, con cuidado.">
  <span aria-hidden="true">Mover, con</span>
  <span className="fixed-clipped-word-slot" aria-hidden="true">
    <AnimatePresence initial={false}>
      <motion.span key={words[active]}
        initial={{ opacity: 0, y: '90%' }} animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: '-90%' }}
        transition={{ type: 'spring', stiffness: 65, damping: 20 }}>
        {words[active]}
      </motion.span>
    </AnimatePresence>
  </span>
</h1>
~~~

This sketch is **not** a packaged shared component. Real code must ensure the initial word renders without JS, keying does not trigger parent remounts, `prefers-reduced-motion` is active before scheduling new intervals, reduced-motion transitions are disabled, and the pause mechanism satisfies the actual runtime and accessibility needs. Do not hard-code Agurto's words, dimensions or gold accent into another brand.

## 4. Media truth and visual identity

- A site's service cards, real-work gallery, team portrait and editorial/AI hero scenes may have different provenance. Track it in a media manifest. A generated portrait is **not** the original person's face or proof of identity; preserve authentic originals and do not assert otherwise.
- Perform the actual photo grading/retouch in source assets where approved; use responsive AVIF/WebP and correct sizes/priorities. Avoid compounding blanket CSS filters on already graded photographs.
- Choose a meaningful frame rather than merely using huge images. Alternate image and useful information so the rest of the site never reads as an endless photo slideshow. Give users a direct route to services, proof, process and contact.
- Preserve the consumer brand contract and legal identity. Handbook examples illustrate *mechanics*, not shared wording, palette, photo style, uniforms or geography.

## 5. Acceptance matrix and evidence

| Scenario | Acceptance signal |
| --- | --- |
| First load, SSR/no JS, slow hydration | Real H1 and CTA are visible, no flash of empty or duplicate text. |
| Keyword changes across all states | Correct full words/accents, smooth vertical transition, one prominent word, no CTA movement/CLS. |
| Motion reduced, pause, hidden/offscreen | Static claim under reduced motion; visible pause freezes scene and word, manual selection need not stop the independent word clock, hidden/offscreen and menu-open suspend both. |
| Scene change, open nav, sticky scroll | Hero/carousel/header feedback remains usable; text never disappears or overlaps navigation. |
| 320px, 390px, desktop, short heights, 200% zoom | All words/CTA/controls fit and remain keyboard/gesture accessible; no unwanted horizontal scroll. |
| Accessibility and performance | Focus and contrast pass, meaningful H1, no rapid announcements, media load/INP/LCP/CLS meet product budgets. |
| End-to-end conversion and live release | Correct service and quote/contact routes, real photos and disclosures, exact-SHA build, browser screenshot/video inspection plus live-domain smoke. |

A passing typecheck/build or a screenshot from a single animation frame is **not** evidence that the motion or pause behavior was exercised. Use `pat-visual-evidence-integrity`, `pat-performance-budgeting` and the product's own tests. Label unrun browser/native checks `NOT RUN` explicitly.

## 6. Adoption in a new public web task

During the normal `pb-frontend-quality-review` flow, write only a small hero decision: (1) proposition/CTA, (2) media rights and desktop/mobile crop, (3) static versus moving imagery, (4) whether word rotation improves the message, (5) existing motion primitive, (6) independent timers/explicit pause/reduced-motion strategy, (7) verification matrix. Prefer **no** rotating word when it adds noise or when each word changes the meaning of the offer.

Use a donor only after the exact behavior has been observed. The documented MelodIQ Ops OS/Agurto learning on 2026-10-30 was the **failed identification** of a magnetic letter hover as the requested `Animated Hero`, followed by correction to the original rotating whole-word design. This lesson applies across future websites; it does **not** certify that other Verticals already adopted or tested that component.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "marketing-hero-brief-and-source",
      "type": "decision-question",
      "force": "must",
      "text": "For a public marketing hero, check the approved brand, truthful first-viewport offer, primary CTA, image rights and responsive crops before choosing motion. If a specific component is named, inspect its exact page and original code rather than guessing its behavior.",
      "source": "pat-public-marketing-hero-motion",
      "covers": [
        "accessibility",
        "hero-fidelity"
      ],
      "activate_when": [
        "archetype:marketing-hero-change",
        "archetype:public-client-website"
      ],
      "phase": [
        "planning"
      ],
      "priority": 73
    },
    {
      "id": "marketing-hero-rotating-word-pattern",
      "type": "pattern",
      "force": "must",
      "text": "When rotating words suit the approved marketing message, keep the lead phrase steady and rotate complete words in a clipped stable slot independently of photo scenes. Provide server-readable H1, no-JS/reduced-motion fallback, visible pause for all autoplay, independent timers and no duplicate intervals. Do not confuse timed whole words with magnetic letter hover.",
      "source": "pat-public-marketing-hero-motion",
      "covers": [
        "accessibility",
        "compatibility",
        "hero-fidelity"
      ],
      "activate_when": [
        "archetype:marketing-hero-change",
        "archetype:public-client-website"
      ],
      "phase": [
        "implementation"
      ],
      "priority": 78
    },
    {
      "id": "marketing-hero-live-acceptance",
      "type": "verification",
      "force": "must",
      "text": "For a material hero change, verify desktop and 320px/390px/200% zoom, dedicated mobile crop, headline/CTA, carousel/header controls, visible pause freezing scene and words, independence after manual scene choice, reduced motion, background/menu lifecycle, stability, exact-SHA build and live browser smoke; report unrun gates.",
      "source": "pat-public-marketing-hero-motion",
      "covers": [
        "accessibility",
        "compatibility",
        "hero-fidelity",
        "performance"
      ],
      "activate_when": [
        "archetype:marketing-hero-change",
        "archetype:public-client-website"
      ],
      "phase": [
        "verification"
      ],
      "priority": 88
    }
  ]
}
```
