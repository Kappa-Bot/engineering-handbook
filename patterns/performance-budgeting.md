---
id: pat-performance-budgeting
kind: pattern
status: active
owner: engineering
version: "0.15"
applies_to:
  - performance-sensitive-products
sources:
  - src-webdev-core-web-vitals-thresholds
  - src-chrome-devtools-rendering-performance
  - src-w3c-high-resolution-time
  - src-node-perf-hooks-time-origin
  - src-w3c-resource-timing
  - src-w3c-performance-timeline-observer
  - src-w3c-timing-entry-names-registry
  - src-w3c-intersection-observer-geometry
  - src-w3c-resize-observer-layout-box
  - src-w3c-cssom-view
  - src-w3c-wasm-web-api-streaming
  - src-whatwg-html-responsive-image-preload
  - src-w3c-largest-contentful-paint-20261117
  - src-whatwg-html-page-transition-events
  - src-modern-web-guidance
  - src-llvm-auto-vectorization
  - src-gcc-x86-cpu-dispatch
  - src-intel-sdm-packed-float-minimum
  - src-prometheus-histogram-quantile-aggregation
  - src-nist-engineering-right-censoring
last_verified: 2026-11-22
review_due: 2027-02-19
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

### Performance review: locate the actual bottleneck

A review can be read-only; a request to measure or diagnose does not authorize deployment, changing production data, increasing a provider tier or running an unapproved load test.

1. Pick one user or operational **journey** with a measurable symptom and representative workload. Separate cold/warm, preview/production and small/large datasets instead of averaging incompatible runs.
2. Break its duration/resource use across DNS/network/transfer, edge/server, authentication, database/query fan-out, serialization, hydration/render, interactions and any background jobs that actually participate. A slow dashboard may be waiting for SQL, not the React tree.
3. Inspect real queries/plans/index coverage, pagination and returned payload size when SQL is involved. Avoid adding indexes, caches or parallel fetches without examining write cost, invalidation, tenant isolation, failure behavior and consistency.
4. For UI measure actual content readiness and interaction, not only skeleton visibility or first paint. Check JavaScript, images/fonts/media, long tasks, layout/paint, memory, mobile CPU/network and motion as relevant; report field and controlled-lab evidence separately.
5. Compare candidate changes under matched conditions with sample counts, dispersion and adverse metrics. A lower LCP with materially worse INP, correctness or backend workload is a trade-off, not a blanket victory.
6. Set the repository's actual budget/cadence from its critical journey and risk; do not assume a universal Lighthouse score or run expensive browser/load gates on unrelated commits.

For an existing elapsed-time budget, record the start signal, usable
completion signal and observing clock. Prefer one observer measuring both
ends on a monotonic clock. Keep wall-clock timestamps for log correlation.
Before subtracting readings from separate observers, establish their common
monotonic timebase and the accuracy needed for the verdict. For example,
raw `performance.now()` readings from separate Node.js processes use their own
time origins. If only separate stages are measurable, report those durations
and keep the end-to-end duration unverified. See
`src-w3c-high-resolution-time` and `src-node-perf-hooks-time-origin`.

When a performance budget uses a pooled latency percentile, record the
measured event, cohort selection, time window, sample count and estimation
method. Count each compatible observation once. Combine raw observations or
compatible histogram counts for that population before computing the
percentile. Record bucket resolution when reporting a histogram estimate.
Averages of worker or time-window percentiles, even weighted by sample count,
do not substantiate a pooled percentile. If only those summaries are
available, keep their labels and report the pooled percentile as unverified.
See `src-prometheus-histogram-quantile-aggregation`.

When a timeout ends observation before usable completion, retain the
attempt in its eligible population and record the timeout and last
observation time. Label any percentile calculated only from completed
attempts with that population. Report an exact all-attempt completion
percentile only when the observations determine it. If the observations
leave it indeterminate, record supported bounds or mark the exact percentile
unverified. If observation ends before a later deadline, keep that attempt's
outcome at the deadline unverified unless separately observed. See
`src-nist-engineering-right-censoring` for the observation boundary.

### SIMD and CPU vectorization reviews

For a review of an actual SIMD or autovectorized path, record the target CPU/OS, compiler and build flags. If the build dispatches at runtime, verify that each advertised variant is selected only with its required ISA enabled and that supported targets without it can use the baseline fallback. Compare baseline and vector results under the same arithmetic contract, including reordering or floating-point tolerances where relevant. Cover representative sizes, short inputs and tails that do not fill a vector. Measure matched workloads from equivalent inputs to usable outputs, including any packing, layout conversion and dispatch. Compiler remarks or detected ISA support can identify a code path; measure end-to-end performance before claiming gains. Mark unrun target or fallback cases NOT RUN. See `src-llvm-auto-vectorization` for tails, reductions and vectorization remarks and `src-gcc-x86-cpu-dispatch` for x86 build flags and runtime detection.

When the supported floating-point contract specifies NaN or signed-zero
behavior, exercise those inputs on the baseline and vector paths. Test both
operand orders where they can affect the result. Compare the result class or
exact bit pattern as required by the contract. For example, x86 `MINPS` can
select the second operand for zero ties or an unordered comparison. Finite
controls can pass while these results differ. Keep the observed instruction,
compiler flags and tested CPU with the result. See `src-intel-sdm-packed-float-minimum`.

