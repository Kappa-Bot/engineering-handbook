---
id: pb-repository-adoption
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - all-repositories
  - codex
sources:
  - src-openai-codex-agents
last_verified: 2026-08-15
review_due: 2026-11-15
---

# Repository Adoption

## Purpose

Adopt the Engineering Handbook in a repository without copying the handbook into it or turning `AGENTS.md` into a permanent context dump.

The target state is deliberately small:

```text
global engineering instructions
        +
repo-root AGENTS.md with local facts only
        +
optional deeper AGENTS.md only where local constraints genuinely differ
        +
current task and task-specific context
```

The root `AGENTS.md` is authoritative for repository-local operating context. Universal rules remain canonical in the handbook/global distribution artifact.

Before relying on that layering, verify global Codex adoption using `playbooks/codex-global-adoption.md`. A repo-local `AGENTS.md` can still be discovered without the global file, but universal handbook behavior must not be assumed to be active merely because the repo contract exists.

## What belongs in a repo `AGENTS.md`

Include information that materially changes how an agent should work in this repository:

- repository purpose and ownership boundary;
- real bootstrap/dev/check/test/build commands;
- architecture boundaries that are easy to violate accidentally;
- local Definition of Done or scope-to-gate mapping;
- canonical local architecture/decision references;
- explicit, permitted handbook exceptions;
- persistent local handoff constraints when they differ from the global model.

## What does not belong

Do not copy:

- zero-subagent, no-worktree, reuse-first, scope-control, or verification policies already supplied globally;
- generic coding advice;
- whole architecture documents that can be referenced by path;
- task-specific plans or temporary instructions;
- commands that have not been verified to exist;
- aspirational future architecture presented as current fact;
- handbook source text merely to make the repo “self-contained”.

If removing a paragraph from `AGENTS.md` would not change an agent's behavior in this repository, it is probably unnecessary permanent context.

## Adoption procedure

### 1. Inspect before writing

Read the repository before creating or replacing instructions:

- existing root and nested `AGENTS.md` / `AGENTS.override.md` files;
- README and contributor docs;
- package/task runner configuration;
- CI workflows and real verification gates;
- architecture/ADR docs;
- directory structure and major ownership boundaries.

Do not infer commands from convention when the repository can tell you the exact command.

### 2. Preserve existing useful local knowledge

If an `AGENTS.md` already exists, classify each instruction:

- **universal** → remove duplication and rely on the handbook/global layer;
- **repo-local and durable** → keep or rewrite concisely;
- **directory-local** → move closer to the governed subtree only when doing so improves scope accuracy;
- **task-specific or stale** → remove after confirming it is no longer required;
- **conflicting** → resolve deliberately against handbook precedence and local decisions rather than silently choosing one.

Do not overwrite an existing instruction file from the template without reviewing its content.

### 3. Instantiate the root contract

Use `templates/AGENTS.repo.md` as a checklist, not as text that must all survive.

Delete empty/inapplicable sections. The finished repo file should normally be substantially shorter than the template.

Prefer a compact command map such as:

````markdown
## Working commands

```text
check: npm run check
test:  npm test
build: npm run build
```
````

instead of generic prose explaining how tests work.

### 4. Decide whether nested instructions are justified

Codex discovers project instructions from the repository root toward the current working directory and gives later/closer instructions higher precedence according to its own discovery semantics.

Create a nested `AGENTS.md` only when a subtree has durable constraints that should not burden unrelated work, for example:

- a frontend package with its own commands and UI constraints;
- infrastructure code with distinct deployment gates;
- a generated-code directory with special editing restrictions.

Do not create one per folder by convention.

### 5. Verify the repository contract

Before adoption is considered complete:

- every documented command exists or is explicitly scope-qualified;
- referenced paths/docs exist;
- no placeholder tokens remain;
- no universal policy has been needlessly recopied;
- no stale task-specific instruction remains;
- local exceptions, if any, are explicit and permitted;
- instruction scope matches where the file is located.

### 6. Verify Codex discovery

Start a new Codex session/run from the repository after changing instructions.

Use an instruction probe such as:

```powershell
codex --ask-for-approval never "Summarize the current instructions and distinguish global from repository-specific guidance."
```

Check that the observed local guidance matches the repository contract. Do not treat the file merely existing in Git as proof that the intended instruction chain is active.

## Existing repositories vs new repositories

### Existing repository

Prefer reduction over replacement. Preserve valid local knowledge, remove global duplication, verify real commands, then add only missing local boundaries.

### New repository

Start from `templates/AGENTS.repo.md`, but commit only populated sections. A new repo should not inherit placeholder sections or guessed gates.

## Promotion back to the handbook

Repository adoption is also a learning loop. When the same local instruction repeatedly appears across repositories, ask whether it should be promoted through `governance/knowledge-promotion.md`.

Do not solve repeated duplication by copy-pasting the same rule into more `AGENTS.md` files.

## Definition of done

A repository is handbook-adopted at the instruction layer when:

- its root `AGENTS.md` contains concise, verified repo-local context;
- universal behavior is not duplicated unnecessarily;
- nested instruction files exist only where scoped differences justify them;
- commands and references have been checked against the repository;
- global instruction adoption has been checked rather than assumed;
- a fresh Codex run has demonstrated the expected instruction chain;
- unresolved conflicts or permitted exceptions are recorded rather than hidden.

This playbook intentionally does not define a central registry of adopted repositories or automatic file generation. Those mechanisms should be added only if real pilot adoption shows they reduce meaningful drift or effort.
