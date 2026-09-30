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

**Latest owner amendment (2026-09-30, Platform Core continuation):** supersedes the earlier routing amendment below. Requested defaults are now `Sol 6.1 high` for the parent, `Astra 6 xhigh` for `design-quality`, and `Luna 6 xhigh` for `delivery`. The owner also requests continuation through all feasible authorized work without incremental monetary cost, minimal communication/tokens and relevant use of caveman Ultra, Superpowers, taste, impeccable, Emil Kowalski, playwright-cli and available MCPs/CLIs. `std-owner-authorized-role-pods` version 1.3 is the current normative authority, including EUR 0 controls, real runtime boundaries, necessary safety/review communication exceptions and migration of active consumer/distributed instructions. Topology, independent review, scope and sensitive-action gates remain intact. Updating the Handbook does not itself configure a workstation or live model.

The earlier amendment and decision outcome below are preserved as historical evidence, not current model routing or an exception to the current Standard.

**Routing amendment (2026-09-30):** the owner-default parent/orchestrator is now `Sol 6.1` at `xhigh`. Role topology and delegated defaults are unchanged.

## Context and problem statement

The Handbook intentionally defaults to zero subagents because unnecessary delegation multiplies prompt, model, tool and coordination cost. Some explicitly owner-authorized initiatives nevertheless benefit from a tiny number of persistent specialized roles.

The operating model must define role consolidation, spawn authority, model routing, communication cost, durable continuity and exact-head verification without turning every plan into an agent swarm.

## Decision drivers

- preserve zero subagents as the universal default;
- require explicit owner/repository authorization;
- minimize role count and inter-agent traffic;
- keep only stable cohesive role types;
- keep the parent authoritative for continuity, integration, Production and final claims;
- spend the strongest delegated reasoning only on high-leverage decisions/review;
- route bulk frozen implementation to the efficient implementation role;
- survive process loss without pretending hidden memory is durable;
- preserve normal Handbook integrity/distribution behavior.

## Considered options

### One fresh subagent per task

Rejected: maximizes rediscovery, prompt duplication and coordination cost.

### Multiple specialist/reviewer agents

Rejected: over-partitions initiatives, creates shared-file conflicts and burns context on coordination.

### Parent plus two persistent role pods

Chosen. Only `design-quality` and `delivery` are delegated roles. The parent is not a subagent and remains the integration/verification authority.

## Decision outcome

Adopt opt-in `OWNER_AUTHORIZED_ROLE_PODS` with this owner-default topology:

```text
parent/orchestrator — Sol 6.1 xhigh
├── design-quality — Astra xhigh
└── delivery       — Terra ultra
```

Responsibilities:

- parent: orchestration/context continuity, integration/conflicts, Git/worktrees, Production/provider actions, exact-head verification, final claims/blocker decisions;
- `design-quality`: high-leverage architecture, security/contracts, product/UX/UI/design, ambiguous trade-offs, difficult diagnosis and independent review when that is the highest-value dispatch;
- `delivery`: implementation from frozen authority, TDD, settled-behavior debugging, mechanical refactors/migrations/config/docs and unambiguous fixes.

Constraints:

- explicit durable authorization required;
- at most two subagents and only the two canonical roles;
- no third reviewer/specialist role;
- maximum concurrency two;
- nested spawning prohibited;
- only parent spawns/integrates/closes;
- every spawn starts `/caveman Ultra`;
- target one parent dispatch + one final handoff per role per megaplan;
- target two total transmissions; hard maximum three only for a material blocker or authority/head delta;
- no direct delegate-to-delegate messaging or progress chatter;
- durable repo state carries continuity;
- role/model/skill selection is recorded truthfully;
- lost runtime becomes a new generation of the same logical role;
- parent exact-head verification remains mandatory.

`OWNER_AUTHORIZED_TWO_AGENT_LOW_COMMS` may be used as a stricter compatibility delta when both canonical roles are required, but it does not create `master`/`implementer` or any alternate taxonomy.

## Consequences

### Positive

- substantially lower prompt/model/coordination overhead;
- strongest delegated reasoning concentrated on decisions/review instead of mechanical work;
- bulk implementation stays on a cheaper execution role;
- stable responsibility across long executions;
- deterministic restart/recovery contract;
- fewer write conflicts and less status chatter;
- portable cross-repository behavior.

### Tradeoffs

- parent must perform final integration review because no third reviewer exists;
- `design-quality` cannot be automatically spent both before and after every implementation without violating the communication objective;
- durable manifests add a small documentation cost;
- runtime model aliases may change, so actual values must always be recorded truthfully.

## Re-evaluation triggers

Revisit when model availability/pricing materially changes, native durable role identity changes restart semantics, or evidence shows this communication/model routing reduces quality or costs more than it saves.

## Sources

- `src-openai-codex-agents`
- `src-openai-codex-skills`
- `src-git-worktree`
