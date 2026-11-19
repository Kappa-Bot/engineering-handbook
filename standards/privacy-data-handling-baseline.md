---
id: std-privacy-data-handling-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - applications
  - services
  - internal-consoles
  - connected-products
  - ai-agentic-workflows
sources:
  - src-eu-gdpr
  - src-aepd-privacy-clause-faq
  - src-nist-ssdf-11
  - src-owasp-asvs-500
last_verified: 2026-11-19
review_due: 2027-02-19
---

# Privacy and Personal Data Handling Baseline

## Purpose, scope and authority

This is the cross-product **engineering** baseline for personal data handled by MelodIQ/Kappa-Bot products, connected CRM/API services, internal operator consoles, agent workflows and public web surfaces. It covers data discovery, minimization, purpose-specific behavior, exposure, lifecycle and actual technical evidence. **It is not legal advice or a universal privacy policy template.**

For a public/commercial Spanish client website, [Public Website Legal and Trust](public-website-legal-trust-baseline.md) remains the canonical normative owner for the actual site obligations and published legal identity/copy, with the [Spanish privacy/consent audit](../playbooks/spanish-client-website-privacy-consent-audit.md) as the specialized procedure. This Standard governs general data-handling engineering and does not override the applicable legal determination. Real controllers/clients and their qualified advisers approve legal bases, disclosure, contracts and final retention decisions.

The [Security/Identity](security-identity-baseline.md), [Architecture/Data Integrity](architecture-data-integrity-baseline.md) and [Production Operability](production-operability-baseline.md) Standards own authorization, consistency, privileged credentials and operational recovery. This Standard adds **privacy-specific questions and proof**, not new alternative implementations for those controls.

## 1. Identify every personal-data path before assessing it

For a material privacy change or audit, trace the real flow:

```text
collection / derived event
  → browser or agent/runtime
  → authenticated or anonymous API
  → server/queue/database/object store
  → integration/processor/log/analytics
  → retention, export, deletion and recovery
```

For each material purpose, identify actual data fields/categories, controller and processor relationships, source and recipients, jurisdiction/transfer questions, protection boundary, retention criterion, consent/legal decision if applicable, and real deletion/export mechanism. Include **indirect** personal data: IPs, URLs/referrers, image metadata, attachments, event properties, telemetry, support notes, prompt/tool transcripts, exported datasets, backup copies and derived/profiling fields.

Do not infer that a product stores no personal data because its public form is absent or its analytics SDK claims to use no cookies. Do not invent vendors, data locations, legal bases, DPA acceptance or fixed universal retention periods.

## 2. Minimum necessary data and purpose-specific behavior

- Collect, expose and keep the minimum information necessary for the verified product purpose. Required/optional fields, default values, attachments and secondary enrichment should reflect that purpose rather than the database's full schema.
- Separate requested service delivery, account/security operations, optional analytics/attribution and unrelated commercial communications. A consent checkbox is **not** universally the appropriate legal basis; assess each purpose with the responsible owner.
- Gate optional terminal access/analytics/cross-site providers when legally/contractually required; test that rejection/withdrawal actually stops future optional calls without disabling the essential service. UI label alone is insufficient.
- Avoid PII in query parameters, referrers, third-party analytics payloads, telemetry, exception strings, share links, screenshots, test fixtures and public logs. A hash or pseudonymous identifier can remain personal data depending on context; treat it proportionately.
- Preserve private data in access-controlled server/storage paths. Client-only hiding, unguessable identifiers and CSS are not access controls. Secure file upload includes content/type validation, metadata handling, access TTL and retention as appropriate to the real workflow.

## 3. Access, data boundaries and agency/agent use

