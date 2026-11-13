---
id: pb-search-visibility-service-operations
kind: playbook
status: active
owner: engineering
version: "1.0"
applies_to:
  - marketing-workflows
  - client-business-websites
  - public-marketing-websites
  - organic-search-services
sources:
  - src-google-seo-starter-guide
  - src-google-sitemaps
  - src-google-block-indexing
  - src-google-ai-features
  - src-google-local-ranking
  - src-google-sitelinks
  - src-openai-web-crawlers
  - src-bing-ai-performance
  - src-indexnow-protocol
  - src-w3c-wcag-22
  - src-webdev-core-web-vitals-thresholds
  - src-aepd-cookie-guide
last_verified: 2026-11-13
review_due: 2027-02-13
---

# Organic Search & Answer Visibility — delivery operating system

## Scope, authority and outcome

This is the **commercial delivery procedure** for MelodIQ Systems to offer a repeatable organic visibility service to eligible Spanish SMEs and larger businesses. It covers discovery, search opportunity, implementation, technical QA, local profiles, content, AI-answer observations, measurement, operations and handoff. It is **not a second SEO technical standard**. The authoritative technical floor is [`std-public-web-discoverability-baseline](../standards/public-web-discoverability-baseline.md), and the technical release sequence is [`pb-public-web-discoverability-launch](public-web-discoverability-launch.md). Client truth, conversion, legal, security, accessibility and release rules remain with their existing canonical owners. The market evidence is [`ref-search-visibility-research-2026-11](../references/search-visibility-research-2026-11.md) and pricing is [`ref-search-visibility-pricing-spain-2026-11](../references/search-visibility-pricing-spain-2026-11.md).

**Service promise:** inspect and improve the business's discoverability and ability to convert qualified organic visitors using verifiable work. **Never promise** first place, sitelinks, a Knowledge Panel, indexing by a particular date, AI citations, a fixed lead volume or revenue. A technically indexable URL is not an indexed URL; an indexed URL is not a ranking or a lead. Search and answer engines control their own output.

**Vocabulary.** SEO = improving technical access, content relevance, reputation and search experience; local SEO = visibility for eligible geographically relevant businesses; AEO = making authentic answers clear and usable in search/answer interfaces; GEO / LLMO = emerging practitioner labels for discoverability and attribution in generative/search-assisted systems. These are **service lenses**, not four independent ranking algorithms or a reason to sell redundant work. AI Search exposure and model-training access are different decisions.

**Delivery states:** `PASS (test actually run, evidence recorded); `FAIL (observed failure); `NOT RUN (not attempted); `BLOCKED (cannot proceed without a dependency); `OWNER ACTION (needs client-owned account, permission, fact or decision); `N/A (not applicable, with reason). Never turn absence of data into zero or a green check.

## 0. Engagement envelope and decision gates

