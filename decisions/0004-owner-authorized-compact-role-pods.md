---
status: accepted
date: 2026-09-02
decision-makers:
  - owner
  - engineering
consulted: []
informed: []
---

# Add owner-authorized compact role pods with durable logical identity

## Context and problem statement

The Handbook intentionally defaults to zero subagents because unnecessary delegation multiplies prompt, model, tool and coordination cost. Some explicitly owner-authorized initiatives are nevertheless broad enough to benefit from parallel or specialized work, particularly when product/design authority, implementation and independent review are distinct responsibilities.

The earlier guidance allowed subagents when useful but did not define:

- how aggressively roles should be consolidated;
- who may spawn and integrate;
- how many agents are normally justified;
- how model/reasoning profiles are selected;
- how all Kappa-Bot subagents receive `/caveman Ultra`;
- how one live agent is reused across many related milestones;
- how continuity works after a thread is stopped or a machine restarts;
- how token savings are measured without weakening verification.

A first implementation attempt used a self-modifying bootstrap workflow. It accumulated failed commits while the intended canonical corpus never reached the branch. That mechanism was rejected: governance artifacts must be committed directly and verified by the normal Handbook pipeline.

## Decision drivers

- preserve zero subagents as the universal default;
- require explicit owner/repository authorization;
- minimize role and concurrency count;
- reuse one live agent per cohesive responsibility;
- keep the parent authoritative for integration and final claims;
- survive process loss without pretending hidden memory is durable;
- reduce repeated context transmission;
- keep model/skill use truthful and proportional;
- preserve normal Handbook compilation, integrity and distribution behavior.

## Considered options

### One fresh subagent per task

Simple task assignment but maximizes rediscovery, prompt duplication and review/coordination cost. Rejected.

### Five or more persistent specialist agents

Provides narrow specialization but over-partitions most initiatives and creates shared-file conflicts. Rejected as a default.

### Three permanent subagents: design, implementation and QA

Stronger separation, but the independent design authority can already review implementation while the parent performs final integration review. A third permanent reviewer is unnecessary for most work.

### Two persistent role pods plus parent orchestrator

Chosen. The normal roles are `design-quality` and `delivery`. The parent owns shared decisions, integration, exact-head verification, merge and cleanup. A third bounded reviewer is exceptional and must be justified by uncovered risk or a genuinely independent workstream.

## Decision outcome

Adopt the opt-in profile `OWNER_AUTHORIZED_ROLE_PODS`.

Normal topology:

```text
parent/orchestrator
├── design-quality — all research, UX/product/brand authority and independent implementation review
└── delivery       — all implementation, tests, fixes and focused commits
```

Constraints:

- explicit durable authorization is required;
- normal maximum is two subagents;
- maximum concurrency is two;
- nested spawning is prohibited;
- only the parent spawns, integrates and closes;
- one role owns every task of its type for the complete initiative;
- every Kappa-Bot spawn prompt starts with `/caveman Ultra`;
- role/model/skill selection is recorded truthfully;
- a lost agent becomes a new generation of the same logical role;
- durable manifests, exact SHAs, ownership and evidence—not hidden memory—carry continuity;
- exact-head verification remains mandatory.

Canonical artifacts:

- `standards/owner-authorized-role-pods.md`;
- `playbooks/owner-authorized-role-pod-execution.md`;
- `patterns/durable-logical-agent-handoff.md`;
- `references/owner-authorized-role-manifest.md`;
- `machine-readable/owner-authorized-role-pods.v1.json`.

## Consequences

### Positive

- lower prompt and model overhead than microtask spawning;
- stable responsibility across long executions;
- one independent implementation reviewer without a permanent third agent;
- deterministic restart/recovery contract;
- fewer write conflicts;
- portable cross-repository behavior;
- truthful record of actual models, skills and evidence.

### Tradeoffs

- the design-quality role carries both design authority and implementation review, so the parent must still perform final integration review;
- durable manifests add a small documentation cost;
- a live role may accumulate stale context and must be replaced when its assumptions are no longer reliable;
- exact model aliases may change, so aliases are owner defaults rather than permanent capability claims.

## Re-evaluation triggers

Revisit when:

- repeated initiatives prove two pods insufficient or consistently excessive;
- Codex provides a durable native role/thread identity with verified restart semantics;
- nested orchestration becomes safe and materially cheaper;
- model aliases or pricing invalidate the routing defaults;
- evidence shows the manifest cost exceeds the context it saves;
- independent review quality suffers from combining design and QA.

## Sources

- `src-openai-codex-agents`
- `src-openai-codex-skills`
- `src-git-worktree`
