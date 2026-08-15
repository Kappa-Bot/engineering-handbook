---
id: pb-new-repository-bootstrap
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - new-repositories
  - all-repositories
sources: []
last_verified: 2026-08-15
review_due: 2027-02-15
---

# New Repository Bootstrap

## Purpose

Create a new repository that starts with a clear ownership boundary, real working commands, minimal permanent agent context, and an evidence-based verification path without pre-installing speculative architecture or process.

This playbook defines the **engineering contract**, not a universal code scaffold. Stack-specific templates and automation should appear only after repeated real projects prove that they save more effort than they create.

Use together with:

- `pb-repository-adoption` for the repo-local agent contract;
- `pb-engineering-change` for the first implementation change;
- `pol-reuse-first` before choosing or building reusable infrastructure;
- `pol-workspace-git-hygiene` for branch/workspace behavior;
- `pol-verification-definition-of-done` for truthful gates.

## Target state

A newly bootstrapped repository should be understandable without a long verbal briefing:

```text
clear purpose and ownership
        +
minimal source/config structure that actually exists
        +
real local commands
        +
small repo AGENTS.md
        +
explicit local verification contract
        +
durable decisions only where needed
        ↓
ready for the first engineering change
```

The goal is not “complete project infrastructure”. The goal is a trustworthy starting point that can evolve from evidence.

## 1. Define repository ownership before structure

State the repository's responsibility in one short paragraph before deciding its folder tree or framework.

Resolve:

- what capability/product/component the repository owns;
- who or what consumes it;
- what it explicitly does **not** own when the boundary is easy to confuse;
- whether it is an application, shared package, service, infrastructure repository, documentation repository, or another clear ownership unit;
- whether splitting this work into a separate repository actually improves ownership or creates unnecessary coupling/coordination.

Do not create a repository merely because a subdirectory could become one.

## 2. Search before choosing the starting architecture

Before selecting a framework, scaffold, package layout, auth solution, CI pattern, deployment mechanism, or reusable component:

1. check the Engineering Handbook;
2. check relevant internal repositories and Platform Core/shared assets;
3. inspect mature external solutions when the decision is material;
4. use `pb-external-solution-evaluation` for expensive or durable external choices;
5. design new infrastructure only when existing options do not fit.

A new repository is not permission to redesign solved company-wide concerns from zero.

## 3. Decide only what is needed to start

Make enough technical decisions to create a coherent first vertical slice. Defer decisions that are not yet exercised.

Typical early decisions may include:

- runtime/language/framework where required by the product;
- package/dependency manager;
- deploy/runtime target when it constrains architecture;
- data/API ownership when the first slice needs it;
- repository visibility and licensing where relevant;
- initial verification commands.

Do **not** create ADRs for obvious/reversible defaults. Record an ADR when a choice is durable, expensive to reverse, affects public/cross-repo contracts, or establishes a long-lived architectural boundary.

## 4. Create the minimum useful repository surface

Create only files/directories with an immediate purpose.

A typical repository may need some of:

```text
README.md
AGENTS.md
.gitignore
<dependency/package manifest>
<lockfile>
<source root>
<tests only when tests exist>
<env example only when documented configuration exists>
<tool configuration only for tools actually used>
```

This is not a mandatory file list.

### Avoid bootstrap debris

Do not add:

- empty `docs/`, `tests/`, `scripts/`, `infra/`, `packages/`, `src/` subtrees for hypothetical future work;
- placeholder CI workflows that run no meaningful gate;
- unused lint/format/test tools “because every repo should have them”;
- example secrets or real credentials;
- duplicate handbook policies;
- architecture documents that describe a future system as if it already exists;
- generated sample code that will immediately be deleted unless the scaffold itself is the chosen implementation.

Git does not need empty directories to communicate an architecture plan.

## 5. Establish a human entry point

The initial `README.md` should answer the questions a new engineer/agent actually needs:

- what this repository is;
- how to bootstrap/run it when those operations already exist;
- where important repo-local architecture or operational docs live;
- maturity/status caveats when the repository is intentionally incomplete.

Do not turn the README into a copy of the Engineering Handbook or an exhaustive reference manual.

## 6. Establish real working commands

Determine commands from the actual stack and configuration, not convention.

Prefer a small stable command surface such as:

