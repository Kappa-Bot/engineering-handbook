---
id: ref-internal-engineering-donor-audit
kind: reference
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
  - all-repositories
sources:
  - src-nist-ssdf-11
  - src-nist-ssdf-publications
  - src-owasp-asvs-500
  - src-github-deployment-environments
  - src-github-actions-security
  - src-openssf-scorecard
  - src-opentelemetry-signals
  - src-openapi-spec
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Internal Engineering Donor Audit — 2026-08-15

## Status

Supporting evidence, not a normative Standard.

This audit extends `ref-internal-ui-pwa-donor-audit` across architecture, data, security, testing, CI/CD, release, operations, observability, performance, APIs and software supply chain.

Audited repositories and main-tree snapshots:

- `Kappa-Bot/CCSE-AI-Coach` — `4aaada8d5cfcf132d7873585124beb94f7ddf32d`;
- `Kappa-Bot/alumini-bartra-webapp` — `d227118151f90e8b625d31c4ce86eac3375f02f1`;
- `Kappa-Bot/cogop-barcelona-attendance` — `e7bd5ad1e8c02cded380dd17c8f007481af37dc7`;
- `Kappa-Bot/movops-os` — `3c8de888357f04e8f50dddb1d84bf7dd540b2dbe`.

The goal is not to select a best repository. Each donor is stronger in different areas. Promotion keeps the reusable invariant and removes provider/product-specific assumptions.

## CCSE-AI-Coach

Strong reusable evidence:

- explicit concern ownership: Clerk identity, Supabase domain persistence/RLS, Stripe billing, Sentry error/tracing, Checkly production synthetics;
- `service_role` reserved for administrative/cron/backfill work rather than normal user execution;
- entitlement resolution centralized instead of relying on isolated proxy fields;
- GDPR requests recorded/auditable before later manual action;
- separate Production and Preview configuration audits;
- deployment/environment runbooks and Supabase migration automation;
- security/content/release verification as distinct concerns.

Do not promote as universal defaults:

- Clerk, Supabase, Stripe, Vercel, Sentry or Checkly themselves;
- CCSE domain scoring, trial or billing rules;
- direct provider-specific environment variable names.

Promoted principle: **name authoritative owners and keep provider snapshots/derived state subordinate to the real source of truth.**

## Aluminio Bartra webapp

Strong reusable evidence:

- explicit mock-first architecture when real persistence was intentionally unavailable;
- visible demo boundaries rather than pretending localStorage was production persistence;
- inactive future Supabase artifacts kept as reference without runtime coupling;
- no fake access-link revocation in a client-only demo because real revocation requires server persistence;
- selective real capabilities instead of building every future backend feature early;
- architecture decisions record tradeoffs and future migration cautions.

Do not promote:

- mock-first as a preferred production architecture;
- localStorage as durable SaaS persistence;
- Supabase future artifacts as an organization-wide database choice.

Promoted principle: **a demo may be incomplete but MUST remain truthful about what is real, mocked or scaffolded.**

## COGOP Barcelona Attendance

Strong reusable evidence:

- server/data-side role validation; UI role state is not security;
- privileged service role limited to server/scripts;
- signed/revocable access-link semantics and bearer-link operational discipline;
- QR credentials store hash while raw value is shown/exported only when needed;
- audit/state/revocation preferred to destructive delete when history matters;
- explicit integrity rule: do not fabricate attendance when the required activity/permission does not exist;
- frozen dependency install, repeatable local setup, database lint/test/schema verification, browser/visual/responsive checks;
- release flow distinguishes quality from remote deployment and validates exact SHA, target, migrations/schema and signed-session smoke;
- Production never receives seed/reset;
- physical checks are recorded as passed/failed/not performed rather than inferred.

Do not promote:

- church-specific roles/reporting semantics;
- exact QA branch topology;
- Supabase/Vercel implementation details as universal.

Promoted principles: **authorization at the protected boundary; integrity-sensitive failures fail explicitly; build quality and deployed quality are different evidence.**

## MovOps OS

Strong reusable evidence:

- avoids extracting a generic MovOps/white-label core before a second customer validates the abstraction;
- backend-light domain demo while the small/high-value admin access boundary is real server-side;
- domain aggregates and resource abstractions introduced because present workflows justify them, not to chase architecture patterns;
- layered testing: domain, component, E2E, accessibility;
- E2E access harness uses high-entropy credentials, stores/passes verifier material appropriately and does not print secrets;
- explicit acceptance, CI-state, release and donor-reuse documentation;
- metrics/analytics shown only when they change operational decisions.

Do not promote:

- Agurto-specific domain aggregates as generic business abstractions;
- historical multi-agent execution model;
- exact viewport/phase/acceptance numbering.

Promoted principles: **generalization requires evidence; make cheap important security boundaries real even when the surrounding demo is mocked; verification layers map to failure classes.**

## Combined model

```text
CCSE
source-of-truth ownership + environment/runbook maturity
        +
Bartra
truthful mock/demo capability boundaries
        +
COGOP
server-side authorization + release/environment integrity
        +
MovOps
anti-premature-generalization + layered evidence
        +
primary external authority
NIST SSDF + OWASP ASVS/Cheat Sheets + GitHub + OpenSSF + OTel + OpenAPI
        ↓
organization engineering baselines
```

## Promoted cross-repository principles

1. **Truthful engineering.** Do not make a missing production capability look present.
2. **Explicit sources of truth.** Name which system/boundary owns each durable concern.
3. **Authorization lives at the protected operation/data boundary.** UI is not the gate.
4. **Least privilege and secret containment.** Administrative/service credentials stay server/automation scoped.
5. **Generalization follows consumers.** Product-specific code may stay local until reuse is demonstrated.
6. **Data history has semantics.** Prefer revoke/void/status/audit over destructive deletion when history matters.
7. **Evidence is risk-based.** Use the cheapest layer that can falsify the important assumption.
8. **CI green is scoped evidence.** Build/test success does not prove remote deployment or production behavior.
9. **Release provenance matters.** Know the exact source/build, target, migrations and post-deploy result.
10. **Observability answers questions.** Do not collect signals or create dashboards without diagnostic/decision value.
11. **Formal API contracts are contextual.** OpenAPI is useful when independent consumers make drift expensive, not for ceremony.
12. **Supply-chain controls are proportional.** Immutable Actions, least privilege and dependency hygiene are baseline; SBOM/signing/attestation depend on distribution/risk.
13. **Performance budgets are product/journey-specific.** Measure representative user impact instead of importing arbitrary universal numbers.

## External-source status note

NIST SP 800-218 / SSDF v1.1 remains the current final general SSDF baseline used by this handbook. NIST lists SP 800-218 Rev.1 / SSDF v1.2 as a draft as of this audit; draft existence MUST NOT be treated as final normative replacement.

OWASP ASVS 5.0.0 is used as a verification catalog, not as an automatic requirement that every repository execute every ASVS control.

OpenSSF Scorecard is an evaluation signal, not a universal numeric acceptance threshold.

OpenTelemetry and OpenAPI are preferred standards when their mechanisms are actually needed; neither is a mandatory dependency for all products.
