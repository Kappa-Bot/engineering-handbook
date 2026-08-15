# Engineering Handbook Repository Instructions

These instructions govern edits to this repository only. They are intentionally small.

## Purpose

Treat this repository as the canonical source for cross-repository engineering governance and promoted knowledge.

## Editing rules

- Search `machine-readable/catalog.yaml` and the repository before creating a new topic.
- Maintain at most one active canonical normative document per topic.
- Do not copy a universal rule into multiple pages. Link to the canonical artifact instead.
- Keep repo-specific architecture, commands, domain decisions, and exceptions in the consumer repo unless deliberately promoted.
- Do not turn external guidance directly into a `MUST`; apply `governance/source-authority.md` and `governance/knowledge-promotion.md` first.
- Register material external sources in `machine-readable/sources.yaml` and reference source IDs from governed documents.
- Update `machine-readable/catalog.yaml` whenever an internal artifact is added, moved, superseded, or retired.
- Preserve meaningful decision/supersession history instead of rewriting history to look current.
- Do not create empty taxonomy folders or speculative automation.
- Keep temporary/scratch/review artifacts outside the repository.
- Keep changes narrow; no unrelated cleanup or refactors.

## Operating model

- Zero subagents by default.
- One normal working tree by default; no Git worktree unless explicitly requested or clearly justified by real same-repo parallelism.
- Plan proportionally for non-trivial changes; do not over-plan mechanical edits.
- Never destroy unmerged or user-authored work during cleanup.
- Never claim a verification gate passed unless it was actually run and observed.

Canonical policies: `pol-agent-operating-model`, `pol-workspace-git-hygiene`, `pol-reuse-first`, `pol-verification-definition-of-done`.
