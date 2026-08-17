---
id: std-testing-release-quality-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - application-repositories
  - services
  - releaseable-products
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-github-deployment-environments
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Testing and Release Quality Baseline

## Purpose

Define the minimum evidence discipline for code changes, CI and releases without prescribing one test framework, one CI provider or one universal pipeline.

The objective is to match evidence to risk and to keep build/test/deployment claims distinct.

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

## 4. CI evidence is scoped evidence

A green CI result means only that the configured jobs completed successfully for that commit/run.

CI MUST NOT be described as proving:

- remote deployment succeeded, unless deployment was part of the run;
- production configuration is correct, unless verified;
- native-device behavior was tested, unless it was;
- visual correctness, unless rendered evidence was inspected/validated;
- external integrations are live, unless exercised;
- security beyond the controls actually checked.

Apply `pol-truthful-engineering`.

## 5. Release identity and target are explicit

A release/deployment flow SHOULD be able to identify:

- exact source commit/build;
- target environment;
- configuration/secrets scope;
- migrations/data changes;
- deployment result;
- smoke/health evidence;
- rollback/forward-fix path where consequence justifies it.

For higher-risk production promotion, expected commit/SHA or equivalent immutable build identity SHOULD be checked rather than deploying an ambiguous moving branch state.

## 6. Environment progression

Local, Preview, QA/Staging and Production MAY use different verification depths.

Production promotion SHOULD add evidence for risks that cannot be proven locally, such as:

- remote environment configuration;
- real provider integration;
- migration state;
- environment-specific authorization/secrets;
- deployment health;
- production-safe smoke.

The exact environment names are repo-local.

## 7. Database/migration release safety

When a release changes persistent schema/data:

- migration order and target MUST be explicit;
- compatibility with currently deployed code SHOULD be considered;
- destructive migrations need a deliberate recovery/forward-fix plan;
- Production seeds/resets MUST NOT run as ordinary release setup;
- schema verification SHOULD occur after applying migrations when the platform allows it.

## 8. Physical/native checks

When acceptance depends on real hardware/browser/PWA/camera/keyboard/printing/device behavior, automation/emulation does not automatically replace physical validation.

Record such checks as `passed`, `failed` or `not run/not performed`.

## 9. Release Definition of Done

A release-relevant change is complete when:

- applicable automated layers pass;
- target/build identity is known;
- migrations/config changes are accounted for;
- critical negative paths are covered;
- remote/native/visual gates are either executed or explicitly unrun;
- no evidence claim exceeds what the gates actually demonstrated.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "testing-risk-based-evidence",
      "type": "decision-question",
      "text": "What is the cheapest reliable evidence that catches each material failure class introduced by this change?",
      "source": "std-testing-release-quality-baseline",
      "covers": ["availability", "compatibility"],
      "activate_when": ["intent:modify", "intent:release"],
      "force": "must",
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
    }
  ]
}
```
