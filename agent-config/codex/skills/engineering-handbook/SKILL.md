---
name: engineering-handbook
description: Apply Kappa-Bot cross-repository engineering governance and reusable guidance to all engineering/repository work. Use the lightweight global + repo-local baseline for trivial edits; use the deterministic context router for non-trivial engineering changes, architecture/data, security/identity, testing/CI/release, production readiness/observability, dependencies/supply chain, API contracts, performance, UI/UX/PWA, dynamic Agency Agents runtime routing, repository lifecycle/adoption, reuse/search-before-build, verification, and handbook maintenance.
---

# Engineering Handbook

Use this single generic router for progressive disclosure. The Handbook governs all repository engineering work, but not every task needs a full context query. Prefer the distributed deterministic context runtime over manual handbook loading; do not create domain-specific skills that duplicate handbook content.

## Default hot path

1. Read the consumer repository's applicable `AGENTS.md` and repo-local decisions for local facts, commands, architecture, product/domain constraints and gates.
2. Apply the small distributed global handbook baseline to every engineering task. For a trivial/mechanical edit whose risk and decision are fully covered by the global baseline plus local instructions, stop here and implement proportionally rather than manufacturing context ceremony.
3. For non-trivial, risky, cross-cutting, ambiguous or quality-sensitive work, resolve this skill's sibling `references/` directory. It contains the distributed runtime at `automation/engineering_context` and compiled corpus at `machine-readable/compiled`.
4. Run one context request:

   `python -m automation.engineering_context context --repo "<repo-root>" --handbook machine-readable/compiled --mode plan --task "<task>" --metrics`

   Add repeated `--changed <path>` arguments when changed paths are already known. The context command fails closed when compiled artifacts are missing, malformed, or stale versus the bundled canonical Markdown; regenerate/fix the corpus rather than bypassing that check.
5. Use `descriptor`, `repo_route`, `capsule` and `planning_ir_seed` as the compact task context. Do not fill unused context budget with extra handbook prose.
6. Read canonical handbook Markdown only when the capsule reports uncovered required risk, bounded uncertainty needs resolution, an escalation asks for canonical guidance, or exact normative/detail context is materially necessary.
7. Before implementation or verification when the risk/scope changed materially, call the same command with `--mode implement` or `--mode verify`; use `--base-context` when a prior capsule is available so only the delta needs attention.
8. Keep repo-local authority and handbook precedence intact. A compiled capsule is a generated projection, never a second source of truth; canonical Markdown wins on conflict.

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
- material design context: `pat-design-context-layering`;
- PWA: `std-web-pwa-baseline`;
- reuse/search-before-build: `pol-reuse-first`;
- verification claims: `pol-verification-definition-of-done`.

Add a Pattern, Playbook or Reference only when it changes the decision or procedure. Do not bulk-read `references/`.

## Dynamic agent runtime routing

Zero spawned workers remains the default.

When delegation could materially improve the result, resolve only this compact routing corpus in addition to normal task-specific context:

- `std-agent-runtime-routing`;
- `pb-agent-runtime-routing`;
- `ref-agency-agents-specialist-routing`;
- `ref-agent-runtime-manifest` only when durable worker/recovery state is warranted;
- `machine-readable/agent-runtime-routing.v1.json`.

Decision order:

```text
deterministic tool/script
→ direct controller execution
→ one Agency Agents specialist
→ second independent specialist only for distinct parallel value or required review
```

Do not route by fixed `parent/design-quality/delivery` roles. Do not bind Luna/Sol/Astra or reasoning effort to persona names.

For frozen bounded implementation with explicit acceptance, existing patterns and strong deterministic verification, prefer the efficient tier (currently Luna) at low/medium effort. For multi-component reasoning/integration/debugging, start around Sol medium/high. Reserve Astra high/xhigh for genuine high-uncertainty/high-impact work; `max` is eval-gated, not a default.

Every spawn sets both model and reasoning effort explicitly where supported. Resolve the real spawn allowlist and record requested/actual values; do not silently inherit or substitute.

Independent review is triggered by the risk boundary. Do not spawn a reviewer for low/medium-risk work already proved by strong deterministic tests/diff inspection. Use independent review for the Standard's security/data/money/Production/public-contract/concurrency/high-impact triggers, routing the reviewer with the same model/effort heuristics rather than defaulting to Astra.

Escalate by cause rather than automatic retry ladders. Environment/provider failures do not justify stronger reasoning; authority ambiguity requires authority resolution; clear defects may return to the same cheap implementer; only actual reasoning insufficiency justifies raising model/effort.

Routine concurrency is zero/one, with at most two concurrent workers unless a distinct contribution clearly outweighs context/coordination cost. Nested spawning is off by default.

## Context and authority discipline

- `AUTHORITATIVE SOURCE` = canonical handbook Markdown plus permitted repo-local decisions.
- `GENERATED / INSTALLED ARTIFACT` = compiled JSON, installed skill bundle and global Codex config.
- `RUNTIME CONTEXT` = selected task capsule and repo route.
- Do not turn a Pattern, Playbook, generated unit or external source into a `MUST` unless active Policy/Standard/Governance supports that force.
- Provider/framework/product choices remain repo-local unless deliberately promoted.
- Do not use cross-repository guidance to erase product identity, domain workflow or deliberate local architecture.
- If expected guidance is missing or stale, report the gap rather than inventing handbook authority.

## Specialist, skill and design-context discipline

`pol-agent-operating-model` owns specialist and skill routing. Use `ref-agency-agents-specialist-routing` when specialist expertise can materially change the result and `std-agent-runtime-routing` to decide whether to spawn plus which model/effort to use.

Use the smallest relevant process/craft skill set and never invoke a large design/motion stack merely because it is installed.

For materially visual work, resolve the product-owned design contract and `pat-design-context-layering` before using external precedents. `ref-external-design-intelligence-corpus` is a discovery/reference source, not a style authority.

When workers are spawned, give each one a compact task-local dispatch and only material deltas afterward. Prefer minimal/isolated context when supported. Mark incompatible profiles/skills `N/A` rather than invoking them performatively. Discover actual agents/models/efforts/skills/MCPs/CLIs/auth/scopes, prefer available playwright-cli for suitable browser exploration, and retain the repository's real test gates. Avoid duplicate tool actions and respect the cost ceiling.

## Handbook maintenance

When editing canonical handbook guidance, keep `agent-context` blocks as compact projections of already-supported meaning; they must not silently create or strengthen rules. Regenerate/check compiled artifacts with:

`python -m automation.engineering_context check --root .`

When a plan, ADR, evaluation or review materially depends on handbook guidance, preserve relevant handbook IDs for traceability. Keep repo-specific conclusions local unless knowledge-promotion rules justify promotion.
