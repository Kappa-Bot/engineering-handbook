---
id: std-owner-authorized-role-pods
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
  - src-git-worktree
last_verified: 2026-09-02
review_due: 2026-12-02
---

# Owner-Authorized Role Pods

## Purpose

Provide an explicit opt-in operating model for substantial work that benefits from a small number of persistent subagents without making multi-agent execution the default or multiplying prompt, model, tool and coordination cost.

This Standard refines `pol-agent-operating-model`. It does not replace the zero-subagent default.

## Activation

`OWNER_AUTHORIZED_ROLE_PODS` is active only when at least one of these is recorded in the approved task/run manifest:

- the owner explicitly authorizes subagents for the initiative; or
- permitted repository-local authority explicitly authorizes this profile.

The authorization reference MUST be durable and unambiguous. General permission to modify a repository is not permission to spawn subagents.

Without recorded activation, use zero subagents.

## Compact topology

The normal maximum is **two persistent subagents plus the parent orchestrator**:

```text
parent/orchestrator
├── design-quality pod  — research, product/UX/architecture/brand decisions and independent review
└── delivery pod        — implementation, tests, fixes and focused commits
```

One subagent is valid when one cohesive delegated workstream is sufficient.

A third subagent is exceptional. It requires the approved plan to document a genuinely independent workstream or uncovered review risk that cannot be handled safely by the parent or existing pods. The run manifest records the reason and disjoint ownership.

Rules:

- maximum normal subagent count: 2;
- maximum concurrent subagents: 2;
- nested spawning: prohibited;
- only the parent orchestrator may spawn, steer, replace, stop or close subagents;
- never create an agent per route, page, component, test, ticket, finding or checklist item;
- consolidate all tasks of the same responsibility into the same live role pod.

## Persistent live roles

A pod is assigned one cohesive workstream and is reused for that entire workstream while its live context remains reliable. Do not discard and recreate it between milestones merely to obtain a fresh thread.

The parent remains authoritative for:

- shared decisions and scope;
- integration and conflict resolution;
- branch/worktree topology;
- exact-head verification;
- merge, cleanup and final claims.

A subagent report is evidence to inspect, not proof of completion by itself.

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

## Model and reasoning routing

Select the role profile before selecting the available model alias. Record the actual model and reasoning level used; never claim a requested alias was used when unavailable.

Kappa-Bot owner defaults are:

- design, product, UX, brand, architecture and difficult integration/review: strongest suitable general model available; current preferred alias `Sol`, reasoning `xhigh`;
- pure executor following frozen authority: efficient narrow-work model; current preferred alias `Luna`, reasoning `xhigh`;
- exceptional independent read-heavy QA/review: balanced model; current preferred alias `Terra`, reasoning `high` or `xhigh` according to risk.

These are routing defaults, not permanent claims about model availability or capability. Repository/task authority may select a stronger or cheaper profile when justified.

## Required workflow prefix

Every Kappa-Bot subagent spawn prompt under this profile MUST begin exactly:

```text
/caveman Ultra
```

If that workflow is unavailable or inapplicable in the execution environment, record the degradation and use the equivalent Handbook/Superpowers process. Do not fabricate invocation.

## Skill routing

Assign skills by role and stage. Do not load the full installed portfolio into every pod.

- parent: only orchestration, planning, review, verification, worktree and branch-completion skills required by the current stage;
- design-quality: applicable product/design/UX/taste/interaction/prototyping/review skills plus the product-owned design contract;
- delivery: frozen plan, TDD/debugging/execution skills and only the domain/UI skills needed by its owned work;
- platform-inapplicable skills: mark `N/A` with a reason instead of invoking them performatively.

All role prompts reference canonical paths and exact SHAs rather than pasting whole handbooks, specs or research reports.

## Ownership and workspaces

Before parallel write work begins, assign exclusive path ownership or an explicit serialized handoff. Concurrent write-heavy pods MUST NOT target the same files.

Use one normal working tree by default. Additional worktrees are justified only by real same-repository parallel writes with disjoint ownership and must follow `pol-workspace-git-hygiene`.

## Review economy

The design-quality pod may act as the persistent independent reviewer of delivery work because it does not author the implementation diff. The parent performs integration and final exact-head review.

Do not create another reviewer by default. Add one only when the risk matrix identifies an uncovered independent perspective, and close it after that bounded review.

Review at meaningful milestones, not after every microtask. Critical and Important findings block progression until resolved or explicitly rejected with evidence.

## Token and context efficiency

A role pod receives one complete kickoff packet, then only deltas:

```text
exact authority paths and SHAs
+ role charter and owned paths
+ current milestone/task range
+ changed decisions/findings/evidence since last handoff
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
