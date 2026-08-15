# Kappa-Bot Engineering Global Instructions

Canonical source: `Kappa-Bot/engineering-handbook` Foundation v0.1.

- Keep scope narrow; do not perform unrelated refactors or cleanup.
- Search before building: current repo -> handbook -> internal repos/assets -> mature external solutions -> new design.
- Use zero subagents by default. Use them only when explicitly requested or clearly justified by genuinely independent parallel work.
- Use one normal working tree by default. Do not create Git worktrees unless explicitly requested or clearly justified by real parallelism in the same repo.
- Keep transient files outside the repository when practical and leave a clean, accounted-for handoff.
- Never destroy unmerged or user work to clean the workspace.
- Plan proportionally before complex implementation; keep trivial work lightweight.
- Do not silently expand scope.
- Never claim a verification gate passed unless it was actually run and observed.
- Load repo-local `AGENTS.md` and specialized skills/playbooks only when relevant; avoid bloating permanent context.

Canonical policy IDs: `pol-agent-operating-model`, `pol-workspace-git-hygiene`, `pol-reuse-first`, `pol-verification-definition-of-done`.
