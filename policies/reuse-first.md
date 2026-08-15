---
id: pol-reuse-first
kind: policy
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Reuse First / Search Before Build

## Principle

Do not invent a solution until reasonable reuse paths have been checked.

The objective is not maximum reuse at any cost. The objective is to avoid paying repeatedly for solved problems while still rejecting solutions that do not fit.

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

Apply `gov-source-authority` when external material influences a durable decision.

## What counts as reuse

Reuse can mean:

- using an existing implementation unchanged;
- adapting an internal component or pattern;
- adopting a standard or mature library;
- copying a template we own;
- using an external concept while implementing it locally;
- reusing a decision/evaluation so the same tradeoff is not researched again.

Reuse does not require sharing runtime code when sharing code would create harmful coupling.

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
- additional research has low probability of changing the decision; or
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
