---
id: pat-public-marketing-hero-motion
kind: pattern
status: active
owner: engineering
version: "0.5"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - product-vertical-public-pages
sources:
  - src-21st-tommy-animated-hero
  - src-tommy-twblocks-hero5
  - src-w3c-wcag-22
last_verified: 2026-11-05
review_due: 2027-02-05
---

# Public Marketing Hero: Photo, Story and Rotating-Word Motion

## Scope and authority

This Pattern turns a repeated commercial-site design decision into a discoverable, testable starting point. It complements `std-ui-ux-quality-baseline` and `pb-frontend-quality-review`; **it is not a mandatory hero template, motion-library requirement or portfolio-wide visual skin**. For public marketing pages that deliberately use an autoplay scene selector, the owner-approved control inventory and independent-motion behavior in §2.1 are the portfolio default. **A timed carousel does not authorize adding a play/pause button.** Brand, wording, color, imagery, privacy, service geography and conversion destination remain owned by the implementing repository and client approval. It does not govern authenticated CRM/clinical/operator screens. Read `pb-public-client-website-delivery` for end-to-end website composition.

Read `pat-design-context-layering` first when platform/vertical/tenant boundaries differ. When a named external component is specified, inspect the **exact component page and actual source**. Do not infer behavior from a library search result, a title containing 'interactive', a still image or an unrelated demo.

For long-form source, reference or training surfaces, use [Editorial Reading and Navigation](editorial-reading-navigation.md) to compose the first view. For a moving marketing hero, apply [Interaction Continuity](interaction-continuity.md) to keep first-frame copy, the CTA and its hit area available during and after the effect.

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
6. Header dropdowns, dots/arrows, navigation, scroll targets and WhatsApp/contact affordances need predictable pointer/keyboard/touch feedback. If a carousel auto-advances, follow the owner-approved control inventory and lifecycle contract in §2.1; handle reduced motion, navigation, hidden/offscreen state and reading time deliberately.

### Photo-fidelity and composition gate (owner correction, 2026-11-05)

A high-contrast **full-bleed photographic hero must still read as a photograph**. Reject near-opaque cream/white overlays, unilateral light gradients, artificial side-to-side exposure fades, blanket saturation loss, aggressive filters and copy-driven masks that erase half a scene. This is a concrete regression class: a clinic website published a photographic hero with a 0.91-alpha pale side wash, making carefully generated original images almost disappear. Passing responsive checks did not make that visual output acceptable.

- Start with a source photograph composed for the intended text zone and crop; choose background and typography together. If readability needs help, test a **neutral, spatially uniform translucent dark scrim** at the minimum contrast-safe opacity, or a genuinely localized text treatment. A decorative 'mist' fade is **not** an acceptable substitute for contrast testing.
- Preserve the visual integrity of the **actual full scene** (same exposure/saturation from left to right) on desktop and recomposed portrait mobile assets. Check focal subjects and photograph fidelity in **rendered screenshots**, not only DOM geometry or calculated LCP. Compare against the owner's approved live reference, including scene two/three and responsive variants.
- When a transparent header sits on the image, check the **original logo asset**, navigation, telephone/WhatsApp prompts and focus states over *each* photo; an original logo may use a reversible on-photo CSS presentation variant if the owner approves, never an unrequested plaque or brand redesign. Scrolling restores an opaque and readable header.
- Keep the photographic treatment and palette **site-specific**. A warm nonwhite canvas, softened dark type, or an exact CTA inventory applies when explicitly approved in the consumer's DESIGN.md; do not impose one client's skin or gallery/blog count across the portfolio.
- A hero change cannot silently add, remove, duplicate or move a utility section (e.g. Maps). Route-level content ownership belongs to the site's source brief and should be independently checked in every locale.

## 2.1. Scene controls, autoplay and owner authority (public websites)

**Non-negotiable no-surprise-UI rule (owner correction, 2026-11-02):** **NEVER add a hero pause/play button, floating media toggle, hidden playback button or adjacent playback icon just because the carousel auto-advances, a component donor contains one, or an automated review suggests one.** The default control inventory is the site's **explicitly approved** arrows, scene dots, swipe/keyboard behavior and optional next-section cue. A playback button is permitted **only when that site's owner specifically asks for or approves that control**. A request such as “auto-advance the photos every five seconds” authorizes the timing, **not** new controls or a redesign. Before copying an existing hero (including Pinturas García) into another client project, remove all donor-specific controls that the new owner has not approved.

