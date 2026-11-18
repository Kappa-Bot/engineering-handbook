---
id: std-agent-runtime-routing
kind: standard
status: active
owner: engineering
version: "2.0"
applies_to:
  - all-repositories
  - codex
  - multi-agent-execution
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
  - src-openai-models
  - src-openai-reasoning
  - src-openai-model-selection
  - src-openai-codex-subagents
  - src-openai-codex-config-reference
  - src-openai-responses-multi-agent
  - src-openai-agents-api-multi-agent
  - src-agency-agents
last_verified: 2026-11-18
review_due: 2027-02-18
supersedes:
  - std-owner-authorized-role-pods
---

# Agent Runtime Routing

## Purpose and November 2026 quality-first revision

Maximize **verified engineering quality and task completion inside the owner's actual authorization and monetary ceiling**. Reasoning depth and context are resources to invest when they improve analysis, implementation, review or recovery; minimizing tokens per worker is no longer the primary goal. Prevent avoidable duplication, but do not downgrade a complex task merely to save reasoning tokens.

The October 2026 low-effort/economy experiment (revision 1.1) is superseded for **new** work. The 2026-11-18 owner direction allows materially higher reasoning effort and token use, while retaining the existing prohibition on **additional monetary charges without authorization**, no automatic GitHub Actions dependency and no requirement to multiply agents. The expanded default is Sol/high; Luna/high remains useful for bounded, repeatable work, and Astra/high–xhigh is normal for genuinely difficult decisions rather than an exception requiring a failed cheap run. This is a task-routing choice, not evidence that any provider entitlement or workstation has changed.

This remains the single normative routing document. The JSON profile is its machine-readable projection; the playbook explains adoption. Historical fixed parent/design-quality/delivery role pods remain superseded.

## Authority and sensitive boundaries

```text
external non-negotiable obligation
→ Handbook Governance / Policy / Standard
→ permitted repo-local authority
→ approved task/spec/plan
→ runtime routing decision
→ Agency Agents persona / optional process method
```

A persona, model, reasoning setting or scope instruction never grants provider, Production, billing, credential, destructive-action or customer-data authority. A written read-only scope is not proof of a separate runtime permission sandbox. The controller must preserve the actual tool permission boundary.

## Spawn value and topology

Use zero spawned workers by default. **Availability is not authorization to spawn.** In current local Codex, delegation is triggered by an explicit user request or an applicable repository/skill instruction asking for delegation; a general request to edit a project alone does not activate it. Once a particular initiative authorizes delegation, do not ask for approval at every routine spawn within its scope. Choose the first adequate route:

1. an existing deterministic tool or script;
2. the current controller with its existing context;
3. one Agency Agents specialist;
4. a second specialist for a distinct independent workstream or required independent review.

A spawn needs at least one material advantage: specialist expertise; clean context for a cohesive workstream; isolation of large research/test logs; genuinely independent parallel work; or required review independence. A matching profile alone is insufficient. A delegated initiative retains its justified independent work/review; quality is not improved by ceremonial agent proliferation.

Agency Agents remains the specialist catalog. Select its narrowest relevant current profile and record its observed revision. Persona, model and effort are separate choices. The controller can use a profile directly when no separate worker is useful. `Agents Orchestrator` is optional; upstream mandatory ceremony, per-task QA swarms or repeated retries are not Handbook authority.

Normal staffing is one worker per cohesive responsibility, with the owner-preferred cap of **two concurrent subagents**. More needs explicit authorization and the client must support the cap; do not confuse a concurrency limit with a requirement to spawn two. Nested spawning is off by default; only the controller routes workers unless current repository authority explicitly permits otherwise. Do not create one agent per file, test, finding or checklist row. Reuse a worker for its cohesive responsibility while context remains reliable; serialize shared-file writes and require disjoint ownership for parallel writes.

No repeated owner confirmation is needed for a spawn already inside the authorized task, included usage and permissions. A paid-model purchase, new provider permission or another sensitive action still needs its separate authority.

## Material routing dimensions

Classify only what changes the decision:

| Dimension | Values |
| --- | --- |
| Decision uncertainty | low: specified result/method; medium: choices within stable semantics; high: unresolved architecture/behavior/trade-offs |
| Dependency breadth | local; repository; cross-system |
| Impact and reversibility | low; medium; high: auth, tenancy, durable data, money, public contracts or Production; critical: irreversible/broad consequences |
| Verification strength | strong: material failure classes directly tested; partial; weak |
| Context-transfer cost | low; medium; high |

Do not manufacture numerical precision. A repository's importance or an impressive persona name is not a reason for an expensive model.

## Task-aware model and reasoning selection

Start everyday nontrivial engineering and integration at **`gpt-6.2-sol` / `high`** when the actual Codex client and account expose it. Increase to `xhigh` for complex multi-component debugging, migrations and high-coupling verification. For demanding architecture, authorization, data integrity or adversarial review, **`gpt-6.2-astra` / `high` or `xhigh` is an ordinary justified route**, not a last-resort reward for failed cheaper attempts. This is an organizational preference, not an assertion that higher effort always improves every task.

