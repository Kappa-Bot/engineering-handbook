# <Repository Name> — Repository Instructions

This file contains **repo-specific** instructions. Do not duplicate universal handbook policies here; reference their IDs when useful.

## Purpose

<One paragraph describing what this repository owns and what it does not own.>

## Architecture boundaries

- <Boundary / package / service ownership rule>
- <Forbidden dependency or coupling>
- <Provider/runtime constraint>

## Working commands

Use only commands that actually exist in this repository.

```text
bootstrap: <command>
dev:       <command>
check:     <command>
test:      <command>
build:     <command>
```

Remove lines that do not apply. Do not invent placeholder commands in the final repo file.

## Local Definition of Done

For this repository, a normal change requires:

- <required fast checks>
- <scope-dependent checks>
- <CI/review requirements>
- <release evidence if applicable>

Universal truthfulness rules are defined by `pol-verification-definition-of-done`.

## Local decisions and exceptions

- <Link to local ADRs / architecture docs>
- <Document any permitted handbook exception and its scope>

## Context loading

Load specialized handbook artifacts only when relevant to the task. Keep this file concise and repository-specific.
