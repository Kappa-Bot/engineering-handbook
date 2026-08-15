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
