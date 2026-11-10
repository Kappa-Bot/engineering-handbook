---
id: pb-public-client-website-delivery
kind: playbook
status: active
owner: engineering
version: "0.3"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - product-vertical-public-pages
  - demos
sources:
  - src-w3c-wcag-22
  - src-w3c-aria-apg
  - src-21st-minhxthanh-interactive-selector
  - src-21st-shadcnspace-testimonials-marquee
last_verified: 2026-11-09
review_due: 2027-02-09
---

# Public Client Website: Design-to-Launch Playbook

## Intent and boundaries

The reusable **Pinturas García quality bar** for the next public-facing client website: coherent visual storytelling, an excellent first viewport, useful service exploration, believable—but truthfully labeled—demo content, clear contact actions and an actually verified release. This is the **orchestration playbook**; individual interactions have **one** normative home in the Patterns below. Do not clone García's business, Spanish copy, palette, hero photos, number of sections or image prompt verbatim.

Apply this to independent commercial/service websites, public marketing pages and intentionally public Vertical sites. **Do not route authenticated operations consoles, patient/admin UI, internal tools or a routine webhook change here.** Begin with the target repository's `AGENTS.md`, `DESIGN.md`, legal/content decisions and existing architecture. A simpler one-page offer may need no gallery, rotating heading, autoplay or testimonial strip at all.

