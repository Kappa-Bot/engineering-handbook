---
id: std-agent-runtime-routing
kind: standard
status: active
owner: engineering
version: "1.1"
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
last_verified: 2026-10-15
review_due: 2027-01-15
supersedes:
  - std-owner-authorized-role-pods
---

# Agent Runtime Routing

## Purpose and October 2026 economy revision

Minimize expected total model, tool, reasoning, context-transfer and coordination cost **to verified acceptance**, including correction and independent review. The cheapest individual call is not the objective.

The owner's 2026-10-15 direction is to retain Agency Agents and reduce resource use **per worker**, not to abandon specialist delegation or reduce the security/verification floor. Revision 1.1 changes the frozen-contract starting effort from medium to low, adds explicit economy exception records and bounded context/report budgets. These are organizational operating decisions, not claims that a provider recommends low effort for every task or that a percentage saving has already been measured.

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

Use zero spawned workers by default. Choose the first adequate route:

1. an existing deterministic tool or script;
2. the current controller with its existing context;
3. one Agency Agents specialist;
4. a second specialist for a distinct independent workstream or required independent review.

A spawn needs at least one material advantage: specialist expertise; cheaper offload of a cohesive frozen implementation; isolation of large research context; genuinely independent parallel work; or required review independence. A matching profile alone is insufficient. An explicitly owner-authorized multi-agent task retains its justified workers; economy is not permission to quietly turn it into an unreviewed single-author workflow.

Agency Agents remains the specialist catalog. Select its narrowest relevant current profile and record its observed revision. Persona, model and effort are separate choices. The controller can use a profile directly when no separate worker is useful. `Agents Orchestrator` is optional; upstream mandatory ceremony, per-task QA swarms or repeated retries are not Handbook authority.

Normal staffing is one worker per cohesive responsibility, with a routine ceiling of two concurrent specialists. More requires a recorded distinct contribution and expected benefit. Nested spawning is off by default; only the controller routes workers unless current repository authority explicitly permits otherwise. Do not create one agent per file, test, finding or checklist row. Reuse a worker for its cohesive responsibility while context remains reliable; serialize shared-file writes and require disjoint ownership for parallel writes.

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

## Economy default and cheap implementer gate

For a spawned worker with **frozen material semantics, bounded scope and strong verification**, start with the current efficient tier, presently `gpt-6-luna`, at **low** reasoning effort.

The gate requires explicit acceptance, an existing pattern or specified method, bounded writable scope, no unresolved architecture/security/data-contract decision, reversible or contained impact, tests covering likely failure classes, and no sensitive external action delegated.

Medium effort is available when the task contains a concrete non-mechanical interaction that low effort is unlikely to handle reliably. Record that interaction; do not set medium for every task merely because it is engineering. Freeze or split an oversized task before paying for a larger context. Critical systems may use economical workers for frozen mechanical work; criticality instead strengthens verification and review.

Routine workers use low or medium effort. High effort or a frontier model requires a scoped exception naming the unresolved decision, risk, evidence and return-to-economy condition. This is not a mandatory failed cheap attempt: do not spend a predictably inadequate attempt on a demonstrably difficult security or data-integrity decision.

| Work | Starting route |
| --- | --- |
| Deterministic transformation/check | no spawn |
| Extraction, lookup, mechanical docs/config, small bounded change | efficient / low |
| Frozen-contract implementation with strong verification | efficient / low |
| Bounded interacting logic with explicit contracts | efficient / medium, with the interaction recorded |
| Coupled integration, nontrivial diagnosis or independent integrated security/data/money review | balanced / medium when the capability need is justified |
| High-uncertainty, high-impact architecture/security/authorization decision | capability and effort exception; frontier / high only when its need is demonstrated by the task or evidence |
| Exceptional long-horizon/adversarial reasoning | frontier / xhigh only with a documented lower-route quality gap or compelling task-specific evidence |
| max effort | evaluation-gated exception; never a routine default |

Current tier hints are efficient `gpt-6-luna`, balanced `gpt-6.1-sol`, frontier `gpt-6-astra`. They are not timeless or guaranteed available IDs. Resolve against the actual harness allowlist and included account access. Never silently substitute an expensive model or paid execution mode. Do not bind implementation to one tier or review to another: classify the actual work.

