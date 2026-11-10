---
id: std-public-website-legal-trust-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - public-marketing-websites
  - client-business-websites
  - product-vertical-public-pages
  - demos
sources:
  - src-boe-lssi
  - src-eu-gdpr
  - src-aepd-cookie-guide
  - src-boe-rd1277-health-authorisation
  - src-boe-lopdgdd
  - src-boe-unfair-competition
  - src-boe-patient-autonomy
  - src-boe-image-rights
  - src-eu-ai-act
  - src-eu-consumer-credit-2023
last_verified: 2026-11-10
review_due: 2027-02-10
---

# Public Websites — Legal Transparency, Privacy and Trust Baseline

## Scope and authority

Apply to public client websites and publicly reachable demonstrations developed for Spain/EU. This is an **engineering delivery and evidence standard**, not a substitute for the controller's legal advice. The client's identity, clinical authorisation, actual suppliers, consent conditions and commercial claims are **repo-local facts**; never fill them from guesses or unrelated clinic websites. Recheck current consolidated law and regulator guidance **at the actual launch date**, especially for health, finance and AI.

Distinguish: **legally required when applicable** (cited primary law), **technical controls chosen to reduce risk**, and **owner/legal-signoff gates**. `noindex`, demo notices and Vercel READY do not exempt a website from applicable law.

## 1. Truth mode and responsibility

Every public surface MUST declare its actual mode in delivery evidence: `demo`, `prelaunch` or `commercial`. A publicly reachable demonstration MUST remain `noindex`, truthfully identify illustrative cases/reviews/imagery and avoid pretending to be an authorised clinical service. Do not publish invented NIF, company names, clinicians, registration numbers, endorsements, review totals or patient cases.

Before commercial launch, collect and verify the legally responsible operator and publication approval. For Spanish information-society services, assess the fields of **LSSI art. 10**: legal name, address, direct effective contact, tax number, applicable registration, administrative authorisation and regulated-profession details when applicable (`src-boe-lssi`). This includes a working privacy-rights contact and accessible legal pages. Keep unknown identity fields in an **internal** readiness dossier, not visible as apparently final legal information.

**Healthcare conditional gate:** A healthcare facility's advertising is limited to authorised activities and normally must state its health-registration number or applicable specific health-advertising authorisation under **RD 1277/2003 art. 6.2** (`src-boe-rd1277-health-authorisation`). Verify the actual autonomous-community register, authorisation and authorised service portfolio; present the appropriate identifier in public advertising, not just an internal spreadsheet. Confirm any further local advertising conditions with qualified counsel. Do not import health-specific requirements into non-health websites.

## 2. Privacy is an inventory, not a generic footer

Before releasing the final privacy notice, map actual processing by user journey: static navigation and security logs, contact/WhatsApp, forms, analytics, maps/embedded providers, CRM or booking, and any health data. For each operation record controller/processor/recipient roles, purpose, **GDPR art. 6** lawful ground and **art. 9** condition when special-category data is involved, retention or retention criteria, recipients, international transfers/safeguards, rights, security controls, and DPO when legally required (`src-eu-gdpr`, `src-boe-lopdgdd`). Confirm processor contracts and subprocessor lists; the website code alone does not prove provider arrangements.

Provide comprehensible first-layer notices at data-collection points and an accessible full policy consistent with GDPR arts. 12–14. Do not use acceptance of a privacy notice as blanket permission for marketing. **Clinical informed consent is different from consent to publish a patient's image** (`src-boe-patient-autonomy`, `src-boe-image-rights`). For real case photography obtain separately scoped, documented and revocable permissions, age/capacity review, and editorial approval. Avoid sending diagnoses, radiographs, symptoms or other clinical documents through casual public forms or prefilled WhatsApp messages; direct patients to the clinic's verified secure process.

**Healthcare DPO conditional gate:** check LOPDGDD art. 34.1(l), including its individual-practitioner exception; do not claim a DPO exists (or that no DPO is needed) without analysing the operator's legal structure (`src-boe-lopdgdd`). Also keep clinical data retention, breach procedures and DPIA/records-of-processing decisions separate from a marketing-site-only assessment.

## 3. Third parties, cookies and storage

Inventory **observed** cookies, localStorage, pixels, iframes, SDKs, requests and hosting logs in a clean browser, before and after each choice. Record real names/domains, purposes, parties, durations and legal bases. Necessary first-party preferences selected by the visitor may have different consent treatment from tracking; *document, do not assume* an exemption (`src-aepd-cookie-guide`, `src-boe-lssi`).

For non-exempt purposes requiring consent:

1. Block third-party requests and storage **before** a valid choice, not just the visible banner. Consent must be freely given, informed, specific and demonstrable; neither silence nor scrolling counts.
2. Offer **Accept** and **Reject** on the same level with equivalent prominence and comparable action cost. Separate independent purposes when applicable; optional toggles default off.
3. Allow easy later **withdrawal/reconfiguration** from a persistent footer or policy control. Version and scope the choice; never turn missing/corrupted storage into acceptance. Withdrawing prevents future loads and unmounts active embeds where practicable; it cannot erase data already transmitted to the third party.
4. Preserve functional, nontracking alternatives. An optional map may start as an informative first-party map panel with address/directions and an accessible, informed **load Google map** choice. A deliberate external-link click leaves the site for the provider and must be signposted; merely rendering the link does not authorise a background Google iframe.
5. Validate actual network/storage outcomes for *fresh*, *rejected*, *accepted*, *withdrawn*, *reloaded* and *storage-disabled* sessions, desktop/mobile and every language. An aesthetically correct banner or a code-level condition is not sufficient proof of compliance.

