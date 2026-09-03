---
id: std-testing-release-quality-baseline
kind: standard
status: active
owner: engineering
version: "0.2"
applies_to:
  - application-repositories
  - services
  - releaseable-products
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-github-deployment-environments
last_verified: 2026-09-03
review_due: 2027-03-03
---

# Testing and Release Quality Baseline

## Purpose

Define the minimum evidence discipline for code changes, CI and releases without prescribing one test framework, one CI provider or one universal pipeline.

The objective is to match evidence to risk, keep build/test/deployment claims distinct, and prevent verification machinery from becoming a disproportionate operational cost.

## 1. Test the failure class, not the tool

Use the cheapest layer that can reliably catch the relevant defect.

Typical layers:

- pure/domain/unit tests for deterministic logic and invariants;
- component/module tests for local integration and interaction;
- database/policy tests for schema, constraints, authorization and migrations;
- integration tests for boundary contracts;
- end-to-end tests for critical user/business journeys;
- accessibility/visual/responsive tests where UI risk exists;
- synthetic/production smoke checks for deployed behavior.

No repository is required to implement every layer. The chosen set MUST reflect the actual failure risks.

## 2. Critical invariants require automated regression where practical

Rules involving money, permissions, tenant isolation, history, scheduling conflicts, entitlements, destructive actions, migrations or externally retried mutations SHOULD have automated regression coverage at the authoritative boundary.

Happy-path-only coverage is insufficient for permission/integrity-sensitive behavior.

## 3. Clean and reproducible setup

Automated verification SHOULD start from a known state.

Where setup/seed/migrations are part of the product:

- setup SHOULD be repeatable/idempotent where practical;
- test data MUST be non-production;
- reset/seed commands MUST be prevented from targeting Production accidentally;
- lockfiles/frozen dependency installation SHOULD be used where the ecosystem supports them.

## 4. CI is a metered hot path

Automatic CI consumes wall-clock time, runner quota, provider capacity and developer attention. Treat that cost as part of the engineering design, not as free infrastructure.

Repositories SHOULD define an explicit latency/cost expectation for the high-frequency push/PR path when CI usage is metered, quota-limited or operationally significant. The exact budget is repository-local; the Handbook does not impose one universal duration.

Before adding or expanding an automatic job, establish:

- the material failure class it catches;
- why a cheaper existing layer cannot catch that failure reliably;
- how often the trigger is expected to fire;
- expected or measured wall-clock/runtime cost;
- whether the same commit is already verified by another trigger or environment;
- whether the evidence belongs on every push, only on affected changes, or only at release time.

Do not run expensive layers on every push merely because they exist. Full builds, local database startup, browser-engine installation, broad E2E/visual matrices, remote integration checks, deterministic seeding and deployment verification belong on the automatic hot path only when they provide distinct evidence that is worth their frequency and cost.

Prefer, where applicable:

- one small automatic source-quality job over several setup-heavy jobs;
- change/path classification when a gate is relevant only to a subset of files;
- a near-zero-cost documentation-only path;
- `cancel-in-progress` or equivalent for superseded runs;
- explicit job timeouts;
- safe dependency/tool caching when it materially reduces cost without hiding freshness problems;
- explicit/manual release workflows for expensive environment-specific verification.

Avoid paying for both pull-request and push workflows over the same effective commit unless those runs prove genuinely different acceptance boundaries.

After changing CI, inspect real run timing rather than assuming the optimization worked. A workflow that is logically smaller but still violates the repository's budget remains an unresolved operational defect.

## 5. Verification cadence is part of evidence design

The cheapest reliable evidence and the correct cadence are separate decisions.

A repository MAY use different gates at different frequencies, for example:

```text
high-frequency push/PR
  → hygiene / lint / type/domain tests

scope-dependent local or milestone verification
  → build / database / integration / browser / visual

explicit QA/Production release
  → migration / remote config / deployment / smoke / rollback evidence
```

This is not permission to skip required evidence. It is a requirement to run expensive evidence at the narrowest cadence that still protects the risk before acceptance or release.

A platform build performed by the deployment provider does not automatically require a second full CI build on every push; a second build is justified only when it catches a distinct failure earlier or more reliably.

## 6. Test portfolios have a lifecycle

Test count is not a quality objective by itself. Permanent tests SHOULD remain mapped to current product risks and current consumers.

Delete, merge or replace tests when:

- stronger lower-level coverage now proves the same invariant;
- a product path or consumer no longer exists;
- the test preserves implementation history rather than current behavior;
- several cases duplicate the same failure class without meaningful additional coverage;
- setup cost is disproportionate to the distinct risk being protected.

Repositories MAY define a permanent test budget or layer allocation when growth has become a recurring cost problem. A budget MUST NOT be evaded by moving functional assertions into custom runners or scripts.

## 7. Scripts, workflows and verification helpers need current consumers