For **frozen material semantics, bounded scope and strong verification**, `gpt-6-luna` / `high` is a focused worker alternative. The gate requires explicit acceptance, an existing pattern or specified method, bounded writable scope, no unresolved architecture/security/data-contract decision, reversible or contained impact, tests covering likely failure classes, and no sensitive external action delegated. `medium` is permitted for truly mechanical edits with equally strong checks, but `low` is no longer the default for an engineering delegate.

Use `gpt-6.1-terra` / `high` as an optional specialist for browser/native-app interaction and visual inspection **only where the client and its spawn allowlist actually support it**; when unsupported, use an available Sol/Astra model with real visual tools. `gpt-6.1-sol` / `high` is a compatibility fallback when newer Sol is not exposed in a particular client (for example IDE); it is not a silent downgrade. Native tool availability, vision and effective runtime are separate checks.

Use `medium` when a focused, well-specified task has strong tests and deep analysis adds little. `high` is the normal reasoning setting for substantial engineering. `xhigh` is available for multi-system/high-impact investigation and review without a special economy waiver. `max` is not a blanket default: use it when a concrete high-impact problem and representative evidence justify the latency/token trade-off, recording the reason and observed effect. `ultra` is client/plan-specific and must never be inferred to be a valid CLI value, an API value or the `/caveman Ultra` method.

| Work | Starting route |
| --- | --- |
| Deterministic transformation/check | no spawn |
| Small read-only lookup, extraction, catalog/docs check | `gpt-6-luna` / high; deterministic tool alone if sufficient |
| Frozen-contract implementation with strong deterministic verification | `gpt-6-luna` / high or `gpt-6.2-sol` / medium |
| Ordinary implementation, TDD, API/frontend, scoped refactor | `gpt-6.2-sol` / high |
| Complex integration, race, migration, performance/SQL diagnosis | `gpt-6.2-sol` / xhigh; Astra/high for cross-system difficult invariants |
| High-impact architecture, security/authorization/data decisions | `gpt-6.2-astra` / high–xhigh |
| Visual QA, screenshots, browser/native-app reproduction | `gpt-6.1-terra` / high if client-supported; otherwise Sol/high with real tools |
| Independent review of material correctness/security/tenancy/financial risks | Sol/high–xhigh; Astra/xhigh where complexity or impact merits it |
| Independent exploratory comparison, wide repo search, test-log triage | Luna/high for bounded scope; Sol/high for interconnected conclusions |
| Exceptionally difficult long-horizon/adversarial synthesis | Astra/xhigh, `max` only with recorded quality/cost rationale |

Current tier hints are efficient `gpt-6-luna`, visual `gpt-6.1-terra`, compatible Sol `gpt-6.1-sol`, balanced `gpt-6.2-sol`, frontier `gpt-6.2-astra`. Official API catalog availability is **not** proof of access in Codex CLI, app, IDE, this account or its spawn allowlist. Resolve at invocation time. Do not bind implementation to one tier or review to another: classify the actual work. Neither additional API credits, a paid speed tier, a new provider, GitHub Actions nor other billable services are authorized by this routing change.

## Explicit and effective configuration

Every spawn MUST set model and reasoning effort explicitly when supported. However, **explicit spawn values are not always the effective result**: in current Codex, the selected custom agent TOML's `model` and `model_reasoning_effort` take precedence over explicit spawn values; otherwise the resolution order is explicit spawn → `[agents]` defaults → inherited parent, with model-default effort when a new model is selected without effort. Check custom files, resumptions and actual worker metadata; reject incompatible combinations before execution.

Separate three invocation surfaces: (1) Codex CLI/app/IDE use their supported subagent tools, local `.codex/agents/*.toml` or global `$CODEX_HOME/agents/*.toml`, and `[agents]` settings; (2) Responses API multi-agent uses request-scoped `multi_agent` fields, not a local `config.toml`; (3) Agents API uses `agent.multi_agent` session configuration. Never import an API request field, old `[features]` flag, `agent_type`, `fork_turns`, `close_agent` or `reasoning.effort` blindly into another tool schema. Discover actual tools, client version, accepted model/effort and lifecycle methods. Native `default` / `worker` / `explorer` agents and optional custom TOML agent types are invocation profiles; Agency Agents personas remain independent methodology, not automatically installed native types.

Record, compactly:

```text
explicit delegation authorization + native profile and/or Agency persona @ upstream revision
routing dimensions and bounded/frozen-gate result
requested model / effort / execution mode when exposed
actual model / effort when observable (otherwise NOT_OBSERVED)
owned, read-only and forbidden scope
acceptance, verification, independent-review requirement
unavailable-client/fallback reason; added-money authority if any
```

On supported Codex clients, use this **quality-first backstop** in the existing user `config.toml` without overwriting unrelated settings:

```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 2
default_subagent_model = "gpt-6.2-sol"
default_subagent_reasoning_effort = "high"
```

