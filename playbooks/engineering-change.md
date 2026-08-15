---
id: pb-engineering-change
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# Engineering Change Workflow

## Purpose

Provide one proportional workflow for engineering changes from intake to handoff without turning every task into the same ceremony.

This playbook operationalizes, rather than replaces:

- `pol-agent-operating-model`
- `pol-workspace-git-hygiene`
- `pol-reuse-first`
- `pol-verification-definition-of-done`

Repository-local `AGENTS.md`, architecture decisions, commands, and gates remain authoritative for local facts.

## Core flow

```text
intake
  ↓
reuse / research
  ↓
decision / spec / plan when needed
  ↓
implementation
  ↓
verification
  ↓
review / handoff
  ↓
promote reusable learning when justified
```

The stages describe states of work, not mandatory documents. Small work should stay small.

## 1. Intake: define the change

Before editing, establish enough context to avoid solving the wrong problem.

Identify:

- desired outcome;
- repository and area that own the change;
- known acceptance criteria;
- explicit non-scope where scope creep is plausible;
- risk or reversibility concerns;
- applicable local instructions and decisions.

For a mechanical change, this may be a few sentences. For a substantial change, use `templates/task-spec.md` or an equivalent repo-local spec.

### Complexity decision

Use the lightest path that preserves correctness.

**Small / mechanical** — clear change, narrow scope, low risk, established pattern:

```text
inspect → reuse check → implement → relevant verification → handoff
```

**Non-trivial** — multiple files/components, unclear behavior, migration, meaningful design tradeoff, or material failure risk:

```text
inspect → research/reuse → explicit spec/plan → implement → broader verification → review/handoff
```

**Durable architectural decision** — changes boundaries, ownership, platform direction, public contract, or a long-lived constraint:

Record the decision before or with implementation using the repository's ADR mechanism. Use `templates/decision.md` where no local format already exists.

Do not create a plan, ADR, or research document merely because the template exists.

## 2. Search before building

Apply `pol-reuse-first` before designing a new solution.

Use this order unless the task gives a better reason:

1. same repository;
2. Engineering Handbook;
3. other internal repositories/assets;
4. existing internal patterns/templates;
5. mature external solutions and primary sources;
6. new internal design.

The search depth should be proportional to the cost of being wrong. Do not spend an hour researching a trivial local rename, and do not invent a security-sensitive or architectural mechanism after a superficial search.

### Research boundary

Research is appropriate when information is external, volatile, niche, disputed, high-impact, or when an existing solution may materially reduce work or risk.

Keep external facts separate from internal decisions. A source proving that a tool supports a feature does not prove that the organization should adopt it.

If research produces a potentially reusable source or learning, follow `governance/source-authority.md` and `governance/knowledge-promotion.md` rather than pasting the research into permanent agent context.

## 3. Decide and plan proportionally

Before non-trivial implementation, resolve material design questions that would otherwise cause rework.

A useful implementation plan answers:

- what files/areas change;
- what deliberately does not change;
- key interfaces or migration boundaries;
- verification required for the affected scope;
- any ordering/dependency between steps.

The plan SHOULD be executable and concrete, but MUST NOT become a second permanent architecture document.

Once the design is sufficiently resolved, implementation should proceed; do not keep reopening settled decisions without new evidence.

## 4. Prepare the workspace

Follow `pol-workspace-git-hygiene`.

Default operating model:

- one normal working tree;
- one short-lived branch for the change;
- no Git worktree unless explicitly requested or real same-repo parallelism clearly justifies it;
- no unrelated cleanup bundled into the change;
- no repository-resident scratch/review files when OS temp storage is sufficient;
- never destroy unmerged or user work to obtain a clean workspace.

Before editing an existing repository, account for pre-existing modifications so the task does not accidentally absorb somebody else's work.

## 5. Implement narrowly

During implementation:

