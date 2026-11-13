---
id: ref-spain-sme-lead-web-legal-research-2026-11
kind: reference
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
  - client-business-websites
  - public-marketing-websites
  - spain
  - lead-generation
sources:
  - src-boe-lssi
  - src-eu-gdpr
  - src-boe-lopdgdd
  - src-aepd-cookie-guide
  - src-aepd-privacy-clause-faq
  - src-boe-accessibility-11-2023
  - src-eu-ai-act
  - src-ec-ai-transparency-guidance-2026
  - src-vercel-web-analytics-privacy
  - src-vercel-dpa-2026
  - src-google-consent-mode
  - src-google-analytics-pii
  - src-w3c-wcag-22
  - src-boe-unfair-competition
  - src-boe-image-rights
  - src-observation-vandelay-cookies-2026-11
  - src-observation-vandelay-contact-2026-11
  - src-observation-tda-contact-2026-11
  - src-observation-come-contact-2026-11
  - src-observation-interprint-contact-2026-11
last_verified: 2026-11-13
review_due: 2027-02-13
---

# Spain: SME service websites with lead forms — legal and technical research (November 2026)

> **Evidence reference, not a legal opinion or a second Standard.** The canonical cross-repository delivery obligations are in [Public Websites — Legal Transparency, Privacy and Trust Baseline](../standards/public-website-legal-trust-baseline.md). The repeatable implementation procedure is [Spanish client website privacy and consent audit](../playbooks/spanish-client-website-privacy-consent-audit.md); the per-client evidence record is [Legal evidence pack](../templates/spanish-client-website-legal-evidence-pack.md). Use current primary law and actual provider contracts at each release.

## 1. Scope, research provenance and confidence

Primary case: a Spanish SME's public, informational/service website with a request-for-quote/contact form, optionally photos, delivery to a commercial intake/CRM, optional analytics and no on-site purchase, payment or checkout. Agurto-Web supplied real implementation evidence for opt-in Vercel Web Analytics, a consent/revocation UI, independent campaign attribution and a lead-intake funnel; its exact events, hosting/account ownership, data paths and controller details remain **Agurto repo-local facts**.

This synthesis incorporates the November 2026 exploratory deep-research report and checks its material legal assertions against official AEPD, BOE, EUR-Lex, European Commission and provider sources. The exploratory report listed roughly 29 named site candidates but **did not deliver a reproducible 40–60-site audit** with per-site legal-document URLs, complete captures, browser network traces and dates. It must **not** be cited as a census or evidence that particular businesses violate the law. Four directly linked examples appear below; other domains are leads for later independent inspection, not audited findings. A policy declaring GA4 does not prove the tag loaded, and a visible cookie banner does not prove pre-consent blocking.

Evidence grades:
- **A — primary law/regulator or provider contract:** establishes the stated rule or the provider's documented behavior, not the client's actual configuration.
- **B — captured public policy/form:** establishes what the site **says** at the observation date, not actual request behavior or legal compliance.
- **C — repeatable browser/network/storage trace:** establishes what happened in the tested session, not every geography, browser or subsequent deployment.
- **D — exploratory candidate/inference:** discovery only; do not use to accuse a site or certify a provider.

Do not infer legal approval, DPA execution, data residency, deletion or a live conversion from a green build, a screenshot, a provider marketing statement or a cookie banner.

## 2. Applicability map: mandatory, conditional, recommended

