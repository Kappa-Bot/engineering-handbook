---
id: std-architecture-data-integrity-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - application-repositories
  - services
  - data-backed-products
sources:
  - src-nist-ssdf-11
  - src-madr
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Architecture and Data Integrity Baseline

## Purpose

Define the minimum cross-repository architecture/data discipline without prescribing a universal framework, database, cloud, monorepo layout or backend topology.

The Standard favors explicit boundaries and truthful state over premature abstraction.

## 1. Name sources of truth

For each durable concern that can materially diverge, the repository MUST identify the authoritative source of truth.

Typical concerns include identity, authorization, product/domain state, billing, files, configuration, schedules, audit records and deployment state.

Duplicated representations MAY exist for caching, denormalization, search or integration, but their ownership and reconciliation semantics MUST be clear.

See `pat-source-of-truth-boundaries`.

## 2. Keep domain decisions out of incidental UI state

Business invariants that affect permissions, money, history, scheduling, entitlements, inventory, reporting or external behavior MUST NOT exist only as presentation conditions.

Place durable rules behind a boundary that can be verified independently from a particular screen.

The exact architecture is repo-local: server functions, domain services, database constraints/RLS, RPCs, application services or another appropriate mechanism may satisfy the requirement.

## 3. Prefer the smallest architecture that is honest

Do not introduce a backend, queue, event bus, repository abstraction, generic platform package or distributed component solely because it may be useful later.

Likewise, do not keep a local/mock implementation after the product claims durable production behavior if that implementation can create false confidence.

Complexity is justified by a current invariant, verified scale need, security boundary, integration need, operability need or demonstrated reuse.

## 4. Generalization requires consumers

A product-specific implementation SHOULD remain product-specific until another real consumer or strong independent evidence demonstrates a stable reusable boundary.

Do not extract a generic core merely because names can be parameterized.

When reuse emerges, identify:

- what is genuinely common;
- what remains tenant/product/domain policy;
- compatibility/versioning expectations;
- migration path for existing consumers;
- what evidence demonstrates the abstraction is better than duplication.

## 5. Data integrity before convenience

Where data has operational, financial, legal, security or historical meaning:

- invalid state transitions MUST be rejected rather than silently normalized;
- destructive operations SHOULD be replaced by status/revocation/void/audit semantics when history matters;
- generated identifiers/tokens MUST have documented uniqueness/security requirements;
- idempotency SHOULD be used for retried external or mutation workflows where duplicate effects are harmful;
- migrations MUST be treated as executable changes to production state, not ordinary source edits;
- seed/reset tooling MUST be scoped so Production cannot be reset accidentally.

## 6. Schema and authorization are part of architecture

When the data platform supports server-side constraints or row/data policies, use them where they materially protect invariants or tenant/user isolation.

Client filters and hidden routes MUST NOT be the sole protection for sensitive data.

Provider-specific mechanisms such as PostgreSQL constraints, RLS, Supabase policies or equivalent remain repo-local implementation choices.

## 7. Environment-specific architecture is allowed

Demo, local, Preview, QA and Production MAY intentionally use different components when the difference is explicit and cannot be mistaken for production equivalence.

Use `pol-truthful-engineering` and `pat-capability-environment-integrity`.

## 8. Durable architecture decisions

Record a repo-local ADR/decision when a choice changes long-lived boundaries, source-of-truth ownership, persistence strategy, security model, integration contract, deployment topology, compatibility obligations or costly future migration.

Do not create ADRs for routine implementation detail.

## 9. Definition of done

An architecture/data change is complete when:

- authoritative owners are clear;
- invariants are enforced at an appropriate boundary;
- failure and retry semantics are understood;
- migrations/data transformations have a verification path where applicable;
- mock/demo/production differences are explicit;
- premature reusable abstractions were avoided or justified;
- durable decisions are recorded when future contributors would otherwise need to rediscover them.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "architecture-authoritative-owner",
      "type": "decision-question",
      "text": "What is the authoritative source of truth for each durable concern changed by this task?",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["data-loss"],
      "activate_when": ["capability:persistence", "operation:mutation", "operation:migration"],
      "force": "must",
      "phase": ["planning"],
      "priority": 92
    },
    {
      "id": "architecture-migrations-are-production-state",
      "type": "constraint",
      "text": "Treat migrations as executable changes to production state rather than ordinary source edits.",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["data-loss"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 100
    },
    {
      "id": "architecture-migration-verification",
      "type": "verification",
      "text": "Verify the migration or data transformation path when the change alters durable state.",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["data-loss"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "must",
      "phase": ["verification"],
      "priority": 100
    },
    {
      "id": "architecture-generalization-needs-evidence",
      "type": "constraint",
      "text": "Keep product-specific implementations local until another real consumer or strong evidence demonstrates a stable reusable boundary.",
      "source": "std-architecture-data-integrity-baseline",
      "covers": ["compatibility"],
      "activate_when": ["intent:create", "intent:modify"],
      "force": "should",
      "phase": ["planning"],
      "priority": 35
    }
  ]
}
```