- preserve the requested outcome as the primary scope;
- follow existing local patterns unless there is a deliberate reason to change them;
- prefer the smallest coherent change over speculative abstraction;
- do not perform unrelated refactors “while here”;
- keep generated/transient artifacts out of the repository unless they are intended deliverables;
- make destructive or irreversible operations explicit;
- update durable docs/contracts when the implementation changes them.

### Tests and debugging

Use TDD when the behavior can be expressed meaningfully and the red/green cycle adds value. Do not manufacture trivial tests just to claim TDD.

When behavior is broken or a test unexpectedly fails, diagnose before changing multiple unrelated things. Reproduce the symptom, identify evidence, form a hypothesis, test it, then apply the narrowest justified correction.

## 6. Verify before claiming completion

Apply `pol-verification-definition-of-done` literally: evidence before claims.

Verification comes from the repository's real commands and scope rules. Do not invent a generic gate that does not exist.

Typical evidence may include:

- focused tests for changed behavior;
- broader affected-suite tests;
- lint/typecheck/static analysis;
- build or packaging;
- migration/schema checks;
- visual/manual evidence where automation does not cover the behavior;
- CI or deployment evidence when the repository requires it.

### Scope-to-gate rule

Run every gate required for the changed scope, not every command in the repository by habit.

If a required gate cannot be run:

- do not report it as passing;
- state what was not run and why;
- distinguish verified behavior from remaining risk.

A diff review is evidence about scope, not evidence that runtime behavior works.

## 7. Review and PR

Before opening or merging a PR, inspect the actual diff with fresh eyes.

Check for:

- unrelated files or cleanup;
- accidental secrets or temporary artifacts;
- stale comments/docs;
- duplicated policy or architecture text;
- scope that no longer matches the task;
- missing verification evidence;
- behavior changes not reflected in contracts or docs.

A concise PR description should communicate:

```text
Problem / outcome
What changed
Important non-scope or tradeoffs
Verification actually run
Checks not run / remaining risk
```

Do not inflate a small PR with ceremonial prose, and do not hide a large behavioral change behind a vague one-line description.

Merge only when the repository's actual review/check requirements are satisfied. Prefer squash for a short task branch when intermediate commits contain only iteration noise; preserve meaningful commit history when the repository has a reason to do so.

## 8. Handoff and workspace state

At handoff report what is useful to the next human/agent:

- outcome delivered;
- main files/areas changed;
- verification actually observed;
- required checks not run;
- remaining risk or dependency;
- branch/PR state when relevant.

The working state should be accounted for. Do not leave unexplained scratch files, abandoned worktrees, destructive cleanup, or unmerged user work hidden behind a “done” claim.

Merged remote branches SHOULD be deleted when repository settings/tooling allow it. Inability to delete a branch through the current tool is a tooling limitation to report, not a reason to force-move the ref.

## 9. Promote reusable learning deliberately

After a real project change, ask whether anything learned is genuinely useful across repositories.

- local and specific → keep it local;
- reusable implementation solution → candidate Pattern;
- repeatable procedure → candidate Playbook;
- recurring technical baseline → candidate Standard;
- mandatory cross-repository behavior → candidate Policy;
- stable rule with worthwhile enforcement → candidate executable asset.

Use `governance/knowledge-promotion.md`; do not automatically promote every lesson.

## Stop conditions

Do not silently push through a material unresolved conflict. Re-evaluate before implementation or merge when:

- requirements conflict in a way that changes the outcome;
- a supposedly local change alters a public or cross-repo contract;
- verification reveals a broader regression;
- the implementation needs destructive action not previously accounted for;
- evidence invalidates the chosen design;
- the change is expanding into a different project.

The goal is not to stop work for every uncertainty. The goal is to prevent hidden assumptions from becoming expensive decisions.

## Definition of done for the workflow

A change is ready for handoff when:

- requested scope is implemented or the remaining gap is stated explicitly;
- unrelated changes are excluded;
- applicable verification has fresh evidence;
- unrun gates are named honestly;
- durable decisions/contracts/docs are updated where necessary;
- branch/PR/workspace state is accounted for;
- reusable learning is promoted only when justified.