Do not install a broad cookie-management UI where no optional technologies are used. A **just-in-time, equal-choice embed control** may be appropriate for an optional map, provided the consent and withdrawal behavior above is real. If third-party analytics, ads or other categories are later added, revisit the entire inventory/UI and legal notice; do not silently piggyback on map permission.

## 4. AI imagery, testimonials and health claims

Maintain a media manifest linking each generated/edited asset to its real usage, provenance/rights, image subject, risk of real-person/real-premises confusion, alt text and appropriate in-context disclosure. For **AI Act art. 50** situations, assess the actual roles and whether the material qualifies as a deepfake; publish the applicable transparent disclosure rather than relying only on a remote footer (`src-eu-ai-act`). Do **not** claim every AI-generated decorative image necessarily invokes the same legal duty. Regardless of that classification, an illustration MUST NOT imply it documents a real patient, clinician, procedure, outcome, premises or testimonial unless validated.

**Demo reviews:** unmistakably mark the entire block and each item as fictional examples, with no fake rating aggregate, Google endorsement, review JSON-LD or unverifiable reviews linked as genuine. **Commercial reviews:** verify provenance, authorisation, provider terms, selection policy and truthful star/text correspondence; omit a review module when evidence is unavailable. Fabricated or misleading reviews are prohibited under consumer/unfair-competition rules (`src-boe-unfair-competition`).

**Health advertising:** Require a clinical owner to approve each service/treatment, diagnostic claim, equipment/brand, professional credential, before/after, financing/insurance partner, opening hour and price before making it commercial. Avoid absolute outcomes, unwarranted guarantees, invented evidence and instructions masquerading as diagnosis. Financing disclosures may engage distinct consumer-credit rules; check relevant Spanish transposition and the transition to Directive (EU) 2023/2225 at launch (`src-eu-consumer-credit-2023`).

## 5. Accessible, truthful legal UX and language

- Keep legal, privacy, cookies, AI/media provenance and contact links discoverable from every page; do not hide key obligations behind motion, inaccessible overlays or tiny print.
- Match actual behavior: if an iframe is gated, remove copy saying it auto-loads; if a form is inactive, do not promise a response. Keep dates meaningful and never mislabel drafts as approved.
- Buttons/dialogs for consent must work by keyboard/touch, be perceivable at narrow/mobile viewports, preserve focus and obey reduced-motion preferences. Text must be plain, proportionate and distinct from marketing copy.
- For multiple human languages, keep `lang`, on-screen policy text and **client-side `title`/description** aligned on switches. One URL with language state must **not** be advertised as separate indexable `hreflang` variants; a future SEO launch requires a deliberate URL strategy (`std-public-web-discoverability-baseline`).

## 6. Evidence gates and handoff

| Gate | Minimum proof | Default when unavailable |
| --- | --- | --- |
| `LEGAL_ID` | Owner identity, registration, contacts and health authorisation where relevant, checked from a primary record | `BLOCKED_OWNER` |
| `PRIVACY` | Data-flow/processor/retention/transfer inventory, lawful bases and rights path approved by controller/adviser | `BLOCKED_OWNER_PROVIDER` |
| `COOKIE_TECH` | Fresh/reject/accept/revoke network and storage traces, inventory and real gating | `NOT_VERIFIED` |
| `MEDIA_REVIEWS` | Asset/claim/review provenance with visible disclosures and approval; remove demo reviews before launch | `BLOCKED_CONTENT` |
| `CLINICAL_FINANCE` | Service, clinical and financing claims checked against operator evidence and applicable rules | `BLOCKED_OWNER` |
| `LEGAL_RELEASE` | ES/CA/EN reviewed for content parity, accessibility test, approved domain, final signed texts and exact-deployment evidence | `NOT_READY` |

An engineering green check only closes the **technical** gate it tested. Commercial indexing and approval remain blocked until the real controller and qualified reviewer sign off the applicable evidence. Recheck laws and supplier configuration at launch; report `PASS`, `FAIL` and `NOT_RUN` honestly.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "public-legal-trust-plan",
      "type": "constraint",
      "force": "must",
      "text": "For public client websites, use std-public-website-legal-trust-baseline: verify real operator/health authorisation where applicable, controller and providers, block optional map/analytics requests before consent, allow symmetric reject and revocation, and label AI imagery and demo reviews truthfully. A noindex demo is not a legal exemption; never invent identity or approve commercial release from synthetic tests.",
      "source": "std-public-website-legal-trust-baseline",
      "covers": ["privacy", "legal", "third-party-consent", "commercial-truth"],
      "activate_when": ["archetype:public-client-website"],
      "phase": ["planning", "implementation", "verification"],
      "priority": 94
    }
  ]
}
```