| Topic | Trigger and correct interpretation | Primary source | Evidence / owner |
| --- | --- | --- | --- |
| Operator identity / aviso legal | Commercial information-society provider: evaluate LSSI art. 10 (actual name, address, contact, tax ID, registration/professional/authorisation fields **when applicable**). No checkout is not an exemption. | src-boe-lssi | Verified client identity and public page; controller/client approves. |
| Form privacy information | Personal data collected: GDPR arts. 12–13, sometimes 14; layered notice at collection, full notice, rights, recipients, retention, transfer information. | src-eu-gdpr, src-boe-lopdgdd | Screen and policy matching the actual form; client approves. |
| Basis for requested quote/contact | GDPR art. 6(1)(b) may fit steps at the **person's request** before a contract; check the actual purpose and person involved. Legitimate interests art. 6(1)(f) needs its own assessment. Do not default to consent for the necessary reply. | src-eu-gdpr | Purpose-by-purpose lawful-basis record. |
| Privacy-policy checkbox | **Not legally mandatory as a generic acceptance checkbox.** AEPD says an acknowledgment may evidence receipt of information; it is not itself consent to every processing purpose. Avoid making a generic checkbox the purported lawful basis. | src-aepd-privacy-clause-faq | Accessible first layer; separate optional consents. |
| Email/SMS/WhatsApp promotions | Distinguish responding to the requested quote from unsolicited electronic advertising. LSSI art. 21 requires permission unless its existing-customer/similar-services exception actually applies, with opt-out. | src-boe-lssi, src-eu-gdpr | Channel, purpose, permission/exception and unsubscribe record. |
| Cookies and terminal access | LSSI art. 22(2) covers non-exempt storage/access, including equivalent technologies; consent before non-exempt use, informed equal-choice UI and withdrawal under AEPD guidance. A cookie-free claim is not a legal classification by itself. | src-boe-lssi, src-aepd-cookie-guide | Real inventory and fresh/reject/grant/withdraw network/storage traces. |
| Processing of analytics data | Independently assess GDPR lawful basis, transparency, recipients and minimisation, even where terminal-access rules do not apply. The conservative client opt-in policy may exceed the minimum. | src-eu-gdpr, src-aepd-cookie-guide | Data flow, event allowlist, privacy text and browser trace. |
| Processors/subprocessors | GDPR art. 28: roles depend on actual processing and instructions, not vendor labels. Verify who contracts with whom and the applicable DPA/subprocessor authorisations. | src-eu-gdpr, src-vercel-dpa-2026 | Executed/applicable terms and owner sign-off; not a public-footer claim. |
| Transfers outside EEA | GDPR Chapter V: assess actual processing locations and transfers; adequacy (including EU-US DPF **only for eligible certified recipients and covered transfers**) or applicable safeguards and supplementary assessment where necessary. Never call the invalidated Privacy Shield current. | src-eu-gdpr, src-vercel-dpa-2026 | Provider-specific transfer record, version/date and reviewer. |
| Retention | GDPR art. 5(1)(e) and 13(2)(a): define actual period or criteria for leads, photos, drafts, logs, analytics, backups and rights/claims; dashboard history length is **not** a deletion commitment. | src-eu-gdpr, src-vercel-dpa-2026 | Retention schedule, implemented deletion and exception evidence. |
| Security / breaches | GDPR arts. 32–34: risk-based measures. Notify supervisory authority within 72 hours of awareness **where required**; notify affected persons without undue delay **where high risk requires it**. No blanket six-month IP-log rule. | src-eu-gdpr | Access, encryption, upload controls, incident response and evidence. |
| Records / DPIA / DPO | GDPR art. 30 exemptions are conditional (recurring/non-occasional processing matters); DPIA art. 35 only for likely high risk; DPO duties depend on the actual entity/activity and LOPDGDD art. 34. | src-eu-gdpr, src-boe-lopdgdd | Documented applicability decision, not a universal yes/no. |
| Automated decisions | GDPR art. 22 concerns **solely automated** decisions with legal or similarly significant effects, subject to its conditions/exceptions; ordinary lead scoring does not automatically trigger it. Profiling can still require other disclosures and safeguards. | src-eu-gdpr | Workflow, human role, impact, lawful basis and disclosures. |
| AI transparency | AI Act art. 50 distinguishes providers vs deployers, AI interactions, synthetic-output machine marks, deepfakes and some public-interest text. It is **not** a universal label-every-AI-image-or-paragraph rule. | src-eu-ai-act, src-ec-ai-transparency-guidance-2026 | Per-use-case role/content test; see section 6. |
| Accessibility | Law 11/2023 covers specified products/services and contains microenterprise service exemptions; an informational SME site is **not automatically** in every category. Independently, the Handbook's engineering target is WCAG 2.2 AA. | src-boe-accessibility-11-2023, src-w3c-wcag-22 | Scope decision + keyboard/zoom/AT evidence; no mandatory accessibility widget by default. |
| Photos, testimonials and claims | Verify image rights, permissions, factual claims, endorsements and misleading-advertising risks. AI artwork must not impersonate real staff, customers, premises or completed jobs. | src-boe-image-rights, src-boe-unfair-competition | Provenance, approvals and truthful presentation. |
| Checkout-specific obligations | On-site purchase/payment/contracting creates additional distance-selling/payment/consumer rules; do **not** impose a checkout, cancellation flow or payment policy on a site that merely accepts quote requests. Other advertising/consumer duties can still apply. | src-boe-lssi, src-boe-unfair-competition | Verified business workflow, not assumptions from the word “presupuesto”. |

