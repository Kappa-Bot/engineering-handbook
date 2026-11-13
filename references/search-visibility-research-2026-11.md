---
id: ref-search-visibility-research-2026-11
kind: reference
status: active
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - organic-search-services
  - marketing-workflows
  - client-business-websites
sources:
  - src-google-seo-starter-guide
  - src-google-search-essentials
  - src-google-spam-policies
  - src-google-block-indexing
  - src-google-sitemaps
  - src-google-ai-features
  - src-google-ai-generative-performance
  - src-google-web-multimodal-performance
  - src-google-ai-optimization
  - src-google-sitelinks
  - src-google-local-ranking
  - src-google-business-profile-guidelines
  - src-google-review-structured-data
  - src-google-international-hreflang
  - src-google-product-structured-data
  - src-google-organization-structured-data
  - src-bing-ai-performance
  - src-openai-web-crawlers
  - src-indexnow-protocol
  - src-w3c-wcag-22
  - src-webdev-core-web-vitals-thresholds
  - src-aepd-cookie-guide
  - src-eu-ai-act
last_verified: 2026-11-13
review_due: 2027-02-13
---

# Search visibility research synthesis — Spain, November 2026

## Provenance, limitations and intended use

This is a **non-normative, cross-sector research ledger** derived from the November 2026 investigation and challenged against the Handbook's existing search standard, official provider guidance and the realities of Spanish SME delivery. It does not assert that the linked tools, services, training materials or business accounts are connected, purchased or operational. Its reusable operating procedure is [`pb-search-visibility-service-operations](../playbooks/search-visibility-service-operations.md); the technical norm remains [`std-public-web-discoverability-baseline](../standards/public-web-discoverability-baseline.md).

**Evidence classification:**
- **A — documented:** official search-engine/platform/specification behavior, subject to version and availability.
- **B — measured locally:** reproducible observation with URL, date, device, locale, sample size and tool; describes that site/sample, not all Google users.
- **C — professional hypothesis:** plausible tactic based on practitioner studies, competitor observation or experience; test before selling it as proven.
- **D — unverified/false shortcut:** unsupported causal or ranking claim; reject or investigate without promising value.

**Research boundary:** a public competitor's `robots.txt`/sitemap/HTML reveals declared configuration and accessible pages, not the pages actually indexed, their organic traffic, backlinks, Google sitelinks, conversions or the cause of their rank. A service price published by an agency is that provider's claim, not a market transaction dataset. The previous investigation contained overconfident statements; corrections below are deliberate and take precedence over its draft.

## 1. What is established and what is not

| Topic | Stronger evidence | Safe operational conclusion | Reject |
| --- | --- | --- | --- |
| Search eligibility | `src-google-search-essentials`, `src-google-seo-starter-guide` | Accessible, useful, compliant content is eligible; crawling, indexing and serving are independent decisions | "Sitemap guarantees indexing" |
| Index controls | `src-google-block-indexing` | `robots.txt` controls crawl access; `noindex` controls index eligibility when the crawler can read it; private data needs authentication | "Disallow protects private pages" |
| Sitemaps | `src-google-sitemaps` | Include intended canonical URLs; real `lastmod` may help; XML URL count is inventory | "More URLs or daily changefreq boosts rankings" |
| Canonical | Google Search Central | Canonical is a signal, not an unconditional command; check selected canonical in authorized GSC | "Canonical tag forces Google" |
| Sitelinks | `src-google-sitelinks` | Good navigation, descriptive headings/anchors and useful destinations may help engine-selected sitelinks | "Schema can set sitelinks" |
| Page titles | Google Search Central | Write distinct, accurate titles/snippets for people; engine may rewrite them | "Exactly 60 characters required" |
| E-E-A-T | Google's people-first guidance | Demonstrate authentic experience, expertise, authority and trust, especially in YMYL; these are evaluative concepts | "E-E-A-T is one numerical ranking factor" |
| Local search | `src-google-local-ranking` | Relevance, distance and prominence matter; owner-controlled eligibility/accuracy is foundational | "A fixed NAP punctuation difference causes a penalty" |
| Structured data | `src-google-organization-structured-data` and feature-specific docs | Match visible verified facts; validate eligibility per feature | "Schema is a direct AI ranking API" |
| Reviews | `src-google-review-structured-data` and GBP policy | Real, policy-compliant reviews can inform users; self-serving stars are not an eligible rich-result shortcut | "Any `aggregateRating` gets stars" |
| Performance | `src-webdev-core-web-vitals-thresholds` | Field p75 LCP, INP, CLS plus business UX; lab and field differ | "FID is still a current Core Web Vital" |
| Google AI | `src-google-ai-features` | Google documents no special AI-only file/markup requirement for AI Overviews/AI Mode; Search eligibility matters | "`llms.txt` guarantees AI Overview citations" |
| OpenAI crawlers | `src-openai-web-crawlers` | `OAI-SearchBot` search, `GPTBot` training, `ChatGPT-User` user-triggered access are distinct controls | "Training bot must be allowed to appear in ChatGPT Search" |
| AI citations | Engine-specific documentation and repeatable observation | Citations are probabilistic, query/context-dependent, not a promised output | "One favorable prompt proves visibility growth" |
| FAQ/HowTo | Current Google feature eligibility | Useful visible FAQs may help readers; markup is not a general rich-result entitlement | "FAQ schema is a ranking lever" |
| Link acquisition | `src-google-spam-policies` | Earn genuine relevant editorial references; disclose sponsorship and follow policies | "Buying dofollow links guarantees authority" |
| Language | `src-google-international-hreflang` | Maintain genuinely localized URLs and valid `hreflang`; Catalan is `ca` or `ca-ES`, not `cat` | "Translate metadata only and call it multilingual SEO" |

