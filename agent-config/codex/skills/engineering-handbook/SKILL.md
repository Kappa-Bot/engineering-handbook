---
name: engineering-handbook
description: Apply Kappa-Bot cross-repository engineering governance and reusable guidance for non-trivial engineering changes, architecture/data, security/identity, testing/CI/release, production readiness/observability, dependencies/supply chain, API contracts, performance, UI/UX/PWA, repository lifecycle/adoption, reuse/search-before-build, verification, and handbook maintenance. Do not use for trivial repo-local edits fully covered by local instructions.
---

# Engineering Handbook

Use this single generic router for progressive disclosure. Prefer the distributed deterministic context runtime over manual handbook loading; do not create domain-specific skills that duplicate handbook content.

## Default hot path

1. Read the consumer repository's applicable `AGENTS.md` and repo-local decisions for local facts, commands, architecture, product/domain constraints and gates.
2. Resolve this skill's sibling `references/` directory. It contains the distributed runtime at `automation/engineering_context` and compiled corpus at `machine-readable/compiled`.
3. From that `references/` directory, run one context request for non-trivial work:

   `python -m automation.engineering_context context --repo "<repo-root>" --handbook machine-readable/compiled --mode plan --task "<task>" --metrics`

   Add repeated `--changed <path>` arguments when changed paths are already known.
4. Use `descriptor`, `repo_route`, `capsule` and `planning_ir_seed` as the compact task context. Do not fill unused context budget with extra handbook prose.
5. Read canonical handbook Markdown only when the capsule reports uncovered required risk, bounded uncertainty needs resolution, an escalation asks for canonical guidance, or exact normative/detail context is materially necessary.
6. Before implementation or verification when the risk/scope changed materially, call the same command with `--mode implement` or `--mode verify`; use `--base-context` when a prior capsule is available so only the delta needs attention.
7. Keep repo-local authority and handbook precedence intact. A compiled capsule is a generated projection, never a second source of truth; canonical Markdown wins on conflict.

## Fallback routing

If the distributed runtime is unavailable or cannot classify the task safely, use `references/machine-readable/catalog.yaml` and load only the smallest applicable canonical set. Typical anchors are:

- architecture/data: `std-architecture-data-integrity-baseline`;
- capability truth: `pol-truthful-engineering`;
- security/auth/secrets: `std-security-identity-baseline`;
- testing/release/migrations: `std-testing-release-quality-baseline`;
- production/observability: `std-production-operability-baseline`;
- dependencies/supply chain: `std-dependency-supply-chain-baseline`;
- API contracts: `pat-api-contract-evolution`;
- performance: `pat-performance-budgeting`;
- UI/UX: `std-ui-ux-quality-baseline`;
- PWA: `std-web-pwa-baseline`;
- reuse/search-before-build: `pol-reuse-first`;
- verification claims: `pol-verification-definition-of-done`.

Add a Pattern or Playbook only when it changes the decision or procedure. Do not bulk-read `references/`.

## Context and authority discipline

- `AUTHORITATIVE SOURCE` = canonical handbook Markdown plus permitted repo-local decisions.
- `GENERATED / INSTALLED ARTIFACT` = compiled JSON, installed skill bundle and global Codex config.
- `RUNTIME CONTEXT` = the selected task capsule and repo route.
- Do not turn a Pattern, Playbook, generated unit or external source into a `MUST` unless active Policy/Standard/Governance supports that force.
- Provider/framework/product choices remain repo-local unless deliberately promoted.
- Do not use cross-repository guidance to erase product identity, domain workflow or deliberate local architecture.
- If expected guidance is missing or stale, report the gap rather than inventing handbook authority.

## Handbook maintenance

When editing canonical handbook guidance, keep `agent-context` blocks as compact projections of already-supported meaning; they must not silently create or strengthen rules. Regenerate/check compiled artifacts with:

`python -m automation.engineering_context check --root .`

When a plan, ADR, evaluation or review materially depends on handbook guidance, preserve relevant handbook IDs for traceability. Keep repo-specific conclusions local unless knowledge-promotion rules justify promotion.
