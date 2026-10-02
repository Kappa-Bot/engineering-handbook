---
id: brand-melodiq-systems-design
kind: brand-contract
status: active
owner: brand-owner
version: "1.2"
applies_to:
  - melodiq-corporate-surfaces
sources:
  - src-awesome-design-md
  - src-w3c-wcag-22
last_verified: 2026-10-02
review_due: 2027-04-02
---

# MelodIQ Systems — Design DNA

> Precise systems. A restrained melodic gesture. Quiet confidence.

## 0. Authority, scope and evidence

This is the single current contract for **MelodIQ Systems corporate identity**, deliberately centralized at the owner's request. It is **not** a portfolio-wide art direction, a new universal Standard, or permission to recolor customer products. Preserve `pat-design-context-layering` and `std-ui-ux-quality-baseline`.

Applies to the corporate website, corporate presentations, company-brand communications, logo exports and profile imagery. ChurchOS, other verticals, Platform Admin and tenant interfaces retain their own design authority. A discreet company endorsement does not import this entire theme. Adoption in an existing product requires an explicit product-owned decision.

Three evidence classes must remain distinct:

| Class | Meaning | Examples |
|---|---|---|
| Locked identity | Owner-approved direction; do not reinterpret | Name, violet/lilac family, selected M–Q mark, melodic Q tail, restrained character |
| Recorded artifact | Observed bytes, not proof of production quality | Frozen v2 PNGs, archive dimensions and checksums, archived MAIN email styles |
| Implementation default | Precise starting contract for new corporate surfaces; not a measured or shipped UI | Type scale, control geometry, layout, motion and export acceptance budgets below |

New implementation defaults need rendered acceptance at first use. They do not retroactively certify mockups. `tokens.json` owns the numerical token values; this document owns intent, scope and acceptance rules. If prose, tokens and assets conflict, stop the affected change and reconcile them together rather than selecting whichever is convenient.

**Reference method:** use the decision structure described by `src-awesome-design-md`—atmosphere, semantic color, typography, components, layout, depth, responsive behavior and agent guidance. Do not import another company's skin or claim an official certification. Existing evaluation: `ref-external-design-intelligence-corpus`.

## 1. Canonical materials and migration

