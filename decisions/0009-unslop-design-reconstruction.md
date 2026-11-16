---
id: adr-0009-unslop-design-reconstruction
kind: decision
status: accepted
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - user-facing-web-surfaces
sources:
  - src-unslop
last_verified: 2026-11-16
review_due: 2027-02-16
---

# Adopt Unslop as an aggressive design reconstruction method

## Context and owner authorization

On 2026-11-16 the owner explicitly authorized a fully aggressive incorporation of Unslop into the Engineering Handbook, including replacing old design models/directives and improving the method for MelodIQ. This supersedes the earlier proposal to keep it merely as a selective, conservative reference behind existing aesthetics. The requested deliverable is the Handbook and its routing/distribution source, not simultaneous edits or releases of all products.

The inspected Handbook base is `2fa4fcb94c5d7d66bd0ce142b72449d5c1faca21`. Its UI Standard and donor learning already protect accessibility, semantic states and evidence, but design-context adoption explicitly favors incremental preservation. The frontend workflow can excuse generic composition, and operator/hero patterns carry preferred visual recipes. The task router also misses ordinary English/Spanish Unslop requests. These gaps would make a reference-only addition ineffective.

The upstream source is pinned to `heydamir/unslop@620163eedb3529d9cd23a3994ed8d287d06f760d`. [The assessment](../references/unslop-adoption-assessment.md) evaluates applicability, limits, adaptations and attribution. It is evidence for a design method, not proof of product outcomes or accessibility certification.

## Decision

1. **Make the method operational and mandatory for material design work.** Keep `std-ui-ux-quality-baseline` as the single normative UI owner. Incorporate rendered diagnosis, product direction, transformation depth, all nine passes with dispositions, and evidence-based acceptance through `pb-frontend-quality-review`. Evolve existing design-context ownership; do not create a competing anti-slop Standard or standalone skill.
2. **Prefer reconstruction when the problem is systemic.** Prior approval, implementation cost already spent, existing tokens and donor precedent do not grandfather a weak design. Within an authorized redesign, replace structure, section order, typography, palette, geometry, materials, components, imagery and motion as needed. Supersede affected local decisions and intentional visual baselines explicitly.
3. **Go beyond upstream.** Remove its preservation of section order/light-slop styling, three-render ceiling, universal typography/color prohibitions and assumed superiority of a generated scene hero. Require the real journey, states, responsive behavior, accessible interaction, truthful media and risk-relevant performance. A finished alternative without paid/generated media is preferable to an unfulfilled placeholder.
4. **Retire portfolio visual recipes, not useful mechanics.** Glass, compact hover rails, curtain theme changes, full-height photographs, animated words and one-family typography remain evaluated techniques, not inherited portfolio defaults. Historic client decisions are evidence with a scope/date, not universal prohibitions. Current explicit constraints and permissions still bind their actual task.
5. **Make the rule discoverable and testable.** Update global/router source, bilingual task classification, phase-specific projections and compiled context. Preserve isolation from documentation/licensing research, backend work and small fixes; routing supplies guidance, never permission. Extend the existing frontend and policy tests rather than adding a parallel execution system.
6. **Keep nonvisual truth and permissions intact.** This decision does not grant new customer-data access, new paid tools, account/SDK/plugin installation, outbound contact, publication, provider changes or edits outside the authorized repository/surface. Audit-only remains read-only. Do not weaken functional, accessibility, privacy, security, legal or release gates to obtain a prettier result.
7. **Attribute the adaptation.** Preserve Damir Sokolovsky / @heydamir, the pinned source, CC BY 4.0 link and a clear modification record for adapted material. Do not relicense unrelated Handbook content or transplant unreviewed assets/scripts.

## Supersession map

| Earlier behavior | Active replacement |
| --- | --- |
| Design-context adoption retains validated art direction by default | Existing design competes on current evidence; authorized reconstruction can replace it |
| Visual distinction only matters when separately requested | Material UI work must fit the actual product/task; a quiet utility still cannot be an indiscriminate template |
| Render/inspect is only a recommendation | Required real-render evidence gates material visual acceptance; missing evidence is incomplete |
| Three broad theses or a cosmetic polish pass can close anti-slop | Diagnosis, five-line direction, nine-pass dispositions and critical-journey acceptance |
| Preferred glass/rail/hero/type treatments behave as portfolio recipes | Optional mechanics selected through the new direction and tested in context |
| Historic single-client hero controls become a universal rule | Current scoped control decisions plus accessible behavior; preserve history without freezing every future design |
| External Unslop name is just documentation | Recognized ES/EN task routing with explicit negative cases and one generic Handbook router |

These are updates to existing active owners, not wholesale retirement of their unrelated content. Historical ADRs and donor reports remain historical. No database, runtime-model policy, business naming contract, legal identity or live application is changed by this decision.

## Alternatives rejected

- **Reference-only or pilot-only adoption:** would preserve the exact conservatism the owner rejected and leave ordinary requests unrouted.
- **Verbatim upstream replacement:** would exchange old recipes for a new neutral visual template, weaker verification and static presentation tooling.
- **Second Unslop skill plus duplicate UI policy:** would split authority, add context drift and bypass the existing deterministic distribution path.
- **Automatic mass redesign/publication:** exceeds the requested Handbook scope and cannot supply consumer-specific evidence.

## Validation, adoption and maintenance

Validate structural integrity, deterministic compilation/freshness, bilingual routing and negatives, normative projections, package distribution and scenario reasoning. Tests prove those behaviors, not better aesthetics, conversion uplift or production performance. Consumer visual acceptance still requires executing the actual product.

The new source policy is active without waiting for a portfolio pilot. Consumers receive it through their normal authorized Handbook/global refresh; source merge is not proof of an installed workstation version. Verify the refreshed bundle and representative routing before claiming consumer adoption. Do not install a second skill as a shortcut.

Review by 2027-02-16 or after contradictory consumer evidence, an upstream license/behavior change or a routing failure. Evaluate pinned upstream deltas deliberately; no automatic code import, background observer, new scheduler or universal palette is created.
