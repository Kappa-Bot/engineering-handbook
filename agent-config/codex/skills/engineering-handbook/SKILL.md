---
name: engineering-handbook
description: Apply Kappa-Bot cross-repository engineering governance and reusable guidance for non-trivial engineering changes, architecture/data, security/identity, testing/CI/release, production readiness/observability, dependencies/supply chain, API contracts, performance, UI/UX/PWA, repository lifecycle/adoption, reuse/search-before-build, verification, and handbook maintenance. Do not use for trivial repo-local edits fully covered by local instructions.
---

# Engineering Handbook

Use this single generic router to load only the installed handbook references relevant to the current task. Do not bulk-read the bundle and do not create domain-specific skills that duplicate handbook content.

## Operating sequence

1. Read the repository's applicable `AGENTS.md` and repo-local decisions for local facts, commands, architecture, product/brand/domain constraints and gates.
2. Identify the cross-repository question that can materially change the work.
3. Load only the relevant files under `references/`; use `references/machine-readable/catalog.yaml` for canonical IDs/paths.
4. Apply handbook precedence rather than treating every artifact as equally normative.
5. Keep external facts, internal decisions, implementation, verification and adoption distinct when it affects claims.
6. If expected guidance is missing or stale, report the gap rather than inventing handbook authority.

## Routing guide

- **Non-trivial engineering change:** `references/playbooks/engineering-change.md` plus only affected baselines.
- **Architecture / persistence / data model / reusable-core extraction:** `references/standards/architecture-data-integrity-baseline.md`, `references/playbooks/architecture-data-review.md`; add source-of-truth/capability patterns when relevant.
- **Demo/mock/Preview/Production capability boundary:** `references/policies/truthful-engineering.md` and `references/patterns/capability-environment-integrity.md`.
- **Security / auth / permissions / secrets / access links:** `references/standards/security-identity-baseline.md` and `references/playbooks/security-review.md`; add authorization/token patterns as needed.
- **Testing strategy / CI / migrations / deployment / release:** `references/standards/testing-release-quality-baseline.md` and `references/playbooks/quality-release-review.md`; add risk/provenance patterns as needed.
- **Production readiness / operations / observability:** `references/standards/production-operability-baseline.md` and `references/playbooks/production-readiness-review.md`; add `references/patterns/observability-signals.md` when telemetry is in scope.
- **Dependencies / GitHub Actions / supply chain:** `references/standards/dependency-supply-chain-baseline.md`.
- **HTTP API contract / compatibility:** `references/patterns/api-contract-evolution.md`.
- **Performance / regression budget:** `references/patterns/performance-budgeting.md`.
- **UI/UX / visual frontend work:** `references/standards/ui-ux-quality-baseline.md` and `references/playbooks/frontend-quality-review.md`; add mobile/visual-evidence patterns only when relevant.
- **PWA / installability / offline/update behavior:** `references/standards/web-pwa-baseline.md`; add mobile/visual patterns as needed.
- **Reuse / search-before-build:** `references/policies/reuse-first.md`.
- **External library/framework/service/reference:** `references/playbooks/external-solution-evaluation.md`, `references/governance/source-authority.md`, `references/policies/reuse-first.md`.
- **New repository:** `references/playbooks/new-repository-bootstrap.md`, then repository adoption/template.
- **Repository adoption / AGENTS.md:** `references/playbooks/repository-adoption.md` and `references/templates/AGENTS.repo.md`.
- **Git/workspace:** `references/policies/workspace-git-hygiene.md`.
- **Verification / completion claims:** `references/policies/verification-definition-of-done.md` plus any affected domain Standard.
- **Durable technical decision:** read repo-local architecture first, then `references/templates/decision.md`.
- **Source trust/licensing/evidence:** `references/governance/source-authority.md`.
- **Promoting project learning:** `references/governance/knowledge-promotion.md` and the relevant donor audit when useful.
- **Editing handbook:** `references/CONTRIBUTING.md` plus affected governance/policy.
- **Codex distribution/adoption:** relevant playbook/ADR only.

## Context discipline

- Never bulk-read `references/` merely because the router activated.
- Prefer one playbook plus the smallest supporting Policy/Standard/Pattern set that can change the decision.
- Do not copy handbook prose into repo-local instructions/plans/ADRs when a canonical reference suffices.
- Do not turn a Pattern, Playbook or external source into a `MUST` unless active governance/Policy/Standard supports that force.
- Provider/framework/product choices remain repo-local unless deliberately promoted as a Standard.
- Do not use cross-repository guidance to erase product identity, domain workflow or deliberate local architecture.

## Durable outputs

When a plan, ADR, evaluation or review materially depends on handbook guidance, name the relevant handbook artifact IDs/paths for traceability.

Keep repo-specific conclusions local unless `references/governance/knowledge-promotion.md` justifies promotion.