Every engagement begins with a client-owned project record, stored in the **authorized client workspace**, not in this public Handbook. Reuse the existing CRM/brief rather than creating parallel records. Use [`tpl-search-visibility-client-workbook](../templates/search-visibility-client-workbook.md) as a **field guide**, not an additional database.

Capture: legal/trading name, brand variants, business model, country/regions, physical locations versus service area, genuine services, sectors requiring regulated review, owner, website and canonical host, current hosting/CMS, access boundaries, existing rankings and profiles, customer journey, lead definition, economics, capacity, budget, languages, competition, legal/consent status, seasonality and authorized contacts. For every business claim capture a source, owner and approval. Never infer an office from a registered/fiscal address.

**Permission gate (G0).** Record written authority for: site edit, domain/DNS, Search Console, Bing Webmaster, Google Business Profile, Bing Places, Apple Business Connect, review responses, citation corrections, analytics/cookies, external outreach, publication and spend **separately**. Use delegated least-privilege access; never request a customer's personal password. A contract for SEO is not blanket authorization to change DNS, send communications, buy links, edit third-party profiles, publish testimonials or create CRM records.

**Risk gate (G1).** Mark each target as live public, staged/draft, authenticated/private, legal/compliance, redirect or removed. Protect private/preview and sensitive content independently of `robots.txt`. No unapproved indexing unlock, consent bypass or production form test with synthetic real-world writes.

**Evidence gate (G2).** For each proposed material change record current behavior, desired behavior, evidence/source, impact hypothesis, owner, risk, reversible change and acceptance test. High-risk migration, sitewide canonical, multilingual, business identity or privacy changes require explicit sign-off.

## 1. Choose the correct service route (T00)

| Client model | Search job and commercial KPI | Specialized work | Do not assume |
| --- | --- | --- | --- |
| Local service-area trades (mudanzas, reformas, limpieza) | Calls, qualified enquiries, jobs won by service/area | GBP eligibility, true service areas, service pages, genuine photos, call/WhatsApp handling | A walk-in shop, fixed prices, every municipality served |
| Physical retail / multi-location | Store visits, stock enquiries, sales | Per-real-location profile/page, opening hours, products, directions, local inventory where supported | Fake branches or duplicate listings |
| B2B professional / industrial | Qualified leads, demo requests, pipeline value | Technical case studies, service/industry pages, procurement FAQs, credible authors | That high traffic equals qualified demand |
| Healthcare / legal / finance | Appointments and qualified enquiries with compliance | Regulated-claim review, credentials, local eligibility, YMYL scrutiny, professional rules | Medical outcomes, professional endorsements or unsupported claims |
| Ecommerce / marketplace | Organic transactions, gross margin, category revenue | Product/category architecture, variant/canonical/facets, Merchant Center, availability, stock and feed consistency | That every filter/variant should index |
| Tourism / hospitality | Direct bookings and enquiries | Eligible property/location profiles, availability/pricing truth, seasonal multilingual content | Fake reviews or duplicated property pages |
| Education / nonprofit / association | Enrolments, registrations, donations | Program/event information, eligibility, accurate dates and public trust | Commercial lead model by default |
| SaaS / software / vertical product | Qualified trials, demos, signups | Product/docs/pricing/use cases, feature maturity, API/docs discoverability | That a demo is a live product or private app is public |
| Multi-region / multilingual | Region-specific qualified conversions | Localized content, hreflang, correct `ca`/`es`/`en` language tags, market-specific offer | Machine translation = localized expertise |

**Sector gate:** if the client cannot verify a service, area, qualification, opening hours, price, team member or case study, the content must omit or qualify that claim. For regulated sectors, require client/legal review before publication. A local landing page is justified by real differentiated information and user intent, **not** by multiplying city names.

## 2. Discovery and commercial baseline (T01)

**Inputs:** client brief; authorized site; actual offering and margin; public competitors; any existing GSC/GBP/Bing/analytics access.

1. Define the **primary conversion** (e.g. qualified quote request accepted by CRM, booked consultation, ecommerce order), secondary conversions and disqualifiers. Specify how duplicates, spam, self-referrals, phone/WhatsApp and offline sales are counted.
2. Map customer jobs to intent: navigational/brand, local transactional, non-brand commercial, comparison, informational, post-sale. List query clusters, not arbitrary keyword-density targets.
3. Sample at least three real search competitors per major cluster, not only businesses named by the client. Record query, location, device, date, SERP type, ads vs organic vs local pack, relevant landing URL, page purpose, structured data and genuine proof. Competitor `sitemap.xml` URL count is **inventory, not rankings**.
4. Capture baseline by source, date range, geography, device, property and definition: GSC impressions/clicks/CTR/position and indexing (where authorized); Bing Webmaster; GBP interactions; field CWV; actual form/call conversions and CRM-qualified leads. Mark unavailable access `NOT RUN`/`OWNER ACTION`; never invent history.
5. Map available business capacity: can it fulfil demand? Is the service region real? Is a contact method monitored? What counts as a good lead?
6. Agree deliverable cadence, owners, sign-off, exclusions, response times, costs and a **hypothesis**, not a traffic guarantee.

**Output:** approved discovery record, baseline register, prioritized query/URL/intent map, access/owner-action ledger, contract/scope. **Exit:** no unverified business facts promoted into publishable copy.

## 3. Full audit — reproduce, do not guess (T02)

**Coverage matrix:** enumerate all important URLs, sample representative templates plus high-value/changed pages; crawl full site when size and permissions permit. Audit desktop/mobile and rendered/HTTP evidence as relevant. For each finding record `ID | URL/template | observed state | source/time | expected state | business risk | confidence | owner | fix | verification | status`.

### A. HTTP, robots, crawling and indexing

- Confirm final HTTPS host, apex/www policy, redirects (301/308 as appropriate), loops, chains, status 200/3xx/4xx/5xx, 404/410 and soft-404 behavior.
- Check `robots.txt` including specific user-agent groups; `meta robots` and `X-Robots-Tag`, canonical in actual served HTML, sitemap/indices, XML validity, URLs and image references, duplicate/faceted/parameter URLs, hreflang if real locales.
- Validate the **route policy**: indexable canonical pages should resolve and not carry accidental `noindex`; login, CRM, API, draft and private media stay protected at an auth boundary. A `robots.txt` block is not access control; a crawler blocked by robots may not see a `noindex` tag.
- Include only intended final canonical URLs in sitemap. Use `lastmod` only for significant, evidenced updates; Google ignores `changefreq` and `priority`. Avoid fabricated freshness.
- For crawl incidents, compare actual verified bot logs/CDN/WAF, server errors, throttling, rendered resources and GSC inspection when authorized. `site:` search is a rough discovery check, **not** an exhaustive index audit.
- JavaScript rendering: compare initial HTML and rendered DOM; essential content and links must be discoverable; don't depend exclusively on client-side events. Check crawlable `a href` links, pagination, infinite scroll and media.
- Evaluate international: unique locale URLs, translated content, self/reciprocal hreflang, correct canonical per language, optional `x-default`; no automatic language redirects that block crawlers.

### B. Search appearance and entity

- Distinct meaningful titles/H1s/descriptions for each purpose, no keyword stuffing or hard-coded magic character limits; Google may rewrite titles/snippets.
- Internal linking, orphan pages, breadcrumbs, anchor text, crawl depth by actual site structure, canonical consistency and useful branded destinations for potential sitelinks. **Sitelinks are generated by Google**, not configured by schema.
- Schema.org types and Google eligibility: truthful `WebSite`, `Organization` / eligible `LocalBusiness`, `Service`, `Product`, `BreadcrumbList`, `Article` etc. Check visible facts, correct IDs/URLs, no duplicate/conflicting nodes, safe JSON-LD serialization, Rich Results Test where applicable. Schema validity ≠ guaranteed rich result.
- Do not use self-serving `LocalBusiness` review stars, invented `aggregateRating`, fake awards, fabricated `sameAs` or fictitious office/phone. FAQ content can help readers; FAQ markup is not a guaranteed rich-result tactic.
- Brand favicon, logo, social preview and actual image bytes; OG/Twitter tags and real thumbnail crops, without opening private resources.

### C. Content, reputation and conversion

- Map **one distinct visitor job** to each valuable landing page. Evaluate factual accuracy, unique value, first-hand examples, topical coverage, pricing/eligibility clarity where known, author/organization provenance, update needs, accessible media and conversion friction.
- Inspect real competitor content gaps, not copy. Check titles/intent cannibalization, thin duplicates, doorway area pages, internal anchors and actual proof/rights.
- Verify calls, WhatsApp, email, forms, errors, consent, post-submit acknowledgement, duplicate handling, CRM lead outcome and mobile usability. Never use production synthetic submissions without safe isolated path and authorization.
- Inspect external mentions and links for relevance/legitimacy; reject paid link schemes, private networks, reciprocal spam and fabricated testimonials.
- Check local listings, duplicate profiles, owner access, categories, business hours, service area versus storefront, photos and review policies. Never claim an ineligible address is public-facing.
- Check privacy and accessibility through existing standards: [`std-public-website-legal-trust-baseline](../standards/public-website-legal-trust-baseline.md), [`std-ui-ux-quality-baseline](../standards/ui-ux-quality-baseline.md) and [`pb-conversion-measurement-and-experiments](conversion-measurement-and-experiments.md).