**Important Google measurement update (2026).** Google announced **dedicated Search Console generative-AI performance reports for Search and Discover on 3 June 2026**, globally rolled out by **31 August 2026**. They report AI-feature impressions, pages, countries, dates and device information for Search; the same visibility is also included in overall performance data. Google introduced multimodal Search filters in September 2026, with data when relevant traffic exists. Inspect the actual authorized property and metric definitions: an impression is **not** a citation click, lead or sale; no data is not proof of zero visibility. Do not infer AI referrals from a generic Google organic click. See `src-google-ai-generative-performance`, `src-google-web-multimodal-performance`, `src-google-ai-features` and `src-bing-ai-performance`.

## 2. Technical body of knowledge and audit order

### 2.1 Crawl and rendering

Learn HTTP semantics and status codes first: 200, 301/308, 404, 410, 429, 5xx; redirects, TLS, host, caching, content negotiation, Vary, WAF, CDN, mobile rendering, JS hydration and critical HTML. Robots is a publicly readable crawl policy; separate robots groups can be narrower than `User-agent: *`. Test bot access with verified published IP ranges and logs, not a spoofed User-Agent header.

Operational chain: `DNS/HTTPS → final host/redirect → HTTP status → robots crawl policy → actual HTML/DOM → index directive → canonical → internal link discovery → sitemap → engine index status`. The chain is not guaranteed to end in indexing; each link can fail independently.

For a site migration, inventory old URLs and referring links, map exact 1:1 or nearest genuinely relevant replacements, test redirect chains and canonical consistency, maintain old host as required, and monitor GSC/logs over a realistic observation period. Do not redirect every missing page to the homepage or silently delete an old fallback.

### 2.2 URL architecture and search intent

Classify site type and inventory templates: homepage, service, area, product, category, editorial, FAQ, about, legal, contact, case study, event, filtered search, pagination, locale and private routes. Assign each commercially important intent to a primary useful page. Navigation and contextual links should expose it. Duplicate variants may need consolidation, canonical, noindex or true differentiated content depending on actual intent and crawl budget; **no single rule applies to every parameter**.

Competitor analysis should compare **coverage quality**: which distinct user jobs and locations are answered with evidence, not count of XML entries. A 500-URL sitemap may include duplicates, old posts, cart/account pages or weak content; a 15-URL site may still be technically excellent but commercially narrow.

### 2.3 Structured data and entity

Understand `schema.org` vocabulary versus **Google-supported rich results**: a valid type may have no Google presentation feature. Use stable IDs and URLs for actual entity, website, service and authors, without conflating legal entity, trading brand, agency or customer. Verify real reviews, ratings, opening hours, licenses and locations before markup. Keep client identity and domain in the client repository, not in a universal template. Review markup must meet eligibility rules; a self-serving `LocalBusiness` review aggregate is not a star shortcut.

For publishers, distinguish actual author credentials from pseudonymous/automated authors; an author byline does not manufacture expertise. `dateModified` must reflect real content changes, not a build date.

### 2.4 Images, video, mobile and accessibility

