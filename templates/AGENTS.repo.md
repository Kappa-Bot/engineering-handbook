# <Repository Name> — Repository Instructions

This file contains **repo-specific** instructions for agents working in this repository.

Do not copy universal handbook policies into this file. The global agent configuration and handbook remain canonical for cross-repository behavior. This file should add only the context that is true specifically here.

## Repository purpose

<One short paragraph describing what this repository owns, who/what consumes it, and what is explicitly outside its responsibility.>

## Architecture boundaries

Record only boundaries that materially constrain changes.

- <Primary package/service/domain boundary>
- <Allowed or forbidden dependency/coupling>
- <Provider/runtime/data ownership constraint>

Remove this section if the repository has no meaningful local boundary beyond what its code already makes obvious.

## Working commands

List commands that actually exist and that an agent should prefer for normal work.

```text
bootstrap: <command>
dev:       <command>
check:     <command>
test:      <command>
build:     <command>
```

Delete inapplicable lines. A committed `AGENTS.md` MUST NOT contain invented placeholder commands.

If checks are scope-dependent, state the mapping instead of pretending every change needs every command.

## Local Definition of Done

Describe only repository-specific gates beyond the universal truthfulness requirement in `pol-verification-definition-of-done`.

- <fast check required for most code changes>
- <scope-dependent test/build/typecheck/lint rule>
- <review or release evidence required for specific areas>

If the repository already has a canonical contributor/testing document, reference it instead of duplicating it.

## Local decisions and exceptions

- <Path/link to architecture decisions or other canonical repo-local docs>
- <Any explicitly permitted handbook exception and its exact scope>

Remove this section when there are no material local decisions to surface.

## Context loading

- Load specialized handbook policies, standards, patterns, playbooks, references, or skills only when the task requires them.
- Add nested `AGENTS.md` files only for directories with genuinely different local instructions.
- Keep instructions close to the code they govern; do not move package-specific detail into the root file merely to centralize it.
- Prefer references to canonical repo docs over duplicated prose.

## Handoff notes

Document persistent repository-specific handoff expectations only when they differ from the global operating model.

<Optional local requirement; remove this section if none exists.>
