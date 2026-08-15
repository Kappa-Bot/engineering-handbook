# Engineering Handbook

The Engineering Handbook is the canonical engineering knowledge and operating-system repository for Kappa-Bot products.

Its purpose is to turn engineering learning into a governed system that can be discovered, challenged, promoted, applied, verified, versioned and retired without repeatedly reinventing the same decisions.

## Mission

Make strong engineering the default across repositories while keeping permanent agent context small and product-specific freedom high.

```text
Engineering Handbook
        ↓
small global instructions
        +
small repo-local instructions
        +
one generic on-demand handbook router
        ↓
current task
        ↓
load only the relevant Policy / Standard / Pattern / Playbook / Reference
```

## Core principles

- **Reuse first. Search before build.**
- **Canonical baseline, not ceiling.** Mature products can discover stronger practice; validate and promote it upward.
- **Truthful engineering.** Never simulate confidence or production capability that does not exist.
- **Single source of truth.** One active canonical normative artifact per topic.
- **Evidence before claims.** A gate passed only if it was actually executed and observed.
- **Production-minded, not speculative.** Complexity requires a current reason.
- **No silent scope creep.** Keep changes narrow and reviewable.
- **No documentation cemetery.** Create categories only when a real artifact exists.
- **Automate stable rules, not opinions.** Enforcement follows demonstrated value.
- **Repo-local identity stays local.** Brand, product workflow and domain decisions are not homogenized by the handbook.

## Taxonomy and precedence

| Kind | Purpose | Normative? |
|---|---|---|
| Governance | authority, precedence, lifecycle, promotion | yes |
| Policy | mandatory cross-repository behavior | yes |
| Standard | technical baseline for a defined scope | yes |
| Pattern | reusable solution | no unless referenced normatively |
| Playbook | repeatable procedure | no unless referenced normatively |
| Reference | evidence/research | no |
| Template | reusable starting artifact | only when explicitly required |
| Executable asset | script/rule/hook/CI/gate/skill | enforces or assists stable rules |
| Decision | durable historical choice | records rationale/authority |

Precedence:

```text
external non-negotiable obligation
→ Handbook Governance
→ active Policy
→ active Standard
→ permitted repo-local decision/exception
→ Pattern
→ Playbook
→ Reference/research
```

## Engineering baselines

### Architecture, data and capability truth

Use:

- `policies/truthful-engineering.md`;
- `standards/architecture-data-integrity-baseline.md`;
- `patterns/source-of-truth-boundaries.md`;
- `patterns/capability-environment-integrity.md`;
- `playbooks/architecture-data-review.md`.

Key ideas: name authoritative owners, keep domain invariants out of incidental UI state, protect history/integrity, treat migrations as production state changes, and do not extract generic cores before real consumers validate the abstraction.

### Security and identity

Use:

- `standards/security-identity-baseline.md`;
- `patterns/authorization-privileged-boundaries.md`;
- `patterns/token-secret-link-handling.md`;
- `playbooks/security-review.md`.

Authentication and authorization are separate. Protected operations validate permissions at a server/data boundary. Privileged credentials stay out of client code. Bearer links/tokens are credentials. OWASP ASVS is used proportionally as a verification catalog.

### Testing, CI/CD and release integrity

Use:

- `standards/testing-release-quality-baseline.md`;
- `patterns/risk-based-verification-matrix.md`;
- `patterns/release-provenance-environment-gates.md`;
- `playbooks/quality-release-review.md`.

Test the failure class, not the fashionable tool. A green CI run proves only its configured gates. Build, deployment, migrations, post-deploy smoke and native/manual checks remain distinct evidence states.

### Production operability

Use:

- `standards/production-operability-baseline.md`;
- `patterns/observability-signals.md`;
- `playbooks/production-readiness-review.md`.

Choose logs, metrics, traces, synthetics and domain health because they answer operational questions. OpenTelemetry is optional; if used, prefer relevant stable semantic conventions. Do not create decorative dashboards or report unknown data as zero.

### Dependencies and supply chain

Use `standards/dependency-supply-chain-baseline.md`.

Lock dependency resolution where the ecosystem supports it, evaluate meaningful dependencies, keep privileged CI least-privileged, and prefer immutable full-SHA references for third-party GitHub Actions. OpenSSF Scorecard is a signal, not a magic threshold. SBOMs, signing and attestations are risk/distribution-driven rather than universal ceremony.

### APIs and integration contracts