Use real assets with rights, alt text based on **function** (informative image = accurate description; decorative = `alt=""`), captions when useful, responsive dimensions, sensible `srcset`/`sizes`, no LCP lazy loading, real OG preview and a legible favicon. Test 320–desktop widths relevant to the actual layout, 200% zoom, keyboard and assistive technologies where available. WCAG conformance is not certified by Lighthouse alone. For moving carousels, evaluate pause/stop/hide and reduced motion against actual WCAG requirements; design approval does not waive accessibility obligations.

Core Web Vitals are field **p75** signals: LCP good ≤2.5s, INP good ≤200ms, CLS good ≤0.1. FID was replaced by INP. Segment mobile/desktop, samples and page types; a small lab median is not field p75.

## 3. Search content, topical coverage and reputation

**Evidence-first content**: a page should answer the real customer's question better than a generic competitor result. Verify the service, eligibility, exclusions, price factors, response process, qualifications, proof, service area and next step. Show original observations, photos/case details, examples and updated sources when available. Content can be AI-assisted editorially but requires factual and legal review. No mass-published near-duplicate location pages, scraped summaries, keyword stuffing, fake FAQs, generic "best in town" claims or invented testimonials.

**Commercial intent ladder:** awareness (problem), comparison (alternatives and price factors), decision (service/eligibility/real proof/CTA), aftercare (instructions and support). A blog that never links meaningfully to real service pages may be low-value for leads. Equally, a pure sales page may not answer pre-purchase questions.

**External reputation:** accurate business profiles, legitimate directories that users actually consult, sector associations, local partnerships and earned editorial coverage. A "citation" (NAP mention) and a backlink are different. A nofollow link may still have referral and brand value. Link metrics such as DR/DA are third-party estimates, not Google's public ranking score.

## 4. Spain-specific operating branches

### Service-area businesses

Check GBP eligibility, service area, address visibility, official name and actual categories. A sole trader with a registered home address does not automatically have a public storefront. Do not embed an invented map pin. Distinguish telephone lead from qualified quote and closed job. Verify municipal/sector regulations before publishing procedural claims.

### Professional services, healthcare, legal and finance

YMYL content has high stakes. Require licensed/professional reviewer where applicable, date, jurisdiction, actual qualifications, professional advertising compliance and privacy. Avoid medical outcome claims, false guarantees, case-identifying details and automated publication of personal histories. Structured data cannot substitute for professional verification.

### Ecommerce

Inventory catalog and business rules: product availability, price, tax/shipping/returns, canonical category hierarchy, product variants, filters, pagination, discontinued items, product schema and Merchant Center/feed consistency. Use robots/canonical/noindex deliberately for facets and internal search; not every filter should index. For products with variants, preserve genuinely useful canonical targets; do not collapse different products blindly. Track organic **revenue and margin** with lawful measurement, not only sessions.

### B2B and SaaS

Optimize for qualified problem/industry/service searches, genuine product maturity, comparison pages with fair evidence, documentation and case studies. A demo, waitlist or mocked feature is not a shipped capability. Track pipeline stages and attribution limitations rather than counting every visit as a sales opportunity.

### Tourism, hospitality, multi-location and multilingual

Real location/property pages need distinct inventory, availability and policies. Seasonal demand and locale-specific terminology matter. Spanish and Catalan pages require full useful localization and `hreflang`, not empty translated shells; `ca-ES` is a valid tag, `cat` is not. Include `x-default` only when it corresponds to a real fallback. For multi-country, verify country, currency, taxes, service eligibility and translated legal claims.

### Education, public-interest and nonprofit

Use accurate dates, program requirements, admissions, fees and accessibility; event structured data only for real events. The primary outcome may be applications, registrations or participation, not sales. Follow privacy obligations for minors and sensitive contexts.

## 5. AI-assisted search: sober method

AEO/GEO/LLMO are evolving labels, not a single official standard. Provider controls differ:

| Provider surface | Primary documented control | What can be measured | What cannot be guaranteed |
| --- | --- | --- | --- |
| Google Search / AI Overviews / AI Mode | Googlebot + ordinary Search eligibility, snippet controls | Web data + dedicated generative-AI Search/Discover impressions/pages/country/date reports (2026); multimodal filters when relevant | A specific AI answer/citation or separate AI-only CTR |
| Bing / Copilot | Bing crawl/index rules, Webmaster Tools, IndexNow for supported URLs | Bing Webmasters data, AI Performance where available | Instant indexing or Copilot endorsement |
| ChatGPT Search | `OAI-SearchBot` policy and reachable public content | Observed source URLs/referrals where accessible | That GPTBot permission improves Search |
| Other answer engines | Each engine's own official rules | Repeatable sampled prompt/answer observations | Stable inclusion across users or model versions |

