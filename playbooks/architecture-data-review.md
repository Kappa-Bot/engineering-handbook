---
id: pb-architecture-data-review
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - architecture-changes
  - data-model-changes
  - persistence-changes
sources:
  - src-nist-ssdf-11
  - src-madr
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Architecture and Data Review

Use this playbook for changes that alter durable boundaries, persistence, tenancy, important domain invariants, integrations or reusable-core extraction.

## 1. Start from the product invariant

Write the concrete behavior that must remain true.

Avoid beginning with a technology choice.

## 2. Map authoritative owners

For each affected concern, identify:

- source of truth;
- who may write;
- who may read;
- derived copies/caches;
- retry/reconciliation behavior;
- historical/audit requirements.

## 3. Inspect donors before inventing

Search current repo → handbook → mature internal repos.

For transversal work, compare donors only when their context is close enough to improve the decision. Do not copy provider-specific mechanics without checking fit.

## 4. Challenge complexity

For each new abstraction/service/table/queue/package ask:

- what present requirement forces it?
- what fails without it?
- can the boundary remain local until a second consumer exists?
- does the abstraction remove meaningful duplication or only rename it?

## 5. Review data failure modes

Cover, where applicable:

- duplicates/retries;
- partial writes;
- stale derived state;
- race/conflict behavior;
- destructive history loss;
- migration rollback/forward-fix;
- seed/reset safety;
- external provider outage.

## 6. Record durable decisions

Use `templates/decision.md` when the choice would otherwise be rediscovered.

## 7. Verify

Run the smallest evidence set that can falsify the risky assumptions:

- domain/unit tests for invariants;
- database/policy tests for data isolation;
- migration verification;
- integration/E2E for boundary crossing;
- explicit environment check for real external systems.

Report anything not run.
