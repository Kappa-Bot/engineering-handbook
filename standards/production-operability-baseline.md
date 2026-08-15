---
id: std-production-operability-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - production-applications
  - production-services
sources:
  - src-nist-ssdf-11
  - src-opentelemetry-signals
  - src-opentelemetry-semantic-conventions
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Production Operability Baseline

## Purpose

Define the minimum ability to understand, operate and recover a production product without forcing every repository into enterprise SRE ceremony or a particular observability vendor.

The required depth is proportional to consequence, usage and operational complexity.

## 1. Runtime truth is separate from build truth

A successful build or CI run does not prove the deployed product is healthy.

Production-relevant systems SHOULD have an environment-appropriate way to answer:

- what version/build is running;
- whether the critical surface is reachable/healthy enough for its purpose;
- whether material failures are occurring;
- where an operator can find useful diagnostic context;
- what recovery/escalation action exists.

## 2. Select observability signals by question

Logs, metrics, traces, synthetic checks, domain events and profiles are tools, not mandatory badges.

Choose a signal because it answers an operational question. Do not collect every signal merely because a platform supports it.

Examples:

- errors/logs: what failed and with which safe context?
- metrics: is a quantity/rate/latency changing?
- traces: where did a request/operation spend time across boundaries?
- synthetics: can an externally important journey/surface still work?
- domain health: is the product producing valid business outcomes?

Use `pat-observability-signals`.

## 3. Observability must be actionable and safe

Operational telemetry SHOULD contain enough stable context to correlate failures without leaking secrets or unnecessary personal data.

Secrets, bearer credentials and sensitive payloads MUST NOT be intentionally logged.

High-volume telemetry SHOULD be bounded by diagnostic value, cost and privacy.

If OpenTelemetry is used, prefer applicable stable semantic conventions instead of inventing incompatible naming where practical. OpenTelemetry itself is NOT required by this Standard.

## 4. User-impact and system health are different

A process being up does not necessarily mean the product works.

For important products, include at least one signal tied to externally meaningful behavior when infrastructure health alone can miss user-impacting failure.

Examples include signed/authenticated smoke, synthetic checkout/check-in, successful provider callback, data freshness or queue progress.

Do not create synthetic actions that mutate real production business state unless the workflow safely isolates/reverses them.

## 5. Reporting semantics remain truthful

Operational/product reports MUST distinguish unknown, unavailable, excluded or partial data from a meaningful zero when that distinction changes interpretation.

Do not manufacture a metric to fill a dashboard.

Metrics and alerts SHOULD exist because they influence diagnosis, product decisions or response—not because an observability stack offers a widget.

## 6. Recovery is part of readiness

For material production risks, know the practical recovery mechanism:

- retry/replay;
- rollback;
- forward-fix;
- credential rotation;
- migration repair;
- restore/reconciliation;
- feature disable/degradation;
- operator runbook.

Not every application needs a formal incident-management program. High-consequence operations do need recoverable procedures that are more concrete than “fix it manually”.

## 7. Data durability

When loss of durable data would be materially harmful, the product SHOULD have a provider-appropriate backup/restore or recovery strategy and enough knowledge to verify that the strategy is usable.

Do not claim recoverability solely because a provider markets backups; understand the configured product/tier and restore path relevant to the application.

## 8. Production configuration

Production configuration/secrets MUST be treated as environment-specific state.

Deployment/readiness review SHOULD account for configuration that cannot be proven from source alone.

## 9. Definition of done

A production-operability change is complete when:

- important runtime failures can be observed with useful safe context;
- health/version evidence exists where the product risk warrants it;
- operational claims distinguish build, deployment and runtime truth;
- critical recovery mechanisms are known;
- telemetry does not intentionally expose credentials/sensitive data;
- unknown/partial data is not presented as meaningful zero;
- any unverified backup/restore/native/provider assumptions are disclosed.