## Web surfaces

Core Web Vitals are useful field/user-experience indicators for public/user-facing web surfaces. Current Google guidance uses LCP, INP and CLS with user-experience thresholds, evaluated at the 75th percentile for field classification.

Do not turn those metrics into the only performance definition for an application. An operational workflow may also care about API latency, initial JS cost, data-table responsiveness or task completion time.

Use `pb-modern-web-platform-workflow` for native browser opportunities and support/fallback checks. Separate request/server/query time, transfer, hydration/render and interaction-to-useful-content before optimizing. A matching skeleton reserves the real layout and represents pending work; it is not proof that content arrived sooner. Expose usable shells/sections without waiting for unrelated data. Resolve identity, tenant and permissions before overlapping independent reads, and preserve bounded workload, cache isolation, errors and truthful completion. Browser `content-visibility`, animation or prefetch cannot repair excessive SQL fan-out by itself.

When a web journey already uses `WebAssembly.instantiateStreaming()`,
verify the response's `Content-Type` and the outcome of that call in the
supported runtime. Hold the valid module bytes and successful response
status fixed. Compare `application/wasm` with `application/octet-stream`
or an absent header. Buffered instantiation can succeed even when the
streaming call rejects the response. Measure startup separately if the
change claims a speedup. See `src-w3c-wasm-web-api-streaming` §1.

When an existing lab check uses browser Long Tasks, record support for
`longtask` in `PerformanceObserver.supportedEntryTypes` and collect entries
with `PerformanceObserver` during the measured window. The direct
`performance.getEntriesByType("longtask")` query can be empty while the
observer receives entries. Confirm collection with a bounded positive
control and compare the observed task interval with the measured work.
Report unsupported coverage as unavailable. See
`src-w3c-performance-timeline-observer` §§5 and 6.4 and
`src-w3c-timing-entry-names-registry` §3.

When an existing `IntersectionObserver` trigger requires positive overlap,
include a separated target, one touching the root edge, and one partly
inside. `isIntersecting` can be true at edge contact with zero intersection
area. Compare the actual rectangle and ratio with the trigger's required
threshold. Verify what the consumer records when that condition changes.
Use separate rendered evidence if the contract concerns what a user sees.
See `src-w3c-intersection-observer-geometry` §3.2.8.

When an existing `ResizeObserver` consumer uses dimensions for transformed
content, record the observed box and the geometry the consumer needs. Compare
a real size change of the chosen layout box with a transform-only change.
A scale can change `getBoundingClientRect()` without producing an observation
for the target. Verify the consumer's update path and use a real size change
as a control that the observer still receives entries. See
`src-w3c-resize-observer-layout-box` §§3.4.1 and 3.4.8 and `src-w3c-cssom-view` §6.

For browser Resource Timing, a zero `transferSize` can reflect local cache reuse or restricted cross-origin timing. Record the resource origin and timing exposure in the tested browser. A matching `Timing-Allow-Origin` can expose more detail, and browsers can still mask size values. Confirm cache reuse or revalidation with matched cold and warm runs and separate request evidence. Record masked values as unavailable for transfer conclusions. Use a separate measurement for exact wire or header bytes. See `src-w3c-resource-timing`.

For an existing responsive image preload, compare the rendered image's
`currentSrc` with the image requests actually made at representative
viewport widths and device pixel ratios. Under matched cache conditions,
look for both an extra request for an unselected variant and repeated
requests for the selected URL. If the image is claimed as Largest
Contentful Paint (LCP), identify the observed candidate element and URL
separately. See `src-whatwg-html-responsive-image-preload` and
`src-w3c-largest-contentful-paint-20261117` §3.1.

When measuring first useful content across browser navigation, record a
back/forward cache restore separately from a new document load or reload.
Check `pageshow.persisted` on the observed history transition and record the
browser and harness configuration. In a lab, a stable document marker and an
origin request log can corroborate restoration. A warm HTTP cache can supply a
new document without a new origin request. Assess usable content and any
required refresh in the actual restored state. See `src-whatwg-html-page-transition-events`.

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
      "id": "performance-bottleneck-triage",
      "type": "decision-question",
      "text": "For a performance audit, identify the critical journey and representative workload. Trace client/network/server/auth/SQL/hydration/background segments and choose matching metrics; distinguish perceived shell readiness from real data completion. Audit alone does not authorize load tests, deploys or provider spending.",
      "source": "pat-performance-budgeting",
      "covers": ["performance"],
      "activate_when": ["archetype:performance-review", "risk:performance"],
      "force": "must",
      "phase": ["planning", "implementation"],
      "priority": 96
    },
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
      "id": "performance-simd-path-evidence",
      "type": "verification",
      "force": "should",
      "text": "Compare baseline and vector results on relevant target CPU/OS and build settings. Where optional ISA variants are supported, check runtime dispatch and the baseline fallback. Verify the arithmetic contract on representative, short and non-multiple lengths. Measure matched end-to-end work including dispatch, packing or conversions where used. Compiler remarks identify compilation choices; report speed only from measurements. Mark unrun target and fallback cases NOT RUN.",
      "source": "pat-performance-budgeting",
      "covers": [
        "simd-path-correctness"
      ],
      "activate_when": [
        "archetype:simd-implementation-review"
      ],
      "phase": [
        "planning",
        "verification"
      ],
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
