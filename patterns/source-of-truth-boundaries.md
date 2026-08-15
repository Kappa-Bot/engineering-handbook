---
id: pat-source-of-truth-boundaries
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - data-backed-products
  - integrated-systems
sources:
  - src-nist-ssdf-11
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Source-of-Truth Boundaries

## Intent

Prevent contradictory application state by assigning clear ownership to durable concerns.

## Pattern

For each concern, define:

```text
Concern
  → authoritative owner
  → derived/replicated representations
  → write path
  → read path
  → reconciliation/failure behavior
```

Examples:

- identity may be owned by an identity provider while the app stores a local profile snapshot;
- billing may be owned by a payment provider while the app stores normalized entitlement state;
- operational records may be owned by the application database while analytics/search indexes are derived;
- deployment truth belongs to the deployment platform/environment, not to a successful build alone.

## Rules of thumb

- One concern can have multiple representations but SHOULD have one authoritative owner for each decision.
- A cache MUST NOT silently become the write authority.
- A replicated snapshot MUST have a refresh/reconciliation story when staleness can change a decision.
- External-source webhooks/events SHOULD be idempotent where retries are possible.
- Privileged administrative writes SHOULD be distinguishable from user-scoped writes.
- Do not read one field as a proxy for a richer canonical state when the proxy can become stale or ambiguous.

## When not to use

Do not invent extra layers for purely local state that has no realistic divergence risk.

The purpose is clarity, not mandatory indirection.
