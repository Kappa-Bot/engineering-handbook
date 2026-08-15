---
id: pat-risk-based-verification-matrix
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - verification-plans
  - test-strategies
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Risk-Based Verification Matrix

## Intent

Choose verification by failure consequence instead of mechanically running every possible test category.

## Pattern

For a material change, map:

```text
risk / invariant
  → failure mode
  → cheapest reliable evidence
  → environment required
  → acceptance status
```

Example:

| Risk | Evidence | Environment |
|---|---|---|
| pure pricing/status rule | unit/domain tests | local/CI |
| authorization regression | integration + negative matrix | local/CI with real policy boundary |
| migration correctness | migration apply + schema/data checks | disposable DB / QA |
| critical browser journey | E2E | local/Preview |
| visual composition | rendered inspection/evidence | browser |
| camera/PWA install/keyboard | physical device when required | device |
| deployment/config | remote smoke/inspect | QA/Production |
| live external provider | contract/integration/synthetic check | environment with real provider |

## Principles

- Do not use E2E when a pure test catches the same risk faster and more deterministically.
- Do not use unit tests to claim a remote integration works.
- Negative cases are first-class for authorization, integrity and failure recovery.
- Evidence matrices SHOULD remain small; include only risks that can change acceptance.
- If a risk has no feasible automated gate, make the manual/native check explicit rather than hiding the gap.

## Status vocabulary

Prefer:

- passed;
- failed;
- not run;
- blocked;
- not applicable.

Avoid vague states such as “looks okay” for acceptance evidence.
