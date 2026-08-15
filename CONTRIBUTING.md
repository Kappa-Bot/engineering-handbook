# Contributing

Changes to the Engineering Handbook must preserve authority, traceability, progressive disclosure, and a single source of truth.

Use `playbooks/engineering-change.md` for the normal engineering workflow: intake, reuse/research, proportional planning, implementation, verification, PR, and handoff. This document contains only the additional rules specific to changing the handbook itself.

## Before editing handbook knowledge

Classify the artifact before writing it:

- **research** — evidence gathering; not authoritative;
- **decision** — a durable choice and its consequences;
- **governance/policy/standard** — normative behavior;
- **pattern** — reusable solution;
- **playbook** — reusable procedure;
- **reference** — supporting knowledge;
- **template/executable asset** — repeatable implementation of stable knowledge.

Do not silently move from research to implementation or from recommendation to mandatory policy.

Before creating a new artifact:

1. search `machine-readable/catalog.yaml` for the canonical topic;
2. determine whether the learning is truly cross-repository or should remain local;
3. evaluate material external sources through `governance/source-authority.md`;
4. promote knowledge through `governance/knowledge-promotion.md` rather than jumping directly to a stronger artifact kind;
5. update/supersede a canonical artifact instead of creating a competing active page.

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

Other artifact kinds SHOULD use enough metadata to support discovery, applicability, source traceability, ownership, and review without inventing fields that have no operational purpose.

## Normative changes

A new or strengthened `MUST`, `MUST NOT`, or organization-wide `SHOULD` requires:

- a clear problem statement;
- defined applicability;
- evidence proportionate to the rule's impact;
- consistency with governance and existing active policies;
- an exception model where exceptions are legitimate;
- a migration note when existing repositories are affected.

Source authority alone does not make a rule universally applicable.

## Registry maintenance

When a handbook change adds, moves, supersedes, or retires an internal artifact, update `machine-readable/catalog.yaml` in the same change.

When it introduces or materially revalidates an external source, update `machine-readable/sources.yaml` in the same change.

Internal docs SHOULD cite stable source IDs instead of duplicating source metadata.

## Automated integrity check

Run the repository-local integrity checker before handing off a handbook change when PowerShell is available:

```powershell
pwsh -File .\automation\handbook\check-integrity.ps1
```

The checker validates structural invariants that otherwise create manual drift:

- duplicate catalog/source IDs;
- duplicate or missing catalog paths;
- required catalog/source registry fields;
- frontmatter presence and ID/kind/status alignment for governed artifacts;
- unknown `src-*` references in source-bearing handbook artifacts;
- the current Engineering Handbook skill bundle header and include paths.

It deliberately does **not** judge architecture quality, normative wording, applicability, source freshness, or whether a new artifact should exist. Those remain semantic review responsibilities.

If the environment cannot run PowerShell, report this gate as **not run**; do not claim the integrity check passed based on manual inspection alone.

## Handbook review checklist

In addition to the engineering-change verification and automated integrity check, confirm:

- no duplicate active normative topic was created;
- normative language matches the intended force;
- source authority is not confused with organizational applicability;
- repo-local material has not leaked into a universal rule;
- no speculative folder or automation was added;
- no second source of truth was created by copying canonical content;
- all claimed verification was actually executed.
