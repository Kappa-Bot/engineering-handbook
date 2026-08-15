---
id: pat-visual-evidence-integrity
kind: pattern
status: active
owner: engineering
version: "0.1"
applies_to:
  - visual-regression
  - ui-acceptance
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Visual Evidence Integrity

## Intent

Screenshots are useful only when they prove the state they claim to show.

This Pattern was promoted after mature internal projects exposed false confidence from large screenshot sets whose filenames, state transitions, viewport identities or retained artifacts did not match the actual UI.

The objective is **evidence truth, not screenshot volume**.

## 1. Define semantic coverage before capture

For a material visual acceptance run, define the required semantic states first.

Good state names describe product meaning:

- `origin-validation`;
- `inventory-multi-room`;
- `theme-dark`;
- `agenda-month`;
- `draft-resumed`.

Avoid opaque `state-01`, `step-07` or screenshot-count targets unless the number itself is a stable domain concept.

Completeness comes from the required-state matrix, not from "we generated N screenshots".

## 2. Assert state before capture

A capture helper MUST NOT assume that clicking a button advanced the UI.

Before retaining evidence:

- drive the UI through deterministic user/product actions or deliberate seeded state;
- assert the semantic marker that proves the intended state;
- only then capture.

Examples:

- assert the Month control is selected before naming a screenshot `agenda-month`;
- assert the expected validation message before `*-validation`;
- assert theme resolution before `system-dark`;
- assert the expected workflow chapter before calling it populated/review.

A filename is metadata, not proof.

## 3. Isolate scenarios

Each semantic scenario MUST begin from a deliberate state boundary.

Where browser persistence matters:

- use a fresh context/storage state; or
- explicitly seed the exact persistence needed by that scenario.

An "empty" capture MUST NOT accidentally inherit a draft from a previous scenario. Viewport/theme/project loops MUST NOT leak local/session state unless the scenario explicitly tests persistence.

## 4. Bind provenance to the artifact

When visual evidence is used for durable acceptance/release claims, retain enough metadata to establish what produced it.

A strong metadata contract includes, as applicable:

- browser/project;
- route/surface;
- semantic state;
- CSS viewport width/height;
- device scale factor;
- actual image pixel dimensions;
- theme/color-scheme state;
- capture kind (`viewport`, `full-page`, `print`, etc.);
- build/commit identifier when evidence spans releases;
- artifact SHA-256 or equivalent content hash.

CSS viewport dimensions and image pixel dimensions are not necessarily equal on device-emulation projects. Evidence tooling MUST account for device scale rather than declaring valid mobile images corrupt—or accepting mislabeled images—based on raw dimensions alone.

## 5. Prevent overwrite and cross-run contamination

Different projects/browsers/viewports/themes/states MUST resolve to distinct artifact identities unless they are intentionally declared equivalent.

Dedicated cross-browser runs SHOULD use dedicated project names/roots so results from a base suite cannot silently overwrite or mix with canonical cross-browser evidence.

Before a canonical evidence run, clear or isolate its output root so stale files cannot make incomplete coverage appear complete.

## 6. Detect fake diversity

If two semantic states are expected to look different, exact-identical screenshot hashes SHOULD fail the evidence check unless the equivalence is explicitly justified.

Duplicate detection is not a visual-regression algorithm; it is a guard against:

- blind state loops;
- failed navigation;
- overwritten output paths;
- un-applied themes;
- stale captures.

## 7. Review boards/contact sheets

Contact sheets/boards can accelerate human visual review but are derived artifacts.

If a release/acceptance claim depends on them:

- generate them from verified evidence metadata;
- retain them as named artifacts;
- fail the evidence gate when a required board is missing.

Do not claim a board was reviewed if it was not retained/generated in the canonical run.

## 8. Geometry evidence

Document-level overflow checks are not enough for transformed/animated compositions.

For critical elements, visual QA MAY include assertions that their bounding boxes remain within the practical visual viewport or intended container at important animation/layout states.

Use this to catch content that is technically inside the layout tree but visibly clipped/offscreen.

## 9. Automation vs native truth

Automated browser evidence SHOULD cover repeatable regressions broadly.

It MUST NOT be reported as proof of:

- launcher icon refresh on a real OS;
- native virtual-keyboard behavior that was not exercised;
- physical camera ergonomics;
- installed-PWA behavior on an untested platform;
- assistive-technology combinations not actually tested.

Record those as separate manual/native gates.

## 10. Minimum acceptance record

A material visual acceptance result SHOULD make it possible to answer:

1. What exact build was tested?
2. Which semantic states were required?
3. Which browsers/projects/viewports/themes produced evidence?
4. Was state asserted before capture?
5. Was scenario storage isolated?
6. Were expected-distinct frames checked for accidental duplicates?
7. Which visual/native checks were manual?
8. What was not run?

If those questions cannot be answered, the evidence is useful for debugging but weak as release proof.