The distinction **legal requirement / regulator interpretation / internal engineering standard / vendor contract / client approval** is part of the record for every launch. A provider's self-described GDPR compliance does not transfer the controller's accountability.

## 3. Form-only site: information, consent and commercial boundaries

The core request is to answer a quote/contact initiated by the visitor. Its first layer should be close to the submission action, with a real link to the full privacy notice. Do not invent the client's corporate suffix, CIF/NIF, privacy email, postal address or retention period. Required vs optional fields, photos and follow-up channels must match the real workflow.

An original **illustrative first layer** (not final client copy):

> Responsable: [razón social verificada]. Finalidad: atender y gestionar la solicitud de información o presupuesto y la documentación que decidas adjuntar. Base jurídica: [medidas precontractuales solicitadas por la persona, art. 6.1.b RGPD, si realmente procede; otra base validada en caso contrario]. Destinatarios: [categorías reales de encargados/terceros]. Conservación: [plazo o criterio aprobado]. Derechos: [canal real de ejercicio]. Información completa: [enlace a Privacidad].

No generic “Acepto la política de privacidad” checkbox is required by default (src-aepd-privacy-clause-faq). If an acknowledgment is retained for evidence, label it as **haber recibido/leer información**, never as blanket legal consent. A genuinely optional newsletter, unrelated commercial follow-up, marketing profiling or campaign attribution requiring consent needs its own affirmative, non-preselected control and must not block the core quote submission.

Photos can reveal faces, addresses, documents or special-category information **depending on content**. Keep them optional unless justified; set size/type/quantity limits, server validation, malware and access protections appropriate to risk, secure/private storage, expiring links where used, explicit retention and deletion across backups where feasible. Never place raw images, file names, contact data, request IDs or full URLs with personal parameters in analytics.

Response to a quote is not automatically a marketing campaign. Subsequent unrelated advertising by email or messaging is a separate decision. A form without checkout is still personal-data processing and a commercial site under LSSI.

## 4. Analytics, cookies and embedded providers

### Do not collapse two different legal questions

1. **Terminal access:** Does a script, cookie, localStorage, fingerprinting or similar technology store/access information on the visitor's device for a non-exempt purpose? Assess LSSI 22(2) and AEPD cookie guidance.
2. **Personal-data processing:** Regardless of cookies, does the service process personal data (including request-derived identifiers or IPs in its path)? Assess GDPR purpose, legal basis, transparency, recipients, transfers and retention.

Consequently, “cookieless” neither guarantees exemption nor proves consent is always required. Choose the safer implementation for the client and document why. Security cookies such as Cloudflare cf_clearance can be necessary for anti-bot/availability, but **classify the actual purpose and configuration**; distinguish them from optional analytics and still document associated data processing. Do not claim that a security cookie contains no data or that its lifetime is universal without provider/configuration evidence.

| Stack | What official sources support | Delivery decision / caution |
| --- | --- | --- |
| Vercel Web Analytics | Vercel documents aggregated privacy-oriented measurement, no third-party cookies and a request-derived visitor hash; an enabled script transmits page views. See src-vercel-web-analytics-privacy. | For Agurto, the adopted policy is affirmative opt-in with future-send checks. Do not claim “no data”, “fully anonymous in every legal sense”, or “12 months = deletion”; review current plan, DPA and provider changes. |
| GA4 / gtag | Often uses _ga family and event processing; actual storage, identifiers, settings and retention vary. Google prohibits PII in Analytics. See src-google-analytics-pii. | Audit the real tags, cookies, URLs, event payloads and legal grounds. Do not paste Google-specific cookie names into a Vercel-only policy. |
| Google Tag Manager | Container that can load many different tags; its presence alone is not proof that GA4 is active or that no other third parties load. | Inventory every deployed tag and trigger. Consent configuration must be verified against real network requests. |
| Google Consent Mode v2 | Google documents analytics_storage, ad_storage, ad_user_data and ad_personalization and basic/advanced operation; advanced mode may transmit cookieless pings while consent is denied. See src-google-consent-mode. | A “denied” setting is not proof of **zero** requests. Decide basic blocking vs advanced pings only after legal review and actual trace; do not infer ePrivacy compliance from Google defaults. |
| Matomo / Plausible / Fathom / self-hosted logs | Different collection, storage, location and configuration options; brand names alone do not prove EU hosting, non-personal data or consent exemption. | Assess the concrete deployment, access to terminal, identifiers, contracts and transfers; prefer data minimisation where the measurement need permits it. |
| Maps, video, chat, captcha, social widgets | Third-party iframes/SDKs can transmit IP and other metadata before a visitor chooses anything. | Inventory, gate optional non-exempt loads, provide functional alternative; treat anti-abuse controls and truly necessary security separately. |
| Consent and campaign attribution | Distinct purposes and choices; a stored preference may itself be necessary to remember the choice. | Keep versioned, expiring and revocable states, with rejected/expired/corrupt/storage-disabled handling and no accidental grant. |

