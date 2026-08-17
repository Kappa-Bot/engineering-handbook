---
id: std-dependency-supply-chain-baseline
kind: standard
status: active
owner: engineering
version: "0.1"
applies_to:
  - repositories-with-third-party-dependencies
  - ci-cd
sources:
  - src-nist-ssdf-11
  - src-openssf-scorecard
  - src-openssf-secure-software-guiding-principles
  - src-github-actions-security
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Dependency and Software Supply-Chain Baseline

## Purpose

Reduce avoidable dependency and CI/CD supply-chain risk without requiring SBOMs, signing, attestations or security-scoring bureaucracy for every small repository.

## 1. Dependencies are engineering decisions

Before adding a meaningful third-party dependency, apply reuse/evaluation proportionally:

- actual fit;
- maintenance/activity;
- security posture/history;
- license/reuse constraints;
- ecosystem maturity;
- transitive complexity;
- lock-in and replacement cost.

Do not add a package for trivial functionality merely to avoid writing a few maintainable lines; likewise, do not reimplement mature security/protocol functionality without a strong reason.

## 2. Reproducible dependency resolution

Repositories SHOULD commit and use the ecosystem's lockfile when lockfiles are a normal supported mechanism.

CI/release SHOULD use frozen/immutable installation where supported so the tested dependency graph is not silently different from the committed one.

Generated/vendor directories SHOULD NOT be committed unless the ecosystem/deployment model deliberately requires it.

## 3. Maintain supported dependencies

Critical dependencies SHOULD remain within supported/security-maintained versions according to risk.

Do not upgrade everything immediately merely because a new version exists. Do not indefinitely ignore known exploitable vulnerabilities in reachable code.

Upgrade decisions SHOULD consider breaking change cost, vulnerability exploitability/reachability and provider/framework support windows.

## 4. Third-party GitHub Actions/workflows

For GitHub Actions, third-party actions SHOULD be pinned to a full-length commit SHA for immutable execution, especially in workflows with secrets, write permissions or deployment authority.

Verify the pinned SHA belongs to the intended upstream source/version.

Workflow `GITHUB_TOKEN` permissions SHOULD be explicitly reduced to the minimum needed for sensitive workflows.

Untrusted pull-request/fork code MUST NOT be given production secrets or privileged deployment credentials.

## 5. Dependency/project security signals

OpenSSF Scorecard MAY be used as one input when evaluating an open-source project.

A Scorecard result MUST NOT be treated as proof that a dependency is safe or unsafe, nor should a universal numeric threshold replace context-specific review.

Combine automated signals with applicability, maintenance, provenance and the security sensitivity of the dependency.

## 6. Artifact provenance, SBOMs and signing

SBOMs, build provenance/attestations, signed releases and artifact verification SHOULD be adopted when distribution model, customer/compliance needs, artifact risk or supply-chain threat justifies them.

They are not universal requirements for every privately deployed web application.

When used, generate them from the real build/release process rather than maintaining decorative files by hand.

## 7. CI/CD is privileged software

Treat workflow code and reusable automation as executable production-adjacent code when it can:

- write repository state;
- access secrets;
- deploy;
- publish artifacts;
- mutate databases/cloud resources.

Review changes to that automation with consequence-appropriate care.

## 8. Secret isolation

Dependencies or third-party workflows SHOULD receive only the credentials they need.

Do not expose broad environment secrets to an entire job merely for one narrow step when scoping is practical.

## 9. Definition of done

A material dependency/supply-chain change is complete when:

- the new dependency/tool has a reason to exist;
- version resolution is reproducible where supported;
- security/license/maintenance risks were considered proportionally;
- privileged CI dependencies are immutable/scoped appropriately;
- no untrusted execution path receives production secrets;
- stronger provenance/SBOM/signing controls were considered when distribution/risk warrants them.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "supply-chain-dependency-fit",
      "type": "decision-question",
      "text": "Does the proposed dependency justify its maintenance, security, licensing, transitive complexity, lock-in, and replacement cost?",
      "source": "std-dependency-supply-chain-baseline",
      "covers": ["compatibility"],
      "activate_when": ["intent:create", "intent:modify"],
      "force": "should",
      "phase": ["planning"],
      "priority": 35
    },
    {
      "id": "supply-chain-actions-pin",
      "type": "constraint",
      "text": "Prefer full-length immutable commit SHAs for third-party GitHub Actions, especially when workflows have secrets, write permissions, or deployment authority.",
      "source": "std-dependency-supply-chain-baseline",
      "covers": ["compatibility"],
      "activate_when": ["surface:ci", "operation:deployment"],
      "force": "should",
      "phase": ["planning", "implementation", "verification"],
      "priority": 70
    },
    {
      "id": "supply-chain-untrusted-no-production-secrets",
      "type": "constraint",
      "text": "Do not give untrusted pull-request or fork execution production secrets or privileged deployment credentials.",
      "source": "std-dependency-supply-chain-baseline",
      "covers": ["credential"],
      "activate_when": ["surface:ci", "risk:credential"],
      "force": "must-not",
      "phase": ["implementation", "verification"],
      "priority": 100
    }
  ]
}
```
