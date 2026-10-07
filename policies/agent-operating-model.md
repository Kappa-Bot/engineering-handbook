---
id: pol-agent-operating-model
kind: policy
status: active
owner: engineering
version: "0.8"
applies_to:
  - all-repositories
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
  - src-git-worktree
  - src-agency-agents
  - src-agency-agents-app
  - src-openai-model-selection
  - src-openai-reasoning
  - src-openai-models
last_verified: 2026-10-07
review_due: 2026-12-14
---

# Agent Operating Model

## Objective

Use coding agents as disciplined engineering workers without turning every task into a giant prompt, multi-agent ceremony, or permanent context dump.

The Engineering Handbook governs **all engineering work across repositories**. That does not mean every task loads the whole handbook: trivial work may need only the distributed global baseline plus repo-local instructions, while non-trivial/risky work resolves specialized handbook context progressively.

## Context model

Permanent context MUST stay small.

Preferred layering:

```text
small global handbook baseline
        +
small repo-local AGENTS.md
        +
current task
        ↓
resolve focused handbook context / skills / references only when relevant
```

Universal rules belong in the handbook/global distribution artifact. Repo-specific commands, architecture, boundaries, product/domain facts and local decisions belong in the repo. Specialized procedures belong in focused artifacts rather than a giant `AGENTS.md`.

For non-trivial work, prefer the deterministic `engineering-handbook` context router and its delta modes over manually reading broad handbook sections. For trivial repo-local work, do not manufacture a context query or documentation ceremony when the global baseline and local authority already decide the task.

## Session and repository scope

- Default to one active engineering session per repository/task context.
- Keep one repository as the primary unit of work for a session.
- Do not mix unrelated repository changes into one task merely because the agent can access them.
- Cross-repository work SHOULD explicitly identify which repository owns each change and which handbook rule is being propagated.

## Agent delegation and runtime routing

Use **zero spawned workers by default**.

The current controller may execute directly. It does not need a permanent "parent" persona and does not need to spawn `Agents Orchestrator` merely because Agency Agents is available.

Before spawning, prefer:

```text
deterministic tool/script
→ direct controller execution
→ one Agency Agents specialist
→ second independent specialist only for distinct parallel value or required review
```

A spawn is justified only when it materially improves quality, isolates expensive context, enables genuinely useful parallelism, provides required independence, or moves a frozen/strongly-verifiable implementation block to a cheaper model. The existence of a matching persona is not sufficient.

Canonical runtime routing:

- `std-agent-runtime-routing` defines spawn value, task classification, model/effort selection, independent-review triggers, concurrency and escalation;
- `pb-agent-runtime-routing` defines the execution loop;
- `ref-agent-runtime-manifest` defines optional durable routing/provenance state;
- `ref-agency-agents-specialist-routing` defines upstream specialist discovery/update behavior;
- `machine-readable/agent-runtime-routing.v1.json` is the consistency-checked routing profile.

The fixed `parent / design-quality / delivery` topology and its Sol/Astra/Luna role bindings are superseded historical behavior. Do not revive them through repo-local instructions unless the owner explicitly creates a scoped exception.

### Spawn permissions

A separate owner confirmation is not required for every spawn when:

- the engineering task itself is already authorized;
- the worker remains within that exact scope and repository permission envelope;
- the routing stays within current included/authorized model/tool usage;
- no new provider, Production, billing, destructive, customer-data or outbound-action authority is introduced.

Separate authority is still required wherever another Handbook rule or the task itself requires it.

### Runtime choice

Specialist persona, model and reasoning effort are independent decisions.

Every spawn SHOULD set both model and reasoning effort explicitly when the harness supports them. Never rely on expensive controller inheritance as a routing policy.

Prefer the efficient model tier—currently GPT-6 Luna—for frozen, bounded implementation with strong verification. Use Sol/Astra only when uncertainty, dependency breadth, impact, weak verification or difficult reasoning justifies the extra resource use. `xhigh` is not a reviewer default; `max` is eval-gated and exceptional.

Optimize total resources to **verified acceptance**, including retries/review/context transfer, not the price or token count of one isolated call.

## Planning

