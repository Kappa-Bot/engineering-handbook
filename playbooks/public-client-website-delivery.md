---
id: pb-public-client-website-delivery
kind: playbook
status: active
owner: engineering
version: "0.4"
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
last_verified: 2026-11-16
review_due: 2027-02-16
---

# Public Client Website: Design-to-Launch Playbook

## Intent and boundaries

Deliver a client-specific commercial experience with a clear proposition, recognizable direction, useful service exploration, truthful content, working contact actions and an actually verified result. [UI/UX Quality Baseline §1](../standards/ui-ux-quality-baseline.md#1-product-specific-design-and-reconstruction) and `pb-frontend-quality-review` own diagnosis, direction, nine-pass reconstruction and acceptance. This is the **delivery orchestration playbook**; the linked Patterns supply optional mechanics, not a required component list or portfolio skin.

Apply this to independent commercial/service websites, public marketing pages and intentionally public Vertical sites. **Do not route authenticated operations consoles, patient/admin UI, internal tools or a routine webhook change here.** Begin with the target repository's `AGENTS.md`, `DESIGN.md`, legal/content decisions and existing architecture. A simpler one-page offer may need no gallery, rotating heading, autoplay or testimonial strip at all.

**Historical implementation donor:** [Kappa-Bot/pinturas-garcia](https://github.com/Kappa-Bot/pinturas-garcia), validated reference commit `ea4f3ac408a5aa4ee52394bbaf0f8a0289691304`, hosted as a public **noindex demo** at `https://pinturas-garcia.vercel.app/` on 2026-11-02. This is prior implementation evidence, not the canonical aesthetic for new clients or a promise of current deployment health. Recheck live status before using it; do not copy its business, wording, palette, photos or section count.

**Supersession, 2026-11-16:** a donor-derived photographic hero, transparent header, rotating headline, gallery/marquee bundle and one-family typography are no longer delivery defaults. Select or replace them through the current direction. Previously approved aesthetics can be superseded within authorized redesign; current factual, rights, privacy and release constraints remain in force.

## 1. Start from the conversion story, not a component list

Reuse the approved commercial brief through `pb-marketing-context-and-content` before writing CSS or image prompts. Its audience, offer, proof, voice and primary action are the single commercial source; use `tpl-product-marketing-context` only to fill material gaps, not to create a parallel brief. Add these delivery-specific decisions to the existing record:

| Decision | Evidence the implementing repo must supply |
| --- | --- |
| Design context | Current brief, authentic brand assets, `DESIGN.md` and rendered diagnosis; chosen or superseded visual decisions under the current direction, not inherited typography/colors |
| First-screen job | Intelligible offer and useful supporting proof, primary action and any genuinely useful secondary action |
| Conversion | Phone, messaging destination, contact hours, privacy/consent and which lead fields are useful |
| Site truth mode | `demo` vs `real`, image provenance, review source, indexability, approval owner |
| Technical owner | Existing code/repo, build, hosting/project ID, environment, DNS/domain, release gates |

Build the narrative around visitor decisions, not a fixed section sequence. Offer, services, proof, process, contact and legal information may be grouped or ordered differently; a hero/gallery/reviews chain is one possible composition, not a default. In an authorized redesign, remove redundant sections and reconstruct their hierarchy while preserving required facts and working destinations. Reject generic "somos líderes" filler and ornamental sections with no user purpose.

## 2. Hero, prompt craft and media direction

Select typography-led, product-led, photographic or another fitting first-view composition from the current direction. Use `pat-public-marketing-hero-motion` only for the mechanics selected. A full-viewport photo, multiple scenes, transparent header and entrance choreography are not required. Where photography explains the service, prefer useful rights-cleared source material; generate illustrative media only when it serves the brief, its cost is authorized and its provenance is truthful. Without useful imagery, deliver a complete composition rather than an empty visual slot.

**Image-prompt brief per scene (reusable schema, not a shared text prompt):**

- **Subject/action:** the actual service, material, spatial context and accurate tools/working practice—not a random attractive person or misleading brand/logo.
- **Composition:** lens/camera height, foreground/background layering, where the copy and controls need negative space, subject gaze/action and hero focal point.
- **Art direction:** site-specific palette, natural light, tactile surface texture, photographic realism, amount of contrast, what clichés to avoid.
- **Responsive outputs:** derive aspect ratios and focal placement from the selected desktop/mobile composition. A landscape plus recomposed portrait pair may help; 9:16 is not a mandatory mobile format. Do not assume a center-cropped desktop image works on mobile.
- **Truth/rights:** mark generated/illustrative artwork in the media manifest and do not imply a real client job or verifiable team portrait. Get approval before publishing.
- **Performance:** optimize AVIF/WebP variants, intrinsic dimensions, responsive `picture`/`srcset`, LCP priority of the first hero image, lazy-load noncritical media, useful alt text without keyword stuffing.

### Reusable prompt frames (fill with local evidence)

Use these as **input structure only when photographic scenes are selected**, not as universal styling or a requirement to generate images. Adapt the frame, number of actions and aspect ratios to the direction. Where several scenes are useful, vary subject, location and shot scale rather than creating clones.

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

For **header copy prompts** (text, not background images), request a concise factual service headline, useful location/scope information, short labels matching the *actual* actions and a hierarchy based on visitor intent. Do not impose a universal word count, messaging channel or keyword quota. Reject copy that could fit any competitor; if rotating words are selected, every alternative must leave the proposition true.

**Headline motion:** select it only when it materially helps the message. If used, keep the lead phrase and keyword slot stable, independent of any scene changes; derive cadence from reading needs and test the stopping/lifecycle behavior. Do not add photo zoom or content entrances merely because a donor has them. A real H1 and CTA must work immediately before JS.

**Hero controls:** use `pat-public-marketing-hero-motion` §2.1 for scoped control decisions, accessibility, timer independence and lifecycle. A delegated design can select accessible stopping controls or static/manual behavior without another aesthetic approval for each control. Respect explicit current site restrictions; unresolved accessibility conflicts are not `PASS`. Agurto's historical five-second/no-pause decision is not a portfolio rule or permission to change that site. Do not add autoplay simply to showcase animation.

### Image integrity, information density and route hygiene

Treat the current visual direction and any applicable reference as **rendered-state evidence**, not a reason to preserve a failed composition. For a selected photographic hero, compare actual desktop/mobile output with source assets and apply the photo-fidelity gate in `pat-public-marketing-hero-motion`. For another composition, verify its own content and hierarchy rather than forcing a photograph. If the header overlays media, authentic logo assets, navigation and contact prompts must remain readable over every scene.

A public page should earn every section by answering a visitor question or supporting a concrete action. Remove repeated maps, duplicated location blocks, generic pseudo-benefits, decorative badges, empty panels, vague adjectives, invented clinician/service claims and technical jargon. Keep location information discoverable; a bounded visual fix must not silently change route ownership, while an authorized wider redesign can document and implement a better hierarchy with working destinations. Choose spacing and palette for the current direction rather than inheriting a white template or a previous client's colors. Verify actual computed colors and contrast rather than trusting variables alone.

**Typography roles and navigation fidelity:** define the type roles that serve the direction: display headings, reading text, controls and data may deliberately use different families or weights. Do not force every element to inherit the hero family or preserve a weak pairing merely because it was approved before. Historic CSS `font` shorthands and fallback loading must not silently substitute unrelated fonts. Verify computed families **against the chosen role map**, weights and wrapping on the homepage and representative inner pages, desktop/mobile/200% zoom. Group content by visitor task rather than donor navigation; preserve or intentionally migrate established deep links and localized variants with clear routes to nested content.

For a useful health/practical blog, offer short answerable topics (habits, stepwise techniques, signs to discuss with a professional), relevant original images or verified rights-cleared media, honest provenance and readable article text. Link to appropriate primary sources for material recommendations; no stock AI prose, invented case histories, placebo 'tips', made-up authors/dates, unconfirmed claims or advice pretending to diagnose. Check every locale, image request, article expansion/link and reduced-motion mode. **A test passing is not permission to publish a visibly empty or generic page.**

## 3. Header and CTA prompts

Treat the header as a functional interaction system, not an isolated logo row:

1. Choose a header suited to the composition. A solid header is complete; a transparent overlay is optional and needs adequate logo/menu/text contrast across every image and scroll state. Protect content from overlap and preserve a readable fallback; glass is not required.
2. Desktop navigation should offer truthful, short links to the important destinations and clear **call, WhatsApp or quote actions** where those are real approved channels. Place them according to the current hierarchy, not an inherited right-edge recipe. Mobile should expose the primary next action and navigation without obscuring content or identity.
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

**Publish, when authorized:** preserve repository history and source provenance; run lint/build/test and verify the configured repository-to-host deployment path, correct project/team, environment and domain ownership, production-ready status, access matching intent and exact deployed SHA. Configure deployment automation only within the authorized hosting scope. Never change DNS, spend money or disable protection for an unrelated live client site on assumption. Demo/preview: `noindex` HTML and response headers, no analytics/review schema that misrepresents the fixture. Real production: apply `std-public-web-discoverability-baseline` and `pb-public-web-discoverability-launch`, and only enable indexing with a real approved domain/content/legal posture. A design task or Handbook revision alone does not authorize a live release.

## 7. Evidence before saying "finished"

Exercise only the selected mechanics; mark absent carousel, gallery, comparator or marquee cases inapplicable rather than adding those components to satisfy a checklist.

- **Design fit:** compare real screenshots at desktop (~1440px), 768px, 390px and 320px against the current direction and diagnosed problems; include short heights, 200% zoom, meaningful content below fold, **computed typography matching the chosen role map**, and media focal points where used. Check no blank images, overlapping fixed header or horizontal page overflow. Cosmetic change alone cannot close a systemic composition/content finding.
- **Behavior:** navigation anchors/nested guide links and preserved deep links, menu/focus/Escape, call/WhatsApp destinations, required-form validation and prefilled message, hero arrow/dot/pause/swipe/keyboard/independent word timing, gallery every panel, **handle-only comparator drag vs passive hover, real touch drag and keyboard**, reviews readability and pause, reduced motion and hidden-tab behavior.
- **Quality:** page loading/LCP/CLS/INP budgets where measured, alt text, semantics, keyboard focus, section headings, image rights, legal/privacy/robots, broken links and console errors. Respect `pb-frontend-quality-review`, `std-ui-ux-quality-baseline` and `pat-visual-evidence-integrity`.
- **Deployment, if in scope:** exact commit and linked repo, build result, host READY/access, live page plus mobile browser smoke, final URLs and configured deploy-path confirmation. Distinguish `PASS`, `FAIL`, `NOT RUN` and inapplicable checks; a successful build alone does not certify real interactions or a live release.

Finish with a concise handoff: URL, SHA, what changed, demo-vs-real limitations, observed tests and anything needing client confirmation. If the site lacks authentic source material or real numbers, say so; do not silently make them up.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "public-client-website-brief",
      "type": "decision-question",
      "force": "must",
      "text": "For a public client website, apply std-ui-ux-quality-baseline section 1 and pb-frontend-quality-review to the current brief via pb-marketing-context-and-content. Verify identity/offer/proof, real CTA, demo truth, rights and hosting scope. Choose composition and optional media/gallery/reviews from visitor needs; replace inadequate inherited aesthetics within authorized redesign. Keep missing facts explicit and do not clone another client's visuals.",
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
      "text": "Implement the chosen product-specific composition, accurate offer, deliberate typography roles, real contact actions, working validated quote flow and legal/SEO scope. Photography, transparent headers, rotating words, galleries and review marquees are optional. Use the linked patterns only for selected mechanics; keep fixtures explicit and never fabricate client jobs, testimonials or Google reviews. Supersede changed visual decisions coherently.",
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
      "text": "Before handoff, verify the current direction and diagnosed findings at 1440/768/390/320px and zoom, header/navigation, typography role map, selected hero/gallery/review mechanics, keyboard/touch/reduced motion, quote validation, media truth, legal/indexability and build/tests. If publication is authorized, verify exact deployed SHA, host state and live desktop/mobile smoke. Report PASS/FAIL/NOT RUN and inapplicable checks honestly.",
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
      "text": "Define intentional typography roles from the current direction; headings, reading copy, controls and data may use different families. Replace weak inherited choices and prevent accidental CSS/font fallbacks. Organize navigation by visitor tasks, preserve or deliberately migrate localized deep links, and verify computed role families, wrapping and readability on representative inner pages and 200% zoom.",
      "source": "pb-public-client-website-delivery",
      "covers": ["accessibility", "compatibility", "hero-fidelity"],
      "activate_when": ["archetype:public-client-website"],
      "phase": ["implementation", "verification"],
      "priority": 79
    }
  ]
}
```
