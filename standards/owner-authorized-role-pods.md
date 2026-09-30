---
id: std-owner-authorized-role-pods
kind: standard
status: active
owner: engineering
version: "1.3"
applies_to:
  - all-repositories
  - codex
  - multi-agent-execution
sources:
  - src-openai-codex-agents
  - src-openai-codex-skills
  - src-git-worktree
last_verified: 2026-09-30
review_due: 2026-12-14
---

# Owner-Authorized Role Pods

## Purpose

Provide an explicit opt-in operating model for substantial work that benefits from a very small number of persistent subagents without making multi-agent execution the default or multiplying prompt, model, tool and coordination cost.

This Standard refines `pol-agent-operating-model`. It does not replace the zero-subagent default.

## Activation

`OWNER_AUTHORIZED_ROLE_PODS` is active only when at least one of these is recorded in the approved task/run manifest:

- the owner explicitly authorizes subagents for the initiative; or
- permitted repository-local authority explicitly authorizes this profile.

The authorization reference MUST be durable and unambiguous. General permission to modify a repository is not permission to spawn subagents.

Without recorded activation, use zero subagents.

## Compact topology

There are only two normal delegated role types:

```text
parent/orchestrator
├── design-quality  — high-leverage decisions, architecture, security, product/UX/design and independent review
└── delivery        — implementation, tests, mechanical fixes, migrations and focused commits
```

One subagent is valid when one cohesive delegated workstream is sufficient. Both are valid when their distinct responsibilities materially save work or improve quality.

No third subagent role exists under this profile. If another perspective is needed, route it through the existing `design-quality` role or keep it with the parent; do not create a new reviewer/specialist taxonomy.

Rules:

- maximum subagent count: 2;
- maximum concurrent subagents: 2;
- nested spawning: prohibited;
- only the parent orchestrator may spawn, steer, replace, stop or close subagents;
- never create an agent per route, page, component, test, ticket, finding or checklist item;
- consolidate all tasks of the same responsibility into the same live role pod.

## Owner-default model routing

Select the role profile before selecting the available model alias. Record the requested and actual model and reasoning level used; never claim a requested alias was used when unavailable.

Kappa-Bot owner defaults, amended by the owner on 2026-09-30, are:

- parent/orchestrator: `Sol 6.1`, reasoning `high`;
- `design-quality`: `Astra 6`, reasoning `xhigh`;
- `delivery`: `Luna 6`, reasoning `xhigh`.

The routing intent is strict even when aliases change: the parent preserves continuity and integration; `design-quality` receives high-leverage reasoning; `delivery` receives frozen, already-specified implementation and mechanical work. Versions are intentional: do not silently substitute an older generation or Terra for the requested routing. Resolve actual harness model identifiers instead of inventing them. An unavailable requested model may use only an already-authorized fallback that preserves responsibilities, review independence and the run's cost ceiling; otherwise record the configuration blocker and continue unaffected authorized work.

`design-quality` is for architecture, security/contracts, product decisions, UX/UI/design, ambiguous trade-offs, difficult diagnosis and the highest-leverage independent review point. It should not spend its context on routine implementation already frozen by authority.

`delivery` is for implementation, TDD, settled-behavior debugging, mechanical refactors, migrations, workflow/config edits, documentation synchronization and unambiguous review fixes. It MUST NOT redesign product/architecture semantics when authority is materially ambiguous; escalate that ambiguity to the parent for routing to `design-quality` when needed.

## Persistent live roles

A pod is assigned one cohesive workstream and is reused for that entire workstream while its live context remains reliable. Do not discard and recreate it between milestones merely to obtain a fresh thread.

The parent remains authoritative for:

- orchestration and context continuity;
- acceptance/integration of shared decisions;
- conflict resolution;
- branch/worktree topology;
- Production/provider actions;
- exact-head verification;
- merge, cleanup and final claims.