- Protect data reads, exports, mutations and indirect search from inappropriate roles, objects and tenants at the authoritative server/data boundary. Apply the Security Standard's negative-path tests.
- Scope service credentials and automated agents to the actual purpose and approved systems. Prompt context, retrieval indexes, memory, tool responses and downstream model/provider calls are **data processing paths**; assess their data categories, access, retention and provider boundaries before reusing customer data in a new agent workflow.
- Preserve real tenant/demo/Preview/QA/Production isolation. Synthetic or seeded examples MUST be marked as examples; do not mix production customer content into demos/tests without an approved, protected purpose and path.
- Check exports, emails, notifications, logs and support access as independent disclosure surfaces. A deleted UI row is not proof that a queue, blob, backup, replica or external recipient no longer has data.

## 4. Retention, correction, erasure and operational lifecycle

- Establish a product/owner-approved retention **rule or criterion** per purpose and data category, including drafts, completed leads, uploaded media, authentication/session data, analytics, logs and temporary files as relevant. Do not invent a single global TTL.
- Identify what starts the clock, where it is enforced, what deletion means, whether backups/archives or external processors need separate handling, how retries/crashes avoid orphaned copies, and what lawful restrictions or preservation obligations apply.
- Provide an owner-accountable path for access, correction, portability and erasure requests where legally applicable. Product tooling may implement the mechanical path; the controller decides eligibility, timing and exceptions.
- Treat retention and deletion changes as durable-data changes requiring [Architecture/Data Review](../playbooks/architecture-data-review.md) and relevant release/rollback evidence. Do not run deletion tests against real production data merely to prove a workflow.
- For accidental exposure or breach indicators, preserve suitable restricted evidence, escalate through the actual incident owner and assess notification duties with the controller. Do not copy private records or exploit details into public issues.

## 5. Review and verification

Select proportionate evidence by the affected boundary:

| Failure class | Useful proof |
| --- | --- |
| Unexpected collection/analytics before a permitted choice | Fresh browser profile and request/storage capture before and after consent, withdrawal/reload and relevant cross-tab state |
| PII in frontend, URL, telemetry or third-party calls | Payload/URL/referrer/network and client-bundle inspection, representative safe fixtures; provider behavior actually observed |
| Role/tenant leak | Denied cross-role, cross-object and cross-tenant reads/exports using authorized non-production fixtures |
| Orphaned upload/draft or failed erasure | Real lifecycle tests with queue/retry/partial failure, object-store checks and documented retention semantics |
| Agent cross-purpose data use | Trace prompt/context/tool/provider records, permissions and retention from the actual integration; do not assume a no-store setting without evidence |
| Public legal disclosure, cookie exemptions, provider contracts | Controller-approved facts and specialist public-site legal audit; technical tests do not sign the legal determination |

Use the existing [Quality and Release Review](../playbooks/quality-release-review.md) evidence vocabulary: `passed`, `failed`, `not run`, `blocked`, `not applicable`. A static scan or generic GDPR banner is never a full privacy PASS. A review-only task identifies findings; correction, external publication and Production changes require separate authority. Report restricted findings with appropriate access controls.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "privacy-data-flow-review",
      "type": "decision-question",
      "text": "For a privacy review, map actual personal-data categories and purposes through client, server, storage, analytics/logs, integrations and agents; identify controller/processor roles, consent/legal decisions, access and retention/deletion boundaries without inventing a legal basis or fixed TTL. Use public website legal owner only for an actual public site.",
      "source": "std-privacy-data-handling-baseline",
      "covers": ["privacy-exposure"],
      "activate_when": ["archetype:privacy-review", "risk:privacy-exposure"],
      "force": "must",
      "phase": ["planning", "implementation"],
      "priority": 98
    },
    {
      "id": "privacy-boundary-evidence",
      "type": "verification",
      "text": "Verify the affected collection-to-recipient-to-retention path: consent/network when applicable, no unapproved PII leakage, negative role/tenant access, and actual safe deletion/export behavior. Distinguish technical evidence from legal/controller approval and identify unrun external or Production gates.",
      "source": "std-privacy-data-handling-baseline",
      "covers": ["privacy-exposure"],
      "activate_when": ["archetype:privacy-review", "risk:privacy-exposure"],
      "force": "must",
      "phase": ["verification"],
      "priority": 98
    }
  ]
}
```