A minimal original **optional-analytics notice** for a Vercel-only site:

> ¿Nos ayudas a mejorar esta web? Si lo permites, activaremos estadísticas de uso con Vercel Web Analytics. Puedes rechazarlas y seguir usando el formulario con normalidad, o cambiar tu elección desde Cookies cuando quieras. [Rechazar estadísticas] [Permitir estadísticas] [Información y configuración].

Do not mention “cookies publicitarias”, “Google Analytics” or “personalización” unless actually deployed. Show Accept and Reject with comparable prominence and effort. A client-side banner without request blocking is insufficient.

### Network/storage test matrix

For each supported language, origin, viewport and materially distinct browser, record request URL/domain, initiator, cookies, storage keys, timestamps and redacted payloads:

| State | Expected proof |
| --- | --- |
| Fresh visitor | Only exempt/necessary traffic and storage; optional analytics absent under the chosen opt-in contract. |
| Explicit rejection | No new optional analytics loads/events; core navigation and quote form remain usable. |
| Explicit acceptance | Only the chosen category loads; sanitized allowlisted events; no personal fields. |
| Withdraw after acceptance | Future optional requests blocked; active embeds removed where feasible; previously sent data cannot be “unsent”. |
| Reload, navigation, expiry, corrupted/blocked storage | No silent grant; preference behavior is stable and understandable. |
| Multiple tabs and history | No stale consent continuing to send after withdrawal; recheck send boundary. |
| GPC / DNT | Test **if the site implements a policy for them**; do not misstate a universal Spanish requirement. |
| Slow hydration / first interaction | Controls are not falsely interactive before ready; keyboard/focus and the commercial form survive. |
| Error/retry/duplicate submit | No invented successful conversion; receiver acceptance and completion remain distinct. |
| Actual production receipt | Separate isolated success tests from observed real destination events; never create fake commercial leads to prove a chart. |

## 5. Processing roles, provider contracts, transfers and retention

Illustrative **flow** (replace every component with actual per-client evidence):

Visitor -> edge/hosting/security logs -> public form -> validated server receiver -> lead database/CRM -> authorised SME staff -> requested response. Optional branch: affirmative analytics choice -> analytics SDK/event endpoint. Separate optional branch: consented marketing/attribution where actually implemented. Photos -> private object storage -> authorised access -> deletion schedule.

The SME generally determines the purpose of its quote handling and is controller. A development agency **may** be a processor where it accesses/processes lead data under the SME's instructions; a one-off code-only delivery does not automatically make it one. A hosting account can belong to the agency or SME; contract chain and the provider's separate-controller activities must be assessed for each data flow. Do not assume all cloud vendors are direct subprocessors of the agency or that a particular Supabase project is hosted in the US.

For every real provider capture:
- Contracting legal entity, account/plan owner, service, data categories, processing role for **each** activity.
- Applicable DPA and version, execution/acceptance evidence, art. 28 instructions and subprocessor authorisation/notice procedure.
- Current subprocessor list and locations; security and access measures; breach notice and assistance; rights assistance; audit terms; return/deletion terms.
- Transfer route, actual country, adequacy or SCCs and supplementary assessment if applicable; DPF certification/scope only if verified for that recipient and processing.
- Retention by category (live leads, drafts, photos, analytics, logs, backups, provider copies), legal hold and deletion evidence.

**Vercel-specific observed source fact (13 Nov 2026):** its DPA, effective 31 March 2026, states coverage for Enterprise and Pro, distinguishes customer-data processor activities from some service-generated/contact-data controller activities, lists subprocessors through its Trust Center, and identifies primary US processing facilities. This **does not prove** the DPA covers an individual client's account chain, that a subprocessor list was approved, or that all data are deleted after an Analytics dashboard window (src-vercel-dpa-2026). Preserve the applicable version and account owner in the client evidence pack. Its Schedule 1 also states that customers are prohibited from including special-category/sensitive data in Customer Data: for optional photo uploads, check **whether the actual Vercel path receives those files or their contents** and prevent prohibited data exposure rather than assuming every upload traverses Vercel.