**AI visibility experiment:** freeze a query cohort (e.g. 20–30 real buyer questions across brand, service, comparison, local and troubleshooting); document language, geography, engine, date, account/personalization, exact prompt and repeat count. Capture mention, direct URL citation, factual accuracy, competitor mentions and variance. Report numerator/denominator, not a made-up "AI rank"; keep search clicks and qualified leads in separate columns. Changes in model or prompt mix invalidate simple before/after comparisons.

**Optional protocols:** `llms.txt` is a community proposal, not a Google/OpenAI requirement; Markdown negotiation and HTTP Link metadata can serve legitimate agent clients but are not proven ranking factors. Preserve canonical HTML, robots, access control, caching and content parity. Never disclose private client records to an "AI crawler" or build an API just for GEO hype.

## 6. Legal, privacy and ethics for Spain

Use the existing [`std-public-website-legal-trust-baseline](../standards/public-website-legal-trust-baseline.md), `src-aepd-cookie-guide` and applicable EU/Spanish legislation. Record the controller, processor, lawful basis, privacy notice at collection, retention, processors/transfers, data subject rights, marketing permissions and data minimization. Non-essential cookies/tracking generally need valid prior consent; **a cookie banner is not universally required when only exempt strictly necessary technologies are used**. Do not install GA4/GTM/call recording/pixels/third-party maps without the client's legal and technical approval. Do not put raw PII into search prompts, audit reports or public examples.

Legal pages should remain accessible to visitors regardless of whether a site chooses to index them; legal review decides content and obligations, not a blanket SEO preference. Sector regulations and EU accessibility obligations may impose stronger requirements than this research summary; legal advice is an independent professional task.

No fake reviews, selective review gating, paid endorsements disguised as organic, scraped personal details, falsified schema, link networks, fabricated service locations or deceptive comparisons. Protect confidential clients and media rights. A legitimate case study requires explicit permission and proof.

## 7. Training and continuous learning syllabus

The recommended order is **foundations → verification → specialization → experiments**. Record completion with a hands-on artifact, not a certificate screenshot.

| Module | Primary / useful training material | Practical exam |
| --- | --- | --- |
| Search foundations | Google Search Central SEO Starter Guide, Search Essentials, Search Central documentation and official Search Central videos | Explain crawl vs index vs serve; inspect 10 URLs and report evidence |
| HTTP/technical SEO | RFC 9110, robots `src-google-block-indexing`, sitemap `src-google-sitemaps`, Google canonical/JS docs | Diagnose robots/noindex/canonical/redirect conflict without exposing private routes |
| Search Console | Google Search Console Help, URL Inspection, Performance, Page Indexing | Produce baseline with filters/date/device and limitations |
| Local SEO | Google Business Profile eligibility/guidelines, `src-google-local-ranking`, Bing Places | Distinguish storefront vs service-area business; identify real duplicate and permissions |
| Content / editorial | Google's people-first content guidance and spam policies; Diátaxis for documentation | Draft one factual service page and one evidence-backed case study |
| Structured data | Schema.org + Google feature-specific docs and Rich Results Test | Build and validate truthful graph; reject ineligible self-serving review markup |
| Performance / accessibility | web.dev Core Web Vitals, W3C WCAG 2.2 and WAI APG | Diagnose LCP/INP/CLS field vs lab; keyboard/zoom/image alternatives |
| Ecommerce | Google Search Central ecommerce docs, Product structured data, Merchant Center official docs | Audit a category, a variant, a facet and a discontinued product |
| International | Google's localized versions / hreflang guidance | Test `es-ES` / `ca-ES` and canonical/hreflang reciprocity |
| AI search | Google AI features, OpenAI crawler docs, Bing AI Performance | Separate search/training bots; run a repeatable, honest citation sample |
| Analytics / privacy | Google Analytics official learning, AEPD cookie guidance, RGPD/LSSI | Define consent-safe lead attribution with zero PII leakage |
| Agency economics | Source-specific Spanish price benchmarks + internal time ledger | Quote a scope with hours, QA, exclusions, margin and no ranking promise |

**Secondary learning options:** Ahrefs Academy, Semrush Academy, LearningSEO.io, Search Engine Journal/Land, SEOFOMO, sector events, practitioner case studies and books. These are useful for discovering hypotheses and tools, **not authority for a cross-repository MUST**. For books/courses, record edition/date because search engines change faster than printed material. Practical competence is demonstrated by a documented audit and safe production delivery, not the number of certificates.

### Skill progression

- **Level 1 (auditor):** can produce a reproducible crawl/index/canonical audit and distinguish fact from inference.
- **Level 2 (implementer):** can fix a scoped issue with tests, staging, rollback and post-release verification.
- **Level 3 (strategist):** can map intent to real business offers, prioritize with economics, design local/content strategy and avoid doorway spam.
- **Level 4 (service lead):** can price and scope ethically, coordinate legal/owner gates, measure qualified outcomes, coach reviewers and revalidate evolving AI features.

Assess with three varied simulated briefs (e.g. local trade, regulated clinic, multi-locale ecommerce), not only a single moving company. Require one intentionally blocked test to verify the learner can say `NOT RUN`.

## 8. Rejected or unverified claims from the preliminary research

The initial research draft is **not a publication-ready standard**. In particular, do not promote the following statements:

1. "All informative images need a descriptive alt; decorative images must also have text." Decorative images appropriately use `alt=""`; the alt decision depends on function.
2. "FID is the current Core Web Vital." Current interaction metric is **INP**.
3. "Allow GPTBot to be cited in ChatGPT Search." Training and search controls are distinct.
4. "AI Overviews require FAQPage/HowTo/Person schema or llms.txt." Google's own AI-features guidance says no special markup/files.
5. "Search Console has no separate generative-AI performance reports" or "every property has nonzero AI visibility." Google introduced dedicated reports in 2026; inspect the actual property, reporting scope and data before making claims.
6. "site:domain proves all pages indexed." It is an approximate diagnostic; URL Inspection/Page Indexing are more appropriate when authorized.
7. "Google local ranking uses reviews as its fixed second factor." Google describes relevance, distance and prominence; there is no public fixed universal factor ordering.
8. "Every business must publish its fiscal/home address and embed a Google Map." Service-area businesses and privacy/eligibility can require different public presentation.
9. "Create one local page for every city with a keyword swapped." Doorway content can violate search spam policies.
10. "Every FAQ schema yields featured snippets, every rating yields stars." Rich result eligibility and actual display are separate.
11. "An exact title/description character count or keyword density improves rank." No universal fixed-length or density rule.
12. "A sitemap's 500 URLs means 500 ranked/indexed pages." False; it lists publisher-submitted URLs.
13. "An AI-generated case study or sample price can be published as a real client fact." False; owner evidence and permission required.
14. "Google requires a new `llms.txt` for AI search." False according to current primary guidance.
15. "An increase in one lab LCP sample proves field performance improvement." False; report conditions, distribution and field p75.
16. "SEO agencies can guarantee a minimum traffic increase by contract." The agency may commit **work and measurement**, not uncontrollable outcomes.
17. "Use invented Agurto business facts (20 years, guardamuebles, a fabricated street/CIF) as templates." **Never** use them. A case example cannot authorize claims.
18. "GBP exact punctuation matches across every directory or Google penalizes it." Preserve consistent identity, but do not claim an automatic punctuation penalty.
19. "A green deployment and successful unit tests prove search indexation." No; they prove only their tested scope.
20. "Paid placements and bulk guest posts are automatically earned authority." No; assess editorial merit, sponsorship and search spam policy.

## 9. Evidence and revalidation register

For each volatile claim, record `source ID | URL | exact claim | published/updated date if shown | date actually checked | scope | evidence tier | known limits | owner | next review`. Do not silently carry forward stale screenshots or tool labels. When a provider changes a product, first update the reference/evidence, then adjust the canonical standard/playbook only if the new behavior is actually verified and generally applicable.

**Official source anchors:** Google Search Central SEO Starter Guide (`src-google-seo-starter-guide`), Search Essentials (`src-google-search-essentials`), spam policies (`src-google-spam-policies`), AI features (`src-google-ai-features`), local ranking (`src-google-local-ranking`), sitemap (`src-google-sitemaps`), sitelinks (`src-google-sitelinks`), OpenAI crawler policy (`src-openai-web-crawlers`), Bing AI Performance (`src-bing-ai-performance`), W3C WCAG (`src-w3c-wcag-22`), web.dev CWV (`src-webdev-core-web-vitals-thresholds`) and AEPD (`src-aepd-cookie-guide`). Source URLs and review dates are registered centrally in `machine-readable/sources.yaml`.

**Market and service design:** the separate [Spain price reference](search-visibility-pricing-spain-2026-11.md) labels vendor self-report, sample limitations and MelodIQ hypotheses. Neither its numbers nor this research automatically set the agency's public price list or create a client commitment.
