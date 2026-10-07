---
id: std-agent-runtime-routing
kind: standard
status: active
owner: engineering
version: "1.0"
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
  - src-agency-agents
last_verified: 2026-10-07
review_due: 2027-01-07
supersedes:
  - std-owner-authorized-role-pods
---

# Agent Runtime Routing

## Purpose

Route engineering work through the minimum agent structure, model capability and reasoning effort needed to reach **verified acceptance**, rather than through permanent organizational roles.

The optimization target is not the cheapest single call. It is the lowest expected total model/tool/context cost that reliably produces an acceptable result, including retries, review and verification.

This Standard supersedes the fixed `parent / design-quality / delivery` topology. Agency Agents supplies specialist personas; the current controller owns task continuity and integration unless it deliberately delegates those responsibilities.

## Authority

Agent personas and model-routing heuristics are subordinate to:

```text
external non-negotiable obligation
→ Handbook Governance / Policy / Standard
→ permitted repo-local authority
→ approved task/spec/plan
→ runtime routing decision
→ Agency Agents persona / optional process method
```

A model or persona never grants new scope, provider, Production, billing, credential, destructive-action or user-data authority.

## Default: do not spawn

Use **zero subagents by default**.

Before spawning, choose the cheapest reliable execution path in this order:

1. deterministic tool/script already performs the transformation or check;
2. current controller executes directly with existing context;
3. one Agency Agents specialist is spawned;
4. a second independent specialist is added only when a distinct workstream or risk boundary justifies it.

Do not spawn when context transfer, rediscovery, coordination and verification are likely to cost more than finishing the bounded task directly.

A specialist spawn does not require a separate owner confirmation when the engineering task itself is already authorized, the spawn remains inside that scope/permission envelope, and no new monetary/provider/sensitive authority is introduced. Explicit owner authority is still required wherever another Handbook rule requires it.

## Spawn value test

Spawn only when at least one material advantage exists:

- a specialist method is likely to improve a decision or implementation materially;
- a cohesive implementation block can be offloaded to a cheaper model with strong verification;
- a large read/research task can be isolated from the controller context;
- two workstreams are genuinely independent and parallelism materially helps;
- independent review is required by the risk boundary.

"Agency Agents has a matching profile" is not sufficient reason to spawn.

`Agents Orchestrator` is an optional specialist, not the mandatory parent. Use it only when real coordination complexity justifies its own context and process overhead. Its upstream mandatory per-task QA loops are not Kappa-Bot policy.

## Runtime classification

Classify only the dimensions that can change routing; do not manufacture a numeric precision score.

### Decision uncertainty

- **low** — result and method are already specified;
- **medium** — implementation choices remain but semantics are stable;
- **high** — architecture, intended behavior or trade-offs remain materially unresolved.

### Dependency breadth

- **local** — one bounded component/pattern;
- **repository** — multiple coupled components in one repository;
- **cross-system** — contracts, providers or multiple repositories interact.

### Impact and reversibility

- **low** — local/reversible failure with strong containment;
- **medium** — meaningful regression or rollback cost;
- **high** — security, authorization, tenant isolation, durable data, money, public contracts or production behavior;
- **critical** — irreversible/destructive or broad externally visible consequences.

### Verification strength

- **strong** — deterministic tests/checks can directly detect the relevant failure class;
- **partial** — useful automation exists but important judgment/evidence remains;
- **weak** — correctness depends heavily on reasoning, live evidence or human judgment.

### Context-transfer cost

- **low** — bounded authority and few relevant files;
- **medium** — non-trivial repo context must be transferred;
- **high** — spawning would duplicate a large context the controller already holds.

## Cheap implementer gate

A cost-efficient implementer is the preferred default when **all material semantics are frozen** and verification is strong enough to catch likely mistakes.

Strong indicators:

- acceptance criteria are explicit;
- an existing implementation pattern is available;
- writable scope is bounded;
- no unresolved architecture/security/data-contract choice remains;
- the change is reversible or low/medium blast radius;
- tests or deterministic checks cover the relevant behavior;
- no Production/provider/customer action is delegated.

When these conditions hold, prefer the efficient model tier—currently GPT-6 Luna—at `low` or `medium` effort. Do not spend Sol/Astra merely because the repository or feature is important.

Critical systems may still use a cheap implementer for frozen mechanical work; criticality instead increases the verification/review gate.

## Model routing

Model names are current preferred mappings, not timeless aliases. Resolve them against the actual Codex spawn allowlist before use and record requested versus actual values.

