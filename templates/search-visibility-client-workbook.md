---
id: tpl-search-visibility-client-workbook
kind: template
status: active
owner: engineering
version: "1.0"
applies_to:
  - organic-search-services
  - client-business-websites
  - marketing-workflows
sources: []
last_verified: 2026-11-13
review_due: 2027-02-13
---

# Client search-visibility delivery workbook — COPY INTO AUTHORIZED CLIENT WORKSPACE

This is a **field template**, not an instruction to create a second CRM or to commit client records to the public Handbook. Reuse the client's approved project tracker and store any personal/financial data only in its authorized system. Procedure: [`pb-search-visibility-service-operations](../playbooks/search-visibility-service-operations.md). Technical authority: [`std-public-web-discoverability-baseline](../standards/public-web-discoverability-baseline.md).

## A. Engagement header and truth record

| Field | Value / evidence |
| --- | --- |
| Project ID / client-owned workspace | [ ] |
| Owner, editor, developer, reviewer, account manager | [ ] |
| Business legal name / trading name / approved aliases | [ ] |
| Primary market and sector / regulated advertising review | [ ] |
| Website canonical origin / CMS / hosting / deployment | [ ] |
| Real physical locations vs service area (owner-confirmed) | [ ] |
| Actual services/products and exclusions | [ ] |
| Customer jobs, primary audience and decision triggers | [ ] |
| Brand voice, licensed assets, testimonials and proof owner | [ ] |
| Contract scope, budget, capacity and reporting cadence | [ ] |
| Start date, observation baseline, release/rollback authority | [ ] |
| Approval owner and date for business claims | [ ] |

**Proof ledger:** each material claim (prices, years, vehicles, certifications, staff, results, service areas, reviews, hours, availability, guarantees) has `claim ID | exact claim | source | owner | verified date | publication rights | approved? | affected URLs`. If not approved, omit or qualify; never fill with illustrative client facts.

## B. Access and permissions — separate authorizations

| Capability | Owner | Access status | Permission / date | Constraint |
| --- | --- | --- | --- | --- |
| GitHub/site code or CMS | [ ] | [ ] | [ ] | [ ] |
| Production deploy / rollback | [ ] | [ ] | [ ] | [ ] |
| Domain / DNS | [ ] | [ ] | [ ] | [ ] |
| Search Console | [ ] | [ ] | [ ] | [ ] |
| Bing Webmaster | [ ] | [ ] | [ ] | [ ] |
| Google Business Profile | [ ] | [ ] | [ ] | [ ] |
| Bing Places / Apple Business Connect | [ ] | [ ] | [ ] | [ ] |
| Analytics/consent manager | [ ] | [ ] | [ ] | [ ] |
| CRM/qualified-lead metrics | [ ] | [ ] | [ ] | [ ] |
| Review responses / third-party corrections | [ ] | [ ] | [ ] | [ ] |
| Paid tools/outreach/external spend | [ ] | [ ] | [ ] | [ ] |
| Public claims/assets/content approval | [ ] | [ ] | [ ] | [ ] |

Statuses: `PASS` (authorized and verified), `NOT RUN`, `BLOCKED`, `OWNER ACTION`, `N/A`. **No passwords in this workbook.** Client owns accounts and access.

## C. Business goals and measurement contract

| KPI | Definition / source | Baseline period | Baseline value | Target as hypothesis | Limits |
| --- | --- | --- | --- | --- | --- |
| Qualified organic leads | CRM source + dedupe + qualification rule | [ ] | [ ] | [ ] | Attribution imperfect |
| Organic site clicks | GSC property, search type, geography, device | [ ] | [ ] | [ ] | Not sessions |
| Organic sessions | Consented analytics, source/medium definition | [ ] | [ ] | [ ] | Consent/sample effects |
| Non-brand impressions/clicks | GSC query cohort and filters | [ ] | [ ] | [ ] | Hidden/anonymized queries |
| GBP calls/website interactions | Eligible owner profile report | [ ] | [ ] | [ ] | Not all qualified leads |
| Ecommerce revenue/margin | Authorized transaction source | [ ] | [ ] | [ ] | Refunds, taxes, attribution |
| Field LCP/INP/CLS p75 | CrUX/RUM with coverage | [ ] | [ ] | [ ] | Field vs lab |
| AI citation sample | Fixed prompts, engines, repeats, URLs | [ ] | [ ] | [ ] | Observation, not rank |

