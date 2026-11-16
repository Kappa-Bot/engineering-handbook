---
id: pat-public-marketing-hero-motion
kind: pattern
status: active
owner: engineering
version: "0.6"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - product-vertical-public-pages
sources:
  - src-21st-tommy-animated-hero
  - src-tommy-twblocks-hero5
  - src-w3c-wcag-22
last_verified: 2026-11-16
review_due: 2027-02-16
---

# Public Marketing Hero: Composition and Optional Motion

## Scope and authority

This Pattern provides optional photographic, scene-selector and rotating-word mechanics. [UI/UX Quality Baseline §1](../standards/ui-ux-quality-baseline.md#1-product-specific-design-and-reconstruction) and `pb-frontend-quality-review` control the diagnosis, direction and acceptance. **Neither photography, viewport-filling composition, autoplay, word rotation nor a donor's control inventory is a portfolio default.** An authorized redesign can replace an inadequate hero and supersede its old aesthetic contract. Legal identity, verified claims, media rights, privacy, service geography, current explicit constraints and conversion behavior remain protected. This Pattern does not govern authenticated CRM/clinical/operator screens. Read `pb-public-client-website-delivery` for end-to-end website composition.

**Supersession, 2026-11-16:** earlier portfolio assumptions about photographic choreography and a universal no-pause/play rule are retired. §2.1 retains the dated Agurto decision as history, separates current site constraints from new design authority, and keeps accessibility gaps explicit.

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

## 2. Photographic composition, when selected

Apply this section only when the current direction deliberately uses a photographic hero. A typography-led or product-led first view is not an incomplete version of this pattern.

1. Start with the actual approved image(s): focal subject, safe space for copy, mobile crop, lighting, contrast, rights/provenance and image budget. If an editorial/AI image is used, never present it as documentary proof of a completed job. Avoid visible per-photo 'AI' noise when a truthful site-level disclosure already exists and no local law requires another treatment.
2. Compose the navigation overlay, heading, useful supporting sentence, CTA and optional scene controls within the intended viewport. Transparent header at scroll top may be appropriate; sticky/scrolled state must regain an opaque/legible surface and a clear focus ring.
3. If motion materially improves understanding or character, choreograph only the selected effects. Static photography is a complete option. Do not require zoom, title entrances or buttons flying in from opposite sides. Crossfade scenes without a blank stage when transitions are selected; keep first-frame copy, actions and hit areas immediately usable.
4. Choose duration, amplitude and easing from the current direction, reading task and device measurements. Historical donor entrance/crossfade timings are not default tokens or proof of quality. Replace inherited motion when it distracts, delays content or harms interaction.
5. Separate motion layers: **scene transition**, **first-entry content reveal**, and **rotating word** are independent. Do not replay all entrance animations every time a keyword changes. A manual scene change must not force the H1 to remount or lose focus.
6. Header dropdowns, dots/arrows, navigation, scroll targets and WhatsApp/contact affordances need predictable pointer/keyboard/touch feedback. If a carousel auto-advances, select its controls and accessible stopping behavior under §2.1; handle reduced motion, navigation, hidden/offscreen state and reading time deliberately.

### Photo-fidelity and composition gate

A composition that promises **full-bleed photography must still communicate its intended scene**. The historical 2026-11-05 correction concerned a clinic hero with a 0.91-alpha pale wash that unintentionally erased useful original imagery. Its general lesson is to verify the rendered composition, not to prohibit gradients, asymmetric lighting, duotone or other deliberate art direction. A chosen editorial treatment can transform an image; do not disguise a failed implementation as intentional styling after the fact.

- Choose source, crop, type and any overlay together. A uniform scrim, localized text surface, gradient or another treatment is a candidate, not a requirement. Test actual text/control contrast and whether the treatment helps the selected direction rather than hiding its focal content.
- Check intended subjects, visible scene information, grading and crops in **rendered desktop/mobile states** against the current direction and source assets. Exposure/saturation need not be uniform across a scene. If several scenes exist, inspect every active scene and meaningful transition; do not require an inherited two/three-photo inventory.
- When a header overlays media, check authentic logo assets, navigation, real contact actions and focus across every selected scene and scroll state. Reversible presentation variants may be chosen within delegated visual authority; replacing the authentic mark or misrepresenting identity is a separate decision. Scrolled navigation must remain readable, without a mandatory material.
- Keep treatment and palette **site-specific**. Current explicit constraints remain applicable; an authorized redesign can supersede weak historical palette, overlay and CTA-presentation choices while preserving real destinations and capabilities. Do not impose another client's skin or section counts.
- A bounded hero change cannot silently alter the site's utility sections or conversion flow. An authorized wider redesign may recompose section order and placement; record the revised content contract and verify that required information, destinations and localized variants are not lost or duplicated.

## 2.1. Scene controls, autoplay and scoped design authority

### Current design decisions

Choose controls as part of the authorized direction and the actual interaction, not by copying a donor inventory. There is **no global veto on pause/play controls**. Where the owner has delegated new design or redesign decisions, the agent can select and implement a visible accessible stopping control, a manual selector or a static hero without requesting another aesthetic confirmation for each control. A narrow timing or defect fix does not confer that wider redesign scope.

An explicit **current** site constraint still matters. If it forbids a control or fixes autoplay behavior, do not silently bypass it with hidden UI or change the requested behavior. Resolve any conflict with the accessibility baseline through a scoped decision; record an unmet requirement as `FAIL`/`BLOCKED`, never as conformance. This applies to both moving scenes and rotating words.

### Historical Agurto decision — not a portfolio rule

The owner correction recorded on **2026-11-02** selected three photos advancing every **5,000 ms**, side arrows, **three centered dots**, horizontal swipe and keyboard selection, a separate headline clock (3,000 ms), reduced-motion static content and hidden-tab suspension. It also expressly rejected pause/play UI, including hidden controls. That replaced earlier manual-only instructions **for that historical Agurto scope**.

Keep this record to explain the original implementation and its five-button regression expectation. It is neither verification of the current live site nor authority to change Agurto from the Handbook. For maintenance of that contract, read the consumer's current instructions and test the still-applicable inventory and timing. For a separately authorized redesign, document the replacement decision instead of exporting this old constraint to a new design or another client. No consumer deployment follows from this revision.

### Mechanics for the selected behavior

1. **Deliberate control inventory.** Use only controls that support the chosen interaction and make their purpose, selected state, focus, hit areas and responsive placement clear. A manual selector does not need a decorative playback button; an autoplay design must satisfy its applicable stopping requirement.
2. **Independent scene and word clocks, when both exist.** Derive cadence from the local reading task, not a donor. Selecting a scene may restart its own timer, but must not remount the word headline, reset an unrelated clock or create duplicate intervals. Manual selection remains functional.
3. **Accessibility is an acceptance requirement.** Apply WCAG 2.2 SC 2.2.2 to the actual moving/auto-updating content. Where it requires a way to pause, stop or hide content, implement and test one, or use a design without that automatic behavior. Reduced-motion and tab-visibility safeguards alone do not prove conformance. If a current explicit constraint prevents a conforming implementation, surface the conflict rather than inventing a pass.
4. **Lifecycle and focus.** Honor `prefers-reduced-motion` with a readable static scene/word; clear timers on unmount and during hidden-tab state. Handle offscreen/menu-open/focus suspension when implemented, and ensure returning to a visible tab never duplicates timers. Do not make hover an undisclosed prerequisite for a scene change.
5. **Responsive composition.** Keep the chosen controls stable and reachable; safe areas, touch targets and focus rings matter at 320px, 390px and desktop/zoom. Neither the H1/CTA nor the scroll cue may be obstructed. Placement follows the current direction, not a mandatory centered-dot arrangement.

### Required verification for a moving hero

- Assert the **current design's control inventory**, accessible names and behavior. Apply the historical Agurto five-button expectation only when that remains the explicitly applicable consumer contract; do not turn it into a default for other sites or redesigns.
- With autoplay selected, check the specified interval immediately before and at its boundary, wraparound and manual-selection countdown; verify rotating words remain independent. For maintenance of the historical 5,000 ms Agurto contract, the relevant boundary is 4,999/5,000 ms.
- Verify swipe/keyboard navigation, reduced motion, hidden/visible tab, cleanup, no-JS first scene/H1/CTA, mobile/desktop placement, zoom and no layout jump.
- Verify that the selected stopping mechanism is accessible and stops all intended moving concerns, or document why the automatic behavior does not require it. **Do not declare WCAG 2.2.2 conformance solely from autoplay tests, reduced-motion support or a screenshot**; unresolved gaps are not passing results.

## 3. Rotating-word title contract

Apply this only when the current direction selects rotating words. Reuse useful Hero5 **structure and purpose**, not its site styling or an obligation to animate the headline:

- **Stable lead:** a short phrase that never moves when the keyword changes (e.g., 'Mover, con').
- **Whole-word states:** use a small useful set of truthful, grammatical words, not a stream of individual glyphs. The donor's two-to-four-word set is an example, not a quota. Preserve accents and punctuation; the longest translated word must fit.
- **Single slot:** align an overflow-clipped word slot to the chosen composition; reserve sufficient dimensions before hydration and font load so swapping cannot move the CTA or create CLS. It need not be a centered second line. Measure/size for the **longest** state, including on 320px screens, 200% zoom and large text.
- **Motion:** select direction, transition and reading time from the current composition and actual copy. The donor's vertical fade/spring and 2–4-second cadence are examples, not required tokens. Keep one coherent readable claim; do not create a blank or contradictory overlapping state.
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
- Preserve authentic identity, third-party brand rights and verified business facts. Supersede inadequate aesthetic decisions within authorized redesign under `std-ui-ux-quality-baseline` §1. Handbook examples illustrate *mechanics*, not shared wording, palette, photo style, uniforms or geography.

## 5. Acceptance matrix and evidence

Apply rows to the selected mechanics. A static hero does not need invented timers or scene controls to pass; mark those cases inapplicable with a reason.

| Scenario | Acceptance signal |
| --- | --- |
| First load, SSR/no JS, slow hydration | Real H1 and CTA are visible, no flash of empty or duplicate text. |
| Keyword changes across all states | Correct full words/accents, smooth vertical transition, one prominent word, no CTA movement/CLS. |
| Motion reduced, hidden/offscreen, chosen controls | Static claim under reduced motion; current scoped control contract respected; hidden tabs suspend photo rotation; applicable stopping mechanism and menu/offscreen lifecycle verified separately. |
| Scene change, open nav, sticky scroll | Hero/carousel/header feedback remains usable; text never disappears or overlaps navigation. |
| 320px, 390px, desktop, short heights, 200% zoom | All words/CTA/controls fit and remain keyboard/gesture accessible; no unwanted horizontal scroll. |
| Accessibility and performance | Focus and contrast pass, meaningful H1, no rapid announcements, media load/INP/LCP/CLS meet product budgets. |
| End-to-end conversion; live release only when authorized | Correct service and quote/contact routes, truthful media and disclosures, exact-SHA build/render evidence; live-domain smoke only within authorized publication scope. |

A passing typecheck/build or a screenshot from a single animation frame is **not** evidence that the motion or pause behavior was exercised. Use `pat-visual-evidence-integrity`, `pat-performance-budgeting` and the product's own tests. Label unrun browser/native checks `NOT RUN` explicitly.

## 6. Adoption in a new public web task

Within the direction and evidence record from `pb-frontend-quality-review`, decide the hero's proposition/CTA, whether media is useful and rights-cleared, responsive composition, static versus moving behavior, selected primitives and control/accessibility strategy. Do not create a parallel visual brief or preserve a weak hero merely to match a donor. Prefer **no** rotating word when it adds noise or changes the meaning of the offer. Record the relevant verification matrix; redesign authority does not authorize publication.

Use a donor only after the exact behavior has been observed. The documented MelodIQ Ops OS/Agurto learning on 2026-10-30 was the **failed identification** of a magnetic letter hover as the requested `Animated Hero`, followed by correction to the original rotating whole-word design. This lesson applies across future websites; it does **not** certify that other Verticals already adopted or tested that component.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "marketing-hero-brief-and-source",
      "type": "decision-question",
      "force": "must",
      "text": "For a public hero, apply std-ui-ux-quality-baseline section 1 to the current direction, truthful offer and real CTA. Photography, full-viewport layout and motion are optional, not inherited defaults. Check media rights and responsive composition when relevant. If a specific component is named, inspect its exact page and original code rather than guessing behavior.",
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
      "text": "If rotating words serve the current direction, keep a steady lead and stable whole-word slot independent of scenes, with SSR/no-JS/reduced-motion fallbacks and managed timers. A delegated redesign can choose accessible pause/stop controls or static/manual behavior; there is no portfolio pause/play veto. Respect explicit current site constraints and report unresolved WCAG 2.2.2 gaps. Whole-word rotation is not magnetic letter hover.",
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
      "text": "Verify desktop, 320/390px, 200% zoom, composition, H1/CTA/current controls. Test selected media/motion clocks, reduced motion, lifecycle and WCAG 2.2.2 stopping. Bind build; live smoke needs authority. Disclose gaps; no inherited control defaults.",
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
      "text": "When photography is selected, compose source, crop, type and overlay against the current direction. Verify meaningful focal content, contrast, authentic logo/real CTAs and every active scene on desktop/mobile. Reject unintended scene loss, not deliberate gradients or grading. No inherited scrim, palette or section quota; nonphotographic designs use their own composition checks.",
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