**Canonical implementation donor:** [Kappa-Bot/pinturas-garcia](https://github.com/Kappa-Bot/pinturas-garcia), validated reference commit `ea4f3ac408a5aa4ee52394bbaf0f8a0289691304`, hosted as a public **noindex demo** at `https://pinturas-garcia.vercel.app/` on 2026-11-02. This is prior implementation evidence, not a promise that the deployment is healthy at future dates; recheck live status before using it.

## 1. Start from the conversion story, not a component list

Reuse the approved commercial brief through `pb-marketing-context-and-content` before writing CSS or image prompts. Its audience, offer, proof, voice and primary action are the single commercial source; use `tpl-product-marketing-context` only to fill material gaps, not to create a parallel brief. Add these delivery-specific decisions to the existing record:

| Decision | Evidence the implementing repo must supply |
| --- | --- |
| Design context | Approved typography/colors, brand assets and local `DESIGN.md`; do not homogenize client identities |
| First-screen job | One intelligible headline, support claim, primary quote/contact CTA, secondary exploration CTA |
| Conversion | Phone, messaging destination, contact hours, privacy/consent and which lead fields are useful |
| Site truth mode | `demo` vs `real`, image provenance, review source, indexability, approval owner |
| Technical owner | Existing code/repo, build, hosting/project ID, environment, DNS/domain, release gates |

Build a coherent narrative: **hero → services/benefits → selective gallery or proof → process/trust → reviews if appropriate → contact/quote → legal/footer**. Change order to fit the business. Avoid repetition, generic "somos líderes" filler and ornamental sections with no user purpose.

## 2. Hero, prompt craft and media direction

Follow `pat-public-marketing-hero-motion`. For a photographic service business with distinctive visual scenes, a full-viewport photo can carry transparent-over-hero navigation, readable headline, human supporting copy, service CTAs and subtle entry choreography. Use 2–4 scenes **only** when each supports a different true service story; a single strong hero may be better.

**Image-prompt brief per scene (reusable schema, not a shared text prompt):**

- **Subject/action:** the actual service, material, spatial context and accurate tools/working practice—not a random attractive person or misleading brand/logo.
- **Composition:** lens/camera height, foreground/background layering, where the copy and controls need negative space, subject gaze/action and hero focal point.
- **Art direction:** site-specific palette, natural light, tactile surface texture, photographic realism, amount of contrast, what clichés to avoid.
- **Two outputs:** a deliberate landscape composition and an explicitly recomposed 9:16 portrait scene; do not assume a center-cropped desktop image works on mobile.
- **Truth/rights:** mark generated/illustrative artwork in the media manifest and do not imply a real client job or verifiable team portrait. Get approval before publishing.
- **Performance:** optimize AVIF/WebP variants, intrinsic dimensions, responsive `picture`/`srcset`, LCP priority of the first hero image, lazy-load noncritical media, useful alt text without keyword stuffing.

### Reusable prompt frames (fill with local evidence)

Use these as **input structure** for generating/recommissioning a hero/header background, not as universal visual styling. Supply one brief **per service scene**; explicitly vary subject, location and shot scale so the resulting slide set has a narrative rather than four clones.

```text
ESCENA DESKTOP · paisaje para hero/header
Cliente/sector: [marca real, servicio y zona aprobados].
Historia visual: [acción/material/espacio verdadero o claramente ilustrativo].
Fotografía editorial creíble: [plano, lente, ángulo, hora/luz, texturas,
dirección de arte según DESIGN.md].
Composición 16:9 / extra-wide: sujeto y herramientas a [lado], dejar [lado]
de espacio negativo real para [titular + subtítulo + dos CTAs].
Zona superior segura para logotipo, navegación y botón de contacto.
Contraste natural que admita texto superpuesto sin oscurecer todo el encuadre.
Evitar: letras incrustadas, marcas inventadas, manos/herramientas deformes,
uniformes/logotipos falsos, estética de stock genérica, prueba visual de
trabajos/clientes que no han existido. Sin marcas de agua falsas.

ESCENA MÓVIL · retrato 9:16 de la misma historia, recompuesta
Rediseñar el encuadre (no simple recorte del desktop), mantener el mismo
servicio/sujeto/material, con espacio seguro superior para la cabecera y
zona legible para H1, CTAs y controles; sujeto reconocible al ancho de 390px.
Mantener la dirección de arte, pero simplificar detalles periféricos.
```

For **header copy prompts** (text, not background images), request from the real brief: one factual ≤10-word service headline, a useful location/scope supporting sentence, short action labels matching the *actual* phone/WhatsApp endpoints, concise section names and four optional interchangeable grammatical hero keywords. Reject slogans that could fit any competitor; ensure each alternate word leaves the proposition true.

**Headline motion:** when grammatical, keep the lead phrase stable and rotate a whole keyword in its own clipped, layout-stable slot, independent of scene changes. An example cadence is scenes ~7.6s and words ~2.8s, **not** universal timing. Fade/zoom the photo softly; reveal title/support/CTAs once, rather than remounting the whole hero for every word. A real H1 and CTA must work before JS.

**Hero controls:** take the **exact controls approved for this specific client**, using `pat-public-marketing-hero-motion` §2.1 as the sole authority for playback UI, accessibility decision, timer independence and lifecycle. Do not inherit donor/demo pause buttons or assume autoplay authorizes an extra playback control. Agurto is the explicit five-second-autoplay/no-pause-button precedent. The accessibility stop-mechanism decision must be documented separately and never used to silently introduce a rejected control. Do not add autoplay simply to showcase animation.

### Image integrity, information density and route hygiene

Treat the owner's visual reference as **rendered-state evidence**. Before release, compare the delivered hero at desktop and portrait-mobile sizes with its source photographs. Reject pale directional gradients, photo-bleaching filters and decorative fades that make the source image illegible; follow the canonical photo-fidelity gate in `pat-public-marketing-hero-motion`. A transparent-at-top header, reversible logo treatment and contact prompts must remain readable over every scene.

A public page should earn every section by answering a visitor question or supporting a concrete action. Remove repeated maps, duplicated location blocks, generic pseudo-benefits, decorative badges, empty panels, vague adjectives, invented clinician/service claims and technical jargon that burdens readers. If a map has its own clearly discoverable directions page, don't silently duplicate it on the homepage; **follow the local owner's route decision**. Prioritize generous layout and a reasonable reading rhythm. Use the **consumer's actual approved palette** (including nonwhite surfaces and softened dark text if requested), never a universal white template or artificially black body copy. Verify actual computed colors and contrast rather than trusting variables alone.

**Typeface and navigation fidelity:** once the brand/owner selects the hero's actual type family, carry that **same family** through section headings, body copy, cards, menu and footer links, captions, controls and forms, unless the approved design explicitly defines a second role. Historic CSS `font` shorthands must not silently reintroduce Georgia/Times or another unrelated family. Verify computed families in the browser on the homepage **and at least two inner pages**, desktop/mobile/200% zoom; check font weights and wraps after overriding older rules. A content taxonomy should reflect the visitor's task: a first-visit checklist naturally belongs within a practical dental guide, not necessarily as another full top-level navigation item. Preserve established deep links and localized variants when changing visible labels; leave clear body links to nested content.

For a useful health/practical blog, offer short answerable topics (habits, stepwise techniques, signs to discuss with a professional), relevant original images or verified rights-cleared media, honest provenance and readable article text. Link to appropriate primary sources for material recommendations; no stock AI prose, invented case histories, placebo 'tips', made-up authors/dates, unconfirmed claims or advice pretending to diagnose. Check every locale, image request, article expansion/link and reduced-motion mode. **A test passing is not permission to publish a visibly empty or generic page.**

## 3. Header and CTA prompts

Treat the header as a functional interaction system, not an isolated logo row:

1. At the top of the hero, consider a transparent overlay with adequate logo/menu/text contrast; on sticky scroll use an opaque or glass-backed surface that remains legible across every image. Protect content from header overlap.
2. Desktop navigation should offer truthful, short anchors to the most important sections and clear **call and WhatsApp/quote actions** at the right edge when those are real approved channels. Mobile should prioritize the menu and one primary contact action without crushing the brand.
3. Use functional `tel:` and properly encoded `https://wa.me/<countrycode><number>` links. Do not put invented numbers in UI, claim a chat is already open, or send messages without a deliberate user action.
4. If a messaging CTA prepares a quote, write a short client-specific **prefill message** with service, city/zone, timescale and useful form values. Let the person review/edit it in WhatsApp. Do not quietly store personal data or invent a backend.
5. Test menu open/close against hero autoplay, scroll locking, backdrop, focus return, Escape, short viewports, 320px width and long translated labels. Focus/tap targets and high-contrast states matter as much as the screenshot.

## 4. Selectable service gallery

When photo-rich categories improve discovery, adopt `pat-public-service-gallery-selector`: expanding image panels on desktop, mobile horizontal scroll-snap plus details, accessible selection, actual category copy and specific mobile portrait assets. Four well-chosen panels are an effective **García variant**, not a universal quota. Use a straightforward grid if accessibility, content count or performance makes expansion unhelpful. Reference the original `@minhxthanh/interactive-selector` for interaction intent, and the checked García source for the local adaptation; verify licensing before reusing source.

For before/after comparisons, obey the **separate comparator contract** in `pat-public-service-gallery-selector` §5: only an actively dragged visible handle moves the divider; mouse hover must not move it. Provide touch and keyboard support, no hover resets and truthful labeling. A “Resultados” page can also feature several **single** conceptual photographs rather than force invented before/after pairs. Disclose that generated demo imagery does not depict actual patients or treatment outcomes.

## 5. Reviews, trust and demo truth

Consult `pat-public-client-reviews-marquee` for spacing, CSS-only animation, pause, mobile behavior, source attribution and review modes. One-row García-style or two-opposing-row neutral variants are valid; choose based on density and reading comfort.

- **Demo:** sample testimonials may exist **only when conspicuously labeled** `DEMO · OPINIONES FICTICIAS` above the section **and** `Reseña ficticia`/`Ejemplo` on each card. Use fictional initials/names, no faux verified customers, no fake aggregate, no fake Places links, no `Review`/`AggregateRating` JSON-LD, no Google branding that suggests Google supplied or authenticated the data. Keep demo/staging `noindex`.
- **Live client site:** replace fixtures with real authorized reviews and proper per-provider attribution. If genuine testimonials cannot be provided or verified, **omit the section** or use a truthful non-review trust module (process, warranties actually offered, contact, credentials).
- **Motion:** scrolling content needs an explicit usable pause control, pauses on hover/focus, is static for reduced motion and never blocks reading. Real source integrations require separate authorization, current policy verification and cost/privacy review.

Visual polish is not permission to fabricate social proof. The García demo’s original decorative review styling is a design precedent only; apply the stricter demo-safe trust contract above on new sites.

## 6. Lead flow and release

**Legal, consent and trust:** apply `std-public-website-legal-trust-baseline` for verified responsible-party details, sector-specific healthcare advertising, real third-party consent/revocation, privacy inventories, AI imagery and reviews. The present playbook owns the **delivery sequence and visual experience**; the Standard is the **only normative home** for these cross-client legal/consent gates. A noindex demo still requires truthful disclosures and safe third-party behavior.

**Quote/contact:** choose the few fields that materially help the business respond (service, location, contact, optional dimensions/details/timing). Label required fields, validate before launch, preserve entries and give clear errors. For a static demo, an explicit WhatsApp prefill is an honest working conversion; do not claim database delivery, email send or lead tracking that was not implemented. For production, follow the approved backend/CRM/consent/data retention design.

For measurement use `pb-conversion-measurement-and-experiments`: a prefill/contact click is channel intent, not a sent message, accepted form or received lead. If CRM handoff is in scope, use `pb-lead-qualification-and-handoff` and preserve the existing owner/stages. Neither playbook authorizes adding tracking or sending messages automatically.

**Publish:** preserve repository history and source provenance; run lint/build/test, set and verify GitHub-main-to-Vercel (or host) auto-deploy, correct project/team, environment and domain ownership, production-ready status, public/private access matching intent, and exact deployed SHA. Never change DNS, spend money or disable protection for an unrelated live client site on assumption. Demo/preview: `noindex` HTML and response headers, no analytics/review schema that misrepresents the fixture. Real production: apply `std-public-web-discoverability-baseline` and `pb-public-web-discoverability-launch`, and only enable indexing with a real approved domain/content/legal posture.

## 7. Evidence before saying "finished"

- **Design fidelity:** compare real screenshots at desktop (~1440px), 768px, 390px and 320px; include short heights, 200% zoom, meaningful content below fold, **hero/body/card/menu/form computed type-family equality**, and photo focal points. Check no blank images, overlapping fixed header or horizontal page overflow.
- **Behavior:** navigation anchors/nested guide links and preserved deep links, menu/focus/Escape, call/WhatsApp destinations, required-form validation and prefilled message, hero arrow/dot/pause/swipe/keyboard/independent word timing, gallery every panel, **handle-only comparator drag vs passive hover, real touch drag and keyboard**, reviews readability and pause, reduced motion and hidden-tab behavior.
- **Quality:** page loading/LCP/CLS/INP budgets where measured, alt text, semantics, keyboard focus, section headings, image rights, legal/privacy/robots, broken links and console errors. Respect `pb-frontend-quality-review`, `std-ui-ux-quality-baseline` and `pat-visual-evidence-integrity`.
- **Deployment:** exact commit and linked repo, build result, host READY/public access, live page plus mobile browser smoke, final URLs and automatic deploy confirmation. Distinguish `PASS`, `FAIL` and `NOT RUN`; a successful build alone does not certify real interactions.

Finish with a concise handoff: URL, SHA, what changed, demo-vs-real limitations, observed tests and anything needing client confirmation. If the site lacks authentic source material or real numbers, say so; do not silently make them up.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "public-client-website-brief",
      "type": "decision-question",
      "force": "must",
      "text": "For a new public client website, use pb-public-client-website-delivery and the approved brief via pb-marketing-context-and-content: verify brand/offer/proof, real CTA, demo truth, images, domain/host and whether hero/gallery/reviews help. Keep missing facts explicit; do not clone another client's visuals.",
      "source": "pb-public-client-website-delivery",
      "covers": ["accessibility", "hero-fidelity", "compatibility", "commercial-truth"],
      "activate_when": ["archetype:public-client-website"],
      "phase": ["planning"],
      "priority": 85
    },
    {
      "id": "public-client-website-implementation",
      "type": "constraint",
      "force": "must",
      "text": "For a public client website, implement an accurate first-screen offer, site-specific desktop/mobile image prompts, transparent-to-readable header with real contact actions, intentional service/gallery and demo-safe reviews when useful, working validated quote flow and legal/SEO scope. Use canonical hero/gallery/reviews patterns; never fabricate project photos as client jobs or Google reviews.",
      "source": "pb-public-client-website-delivery",
      "covers": ["accessibility", "hero-fidelity", "compatibility", "commercial-truth"],
      "activate_when": ["archetype:public-client-website"],
      "phase": ["implementation"],
      "priority": 86
    },
    {
      "id": "public-client-website-live-handoff",
      "type": "verification",
      "force": "must",
      "text": "Before handoff of a public client site, inspect 1440/768/390/320px, header and menus, hero/body typography continuity, each hero/gallery/review interaction including passive hover vs captured handle drag, keyboard/touch/reduced motion, quote validation/contact links, media truth, legal/noindex or production SEO, build/tests, exact deployed SHA, host READY and live desktop/mobile smoke. Report PASS/FAIL/NOT RUN honestly.",
      "source": "pb-public-client-website-delivery",
      "covers": ["accessibility", "performance", "hero-fidelity", "compatibility", "commercial-truth"],
      "activate_when": ["archetype:public-client-website"],
      "phase": ["verification"],
      "priority": 92
    },
    {
      "id": "public-client-site-type-and-guide-hierarchy",
      "type": "pattern",
      "force": "must",
      "text": "Keep the owner's approved hero type family coherent across public headings, copy, navigation, cards, footer and forms, even if historic CSS shorthands specify a serif. Group practical first-visit information under the dental/consumer guide, preserve localized deep links, and keep primary navigation short and action-oriented. Verify computed type families on inner pages and 200% zoom.",
      "source": "pb-public-client-website-delivery",
      "covers": ["accessibility", "compatibility", "hero-fidelity"],
      "activate_when": ["archetype:public-client-website"],
      "phase": ["implementation", "verification"],
      "priority": 79
    }
  ]
}
```
