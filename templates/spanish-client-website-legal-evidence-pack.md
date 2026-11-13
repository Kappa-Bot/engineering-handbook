---
id: tpl-spanish-client-website-legal-evidence-pack
kind: template
status: active
owner: engineering
version: "0.1"
applies_to:
  - client-business-websites
  - public-marketing-websites
  - spain
  - lead-generation
sources:
  - src-boe-lssi
  - src-eu-gdpr
  - src-aepd-cookie-guide
  - src-aepd-privacy-clause-faq
  - src-eu-ai-act
  - src-boe-accessibility-11-2023
last_verified: 2026-11-13
review_due: 2027-02-13
---

# Client evidence pack — Spain, informational website with quote/contact form

**Copy into the authorised client repository or private compliance workspace; do not complete it with private client data in the public Handbook.** Use with [the canonical legal/trust standard](../standards/public-website-legal-trust-baseline.md) and [the audit playbook](../playbooks/spanish-client-website-privacy-consent-audit.md). Bracketed fields mean **unknown**, not approved.

## A. Scope and identity

- Client / verified legal operator: [ ]
- Legal form, NIF/CIF, address, direct contact, registry/regulated details if applicable: [ ]
- Controller contact and rights channel; DPO if legally required: [ ]
- Client approver / legal adviser and approval date: [ ]
- Website domains, languages, deployment SHA, environment: [ ]
- Mode: [ ] demo  [ ] prelaunch  [ ] commercial
- Services offered: [ ]
- Commercial conversion: [ ] contact  [ ] quote  [ ] call  [ ] booking  [ ] binding online contract  [ ] payment
- Explicit **no-checkout/no-payment** confirmation if true: [ ]
- Sensitive sector / minors / regulated-profession branch, if applicable: [ ]
- Evidence for legal identity and factual claims: [ ]

## B. Processing and provider inventory

Add one row per actual purpose and recipient; remove irrelevant example rows.

| Purpose / user action | Personal data and attachments | GDPR basis + reasoning | Controller / processor / recipient | Country / transfer | Retention / deletion | User notice | Evidence status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Requested quote/contact | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Hosting/edge/security logs | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Draft form/optional photos | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| CRM / email notification | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Optional analytics | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Optional marketing / attribution | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Optional AI / third-party embeds | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Per-provider record: [vendor/product, account/plan owner, role for each processing purpose, DPA URL/version/applicability, contract acceptance, subprocessor list and notice, actual region, Chapter V mechanism, retention vs dashboard history, deletion assistance, access and incident contact].

- Agency processes data under client instructions? [ ] yes  [ ] no  [ ] unresolved
- Controller–agency DPA needed and evidenced? [ ]
- Agency/provider and/or controller/provider contractual chain evidenced? [ ]
- EU-US DPF certification/scope or SCCs/other transfer basis actually verified? [ ]
- Real retention period/criteria approved for leads, photos, logs, backups and analytics? [ ]
- Access, upload validation, private storage, incident response and deletion controls evidenced? [ ]

## C. Public legal surfaces and purpose separation

| Surface | Applicable? | URL / screenshot | Controller approved? | Evidence / unresolved facts |
| --- | --- | --- | --- | --- |
| Aviso legal / LSSI art. 10 identity | [ ] | [ ] | [ ] | [ ] |
| Privacy policy (GDPR arts. 12–14) | [ ] | [ ] | [ ] | [ ] |
| Form first-layer notice | [ ] | [ ] | [ ] | [ ] |
| Cookie/storage policy and preferences | [ ] | [ ] | [ ] | [ ] |
| Optional marketing permission / opt-out | [ ] | [ ] | [ ] | [ ] |
| AI disclosure (only if triggered) | [ ] | [ ] | [ ] | [ ] |
| Accessibility legal-scope decision | [ ] | [ ] | [ ] | [ ] |
| Sector-specific authorisation/terms | [ ] | [ ] | [ ] | [ ] |