The concurrency key limits spawned threads **excluding** the controller; a harness may have its own smaller limit. The backstop is **not a hard override** of custom agent TOML or explicit spawn values. Do not install it when unsupported; fall back to an observed available model/effort and document the difference. Keep Agency Agents available; inspect custom profile overrides without replacing persona instructions or unrelated user settings. Verify runtime via supported readback/metadata; this repository cannot update a workstation by itself.

If a requested setting is unsupported, inspect the actual allowlist, select the nearest **capable** route that preserves risk/quality and the monetary ceiling, and record the change before execution. When a custom agent file pins a contradictory effort/model, correct that file only with authority or select a compatible native profile; re-sending `spawn` overrides does not fix it. If included/free usage is uncertain, stop the potentially billable action, not unrelated permitted work. Independent review remains required where triggered; inability to provide it is a blocker, not a waiver.

## Context and token budgets

Budgets apply to coordination, not to truncating material evidence:

- Target around **3,000 input tokens** for a typical coherent dispatch, excluding referenced source files that the worker actually needs. Up to ~6,000 is reasonable for a high-risk interface/acceptance contract; these are advisory guidance, not fabricated API token-limit settings.
- Target around **650 words** for a normal completion handoff: changed paths/commits, commands and exits, findings, blockers and next action. Store detailed evidence in its canonical location and reference it.
- Exceed either target for concrete complexity, incomplete cross-system interfaces, acceptance, safety or recovery needs; record the reason. Never omit a risk or required result to meet a word count.
- Send authority paths/SHAs, the specific task and deltas. Do not copy full transcripts, the Handbook, the entire plan, all Agency personas, whole logs or unrelated research into every worker.
- Prefer isolated/minimal context where supported. Reuse the established repository session and cohesive workers. Restart from a compact durable handoff only when context is unreliable.
- Use focused tests while correcting; run the full required gates on the integrated exact candidate. Reuse prior evidence only when its relevant inputs are demonstrably unchanged.
- Do not busy-poll or request repetitive status reports. Use supported completion events/waits. Do not rerun a successful implementation on a stronger model for reassurance; a distinct independent review is different.

Record input, cached-input, output and reasoning tokens only where observable; otherwise use null/NOT_OBSERVED. Record wall time/retries where observable, with no fabricated pricing. Compare comparable workstreams before claiming savings. A preset, concurrency cap or requested model is configuration evidence, not proof of a percentage reduction.

## Escalation by cause

Never implement an automatic Luna → Sol → Astra ladder.

| Cause | Response |
| --- | --- |
| Environment, network, provider or tool failure | repair/isolate environment; no effort increase |
| Missing or contradictory authority | resolve the contract |
| Clear code defect with evidence | same worker may correct it |
| Repeated hypothesis without new evidence | change diagnosis/method or specialist; stop the repetitive loop |
| Inability to reconcile invariants with adequate context | increase one of capability/effort with a scoped reason |
| Context overload | narrow or restart from durable state |
| New material risk | reclassify work and review gate |

After two unsuccessful correction cycles on the same failure, the controller must diagnose the cause and re-contract the next step before another attempt. This is not an automatic model upgrade or permission to abandon a mandatory test. Change one routing variable at a time when practical; reclassify later tasks from their own complexity, not by inheriting an emergency `max` or forcing Luna/low.

## Independent review: unchanged quality floor

Independent model review is risk-triggered, not universal. Require an independent worker for material changes to:

- authentication/authorization, tenant isolation, secrets or privileged boundaries;
- destructive/nontrivial durable-data migration or recovery;
- billing, money or externally consequential financial behavior;
- broad Production/provider configuration or irreversible external actions;
- costly public/external contract compatibility;
- concurrency/atomicity that automation only partially covers;
- high-impact architecture with weak/partial deterministic verification.

A deterministic low/medium-risk change may close with tests plus controller diff inspection. A mandatory review cannot be removed to meet the token budget. The author is not its own independent reviewer. The controller qualifies only when it did not author the implementation under review. Route the reviewer independently using the same dimensions: bounded evidence review may use Luna/high; integrated correctness/security review normally uses Sol/high–xhigh; Astra/xhigh is justified for materially complex, adversarial or high-impact risk. The reviewer must see the complete relevant contract, not just the author's summary.

## Adoption and completion

At the next cohesive boundary, controllers adopt this revision for **new workers** and reconcile defaults/overrides before reuse. Do not hot-swap instructions or cancel useful in-flight work solely to change a label. Resume the existing repository session, preserve work and independent-review obligations, and record whether local configuration has actually been applied.

The machine-readable profile and playbook must agree with this Standard. Existing registry IDs/paths stay stable; historical commits preserve previous policy. This revision does not enable provider actions, change product architecture or authorize added monetary charges.

A worker report is evidence, not completion. The controller owns integration, exact-head verification, disclosure of unrun gates and final claims. Record quality failures and routing degradations honestly; never exchange a lower token count for false acceptance.
