---
id: pol-reuse-first
kind: policy
status: active
owner: engineering
version: "0.3"
applies_to:
  - all-repositories
sources:
  - src-ponytail
last_verified: 2026-11-17
review_due: 2027-02-17
---

# Reuse First / Search Before Build

## Principle

Do not invent a solution until reasonable reuse paths have been checked.

The objective is not maximum reuse at any cost. The objective is to avoid paying repeatedly for solved problems while still rejecting solutions that do not fit.

The Engineering Handbook is the canonical cross-repository baseline, **not a guarantee that no mature internal implementation is better**.

## Search order

For a non-trivial engineering problem, search in this order unless the task clearly makes a step irrelevant:

1. the current repository;
2. the Engineering Handbook;
3. other internal repositories/assets;
4. existing internal patterns/templates/skills/scripts;
5. mature external solutions;
6. only then design a new solution.

For external research, prefer in roughly this order:

1. official standards/specifications;
2. official vendor/framework documentation;
3. original implementations/reference projects/design systems;
4. mature high-quality engineering handbooks;
5. community sources for discovery or gap-filling.

Apply `gov-source-authority` when external material influences a durable decision. For material external adoption choices, use `pb-external-solution-evaluation` rather than inventing a one-off comparison process.

## Handbook baseline vs internal frontier

For ordinary/local work, finding an applicable handbook solution can be a valid stop condition.

For **new transversal, architecture-significant, quality-sensitive, or expensive work**, do not assume that the handbook's current baseline is the strongest internal practice. When a mature internal repository is likely to contain relevant validated experience, compare it before freezing a new cross-repository solution.

This comparison MUST remain proportional. Do not scan the portfolio for a trivial CSS adjustment, typo, local bug or routine implementation when the probability of changing the decision is low.

If a mature repository contains a stronger generalizable practice:

1. use/evaluate it in the current decision as appropriate;
2. challenge it against primary external sources when the topic has authoritative standards;
3. promote the improved synthesis through `gov-knowledge-promotion`;
4. avoid leaving a silent stronger "shadow standard" only in the donor repository.

A donor repository is evidence, not automatic authority. Product-specific implementation details remain local.

## What counts as reuse

Reuse can mean:

- using an existing implementation unchanged;
- adapting an internal component or pattern;
- adopting a standard or mature library;
- copying a template we own;
- using an external concept while implementing it locally;
- reusing a decision/evaluation so the same tradeoff is not researched again;
- promoting a stronger validated project practice so future repositories consume the improved canonical baseline.

Reuse does not require sharing runtime code when sharing code would create harmful coupling.

## Minimum complete change

For non-trivial implementation, simplification or code review, the agent MUST trace the owning flow before choosing a solution: entry point, direct and relevant indirect callers, public/exported contracts, configuration/registries, persistence and external effects, tests and fixtures. Search beyond the current diff where a consumer can change the conclusion. Before deleting apparently unused code, account for dynamic imports, routes, jobs, generated clients, translation keys and external consumers; a missing literal reference is not proof of dead code.

Choose the first **semantically complete and suitable** option: omit unrequested/speculative scope; reuse/adapt the canonical repository solution; use an adequate native/platform or standard-library primitive; reuse an installed dependency; implement the readable local minimum. This decision ladder complements the search order above, not a prohibition on checking primary sources. A new dependency or abstraction needs a current unmet contract, risk, repeated consumer or demonstrated total-cost reason. Native or pre-existing is not automatically suitable.

The implementation MUST fix the cause at its actual owner and preserve the complete requested outcome plus affected invariants. Do not move code while dropping validation, permissions, tenant scoping, constraints, atomicity, error handling, idempotency, accessibility or truthful operation states. A coherent abstraction or approved redesign may require a larger patch yet reduce duplicated ownership and failure modes. Split code by responsibility and change reason, not arbitrary file/line limits; do not trade readable types and explicit boundaries for code golf.

**Minimal means minimum complete change, not shortest diff or least delivered scope.** Do not preserve a weak visual system under an authorized Unslop redesign, create parallel legacy/new paths without a migration reason, or bundle unrelated modernization. Apply `std-ui-ux-quality-baseline` and `pb-modern-web-platform-workflow` when the actual change concerns browser behavior, not for backend-only work.

Verification remains risk-based under `pol-verification-definition-of-done` and `pat-risk-based-verification-matrix`. A small test is a floor, never a universal one-test ceiling; assertions or mocks do not prove real authorization, concurrency, integration or browser behavior. Reviews MUST describe a concrete affected condition, impact and correction, inspect relevant transitive consumers, and distinguish verified defects from hypotheses and unrun checks. Do not cap findings at an arbitrary count or invent findings to fill a quota; deduplicate and prioritize actionable results.

An intentional `shortcut:` or debt comment is evidence to inspect, not an exemption. Material accepted debt belongs in the existing issue/ADR with the affected invariant/limit, owner, review date or trigger and corrective path. Current security, privacy, legal, accessibility or user-contract violations cannot be deferred solely because a scale threshold has not been reached. A review summary is not release authorization or proof of tests/deployment.

This method is adapted from Ponytail under [ADR 0010 and the attributed assessment](../references/modern-web-ponytail-adoption-assessment.md); it introduces no persona, hook, mode or line-count metric.

## Evaluation criteria

Before adopting an internal or external solution, evaluate the dimensions that matter to the task:

- functional fit;
- maintenance maturity;
- security;
- performance;
- accessibility;
- licensing;
- complexity and operational burden;
- lock-in;
- compatibility with architecture and deployment model;
- migration cost;
- long-term ownership.

Do not create fake numeric scores when a concise tradeoff analysis is clearer.

## Stop conditions

Stop searching and proceed when:

- an existing solution clearly fits and its risks are understood; or
- additional research/internal comparison has low probability of changing the decision; or
- the problem is sufficiently local/simple that further research costs more than implementation.

Search-before-build MUST NOT become research paralysis.

## New design

When a new solution is justified, record the reason if the choice is durable or expensive. Typical reasons:

- existing solution does not meet requirements;
- licensing is unacceptable;
- operational complexity is disproportionate;
- security/architecture incompatibility;
- reuse would create stronger coupling than a small local implementation;
- no mature solution exists.

If the resulting learning becomes reusable, consider promotion through `gov-knowledge-promotion`.

## Agent context contract

```json agent-context
{
  "units": [
    {
      "id": "reuse-before-new-design",
      "type": "decision-question",
      "text": "Trace the owner, callers and invariants; which suitable repo, handbook, platform, installed dependency or mature external solution meets the complete request before new design?",
      "source": "pol-reuse-first",
      "covers": ["compatibility"],
      "activate_when": ["intent:create", "intent:modify"],
      "force": "must",
      "phase": ["planning"],
      "priority": 40
    },
    {
      "id": "minimum-complete-change",
      "type": "constraint",
      "text": "Trace direct/indirect consumers and contracts; fix the owning cause with the smallest complete solution. Preserve safety, data, accessibility and approved redesign; no LOC quota, scope cuts, shortcut immunity or one-test ceiling. Verify real affected boundaries and report concrete findings/gaps.",
      "source": "pol-reuse-first",
      "covers": ["change-completeness"],
      "activate_when": ["archetype:lean-change"],
      "force": "must",
      "phase": ["planning", "implementation", "verification"],
      "priority": 100
    }
  ]
}
```
