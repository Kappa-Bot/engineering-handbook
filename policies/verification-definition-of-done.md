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

## Core rule

**Evidence before claims.**

An agent or engineer MUST NOT state or imply that a gate passed unless that gate was actually executed and its result observed for the relevant change.

Examples:

- `tests pass` requires a completed relevant test run;
- `build passes` requires the actual build command to succeed;
- `lint clean` requires the linter result;
- `CI green` requires current CI status;
- `bug fixed` requires verification of the original failure mode, not merely code inspection.

## Repository-defined gates

The consumer repository owns its exact commands and test matrix. The handbook defines the truthfulness model, not one universal command set.

A useful conceptual hierarchy is:

```text
G0 — workspace
correct repo / expected base / state understood

G1 — fast local
format / lint / typecheck / unit as applicable

G2 — scope-dependent
integration / E2E / accessibility / PWA / security / performance as applicable

G3 — PR
required CI / review / repository policy checks

G4 — release
release/deployment/browser/device/production evidence as applicable
```

Not every repository has every gate. Do not invent a gate that the project does not actually need.

## Definition of Done

A task is done when all of the following that apply are true:

- requested outcome and acceptance criteria are satisfied;
- scope did not silently expand;
- relevant code/docs/config are internally consistent;
- repository-defined required verification has been run successfully;
- scope-dependent checks have either run or are explicitly declared not run with a reason;
- no known critical regression is being hidden by a narrow test selection;
- workspace/handoff state is accounted for;
- documentation is updated when the real operating contract changed;
- remaining risks/dependencies are explicit.

## Unrun checks

A check that was not executed MUST be reported as **not run**, not as assumed passing.

Good:

> `pnpm test` passed. Playwright was not run because this change is documentation-only and the repo does not require E2E for docs changes.

Bad:

> All checks pass.

when only one check was run.

## Scope-sensitive verification

Verification SHOULD target the risk of the change.

- Documentation-only: links/metadata/catalog consistency may be enough.
- Pure refactor: existing behavior tests + type/build checks may be important.
- Authentication/security: relevant negative tests and security review may be mandatory later under a security standard.
- UI behavior: build/unit alone may be insufficient; browser evidence may be relevant.

The exact matrix belongs to repository/standard-level guidance when introduced.

## Handoff report

A concise handoff SHOULD include:

- outcome;
- changed files/areas;
- commands/checks actually run and results;
- checks not run and reasons;
- known risks or external dependencies;
- Git/workspace state if material.

Do not use confidence, agent self-report, or code appearance as substitutes for verification evidence.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "verification-evidence-before-claims",
      "type": "constraint",
      "text": "Do not claim a gate passed unless it was executed and its result observed for the relevant change.",
      "source": "pol-verification-definition-of-done",
      "covers": ["availability"],
      "activate_when": ["intent:modify", "intent:release", "operation:deployment"],
      "force": "must-not",
      "phase": ["verification"],
      "priority": 100
    },
    {
      "id": "verification-unrun-status",
      "type": "verification",
      "text": "Record applicable checks as passed, failed, not run with a reason, or not applicable rather than assuming success.",
      "source": "pol-verification-definition-of-done",
      "covers": ["availability"],
      "activate_when": ["intent:modify", "intent:release"],
      "force": "must",
      "phase": ["verification"],
      "priority": 90
    }
  ]
}
```