### D. Performance and experience

- Record **field** p75 Core Web Vitals separately from lab diagnostics: LCP good ≤2.5s, INP good ≤200ms, CLS good ≤0.1; segment mobile/desktop, origin/URL and sample coverage. Do not report FID as current CWV. Lab Lighthouse is a reproducible diagnostic, not user experience proof.
- Audit LCP resource, responsive images, `sizes`/`srcset`, format, caching, font loading, JS execution, interaction responsiveness, CLS, keyboard and reduced-motion. No mandatory tool or arbitrary "all green" promise.

**Output:** URL inventory + audit matrix, reproducible evidence, top opportunities and blocked external dependencies. **Exit:** high-severity claims have HTTP/DOM/account evidence, not a screenshot-only guess.

## 4. Prioritization and client roadmap (T03)

For each candidate use a **reasoned** score, not a fake ROI model:

- Impact `I` 1–5: verified business relevance and severity (5 = key route blocked, privacy leak or conversion unavailable; 1 = cosmetic).
- Confidence `C` 1–5: direct observed proof and expected mechanism (5 = repeatable and source-backed; 1 = speculation).
- Effort `E` 1–5: total implementation + QA + coordination.
- Risk `R` 1–5: security, legal, regressions, migration, business truth.
- Indicative order = `(I × C) / (E + R)`, with mandatory security/legal blockers overriding score. **Never present the score as a predicted traffic increase.**

