---
id: std-owner-authorized-role-pods
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
  - src-git-worktree
last_verified: 2026-09-14
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

Select the role profile before selecting the available model alias. Record the actual model and reasoning level used; never claim a requested alias was used when unavailable.

Kappa-Bot owner defaults are:

- parent/orchestrator: `Sol`, reasoning `xhigh`;
- `design-quality`: `Astra`, reasoning `xhigh`;
- `delivery`: `Terra`, reasoning `ultra`.

The routing intent is strict even when aliases change: the parent preserves continuity and integration; `design-quality` receives scarce high-leverage reasoning; `delivery` receives frozen, already-specified implementation and mechanical work. Runtime availability may require a truthful fallback, but it MUST NOT silently invert responsibilities or invent an unavailable alias.

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
- use a **hard ceiling of three total transmissions** only when a material blocker or authority/head delta genuinely requires one extra exchange;
- no direct `design-quality` ↔ `delivery` messaging;
- no progress chatter, repeated specs, repeated diffs or repeated logs;
- after kickoff, send only deltas and canonical path/SHA references.

Do not automatically dispatch `design-quality` both before and after every implementation. Use its one normal dispatch at the highest-leverage decision or review point for that megaplan. The parent still performs final exact-head verification.

`OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS` remains a narrower compatibility profile for runs that explicitly require both canonical roles, but it MUST NOT introduce `master`/`implementer` or any alternate role taxonomy. Its low-communication limits inherit and tighten this Standard.

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

Assign skills by role and stage. Do not load the full installed portfolio into every pod.

- parent: only orchestration, planning, verification, worktree and branch-completion skills required by the current stage;
- design-quality: applicable architecture/security/product/design/UX/taste/interaction/prototyping/review skills plus product-owned authority;
- delivery: frozen plan, TDD/debugging/execution skills and only domain/UI skills needed by its owned implementation;
- platform-inapplicable skills: mark `N/A` with a reason instead of invoking them performatively.

All role prompts reference canonical paths and exact SHAs rather than pasting whole handbooks, specs or research reports.

## Ownership and workspaces

Before parallel write work begins, assign exclusive path ownership or an explicit serialized handoff. Concurrent write-heavy pods MUST NOT target the same files.

Use one normal working tree by default. Additional worktrees are justified only by real same-repository parallel writes with disjoint ownership and must follow `pol-workspace-git-hygiene`.

## Review economy

`design-quality` may act as the independent reviewer because it does not author the implementation diff. The parent performs integration and final exact-head review.

Do not create another reviewer. Review at meaningful risk boundaries, not after every microtask. Critical and Important findings block progression until resolved or explicitly rejected with evidence.

## Token and context efficiency

A role pod receives one complete kickoff packet, then only a material blocker/authority delta if necessary:

```text
exact authority paths and SHAs
+ role charter and owned paths
+ megaplan/task range
+ required verification
+ durable handoff path
```

Keep detailed progress, screenshots, findings and test evidence in repository artifacts. Do not repeatedly retransmit them through chat.

## Verification and completion

The parent MUST independently inspect the integrated diff and run the required exact-head gates before any completion claim. A pod's success message, local partial check or screenshot alone is insufficient.

Final cleanup removes only resources owned by the run and only after proving no unique work will be lost.

## Related authority

- `pol-agent-operating-model`
- `pol-workspace-git-hygiene`
- `pol-verification-definition-of-done`
- `pb-owner-authorized-role-pod-execution`
- `pat-durable-logical-agent-handoff`
- `ref-owner-authorized-role-manifest`
- `machine-readable/owner-authorized-role-pods.v1.json`
