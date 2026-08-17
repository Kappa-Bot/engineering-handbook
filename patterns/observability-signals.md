---
id: pat-observability-signals
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - production-applications
  - services
sources:
  - src-opentelemetry-signals
  - src-opentelemetry-semantic-conventions
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Observability Signals by Diagnostic Question

## Intent

Select the smallest telemetry set that lets operators understand important failures and user impact.

## Start with questions

Examples:

- Why did this request fail?
- Is error rate increasing?
- Which external dependency is slow?
- Is the user's critical journey reachable?
- Is scheduled/background work progressing?
- Which build introduced the regression?

Then choose signals.

## Signal guide

### Logs / error events

Best for discrete failures and diagnostic detail.

Prefer structured fields for stable dimensions such as environment, release/build, operation and safe correlation IDs.

Do not log secrets, authorization tokens or unnecessary sensitive payloads.

### Metrics

Best for aggregate rates, counts, latency distributions, saturation/capacity and business-operational indicators.

Use bounded dimensions. Avoid unbounded high-cardinality labels merely because they are available.

### Traces

Useful when an operation crosses meaningful process/service/provider boundaries and finding where time/failure occurred is otherwise difficult.

Do not add distributed tracing to a simple single-process application if ordinary error context already answers the important questions.

### Synthetic checks

Useful for externally meaningful availability/behavior that infrastructure health cannot prove.

Keep them deterministic and safe. Prefer read-only or isolated test identities/data for production synthetics.

### Domain/operational signals

Some of the most useful signals are domain-specific: stale jobs, unprocessed callbacks, failed payments, invalid attendance capture, conflict rates or migration drift.

Only measure them if someone can interpret and act on them.

## Correlation

Where multiple signals exist, propagate safe correlation/release/environment context so an operator can move from an alert to relevant diagnostic evidence.

When using OpenTelemetry, follow applicable semantic conventions where stable and relevant rather than inventing incompatible names.

## Cardinality, cost and privacy

Telemetry is production data. Review retention, volume, PII and cardinality when they affect cost/privacy/operability.

More telemetry is not automatically more observable.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "observability-question-before-signal",
      "type": "decision-question",
      "text": "Which operational question must be answered, and what is the smallest log, metric, trace, synthetic, or domain signal that reliably answers it?",
      "source": "pat-observability-signals",
      "covers": ["availability"],
      "activate_when": ["delivery:production", "operation:integration", "operation:deployment"],
      "phase": ["planning"],
      "priority": 70
    },
    {
      "id": "observability-no-sensitive-telemetry",
      "type": "constraint",
      "text": "Do not log secrets, authorization tokens, or unnecessary sensitive payloads; treat telemetry volume, retention, PII, and cardinality as production concerns.",
      "source": "pat-observability-signals",
      "covers": ["credential"],
      "activate_when": ["risk:credential", "delivery:production"],
      "force": "must-not",
      "phase": ["implementation", "verification"],
      "priority": 94
    }
  ]
}
```