A subagent report is evidence to inspect, not proof of completion by itself.

## Low-communication contract

Inter-agent traffic is a cost center. Prefer repository state over conversation.

For each cohesive megaplan/workstream and each active delegated role:

- target **one parent dispatch** containing the complete task-local packet;
- target **one final handoff** back to the parent;
- target at most **two total transmissions** per role for the megaplan;
- use a **hard ceiling of three routine transmissions** only when a material blocker or authority/head delta genuinely requires one extra transmission;
- no direct `design-quality` ↔ `delivery` messaging;
- no progress chatter, repeated specs, repeated diffs or repeated logs;
- after kickoff, send only deltas and canonical path/SHA references.

The routine ceiling is not a safety, review or completion shortcut. Required clarification of a genuine safety/authority blocker, independent review findings, corrective delivery and re-review may exceed it only through minimal parent-mediated deltas with the reason and observed count recorded in the existing manifest. Never hide a blocker, skip review, approve unresolved findings or stop otherwise executable authorized work to satisfy a message counter. Do not manufacture new workstreams to reset the budget.

Do not automatically dispatch `design-quality` both before and after every implementation. Use its one normal dispatch at the highest-leverage decision or review point for that megaplan; required risk-boundary review and corrective re-review remain mandatory. The parent still performs final exact-head verification.

`OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS` remains a narrower compatibility profile for runs that explicitly require both canonical roles, but it MUST NOT introduce `master`/`implementer` or any alternate role taxonomy. Its low-communication limits inherit this Standard, including necessary safety/review exceptions.

## Authorized exhaustive execution and zero incremental cost

When the owner authorizes finishing all feasible work without additional monetary cost, record that instruction in the existing run manifest and apply this mode to the approved program, not to an unlimited backlog.

- Continue through every dependency-ready authorized phase and its necessary fixes, tests, review, integration and already-authorized release/adoption work. Do not stop merely because a task, PR, checkpoint or phase finished, or to request routine reapproval already granted.
- Keep verified checkpoints and compact durable state as recovery boundaries, not voluntary stopping points. Compact or resume through supported runtime mechanisms and reuse the same logical roles while executable authorized work remains.
- A blocked provider, unavailable optional tool, missing human acceptance or costly action blocks only dependent work. Record the exact gap and continue independent authorized work. Mandatory evidence still blocks its own gate.
- Stop only when the authorized feasible scope is exhausted, all remaining paths require unavailable evidence/authority or violate a limit, or the runtime imposes a real session/context/quota boundary. On a forced boundary, preserve recoverable state and the next exact action; do not promise background continuation or unlimited runtime.
- Do not reinterpret this mode as authorization for unrelated product scope, architecture changes, destructive operations, real-user notifications or bypassing security/release gates.

The incremental monetary ceiling is **EUR 0** unless the owner explicitly amends it. It covers more than purchases: no paid upgrades, top-ups, separately billed model/API calls, new chargeable resources, trials with payment exposure, billable usage overages or metered provider actions outside verified included allowances. Reusing an existing service is not proof that additional usage is free.

Before a potentially chargeable action, establish that it is included/free within the current authorized entitlement and remaining allowance. If that cannot be established, do not perform that action; record the cost uncertainty and continue other work. Prefer local/ephemeral verification and existing authorized resources. Never alter billing limits or disable safeguards to continue.

Separate the authorized EUR 0 ceiling, actions actually performed and billing evidence actually observed. Do not report an audited EUR 0 invoice merely because no upgrade was purchased.

## Logical continuity

Runtime agent identity is not durable project state. A stopped, closed, lost or post-restart agent is a new process generation even when it continues the same logical role.

Continuity MUST be carried by a durable logical role record containing at least:

- stable `role_id` and incrementing `generation`;
- role charter, non-goals and owned paths;
- exact base, plan and current-head references;
- accepted commits/evidence;
- open findings and blockers;
- verification actually run;
- next exact action.

