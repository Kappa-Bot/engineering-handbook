# MelodIQ Mindset — engineering repository instructions

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

- Zero subagents by default. Spawn only when the user expressly requests delegation or applicable repository/skill instructions request it; merely asking to edit the Handbook does not authorize spawning.
- One normal working tree by default; no Git worktree unless explicitly requested or clearly justified by real same-repo parallelism.
- Plan proportionally for non-trivial changes; do not over-plan mechanical edits.
- Never destroy unmerged or user-authored work during cleanup.
- Never claim a verification gate passed unless it was actually run and observed.
- Before publishing a Handbook source edit, regenerate compiled artifacts and run `python -m automation.engineering_context check --root .`, `python -m automation.engineering_context doctor --root .` and scoped tests. Publish canonical sources and regenerated indices **together in one commit/PR merge**; never send sequential source-then-index GitHub Contents commits directly to `main`. If checks cannot run, retain the work in a branch/PR and record the missing gate.
- The Handbook **must not install or require automatic preflight/update hooks for ANY coding-agent client** (Codex, Claude Code, Cursor, Gemini CLI, VS Code/Copilot, Windsurf, Cline, OpenCode or others). `doctor`, `preflight`, audit and updates are explicit/manual commands only. Reject invalid remote candidates without blocking chats, use verified local snapshots when available and never claim security or release compliance without evidence. Any migration tool must preserve unrelated hooks, project/user state and platform-managed safety controls.
- Codex can load hooks from user, system, trusted project, TOML and plugins. Handbook `doctor` can only show whether its own user-level hooks are removed; inspect resolved hook sources in `/hooks` before declaring a workstation healthy. Never remove unrelated hooks as part of a Handbook repair.

Canonical policies: `pol-agent-operating-model`, `pol-workspace-git-hygiene`, `pol-reuse-first`, `pol-verification-definition-of-done`.
