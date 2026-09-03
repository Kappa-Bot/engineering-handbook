---
id: pb-quality-release-review
kind: playbook
status: active
owner: engineering
version: "0.2"
applies_to:
  - release-reviews
  - ci-cd-changes
  - high-risk-changes
sources:
  - src-nist-ssdf-11
  - src-github-deployment-environments
last_verified: 2026-09-03
review_due: 2027-03-03
---

# Quality and Release Review

Use when a change modifies test strategy, CI, migrations, deployment, production configuration or a business-critical flow.

## 1. State acceptance risks

List the small set of failures that would make the change unacceptable.

## 2. Map evidence and cadence

Use `pat-risk-based-verification-matrix`.

For each risk, select:

- cheapest reliable evidence;
- required environment;
- the narrowest cadence/trigger that still runs before the protected decision;
- any material CI/provider cost introduced by that cadence.

Do not turn every required release check into an every-push check.

## 3. Separate build from deployment

Answer independently:

- did source checks pass?
- was an artifact/build produced?
- was the intended commit deployed?
- did the target environment accept the deployment?
- did post-deploy smoke/health pass?
- were manual/native gates executed?

## 4. Review persistent changes

If schema/data changes:

- identify migrations;
- confirm target;
- verify compatibility assumptions;
- define recovery/forward-fix;
- ensure seed/reset is not production release setup.

## 5. Review environment boundaries

Confirm that Preview/QA/Production secrets/config do not silently inherit from the wrong scope.

Do not print secret values to prove they exist.

## 6. Review CI economics before expanding automation

For every automatic workflow affected by the change, answer:

- what events trigger it (`push`, PR, schedule, manual, release, etc.)?
- can the same effective commit trigger overlapping runs?
- which failure class does each job catch that another job does not?
- what did recent representative runs actually take?
- what is the repository's high-frequency CI latency/cost budget?
- is `cancel-in-progress` or equivalent enabled where superseded work has no value?
- are timeouts explicit?
- can documentation-only or unrelated changes take a near-zero-cost path?
- are database startup, full builds, browser installation, E2E/visual suites or remote checks being charged on every push without distinct value?
- would an explicit milestone/release workflow preserve the evidence with much lower frequency?

If recent runs are available, use observed timings rather than estimates. Compare before/after when the purpose of the change is cost or latency reduction.

Do not preserve expensive CI because “it is safer” without identifying the distinct risk it catches. Safety is evidence coverage, not job count.

## 7. Review test, script and workflow lifecycle

Before adding automation, look for existing assets that can be extended or replaced.

Remove or consolidate when appropriate:

- duplicate tests covering the same failure class;
- tests for removed product paths;
- one-off release/import/repair scripts with no current caller or runbook;
- obsolete fixtures/helpers used only by deleted tests;
- workflows whose trigger or consumer no longer exists;
- historical automation retained only as an archive.

Git history is normally the archive. A repository should not pay maintenance or CI cost to keep completed execution machinery alive without a current consumer.

## 8. Run gates

Prefer deterministic cheap gates first, then scope-dependent local/milestone checks, then expensive remote/native checks only where they add distinct evidence.

A healthy decomposition often looks like:

```text
push/PR hot path
  → small source-quality gate

material affected scope
  → build / DB / integration / browser / visual as required

explicit release
  → remote environment / migration / deploy / smoke / rollback evidence
```

The exact commands and budgets remain repository-local.

## 9. Record limitations

A release note/handoff should include unrun or blocked gates that matter.

“CI green” is never a substitute for that disclosure.