Use `patterns/api-contract-evolution.md` when independent consumers make interface drift expensive. OpenAPI is the preferred formal description for HTTP APIs when a formal contract is warranted; it is not required for every internal route.

### Performance

Use `patterns/performance-budgeting.md`.

Measure representative user/product constraints and define repo-specific budgets only where repeated regression risk justifies them. Core Web Vitals are useful web signals, not the complete performance definition for every product.

### UI/UX and frontend quality

Use:

- `standards/ui-ux-quality-baseline.md`;
- `playbooks/frontend-quality-review.md`;
- `patterns/mobile-responsive-interaction.md` when physical mobile constraints matter;
- `patterns/visual-evidence-integrity.md` when rendered evidence supports acceptance.

The handbook does **not** prescribe a component library, dashboard grammar, palette, radius, CSS framework or common art direction. Quality is the floor; product character is repo-local.

### PWA

Use `standards/web-pwa-baseline.md`. PWA is capability-driven and scoped to the surface that gains value. Service worker/offline/push are not mandatory badges.

## Donor evidence

Two references preserve the internal evidence that created the first product-quality baselines:

- `references/internal-ui-pwa-donor-audit.md`;
- `references/internal-engineering-donor-audit.md`.

They audit CCSE-AI-Coach, Aluminio Bartra, COGOP Barcelona Attendance and MovOps OS. Donor choices are evidence, not automatic norms: provider/product details are removed and relevant primary sources challenge the reusable principle before promotion.

## Default task flow

1. Read the consumer repo's applicable `AGENTS.md` and repo-local decisions.
2. Search the current repo.
3. Search the handbook.
4. For transversal/quality-sensitive decisions, compare relevant mature internal donors when doing so may materially improve the result.
5. Evaluate external mature/primary solutions when needed.
6. Design new only when reuse/adaptation does not fit.
7. Verify the risks relevant to the changed scope and disclose meaningful unrun gates.

Use `playbooks/engineering-change.md` as the proportional workflow and `policies/reuse-first.md` for the search contract.

## Repositories and knowledge promotion

A repository-level `AGENTS.md` contains verified local facts: purpose, commands, architecture boundaries, product/domain decisions and local gates. It should not duplicate universal handbook prose.

Use `playbooks/repository-adoption.md` and `templates/AGENTS.repo.md`.

Validated repo learning may be promoted through `governance/knowledge-promotion.md`. The handbook is the current approved baseline, not proof that every existing implementation is weaker.

## Source, distribution and runtime

Keep three layers distinct:

```text
AUTHORITATIVE SOURCE
handbook + repo-local canonical docs
        ↓
GENERATED / INSTALLED ARTIFACTS
Codex global config and generic handbook references
        ↓
RUNTIME CONTEXT
only material actually loaded for the current task
```

The installed global `AGENTS.md` and installed handbook references are generated distribution artifacts, not second sources of truth.

## Codex adoption

Canonical global instructions: `agent-config/codex/AGENTS.global.md`.

Canonical generic handbook router: `agent-config/codex/skills/engineering-handbook/SKILL.md`.

There are **no domain-specific UI/security/architecture/etc. skills**. Engineering knowledge remains ordinary governed handbook artifacts; the single generic router only helps progressive disclosure.

Distribution scripts:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Check
```

Use the corresponding adoption playbooks/ADRs before installation changes.

## Handbook integrity

Run:

```powershell
pwsh -File .\automation\handbook\check-integrity.ps1
```

The checker validates structural invariants such as catalog IDs/paths, frontmatter/source references and skill bundle integrity. It is intentionally not a generic repo-doctor.

## External source baseline

Primary/official authority is preferred. Important current anchors include:

- NIST SP 800-218 / SSDF v1.1 as the final general SSDF baseline; SSDF v1.2 is tracked as draft until finalized;
- OWASP ASVS 5.0.0 plus applicable OWASP Cheat Sheets;
- W3C WCAG/APG and web platform specs;
- Git/GitHub official documentation;
- OpenTelemetry when telemetry standardization is needed;
- OpenAPI when an HTTP API contract warrants formalization;
- OpenSSF security guidance/Scorecard as supply-chain inputs.

All material sources live in `machine-readable/sources.yaml` and are subject to review dates/volatility.

## Repository map

```text
engineering-handbook/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── governance/
├── policies/
├── standards/
├── patterns/
├── playbooks/
├── references/
├── agent-config/codex/
├── automation/
├── templates/
├── decisions/
└── machine-readable/
```

Start from `governance/handbook-governance.md` when authority/precedence is in question; otherwise load only the artifact that can materially change the task.
