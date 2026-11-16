---
id: ref-unslop-adoption-assessment
kind: reference
status: active
owner: engineering
version: "1.0"
applies_to:
  - engineering-handbook
  - user-facing-web-surfaces
  - design-research
sources:
  - src-unslop
last_verified: 2026-11-16
review_due: 2027-02-16
---

# Unslop: method adoption and stronger delivery contract

## Evidence and authority

Inspected source: [Damir Sokolovsky's Unslop](https://github.com/heydamir/unslop/tree/620163eedb3529d9cd23a3994ed8d287d06f760d), commit `620163eedb3529d9cd23a3994ed8d287d06f760d`, dated 2026-11-15T00:55:18Z, assessed 2026-11-16. Pin the commit rather than assuming a package version; the inspected plugin metadata has no semantic version. `src-unslop` is Tier B for an original design method and implementation, not an independent effectiveness study or accessibility authority.

The owner authorized aggressive Handbook adoption on 2026-11-16. `adr-0009-unslop-design-reconstruction` records the applicability decision. Normative force comes from the updated `std-ui-ux-quality-baseline`, not directly from this external source. `pat-design-context-layering` owns context resolution; `pb-frontend-quality-review` owns the operational procedure.

| Inspected upstream artifact | Blob SHA | Role |
| --- | --- | --- |
| `skills/unslop/SKILL.md` | `93eed69f2a91b28035e91998a641d6a3faf9b62e` | Direction, ordered passes, restrictions and acceptance checklist |
| `skills/unslop/references/signs.md` | `7b6ab40d8684a63c2156ed6910abcc960cf29c42` | Concrete signs of generic visual/textual output |
| `skills/unslop/references/tokens.md` | `fbb051825c9695151a9757cc3e16bcbc1e9d8a95` | Suggested visual values, not universal standards |
| `skills/unslop/references/visuals.md` | `d7e89c14ddc675def22a46435ef1f2053d8d9362` | Image direction, composition and generation workflow |
| `skills/unslop/scripts/snapshot.mjs` | `ef226aa4650fb84d238d434035d73606abdcb88a` | Browser/HTML snapshot utility |
| `skills/unslop/scripts/story.mjs` | `daa0695a9df4955555b147ee9e7683f24ea71cae` | Presentation video utility |
| `LICENSE` | `da6ab6cc8f333d7e89a99812866df8f24374d47c` | CC BY 4.0 notice and conditions |

Use the pinned commit path for source comparisons. Repository popularity and example before/after videos do not establish better task performance, revenue, accessibility or maintainability.

## Full method, deliberate improvements

| Source capability or constraint | Handbook adoption and improvement |
| --- | --- |
| Inspect before editing; enumerate defects by location | Adopt as rendered diagnosis and an actionable route/state/element record, including the actual journey and semantic states |
| Product, character, world, focal moments and signature | Adopt the direction framework; tie it to verified content, user work and acceptance rather than generic premium adjectives |
| Nine ordered design passes | Adopt every dimension in the existing frontend Playbook; require changed/retained/not-applicable dispositions and revisit dependencies when copy or layout changes |
| Preserve sections/order and keep palette/type/layout for light slop | Replace with diagnosis-led reconstruction; earlier approval is not permanent protection when the owner authorizes redesign |
| Keep a run under three product renders | Reject as an acceptance ceiling; use risk/state coverage and actual defect closure without inventing an iteration quota |
| Ban hue gradients, weights 700–900, italic, colored icons and similar treatments | Replace blanket bans with deliberate role, readable hierarchy, accessibility and measured-cost evaluation; no universal neutral skin |
| Generated scene is the strongest hero | Replace with comparison of real imagery, truthful product view, editorial/type-led composition and purposeful generated artwork |
| Plausible mock numbers and names | Keep only as identifiable synthetic fixtures/demo content; never silently promote them to reviews, customers, metrics or production evidence |
| Leave an empty image slot when generation is unavailable | Deliver a complete alternative using authorized assets, or mark the actual deliverable blocked/incomplete |
| Static snapshot or story video | Optional presentation/prototyping, not production implementation, functional equivalence or release proof |

The adoption deliberately changes both upstream constraints and old Handbook defaults. It does not preserve a weak interface under the label of "brand consistency", and it does not replace that interface with the same new template across every product. Legal identity, facts, tenant/data boundaries and task authority are not aesthetic constraints to discard.

## Environment, risk and maintenance fit

- **Stack fit:** the method operates on product/source/render evidence rather than requiring React, Tailwind or a new component library. This fits heterogeneous MelodIQ public sites and operational applications without a shared CSS migration.
- **Real product scope:** application quality includes pending/empty/error/confirmed states, progressive availability, dense content, keyboard, touch, zoom, locales, theme and route continuity. A single polished screenshot cannot establish it.
- **Accessibility and performance:** existing canonical UI and performance owners remain controlling. No tiny-font, contrast, one-chart, blur or animation recipe overrides them. Fix the critical journey before claiming a design success.
- **Operational cost:** reuse the existing deterministic router, tests and distribution bundle. Do not add model calls, paid image services, observers, schedulers or dependencies merely to adopt a design method.
- **Permission fit:** current explicit constraints remain distinguishable from old defaults. An authorized visual rewrite can revise visual decisions; an audit, read-only reference or local change cannot authorize a release or mutation of another product.
- **Maturity/effectiveness:** inspected code and examples support the method's existence, not a statistically measured benefit. Evaluate consumer outcomes after real use and revise the canonical method when evidence contradicts it.

## Why executable tools are not imported

The snapshot utility launches a new browser, clones page DOM, collects styles/assets and saves HTML plus a screenshot. It does not redact sensitive information. It removes scripts and responsive sources and freezes the selected image; remaining external URLs may still load remotely. Therefore it is neither a sanitized archive nor a functional/responsive equivalent of the application.

The story utility executes a local presentation through a browser, serves files on loopback, invokes ffmpeg with overwrite behavior and removes a fixed `.story-frames` directory. The pinned revision includes path-containment fixes and related tests; those tests are not a visual-quality suite. Future authorized use needs an isolated, disposable output directory, reviewed inputs, explicit overwrite targets and data minimization. Neither script was executed for this Handbook integration.

No script, bundled demo, generated image, reference asset or external dependency is copied into the Handbook bundle. Adopting the complete design method does not require adopting a video server or an unaudited data capture path.

## Evaluation scenarios and evidence limits

Use these scenarios for semantic review, in addition to the existing deterministic contract/routing suite:

| Scenario | Required decision |
| --- | --- |
| Previously approved glass dashboard; full redesign authorized; weak hierarchy | Reconstruct the composition and replace the old material/tokens when justified; preserve capabilities and data/roles |
| Clean landing with interchangeable headlines and no product identity | Diagnose real slop despite tidy spacing; change content and composition, not only color |
| Distinctive, readable interface using strong weights and a purposeful gradient | Retain supported expression; do not normalize it to the author's preferences |
| Attractive hero with broken form, hidden focus or delayed available content | Keep acceptance incomplete and fix the actual flow; presentation is not a substitute |
| Read-only audit or license documentation task | No edits/publication, and no design runtime guidance for mere source research |
| Dense CRM with real customer records | Use safe fixtures or redacted evidence; no private snapshots in the public Handbook |
| No paid image capability | Choose a complete honest composition without fabricated claims or unauthorized spending |
| One typo/margin or backend-only change | Stay within the bounded task; no implicit full redesign |

These are test/review inputs, not claims that deployed applications passed. The delivery record identifies tests actually run, unavailable gates and observed review results. There is no asserted portfolio redesign, new consumer installation, performance gain, conversion uplift or security certification.

Task classification is heuristic guidance selection, not a general natural-language permission parser. The design-specific negative cases do not certify every negated deployment/mutation phrase in the existing runtime. Agents must still resolve the actual current request and permissions; a descriptor risk or operation tag never authorizes an action.

## Attribution and reuse

Original work: **Unslop**, created by **Damir Sokolovsky ([@heydamir](https://x.com/heydamir))**, [source repository](https://github.com/heydamir/unslop), [pinned source](https://github.com/heydamir/unslop/tree/620163eedb3529d9cd23a3994ed8d287d06f760d). Licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); [complete upstream license and warranty disclaimer](https://github.com/heydamir/unslop/blob/620163eedb3529d9cd23a3994ed8d287d06f760d/LICENSE).

**Modified by MelodIQ / Kappa-Bot on 2026-11-16:** substantial adaptation of the direction framework, anti-slop diagnosis and nine-pass method in the UI Standard, Design Context Layering and Frontend Quality Review. Changes include aggressive structural freedom, explicit supersession, removal of stylistic/render-count prescriptions, real-flow acceptance, privacy and permission boundaries, and deterministic routing. Preserve this credit, source/license links and modification statement when sharing those adapted portions. No endorsement by the original author is implied; the upstream license supplies no warranties.

This notice concerns the adapted material, not a blanket relicensing of unrelated Handbook code/documents. It does not assert that applying the method automatically requires adding attribution to every application's user-facing footer. Any future reuse of upstream assets, scripts or videos requires retaining the notices applicable to that actual material.

Review the pinned source and adaptation by 2027-02-16 or on contradictory evidence, license changes or material upstream changes. Update deliberately; do not auto-import upstream instructions into normative policy.
