---
id: pb-owner-authorized-role-pod-execution
kind: playbook
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

# Owner-Authorized Role-Pod Execution

## Purpose

Operationalize `std-owner-authorized-role-pods` for one substantial initiative using the smallest useful number of persistent subagents, explicit ownership, low communication and durable restart-safe state.

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
active delegated roles
maximum concurrency
```

If explicit owner or permitted repository authorization is absent, stop and use the zero-subagent default.

## 1. Freeze the only delegated role types

The parent is not a subagent. Owner-default routing is:

```text
parent/orchestrator — Sol xhigh
  orchestration, continuity, integration, git/worktrees, Production,
  exact-head verification, final claims and blocker decisions

design-quality — Astra xhigh
  architecture, security/contracts, product/UX/design, ambiguous trade-offs,
  difficult diagnosis and the highest-leverage independent review point

delivery — Terra ultra
  frozen-plan implementation, TDD, mechanical fixes/refactors/migrations,
  docs/config synchronization and focused commits
```

Only `design-quality` and `delivery` may be delegated under this profile. One pod is valid. Both are valid when useful. No third delegated role exists.

Use only one pod when the second role would not save more work or risk than it costs.

Reject these decompositions:

```text
one agent per page/component/test/finding/checklist item
microtask fan-out
separate QA/reviewer role
parallel specialist taxonomy beyond design-quality + delivery
```

## 2. Create compact durable run state

Create only the repository-local state needed for recovery, for example:

```text
docs/engineering/agents/<initiative>/
  run.md
  progress.md
  roles/
    design-quality.md
    delivery.md
  handoffs/
```

Use `ref-owner-authorized-role-manifest`. Do not create a general task database or daemon.

## 3. Assign ownership

For each live role, record writable, read-only and forbidden paths plus acceptance criteria. One shared file has one writer at a time. Ownership transfer is explicit.

`design-quality` normally authors decision/design/review artifacts only, not the implementation diff. `delivery` is the implementation writer. The parent integrates and resolves conflicts.

## 4. Select workspace topology

Start with one implementation branch/worktree. Add another worktree only for real same-repository disjoint parallel writes and only when repository policy permits it.

The parent owns creation/cleanup, merge/rebase/conflict resolution and proof that no unique work is discarded.

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
mission/non-goals
owned/forbidden paths
megaplan/task range
required verification
handoff path
```

Target one parent dispatch per active role for the entire cohesive megaplan. Reference files and SHAs instead of pasting durable authority.

## 6. Enforce the communication budget

For each role per megaplan:

```text
target parent dispatches: 1
target total transmissions: 2  # kickoff + final handoff
hard ceiling: 3                # only one material blocker/authority delta may add an exchange
```

No direct subagent-to-subagent messaging. No progress chatter. No repeated specs, diffs or logs. Repository artifacts are the shared memory.

A role should continue through routine/recoverable friction without asking the parent to restate authority. Use the extra exchange only for a material blocker or changed authority/head that makes safe continuation impossible.

## 7. Route skills narrowly

Process skills first, then only the domain/design skills that can materially change the role's work. Do not load the complete installed skill portfolio into every role.

- parent: orchestration/planning/verification/integration skills for the current stage;
- design-quality: applicable architecture/security/product/design/UX/review skills;
- delivery: frozen authority + TDD/debugging/execution/domain skills needed to implement it.

Mark inapplicable skills `N/A`; do not invoke performatively.

## 8. Execute the megaplan with minimal handoffs

Preferred loop:

```text
parent resolves/freeze scope + authority
→ optionally dispatch design-quality ONCE at the highest-leverage unresolved decision/review point
→ parent accepts durable decision/review artifact
→ dispatch delivery ONCE with the frozen megaplan
→ delivery executes through all specified tasks, tests, fixes and commits
→ optional single blocker/authority delta only if materially necessary
→ delivery writes final durable handoff
→ parent integrates and runs exact-head verification
```

Do not automatically use `design-quality` both before and after every delivery pass. If architecture/design is already settled, reserve Astra for the final high-risk review only when that review is materially valuable. If final review is unnecessary, the parent performs exact-head review directly.

Do not stop a megaplan at every milestone just to exchange status messages. Milestone state belongs in the repo.

## 9. Coordinate concurrency conservatively

Maximum concurrent subagents is two, but low communication matters more than parallelism. Serialize whenever shared authority or paths could race.

Safe concurrency requires disjoint ownership and already-frozen contracts. Neither role may silently spawn helpers.

## 10. Handle compaction, interruption and restart

Before compaction/parking/shutdown, durable state must contain:

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
3. record actual replacement model/reasoning;
4. provide manifest, exact SHAs and only the required delta;
5. reconcile current branch/diff before editing;
6. never claim hidden-memory recovery.

A replacement generation is not a new specialist role and does not expand the two-role limit.

## 11. Completion gate

The parent closes the run only after:

- approved scope maps to delivered artifacts;
- required exact-head gates were freshly run;
- Critical/Important findings are zero or explicitly dispositioned with evidence;
- delegate reports were independently checked;
- Production/provider state is verified when applicable;
- merged repository state is verified;
- owned temporary branches/worktrees/resources are safely removed;
- unrun/unreachable evidence is reported truthfully.

## Compact one-shot example

```text
parent: Sol xhigh
design-quality: Astra xhigh
delivery: Terra ultra
max delegated roles: 2
normal dispatches per role per megaplan: 1
normal total transmissions per role: 2
hard ceiling of three transmissions per role: material blocker/authority delta only
```

This is the owner-default topology, not authorization for any product scope. Explicit durable activation remains required.
