# Contributing

Changes to the Engineering Handbook must preserve authority, traceability, progressive disclosure, and a single source of truth.

## Before editing

Classify the change before writing it:

- **research** — evidence gathering; not authoritative;
- **decision** — a durable choice and its consequences;
- **governance/policy/standard** — normative behavior;
- **pattern** — reusable solution;
- **playbook** — reusable procedure;
- **reference** — supporting knowledge;
- **template/executable asset** — repeatable implementation of stable knowledge.

Do not silently move from research to implementation or from recommendation to mandatory policy.

## Change flow

1. Define the problem or reusable learning.
2. Search the current repository and `machine-readable/catalog.yaml` for an existing canonical topic.
3. Check whether the solution already exists in another internal repository.
4. Research external solutions only when they materially improve the decision.
5. Register material external sources in `machine-readable/sources.yaml`.
6. Separate source facts from internal applicability and internal decisions.
7. Keep non-generalizable knowledge repo-local.
8. Promote generalizable knowledge through `governance/knowledge-promotion.md`.
9. Update or supersede the canonical artifact rather than creating a competing page.
10. Update lifecycle metadata and `machine-readable/catalog.yaml`.
11. Verify links, metadata, scope, and any executable checks that actually exist.

## Required metadata

Active governance, policies, and standards use frontmatter equivalent to:

```yaml
---
id: pol-example
kind: policy
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources:
  - src-example
last_verified: 2026-08-15
review_due: 2027-02-15
---
```

Required fields:

- `id`
- `kind`
- `status`
- `owner`
- `version`
- `applies_to`
- `sources`
- `last_verified`
- `review_due`

Use `supersedes` and `superseded_by` only when they are real.

Decision records are historical artifacts and follow the decision template instead of the active-document lifecycle model.

## Normative changes

A new or strengthened `MUST`, `MUST NOT`, or organization-wide `SHOULD` requires:

- a clear problem statement;
- defined applicability;
- evidence proportionate to the rule's impact;
- consistency with governance and existing active policies;
- an exception model where exceptions are legitimate;
- a migration note when existing repositories are affected.

Source authority alone does not make a rule universally applicable.

## Review checklist

Before handoff, confirm:

- no duplicate active normative topic was created;
- source IDs resolve in `machine-readable/sources.yaml`;
- internal IDs and paths resolve in `machine-readable/catalog.yaml`;
- normative language matches the intended force;
- repo-local material has not leaked into a universal rule;
- no speculative folder or automation was added;
- all claimed verification was actually executed;
- unrun checks are named explicitly rather than implied as passing.
