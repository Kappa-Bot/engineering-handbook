---
id: pat-release-provenance-environment-gates
kind: pattern
status: active
owner: engineering
version: "0.5"
applies_to:
  - ci-cd
  - deployments
  - production-releases
sources:
  - src-github-deployment-environments
  - src-github-actions-security
  - src-nist-ssdf-11
  - src-rfc-9110
  - src-rfc-9111
  - src-kubernetes-deployment-rollout-status
last_verified: 2026-11-21
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

When reviewing an existing release, compare the approved commit or build identifier with evidence from the intended deployment. For a Preview or Production alias, verify which deployment it resolves to. Record an identity mismatch as a failed check and missing version evidence as unverified. Changing an alias or promoting a build requires separate authorization.

When a captured version receipt may have come from a cache, keep the approved immutable commit/build, resolved deployment target and exact received response separate. Record the URL or alias, observation time and relevant `Cache-Control`, `Age` and platform cache metadata when available. A missing `Age` header does not establish origin contact, and a current `no-store` policy does not resolve earlier cache provenance. Keep a mismatched observed response as a failed response check. Mark current deployment identity `UNVERIFIED` when cache ambiguity or missing independent target evidence prevents attribution. Keep a confirmed target identity mismatch failed. See `src-rfc-9111` §§4.2.3, 5.1 and 5.2.

When a release check needs exact current bytes from a version endpoint and
the client makes a conditional GET, record the network response and the body
the client used. A `304 (Not Modified)` carries no content. A cache can update
the matching stored response's headers and reuse its body, so the application
can receive a `200` with previously stored bytes. A weak `ETag` can identify
equivalent representations whose bytes differ. Compare the bytes used with
independent evidence for the current representation at the intended target.
If that evidence is missing, report exact byte equality as unverified. Assess
the claimed build identity separately. See `src-rfc-9110` §§8.8.1, 13.1.2
and 15.4.5 and `src-rfc-9111` §4.3.4.

When a release gate claims that every serving target in a rollout is on one
revision, record the intended traffic scope, observation window and available
serving membership and version evidence. Attribute responding versions to
that scope. Repeated responses from one target cover only that target.
Report a confirmed unexpected revision in scope as failed and incomplete
membership or revision evidence as unverified. Evaluate an intentionally
mixed rollout against its declared cohort. Record controller completion and
observed runtime responses separately when both are available. See
`src-kubernetes-deployment-rollout-status` for an example of controller
completion evidence.

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

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "release-immutable-identity",
      "type": "decision-question",
      "text": "Which immutable commit or build identity is being promoted, to which environment, and how will the target identity be verified before environment-changing work?",
      "source": "pat-release-provenance-environment-gates",
      "covers": ["compatibility", "availability"],
      "activate_when": ["operation:deployment", "delivery:production"],
      "phase": ["planning", "implementation"],
      "priority": 96
    },
    {
      "id": "release-identity-target-verification",
      "type": "verification",
      "text": "Verify the expected immutable source or build identity, target environment, deployment result, and applicable post-deploy health or smoke evidence as distinct states.",
      "source": "pat-release-provenance-environment-gates",
      "covers": ["compatibility", "availability"],
      "activate_when": ["operation:deployment", "delivery:production"],
      "phase": ["verification"],
      "priority": 100
    },
    {
      "id": "observed-release-provenance",
      "type": "verification",
      "text": "Compare the expected commit or build identifier with the version observed on the intended deployment. Resolve any Preview or Production alias to its actual target. Report mismatched identity as failed and missing evidence as unverified. Record build and smoke results separately.",
      "source": "pat-release-provenance-environment-gates",
      "covers": ["release-provenance"],
      "activate_when": ["risk:release-provenance"],
      "phase": ["planning", "implementation", "verification"],
      "priority": 96
    },
    {
      "id": "release-version-cache-evidence",
      "type": "verification",
      "force": "should",
      "text": "Compare the approved immutable ID, resolved Preview or Production target and exact version response received. Record observation time, relevant Cache-Control and Age headers, and available platform cache metadata. Keep an observed response mismatch as a failed response check and a confirmed deployment mismatch as failed. Mark deployment identity UNVERIFIED when attribution or target evidence is missing. Missing Age or a current no-store policy cannot settle earlier cache provenance.",
      "source": "pat-release-provenance-environment-gates",
      "covers": [
        "release-version-cache-attribution"
      ],
      "activate_when": [
        "archetype:release-version-cache-review"
      ],
      "phase": [
        "planning",
        "verification"
      ],
      "priority": 95
    },
    {
      "id": "release-no-production-seed-reset",
      "type": "constraint",
      "text": "Do not run local or demo reset/seed behavior against Production as ordinary release setup.",
      "source": "pat-release-provenance-environment-gates",
      "covers": ["data-loss"],
      "activate_when": ["operation:deployment", "delivery:production"],
      "force": "must-not",
      "phase": ["implementation", "verification"],
      "priority": 100
    }
  ]
}
```