No universal “keep leads 2–3 years”, “keep logs six months” or “delete everything at the dashboard retention horizon” rule exists for every such site. Obtain the controller's purpose-based schedule and verify implementation.

## 6. AI transparency and media truth

Decision matrix under AI Act art. 50 (src-eu-ai-act; src-ec-ai-transparency-guidance-2026):

| Use | Legal/technical analysis | Public experience |
| --- | --- | --- |
| No AI-facing functionality, ordinary human-edited content | Do not invent an “AI transparency policy” merely because developers used an AI coding assistant. Assess any actual personal-data transfer to AI tools separately. | No automatic standalone AI notice. |
| Visitor-facing AI chatbot/agent | Check provider vs deployer duties and the obligation to inform users they interact with AI, subject to legal exceptions. Also GDPR information if conversation data are processed. | Clear in-context “Estás hablando con un asistente de IA”; human escalation and privacy link as appropriate. |
| AI-assisted triage of submitted leads | Inventory actual processing, provider role, retention, lawful basis, security and human oversight; GDPR art. 22 only where its significant solely automated decision threshold is met. | Describe actual relevant processing in Privacy, not a fictional chatbot banner. |
| Synthetic decorative image or copy | Not every generated image is a legally defined deepfake; distinguish provider machine-readable marking from deployer disclosure duties and assess misleading impression. | Honest illustration/provenance where needed; no false real-customer or real-premises claim. |
| Deepfake resembling an existing/plausible real subject/event and appearing authentic | Apply the art. 50(4) deployer disclosure test and exceptions; respect image rights and truthful advertising independently. | Clear in-context disclosure on first exposure, not only a buried legal footer. |
| AI-generated text on matters of public interest | Apply the specific publication, purpose and human-review/editorial-control conditions and exceptions. | Label only when the applicable test is met. |

The European Commission's July 2026 transparency guidance (art. 50 obligations applying from 2 August 2026, subject to relevant transitions) distinguishes provider machine-readable output marking from deployer visible disclosures. Do not turn a provider-only obligation into a blanket label rule for every SME. Review the applicable consolidated law and transition provisions before future releases.

## 7. Accessibility, consumer law and sector branches

WCAG 2.2 AA is the **Handbook engineering quality target** (src-w3c-wcag-22; std-ui-ux-quality-baseline), not proof that Law 11/2023 automatically covers every public page. For that law, classify the actual service category (including whether there is an actual electronic contracting service), dates, business size and microenterprise exemptions. A “contact us for a quote” form is not automatically a checkout. Other disability/consumer laws may still matter; record applicability rather than claiming blanket exemption. An accessibility toolbar or declaration is not universally mandatory merely because a site is publicly visible.

No on-site sale means no need to invent checkout flows, payment-card terms, withdrawal buttons or pricing for nonexistent transactions. It does not remove identity, privacy, advertising truth, consent, accessibility engineering or security obligations. Add sector-specific gates for health, finance, regulated professions, children, transport, reservations or actual remote contracting only when triggered by real facts.

## 8. Empirical comparison: observations versus unverified leads

The exploratory sample was **purposive, not representative**, and most of its claimed technical observations lack saved request/response evidence. The only directly cited public pages retained in the research result are:

| Site / sector | Direct evidence URL | Narrow supported observation | Not established |
| --- | --- | --- | --- |
| Vandelay, digital agency | https://vandelay.es/politica-de-cookies/ ; https://vandelay.es/contacto/ (src-observation-vandelay-cookies-2026-11; src-observation-vandelay-contact-2026-11) | Published cookie inventory naming _ga and WordPress-related entries; contact page exposes consent-management UI. | Whether the currently served tag is blocked before consent; legal sufficiency. |
| The Digital Adgency, agency | https://thedigitaladgency.com/contacta-y-crece/ (src-observation-tda-contact-2026-11) | Contact page displays cookie-consent wording and a preferences entry. | GTM/Consent Mode runtime behavior, request blocking, full vendor inventory. |
| COME, restaurant | https://come.com.es/contacto/ (src-observation-come-contact-2026-11) | Contact page has a form and privacy-policy acknowledgment. | Whether a cookie banner appears in all contexts or whether non-exempt tracking occurs. |
| Interprint BCN, print services | https://www.interprintbcn.com/contacto/ (src-observation-interprint-contact-2026-11) | Contact page links an aviso legal and identifies a business name in the footer. | Completeness/currentness of the policy, actual analytics configuration. |

