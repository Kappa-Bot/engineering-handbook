---
id: gov-handbook-governance
kind: governance
status: active
owner: engineering
version: "0.1"
applies_to:
  - engineering-handbook
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Handbook Governance

## Purpose

This document defines the authority, scope, precedence, canonicality, ownership, and exception model of the Engineering Handbook.

## What the handbook governs

The handbook is authoritative for engineering knowledge deliberately promoted to cross-repository scope. It governs reusable engineering behavior and knowledge, not every local implementation detail.

Consumer repositories remain authoritative for their own:

- product/domain decisions;
- exact commands and tool versions;
- architecture that is not promoted as universal;
- deployment topology;
- local ADRs;
- approved exceptions permitted by handbook governance.

The handbook does not override law, contractual obligations, provider constraints, security obligations, or other non-negotiable external requirements.

## Normative language

- **MUST / MUST NOT** — mandatory inside the declared `applies_to` scope unless a permitted exception exists.
- **SHOULD / SHOULD NOT** — expected default; deviations need a concrete reason.
- **MAY** — optional.

Normative force applies only inside the document's declared scope. A statement is not universal merely because it appears in the handbook.

## Precedence

When two applicable pieces of guidance conflict, use this order:

1. External non-negotiable obligations.
2. Active Handbook Governance.
3. Applicable active Policy.
4. Applicable active Standard.
5. Approved repo-local decision or explicitly permitted exception.
6. Pattern.
7. Playbook.
8. Reference or research.

A repo-local ADR MUST NOT silently override an applicable Policy or Standard. If a mandatory rule allows exceptions, the local decision records the exception; it does not rewrite the universal rule.

## Direct owner instructions

A direct owner instruction may select among permitted options or activate a permitted exception. Example: `pol-workspace-git-hygiene` allows an explicitly requested worktree even though normal operation uses one working tree.

A direct instruction SHOULD NOT be treated as an invisible permanent policy change. If the instruction should become the new default, update the canonical handbook artifact.

## Canonicality

There MUST be at most one active canonical normative document per topic.

When guidance changes:

- update the active document when the topic remains fundamentally the same;
- create a new decision record when the rationale/history matters;
- supersede an older artifact when replacement is clearer than mutation;
- preserve meaningful history instead of maintaining two active truths.

Other documents SHOULD link to the canonical artifact instead of copying its normative text.

## Ownership

`owner: engineering` means responsibility for:

- maintaining applicability;
- reviewing the artifact by `review_due`;
- resolving conflicts;
- approving normative changes;
- deciding whether an exception or promotion is justified.

More granular ownership is introduced only when the organization actually needs it.

## Exceptions

An exception to mandatory handbook guidance is valid only when the governing artifact permits exceptions.

A material exception MUST be:

- explicit, not inferred;
- scoped to a repository, task, environment, or time window;
- no broader than necessary;
- recorded where future maintainers can discover it;
- reviewed when its reason expires or changes.

Examples of material exceptions include unusual workspace topology, security-control deviation, persistent architectural divergence, or a release gate intentionally waived by an authorized owner.

## Universal vs repo-local

A rule belongs in the handbook only if its value is genuinely cross-repository or strategically reusable. Local decisions remain local until deliberately promoted through `gov-knowledge-promotion`.

This prevents the handbook from becoming a mirror of every product repository.

## Governance changes

Changes to authority, precedence, canonicality, lifecycle, source-tier semantics, or promotion rules SHOULD receive a decision record when they materially alter the operating model.
