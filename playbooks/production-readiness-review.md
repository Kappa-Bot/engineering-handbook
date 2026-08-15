---
id: pb-production-readiness-review
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - production-readiness
  - production-releases
sources:
  - src-nist-ssdf-11
  - src-openssf-secure-software-guiding-principles
  - src-opentelemetry-signals
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Production Readiness Review

Use before a first production launch or a change that materially alters production risk. Keep the review proportional; a small low-risk site does not need a microservices/SRE launch checklist.

## 1. Capability truth

Confirm which capabilities are actually production-real:

- persistence;
- auth/authz;
- external integrations;
- billing/delivery;
- migrations;
- PWA/offline if claimed.

Remove or clearly isolate demo/mock fallbacks.

## 2. Security boundaries

Review:

- privileged credentials;
- authorization at protected operations;
- environment secret scope;
- abuse/replay/idempotency where relevant;
- negative-path security evidence.

## 3. Data and migrations

Confirm:

- Production cannot be reset/seeded by ordinary setup;
- migrations target the intended environment;
- backup/recovery implications are understood;
- destructive/history-sensitive changes have a deliberate path.

## 4. Release provenance

Know the exact build/commit and target environment.

Separate:

- source checks;
- deployment result;
- migration result;
- post-deploy smoke;
- physical/native/manual checks.

## 5. Runtime operability

Answer:

- how will we know the important product path is broken?
- where will useful diagnostic evidence appear?
- which build/environment is running?
- what is the first recovery action?

Add logs/metrics/traces/synthetics only where they answer those questions.

## 6. Dependency/supply-chain review

For privileged workflows and critical dependencies:

- confirm lock/resolution discipline;
- review unsupported/high-risk dependencies;
- pin third-party Actions/workflows immutably where appropriate;
- minimize workflow permissions/secrets;
- consider SBOM/provenance/signing only where distribution/risk warrants.

## 7. API/compatibility review

If independent consumers exist, confirm contract/version/deprecation expectations and whether formal OpenAPI/contract tests would reduce real risk.

## 8. Performance

For performance-sensitive user journeys, compare against a representative baseline or repo-specific budget. Do not create arbitrary launch-blocking numbers without a measurement contract.

## 9. Final readiness record

Report only meaningful outcomes:

```text
passed
failed
not run
blocked
not applicable
```

Include material residual risk and manual/provider/device assumptions.

A polished launch checklist is not evidence. Executed, attributable checks are.
