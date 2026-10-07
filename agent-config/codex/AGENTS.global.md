# Kappa-Bot Engineering Global Instructions

Canonical source: `Kappa-Bot/engineering-handbook`.

The Engineering Handbook governs all engineering/repository work. Keep this file small: trivial local work may be decided by this baseline plus repo-local authority, while specialized procedures belong in focused handbook artifacts loaded only when relevant.

- Keep scope narrow. No unrelated refactors, abstractions, or cleanup.
- Reuse first: current repo → handbook → relevant mature internal assets/repos → mature external solutions → new design.
- Treat the handbook as the canonical baseline, not a ceiling: for new transversal or quality-sensitive work, compare relevant mature internal implementations when that can materially improve the result.
- Keep capabilities truthful across local/demo/Preview/QA/Production. Do not simulate unavailable persistence, security, deployment, offline or integration behavior.
- Use zero spawned workers by default. Route in this order: deterministic tool/script → direct controller execution → one Agency Agents specialist → second independent specialist only for distinct parallel value or a required review boundary.
- Agency Agents is the upstream specialist-persona catalog. A matching persona is not itself a reason to spawn; use `std-agent-runtime-routing`, `pb-agent-runtime-routing` and `ref-agency-agents-specialist-routing`.
- Do not use fixed `parent/design-quality/delivery` identities or bind models to job titles. Specialist persona, model and reasoning effort are separate runtime decisions.
- Prefer the efficient model tier (currently GPT-6 Luna) at low/medium effort for frozen, bounded implementation with strong verification. Use Sol/Astra only when uncertainty, dependency breadth, impact, weak verification or genuinely difficult reasoning justifies the extra resource use.
- Every spawn sets both model and reasoning effort explicitly when supported; resolve the actual spawn allowlist and record requested/actual values rather than silently substituting. Do not let a worker accidentally inherit an expensive controller configuration.
- Independent model review is risk-triggered, not universal. Strong deterministic tests + diff inspection can close low/medium-risk work; security/authz/tenant isolation, durable-data migration, money, consequential Production/provider actions, costly external contracts, partial concurrency proof or high-impact weakly-verifiable architecture require independent review.
- Escalate by cause, not by automatic Luna→Sol→Astra retry ladders: fix environment failures, resolve authority ambiguity, let the same worker fix clear defects, change method/specialist for repeated bad hypotheses, and increase capability/effort only for actual reasoning insufficiency.
- Keep routine concurrency at zero/one and at most two workers concurrently unless a distinct contribution clearly exceeds context/coordination cost. No nested spawning by default; controller owns integration and final claims.
- When the owner authorizes exhaustive zero-cost execution, continue dependency-ready authorized work through checkpoints while respecting actual runtime, mandatory evidence, sensitive-action authority and monetary limits.
- Use one normal working tree by default. Do not create Git worktrees unless explicitly requested or real same-repo parallelism clearly justifies one.
- Preserve unmerged and user work. Never use destructive cleanup merely to simplify the workspace.
- For actively managed Kappa-Bot project repos, `main` is the default persistent product branch. Feature/release/docs branches are temporary source-control tools and must be resolved/deleted after integration or initiative closure without destroying unique work. Do not create or preserve a `qa`/`staging` branch as an environment boundary unless the owner explicitly approves that exception.
- For Supabase-backed Kappa-Bot projects, the default persistent paid remote database topology is **Production only**. Pre-production database/integration verification uses local or otherwise ephemeral non-Production Supabase. Do not provision or retain a paid QA/Staging Supabase project, Supabase database branch, or one database environment per vertical/Git branch unless the owner explicitly approves the cost exception. A Git branch never implies a provider database branch/project, and Production must not be used as general QA merely because a remote QA environment is absent.
- Keep transient scratch/review files outside the repo when practical.
- Plan proportionally before non-trivial implementation; keep mechanical work lightweight.
- Keep research, decision, spec, plan, implementation, verification and adoption distinct when the distinction matters.
- Do not silently expand scope.
- Never claim a gate passed unless it was actually executed and observed.
- Distinguish source/build checks from deployment, migration, runtime, visual and native-device evidence.
- Treat CI and repository automation as metered infrastructure: keep automatic push/PR hot paths small, non-duplicative and timeout-bounded; run expensive build/DB/browser/visual/remote gates only at the cadence their distinct risk requires, and measure real workflow timing after material changes.
- Tests, scripts, docs, workflows, fixtures and generated artifacts need current consumers; merge or remove obsolete machinery instead of keeping implementation history alive in the working repository.
- Never surface raw backend/transport/provider diagnostics as ordinary user-facing product copy; preserve technical detail in appropriate internal observability and present users with human recovery-oriented messages.
- Prefer small, reviewable changes and an explicit handoff.
- Load repo-local `AGENTS.md` and only specialized handbook material required for the task; minimize permanent context and duplicated instructions.
- For non-trivial work, use the single generic `engineering-handbook` router and its deterministic context capsule/delta flow when available; trivial work remains governed by the handbook without requiring a full context query when the baseline and local instructions already decide it.
- For material user-facing UI/PWA work, apply the applicable UI/PWA baseline, `pat-design-context-layering` when design context is material, and inspect rendered output when tooling permits; do not replace product/brand direction with generic framework/SaaS defaults.
- For material UI/UX implementation, route only the skills that can change the result: `ui-ux-pro-max`, `taste`, `impeccable`, and the relevant Emil interaction/motion/prototyping/library skills. Do not invoke the full design-skill set performatively.
- For substantial agentic execution, use only the planning/TDD/debugging/verification/review methods required by the stage/risk. `/caveman Ultra` is optional when installed and useful; no process-skill suite is the specialist-agent taxonomy.
- Discover actual MCP/CLI availability, authentication and permissions; prefer available `playwright-cli` for suitable browser exploration while retaining the repo's required test gates. Avoid duplicate tool actions and load only relevant resources under the Standard's cost controls.
- For material architecture/data/security/release/production changes, apply the corresponding handbook baseline and keep provider/tool choices contextual.
- Generated handbook capsules never override canonical Markdown or permitted repo-local decisions.
- Reconcile active consumer routing and installed projections through existing adoption/sync procedures; a Handbook commit is not proof that a workstation or live model was updated. Refresh/reconcile Agency Agents at safe boundaries, record material upstream revision/runtime routing, and do not equate an Agency Agents app binary update with persona reconciliation. Preserve unrelated local settings and historical evidence.
- Do not create domain-specific skills to duplicate the handbook.

Canonical policy IDs:
`pol-agent-operating-model`, `pol-workspace-git-hygiene`, `pol-reuse-first`, `pol-verification-definition-of-done`, `pol-truthful-engineering`.

Canonical cross-cutting Standard IDs:
`std-architecture-data-integrity-baseline`, `std-security-identity-baseline`, `std-testing-release-quality-baseline`, `std-production-operability-baseline`, `std-dependency-supply-chain-baseline`, `std-ui-ux-quality-baseline`, `std-web-pwa-baseline`, `std-agent-runtime-routing`.
