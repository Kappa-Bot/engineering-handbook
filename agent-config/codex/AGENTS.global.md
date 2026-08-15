# Kappa-Bot Engineering Global Instructions

Canonical source: `Kappa-Bot/engineering-handbook`.

Keep this file small. Specialized procedures belong in repo instructions or governed handbook artifacts loaded only when relevant.

- Keep scope narrow. No unrelated refactors, abstractions, or cleanup.
- Reuse first: current repo → handbook → relevant mature internal assets/repos → mature external solutions → new design.
- Treat the handbook as the canonical baseline, not a ceiling: for new transversal or quality-sensitive work, compare relevant mature internal implementations when that can materially improve the result.
- Keep capabilities truthful across local/demo/Preview/QA/Production. Do not simulate unavailable persistence, security, deployment, offline or integration behavior.
- Use zero subagents by default. Use them only when explicitly requested or when genuinely independent work clearly benefits.
- Use one normal working tree by default. Do not create Git worktrees unless explicitly requested or real same-repo parallelism clearly justifies one.
- Preserve unmerged and user work. Never use destructive cleanup merely to simplify the workspace.
- Keep transient scratch/review files outside the repo when practical.
- Plan proportionally before non-trivial implementation; keep mechanical work lightweight.
- Keep research, decision, spec, plan, implementation, verification and adoption distinct when the distinction matters.
- Do not silently expand scope.
- Never claim a gate passed unless it was actually executed and observed.
- Distinguish source/build checks from deployment, migration, runtime, visual and native-device evidence.
- Prefer small, reviewable changes and an explicit handoff.
- Load repo-local `AGENTS.md` and only specialized handbook material required for the task; minimize permanent context and duplicated instructions.
- For material user-facing UI/PWA work, apply the applicable UI/PWA baseline and inspect rendered output when tooling permits; do not replace product/brand direction with generic framework/SaaS defaults.
- For material architecture/data/security/release/production changes, apply the corresponding handbook baseline and keep provider/tool choices contextual.
- When available, use the single generic `engineering-handbook` router for non-trivial cross-repository guidance; do not create domain-specific skills to duplicate the handbook.

Canonical policy IDs:
`pol-agent-operating-model`, `pol-workspace-git-hygiene`, `pol-reuse-first`, `pol-verification-definition-of-done`, `pol-truthful-engineering`.

Canonical cross-cutting Standard IDs:
`std-architecture-data-integrity-baseline`, `std-security-identity-baseline`, `std-testing-release-quality-baseline`, `std-production-operability-baseline`, `std-dependency-supply-chain-baseline`, `std-ui-ux-quality-baseline`, `std-web-pwa-baseline`.
