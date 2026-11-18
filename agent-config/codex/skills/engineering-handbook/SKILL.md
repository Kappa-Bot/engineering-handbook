---
name: engineering-handbook
description: Use when working in Kappa-Bot repositories on engineering, architecture/data, security, testing/release, operations/dependencies, APIs, UI/UX/PWA, Unslop/redesign, Modern Web Guidance/native browser features, Ponytail/refactoring, custom agents or connected CRM/websites, public-site SEO, marketing/copy/CRO, leads/conversion measurement, agent routing, adoption or Handbook maintenance.
---

# Engineering Handbook

Use this single generic router for progressive disclosure. The Handbook governs all repository engineering work, but not every task needs a full context query. Prefer the distributed deterministic context runtime over manual handbook loading; do not create domain-specific skills that duplicate handbook content.

## Default hot path

1. Read the consumer repository's applicable `AGENTS.md` and repo-local decisions for local facts, commands, architecture, product/domain constraints and gates.
2. Apply the small distributed global handbook baseline to every engineering task. For a trivial/mechanical edit whose risk and decision are fully covered by the global baseline plus local instructions, stop here and implement proportionally rather than manufacturing context ceremony.
3. For non-trivial, risky, cross-cutting, ambiguous or quality-sensitive work, resolve this skill's sibling `references/` directory. It contains the distributed runtime at `automation/engineering_context` and compiled corpus at `machine-readable/compiled`.
4. Run one context request **with that `references/` directory as the working directory**, not the consumer repository. Pass the consumer's absolute path to `--repo`:

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
- material HTML/CSS/client-side behavior, native dialogs/forms/tables, browser support/fallbacks: `pb-modern-web-platform-workflow` (pinned guide locators, no CLI installation required);
- custom product agents, internal CRM/API or connected public websites: `ref-connected-product-resource-map` (local stack and boundary owners, not another architecture);
- Modern Web Guidance or Ponytail source evaluation: `ref-modern-web-ponytail-adoption` (immutable source/resource paths, licenses, adaptations and execution/privacy review);
- material design, Unslop/anti-slop or redesign: `std-ui-ux-quality-baseline`, `pat-design-context-layering` and `pb-frontend-quality-review`;
- long-form web documents, live contents, citation and reading continuity: `pat-editorial-reading-navigation`;
- interruptions, mixed-input disclosures or search, and theme paint/contrast: `pat-interaction-continuity`;
- design fit and confirmed operation feedback in forms/collections: `pb-frontend-quality-review`;
- authenticated MelodIQ console theme/sidebar/route interactions: `pat-operator-console-shell-interactions` (after repo-local `DESIGN.md`);
- public marketing/client website hero, first-viewport or animated headline: `pat-public-marketing-hero-motion` (after repo-local design and commercial facts);
- public client-site testimonials, Google-inspired review marquees, or fictional review demos: `pat-public-client-reviews-marquee` (after repo-local design, review provenance and publication state);
- marketing context, copy/CRO, competitor evidence or sales collateral: `pb-marketing-context-and-content` (reuse the approved local brief; template only for material gaps);
- prospecting, lead qualification, RevOps or outbound drafts: `pb-lead-qualification-and-handoff` (channel permission is separate from contact quality; no automatic sending);
- conversion tracking/attribution or A/B experiments: `pb-conversion-measurement-and-experiments` (real outcomes, consent, deduplication and destination evidence);
- SEO, AI-search observations, schema markup or site architecture: `std-public-web-discoverability-baseline` and `pb-public-web-discoverability-launch` (preserve noindex/private gates);
- PWA: `std-web-pwa-baseline`;
- reuse/search-before-build, Ponytail/minimum-complete change, simplification/refactoring/code audit: `pol-reuse-first` (trace all relevant consumers; no line/test quota or safety cuts);
- verification claims: `pol-verification-definition-of-done`.

Add a Pattern, Playbook or Reference only when it changes the decision or procedure. Do not bulk-read `references/`.