These are **examples of public presentation**, not compliance certifications or accusations. Policy contents can change. Re-capture URL, UTC date, visible copy, page state, cookie storage and network HAR before promoting a competitor observation to an operational rule.

The exploratory report additionally **named but did not independently substantiate a full technical/legal audit** of these discovery candidates, grouped for later targeted research:

- Mudanzas: mudanzasdym.com; mudanzasbarrios.es; fcmudanzasytransportes.com.
- Reformas: ureformas.es; bcn3.es; empresareformabarcelona.com; milreformes.com.
- Limpieza/servicios: cliner.com; cleanermax.es; manitasadomiciliomadrid.com.
- Talleres: tallerbarcelona.com; autotalleresbcn.com; arnaureparaciones.es; tallerscompte.com.
- Gestorías/asesorías: barcelonagestoria.es; aygasesores.com; apftconsultoria.es; rospetit.es.
- Despachos/arquitectura: aemeadvocats.com; campsyrojasabogados.com; martinezcaballeroabogados.com; mvaarquitectura.com; arch.cat.
- Agencias/restauración: articagency.com; eltribut.com.

**Do not report “40–60 audited websites”, “GA4 definitely fires before consent” or “site X is unlawful” from this dataset.** The reusable value is the decision matrix, primary-source distinctions, verification procedure and candidate discovery list, not an unsupported sample size.

## 9. False-positive traps in the exploratory report

Reject these claims when encountered in future prompts, audits or auto-generated legal copy:

1. “All public SME websites must legally meet WCAG 2.2 AA and publish an accessibility statement/widget.” **False as a universal legal claim**; retain WCAG as internal engineering target and assess legal scope.
2. “Every form needs an obligatory ‘I accept privacy policy’ checkbox.” **False**; AEPD distinguishes notice from consent.
3. “Every AI-generated text/image must visibly say AI-generated.” **Overbroad**; assess art. 50 roles and content tests.
4. “Every cookieless analytics implementation is exempt” or “every one always needs cookie consent.” **Both overbroad**; inspect terminal access and GDPR processing separately.
5. “GTM + Consent Mode denied guarantees no requests.” **False for some advanced-mode configurations**; test network.
6. “All vendors are US subprocessors and all Supabase data are US-hosted.” **Unverified**; inspect the actual region, roles and contract chain.
7. “Privacy Shield is the current transfer framework.” **Outdated**; assess the current EU-US DPF, SCCs or other lawful routes.
8. “Lead retention is legally fixed at 2–3 years; IP logs at six months.” **Unsupported generalisations**.
9. “Any lead score triggers GDPR art. 22.” **Overbroad**; apply the solely automated significant-effects test.
10. “AEPD must notify every breach to every visitor within 72 hours.” **False**; authority and affected-person notification thresholds/timelines differ.
11. “No payments means no legal obligations” or “a quote request is an online sale.” **Both false**.
12. “A screenshot of a banner proves compliance” or “a passing mock proves a production conversion.” **False evidence level**.

## 10. Maintenance and future reuse

- At **every launch or material change**: re-evaluate actual data flows, third-party SDKs, legal scope, vendor contracts, texts, retention and evidence. A new map, captcha, chatbot, analytics tag or marketing channel reopens the affected assessment.
- **Quarterly or before vendor changes**: recheck volatile provider DPA, subprocessors, transfer and analytics/consent behavior; recheck official AI Act guidance and AEPD cookie updates.
- **Annually or upon legal change**: refresh statutory applicability and controller-approved public texts. Do not silently bump last_verified without checking the source.
- Record **observed / declared / inferred / not verified**, with date, environment and responsible reviewer. Keep client identity, private contracts, raw leads, screenshots with personal data and legal approvals **outside the public Handbook** in the authorised client repository or private dossier.
- If a new investigation adds real browser traces and legal-policy captures for additional sites, append only evidence-backed findings to this reference or supersede it deliberately; never create a second active normative legal standard.

**Reuse path:** standard -> playbook -> per-client evidence pack -> owner/legal sign-off -> technical release evidence. This avoids repeating the whole market study while preserving the right to revalidate volatile facts.
