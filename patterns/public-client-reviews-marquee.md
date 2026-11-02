---
id: pat-public-client-reviews-marquee
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - product-vertical-public-pages
  - demos
sources:
  - src-21st-shadcnspace-testimonials-marquee
  - src-w3c-wcag-22
  - src-google-places-review-attribution
  - src-google-review-structured-data
last_verified: 2026-11-02
review_due: 2027-02-02
---

# Public Client Reviews Marquee: Google-Inspired, Demo-Safe

## Status, intent and authority

**Approved visual reference v1 (2026-11-02).** This Pattern records the MelodIQ interpretation of ShadcnSpace's exact `Testimonials Marquee` at `https://21st.dev/@shadcnspace/components/marquee-01`, accepted as the reusable reference for **future intentional public-site review/testimonial sections**. It is not an instruction to add reviews to every site, to deploy a section in an existing project, or to copy Google's product UI/trademarks. The 21st.dev page and live preview were inspected on 2026-11-02; the component source is gated behind a free account and its reuse license was not verified. The reference design below is an independent adaptation, not copied vendor source.

**Reproducibility target:** a new project using this Pattern should reproduce the approved neutral reference's **content hierarchy, geometry, timings, responsive states, accessibility behavior and demo/real trust boundary** without interpretation or prompt-only guesses. Browser font rasterization can differ; "100%" means the same defined component and verified interactions, **not a promise of pixel-identical antialiasing** on every OS. Any intentional difference is documented against this v1 reference and the consumer's `DESIGN.md`.

This is a reusable Pattern subordinate to `std-ui-ux-quality-baseline`, `std-public-web-discoverability-baseline`, `pat-capability-environment-integrity` and repo-local brand/tenant decisions. Read `pat-design-context-layering` before adapting to another vertical. Public customer identity, claims, actual Google Business Profile, release status and consent remain local.

## 1. Reference anatomy

The original donor has two rows of short cards, moving in opposite horizontal directions, with gradient fades at both edges. It has no Google rating grammar and repeats content heavily. **Our v1 implementation** has:

1. A quiet, centered section heading; a small uppercase visible label `VISTA DE DEMOSTRACIÓN · OPINIONES FICTICIAS` in demo mode; a concise explanatory line.
2. A visible `Pausar movimiento / Reanudar movimiento` control outside the moving region. The control reports its state accessibly and never overlays a card.
3. A horizontally clipped viewport with subtle fade masks. Desktop/tablet: two independently moving rows in opposite directions. At or below 600 CSS px: one row containing **all six unique** cards, not just the desktop top row.
4. Each review card contains: non-photographic initials avatar, display author, month/year, a small `Ejemplo` badge **only in demo mode**, a star row with a numeric accessible label, and review text.
5. No invented aggregate score, review count, Google profile link, Google "G", Google Maps logo, "verified" badge or "Ver en Google" CTA in demo mode.
6. Real-mode cards replace the demo label with accurate provider attribution, the real author's available profile/image and review URL. The real layout is visually similar but cannot silently claim Google verification.

### Fixed neutral reference tokens (desktop)

| Element | Reference v1 | Notes |
| --- | --- | --- |
| Section | background `#f7f7f4`; text `#303a36`; border `#e7e8e2` 1px; radius 18px; padding 35px top / 30px bottom | No pure black text. Consumer's local tokens override palette, not the hierarchy. |
| Intro | max-width 750px; horizontal padding 22px; bottom gap 25px; centered | Heading 23–32px, weight 640, line-height 1.2, letter-spacing -0.8px. |
| Intro label | 10px, weight 700, tracking 0.13em, color `#777e74` | Always visible in demo, never only on hover. |
| Supporting text | max-width 570px, 13px, line-height 1.6, color `#717a73` | States sample nature clearly. |
| Card | width 285px; min-height 174px; padding 16px 17px; radius 13px; border `#e8e9e5` 1px | White surface, shadow `0 3px 12px rgba(36,52,43,.035)`. |
| Horizontal gap | 12px between cards, 12px between duplicated groups | Keep group and track widths deterministic. |
| Vertical gap | 12px between tracks | No oversized empty section. |
| Avatar | 34x34px circle, initials 11px/700 | No generated fake real-person photos. Three muted alternating fills are sufficient. |
| Author | 12px/650; date 10px secondary | Display name/date remain readably associated with quote. |
| Stars | 15px; tracking 1px; default gold `#e6a82e`; empty `#d5d8d2` | Numeric accessible rating; do not rely on color alone. |
| Review | 12px; line-height 1.55; color `#4a514d`; max four lines | Fixture copy should naturally fit. Longer real reviews need a working complete-reading path. |
| Left / right fade | transparent 0%; opaque 7% to 93%; transparent 100% | Mask the viewport, not each card. |
| Track 1 | translateX(0) → translateX(-50%); 56s; linear, infinite | Top row moves left. |
| Track 2 | translateX(-50%) → translateX(0); 64s; linear, infinite | Bottom row moves right, deliberately slightly slower. |
| Typography | Inter, system-ui, -apple-system, sans-serif | Respect repo fonts if they match readability and measured reflow. |

