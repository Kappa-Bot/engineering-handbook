---
id: pb-quality-release-review
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - release-reviews
  - ci-cd-changes
  - high-risk-changes
sources:
  - src-nist-ssdf-11
  - src-github-deployment-environments
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Quality and Release Review

Use when a change modifies test strategy, CI, migrations, deployment, production configuration or a business-critical flow.

## 1. State acceptance risks

List the small set of failures that would make the change unacceptable.

## 2. Map evidence

Use `pat-risk-based-verification-matrix`.

For each risk, select the cheapest reliable evidence and required environment.

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

## 6. Run gates

Prefer deterministic local/CI gates first, then expensive remote/native checks only where they add distinct evidence.

## 7. Record limitations

A release note/handoff should include unrun or blocked gates that matter.

“CI green” is never a substitute for that disclosure.
