---
id: tpl-search-visibility-monthly-report
kind: template
status: active
owner: engineering
version: "1.0"
applies_to:
  - organic-search-services
  - marketing-workflows
  - client-business-websites
sources: []
last_verified: 2026-11-13
review_due: 2027-02-13
---

# Monthly organic visibility report — evidence-first template

**Client:** [ ] · **Site/property:** [ ] · **Period:** [ ] · **Compared with:** [ ] · **Prepared/reviewed by:** [ ] · **Release SHA(s):** [ ].

## Executive result

- **Delivered work:** [3–5 specific changes with PR/release/URL evidence].
- **Business outcome:** [qualified leads/orders/revenue with authorized source, or `NOT RUN`].
- **Search visibility:** [matched-period GSC/Bing data with filters and limitations].
- **Local visibility:** [GBP/Bing Places data where authorized, or `OWNER ACTION`].
- **AI-answer observations:** [sample size, engines, citation/accuracy results, limitations, or `NOT RUN`].
- **Risks/blockers:** [P0/P1, platform account access, owner approvals, legal, technical].
- **Next decision:** [continue, reprioritize, approve scope, or stop unproductive experiment].

## KPI table — never substitute missing data with zero

| Metric | Definition/source | Previous | Current | Change | Sample/filter/limitations |
| --- | --- | ---: | ---: | ---: | --- |
| Qualified organic leads | CRM qualification + dedupe | [ ] | [ ] | [ ] | [ ] |
| Won deals / revenue from organic | Authorized sales source + attribution model | [ ] | [ ] | [ ] | [ ] |
| GSC organic clicks | Property, Web search, locale/device | [ ] | [ ] | [ ] | [ ] |
| GSC impressions | Same property/filter/date range | [ ] | [ ] | [ ] | [ ] |
| CTR | Clicks / impressions, same cohort | [ ] | [ ] | [ ] | [ ] |
| Average position | GSC query/URL cohort; not exact rank | [ ] | [ ] | [ ] | [ ] |
| Brand vs non-brand | Explicit query definition and data limitations | [ ] | [ ] | [ ] | [ ] |
| Indexed priority URLs | GSC inspection/coverage if authorized | [ ] | [ ] | [ ] | [ ] |
| Bing clicks/impressions | Bing Webmaster scope | [ ] | [ ] | [ ] | [ ] |
| GBP interactions | Owner property and reporting scope | [ ] | [ ] | [ ] | [ ] |
| Field LCP/INP/CLS p75 | CrUX/RUM with sample coverage | [ ] | [ ] | [ ] | [ ] |
| GSC generative-AI impressions | Dedicated Search/Discover reports; property and filters | [ ] | [ ] | [ ] | [ ] |
| AI citations/mentions | Fixed prompt cohort with repeats | [ ] | [ ] | [ ] | [ ] |
| Organic referral conversions | Consent-approved analytics/CRM | [ ] | [ ] | [ ] | [ ] |

**Definitions:** impressions are not visits; GSC clicks are not necessarily analytics sessions; leads are not sales; AI citations are not clicks; `site:` is not a reliable index count. Missing tools are `NOT RUN`, not `0`. Field metrics are not lab measurements.

## Implementation evidence ledger

| Issue / page | Before and after evidence | Change / PR | QA gate and status | Production URL / SHA | Owner |
| --- | --- | --- | --- | --- | --- |
| [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

## AI-answer sampling, if contracted

- Fixed cohort ID and buyer-intent categories: [ ]
- Engine/model/surface, date, locale, location, logged-in/personalization: [ ]
- Number of prompts × repeats; any missing responses: [ ]
- Brand mentions: [numerator/denominator]; **direct URL citations**: [numerator/denominator]; accuracy errors: [count/examples redacted].
- Comparator cohort and variance: [ ]. No inference from one prompt.
- Bing AI Performance, **Google Search Console's dedicated 2026 generative-AI Search/Discover impressions** and multimodal filters: report actual authorized property, scope and data, or `NOT RUN`. These are not direct evidence of a cited answer being clicked.
- No fabricated "AI ranking" or claim of guaranteed citation.

## Conversion and commercial truth

- Lead deduplication and source of truth: [ ]
- Source/medium attribution method, consent coverage and caveats: [ ]
- Offline/phone/WhatsApp enquiries counted how: [ ]
- Qualified vs spam/unqualified vs won: [ ]
- Changes in client capacity, seasonality, paid campaigns or site migrations: [ ]
- Observed causal evidence vs correlation: [ ]

## Work, time and next priorities

| Workstream | Committed hours/output | Actual delivered | Evidence | Next action |
| --- | --- | --- | --- | --- |
| Technical / QA | [ ] | [ ] | [ ] | [ ] |
| Content / local | [ ] | [ ] | [ ] | [ ] |
| AI observations | [ ] | [ ] | [ ] | [ ] |
| Coordination / reporting | [ ] | [ ] | [ ] | [ ] |

**Owner actions:** [access, business facts, content approval, profile changes, no forced re-asking].  
**Risks:** [severity, owner, deadline, rollback or mitigation].  
**Next 30 days:** [max 3 evidence-based priorities with acceptance tests].  
**Sign-off:** [reviewer/date, client acceptance if contracted].

## Auditability and communication rules

Every chart/table needs a source, date range, property/filter, collection method and limitations. Don't compare mismatched seasonal windows as if causal. Don't invent GSC AI-only impressions, field metrics, Google rankings or business sales. A screenshot of an AI answer is a single observation; a crawler permission change is not proof of AI citation. Protect personal data and client confidential economics.