| Work | Preferred starting route |
|---|---|
| deterministic transformation/check | no model spawn |
| extraction, lookup, mechanical docs/config, tiny bounded change | Luna low |
| frozen-contract implementation with strong verification | Luna medium |
| tricky but bounded logic with strong verification | Luna high **or** Sol medium; prefer the cheaper configuration that passes representative evals |
| multi-component implementation, integration, migration or difficult debugging | Sol medium/high |
| high-uncertainty architecture/security/data-integrity/authorization decision | Astra high |
| exceptional long-horizon/adversarial reasoning where quality dominates cost | Astra xhigh |
| max effort | prohibited as a routine default; use only when representative evidence shows material benefit over xhigh |

Do not bind a persona to a model. The same specialist can run on Luna, Sol or Astra according to the actual task.

Do not bind review to Astra or implementation to Luna. A deterministic contract review may be cheap; a difficult implementer may require the strongest model.

## Reasoning-effort routing

Reasoning effort is a last-mile control after task clarity, context quality and verification have been improved.

- `low`: little interpretation, strong constraints, strong verification;
- `medium`: normal bounded engineering and the default cheap-implementer effort;
- `high`: multiple interacting constraints, difficult diagnosis, migration/integration or material trade-offs;
- `xhigh`: exceptional reasoning-heavy work where lower settings have a demonstrated quality gap;
- `max`: eval-gated exception only.

Prefer improving the task contract, context or verification before increasing effort.

## Explicit spawn configuration

Every spawned worker MUST specify **both** model and reasoning effort when the harness supports those fields. Never rely on accidental inheritance from an expensive controller.

Record:

```text
specialist profile + upstream revision
routing class / material reasons
requested model + reasoning effort
actual model + effort when observable
owned/read-only/forbidden scope
acceptance + verification
```

If the requested model/effort is unsupported, do not silently substitute. Resolve the current allowlist and choose the nearest already-authorized route that preserves the task's risk/cost intent; otherwise record the routing blocker.

For Codex installations that support subagent defaults, use an efficient deliberate machine-level backstop so an omitted override cannot silently inherit the controller's expensive configuration. The backstop is a safety net, not permission to omit explicit per-spawn routing.

## Escalation by cause

Never implement an automatic `Luna → Sol → Astra` ladder merely because an attempt failed.

- environment/network/provider/tool failure → repair or isolate the environment; do not increase reasoning;
- missing/contradictory authority → resolve the specification/authority;
- clear implementation bug with good evidence → same implementer may correct it;
- repeated failed hypothesis without new evidence → change diagnostic method or specialist;
- inability to reconcile dependencies/invariants despite adequate context → increase model capability or reasoning effort;
- context overload → narrow/restart from durable state instead of buying more reasoning;
- new high-impact risk → reclassify the task and its review gate.

When practical, change one routing variable at a time so the organization can learn whether model capability, effort, context or method caused the improvement.

## Independent review

Independent model review is **risk-triggered, not universal**.

Require an independent worker when the change materially affects:

- authentication/authorization, tenant isolation, secrets or privileged boundaries;
- destructive/non-trivial durable-data migration or recovery;
- billing, money or externally consequential financial behavior;
- broad Production/provider configuration or irreversible external action;
- public/external contracts where compatibility failure is costly;
- concurrency/atomicity invariants that automated verification only partially covers;
- high-impact architecture with weak/partial deterministic verification.

For low/medium-risk work with strong deterministic verification, tests + diff inspection may be sufficient.

Select the reviewer model/effort using the same routing dimensions. A checklist-like review may use Luna; integrated reasoning may use Sol; Astra is reserved for genuinely difficult/high-impact review.

The implementation author cannot count as an independent reviewer. The controller can serve as independent reviewer only when it did not author the implementation being reviewed.

## Concurrency and lifecycle

- default active specialist count: 0;
- normal spawned worker count for a cohesive workstream: 1;
- routine concurrent specialist ceiling: 2;
- use two only for genuinely independent work or a required independent review;
- additional workers require an explicit distinct contribution whose expected value exceeds context/coordination cost;
- nested spawning is off by default; only the controller routes workers unless current repo authority explicitly permits otherwise;
- reuse a worker for a cohesive responsibility while its context remains reliable;
- do not create one agent per file, test, finding or checklist item.

Parallel write-heavy work requires disjoint ownership. Shared-file work is serialized.

## Context and token economy

- prefer isolated/minimal-context spawns when supported;
- send authority paths/SHAs and task-local deltas instead of whole transcripts;
- do not copy the entire Handbook, Agency Agents catalog, plans, logs or test output into each spawn;
- do not poll workers repeatedly; use event/wait mechanisms efficiently when available;
- use focused checks during correction loops and full required gates on the final candidate;
- reuse valid evidence only when the relevant inputs are unchanged;
- do not spawn a reviewer when deterministic evidence already proves the risk being checked.

Optimize **tokens to verified acceptance**, not tokens per call.

## Completion

A worker report is evidence, not completion.

The controller remains responsible for integration, exact-head verification, truthful unrun-gate disclosure and final claims. Sensitive external actions remain governed by their separate authority requirements.
