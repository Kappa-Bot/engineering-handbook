---
id: pb-spanish-client-website-privacy-consent-audit
kind: playbook
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
  - src-boe-accessibility-11-2023
  - src-eu-ai-act
  - src-ec-ai-transparency-guidance-2026
  - src-vercel-web-analytics-privacy
  - src-google-consent-mode
last_verified: 2026-11-13
review_due: 2027-02-13
---

# Spain — privacy, cookies, analytics and AI audit for a client service website

## Use and authority

Repeatable delivery procedure for a Spanish SME's informational/marketing website that collects enquiries or quote requests **without an on-site checkout**. Apply only the relevant branches when the site adds payments, booking contracts, regulated services, minors, chatbots, advertising pixels or other purposes.

The **only canonical normative legal/trust baseline** is [std-public-website-legal-trust-baseline](../standards/public-website-legal-trust-baseline.md). Consult [research and legal distinctions](../references/spain-sme-lead-web-legal-research-2026-11.md) for sources, exclusions, vendor comparisons and the limits of the 2026 exploratory competitor sample. Record actual project facts using [tpl-spanish-client-website-legal-evidence-pack](../templates/spanish-client-website-legal-evidence-pack.md). The client/controller or its qualified adviser approves legal identity, lawful bases, contracts and final copy; engineering verifies behavior and provenance.

Do not copy a competitor's policy or infer compliance from a banner. Do not add a generic CMP, AI policy, DPO, accessibility widget, marketing checkbox or payment disclosure without a triggering fact.

## 1. Intake: establish the actual business and data path

Before implementation, collect the minimum facts from approved project material:

1. **Mode and operator:** demo/prelaunch/commercial; legal operator, NIF/CIF, address, email/contact, registration/regulated-profession details if applicable, languages, jurisdiction and real domain. Do not publish placeholders on a commercial site.
2. **User journey:** information, phone/email/WhatsApp, contact/quote form, optional photos, confirmation, follow-up, CRM handoff, retention, any remote contracting. Verify whether a quote is merely requested or a legally binding purchase is concluded online.
3. **Purpose inventory:** responding to a request, fraud prevention, hosting logs, optional analytics, attribution, marketing, embedded maps/video, AI assistant, lead scoring. Never combine distinct purposes under one checkbox.
4. **Personal data:** fields, URLs/referrers, IP/logs, photos, metadata, CRM IDs, draft state, attachments, messages and downstream recipients. Identify special-category data that may be revealed inadvertently.
5. **Roles/accounts:** actual controller, development agency access/processing, contracting account holder, hosting/edge, form receiver, database/storage, CRM, email/SMS/WhatsApp, analytics, captcha, other processors and separate controllers.
6. **Evidence:** current deployed SHA, provider settings, consent behavior, data retention, signed/applicable DPA, subprocessor list and transfer route. Mark missing owner facts as OPEN rather than inventing them.

If the agency only delivers code and never processes client data, do not automatically designate it as processor. If it operates the service or accesses leads under instructions, assess and document the art. 28 relationship.

## 2. Decision tree: what is needed for this site?

| Question | Yes: evaluate or implement | No: do not fabricate |
| --- | --- | --- |
| Commercial Spanish information-society site? | LSSI art. 10 operator details / Aviso legal, plus truthful service claims. | Still assess other applicable laws for the actual operator. |
| Collects or processes personal data (including form, security logs, analytics)? | GDPR lawful-basis and information assessment; full privacy notice and first layer where data are collected. | No fake “we collect no data” claim without technical proof. |
| Uses non-exempt terminal storage/access or tracking? | Cookie/storage notice, prior consent and real blocking; symmetric Accept/Reject and withdrawal. | Do not force an empty banner solely because the site is commercial. |
| Uses necessary anti-bot/security cookies? | Document actual name, domain, purpose, duration and exemption analysis (e.g., cf_clearance if actually present). | Do not classify security as optional analytics. |
| Sends marketing unrelated to the requested response? | Separate LSSI art. 21 channel-permission/exception analysis and GDPR basis; optional unselected choice where required. | No mandatory newsletter checkbox. |
| Uses third-party maps, video, captcha, chat or social embeds? | Request/storage/role/transfer inventory; optional embed gating or privacy-preserving alternative as applicable. | Do not list imaginary vendors. |
| Uses visitor-facing AI or relevant synthetic/deepfake content? | Role-specific AI Act art. 50 and GDPR review; in-context disclosure when applicable. | No blanket “this site uses AI” notice from use of a coding assistant. |
| Performs solely automated significant decisions or high-risk processing? | GDPR art. 22/35 and relevant AI Act assessment, with legal review. | Ordinary manual quote handling is not automatically high-risk AI. |
| Provides a service covered by Law 11/2023? | Scope, microenterprise exemption and sector rules, plus accessibility evidence. | Do not assert every SME marketing page is legally subject to the same accessibility declaration. |
| Offers checkout, payment or binding online contracting? | Add relevant consumer/e-commerce/payment requirements and specialist review. | For a quote-only site, do not invent payment, refunds or withdrawal workflows. |