Classify `P0`: private data exposed, wrong public business identity, accidental sitewide noindex, broken live conversion, major security/consent breach; `P1`: high-value URLs not indexable, major canonical/sitemap mismatch, material false claim, repeated form failure; `P2`: content gap, linking, schema enhancement, local listing improvements; `P3`: speculative AI files, minor markup polish, optional experiments. Do not force every client into a six-month backlog.

**Output:** ordered backlog, 30/60/90-day milestones or project-specific schedule, dependency map, client approvals, QA gates, estimated hours and **explicit non-goals**. Client approves budget/scope, not rankings.

## 5. Implementation lanes (T04–T08)

### T04 — Technical and release foundations

Use [`pb-public-web-discoverability-launch](public-web-discoverability-launch.md) for route policy, sitemap, canonical, JSON-LD, previews and deployed verification. Add regression tests for the actual failure class. Preserve existing architecture; no automatic rewrite to a new framework, CMS, hosting or analytics stack. Validate all changes in a preview/staging environment before production. Preserve rollback and route history for migrations.

### T05 — Content and information architecture

1. Build a query-cluster → visitor job → **one primary target URL** map. Choose reuse/upgrade/merge/new page. Never create multiple near-identical location/keyword doorways.
2. Brief each page with target customer, evidence, primary question, supporting questions, facts requiring client confirmation, original examples, search intent, outline, media rights, internal links, CTA, success metric and editor.
3. Draft human-useful copy: answer the question early, explain conditions/limitations, distinguish what is confirmed from quoted/estimated, use real photos/cases and cite primary evidence when factual claims matter.
4. Review claims with client/sector specialist. Publish only supported services, prices, staff, credentials, warranties, territories and testimonials. Avoid unlicensed images, fake reviews and mass AI text.
5. Implement semantic headings, descriptive anchors, relevant media alternatives, structured data only if eligible, and crosslinks between service, case, guide and conversion pages.
6. QA factual accuracy, accessible reading, mobile layout, correct metadata, canonical and conversion. Update `lastmod` only when significant content changed.
7. Measure actual search and business outcomes over time. If evidence is absent, label the initiative as a hypothesis.

### T06 — Local search and reputation

1. Verify eligibility and **existing** client-owned GBP before creation. Distinguish customer-facing address from service-area business; follow current Google guidelines. Do not create virtual offices, duplicate profiles or unverified categories.
2. Confirm business name, website, contact, real service areas, category, hours, services and photos with owner; correct only with delegated permission.
3. Audit Bing Places and other **sector-relevant** legitimate listings. Record mismatches; don't spray dozens of irrelevant directories. Normalize meaning and real data; minor "C/" vs "Calle" formatting is not proof of a ranking penalty.
4. Request honest reviews from genuine customers without incentives, gating or fabrication; comply with platform policy and communications/privacy rules. Owner approves responses where needed; no confidential client details in public replies.
5. Create location/service pages **only** for demonstrably served places with unique local utility; avoid a fake map pin or publishing a home/fiscal address as a public shop.
6. Verify changed listings on their public URL; record pending moderation separately. Maps ranking depends on relevance, distance and prominence and is not controlled by the agency.

### T07 — Authority and earned distribution

Inventory useful independent citations, partnerships, professional associations, original case studies and press opportunities. Evaluate editorial relevance, authenticity, owner permission, disclosure and real user value. Avoid buying manipulative links or manufacturing forum/Reddit activity. Track publication URL, rel attribute if relevant, source/date and whether the mention remains live. A purchased placement must not be described as earned authority.

### T08 — AEO/GEO/LLMO as a measured extension, not a separate magic checklist

- Prioritize **ordinary search fundamentals**: crawlable public HTML, accurate entity and service facts, authentic expertise, answers to actual customer questions, useful internal/external evidence and current profiles.
- For Google AI Overviews/AI Mode, Google's primary guidance states **no extra technical or AI-specific markup/file requirement** beyond normal eligible Search content. Do not claim `llms.txt`, FAQ markup or a schema type guarantees citation.
- For ChatGPT Search, distinguish owner-approved `OAI-SearchBot` (search) from `GPTBot` (training) and `ChatGPT-User` (user-triggered fetch). A business may permit search and decline training. Verify official crawler/IP policy and CDN behavior; do not bypass access controls.
- `llms.txt` and alternate Markdown are **optional experiments**, not prerequisites. If already approved, maintain factual links and assess actual use; do not duplicate private content or make unsupported "AI ranking" claims.
- Observe a stable, documented query cohort by engine, date, locale, location, personalization and method. Record answer citation URL, brand mention, accuracy and variability. Compare repeated samples; one prompt is anecdotal. Separate Google Search Console Web clicks/impressions from its **dedicated generative-AI Search and Discover reports** (announced June 2026 and globally rolled out by 31 August 2026), which expose AI-feature impressions/pages/countries/dates and some device filters; use only views and data actually accessible in the authorized property. Multimodal filters were introduced in September 2026. Compare Bing AI Performance, referral traffic and **actual** conversions independently. A Google AI impression is not an AI citation click or qualified lead. Do not invent a dedicated GSC AI Overview metric if the property/interface does not expose one.
- Record failed/negative observations, uncertainty and costs. Stop experiments that do not add useful evidence. Use [`tpl-search-visibility-monthly-report](../templates/search-visibility-monthly-report.md) for honest reporting.

