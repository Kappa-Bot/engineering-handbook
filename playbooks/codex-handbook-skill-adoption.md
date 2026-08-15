---
id: pb-codex-handbook-skill-adoption
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - codex
  - developer-workstations
sources:
  - src-openai-codex-skills
last_verified: 2026-08-15
review_due: 2026-11-15
---

# Codex Engineering Handbook Skill Adoption

## Purpose

Install the Engineering Handbook as one user-level Codex skill so cross-repository procedures and references can be loaded through progressive disclosure instead of permanent global prompt context.

The canonical skill definition is:

`agent-config/codex/skills/engineering-handbook/SKILL.md`

The canonical bundle definition is:

`agent-config/codex/skills/engineering-handbook/bundle.json`

The default installed location is:

`$HOME/.agents/skills/engineering-handbook`

The installed `references/` tree is generated from canonical handbook files. It is a distribution artifact and MUST NOT be edited as an independent source of truth.

## Why one user-level skill

Codex supports a USER skill scope for workflows relevant across any repository. Skills also use progressive disclosure: only skill discovery metadata is present initially; the full `SKILL.md` is loaded when the skill is selected.

Start with one `engineering-handbook` router skill rather than one skill per policy/playbook. This minimizes initial skill-list pressure while still allowing the selected skill to load only the handbook references relevant to the current task.

A plugin is deliberately deferred. User-scope installation fits a single developer's cross-repository setup; reassess plugin packaging when the skill must be distributed to other people, bundled with connectors, or centrally managed.

## What gets installed

`sync-handbook-skill.ps1` installs:

- the canonical `SKILL.md`;
- generated `references/` copied from the paths/directories declared in `bundle.json`;
- `install-manifest.json` with source paths and SHA-256 values for traceability.

Adding a new canonical playbook under an included handbook directory automatically makes it part of the next generated bundle without manually maintaining a second reference list.

## 1. Check current state

From a local checkout of the handbook:

```powershell
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Check
```

States:

- `IN_SYNC` (`0`) — installed skill and generated references match canonical sources;
- `MISSING` (`1`) — user skill is not installed;
- `OUT_OF_SYNC` (`2`) — an expected file differs/is missing or an unexpected stale file exists.

## 2. Preview installation

For a missing skill:

```powershell
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Install -WhatIf
```

If an existing `engineering-handbook` skill directory differs:

```powershell
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Install -BackupExisting -WhatIf
```

The script never replaces an existing skill directory silently.

## 3. Install

```powershell
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Install
```

If a differing target already exists:

```powershell
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Install -BackupExisting
```

A replaced target is moved beside the installed directory using a timestamped `engineering-handbook.backup-*` name.

## 4. Verify source synchronization

```powershell
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Check
```

Do not claim file-level adoption is complete unless the result is `IN_SYNC`.

## 5. Verify Codex discovery and activation

Codex normally detects skill changes automatically; if the skill is not visible, restart Codex.

Use `/skills` in Codex CLI/IDE and confirm `engineering-handbook` is present.

Then explicitly invoke the skill with a representative prompt, for example:

```text
$engineering-handbook For a non-trivial engineering change, tell me which handbook playbook and policies you would load first. Do not load unrelated references.
```

Expected behavior:

- the skill identifies the relevant workflow;
- it loads/selects only the needed references rather than the whole bundle;
- it distinguishes repo-local instructions from cross-repository handbook guidance.

After explicit behavior is reliable, observe implicit activation on representative tasks. The skill description is intentionally scoped away from trivial repo-local edits.

## Duplicate-name check

Codex does not merge same-name skills from different discovery locations. If `/skills` shows more than one `engineering-handbook`, identify the repo/user source intentionally rather than assuming one overrides the other.

Do not create repo-local copies of this cross-repository skill merely to make it available inside a repository.

## Isolated script testing

Use `-SkillsHome` to test installation without touching the real user skill directory:

```powershell
$tempSkillsHome = Join-Path $env:TEMP "engineering-handbook-skills-test"
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Install -SkillsHome $tempSkillsHome
pwsh -File .\automation\codex\sync-handbook-skill.ps1 -Mode Check -SkillsHome $tempSkillsHome
Remove-Item -Recurse -Force $tempSkillsHome
```

## Rollback

If a backup was created:

1. stop/restart Codex if it may have loaded the current skill;
2. remove or move aside the handbook-installed `engineering-handbook` target;
3. restore the desired timestamped backup to `engineering-handbook`;
4. run `/skills` and an explicit invocation to verify the intended skill is active.

## Definition of done

Skill adoption is complete for a workstation when:

- `Check` reports `IN_SYNC`;
- `/skills` shows one intended `engineering-handbook` user skill;
- explicit invocation works on a representative task;
- selected behavior demonstrates reference-level progressive disclosure rather than bulk loading;
- generated references have not become independently edited sources of truth.
