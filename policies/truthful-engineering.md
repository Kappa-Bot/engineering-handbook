---
id: pol-truthful-engineering
kind: policy
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Truthful Engineering

## Purpose

Engineering artifacts, product behavior, documentation, demos, tests and release claims MUST describe capabilities that actually exist in the environment being discussed.

A useful demo can be incomplete. A production system can be intentionally online-only. A CI pipeline can cover only part of the release risk. What is not acceptable is presenting one of those states as something stronger than it is.

## Core rule

**Do not simulate confidence.**

A repository MUST NOT silently make a missing production capability appear present through UI-only restrictions, fake persistence, local fallbacks, synthetic success paths, placeholder security, hidden errors, or unsupported verification claims.

## Capability states

When the distinction can affect a user, operator, reviewer or engineering decision, a capability SHOULD be identifiable as one of:

- real and active;
- real but environment-limited;
- mock/demo/local-only;
- scaffolded or contract-only;
- intentionally unavailable;
- planned/future.

The names do not need to be exposed literally to end users, but the behavior and engineering documentation MUST remain unambiguous.

## Environment integrity

- Production MUST NOT fall back to mock/local persistence merely to keep a workflow appearing successful unless that fallback is an explicit production capability with defined semantics.
- Demo/mock data MUST NOT be described as production persistence.
- Client-side route hiding MUST NOT be described as authorization.
- A non-revocable local token/link MUST NOT be described as revocable security.
- Online-only behavior MUST NOT be described as offline-capable.
- A test double MUST NOT be used as evidence that an external integration or deployment succeeded.
- Preview/QA configuration MUST NOT be assumed to represent Production configuration.
- A green CI result MUST be described only as evidence for the gates actually executed.

## Failure behavior

When a required capability is unavailable, prefer an explicit unavailable/error/degraded state over silently fabricating a successful outcome.

For integrity-sensitive workflows, a truthful failure is better than invented data. Examples include attendance, billing, access control, scheduling, migrations, external delivery and destructive operations.

## Documentation and provenance

Durable architecture/operations documentation SHOULD state the active source of truth, known mock/demo boundaries, environment-specific constraints, and any capability intentionally deferred.

When a capability transitions from mock/scaffold to real production behavior, update the corresponding decisions, verification and operational docs in the same change where practical.

## Verification

Reviewers SHOULD be able to answer:

1. What is real?
2. What is simulated?
3. Which environment was verified?
4. Which external systems were actually exercised?
5. Which gates were not run?
6. Would failure be visible, or silently replaced by a fallback?

If those answers are materially ambiguous, the change is not done.
