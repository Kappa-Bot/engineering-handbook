# Engineering Handbook

The Engineering Handbook is the canonical engineering knowledge and operating-system repository for Kappa-Bot products.

Its purpose is to turn engineering learning into a governed system that can be discovered, challenged, promoted, applied, verified, versioned and retired without repeatedly reinventing the same decisions.

## Mission

Make strong engineering the default across repositories while keeping permanent agent context small and product-specific freedom high.

```text
canonical Handbook Markdown
        ↓
small global + repo-local instructions
        ↓
explicit agent-context projections
        ↓
deterministic compiled corpus
        ↓
single generic handbook router
        ↓
repo profile + current task descriptor
        ↓
minimal phase-specific context capsule
        ↓
canonical Markdown only when escalation/detail requires it
```

The compiled corpus is a generated projection for routing and planning efficiency. It is **not** a second source of truth: canonical Markdown and permitted repo-local decisions retain authority.

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
- **Unused context budget is a feature.** Do not load guidance merely because token capacity remains.

## Deterministic agent context

Key canonical pages may contain a fenced `json agent-context` block that projects only the smallest planning/implementation/verification units needed by agents. Those blocks must express meaning already supported by the page; they cannot create or strengthen authority.

`automation/engineering_context` compiles those projections into `machine-readable/compiled/` and provides deterministic repo profiling, task description, risk coverage, routing, Planning IR and conformance helpers.

Useful commands:

```text
python -m automation.engineering_context check --root .
python -m automation.engineering_context profile-repo --repo <repo>
python -m automation.engineering_context context --repo <repo> --handbook machine-readable/compiled --mode plan --task "<task>" --metrics
```

The `context` command returns a compact task descriptor, repo route, phase-specific capsule and Planning IR seed. If a required risk is uncovered or bounded uncertainty remains material, the agent escalates to canonical guidance rather than fabricating certainty.

Default context budget is intentionally bounded; real-corpus regression tests require representative security, visual/accessibility, migration, agent-tooling and supervised-learning scenarios to remain below 600 estimated tokens while covering their directly inferred risks. Static capsule estimates are not provider-measured token usage or proof of cost savings.

### Selective ECC adoption

The original **Affaan Mustafa / ECC** is a pinned workflow reference, not a replacement Handbook or a blanket plugin installation. See [the adoption assessment](references/ecc-adoption-assessment.md) for the capability-by-capability comparison and [ADR 0007](decisions/0007-selective-ecc-handbook-adoption.md) for the decision and rollout boundary.

Useful deltas live in the existing canonical owners: verification/release evidence, safe browser QA and comparable visual baselines, agent-tool supply-chain review, supervised knowledge promotion, and controlled agent-workflow evaluation. Agency Agents remains the specialist catalog; the single generic router, explicit runtime/cost policy and product-owned design decisions remain intact.

Changes to agent configurations/plugins/hooks/MCP route a compact execution-boundary check; learning/memory work routes a reviewed-promotion check. Ordinary React hooks, webhooks, server memory defects and documentation typos do not pull in this guidance merely through ambiguous keywords. No observer, scheduled model call, MCP server or native plugin is installed by consuming the documentation. Existing consumers require their normal authorized bundle refresh before the new source is effective.

### Selective Marketing Skills adoption

The pinned [Marketing Skills assessment](references/marketing-skills-adoption-assessment.md) and [ADR 0008](decisions/0008-selective-marketing-skills-adoption.md) adopt twelve prioritized workflows as original, scoped Handbook procedures, not twelve competing skills or a plugin installation:

- [Marketing context and content](playbooks/marketing-context-and-content.md): audience, offer, proof, voice, CRO, competitor evidence and sales collateral; reuse the local brief, optionally seeded by [the context template](templates/product-marketing-context.md).
- [Lead qualification and handoff](playbooks/lead-qualification-and-handoff.md): sourced fit/priority, existing CRM ownership/stages, and a separate Spain/EU channel-permission gate.
- [Conversion measurement and experiments](playbooks/conversion-measurement-and-experiments.md): confirmed outcomes, consent/data minimization, deduplication, destination evidence and honest low-traffic decisions.