**Mobile ≤600px:** section padding 26px top / 24px bottom; intro bottom gap 22px; one row only; cards 260px wide and minimum 176px tall; mask fades at 5% and 95%. At 320px and 200% zoom, no horizontal page overflow; only the intentional card viewport may overflow. Respect site light/dark modes by mapping neutral surface/text/border tokens rather than applying a global color filter.

### HTML structure contract

```text
section.review-marquee [aria-labelledby, data-mode="demo|real", data-enhanced, data-paused, data-static]
  header.review-marquee__intro
    visible demo disclaimer when mode=demo
    h2
    supporting description
    button [type=button, aria-pressed, "Pausar/Reanudar movimiento"]
  div.review-marquee__viewport
    div.review-marquee__track.review-marquee__track--desktop [row 1, left]
      div.review-marquee__group [original semantic cards]
      div.review-marquee__group [exact visual clones, aria-hidden/inert]
    div.review-marquee__track.review-marquee__track--desktop [row 2, right; hidden on mobile]
      div.review-marquee__group [other original semantic cards]
      div.review-marquee__group [exact visual clones, aria-hidden/inert]
    div.review-marquee__track.review-marquee__track--mobile [all six, hidden on desktop]
      div.review-marquee__group [six original semantic cards]
      div.review-marquee__group [exact visual clones, aria-hidden/inert]
```

Keep the **two copied groups identical** in order, widths, content and inter-card spacing; there is no extra flex `gap` between groups. Use the same group right padding as inter-card spacing. Then a 50% transform is a mathematically seamless loop; a mismatched gap produces the visible restart jump. Do not keep independently focusable links/buttons inside visually duplicated hidden copies.

## 2. Data contract and visual fixture

The view consumes explicit data. Do not generate new names/text on each render, invent a rating summary or default to sample data after a live-data error.

```ts
type ReviewMode = "demo" | "real";
type ReviewItem = {
  id: string;                       // stable and unique
  author: string;
  avatarInitials?: string;          // demo/local fallback
  avatarUrl?: string;               // only authorized and attributed
  publishedLabel: string;           // month/year or provider timestamp
  rating: 1 | 2 | 3 | 4 | 5;
  text: string;                     // no invented extra claims
  authorProfileUrl?: string;        // real mode only
  sourceReviewUrl?: string;         // real mode only
};
type ReviewsMarqueeProps = {
  mode: ReviewMode;
  reviews: readonly ReviewItem[];
  heading: string;
  description: string;
  sourceLabel?: string;             // real Google Maps attribution only
  disabledMotion?: boolean;
};
```

**Fixed six-item visual fixture** for the approved generic reforms reference (all fictitious; never evidence about an actual company):

| ID | Author | Date | Stars | Text |
| --- | --- | --- | --- | --- |
| demo-01 | Andrea M. | septiembre de 2026 | 5 | Nos explicaron cada paso de la reforma y cumplieron los plazos que habíamos acordado. |
| demo-02 | Víctor P. | agosto de 2026 | 4 | La comunicación fue clara. Valoramos especialmente el desglose del presupuesto. |
| demo-03 | Núria S. | julio de 2026 | 5 | Cuidaron los acabados y dejaron la vivienda recogida al terminar. |
| demo-04 | Jordi C. | junio de 2026 | 5 | Nos ayudaron a aprovechar el espacio del baño sin cambiar todo el diseño. |
| demo-05 | Elena G. | mayo de 2026 | 4 | Respondieron rápido a los cambios que pedimos durante la obra. |
| demo-06 | Laura B. | abril de 2026 | 5 | El resultado del salón encajó con lo que habíamos imaginado. |

