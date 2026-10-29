---
id: ref-public-service-commercial-benchmark-vizcaya-2026-10-29
kind: reference
status: active
owner: engineering
version: "0.1"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - visual-benchmarking
sources:
  - src-reformas-vizcaya-live-2026-10-29
last_verified: 2026-10-29
review_due: 2027-01-29
---

# Public-service commercial web benchmark: Vizcaya (2026-10-29)

## Purpose and limits

This is an **observational design/commercial-content comparison**, not a ranking, code audit, accessibility certification, PageSpeed test, rights clearance, or independent verification of commercial claims. Use it with `pb-frontend-quality-review` to prevent a technically clean or photogenic website from being mistaken for a compelling, complete business experience.

Observed in a real browser on 2026-10-29 at desktop and approximately 390 × 844 mobile:

- **Public reference:** [reformas-vizcaya.com](https://reformas-vizcaya.com/), external source `src-reformas-vizcaya-live-2026-10-29`.
- **Existing internal preview:** [reformasvizcaya.vercel.app](https://reformasvizcaya.vercel.app/), project `Kappa-Bot/IsmaelVizcaya-Web`, reviewed as a scoped, intentionally non-indexable preview.

The source is useful for **content and conversion patterns**, not as unquestioned proof of identity, completed works, customer reviews, prices, rights, results, or code quality. A similar or matching logo does not by itself settle who owns or operates a domain. Before making client-facing claims or reusing external material, independently reconcile business identity, permitted assets and legal information with the actual client. Do not conflate the preview's deliberate noindex/no-form restrictions with an accidental deployment defect.

## Observed comparison

| Visitor need / surface | External public site — observation | Internal preview — observation | Transferable decision |
| --- | --- | --- | --- |
| First-viewport comprehension | Large photographic hero explicitly says reforms in Bilbao/Bizkaia; budget and service-exploration actions are visible with social-proof statements. | Strong residential imagery and large typography, but rotating editorial phrases such as “Toda la casa. Una nueva mirada” need extra interpretation; one action per slide and carousel controls compete for mobile space. | Combine art direction with a clear service/geography/outcome statement and purposeful next action. Avoid abstract-only main proposition and carousel chrome dominating mobile. |
| Navigation and service discovery | Header points to services, zones and prices; home introduces multiple services and links into deeper content. | Simple Inicio/Reformas/Hablemos; one overview route and a very short home below the carousel. | Map real visitor intents and important service categories before designing page quantity. Deep routes only where distinct useful content exists. |
| Reasons to believe | Shows review/volume statements, work examples with before/after controls, and an about section. These claims and photos were **not independently verified**. | Explicitly identifies conceptual/generated visuals and does not invent completed work or testimonials. | Prefer authentic, authorized case studies, provenance and real proof. Never synthesize “verified” reviews, metrics or client outcomes. |
| Practical decision support | Exposes indicative price bands, who coordinates the work, project process, location information, guides and FAQs. | Sparse editorial sections plus a compact services overview, with little help estimating fit or understanding a project. | Provide relevant budget/process/objection answers where the business can substantiate them; a portfolio-style hero alone is not a sales journey. |
| Contact / enquiry | Prominent budget CTA, contact form, telephone and WhatsApp; mobile has bottom call/budget actions plus floating WhatsApp. | Direct personal phone/WhatsApp links and mobile bar; no structured form/backend by the approved preview scope. | Preserve working direct contact; add structured intake only with authorization, privacy, error/success behavior and a real destination. Avoid crowding by multiple fixed buttons. |
| Long-scroll and motion | Information-rich scroll sequence with service imagery, work, FAQ and footer. Some observed reveal moments left content pale/temporarily absent; floating controls risk visual collisions. | Visually coherent minimal sections and controlled conceptual imagery, but the homepage ends before answering many commercial questions. | Build a purposeful long-page narrative with accessible, non-blocking transitions; test long scroll and mobile stacking, not just the first frame. |
| Search/publication | Many visible service/area/content entry points on the public business site; quality and indexation not audited. | Intentionally noindexed preview, not a public SEO release. | Plan truthful indexable route coverage only after client approval and legal/search readiness; apply `std-public-web-discoverability-baseline`. |

## What is worth adopting

1. **Commercial clarity above the fold:** concrete business, actual service area, differentiated outcome and usable next step. A strong photograph, overlay/contrast and expressive headline can support that story without swallowing it.
2. **A complete but selective content journey:** services → relevant detail → how it works → credible evidence and budget context → objection handling → contact. The sequence is a conceptual model, not required page order or component inventory.
3. **Useful dual navigation:** one primary enquiry action and a quieter exploration route, with contextual internal links. Specific CTA count/layout remains a product decision.
4. **Service-intent and local discovery:** distinct pages for distinct helpful content and genuinely served areas, avoiding boilerplate doorway/location proliferation.
5. **Truthful trust and imagery:** real permissions, before/after evidence where it exists, named responsibility, grounded price ranges and identifiable contacts. If proof does not exist, do not counterfeit it.
6. **Mobile enquiry ergonomics:** a legible hero, thumb-friendly contact and a sticky action only when it remains unobtrusive and does not cover the page or focus.
7. **Editorial richness without filler:** intentional photography, responsive crops, consistent type, paced sections and meaningful motion, while explaining enough to let a visitor decide.
8. **Low-friction enquiry:** a real, validated, privacy-compliant form when authorized; phone/WhatsApp fallback; consistent destination and confirmation.

## What not to adopt mechanically

- Source-site logos, text, project photos, reviews, metrics, prices, personal data or contact details without explicit ownership and client verification.
- A promise of “verified reviews”, a reform count, or “real project” based only on a site's own badge or visual appearance.
- Every area/service/blog page regardless of distinctive content and whether the client actually serves it.
- Animated reveal that leaves content blank or inaccessible, auto-rotating content that distracts from the task, and mixed fixed WhatsApp/sticky bars that obscure copy.
- An enquiry route whose form, validation or design diverges from the main CTA promise; the observed `/presupuesto/` form requires independent UX/form verification before using it as a pattern.
- Any implication that a gated demo should be indexed, have lead collection enabled, or replace the client's live domain without the owner's authorization.

## Reusable pre-implementation and acceptance matrix

Create a small repo-local table for each material client business website (or incorporate these columns into an existing design/launch checklist):

| Gate | Question | Evidence / expected disposition |
| --- | --- | --- |
| Identity & rights | Are company, service region, logo, photography, project proof, pricing and contacts confirmed? | Verified client facts and asset permission; unknown stays excluded or explicitly labelled. |
| Baseline & benchmarks | Did we inspect the actual current/preferred site and one to three relevant live examples, beyond the hero, at desktop and mobile? | Dated URLs, representative captures/observations and an explicit adopt/adapt/defer/not-applicable matrix. |
| First viewport | Can a new visitor understand the offer and reach the primary next step without guessing? | Desktop + approx. 390px mobile, copy/crop/contrast/CTAs in rendered browser; no visual overlays. |
| Information architecture | Can visitors find real services, geography, process, proof if any, budget context, FAQs/objections and contact? | Route/section mapping tied to real intent; justify omissions instead of manufacturing content. |
| End-to-end conversion | Do the primary CTA, contextual CTAs and any mobile sticky contact reach a working, truthful destination? | Real click-through including form error/success and privacy if in scope; no dead or contradictory CTA. |
| Visual and motion quality | Is the design distinctive without trading away information, touch access, speed or reduced-motion support? | Comparable scroll checkpoints at desktop/mobile, keyboard/focus, 320px reflow, 200% zoom, motion with and without preferences. |
| SEO/publication | Is this an authorized live commercial site or a gated preview? | Preserve noindex and backend gates until owner approval; follow `pb-public-web-discoverability-launch`. |
| Gap disposition | Where is a relevant reference materially better than our deliverable? | Each gap has adopt/adapt/defer/not-applicable owner decision and evidence; no hand-waved “looks premium” sign-off. |

A reference must not become a visual template or universal feature checklist. `std-ui-ux-quality-baseline` and `pb-frontend-quality-review` remain canonical for quality; the SEO and client-approval standards remain authoritative for indexation and public claims.

## Verification scope

**Performed:** browser-rendered comparison of both homepages at desktop/mobile, the preview's services route, navigation/contact affordances, and observed reference sections/form route.

**Not performed:** automated accessibility/keyboard screen-reader audit, performance/Core Web Vitals, form submission/lead delivery, security/privacy audit, Search Console/indexation checks, independent customer-review/project proof, photography reuse rights, or formal source-code equivalence. Observational screenshots were inspected in the browser; no durable screenshot archive is claimed here.

**Revisit:** the live reference and preview may change. Revalidate material observations before using them as current acceptance evidence. Review due 2027-01-29.