The privacy notice is **information**; a generic “I accept privacy policy” checkbox is not mandatory. If separate marketing consent is necessary, record its actual scope, non-preselected state and withdrawal. Do not describe payments or checkout unless they exist.

## D. Cookies, storage, SDKs and consent

| Name / endpoint | Owner and purpose | Necessary/exempt? Reason | Lifetime/configuration | Pre-choice behavior | After reject | After accept | After withdrawal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [e.g. actual security cookie] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [e.g. actual analytics SDK] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| [actual localStorage/consent key] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Evidence capture for each scenario: date/time UTC [ ], exact SHA [ ], browser/device [ ], origin [ ], HAR/request domains [ ], storage snapshot [ ], sanitized payload inspection [ ], screenshot [ ], reviewer [ ].

- [ ] Fresh/no choice
- [ ] Reject
- [ ] Accept
- [ ] Withdraw
- [ ] Reload and navigate
- [ ] Expired/corrupt/blocked storage
- [ ] Multi-tab
- [ ] Slow hydration / first click
- [ ] Keyboard, reduced motion, narrow viewport and 200% zoom
- [ ] Browser engine coverage (do not call WebKit a physical Safari test)
- [ ] GPC/DNT if the product claims to respect them
- [ ] Form usable with analytics denied
- [ ] No personal data in event payloads or URLs
- [ ] No real commercial test leads or synthetic production conversions

If GA4/GTM is present: basic vs advanced Consent Mode v2, every tag and potential denied-state pings: [ ].

## E. Intake / CRM and event truth

- Actual receiver endpoint and authorisation boundary (private record): [ ]
- Created vs duplicate vs failed vs completed semantics: [ ]
- Optional photo upload and retry behavior: [ ]
- Event allowlist and privacy review: [ ]
- Isolated test evidence: [ ]
- Real production destination evidence (if naturally available): [ ]
- No test lead submitted to live CRM: [ ] confirmed  [ ] not verified
- What remains unobservable until a real visitor submits: [ ]

## F. AI, accessibility, media and sector decisions

- AI actually deployed to visitors, lead processing or published media? [ ] / role [ ]
- AI Act art. 50 provider/deployer, chatbot/deepfake/public-interest text tests: [ ]
- GDPR personal-data processing by AI provider and any automated significant decision: [ ]
- In-context AI disclosure or rationale for not applicable: [ ]
- Source/rights/permissions for photographs, reviews, testimonials and claims: [ ]
- Law 11/2023 scope, service category, microenterprise exemption and any other applicable law: [ ]
- WCAG 2.2 AA engineering checks; keyboard, zoom, screen reader, Safari physical-device status: [ ]
- No fabricated real jobs, customers, star counts or imagery: [ ]

## G. Sign-off and release truth

| Gate | Status: PASS / FAIL / NOT RUN / BLOCKED_OWNER | Evidence link / reviewer / date |
| --- | --- | --- |
| LEGAL_ID | [ ] | [ ] |
| PRIVACY_OWNER | [ ] | [ ] |
| PROCESSOR_DPA_TRANSFER | [ ] | [ ] |
| COOKIE_TECH | [ ] | [ ] |
| FORM_INTAKE | [ ] | [ ] |
| AI_MEDIA_SECTOR | [ ] | [ ] |
| ACCESSIBILITY | [ ] | [ ] |
| DEPLOYED_SHA_DOMAINS | [ ] | [ ] |
| LEGAL_RELEASE_APPROVAL | [ ] | [ ] |

**Technical result:** [DONE / PARTIAL / BLOCKED] — what was actually tested: [ ].

**Legal approval:** [APPROVED BY CONTROLLER / PENDING / NOT ASSESSED] — identity of approver and evidence: [ ].

**Open decisions and owner:** [ ].

**Recheck trigger/date:** [ ].

A technical DONE is not a legal certification. Keep raw contracts, client identity details, lead records and private screenshots in the client's authorised private location; only generalizable, redacted lessons belong in the public Handbook.