Never claim that hidden model memory survived a restart. Use `pat-durable-logical-agent-handoff` and `ref-owner-authorized-role-manifest`.

## Required workflow prefix

Every Kappa-Bot subagent spawn prompt under this profile MUST begin exactly:

```text
/caveman Ultra
```

If that workflow is unavailable or inapplicable in the execution environment, record the degradation and use the equivalent Handbook/Superpowers process. Do not fabricate invocation.

## Skill routing

Assign skills by role and stage. Do not load the full installed portfolio into every pod. `pol-agent-operating-model` owns the applicable portfolio, including caveman Ultra, Superpowers, taste, impeccable and Emil Kowalski interaction/design skills.

- parent: only orchestration, planning, verification, worktree and branch-completion skills required by the current stage;
- design-quality: applicable architecture/security/product/design/UX/taste/interaction/prototyping/review skills plus product-owned authority;
- delivery: frozen plan, TDD/debugging/execution skills and only domain/UI skills needed by its owned implementation;
- platform-inapplicable skills: mark `N/A` with a reason instead of invoking them performatively.

Discover installed skills, MCPs, CLIs, versions, authentication and permissions before relying on them; use the smallest applicable set and reuse evidence on unchanged inputs. Prefer available `playwright-cli` for browser exploration and rendered verification when suitable; use the repository's required Playwright/test commands for its actual gates. A screenshot alone is not functional verification. Select the CLI or MCP that provides the required evidence with less context/operational overhead, without weakening safety or the cost ceiling. Do not duplicate the same action through both merely because both exist.

All role prompts reference canonical paths and exact SHAs rather than pasting whole handbooks, specs or research reports.

## Ownership and workspaces

Before parallel write work begins, assign exclusive path ownership or an explicit serialized handoff. Concurrent write-heavy pods MUST NOT target the same files.

Use one normal working tree by default. Additional worktrees are justified only by real same-repository parallel writes with disjoint ownership and must follow `pol-workspace-git-hygiene`.

## Review economy

`design-quality` may act as the independent reviewer because it does not author the implementation diff. The parent performs integration and final exact-head review.

Do not create another reviewer. Review at meaningful risk boundaries, not after every microtask. Critical and Important findings block progression until resolved or explicitly rejected with evidence. Communication savings never waive this gate.

## Token and context efficiency

A role pod receives one complete kickoff packet, then only a material blocker/authority/review delta when necessary:

```text
exact authority paths and SHAs
+ role charter and owned paths
+ megaplan/task range
+ required verification
+ durable handoff path
```

Keep detailed progress, screenshots, findings and test evidence in repository artifacts. Do not repeatedly retransmit them through chat. Avoid busy polling, repeated whole-repository discovery and rerunning expensive checks on unchanged inputs; required final exact-head gates remain intact.

## Verification and completion

The parent MUST independently inspect the integrated diff and run the required exact-head gates before any completion claim. A pod's success message, local partial check or screenshot alone is insufficient.

Final cleanup removes only resources owned by the run and only after proving no unique work will be lost.

## Migration from earlier routing

The 2026-09-30 owner amendment replaces the previous Sol 6.1 xhigh / Astra xhigh / Terra ultra defaults. Preserve historical decisions and completed-run evidence. At the next safe execution boundary, reconcile active consumer instructions/manifests and distributed Handbook projections with this version; record requested and actual routing separately. Updating this repository does not itself install a skill bundle or change an already-running model on a workstation. Use the existing adoption/synchronization procedures and verify the installed revision without overwriting unrelated local configuration.

## Related authority

- `pol-agent-operating-model`
- `pol-workspace-git-hygiene`
- `pol-verification-definition-of-done`
- `pb-owner-authorized-role-pod-execution`
- `pat-durable-logical-agent-handoff`
- `ref-owner-authorized-role-manifest`
- `machine-readable/owner-authorized-role-pods.v1.json`