- [Numerical tokens](tokens.json): brand values and explicitly scoped implementation defaults.
- [Frozen v2 inventory](assets.v2.json): all 57 archive entries, dimensions where applicable, byte sizes and SHA-256 checksums.
- [Vector master v1 evidence](assets.vector.v1.json): deterministic reconstruction metadata, QA metrics, promotion state and hashes.
- [Original v2 archive](https://drive.google.com/file/d/12tFceHH6O6e31J8hbMBss1C4d9gya3u3/view): restricted Drive access. It contains contact/email material; do not publish the whole ZIP or broaden its permissions.
- Strongest visual reference inside that archive: `assets/reference/melodiq-systems-accepted-brand-board.png`. Inspect the actual image; descriptions are insufficient for reconstructing the mark.

The old archive's `docs/DESIGN.md` and `handbook/ENGINEERING_HANDBOOK_PATCH.md` are historical snapshots, not competing active authorities. The proposed handbook patch is superseded by this integration. Preserve the v2 archive byte-for-byte; future distributions must pin the Handbook revision and link to this contract.

If a tool cannot access the restricted archive, request authorized asset access or use an already verified local copy. Never synthesize a substitute logo, expose private material to a public image host, or assume a chat sandbox URL is durable storage.

## 2. Visual thesis: translate adjectives into decisions

| Intent | Required visual consequence | Reject |
|---|---|---|
| Smooth | Tangentially continuous curves, consistent optical weight, restrained easing | Kinks, pointed mechanical joins, abrupt velocity changes |
| Elegant | Clear hierarchy, ample but purposeful space, few simultaneous effects | Chrome, bevels, glossy mockups, decorative clutter |
| Technological | Precise alignment, legible data, dependable interaction states | Robot stock art, generic circuit textures, gratuitous code ornaments |
| Systems | Repeated rules and clear relationships between elements | A network of random dots, linked-loop tangles, arbitrary variation |
| Melodic | One fluid wave gesture in the Q tail; rhythm through spacing | Literal notes, headphones, equalizers or musical wallpaper added to explain the name |
| Distinctive | The approved M–Q silhouette plus disciplined typography | An infinity logo, an A, a literal fish, a generic AI swoosh |

Technology comes from structure, not ornament. Melody comes from continuity and rhythm, not symbols piled onto the logo. The earlier subtle fish association is not the leading identity and must not be made explicit. Do not add religious symbols to this corporate mark.

## 3. Name, wordmark and commercial truth

Write **MelodIQ Systems** in copy, alt text, metadata and filenames that contain a human-readable name. Keep `MelodIQ` casing; use `melodiqsystems.com` for the owner-reported purchased domain. Purchase does not establish that a website or mailbox is live.

`Systems` remains secondary, never equally heavy or larger than `MelodIQ`. Preserve its existing lockup spacing; do not letter-space normal body copy to imitate the wordmark.

The generated wordmark has a stylized dotted vertical glyph. Do not silently redraw that glyph, infer the logo's exact font from its appearance, or propagate `MelodiQ` as the textual brand name. Preserve approved artwork until a reviewed vector reconstruction exists.

No corporate mailbox, NIF, registered-company suffix, legal clearance, security certification, customer count or performance result is established by this document. Domain ownership and identity approval do not establish registration of the company or trademark.

## 4. Symbol geometry — the non-negotiable visual fingerprint

Use the approved asset, not a generative reinterpretation. The recognizable structure is:

1. A near-vertical left stem anchors the M gesture. Keep it upright; making it a slanted apex changes the reading into an A.
2. The main band descends diagonally into a broad, smooth lower sweep. It is a controlled ribbon, not a folded 3D strip.
3. The upper-right open arc supplies the Q bowl. Its opening and white separation from the diagonal remain visible. Do not close the silhouette into a continuous infinity loop.
4. The Q tail is a **single restrained wave**: it emerges inside the bowl, crosses toward the lower right and ends with a gently lifted, tapered terminal. Preserve the melodic curve; neither a straight slash nor a detached dot is an acceptable replacement.
5. The asymmetric letters are **optically balanced**, not mirrored. Do not enforce mathematical symmetry at the expense of reading M–Q.

### Placement and scaling

Let `H` be the visible symbol's height, excluding raster canvas padding. Clear space is at least `0.25 × H` on every side, measured from visible ink. Preserve the source aspect ratio, use proportional containment, and never stretch a header export to a different ratio. Canvas dimensions in the inventory are not geometric construction measurements.

Initial corporate-use floors: symbol 24 CSS px visible height; horizontal lockup 180 CSS px total width. A 16 px favicon is a separately reviewed micro asset, not proof that every lockup works at 16 px. At small sizes, use symbol only and omit `Systems`; do not invent a simplified drawing without approval.

For a square avatar, center the visible symbol optically, constrain its width to at most 68% of the side, and keep every visible point within a radius of 40% of the canvas side from its center. Test a circular crop. Background fills the square; do not add baked rounded transparent corners merely because one platform shows them.

### Vector master v1 — canonical

The deterministic vector reconstruction in the v3 brand pack is now the **canonical production master** after owner visual acceptance. It contains editable SVG paths and vector gradients with **no embedded raster logo** and **no external font dependency in the symbol SVG**. The archived raster reference remains historical evidence, not the production source.

Recorded symbol QA at the approved reference scale:
- silhouette IoU: **0.988304**
- mean symmetric edge distance: **0.2133 px**
- embedded raster: **false**
- external font dependency: **false**
- source/promotion evidence: [assets.vector.v1.json](assets.vector.v1.json)

The reconstruction method intentionally removes raster stair-stepping without generative redesign: Gaussian edge smoothing at sigma 0.5, saturation contour level 0.16, editable path geometry and vector gradient fills. This is an implementation record, not permission to reshape the M–Q mark.

The outlined horizontal and vertical wordmark reconstructions in the v3 pack are also **canonical** after owner visual acceptance. Use those vector lockups for new production exports. Keep the archived raster wordmark only as historical reference and regression evidence.

Ongoing regression review compares the vector master against the approved reference at 1× and 4× and on paper, white, ink and deep violet. Inspect the near-vertical left stem, Q opening, white separation, lower sweep, melodic Q-tail inflection and tapered terminal. Review actual 16/24/32/48 px symbol exports and a circular avatar crop. The recorded QA metrics support the visual review; neither replaces the other.

## 5. Color system and contrast

The five identity anchors are locked. Supporting interface neutrals are implementation defaults, not additional brand identities.

| Token | Value | Role |
|---|---|---|
| `primary` | `#6D28D9` | Primary corporate accent and light-surface action |
| `lilac` | `#C4B5FD` | Soft support, logo highlight, dark-surface link/accent |
| `deep` | `#2E1065` | Deep brand backdrop, dark secondary surface |
| `ink` | `#1F1B2E` | Default text and dark base |
| `paper` | `#FAF8FF` | Light base |
| `white` | `#FFFFFF` | Raised light surface and primary-button text |
| `muted` | `#625A70` | Secondary text on light surfaces |
| `border` | `#E5DEF2` | Quiet nonessential separators; not the sole control boundary |
| `hover` | `#5B21B6` | Light primary-action hover |

Use semantic light/dark mappings from `tokens.json`, not global color replacements. Do not assume primary violet is a readable text color on every dark surface. Error, warning and success remain established semantic states with text/icon differentiation; do not recolor all status information purple.

Calculated from the opaque sRGB values: ink/paper **15.89:1**, primary/paper **6.74:1**, muted/paper **6.20:1**, lilac/deep **8.25:1**, lilac/paper **1.75:1**. Rounded figures are explanatory; evaluate unrounded ratios for acceptance. Lilac on paper is decorative, not normal reading text.

Apply the existing WCAG baseline (`src-w3c-wcag-22`): normal text 4.5:1, qualifying large text 3:1, essential UI boundaries and indicators 3:1 where applicable. Logo exceptions do not extend to navigation, body copy, tagline text or buttons. Contrast on a gradient is evaluated at the weakest relevant background location.

### Gradient and motif budget

Preserve the gradient inside the approved logo. On a corporate page, allow at most one prominent decorative wave/gradient field per viewport; navigation, controls and reading surfaces remain quiet. Do not stack a mesh gradient, glow, glass panel and particle field to create identity. Approved presentation artwork is reference material, not permission to reproduce its decoration in every component.

No ambient looping logo animation, chromatic rainbow drift, halo around text, faux light-source reflections or gradient-filled body text. Violet/lilac may be expressive in a cover or wallpaper without becoming the default dashboard treatment.

## 6. Typography and spacing

Display/headings: **Manrope**. Body/UI: **Inter**. Fallback: `system-ui, sans-serif`. Email: Arial/Helvetica. These are layout choices; the logo wordmark remains artwork. Obtain font assets through their official distribution and applicable license; font files are not included in this handbook integration.

At a 16 px root, the initial scale is:

| Role | Mobile → desktop | Weight | Line height | Tracking |
|---|---|---:|---:|---:|
| Display | 36 → 56 px | 600 | 1.08 | -0.025em |
| H1 | 32 → 44 px | 600 | 1.15 | -0.02em |
| H2 | 24 → 32 px | 600 | 1.20 | -0.015em |
| H3 | 18 → 20 px | 600 | 1.30 | 0 |
| Body | 16 px | 400 | 1.60 | 0 |
| Secondary | 14 px | 400 | 1.50 | 0 |
| Caption | 12 px | 400 | 1.40 | 0 |
| Label | 14 px | 500 | 1.30 | 0 |

Implement type in rem, allow zoom, and prefer fluid scaling between these endpoints. Do not clip accents, descenders, focus rings or validation text to satisfy a fixed-height composition. Body lines target no more than 68ch. Tabular numeric alignment is reserved for comparable data, not all prose.

Spacing scale: **4, 8, 12, 16, 24, 32, 48, 64, 96 px**. Page container: 75rem maximum, centered; gutters 20/32/48 px for small/medium/large. Section spacing defaults to 48 px mobile and 80 px desktop; the section rhythm is distinct from component padding. A one-pixel optical adjustment is allowed when documented, not a new token family.

## 7. Components, density and states

Corporate surface defaults only; validated product controls keep their existing contracts.

| Element | Geometry and behavior |
|---|---|
| Primary button | 44 px high, 8 px radius, solid accent, explicit verb; only one dominant action in a local action group |
| Secondary button | Same hit area; quiet surface or text treatment; no competing gradient |
| Text link | Identifiable beyond color, visible keyboard focus; never a decorative pill by default |
| Input/select | 44 px minimum control height, persistent visible label, identifiable boundary, hint/error outside the value |
| Card/panel | 12 px radius, 16–24 px content padding; use only for meaningful grouping, never a card inside a card for decoration |
| Navigation | Stable alignment and clear active state; logo does not dominate or obscure the current task |
| Table/list | 44 px default rows; 36 px compact rows only on explicitly dense pointer-led surfaces without sacrificing target/accessibility requirements |
| Dialog/popover | 12 px radius, purposeful elevation, dismissal and focus behavior inherited from the existing accessible primitive |

Specify default, hover, focus-visible, active, disabled, loading, empty, error and success states where relevant. Never convey status solely through violet opacity. Loading does not erase context; empty states explain the next action; errors preserve entered data; success is reported only after the operation succeeds. No fake KPI cards, invented activity or progress bars unrelated to actual progress.

Resting surfaces have no shadow by default. One overlay shadow token is available: `0 8px 24px rgba(31,27,46,0.10)`. Separate surfaces with spacing and hierarchy before adding more borders or shadow layers. A decorative pale border is not an accessible interactive boundary by itself.

## 8. Layout, responsive behavior and motion

Marketing may use one expressive opening section followed by varied evidence-led composition. Repeated corporate operations prefer direct tables, lists and grouped forms. Never copy the brand presentation board into a website as a wall of identical centered cards.

Layout shifts at 768 and 1200 px are starting points, not device assumptions. Reflow according to actual content. Review at 320, 390, 768, 1280 and 1440 CSS px, plus 200% zoom and the relevant WCAG reflow case. No hidden horizontal clipping. Tabular overflow must be contained, labelled and usable; navigation and primary actions remain reachable without hover.

Use a 44 × 44 px corporate touch-target target; the existing accessibility standard determines any legitimate exceptions. On mobile, stack content in reading order, reduce decorative volume before shrinking text and preserve action priority. Do not create a different logo for each breakpoint.

Motion communicates feedback or orientation: 120 ms feedback, 180 ms disclosure, at most 240 ms entrance; `cubic-bezier(0.22, 1, 0.36, 1)`, at most 8 px travel. Animate only the necessary property, never `transition: all`. Frequent operations should not wait for decoration. Respect reduced-motion preferences by removing nonessential entrance/transform effects. No animation is required just to express “melody”.

## 9. Email MAIN — preserve the owner's correction

The approved email is a separate canonical communication artifact. Locate the live Gmail draft by the exact subject **`[MAIN] MelodIQ Systems · Plantilla de correo y firma`** through an authorized connector before editing or copying it. Do not send or overwrite the master when producing a message.

The verified archive of MAIN records these dimensions:

| Block | Font / line height | Important spacing |
|---|---|---|
| Message body | 14 / 22.4 px | 14 px paragraph gap |
| Name | 17 / 23 px | 5 px bottom padding |
| Founder & CEO line | 14 / 21 px | 3 px bottom padding |
| Cybersecurity / IAM | 13 / 20 px | 12 px bottom padding |
| Contacts | 12 / 20 px | Preserve existing links and spacing |
| **Internal footer only** | **10 / 12 px** | 14 px above, 8 px inner top, 3 px paragraph gap, 1 px lilac rule |

**“Compact the footer” never means compact the message or signature.** Apply styles locally to `MELODIQ_INTERNAL_FOOTER_START/END`; do not change inherited body typography. The internal footer contains reuse notes, not outgoing copy: exclude it when sending. Preserve the `MELODIQ_EMAIL_*` and `MELODIQ_SIGNATURE_*` boundaries.

The v2 `email/final-signature.html` is a later design derivative, not a replacement for Gmail MAIN. Its “final” filename does not establish approval or client compatibility; do not let it silently shrink the signature, remove LinkedIn, introduce a new tagline or imply a live corporate mailbox. Embedded data-URI preview HTML is not evidence of correct rendering in Gmail/Outlook. Select transport and test actual receiving clients before any future adoption.

No personal contact information is copied into this public handbook. Obtain it from the authorized master. This integration does not install a Google profile photo or change Gmail settings.

## 10. Communication DNA

Spanish (Spain) by default, direct and courteous. Lead with the user's task, the concrete benefit and its conditions. Use English role titles where already approved. Define technical acronyms when the audience needs it; use precise IAM terminology with specialists.

Prefer: “Conectamos tus herramientas para reducir tareas manuales.” Avoid: “Revolucionamos tu negocio con soluciones disruptivas de IA.” Do not imply measured savings without evidence. Avoid majestic promises, artificial urgency, fabricated testimonials, and speaking as a large team when that is not established.

“Technology meets human potential”, “Systems in harmony” and similar phrases in image explorations are reference copy, not all simultaneously approved master taglines. A new commercial surface must use one deliberate, accurate proposition, not automatically repeat generated slogans.

## 11. Asset readiness — visual approval is not a technical certification

The original archive is intentionally preserved, including its defects. Recorded limitations:

- Primary logo exports are **raster crops**: symbol 510 × 310 and horizontal 610 × 210 px. These canvas dimensions include padding. Upscaling does not create vector detail.
- The “transparent” crop workflow retained background residue/halos. Inspect on dark and saturated backgrounds before release; filenames and an RGBA mode do not prove clean transparency.
- The LinkedIn export has visible lateral fill strips. Several alternate-size assets were resized independently in width and height; a matching output dimension does not prove preserved logo proportions.
- Deck covers contain raster placeholder text. They are not editable presentation masters.
- The deterministic SVG symbol master and outlined vector lockups in the v3 pack are canonical and recorded in `assets.vector.v1.json`. No native AI/Figma master, CMYK print proof or tested email-client suite is present. No font binaries are distributed here.

Existing boards and wallpapers can serve as approved direction. Do not promote a file to production-ready until it passes the relevant gate below. Fixing export defects should preserve the design, not trigger another round of unrelated logo concepts.

## 12. Acceptance gates and change control

For each shipped asset or surface, record its source revision, file hash, target context and evidence. No threshold substitutes for visual judgment.

| Gate | Required evidence |
|---|---|
| Identity | Correct name, selected M–Q silhouette, single melodic tail; no A/infinity/fish reinterpretation |
| Geometry | Proportional scale, correct clear space, no clipped wave; compare source/output aspect ratios before crop |
| Transparency | Review on white, paper, ink and saturated background; outside-art alpha is clean, no rectangular haze or edge fringe |
| Small size | Actual 16/24/32/48 px icon review and circular-avatar crop; reject a blurred reduction |
| Type/content | Correct copy and casing, no baked placeholders presented as an editable template, no invented claims |
| Accessibility | Relevant contrast, keyboard/focus, zoom, reflow and reduced-motion tests; states remain distinguishable |
| Email | Only the internal footer is compact; message/signature preserved; internal notes excluded; receiving-client evidence before transport claims |
| Package | Hashes match, relative paths resolve, required assets included, dimensions accurate, no private contact material in public publication |
| Adoption | Distinguish generated asset, committed contract, installed tool context, deployed surface and human acceptance |

Before changing the logo or a locked identity value, obtain owner visual approval. Numerical corporate defaults may evolve through scoped rendered review; update this document and tokens in the same change. Never overwrite the frozen v2 inventory or modify compiled Handbook files manually.

Consumer repositories should keep a short local pointer to this document and the chosen Handbook revision, plus their actual surface exceptions. Load it only for MelodIQ-branded work. Do not paste the entire design corpus into permanent agent instructions or globally install this palette into every vertical.

### Compact agent brief

> Read this contract, tokens and the required v2 reference asset. Preserve the approved M–Q logo with its single melodic Q wave. Use violet/lilac with quiet neutrals, Manrope/Inter for layout and purposeful hierarchy. Apply only to MelodIQ corporate surfaces. Do not generate a substitute logo or treat archive derivatives as production masters. Preserve Gmail MAIN; compact only its internal footer. Report the exact asset and surface actually verified.