A script, workflow, fixture generator or verification helper SHOULD have an identifiable current caller or operator procedure.

One-off migration/import/repair helpers SHOULD be removed after their purpose is complete unless a current runbook or recurring operation still depends on them. Do not keep automation merely because it once helped a release.

When a helper is retained for recovery, the recovery path and safety boundary SHOULD remain discoverable from current documentation.

## 8. CI evidence is scoped evidence

A green CI result means only that the configured jobs completed successfully for that commit/run.

CI MUST NOT be described as proving:

- remote deployment succeeded, unless deployment was part of the run;
- production configuration is correct, unless verified;
- native-device behavior was tested, unless it was;
- visual correctness, unless rendered evidence was inspected/validated;
- external integrations are live, unless exercised;
- security beyond the controls actually checked.

Apply `pol-truthful-engineering`.

## 9. Release identity and target are explicit

A release/deployment flow SHOULD be able to identify:

- exact source commit/build;
- target environment;
- configuration/secrets scope;
- migrations/data changes;
- deployment result;
- smoke/health evidence;
- rollback/forward-fix path where consequence justifies it.

For higher-risk production promotion, expected commit/SHA or equivalent immutable build identity SHOULD be checked rather than deploying an ambiguous moving branch state.

A repository MAY require a cheap successful CI record for the exact release SHA while keeping expensive release evidence outside that automatic workflow. Documentation-only commits SHOULD not be forced through unrelated runtime/browser/database work solely to obtain an exact-SHA quality marker.

## 10. Environment progression

Local, Preview, QA/Staging and Production MAY use different verification depths.

Production promotion SHOULD add evidence for risks that cannot be proven locally, such as:

- remote environment configuration;
- real provider integration;
- migration state;
- environment-specific authorization/secrets;
- deployment health;
- production-safe smoke.

The exact environment names are repo-local.

## 11. Database/migration release safety

When a release changes persistent schema/data:

- migration order and target MUST be explicit;
- compatibility with currently deployed code SHOULD be considered;
- destructive migrations need a deliberate recovery/forward-fix plan;
- Production seeds/resets MUST NOT run as ordinary release setup;
- schema verification SHOULD occur after applying migrations when the platform allows it.

Database startup and exhaustive DB verification are often expensive. Their cost does not justify omitting them when schema/data risk changes; instead, place them in the scope-dependent or release gate that protects the change without charging unrelated pushes.

## 12. Physical/native checks

When acceptance depends on real hardware/browser/PWA/camera/keyboard/printing/device behavior, automation/emulation does not automatically replace physical validation.

Record such checks as `passed`, `failed` or `not run/not performed`.

## 13. Release Definition of Done

A release-relevant change is complete when:

- applicable automated layers pass;
- target/build identity is known;
- migrations/config changes are accounted for;
- critical negative paths are covered;
- remote/native/visual gates are either executed or explicitly unrun;
- no evidence claim exceeds what the gates actually demonstrated;
- verification cadence did not silently omit a required risk boundary merely to reduce CI cost.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "testing-risk-based-evidence",
      "type": "decision-question",
      "text": "What is the cheapest reliable evidence that catches each material failure class introduced by this change?",
      "source": "std-testing-release-quality-baseline",
      "covers": [],
      "activate_when": ["intent:modify", "intent:release"],
      "phase": ["planning"],
      "priority": 55
    },
    {
      "id": "testing-release-identity",
      "type": "verification",
      "text": "Verify the exact source/build identity and target environment for a production release or deployment.",
      "source": "std-testing-release-quality-baseline",
      "covers": ["availability", "compatibility"],
      "activate_when": ["operation:deployment", "delivery:production"],
      "force": "should",
      "phase": ["verification"],
      "priority": 100
    },
    {
      "id": "testing-migration-release-safety",
      "type": "verification",
      "text": "Verify migration order and target, schema/data result, and relevant compatibility or recovery behavior for persistent-state releases.",
      "source": "std-testing-release-quality-baseline",
      "covers": ["data-loss", "compatibility"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "should",
      "phase": ["verification"],
      "priority": 96
    },
    {
      "id": "testing-ci-evidence-scope",
      "type": "constraint",
      "text": "A green CI result proves only the configured jobs that actually ran for that commit or run.",
      "source": "std-testing-release-quality-baseline",
      "covers": ["availability"],
      "activate_when": ["surface:ci", "operation:deployment"],
      "force": "must",
      "phase": ["verification"],
      "priority": 88
    },
    {
      "id": "testing-migration-compatibility-plan",
      "type": "decision-question",
      "text": "What compatibility with currently deployed code and recovery or forward-fix behavior must this migration preserve?",
      "source": "std-testing-release-quality-baseline",
      "covers": ["compatibility"],
      "activate_when": ["operation:migration", "state:migration"],
      "force": "should",
      "phase": ["planning"],
      "priority": 96
    }
  ]
}
```
