---
id: pat-release-provenance-environment-gates
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - ci-cd
  - deployments
  - production-releases
sources:
  - src-github-deployment-environments
  - src-github-actions-security
  - src-nist-ssdf-11
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Release Provenance and Environment Gates

## Intent

Make it possible to answer exactly what was deployed, where, with which protected context and what happened afterwards.

## Release identity

Prefer deployment from an immutable commit/build identity.

A higher-risk promotion SHOULD verify expected source identity before performing environment-changing work.

Useful provenance may include:

- commit SHA;
- build/artifact identifier;
- workflow/run ID;
- migration version;
- environment;
- deployment URL/version endpoint.

Do not rely on a branch name alone when concurrent changes can move it.

## Environment-scoped credentials

Production credentials SHOULD be available only to jobs that actually target Production.

Where the CI platform supports environment protection, use it when it materially reduces accidental or unauthorized promotion.

Prefer short-lived/OIDC-style cloud authentication over long-lived deployment secrets when supported and justified.

## Gates

Possible gates include:

- required tests;
- exact expected source identity;
- environment approval/protection;
- migration/schema verification;
- deployment completion;
- signed/authenticated smoke;
- post-deploy health/synthetic checks.

Do not enable every gate by default. Use consequence and frequency to justify friction.

## Concurrency

For environments where overlapping deployments can corrupt state or create ambiguity, serialize or otherwise control concurrent promotion.

## Production data safety

Release workflows MUST NOT casually run local/demo reset or seed behavior against Production.

If production bootstrap data is genuinely required, model it as an explicit production migration/operation with its own safeguards and auditability.

## Handoff

A release handoff SHOULD distinguish:

```text
build verified
deployment attempted
deployment succeeded
post-deploy smoke passed
production-native/manual checks passed
```

Never collapse those states into one “green”.