**Agurto binding precedent:** the owner explicitly requested its 3-photo hero to auto-advance every **5,000 ms**, then explicitly rejected the added pause button. Keep exactly its approved side arrows, **three centered dots**, horizontal swipe, keyboard selection, separate rotating headline, reduced-motion static scene and hidden-tab suspension. **No pause/play UI in the Agurto hero—visible, offscreen or screen-reader-only.** Treat the older universal “visible pause for all autoplay” prescription, and any historical manual-only Agurto instruction, as superseded. Never restore either through a generic accessibility refactor. The corresponding app must have a regression test proving the control group has only the five approved buttons.

1. **Preserve exact approved controls.** No extra icon may appear beside/between dots, over the photo, under the heading or inside the navigation when it wasn't in the owner's brief. For a manually operated carousel, do not invent a playback control either. Preserve hit areas, focus, arrows, selected state and responsive placement.
2. **Independent scene and word clocks.** Autoplay timing is a site-level decision, not copied from a demo (Agurto photos: 5,000 ms; headline: 3,000 ms). Selecting a scene may restart only the photo timer. Never remount the word headline, reset its clock because a photograph changed, or create duplicate intervals. Existing user-directed manual selection must remain functional.
3. **Explicit accessibility decision, not an unsolicited button.** WCAG 2.2 SC 2.2.2 requires a mechanism to pause, stop or hide moving/auto-updating content that runs automatically alongside other content. **Removing the visible button does not itself satisfy this criterion**, nor do reduced-motion and tab-visibility safeguards alone prove compliance. For new sites, resolve a suitable owner-approved stopping mechanism and test it (or choose manual-only scenes with owner approval). If the owner mandates autoplay but forbids any conforming mechanism, record the accessibility gap truthfully and seek a separate decision; **do not silently inject the rejected UI or undo the requested five-second timing**. Apply the same reasoning to automatically rotating headline words.
4. **Lifecycle and focus.** Honor `prefers-reduced-motion` with a readable static scene/word; clear timers on unmount and during hidden-tab state. Handle offscreen/menu-open/focus suspension when implemented, and ensure returning to a visible tab never duplicates timers. Do not make hover an undisclosed prerequisite for a scene change.
5. **Responsive composition.** Keep the approved dots centered when adding/removing any optional controls; safe-area constraints, minimum touch targets and focus rings matter at 320px, 390px and desktop/zoom. Neither the H1/CTA nor the scroll cue may be obstructed.

### Required verification for a moving hero

- Assert the **exact owner-approved control inventory**; for Agurto this means arrows + three scene dots, **zero** pause/play buttons or playback UI. Guard against any extra button, regardless of its accessible label.
- With autoplay allowed, check the requested scene interval at its boundary (Agurto: 4,999 ms unchanged, 5,000 ms next), wraparound and manual-selection countdown; verify rotating words remain independent.
- Verify swipe/keyboard navigation, reduced motion, hidden/visible tab, cleanup, no-JS first scene/H1/CTA, mobile/desktop placement, zoom and no layout jump.
- If a separate stopping mechanism was actually approved and implemented, verify its accessibility and that it stops all intended moving concerns. Otherwise, **do not declare WCAG 2.2.2 conformance solely from autoplay tests or a screenshot**.

## 3. Rotating-word title contract

Use the original Hero5 **structure and purpose**, not its site styling:

- **Stable lead:** a short phrase that never moves when the keyword changes (e.g., 'Mover, con').
- **Whole-word states:** two to four approved, grammatical words, not a stream of individual glyphs (e.g., 'cuidado.', 'precisión.', 'confianza.'). Preserve accents and punctuation; the longest translated word must fit.
- **Single slot:** center a fixed-width/height, overflow-clipped second line; reserve its dimensions before hydration and font load so swapping cannot move the CTA or create CLS. Measure/size for the **longest** state, including on 320px screens, 200% zoom and large text.
- **Motion:** a gentle upward/downward enter/exit with fade and a damped spring; about 2–4 seconds of reading between changes, tuned to actual copy. At most one word is prominent/readable at once. Never leave a moment with both words illegible or layer two fully opaque words.
- **Semantics:** maintain **one real H1** in the server-rendered HTML, with a meaningful stable accessible phrase. When alternates are decorative synonyms, keep them out of repetitive screen-reader announcements; when they convey distinct essential claims, render those claims elsewhere as real accessible text rather than silently hiding meaning.
- **SSR/no JS:** the first approved word and CTA are visible without hydration, timers or an external API. Do not render an empty heading or defer SEO text to client effects.
- **Lifecycle:** use one managed timer per independent concern with cleanup, never overlapping duplicates during rerenders. Apply the actual owner-approved stop/visibility policy (and always respect `prefers-reduced-motion` and inactive tabs); do not assume a visible pause button exists. Word changes should not be accidentally coupled to scene selection; WCAG 2.2.2 applies to both moving concerns.
- **Interaction:** this timer does **not** depend on hover. Do not silently substitute a mouse-magnetic effect; mobile/touch receives the same rotating words when motion is enabled or a truthful static fallback when not.
- **Dependencies:** reuse an existing compatible `motion/react`/Framer Motion integration where already present and licensed. Plain CSS or Web Animations may be enough for a simple phrase. Evaluate dependency weight/version/licensing before adding a new animation package; do not transplant the whole donor component merely for one word.