The new methods are active in existing Policy/Standard owners even when not named in a task. Modern web lookup uses the workflow's immutable upstream links and full guide directory; the bundle contains the local synthesis/locators, not an executable third-party plugin or a vendored guide corpus. Read only the relevant complete guide and current support evidence. Follow `ref-modern-web-ponytail-adoption` rather than running an upstream `@latest`/install/hook command. Backend-only work, licensing research and copy fixes do not authorize browser modernization. A classifier match selects guidance, never write/release permissions.

## Dynamic agent runtime routing

Zero spawned workers remains the default. Delegation is enabled for a task only when the user expressly asks for subagents/parallel agent work or applicable repository/skill instructions request it. An authorized engineering change alone is not delegation consent.

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

For substantive engineering, use Sol 6.2/high as the starting point when available; Sol/xhigh for difficult integration or debugging, and Astra 6.2/high–xhigh for complex architecture, security, data or adversarial reasoning. Use Luna/high for frozen bounded work; Terra 6.1/high for actual visual/browser work only when that client supports it. `medium` is available for strongly specified, verifiable work. `max` remains evidence-gated, not a default. Do not import paid model tiers or extra provider costs under this change.

Every spawn sets both model and reasoning effort explicitly where supported. Resolve the real Codex client/spawn allowlist and native custom agent-file overrides; the custom TOML `model`/`model_reasoning_effort` may outrank even an explicit spawn. Do not confuse Agency Agents personas with installed native Codex agent types, or use CLI config keys for Responses/Agents API. Record requested/actual values; do not silently inherit or substitute.

Independent review is triggered by the risk boundary. Do not spawn a reviewer for low/medium-risk work already proved by strong deterministic tests/diff inspection. Use independent review for the Standard's security/data/money/Production/public-contract/concurrency/high-impact triggers, routing the reviewer with the same model/effort heuristics rather than defaulting to Astra.

Escalate by cause rather than automatic retry ladders. Environment/provider failures do not justify stronger reasoning; authority ambiguity requires authority resolution; clear defects may return to the same implementer. More model effort is valid **upfront** for complex work; later increases need a changed reasoning/risk assessment, not an arbitrary retry.

Routine concurrency is zero/one, with at most two spawned workers unless the owner explicitly authorizes another cap. Nested spawning is off by default. Give workers adequate task-local context; follow the Standard's expanded advisory dispatch/handoff budgets, not the October low-token profile.

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

For materially visual work, use the integrated Unslop method owned by `std-ui-ux-quality-baseline` and operationalized by `pb-frontend-quality-review`; resolve product context through `pat-design-context-layering`. In an authorized redesign, replace weak historical composition/tokens and update the local contract instead of treating it as immutable. Follow diagnosis, product direction, nine-pass dispositions and real rendered acceptance; missing required evidence remains incomplete. Narrow fixes and audits do not authorize reconstruction. External design references supply evidence, not a universal skin or a second router.

When workers are spawned, give each one a compact task-local dispatch and only material deltas afterward. Prefer minimal/isolated context when supported. Mark incompatible profiles/skills `N/A` rather than invoking them performatively. Discover actual agents/models/efforts/skills/MCPs/CLIs/auth/scopes, prefer available playwright-cli for suitable browser exploration, and retain the repository's real test gates. Avoid duplicate tool actions and respect the cost ceiling.

## Handbook maintenance

When editing canonical handbook guidance, keep `agent-context` blocks as compact projections of already-supported meaning; they must not silently create or strengthen rules. From the canonical Handbook root, regenerate and then check compiled artifacts with:

`python -m automation.engineering_context compile-handbook --root . --output machine-readable/compiled`

`python -m automation.engineering_context check --root .`

When a plan, ADR, evaluation or review materially depends on handbook guidance, preserve relevant handbook IDs for traceability. Keep repo-specific conclusions local unless knowledge-promotion rules justify promotion.