Fixture partition is deterministic: desktop row one = `demo-01` to `demo-03`, desktop row two = `demo-04` to `demo-06`; each row duplicates its **own** three cards once, visually. The separate mobile-only row contains `demo-01` through `demo-06` in that order, then one hidden-to-accessibility visual clone group. CSS must display **only** the appropriate track set for a viewport, so all six distinct reviews remain readable on mobile without double screen-reader announcements. No random shuffle, fake photos, fake local celebrity names, artificial "verified purchase" glyphs or fabricated exact business metrics.

Verticals replace the fixture with **new explicitly fictitious sector-appropriate copy** while retaining the card contract. Ops OS: practical handling of works/moves, quotes and scheduling. Dental OS: reception, communication and patient experience **without fabricated treatment outcomes or clinical promises**. Church OS: do not impersonate actual attendees; use appropriately labeled community testimony examples only if that surface needs them. MelodIQ corporate may instead choose genuine client cases. No cross-client data reuse by default.

## 3. Motion and interaction contract

The baseline animation is **CSS transforms, not per-frame React state or a timer that shifts items**. Preserve initial SSR cards. Activate movement only when enhanced/hydrated and permitted by user settings; on successful hydration set `data-enhanced="true"`, otherwise leave it absent. Set `data-static="true"` when the fixture is insufficient, touch takeover selects manual scroll, or the app intentionally disables autoplay. The no-JS version remains a meaningful static, horizontally scrollable list.

Reference mechanics:

```css
.review-marquee {
  --mr-surface: #f7f7f4;
  --mr-text: #303a36;
  --mr-muted: #717a73;
  --mr-border: #e7e8e2;
  --mr-card-border: #e8e9e5;
  --mr-star: #e6a82e;
  --mr-empty-star: #d5d8d2;
  color: var(--mr-text);
  background: var(--mr-surface);
  border: 1px solid var(--mr-border);
  border-radius: 18px;
  padding: 35px 0 30px;
  overflow: hidden;
  font-family: Inter, system-ui, -apple-system, sans-serif;
}
.review-marquee__intro {
  max-width: 750px;
  margin: 0 auto;
  padding: 0 22px 25px;
  text-align: center;
}
.review-marquee__eyebrow {
  color: #777e74;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .13em;
}
.review-marquee__intro h2 {
  margin: 11px 0 9px;
  font-size: clamp(23px, 3.3vw, 32px);
  font-weight: 640;
  line-height: 1.2;
  letter-spacing: -.8px;
}
.review-marquee__intro p {
  max-width: 570px;
  margin: 0 auto;
  color: var(--mr-muted);
  font-size: 13px;
  line-height: 1.6;
}
.review-marquee__controls {
  display: flex;
  justify-content: flex-end;
  padding: 0 22px 14px;
}
.review-marquee__pause {
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid var(--mr-border);
  border-radius: 999px;
  color: var(--mr-text);
  background: #fff;
  font: inherit;
  font-size: 12px;
  cursor: pointer;
  display: none;
}
.review-marquee[data-enhanced="true"]:not([data-static="true"]) .review-marquee__pause { display: inline-flex; align-items: center; }
.review-marquee__pause:focus-visible {
  outline: 3px solid currentColor;
  outline-offset: 3px;
}
.review-marquee__viewport {
  overflow: hidden;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent);
}
.review-marquee__track {
  display: flex;
  width: max-content;
  gap: 0;
  margin-bottom: 12px;
}
.review-marquee__track--mobile { display: none; }
.review-marquee__group {
  display: flex;
  flex: none;
  gap: 12px;
  padding-right: 12px;
}
.review-marquee__card {
  box-sizing: border-box;
  width: 285px;
  min-height: 174px;
  flex: none;
  padding: 16px 17px;
  background: #fff;
  border: 1px solid var(--mr-card-border);
  border-radius: 13px;
  box-shadow: 0 3px 12px rgba(36,52,43,.035);
}
.review-marquee__author-row { display: flex; align-items: center; gap: 10px; }
.review-marquee__avatar {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  flex: none;
  border-radius: 50%;
  background: #e5ebe5;
  color: #43544b;
  font-size: 11px;
  font-weight: 700;
}
.review-marquee__author { flex: 1; min-width: 0; }
.review-marquee__author strong { display: block; font-size: 12px; font-weight: 650; }
.review-marquee__author small { display: block; margin-top: 2px; font-size: 10px; color: #8c948e; }
.review-marquee__sample-label { padding: 4px 6px; border-radius: 999px; background: #f2f4ef; color: #7b837b; font-size: 9px; }
.review-marquee__stars { margin: 13px 0 8px; color: var(--mr-star); font-size: 15px; letter-spacing: 1px; line-height: 1; }
.review-marquee__stars .empty { color: var(--mr-empty-star); }
.review-marquee__quote {
  margin: 0;
  color: #4a514d;
  font-size: 12px;
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.review-marquee[data-enhanced="true"]:not([data-static="true"]) .review-marquee__track {
  animation: reviews-left 56s linear infinite;
}
.review-marquee[data-enhanced="true"]:not([data-static="true"]) .review-marquee__track--reverse {
  animation: reviews-right 64s linear infinite;
}
.review-marquee[data-paused="true"] .review-marquee__track,
.review-marquee__track:hover,
.review-marquee__track:focus-within {
  animation-play-state: paused !important;
}
@keyframes reviews-left {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
@keyframes reviews-right {
  from { transform: translateX(-50%); }
  to   { transform: translateX(0); }
}
.review-marquee:not([data-enhanced="true"]) .review-marquee__viewport,
.review-marquee[data-static="true"] .review-marquee__viewport {
  overflow-x: auto;
  -webkit-mask-image: none;
  mask-image: none;
}
.review-marquee:not([data-enhanced="true"]) .review-marquee__group[aria-hidden="true"],
.review-marquee[data-static="true"] .review-marquee__group[aria-hidden="true"] {
  display: none;
}
@media (max-width: 600px) {
  .review-marquee { padding: 26px 0 24px; }
  .review-marquee__intro { padding-bottom: 22px; }
  .review-marquee__track--desktop { display: none; }
  .review-marquee__track--mobile { display: flex; }
  .review-marquee__card { width: 260px; min-height: 176px; }
  .review-marquee__viewport {
    -webkit-mask-image: linear-gradient(90deg, transparent, #000 5%, #000 95%, transparent);
    mask-image: linear-gradient(90deg, transparent, #000 5%, #000 95%, transparent);
  }
}
@media (prefers-reduced-motion: reduce) {
  .review-marquee__track { animation: none !important; }
  .review-marquee__group[aria-hidden="true"],
  .review-marquee__pause { display: none; }
  .review-marquee__viewport {
    overflow-x: auto;
    -webkit-mask-image: none;
    mask-image: none;
  }
}
```