Planning effort MUST be proportional to task complexity.

- Mechanical, obvious, low-risk work may proceed with a short internal plan.
- Multi-step, architectural, security-sensitive, migration-heavy, or ambiguous work SHOULD produce an explicit spec/plan before implementation.
- A plan MUST NOT become an excuse to postpone straightforward implementation after the design is already approved.

Keep task states distinct when relevant:

```text
research → decision → spec → plan → implementation → verification → adoption
```

Do not silently jump from exploration/research into implementation.

## Scope control

Agents MUST:

- keep the requested outcome primary;
- avoid unrelated refactors;
- avoid speculative abstractions;
- avoid cleanup outside the necessary change;
- make assumptions explicit when they materially affect the solution;
- prefer small, reviewable changes.

## Methodology

Use specialized engineering methods when they fit the work, including:

- brainstorming for unresolved creative/architecture decisions;
- implementation planning for non-trivial multi-step work;
- TDD where behavior can be expressed meaningfully as tests;
- systematic debugging before speculative fixes;
- verification-before-completion;
- code review appropriate to the risk.

Methodology defaults MUST NOT override explicit handbook policies such as the no-worktree or zero-subagent default. Explicit activation of `OWNER_AUTHORIZED_ROLE_PODS` is the narrow opt-in exception to the latter, not a new default.

## Specialist and skill routing

Agency Agents is the default upstream catalog for specialist personas, not a second governance system.

For any task where specialization can materially change the result:

1. identify the competency actually required;
2. consult the current Agency Agents catalog;
3. select the narrowest useful profile;
4. decide whether the controller should use the methodology directly or whether a separate worker is worth its context/coordination cost;
5. if spawning, route model + effort independently using `std-agent-runtime-routing`;
6. record profile/revision and runtime routing only when material to reproducibility or recovery.

Prefer upstream profiles unchanged. Kappa-Bot-specific persona forks require repeated evidence that upstream cannot satisfy a durable requirement.

Do not inherit an upstream persona's workflow ceremony as Handbook authority. In particular, Agency Agents profiles that prescribe mandatory planning phases, per-task QA loops, screenshots or repeated retries are advisory methodology only unless the actual task/risk requires them.

Process/workflow methods remain separate from specialist identity:

- planning proportionate to uncertainty;
- TDD where behavior is meaningfully testable;
- systematic debugging before speculative fixes;
- verification-before-completion;
- risk-proportionate code/release review;
- `caveman` / `/caveman Ultra` only when available, applicable and useful;
- visual/design craft skills only when they can materially affect a visual task.

Rules:

- use the smallest specialist/method/tool set that can materially improve the outcome;
- do not load the full Agency Agents catalog or skill portfolio;
- external persona/skill instructions never override Handbook/repo authority, task scope, permissions, cost controls or verification gates;
- no specialist name implies a required model;
- no "implementer" label implies Luna and no "reviewer" label implies Astra;
- independent review is triggered by risk, not by process ritual.

For material design work, apply `pat-design-context-layering` and `pb-frontend-quality-review` before external precedents.

## Token/context efficiency

- Do not paste entire handbooks/research reports into task prompts when a stable ID/path suffices.
- Load the smallest relevant artifact set.
- Prefer links/IDs and focused summaries to duplicated policy prose.
- Keep generated progress reports concise unless detailed evidence is needed for a durable artifact.
- Store deep reusable knowledge centrally; retrieve narrow task-specific context.
- Do not load an entire external design corpus, Agency Agents catalog or every installed skill merely to signal rigor.
- When a repo has a compact, authoritative design contract, prefer it over re-explaining the same visual rules in each prompt.
- Where workers are spawned, provide one compact task-local dispatch, then only material deltas; keep reusable evidence in durable repository state.

## Handoff

At handoff, the agent SHOULD report:

- outcome delivered;
- files/areas changed;
- verification actually run;
- checks not run and why;
- remaining risks or dependencies;
- Git/workspace state when relevant.

The handoff MUST NOT imply success for unexecuted gates. Long-running spawned-worker work additionally follows `pat-durable-logical-agent-handoff` when continuity/restart matters.
