---
id: pb-owner-authorized-role-pod-execution
kind: playbook
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

# Owner-Authorized Role-Pod Execution

## Purpose

Operationalize `std-owner-authorized-role-pods` for one substantial initiative using the smallest useful number of persistent subagents, explicit ownership and durable restart-safe state.

## Entry gate

Before spawning anything, the parent records:

```text
run_id
repository
owner_authorization
base_sha
target_branch
approved_spec + sha
approved_plan + sha
scope boundaries
paid/provider/destructive authority
normal subagent count
maximum concurrency
```

If explicit owner or permitted repository authorization is absent, stop and use the zero-subagent default.

## 1. Consolidate roles before spawning

Partition by cohesive responsibility, not by artifact count.

Default substantial-product topology:

```text
design-quality
  all research, information architecture, product/UX/brand decisions,
  prototypes, design-system authority and milestone/final review

delivery
  all implementation, migrations, tests, fixes and commits
```

The parent keeps integration, shared decisions, conflict resolution, exact-head verification, merge and cleanup.

Use only one pod when the second role would not save more work than it costs. A third pod requires a written exception in the run manifest.

Reject these decompositions:

```text
one agent per page
one agent per component
one agent per test class
one agent per finding
one agent per checklist item
multiple reviewers covering the same risk without a stated reason
```

## 2. Create durable run state

Create a compact repository-local directory appropriate to the initiative, for example:

```text
docs/engineering/agents/<initiative>/
  run.md
  ownership.md
  progress.md
  evidence-index.md
  roles/
    design-quality.md
    delivery.md
  handoffs/
```

Use `ref-owner-authorized-role-manifest` for the run and role fields. Do not create a general task database or daemon.

## 3. Assign ownership

For each live role, record:

- exclusive paths it may modify;
- read-only/shared paths;
- forbidden paths;
- serialized handoff points;
- milestone acceptance criteria.

One shared file has one writer at a time. When ownership moves, both the outgoing handoff and incoming role manifest record the transfer.

## 4. Select workspace topology

Start with one implementation branch/worktree. Use additional worktrees only when two pods must write in parallel to provably disjoint path sets and the repository permits it.

The parent owns:

- creation and cleanup;
- rebases/merges;
- resolution of shared-file conflicts;
- proof that no unique work is discarded.

A subagent does not create or remove another pod's workspace.

## 5. Spawn once

Each spawn prompt begins exactly:

```text
/caveman Ultra
```

The kickoff packet contains only:

```text
role_id + generation
actual model + reasoning
exact authority paths and SHAs
mission and non-goals
owned/forbidden paths
current milestone/task range
required verification
handoff path
```

Record the returned live handle in the role manifest. Keep the same handle alive for the complete assigned workstream.

## 6. Route skills narrowly

Before work, each role records an applicability matrix:

```text
skill/resource | applicable? | reason | stage
```

Do not invoke every installed skill. Use only skills that can materially change the role's decision, implementation or verification. Mark incompatible platform skills `N/A`.

## 7. Execute by milestones

Recommended control loop:

```text
parent freezes milestone scope
→ design-quality produces/updates authority
→ parent accepts exact artifact/sha
→ delivery executes RED → minimum GREEN → refactor while green → focused commits
→ design-quality reviews integrated milestone evidence
→ delivery resolves Critical/Important findings
→ parent runs milestone gates and integrates
→ durable ledgers update
→ same pods continue to next milestone
```

Do not replace pods between milestones. Send only changed decisions, paths, SHAs, findings and evidence as delta prompts.

## 8. Coordinate concurrency

Normal concurrency is at most two subagents.

Safe examples:

- design-quality performs read-only audit while delivery prepares an isolated test harness;
- design-quality reviews a stable milestone while delivery works only on a different, already-frozen disjoint path set.

Unsafe examples:

- both edit shared tokens, navigation or root configuration;
- delivery starts implementation while the design contract governing it is still changing;
- reviewer and delivery race on the same files;
- one pod silently spawns helpers.

When uncertain, serialize.

## 9. Review economy

Use the existing design-quality pod as milestone/final independent reviewer of the implementation. It receives requirements, diff and evidence—not the delivery pod's internal narrative.

The parent reviews integration and final exact head. Add a third reviewer only for a documented uncovered risk; close it after the bounded review.

## 10. Handle compaction, interruption and restart

Before context compaction, parking, shutdown or handoff, update:

```text
current head
accepted commits
owned paths
completed scope
open findings/blockers
verification run
next exact action
```

If a live pod is lost:

1. keep the same `role_id`;
2. increment `generation`;
3. select and record the actual replacement model/reasoning;
4. provide the manifest, exact SHAs and only the necessary delta;
5. require the replacement to inspect current branch/diff before editing;
6. never claim hidden-memory recovery.

## 11. Completion gate

The parent may close the run only after:

- approved scope is mapped to delivered artifacts;
- all required gates were freshly run on exact head;
- Critical/Important findings are zero;
- subagent reports were independently checked;
- merged repository state is verified;
- owned temporary branches/worktrees/resources are safely removed;
- unrun or unreachable evidence is reported truthfully.

## Compact one-shot UI example

For one broad UI recomposition, the default is:

```text
parent/orchestrator: Sol xhigh
subagent design-quality: Sol xhigh
subagent delivery: Luna xhigh
max concurrent subagents: 2
```

`design-quality` owns the complete audit, IA, branding, design system, prototypes and independent UI review. `delivery` owns all implementation tasks throughout the execution. The parent owns decisions, integration, exact-head gates, PRs, merge and cleanup.

This example is a topology pattern, not authorization for any specific product scope.
