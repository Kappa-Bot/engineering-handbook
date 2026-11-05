---
id: adr-0007-selective-ecc-handbook-adoption
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - all-repositories
sources:
  - src-ecc
last_verified: 2026-11-05
review_due: 2027-02-05
---

# Selectively incorporate ECC into the existing Handbook

## Context and authorization

On 2026-11-05 the owner selected the original `affaan-m/ECC` repository and authorized the Engineering Handbook integration discussed in the project conversation. This authorizes the Handbook changes, not a workstation plugin installation, a new service, spending, or product/Production changes.

The inspected Handbook already has canonical policies and technical standards, risk-based review, Agency Agents specialist routing, a single generic Handbook skill, deterministic context compilation, distribution and regression tests. Replacing that system with an external catalog would discard validated internal decisions and duplicate authority.

The static assessment in `ref-ecc-adoption-assessment` pins upstream evidence and distinguishes useful deltas from already-covered or unsuitable guidance. No measured productivity, security or cost improvement is asserted by this decision.

## Decision

Use ECC as a **Tier B workflow reference**, not as the Handbook's runtime or governance dependency.

1. Incorporate supported improvements into the existing canonical topic owners: verification evidence, safe browser QA, visual baselines, agent-tool supply chain, supervised knowledge promotion and workflow evaluation.
2. Keep one generic Handbook router and progressive disclosure. Do not create a parallel set of domain skills or copy the full ECC catalog into permanent agent context.
3. Preserve Agency Agents as the specialist-persona catalog and `std-agent-runtime-routing` as runtime/economy authority. ECC agent names, models, coverage thresholds, timers and choreography do not become defaults.
4. Keep product design, exact commands, environment boundaries, operational limits and exceptions with their existing owners. This change does not reopen approved product decisions or auto-upgrade consumer repositories.
5. Retain original synthesis and source attribution. If future work copies substantial upstream code or text, preserve the applicable copyright/permission notices and inspect the licenses of any separately referenced dependencies.
6. Evaluate any later executable ECC adoption under `pb-external-solution-evaluation` and `std-dependency-supply-chain-baseline`. Do not install hooks, memory observers, MCP servers or native plugins as a side effect of reading this Handbook.

## Alternatives considered

- **Whole plugin as the engineering baseline:** useful for a new environment, but insufficiently tailored to current authority, permissions, consumer distribution and cost constraints. Not selected as the default.
- **Fork/import the complete catalog:** creates duplicate instructions and a substantial maintenance/update obligation without evidence of benefit. Rejected for this scope.
- **Selective synthesis in existing canonical owners:** selected; keeps the existing system coherent while accepting external improvements.

## Consequences and adoption

The Handbook maintains the adopted contracts and their tests; it does not maintain or endorse every upstream skill. Revisit the assessment at its review date or before using a changed upstream executable component. Upstream updates require an explicit diff/applicability review, not automatic synchronization.

The existing bundle manifest already includes the canonical directories and compiled runtime. Consumers receive the new guidance only after their normal authorized Handbook refresh. A merged Handbook change is source delivery, not proof of installation on a developer's Windows machine or rollout to each product. Verify installed revision and routed behavior separately through `pb-codex-handbook-skill-adoption` / `pb-repository-adoption`.

No scheduled work, background learning, new provider access or automatic consumer rollout is introduced. Existing source authority, review requirements and economy controls remain in force.