```text
bootstrap: <actual command>
dev:       <actual command>
check:     <actual fast validation command>
test:      <actual command, if present>
build:     <actual command, if present>
```

Delete operations that do not exist.

If the ecosystem supports a task runner/package-script layer, prefer stable project commands over instructions that require agents to remember low-level tool invocations.

The command names do not need to be identical across technology stacks; the repo contract must state the real commands precisely.

## 7. Create the repo-local AGENTS.md

Use `templates/AGENTS.repo.md` through `pb-repository-adoption`.

The committed file should contain only durable local facts such as:

- purpose/ownership boundary;
- actual commands;
- architecture constraints easy to violate;
- local Definition of Done / scope-to-gate mapping;
- local decision references;
- explicit permitted exceptions.

Delete template placeholders and empty sections before committing.

Universal instructions belong in the global handbook distribution, not in every new repository.

## 8. Define the first real verification contract

A repository is not required to have every possible gate on day one. It is required to be truthful about the gates it actually has.

For the current scope, identify:

- the fastest meaningful local check;
- behavior tests if behavior exists and automated testing is useful;
- build/type/lint/static checks required by the selected stack;
- manual evidence that remains necessary;
- deployment/release verification only when deployment/release exists.

Record the scope-to-gate relationship in repo-local instructions or the repository's canonical testing/contribution doc.

Do not claim “CI-ready”, “production-ready”, or equivalent status merely because configuration files exist.

## 9. Handle configuration and secrets deliberately

When the first implementation requires environment-specific configuration:

- document required variable names and meaning;
- commit safe examples/templates only;
- keep real credentials/secrets out of Git;
- make local bootstrap behavior explicit;
- avoid inventing a generalized secret-management layer before the deployment/runtime actually needs one.

A broader security baseline will belong in a future applicable Standard; this bootstrap playbook does not pretend to define it.

## 10. Establish Git/GitHub behavior proportionally

Follow `pol-workspace-git-hygiene` from the first real change.

Default:

- `main` as the stable/default branch unless the repository has a concrete reason otherwise;
- short-lived task branches;
- PR/review flow for non-trivial changes when GitHub collaboration is in use;
- squash intermediate iteration noise when that produces the clearest history;
- delete merged remote branches when settings/tooling safely support it.

Do not add branch rulesets, required reviewers, CODEOWNERS, release workflows, labels, bots, or reusable CI merely to imitate a large organization. Add them when the repository's collaboration/risk model creates a real enforcement need.

## 11. Verify the bootstrap itself

Before calling the repository bootstrapped, verify:

- README claims match the repository's actual state;
- every command documented in `AGENTS.md` exists and has been run where the environment permits;
- placeholders have been removed from committed files;
- referenced paths exist;
- `.gitignore` covers actual local/generated sensitive noise relevant to the stack;
- no credentials, temp files, generated debris, or unrelated scaffold content are committed;
- the intended global instructions and handbook skill are available or the missing adoption is stated explicitly;
- a fresh Codex run sees the expected repo-local instruction chain when Codex is part of the workflow.

If a gate cannot be executed in the current environment, record it as **not run** rather than downgrading it silently.

## 12. Start product work through the normal change workflow

After bootstrap, stop treating the repository as special.

The first product/engineering increment should use `pb-engineering-change`:

```text
intake → reuse/research → decision/plan if needed → implementation → verification → PR/handoff
```

Do not keep accumulating “bootstrap infrastructure” before delivering a real capability. Let real product work reveal which shared templates, standards, CI, automation, or platform services deserve promotion.

## Promotion loop

When the same bootstrap decision repeatedly appears across independent repositories:

- recurring optional solution → candidate Pattern/Template;
- recurring procedure → candidate Playbook improvement;
- recurring technical baseline → candidate Standard;
- stable enforceable requirement → candidate automation/CI/ruleset.

Use `gov-knowledge-promotion`. Repetition is evidence; one new repository is not.

## Definition of done

A repository is bootstrapped when:

- its ownership boundary is clear;
- the minimum real project surface exists without speculative directories/tooling;
- README and repo-local `AGENTS.md` describe the actual current repository;
- working commands and applicable verification are explicit;
- durable decisions are recorded only where warranted;
- configuration/secrets are not represented by real credentials in Git;
- the first normal engineering change can begin without another round of operating-model setup;
- remaining unimplemented capabilities are described as future work, not masquerading as current infrastructure.