**Engineering quality is separate from minimum legal scope:** target WCAG 2.2 AA under std-ui-ux-quality-baseline even if a particular statute's sectoral trigger does not apply.

## 3. Build one traceable inventory

Create one row per purpose and provider, not one generic “cookies” row:

| Field | Capture |
| --- | --- |
| Purpose | Quote response / hosting security / optional statistics / campaign attribution / optional marketing / AI etc. |
| Data | Fields, metadata, IP, attachment, event properties, retention keys, request headers; redact private samples. |
| Controller and role | Actual legal entity, agency, provider, processor/subprocessor/independent controller where appropriate. |
| Legal ground | GDPR art. 6 ground and reasoning; special-category art. 9 condition if applicable; LSSI 22(2) terminal-access exemption/consent separately. |
| Third parties | Exact vendor, product, account/plan holder, origin/domain, endpoint, subprocessor link and contract evidence. |
| Geography | Real region, transfers and safeguards, not vendor nationality alone. |
| Retention | Live record, photos, draft, logs, backup and provider analytics: period/criteria, deletion and legal hold. |
| User-facing notice | First-layer location, full policy section, consent choice, rights contact and accessibility. |
| Verification | Network/storage trace, timestamp, SHA, browser, screenshot, owner approval and open risks. |

Data flow: visitor -> delivery/security -> form -> server-side validation -> receiver -> CRM/authorised staff -> requested response. Add optional analytics and marketing branches only when consent/legal basis and actual implementation permit them. The CRM/receiver is the source of truth for a created lead; a browser click is not a confirmed lead.

## 4. Draft legal surfaces from facts, not templates alone

**Aviso legal:** actual operator identity and applicable LSSI art. 10 fields; commercial scope, contact, verified regulated-profession or authorisation data where required, content rights and truthful conditions. No invented company suffix, tax number, registration, address or testimonial.

**Privacidad:** first layer near the form and a discoverable full notice covering purposes and lawful bases, recipients/processor categories, international transfers, retention/criteria, rights and contact, DPO if required, complaints to the supervisory authority, obligatory/optional data and relevant automated decisions. If a visitor can upload photos, explicitly address their purpose and retention. The client approves each fact.

**Form acknowledgment:** the AEPD explicitly says that accepting a privacy information clause is **not** a legal prerequisite to process a form. Prefer a clear notice and a link. If the product needs an acknowledgment record, label it as receipt of information; keep any genuinely consent-based optional marketing choice separate and unselected.

**Cookies and storage:** list real purposes, providers, cookie/storage names, lifetime, third-party access and withdrawal path. If the only optional service is Vercel Analytics, name that service rather than falsely listing Google Ads or a generic marketing category. Necessary security cookies are described separately and classified from evidence. Do not say that “no cookies” means “no data processing”.

**IA:** assess each real system, role and output. For an AI chat, use an immediate in-context disclosure and explain relevant personal-data processing. For a deepfake or covered public-interest text, apply the specific art. 50 test. For ordinary editorial AI assistance, avoid unsupported blanket labels; keep provenance and claims truthful.

### Original copy starters (must be completed and approved)

Form first layer:

> Responsable: [identidad verificada]. Usaremos los datos y archivos que envíes para atender tu solicitud de presupuesto o contacto [y otras finalidades reales]. Base jurídica: [artículo y fundamento aprobado]. Conservación: [plazo o criterio]. Destinatarios y transferencias: [categorías/explicación]. Puedes ejercer tus derechos en [canal real]. Más información en [Privacidad].

Vercel-only optional statistics:

> Utilizamos Vercel Web Analytics para comprender el uso de la web y mejorar el formulario, únicamente si lo permites. Puedes rechazar las estadísticas sin perder acceso al servicio y cambiar tu decisión desde Cookies. [Rechazar estadísticas] [Permitir estadísticas] [Más información].

Optional unrelated marketing, **only if actually offered and legally based on consent**:

> [ ] Quiero recibir por [canal concreto] novedades y ofertas de [operador] distintas de la respuesta a mi solicitud. Puedo retirar este permiso cuando quiera.

AI chatbot, **only if actually deployed**:

> Estás hablando con un asistente de inteligencia artificial. [Cómo acceder a atención humana, si existe] · [Información sobre privacidad].

Do not publish bracketed text on a live commercial site.

## 5. Verify consent and form behavior, not just appearance

Capture browser network requests and cookies/localStorage/IndexedDB **before** scripts run and after each transition. Test at least:

| Scenario | Evidence expected |
| --- | --- |
| Fresh/no choice | No optional analytics requests or storage under the chosen opt-in policy; necessary services still work. |
| Reject | Same non-analytics behavior, persistence and no pressure or loss of form functionality. |
| Accept | Only approved SDK/events; inspect URL, referrer and payload for PII, photos, identifiers and private paths. |
| Withdraw | Future optional events stop, including in another tab; user can reconfigure; existing third-party data cannot be unsent. |
| Reload, expired/corrupt preference, disabled storage | No accidental consent; clear failure mode; no hydration flicker or lost first click. |
| Keyboard, 320px, 200% zoom, reduced motion | Equivalent button prominence, accessible focus, no hidden actions, no intrusive overlay. |
| Chromium, Firefox, WebKit | Report the exact engines tested; WebKit automation is not a Safari physical-device test. |
| DNT/GPC | Verify site-specific promises if implemented; do not claim a universal legal behavior. |
| Form without consent | Request flow and validation work; no dependency on Analytics. |
| Retry, timeout, idempotent receiver response | No false form_accepted/form_complete or duplicated commercial lead. |
| Actual production conversion | Observe only when a **real** visitor submits with analytics consent; never manufacture a CRM job or fake event. |

For Google, test both Consent Mode v2 **basic vs advanced** behavior and all tags in GTM. A denied consent state can still permit some cookieless pings in advanced mode; whether they are permitted in the target configuration requires legal and network assessment. For Vercel, verify actual SDK activation and before-send restrictions, not merely that the UI says “rejected”. For Cloudflare, do not disable WAF/anti-bot to make an automated HTTP client pass.

## 6. Contract, retention and security handoff

Give the controller a concise evidence request, not an unsupported “fully GDPR-compliant” badge:

- Controller legal identity, DPO/right-to-contact route if applicable, signed approval of purposes, legal bases, final texts and retention criteria.
- Whether the agency is a processor; actual DPA and instructions where required; access permissions, incident reporting and exit/deletion procedure.
- For each provider: account owner, applicable DPA/terms, subprocessor authorisation and current list, data locations and Chapter V transfer mechanism, security and rights assistance, effective retention and deletion.
- For Vercel Pro, its public 2026 DPA describes processor and separate-controller roles and US processing. **Verify the actual contractual chain**, not just that the plan is Pro.
- Technical protections for photos/leads: TLS, least privilege, private storage, upload validation, logs without PII, backup/restore and incident response appropriate to risk. Where a provider contract restricts sensitive/special-category data (e.g. Vercel DPA Schedule 1), verify whether the actual upload path processes such content and respect that contractual boundary.
- Breach playbook: GDPR art. 33 authority notification when required within 72 hours of awareness; art. 34 notice to people when high risk, without undue delay. Record decisions and exceptions.

Never invent a universal number of months for lead/photo/IP retention, and never equate the analytics dashboard's visible history with deletion.

## 7. Evidence gates and release

Use PASS / FAIL / NOT RUN / BLOCKED_OWNER for each gate:

| Gate | Responsible | Proof |
| --- | --- | --- |
| Operator/claims | Client/controller | Verified legal identity, service claims, assets, reviews and approvals. |
| Privacy basis/text | Client/controller or adviser | Approved purpose/ground/retention/recipient/transfer and form copy. |
| Provider contracts | Contracting parties/controller | DPA applicability, subprocessor/transfer and data deletion record. |
| Cookie technical | Engineering | Browser traces for fresh/reject/accept/withdraw/reload; real script gating. |
| Intake/CRM boundary | Engineering | Isolated tests for created vs duplicate/failed/completed; no fake production leads. |
| UX/accessibility | Engineering + native tester when available | Keyboard, reflow, zoom, focus, motion; label unrun AT/Safari. |
| Production provenance | Engineering | Exact SHA, deployment, domain, pages, real smoke; do not equate READY with all interactions. |
| Final legal release | Client/controller | Signed/recorded approval of public texts and contractual matters; engineering cannot self-certify it. |

A technical DONE may coexist with owner/legal items explicitly OPEN; do not mislabel that as a fully legally approved release. Do not modify unrelated CRM, DNS, Supabase, WAF, billing or other clients during a website-only audit.

## 8. Maintenance triggers

- Every new analytics tag, SDK, iframe, captcha, marketing channel, AI tool, photo field, processor or hosting-region change: reopen the affected inventory and user-facing notice.
- Every material site release: rerun relevant consent/network, form and accessibility tests on the exact candidate; record deployed SHA.
- Every quarter or provider terms update: check vendor DPA, subprocessors, transfers, retention, Google/Vercel consent behavior and current AEPD/AI guidance.
- At least annually or on legal change: ask the controller to revalidate identity, legal text, retention, rights contact and sector applicability.
- Capture dated, redacted proof in the **client's authorised private dossier**, not the public Handbook. Promote only generalizable lessons with evidence and correction history.

Stop at the narrowest evidence-backed result. Do not repeat the exploratory competitor survey merely to audit a new client's form; use the decision tree and current primary sources.
