---
id: pat-risk-based-verification-matrix
kind: pattern
status: active
owner: engineering
version: "0.2"
applies_to:
  - verification-plans
  - test-strategies
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
last_verified: 2026-09-03
review_due: 2027-03-03
---

# Risk-Based Verification Matrix

## Intent

Choose verification by failure consequence instead of mechanically running every possible test category, and choose its cadence so expensive evidence is not charged more often than the risk requires.

## Pattern

For a material change, map:

```text
risk / invariant
  → failure mode
  → cheapest reliable evidence
  → environment required
  → cadence / trigger
  → marginal cost
  → acceptance status
```

Example:

| Risk | Evidence | Environment | Cadence / trigger |
|---|---|---|---|
| pure pricing/status rule | unit/domain tests | local/CI | every affected change |
| authorization regression | integration + negative matrix | local/CI with real policy boundary | affected security/domain change |
| migration correctness | migration apply + schema/data checks | disposable DB / QA | schema/data change + release |
| critical browser journey | E2E | local/Preview | affected milestone / release |
| visual composition | rendered inspection/evidence | browser | material UI change |
| camera/PWA install/keyboard | physical device when required | device | acceptance/release when risk changes |
| deployment/config | remote smoke/inspect | QA/Production | explicit deployment |
| live external provider | contract/integration/synthetic check | environment with real provider | integration/release trigger |

## Principles

- Do not use E2E when a pure test catches the same risk faster and more deterministically.
- Do not use unit tests to claim a remote integration works.
- Negative cases are first-class for authorization, integrity and failure recovery.
- Evidence matrices SHOULD remain small; include only risks that can change acceptance.
- If a risk has no feasible automated gate, make the manual/native check explicit rather than hiding the gap.
- Do not equate “required before release” with “required on every push.” Put expensive evidence at the narrowest cadence that still precedes the decision it protects.
- When an automatic workflow already proves the same failure class, a second PR/push/release execution needs a distinct reason, not merely a different trigger name.
- For metered CI, record actual wall-clock/runtime evidence after materially changing the matrix. An unmeasured automation optimization is not yet proven.
- Prefer one cheap high-frequency gate plus scope/release-specific deeper gates over a universal pipeline that starts databases, browsers, builds and remote checks for unrelated changes.

## Status vocabulary

Prefer:

- passed;
- failed;
- not run;
- blocked;
- not applicable.

Avoid vague states such as “looks okay” for acceptance evidence.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "verification-map-risk-to-cheapest-evidence",
      "type": "pattern",
      "text": "Map each material risk or invariant to its failure mode, cheapest reliable evidence, required environment, and explicit acceptance status.",
      "source": "pat-risk-based-verification-matrix",
      "covers": ["availability", "compatibility"],
      "activate_when": ["intent:modify", "intent:release"],
      "phase": ["planning", "verification"],
      "priority": 72
    },
    {
      "id": "verification-no-unit-proof-for-remote",
      "type": "anti-pattern",
      "text": "Do not use unit tests as evidence that a remote integration, deployment, or physical-device behavior works.",
      "source": "pat-risk-based-verification-matrix",
      "covers": ["availability"],
      "activate_when": ["operation:integration", "operation:deployment", "capability:pwa"],
      "phase": ["verification"],
      "priority": 86
    }
  ]
}
```