### Implementation sketch (adapt, not copy verbatim)

~~~tsx
// Pseudocode for a product-local React component; lifecycle and accessibility are required.
const words = ['cuidado.', 'precisión.', 'confianza.'] as const;
const [active, setActive] = useState(0);
// Resolve prefers-reduced-motion and the approved visibility/stop strategy; scene and word timers remain independent.
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

This sketch is **not** a packaged shared component. Real code must ensure the initial word renders without JS, keying does not trigger parent remounts, `prefers-reduced-motion` is active before scheduling new intervals, reduced-motion transitions are disabled, and any stopping mechanism is evaluated against the approved UI and actual accessibility requirements. Do not hard-code Agurto's words, dimensions or gold accent into another brand.

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
| Motion reduced, hidden/offscreen, owner-approved controls | Static claim under reduced motion; no unrequested pause/play UI; hidden tabs suspend photo rotation; any approved stopping mechanism and menu/offscreen lifecycle verified separately. |
| Scene change, open nav, sticky scroll | Hero/carousel/header feedback remains usable; text never disappears or overlaps navigation. |
| 320px, 390px, desktop, short heights, 200% zoom | All words/CTA/controls fit and remain keyboard/gesture accessible; no unwanted horizontal scroll. |
| Accessibility and performance | Focus and contrast pass, meaningful H1, no rapid announcements, media load/INP/LCP/CLS meet product budgets. |
| End-to-end conversion and live release | Correct service and quote/contact routes, real photos and disclosures, exact-SHA build, browser screenshot/video inspection plus live-domain smoke. |

A passing typecheck/build or a screenshot from a single animation frame is **not** evidence that the motion or pause behavior was exercised. Use `pat-visual-evidence-integrity`, `pat-performance-budgeting` and the product's own tests. Label unrun browser/native checks `NOT RUN` explicitly.

## 6. Adoption in a new public web task

During the normal `pb-frontend-quality-review` flow, write only a small hero decision: (1) proposition/CTA, (2) media rights and desktop/mobile crop, (3) static versus moving imagery, (4) whether word rotation improves the message, (5) existing motion primitive, (6) independent timers/owner-approved control and accessibility strategy, (7) verification matrix. Prefer **no** rotating word when it adds noise or when each word changes the meaning of the offer.

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
      "text": "When rotating words suit the approved marketing message, keep the lead phrase steady and rotate complete words in a clipped stable slot independently of photo scenes. Provide server-readable H1, no-JS/reduced-motion fallback, independent timers and no duplicate intervals. NEVER add hero pause/play UI without explicit site-owner approval; flag WCAG 2.2.2 gaps rather than silently introducing a control. Do not confuse timed whole words with magnetic letter hover.",
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
      "text": "For a material hero change, verify desktop and 320px/390px/200% zoom, mobile crop, H1/CTA, exact owner-approved carousel controls (Agurto: five buttons, no pause/play), requested photo timing, independent word timer, reduced motion, background/menu lifecycle, WCAG 2.2.2 mechanism or documented gap, exact-SHA build and live browser smoke; report unrun gates.",
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
        "verification"
      ],
      "priority": 88
    },
    {
      "id": "marketing-hero-photo-fidelity",
      "type": "pattern",
      "force": "must",
      "text": "For an owner-approved full-bleed photographic marketing hero, preserve the photo's exposure and saturation across the entire image: no near-opaque pale wash, unilateral gradients, artificial bleaching, or source-erasing filter. Compose copy over a suitable photo, or use a measured uniform neutral dark scrim/local text contrast treatment; check actual desktop and portrait mobile screenshots, all scenes, header/logo, direct-contact CTAs and original owner reference. Do not copy a site's palette or section inventory into another client.",
      "source": "pat-public-marketing-hero-motion",
      "covers": [
        "accessibility",
        "hero-fidelity",
        "compatibility"
      ],
      "activate_when": [
        "archetype:marketing-hero-change",
        "archetype:public-client-website"
      ],
      "phase": [
        "implementation"
      ],
      "priority": 90
    }
  ]
}
```
