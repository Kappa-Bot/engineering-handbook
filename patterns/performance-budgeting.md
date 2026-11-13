---
id: pat-performance-budgeting
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - performance-sensitive-products
sources:
  - src-webdev-core-web-vitals-thresholds
  - src-chrome-devtools-rendering-performance
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Performance Budgeting by User Journey

## Intent

Prevent meaningful performance regressions without inventing one universal performance budget for every product and surface.

## Start with user consequence

Identify the journeys/surfaces where latency, rendering, interaction or resource cost materially changes user success.

Examples:

- public landing/lead conversion;
- login/check-in flow;
- operational workspace navigation;
- large report/document render;
- background processing/import;
- API integration latency.

## Measure before optimizing

Capture a reproducible baseline before large optimization work when feasible.

Record enough methodology to compare later:

- environment/build;
- device/browser/network class where relevant;
- data size;
- route/journey;
- warm/cold state;
- metric/tool.

## Web surfaces

Core Web Vitals are useful field/user-experience indicators for public/user-facing web surfaces. Current Google guidance uses LCP, INP and CLS with user-experience thresholds, evaluated at the 75th percentile for field classification.

Do not turn those metrics into the only performance definition for an application. An operational workflow may also care about API latency, initial JS cost, data-table responsiveness or task completion time.

For motion, measure the user-visible interval and next usable action, including rapid repeated input or interruption where relevant. Pair equivalent builds and workloads with the same browser, compiler/configuration, viewport, cache, throttling and timing window. Repeat noisy comparisons in interleaved order where practical. Record interval distributions or missed frames, scripting/long tasks, layout and paint/compositing as separate signals. Frame callback intervals are a useful lab proxy and do not alone identify presented or dropped frames. Event Timing in a controlled run is lab evidence. Field INP needs representative real interactions and field aggregation.

Prefer changes such as a transform on a contained progress fill when they preserve geometry and avoid repeated layout. Measure the result. Transform, clipping, blur and composited snapshots still have paint, memory or compositing costs. Report the metrics that improved, stayed similar or moved adversely, with sample count and dispersion. Keep outliers and distinct per-run or aggregate outcomes visible. Treat an independent rerun as a second series with its own conditions rather than replacing an inconvenient sample. See `src-chrome-devtools-rendering-performance`.

## Budgets

A repository MAY define numeric budgets when repeated regression risk justifies them.

Budgets SHOULD be tied to a surface/journey and measurement method rather than copied globally.

Examples:

- “critical public pages should remain within target CWV under field/lab proxy conditions”;
- “scanner feedback must remain within an interaction threshold on target devices”;
- “quote generation at representative data size must stay under an agreed latency”.

## Optimize the constraint, not the score

Do not degrade accessibility, correctness, maintainability or product identity merely to improve a synthetic score.

Large visual/3D/motion experiences MAY intentionally spend more resources when the business/design value justifies it; they still need deliberate loading/interactivity behavior.

## Regression gate

Automate a performance gate only when:

- measurement is sufficiently stable;
- the budget maps to user/product impact;
- false positives are manageable;
- the team can act when it fails.

Otherwise retain repeatable measurement and review rather than a flaky hard gate.

## Paused implementation evidence

The dated [Platform Core performance/security handoff](../references/platform-core-performance-security-handoff-2026-10-10.md)
is a **non-normative, unverified** implementation example of bounded reads,
demand-loaded sections and targeted refresh. It is not a measured improvement
claim or a universal performance budget.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "performance-user-journey-constraint",
      "type": "decision-question",
      "text": "Which user journey or operational surface is performance-sensitive, what representative measurement describes it, and what regression would materially affect user success?",
      "source": "pat-performance-budgeting",
      "covers": ["performance"],
      "activate_when": ["risk:performance"],
      "phase": ["planning"],
      "priority": 100
    },
    {
      "id": "performance-measure-before-optimization",
      "type": "verification",
      "text": "Compare matched builds, journeys, devices, cache and timing windows. For motion measure input latency, frame intervals and layout/paint separately. Repeat noisy results, retain outliers and partial regressions, and distinguish lab timing from field LCP/INP/CLS.",
      "source": "pat-performance-budgeting",
      "covers": ["performance"],
      "activate_when": ["risk:performance"],
      "phase": ["verification"],
      "priority": 94
    },
    {
      "id": "performance-no-universal-budget",
      "type": "constraint",
      "text": "Do not copy one global performance threshold across unrelated products; define numeric budgets only when repeated regression risk and a stable measurement justify them.",
      "source": "pat-performance-budgeting",
      "covers": ["performance"],
      "activate_when": ["risk:performance"],
      "phase": ["planning", "implementation"],
      "priority": 72
    }
  ]
}
```