SEO, AI-search observations, site architecture, design and website delivery remain with their existing canonical owners. The single router selects compact context for the actual task; currency conversion, database schema, code review and private-console glass work do not become marketing tasks. Product facts and private business records stay local. No campaign, sending, paid tool, account, schedule or consumer installation follows from source publication; existing consumers use their normal authorized bundle refresh.

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
- `playbooks/public-client-website-delivery.md` for the complete public service/client-site flow: proposition, image prompts and desktop/mobile assets, hero, header CTAs, gallery, review truth modes, lead form and verified deployment;
- `standards/public-website-legal-trust-baseline.md` for public/client demos and launches: legally accountable identity, sector-specific health advertising, RGPD/cookies, third-party embeds, AI media disclosure, reviews and launch sign-off;
- `playbooks/spanish-client-website-privacy-consent-audit.md` for Spanish SME service sites with contact/quote forms and no checkout: actual controller/vendor roles, form notices, cookies/analytics, AI and technical/owner gates; use `templates/spanish-client-website-legal-evidence-pack.md` per client and `references/spain-sme-lead-web-legal-research-2026-11.md` for sourced legal distinctions and evidence limits;
- `patterns/mobile-responsive-interaction.md` when physical mobile constraints matter;
- `patterns/operator-console-shell-interactions.md` for reusable theme, sidebar and route-continuity mechanics in authenticated MelodIQ operator consoles;
- `patterns/public-marketing-hero-motion.md` for public/client site first-viewport composition, image/CTA hierarchy and optional Tommy Jepsen-style rotating-word hero motion;
- `patterns/public-service-gallery-selector.md` for @minhxthanh-inspired expanding service-photo panels, mobile scroll-snap, keyboard selection and truthful image provenance;
- `patterns/public-client-reviews-marquee.md` for the approved Google-inspired, demo-safe testimonials marquee (two-row or single-row), source attribution, pause/motion and adoption checks;
- `patterns/visual-evidence-integrity.md` when rendered evidence supports acceptance.

The handbook does **not** prescribe a component library, dashboard grammar, palette, radius, CSS framework or common art direction. Quality is the floor; product character is repo-local.

### Public search presence, SEO and brand

For corporate marketing, public vertical product landings and client/lead websites, use:

- `standards/public-web-discoverability-baseline.md` for indexation, crawl/metadata, truthful entity signals and Agent Discoverability (HTTP Link, negotiated Markdown, conditional DNS-AID);
- `playbooks/public-web-discoverability-launch.md` for an executable per-site audit → identity/visual direction → implementation → release → Search Console monitoring workflow.

A private CRM, demo or prelaunch page does **not** become indexable merely because public SEO is desirable. Domain, legal identity, brand, client facts, launch gate, screenshots and art direction stay with the owning repository; the handbook provides a common quality floor, not identical websites or guaranteed Google rankings.

### Organic search delivery as a service

For MelodIQ Systems' **cross-sector Spanish SME SEO/AEO/GEO/LLMO delivery**, use [the organic search service operating system](playbooks/search-visibility-service-operations.md) alongside the existing canonical [public discoverability Standard](standards/public-web-discoverability-baseline.md) and [technical launch playbook](playbooks/public-web-discoverability-launch.md). It covers discovery, risk/permissions, audit, commercial search intent, local profiles, content, AI-answer sampling, QA, publication, reporting and handoff without duplicating technical authority.

Reusable, **client-workspace-only** templates: [delivery workbook](templates/search-visibility-client-workbook.md), [commercial proposal](templates/search-visibility-commercial-offer.md), and [monthly report](templates/search-visibility-monthly-report.md). The [research and myth corrections](references/search-visibility-research-2026-11.md) and [Spain pricing evidence](references/search-visibility-pricing-spain-2026-11.md) are **non-normative**: published agency prices are not approved MelodIQ tariffs, and AI visibility is not a guaranteed search outcome. No client credentials, domain changes, paid tools, analytics, account creation or publication are authorized by reading these documents.

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
3. For non-trivial cross-repository guidance, use the generic handbook router and its compiled context runtime when available.
4. Escalate from the compact capsule to canonical Markdown only when required risk, uncertainty or exact normative detail warrants it.
5. For transversal/quality-sensitive decisions, compare relevant mature internal donors when doing so may materially improve the result.
6. Evaluate external mature/primary solutions when needed.
7. Design new only when reuse/adaptation does not fit.
8. Verify the risks relevant to the changed scope and disclose meaningful unrun gates.

