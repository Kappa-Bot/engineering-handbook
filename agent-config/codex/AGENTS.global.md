# Kappa-Bot Engineering Global Instructions

Canonical source: `Kappa-Bot/engineering-handbook`.

Keep this file small. Specialized procedures belong in repo instructions, skills, playbooks, standards, patterns, or references loaded only when relevant.

- Keep scope narrow. No unrelated refactors, abstractions, or cleanup.
- Reuse first: current repo → handbook → internal assets/repos → mature external solutions → new design.
- Treat the handbook as the canonical baseline, not a ceiling: for new transversal or quality-sensitive work, compare relevant mature internal implementations when that can materially improve the result.
- Use zero subagents by default. Use them only when explicitly requested or when genuinely independent work clearly benefits.
- Use one normal working tree by default. Do not create Git worktrees unless explicitly requested or real same-repo parallelism clearly justifies one.
- Preserve unmerged and user work. Never use destructive cleanup merely to simplify the workspace.
- Keep transient scratch/review files outside the repo when practical.
- Plan proportionally before non-trivial implementation; keep mechanical work lightweight.
- Keep research, decision, spec, plan, implementation, verification, and adoption distinct when the distinction matters.
- Do not silently expand scope.
- Never claim a gate passed unless it was actually executed and observed.
- Prefer small, reviewable changes and an explicit handoff.
- Load repo-local `AGENTS.md` and only the specialized material required for the task; minimize permanent context and duplicated instructions.
- For material user-facing UI/PWA work, apply the applicable handbook UI/PWA Standard and inspect rendered output when tooling permits; do not replace product/brand direction with generic framework/SaaS defaults.
- When available, use the `engineering-handbook` skill for non-trivial cross-repository engineering workflows; load only references relevant to the current task.

Canonical policy IDs:
`pol-agent-operating-model`, `pol-workspace-git-hygiene`, `pol-reuse-first`, `pol-verification-definition-of-done`.

Canonical UI/PWA IDs:
`std-ui-ux-quality-baseline`, `std-web-pwa-baseline`, `pat-mobile-responsive-interaction`, `pat-visual-evidence-integrity`, `pb-frontend-quality-review`.