## 6. Production release and verification (T09)

**Change review:** PR/diff, source provenance, business claims, permissions, robots/noindex matrix, sitemap, canonical, redirects, privacy and form security. No unapproved domain/DNS changes or extra paid tools. Follow [`pb-quality-release-review](quality-release-review.md).

**Minimal release QA matrix** (expand for affected templates/risks):

| Gate | Test | Acceptance |
| --- | --- | --- |
| Public URLs | Sample all priority URLs, all changed routes and representative templates | Intended status, final canonical host, correct metadata, readable content |
| Private URLs | CRM, admin, API, staging, attachments | Auth/deny at actual boundary; no sensitive data in metadata, sitemap or previews |
| Robots/sitemap | Actual production HTTP and XML | No accidental `noindex`/`Disallow` on approved public routes; no private/redirect URLs in sitemap |
| Structured data | Served JSON-LD + validator where relevant | Factual, consistent, parseable; no self-serving review manipulation |
| Internal links | Crawl and key user journeys | No material 404, orphan primary landing or JS-only navigation |
| Conversion | Safe test with mocks/isolation or explicitly authorized real journey | Correct acknowledgement, deduplication, error handling, no synthetic customer data pollution |
| UX/a11y | Relevant viewport/browser/keyboard/zoom/motion tests | No critical interaction, accessibility or visual regression; unrun native AT marked NOT RUN |
| Performance | Same lab setup before/after; field p75 where available | No unacknowledged material regression; field and lab reported separately |
| Analytics | Consent-approved event flow and lead reconciliation | No duplicate conversion, PII leak or fabricated attribution |
| External accounts | GSC/Bing/GBP where authorized | Owner/permission verified; missing access logged, not green |

**Post-release:** capture exact commit/deployment SHA, canonical and apex HTTP, relevant rendered HTML, sitemap, robots, asset/OG response, form availability and known issues. If a P0 regression occurs, execute the **pre-approved** rollback; do not remove legacy fallback until its observation gate passes. A deployment READY flag is not evidence that all site journeys pass.

## 7. Reporting and iteration (T10–T11)

**Weekly during active changes:** incident/crawl and conversion health, delivered work, blockers, evidence. **Monthly:** compare matched date ranges, seasonal context, brand vs non-brand, geography/device, GSC/Bing, actual qualified leads and closed outcomes if authorized, GBP interactions, content performance, site health, AI observations with sample sizes, work log and next backlog. **Quarterly:** review market/competitors, business economics, customer questions, local listing accuracy, platform policy changes and contract scope.

Use `PASS / FAIL / NOT RUN / BLOCKED / OWNER ACTION / N/A` for every claim. "No data" is not "0"; a tool not connected is not proof the client has no profile. Do not call GSC impressions "visits" or AI mentions "leads"; do not infer causation from before/after traffic without considering seasonality, releases and demand. Do not promise a specific 3/6/12-month ranking.

**Conversion attribution:** identify website event → consent context → deduplicated server record → CRM lead → qualified outcome → sale (when legitimately accessible). Define the source of truth and join key without exposing customer PII to search tools. For phone/WhatsApp without consented tracking, use qualitative/CRM self-report as a separate imperfect signal, not a fabricated organic conversion. Avoid covert scripts, recording calls or third-party pixels.

**Escalation:** suspected manual action, compromised site, private data leak, false medical/legal claim, major drop with confirmed technical cause, GBP suspension or migration rollback: stop discretionary publishing, preserve evidence, notify the owner, apply security/legal procedures. Search volatility alone is not proof of a penalty.

## 8. Roles, capacity and pricing boundaries

**Responsible:** SEO/service lead owns hypothesis, audit, priority and reporting; developer owns code/technical QA; editor/sector specialist owns content factual review; client business owner owns business truth, account delegation and publication; privacy/legal reviewer owns regulated/consent questions; account manager owns scope, change requests and invoicing. One person may hold several roles but **must not claim an independent review that did not occur**.

**Service packaging:** define an initial diagnostic/setup separately from a scoped monthly retainer or fixed project. Price by verified hours, seniority, complexity, QA and tool/licence costs; use [`ref-search-visibility-pricing-spain-2026-11](../references/search-visibility-pricing-spain-2026-11.md) for *nonbinding market benchmarks* and [`tpl-search-visibility-commercial-offer](../templates/search-visibility-commercial-offer.md) for offers. Distinguish included monthly output from one-time technical implementation, external content/photo production, translations, paid placements, ads, tools, taxes and owner-owned subscriptions. No automatic purchases.

**Capacity planning:** budget research + implementation + independent QA + reporting + client communication + contingency. Example: if a package costs €700/month and 12h are committed, €58.33/h is **revenue per committed hour**, not margin; subtract staff, overhead, tools and rework before profitability. Do not sell an unlimited retainer. Review realized hours and outcomes quarterly.

**Change control:** record requested change, impact on time/cost/risk, client authorization and acceptance. An SEO engagement does not silently expand into a redesign, multi-tenant system, CRM rewrite or paid ad campaign.

## 9. Reusable deliverables and acceptance

| Phase | Minimum artifact | Acceptance |
| --- | --- | --- |
| T00–T01 | Client brief, permission matrix, goals, baseline | Owner and scope confirmed; unavailable metrics explicitly marked |
| T02 | Audited URL/issue register + reproducible evidence | Every P0/P1 finding has actual URL, layer and observation |
| T03 | Prioritized backlog + dependencies | Business value, risk, effort and approvals visible |
| T04–T08 | Reviewed changes + content proof + QA | No false claims, access leaks or untested major release |
| T09 | Release report with exact revision and rollback | Production HTTP/HTML and affected journeys actually verified |
| T10–T11 | Monthly report, evidence links and decisions | Outcomes distinguish traffic, AI visibility, qualified leads and revenue |
| Closure | Handoff, credentials ownership, outstanding actions, maintenance scope | Client can retain domain, profiles, source and access without agency lock-in |

The templates below are **copyable into an authorized client workspace**, not customer files to commit here:

- [Client delivery workbook](../templates/search-visibility-client-workbook.md): discovery, audit, issue log, backlog, proof, release and owner actions.
- [Commercial proposal](../templates/search-visibility-commercial-offer.md): clear deliverables, exclusions, fees and change control.
- [Monthly report](../templates/search-visibility-monthly-report.md): honest performance, confidence, conversions and AI sampling.
- [Research/evidence ledger](../references/search-visibility-research-2026-11.md): primary learning, rejected myths and revalidation.
- [Spain pricing benchmark](../references/search-visibility-pricing-spain-2026-11.md): dated source-specific published ranges.

## 10. Definition of done for the service system

The **Handbook** is ready for reuse when canonical links, templates, source registry and catalog are consistent and its integrity/compiled-context checks pass. **Each client** is ready when its own authorized scope, published state, safe conversion path, measurable baseline and QA gates pass; ongoing rankings and AI citations are never release gates. A source update is not proof that every existing consumer automatically adopts it; normal authorized handbook bundle refresh and repo-local implementation remain separate.

**Exceptions:** regulated sectors, client privacy, platform eligibility and business truth take precedence over a generic template. Record deviations in the client project, not as silent changes to universal guidance.
