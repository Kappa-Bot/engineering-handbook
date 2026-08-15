---
id: pol-verification-definition-of-done
kind: policy
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Verification and Definition of Done

## Evidence before claims

A completion claim MUST be backed by evidence appropriate to the change.

- Never claim that a test, build, lint, typecheck, security check, deployment, review, or other gate passed unless it was actually executed and its result was observed.
- If a relevant check cannot be run, state that explicitly and explain the remaining uncertainty.
- Prefer direct verification of user-visible or runtime behavior when the risk warrants it.

## Definition of Done

Unless a repository defines stricter local criteria, work is done when all applicable items below are true:

- requested scope is implemented and acceptance criteria are satisfied;
- no known unrelated changes were introduced;
- relevant tests or checks were executed, or omissions are explicitly reported;
- failures introduced by the change are resolved;
- documentation and configuration affected by the change are updated;
- temporary artifacts are removed;
- Git/workspace state is suitable for handoff;
- remaining risks, limitations, migrations, or follow-up work are stated rather than hidden.

## Proportional verification

Verification SHOULD be proportional to risk. A documentation typo does not require the same gates as an authentication change, but “small change” is not a reason to fabricate or skip a relevant check without disclosure.

## Handoff

A handoff SHOULD identify:

- what changed;
- what was verified;
- what was not verified;
- any remaining repository or operational state the next engineer must know.