Implementation details beyond CSS:

- Visible pause button maintains explicit paused state across hover/blur. Hover/focus pause is an extra convenience, **not** the only pause mechanism. Announce control state with real text and `aria-pressed`; keyboard activation is Space/Enter. When `prefers-reduced-motion` is active, show a static horizontally scrollable list and hide/disable the now-irrelevant movement toggle.
- Observe page visibility and section intersection; suspend animation while the tab is hidden or section is outside the viewport. Resume only if the user has not explicitly paused. Avoid creating duplicate observers or intervals on rerender. Keep the pause position when possible, not restart from card 1 every hover.
- On touch devices the moving row is readable and has a usable stop mechanism. For actual swipe/drag, suspend automatic movement on touch/pointer interaction, maintain a stable visible position, then allow native horizontal scrolling. Do not claim swipe support from `touch-action` alone when the transformed track cannot be dragged. Manual takeover does not secretly restart.
- Under motion reduction/JS failure, original semantic cards remain readable, not blank or duplicated; links to authentic reviews remain accessible. Do not animate all quote text in and out independently.
- When there are fewer than six useful unique reviews, prefer a responsive **static** list/grid instead of looping a small set of people visibly. With zero real reviews, omit the section or show an honest empty state; never fall back to demo testimonials.
- Avoid horizontal document overflow, clipped focus rings, duplicate announcements or focusable cloned links. Check zoom and large fonts; allow taller cards where content requires it.

WCAG 2.2 `2.2.2 Pause, Stop, Hide` applies to automatically moving content lasting more than five seconds. A pause method must be usable by keyboard/touch and visible/understandable in context (source: `src-w3c-wcag-22`).

## 4. Demo, real data and legal/search boundary

| Mode | Content/source | Label and attribution | Production/search behavior |
| --- | --- | --- | --- |
| `demo` | Purely static, named fixture data. No API or paid service. | Prominent `VISTA DE DEMOSTRACIÓN · OPINIONES FICTICIAS` above cards plus `Ejemplo` on every card; no Google logo/source badge or invented review count. | Preview/staging remain `noindex` by default under `std-public-web-discoverability-baseline`. Never include `Review`/`AggregateRating` JSON-LD or imply an actual customer recommendation. |
| `real` | Client-authorized authentic reviews, e.g. approved Places integration where its cost and terms are explicitly accepted. | Actual author credit and all available attribution assets, Google Maps attribution and direct source link when using Google's data; explain sorting/filtering. | Truthful facts only; no synthetic fallback. Follow current provider terms, privacy and eligibility checks. |