## Explicit and effective configuration

Every spawn MUST set model and reasoning effort explicitly when supported. Check resumptions and custom agent/profile configuration as well; an intended low-cost request is not proof of the effective runtime. Avoid accidental inheritance from an expensive controller.

Record, compactly:

```text
profile + upstream revision
routing dimensions and cheap-gate result
requested model / effort / execution mode when exposed
actual model / effort when observable (otherwise NOT_OBSERVED)
owned, read-only and forbidden scope
acceptance, verification, independent-review requirement
budget exception and reason, if any
```

Use an efficient low-effort machine-level subagent default as a backstop **where supported**. It does not replace explicit routing. Keep the Agency Agents mechanism enabled. Inspect existing custom profile overrides without replacing persona instructions or unrelated user settings. Verify the resolved configuration through the harness's supported readback or worker metadata; never claim a machine was updated because this repository changed.

If a requested setting is unsupported, inspect the actual allowlist, select the nearest already-authorized economical route that preserves the risk/quality intent, and record the change before execution. If the effective cost cannot be controlled, stop bulk spawning and resolve configuration. Independent review remains required where triggered; inability to provide it is a blocker, not a waiver.

## Context and token budgets

Budgets apply to coordination, not to truncating material evidence:

- Target at most **1,500 input tokens** for the controller-written dispatch, excluding referenced source files that the worker actually needs. This is an advisory packet budget, not a fabricated API token-limit setting.
- Target at most **400 words** for a normal completion handoff: changed paths/commits, commands and exits, findings, blockers and next action. Store detailed evidence in its canonical location and reference it.
- Exceed either target only for a concrete missing acceptance, interface, safety or recovery fact; record the reason. Never omit a risk or required result to meet a word count.
- Send authority paths/SHAs, the specific task and deltas. Do not copy full transcripts, the Handbook, the entire plan, all Agency personas, whole logs or unrelated research into every worker.
- Prefer isolated/minimal context where supported. Reuse the established repository session and cohesive workers. Restart from a compact durable handoff only when context is unreliable.
- Use focused tests while correcting; run the full required gates on the integrated exact candidate. Reuse prior evidence only when its relevant inputs are demonstrably unchanged.
- Do not busy-poll or request repetitive status reports. Use supported completion events/waits. Do not rerun a successful implementation on a stronger model for reassurance.

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

After two unsuccessful correction cycles on the same failure, the controller must diagnose the cause and re-contract the next step before another attempt. This is not an automatic model upgrade or permission to abandon a mandatory test. Change one routing variable at a time when practical; return later bounded tasks to the economy default.

## Independent review: unchanged quality floor

Independent model review is risk-triggered, not universal. Require an independent worker for material changes to:

- authentication/authorization, tenant isolation, secrets or privileged boundaries;
- destructive/nontrivial durable-data migration or recovery;
- billing, money or externally consequential financial behavior;
- broad Production/provider configuration or irreversible external actions;
- costly public/external contract compatibility;
- concurrency/atomicity that automation only partially covers;
- high-impact architecture with weak/partial deterministic verification.

A deterministic low/medium-risk change may close with tests plus controller diff inspection. A mandatory review cannot be removed to meet the token budget. The author is not its own independent reviewer. The controller qualifies only when it did not author the implementation under review. Route the reviewer independently using the same dimensions: a mechanical contract check may use efficient/low; genuinely integrated risk may justify balanced/medium; Astra/xhigh is not the reviewer default.

## Adoption and completion

At the next cohesive boundary, controllers adopt this revision for **new workers** and reconcile defaults/overrides before reuse. Do not hot-swap instructions or cancel useful in-flight work solely to change a label. Resume the existing repository session, preserve work and independent-review obligations, and record whether local configuration has actually been applied.

The machine-readable profile and playbook must agree with this Standard. Existing registry IDs/paths stay stable; historical commits preserve previous policy. This revision does not enable provider actions, change product architecture or authorize added monetary charges.

A worker report is evidence, not completion. The controller owns integration, exact-head verification, disclosure of unrun gates and final claims. Record quality failures and routing degradations honestly; never exchange a lower token count for false acceptance.
