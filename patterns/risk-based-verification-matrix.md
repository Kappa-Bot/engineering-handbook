---
id: pat-risk-based-verification-matrix
kind: pattern
status: active
owner: engineering
version: "0.7"
applies_to:
  - verification-plans
  - test-strategies
sources:
  - src-nist-ssdf-11
  - src-owasp-asvs-500
  - src-ecma262-string-code-units
  - src-sqlite-last-insert-rowid
  - src-microsoft-replacefilew
  - src-microsoft-dotnet-task-whenall
  - src-microsoft-csharp-async-exception-observation
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
| grounding of in-product AI answers | approved-source claims and missing-source abstention | local fixture / separately authorized model or hosted environment | affected answer or source behavior |

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

For an in-product AI answer grounding review, identify the approved source revision and record which material claims the answer may make. Check that any citation actually supports those claims and that missing or unavailable evidence produces an explicit gap or abstention. Use small local fixtures to test source and fallback contracts. Use observed outputs from authorized executions to assess model behavior or hosted delivery. Record the environment and result for each layer. Mark unobserved checks NOT RUN.

When an existing citation contract includes source offsets, verify the
range on the approved source revision. Record the offset unit, source
encoding and whether the end is inclusive. Include text with repeated
excerpts and multibyte characters before the cited passage. Confirm the
intended occurrence, quoted content and material claim. A matching
excerpt can occur at several positions, and UTF-8 byte offsets can differ
from JavaScript string indices. See `src-ecma262-string-code-units` §6.1.4 for string indexing.

When an existing SQLite write uses a last-insert rowid to report its
outcome, compare the current statement's result with committed row readback.
Seed an earlier successful insert distinct from the row that conflicts. A
skipped insert can leave the earlier rowid in the connection. A successful
insert can leave its rowid there even if it is rolled back. Exercise these
outcomes when the operation permits them. Read from a separate connection
to confirm the intended committed row. See `src-sqlite-last-insert-rowid`.

When an existing Windows publisher replaces a local file while readers
can stay open, verify the operation under the supported sharing modes.
Compare a read on a handle opened before replacement with a new open of
the published path. If the operation can be refused while a reader holds
the file, inspect the retained destination and staged bytes. Exercise the
approved recovery after the handle closes. Use separate evidence for
access-control attributes and crash recovery when those are claimed. See
`src-microsoft-replacefilew`.

When an existing .NET flow uses `Task.WhenAll` and reports member failures,
exercise two controlled tasks that fault independently. Observe the joined
task while one member is still pending. At completion, compare the exception
thrown by `await` with the terminal group's `Task.Exception.InnerExceptions`.
Include cancellation when the flow distinguishes it. Observe any claimed
external resource effects at their actual boundaries. See
`src-microsoft-dotnet-task-whenall` and `src-microsoft-csharp-async-exception-observation`.

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
    },
    {
      "id": "product-ai-grounding-evidence",
      "type": "verification",
      "force": "should",
      "text": "For in-product AI answer grounding, record the expected material claim and approved source revision. Check that actual citations support the claim and that missing or unavailable evidence leads to an explicit gap or abstention. Record fixture/contract checks separately from observed model behavior and hosted evidence. Mark unobserved layers NOT RUN. Follow existing authority for inference and provider access.",
      "source": "pat-risk-based-verification-matrix",
      "covers": [
        "product-ai-grounding"
      ],
      "activate_when": [
        "archetype:product-ai-grounding-review"
      ],
      "phase": [
        "planning",
        "verification"
      ],
      "priority": 90
    }
  ]
}
```