Never write `0` for a missing source. Mark `NOT RUN` with reason. Do not promise numerical growth.

## D. Competitor/intent inventory

| ID | Query / user intent | Locale / device / date | Organic competitor URL | Observed evidence | Opportunity hypothesis | Primary target URL |
| --- | --- | --- | --- | --- | --- | --- |
| Q01 | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Cover brand, non-brand transactional, local, comparison, informational, seasonal and relevant AI-answer questions. Separate ads, local pack, organic links and AI citations. **Do not use sitemap URL counts as ranking evidence.**

## E. Route/indexability matrix

| URL / template | Class (public indexable / excluded / private / redirect / removed) | HTTP | Robots / X-Robots | Canonical | Sitemap | Internal links | GSC status (if authorized) | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| / | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| /servicio-ejemplo | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| /contacto | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| /gracias | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| /admin | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Inspect real served HTTP/HTML. A private route requires actual access control, not only `noindex`. An intentionally excluded page is not automatically a bug.

## F. Audit matrix — checklist with evidence

Use one row per observed failure; all items below are candidate checks, not universal implementation demands.

| Area | Check | Status | Evidence URL / timestamp | Risk / owner |
| --- | --- | --- | --- | --- |
| Technical | HTTPS/final host/redirects/404/410/5xx | [ ] | [ ] | [ ] |
| Technical | Robots groups and CDN/WAF verified access | [ ] | [ ] | [ ] |
| Technical | Meta robots and X-Robots-Tag route policy | [ ] | [ ] | [ ] |
| Technical | Canonicals and duplicates/parameters/facets | [ ] | [ ] | [ ] |
| Technical | XML sitemap/indices/lastmod factual | [ ] | [ ] | [ ] |
| Technical | JS-rendered vs initial HTML and real links | [ ] | [ ] | [ ] |
| Technical | Pagination, filters and internal site search | [ ] | [ ] | [ ] |
| Technical | hreflang, real translations, localized canonicals | [ ] | [ ] | [ ] |
| Search appearance | Titles/H1/descriptions and breadcrumbs | [ ] | [ ] | [ ] |
| Search appearance | Favicon/OG/Twitter/real preview images | [ ] | [ ] | [ ] |
| Structured data | Valid schema, real facts, eligible features | [ ] | [ ] | [ ] |
| Content | Query-to-URL map, uniqueness, helpfulness | [ ] | [ ] | [ ] |
| Content | Real author/proof, sources, rights, dates | [ ] | [ ] | [ ] |
| Content | Alt text by function, captions and media | [ ] | [ ] | [ ] |
| Internal links | No broken/orphan important pages; useful anchors | [ ] | [ ] | [ ] |
| Reputation | Genuine links/citations, no paid-link spam | [ ] | [ ] | [ ] |
| Local | GBP eligibility, real location/service area, profile | [ ] | [ ] | [ ] |
| Local | Bing/Apple listing if relevant; no duplicates | [ ] | [ ] | [ ] |
| Local | Reviews provenance/policy and owner permission | [ ] | [ ] | [ ] |
| Conversion | CTA, forms, phone, WhatsApp, errors, dedupe | [ ] | [ ] | [ ] |
| Conversion | CRM-qualified lead attribution and privacy | [ ] | [ ] | [ ] |
| Experience | Field CWV p75 vs lab and mobile UX | [ ] | [ ] | [ ] |
| Accessibility | Keyboard, 200% zoom, contrast, motion, AT | [ ] | [ ] | [ ] |
| Privacy | RGPD/LSSI/AEPD, consent and external embeds | [ ] | [ ] | [ ] |
| AI search | Google AI eligibility, OAI-SearchBot policy | [ ] | [ ] | [ ] |
| AI search | Prompt sample reproducibility / citations | [ ] | [ ] | [ ] |
| Release | Exact commit, deploy, host, rollback, smoke | [ ] | [ ] | [ ] |

For each `FAIL` create an issue in section G. For `NOT RUN` state tool/access/reason, not "passed".