Google's Places policies require author and Google Maps attribution for API-provided reviews; Google Search's review-snippet guidance excludes fake reviews and limits self-serving `LocalBusiness`/`Organization` review-rich-results eligibility. **Embedding real Google reviews on a business's own site does not guarantee Google search stars** (sources: `src-google-places-review-attribution`, `src-google-review-structured-data`). Google Maps does not "verify" individual experiences in the sense implied by a synthetic verified badge.

A public preview accessible through a temporary URL is still user-visible. The sample disclaimer is part of the component, not a hidden legal-footnote workaround. Do not allow the default public production build to show fictional testimonials as if genuine. The client or site owner approves any real release, data rights, links, indexability and monetizable integration separately.

## 5. Implementation procedure in a future project

1. Read the project's `AGENTS.md` and `DESIGN.md`, approved brand palette, URL/indexability state and existing testimonial components. Do not overwrite a stronger working local solution without reason.
2. Decide whether this section is relevant to the actual information architecture. If not, skip it. Choose `demo` vs `real` **explicitly** and identify the owner of content/attributions.
3. Reuse existing React/CSS/Tailwind primitives when they can reproduce `1–3. Avoid another marquee dependency for a 2-keyframe CSS implementation. Do not copy the gated 21st.dev source without checking its license.
4. Start with the six fixed fixture items and exact neutral metrics. Render the section at 1440×900 to establish a visual reference, then replace sample copy/tokens with client-specific approved demo copy. **Record which numeric/visual overrides are intentional**.
5. Add accessible pause, focus/hover/touch behavior, reduced-motion/static states, offscreen/hidden lifecycle and semantic originals/clones. Real provider mode is a distinct data/auth/attribution task, never smuggled into the visual-only implementation.
6. Integrate on the owning site's appropriate content route. Do not assume the section belongs beneath every hero. Do not move existing CTAs or change the lead form. Keep the page narrative purposeful and within the site's visual direction.
7. Capture real desktop/mobile evidence and run the acceptance matrix. Only report observed tests as PASS. An imported component or successful build alone is **not** visual acceptance.

## 6. Definition of Done for each adoption

| Check | Required observation |
| --- | --- |
| Source/brand | Exact v1 reference and repo-local style decisions noted; no unrelated client brand copied. |
| Desktop | At 1440×900 and a normal desktop width, two rows, opposite directions, 56s/64s loops, equal group widths, 12px gaps, no restart jump, no excessive fade. |
| Responsive | 768px, 390px, 320px, 200% zoom/large text; one row with all six unique cards at ≤600px; no document horizontal overflow or hidden copy/control. |
| Pause & focus | Mouse hover pauses; visible button pauses/restarts; focus/Space/Enter work; manual pause survives pointer leave; mouse/touch manual takeover does not unexpectedly restart. |
| Reduced motion/lifecycle | System reduce = static/readable; hidden tab/offscreen suspends; no-JS renders first cards; no hydration shift or empty state. |
| Accessibility | Unique semantic reviews, cloned group `aria-hidden` and nonfocusable, numeric stars, labels, visible focus, contrast and touch targets. Screen reader behavior checked where accessible. |
| Demo truth | Every example marked, no false Google branding, no invented aggregate, links or schema, noindex/release decision unchanged. |
| Real truth | Only genuine authorized data, author and provider attribution, source URLs, sorting notice; no mock fallback, no unsupported search stars. |
| Performance | CSS transforms, no per-frame React rerenders, minimal dependency/runtime cost, no material CLS, no regression in page loading. |
| Release evidence | Repo tests/build and live rendered page checked where authorized; `PASS`/`FAIL`/`NOT RUN` distinct. No claim of deployment without proof. |

Reference tokens are **measurable defaults**, not permission to force identical brands. If a future design diverges, retain this Pattern as the comparison baseline and document the specific client/vertical reason.

## Source traceability

- `src-21st-shadcnspace-testimonials-marquee`: inspected donor layout/motion (two opposite rows and fade); original code not reused.
- `src-w3c-wcag-22`: pause/stop/hide, focus and reflow requirements.
- `src-google-places-review-attribution`: real provider attribution and review display rules.
- `src-google-review-structured-data`: false reviews, self-serving reviews and structured-data eligibility.