Use `playbooks/engineering-change.md` as the proportional workflow and `policies/reuse-first.md` for the search contract.

## Repositories and knowledge promotion

A repository-level `AGENTS.md` contains verified local facts: purpose, commands, architecture boundaries, product/domain decisions and local gates. It should not duplicate universal handbook prose.

Use `playbooks/repository-adoption.md` and `templates/AGENTS.repo.md`.

Validated repo learning may be promoted through `governance/knowledge-promotion.md`. The handbook is the current approved baseline, not proof that every existing implementation is weaker.

## Source, distribution and runtime

Keep three layers distinct:

```text
AUTHORITATIVE SOURCE
canonical handbook Markdown + permitted repo-local decisions
        ↓
GENERATED / INSTALLED ARTIFACTS
compiled corpus + Codex global config + generic skill bundle
        ↓
RUNTIME CONTEXT
repo profile + task descriptor + only selected phase capsule
```

`machine-readable/compiled/` is generated from explicit structured projections inside canonical pages. The generic skill distributes both this corpus and the small Python runtime, so a consumer repo can obtain task-specific context without bulk-reading handbook documents.

A compiled hash is useful provenance/invalidation data, not authority. If generated output and canonical Markdown conflict, canonical source wins and the generated artifact must be corrected.

## Codex adoption

Canonical global instructions: `agent-config/codex/AGENTS.global.md`.

Canonical generic handbook router: `agent-config/codex/skills/engineering-handbook/SKILL.md`.

Agency Agents is the default upstream specialist-persona catalog for Codex engineering work. The Handbook does **not** impose permanent `parent/design-quality/delivery` roles or model-by-job-title bindings. Runtime routing chooses tool vs direct execution vs specialist spawn, then selects model and reasoning effort independently from task uncertainty, impact, verification and context cost. See `standards/agent-runtime-routing.md` and `references/agency-agents-specialist-routing.md`.

There are **no domain-specific UI/security/architecture/etc. skills**. Engineering knowledge remains ordinary governed handbook artifacts; the single generic router uses the deterministic compiled runtime for the normal hot path and canonical pages for escalation.

Distribution scripts:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Check
```

Use the corresponding adoption playbooks/ADRs before installation changes.

## OpenDesign local design studio (optional)

For visual prototypes, corporate presentation templates and derivative design-system packages, use `pb-open-design-local-adoption`. The first offline corporate kit is at `brands/melodiq-systems/open-design/`, with a compatible 56-token design-system snapshot and an editable A4 commercial draft.

This is a **local-file pilot**: no restricted logos, provider credentials, paid media services, write-capable MCP or OpenDesign-launched Codex are installed or authorized by the Handbook. On Windows/WSL, OpenDesign's Codex launcher can request `danger-full-access`; do not treat its local workspace as a sandbox.

Product and tenant visual authority stays with each consumer repository. An OpenDesign prototype is not released product evidence.

## Handbook integrity

Run both context freshness and structural integrity checks:

```text
python -m automation.engineering_context check --root .
```

```powershell
pwsh -File .\automation\handbook\check-integrity.ps1
```

The Python check enforces deterministic compilation, byte stability and checked-in freshness. The PowerShell checker validates catalog IDs/paths, frontmatter/source references and skill bundle integrity. Neither replaces semantic review.

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
│   └── engineering_context/
├── tests/engineering_context/
├── templates/
├── decisions/
└── machine-readable/
    └── compiled/
```

Start from `governance/handbook-governance.md` when authority/precedence is in question; otherwise prefer the compact compiled route and load canonical artifacts only when they can materially change the task.
