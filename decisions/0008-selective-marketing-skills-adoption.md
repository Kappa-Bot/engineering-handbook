---
id: adr-0008-selective-marketing-skills-adoption
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - marketing-workflows
sources:
  - src-marketingskills
  - src-boe-lssi
  - src-eu-gdpr
  - src-aepd-cookie-guide
  - src-google-ai-features
  - src-google-analytics-pii
last_verified: 2026-11-09
review_due: 2027-02-09
---

# Selectively adopt Marketing Skills procedures

## Context and authorization

On 2026-11-09 the owner authorized integrating prioritized procedures from `coreyhaines31/marketingskills` and making the Handbook consistent. This authorizes Handbook source changes, not plugin installation, new accounts, schedulers, spending, outbound contact or changes to products/CRM.

The inspected upstream revision is `96798cf38736ecdba015a1d2b0521b0c8f8f41dd` (2026-11-06). `ref-marketing-skills-adoption-assessment` records observed versions, ownership, evidence limits, evaluation scenarios and the MIT notice. `src-marketingskills` is Tier B for its original implementation/framework, not independent proof of effectiveness or legal authority.

Existing public-client delivery and discoverability guidance already owns implementation, truthful proof, indexing and release checks. Importing an external catalog as parallel policy would duplicate that authority. Missing reusable procedures concern marketing context/content, evidence-backed qualification/handoff, and conversion measurement/experiments.

## Decision

1. Adopt original, scoped synthesis of product-marketing, cro, copywriting, seo-audit, prospecting, conversion-tracking, site-architecture, revops, ai-seo, competitor-profiling, sales-enablement and ab-testing. Use schema and copy-editing only as supporting references; use cold-email only for internal drafting, never sending. Unresolved channel permission keeps a draft explicitly unapproved for sending.
2. Establish `pb-marketing-context-and-content`, `pb-lead-qualification-and-handoff`, `pb-conversion-measurement-and-experiments` and `tpl-product-marketing-context` as the new canonical owners for those gaps. Keep real business facts, audience decisions, records and approvals local; do not impose upstream context-file locations.
3. Preserve `std-public-web-discoverability-baseline`, `pb-public-web-discoverability-launch`, `pb-public-client-website-delivery` and existing truth/UI/reviews/design/security/verification policies as their topics' authorities. Link to them rather than copying universal rules. No generic heuristic or marketing target overrides a product owner's approved decision.
4. Use the existing single generic Handbook router and progressive disclosure. Do not create parallel domain skills, replace Agency Agents, change runtime/model routing, or install the upstream plugin, tools, hooks or CLIs.
5. Apply Spain/EU legal and consent gates using the registered official sources. Public contact details, valid email delivery and licensed data do not establish permission to send marketing. Separate GDPR processing requirements from LSSI-CE channel requirements. Tracking requires its own approved data/consent contract; hashing/server-side delivery is not an exemption.
6. Keep observed, inferred, proposed and unverified claims distinct. Measure confirmed outcomes rather than button clicks; verify destination receipt when authorized and report unrun gates explicitly. Preserve noindex/demo boundaries and do not guarantee ranking, AI citation, commercial uplift or statistically decisive results.
7. Preserve MIT attribution and the permission notice in the assessment for adapted workflow material. Evaluate separately credited works and any future executable adoption under normal external-solution and dependency/supply-chain review.

## Alternatives considered

- **Install/import the whole catalog:** rejected for this scope; expands instructions, dependencies and maintenance without consumer evidence or installation authority.
- **Create one marketing standard duplicating SEO, UI and truth requirements:** rejected; conflicts with one canonical owner per topic.
- **References only, with no reusable procedure:** insufficient for the approved integration because context, qualification/handoff and measurement gaps remain.
- **Selective procedures through existing routing and owners:** selected; fills the gaps while retaining existing authority and consumer decisions.

## Consequences, validation and maintenance

The Handbook maintains the selected procedures, template and routing/tests, not every upstream module or partner tool. Numeric upstream examples, statistical tables, vendor studies, fixed SLAs and platform claims are not universal requirements. Nonselected modules remain unadopted. New services, recurring work, customer data processing and external mutations require their own authority.

Validate with the three scenarios in `ref-marketing-skills-adoption-assessment`: Spanish business qualification without unauthorized outreach, a truthful noindex client demo, and confirmed/deduplicated form measurement with an honest low-traffic experiment decision. Tests and review provide only the evidence actually observed; no revenue, conversion-rate or cost improvement is asserted.

The public Handbook contains sanitized methods, not leads, CRM exports, interviews, credentials or confidential commercial evidence. Protect private records independently of robots directives and keep their processing/retention boundaries explicit.

Source delivery, merge or publication does not establish an installed consumer revision, a workstation refresh or product rollout. Consumers adopt through their normal authorized Handbook refresh; verify actual revision and routed behavior through `pb-codex-handbook-skill-adoption` / `pb-repository-adoption` before claiming adoption. This decision does not reopen product launch gates or automatically modify consumers.

Review by 2027-02-09 or on a material source/legal/data-boundary change, contradictory evidence or consumer failure. Future updates require a pinned diff/applicability review, not automatic synchronization. Existing source-authority, knowledge-promotion and runtime controls remain in force.