## G. Prioritized issue / implementation register

| ID | Observed failure and evidence | Impact 1–5 | Confidence 1–5 | Effort 1–5 | Risk 1–5 | P0–P3 | Owner | Fix | Regression test | State |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| SEO-001 | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Indicative order `(impact × confidence)/(effort + risk)`; override for privacy/security/legal blockers. Use `observed` vs `inferred` vs `unknown`. Attach exact URL, headers, screenshot/log or GSC evidence; don't publish customer PII.

## H. Content brief — repeat per page

- Page owner, URL, purpose, real target customer, service/region and primary conversion: [ ]
- Query cluster and intent, target vs competing internal URLs: [ ]
- Current page and what will change (upgrade / consolidate / new): [ ]
- Primary answer (2–3 useful sentences, not artificial chunking): [ ]
- Distinct customer questions and constraints: [ ]
- Original proof: source, photo, case, license, client approval: [ ]
- Specific offer, conditions, exclusions, pricing facts if verified: [ ]
- Outline/H1/H2, internal links to genuine destinations, CTA: [ ]
- Metadata, canonical, schema eligibility, media alt/caption: [ ]
- Legal/sector/brand reviewer and date: [ ]
- Acceptance: content factual, accessible, no duplication, deployed route correct, form works: [ ]

## I. Local profile and citations ledger

| Provider | Existing listing URL / ID | Eligible? | Owner/permissions | Name/phone/area verified? | Duplicates? | Action authorized? | Live evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Google Business Profile | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Bing Places | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Apple Business Connect | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Sector-specific directory | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

No invented address, office, service area, hours or reviews. Owner approves public replies and corrections. For service-area businesses respect address visibility.

## J. AI-answer observation ledger

| Sample ID | Engine/surface | Exact prompt | Date/locale/location/account | Repeats | Brand mention | Direct citation URL | Factual accuracy | Competitors mentioned | Caveat |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| AI-01 | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Freeze cohort before comparing periods; record variance and sample size. AI citations ≠ rankings, clicks, referrals or leads. Do not put private customer details in prompts.

## K. Release/QA record

| Field | Evidence |
| --- | --- |
| Scope, PR and diff reviewed | [ ] |
| Claim/asset approvals and privacy gates | [ ] |
| Code SHA, deployment ID and environment | [ ] |
| Canonical + redirect host actual responses | [ ] |
| Public and private route tests | [ ] |
| Sitemap, robots, canonical, JSON-LD | [ ] |
| Internal navigation and form test method (isolated vs production) | [ ] |
| Mobile/desktop/browser/zoom/keyboard | [ ] |
| Performance field/lab conditions and results | [ ] |
| Third-party profile updates actually published | [ ] |
| Rollback reference and observation window | [ ] |
| Remaining FAIL / NOT RUN / OWNER ACTION | [ ] |
| Client approval / release owner | [ ] |

Do not claim `READY` or `PASS` based solely on source code or a Vercel status. Observe the served site and exact revision. For real client forms use safe test isolation; no fake production Jobs.

## L. 30/60/90-day and monthly operations

**30 days:** close approved P0/P1 technical issues, establish reliable measurement and owner actions, prioritize one or two high-value pages, validate forms and local listing truth. **60 days:** expand useful intent coverage, correct citation mismatches with permission, gather genuine proof and inspect early indexing/lead patterns. **90 days:** evaluate matched-period search/lead trends and scope, continue only evidence-backed experiments. Dates are planning checkpoints, not promised ranking deadlines.

Monthly decision: `continue / change priority / stop experiment / request owner action / new quote`. Track committed hours, actual hours, external costs, evidence and next risk. The agency owns work quality; engines and market demand are outside its control.

## M. Closure and handoff

- [ ] Client owns domain, profiles, code/content rights and reporting exports per agreement.
- [ ] Final audit, release revision, delivered work and unresolved items documented.
- [ ] Permissions and credentials handed off/revoked appropriately.
- [ ] Paid services, consent mechanisms and subscriptions identified; no silent ongoing charges.
- [ ] No client personal records, passwords or confidential economics committed to the Handbook.
- [ ] Any generalizable learning submitted through Handbook knowledge promotion, not copied wholesale.
