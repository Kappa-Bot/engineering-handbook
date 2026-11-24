---
id: pb-codex-handbook-skill-adoption
kind: playbook
status: active
owner: engineering
version: "0.3"
applies_to:
  - codex
  - developer-workstations
sources:
  - src-openai-codex-skills
last_verified: 2026-11-21
review_due: 2027-02-19
---

# Codex Engineering Handbook Skill Adoption

## Managed installation and manual updates

[Handbook Discovery and Update](handbook-discovery-and-update.md) owns the current manual-only policy. Run `python automation/codex/handbook_update.py install` explicitly from a trusted checkout. Use `--backup-existing` when replacing an unmanaged installation. The managed workflow verifies and retains immutable snapshots. Use its manual `doctor` and `preflight` commands for local integrity and remote freshness.

The PowerShell workflow below distributes an unenrolled bundle. The portable Python entry point is `python automation/codex/handbook_update.py bundle --source . --skills-home "<skills-home>"`, with `--check` or `--backup-existing` as appropriate. Both use the trusted checkout's Python 3.10+ compiler to verify the bundled corpus before replacing a target. Windows PowerShell 5.1 delegates to the portable Python v1 bundle engine; it does not require the .NET Core path helpers or PowerShell 7 JSON switches. PowerShell 7 retains its existing path and verification contract. The portable `bundle --preview` is read-only and is not a freshness or installation receipt. Both paths require an explicit backup for replacement and refuse enrolled targets. Use the managed installer for enrolled targets.

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

- `IN_SYNC` (`0`) — installed bytes match canonical sources and their compiled corpus passes freshness verification;
- `MISSING` (`1`) — user skill is not installed;
- `OUT_OF_SYNC` (`2`) — an expected file differs, a file is missing or unexpected, or the corpus verifier rejected the bundle.

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

A replaced target is moved to the sibling `skill-backups/` directory with a unique `engineering-handbook.backup-*` name (timestamp or UUID according to the installer). The default backup directory is `$HOME/.agents/skill-backups`, outside the skill discovery directory.

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

If `/skills` shows more than one `engineering-handbook`, inspect the source paths. Codex can discover historical copies under `.agents/skills/engineering-handbook.backup-*`. Preserve those directories in `.agents/skill-backups`, check for name collisions before moving them, and verify discovery again.

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
3. restore the desired timestamped backup from `skill-backups` to the active `engineering-handbook` path;
4. run `/skills` and an explicit invocation to verify the intended skill is active.

## Definition of done

Skill adoption is complete for a workstation when:

- `Check` reports `IN_SYNC`;
- `/skills` shows one intended `engineering-handbook` user skill;
- explicit invocation works on a representative task;
- selected behavior demonstrates reference-level progressive disclosure rather than bulk loading;
- generated references have not become independently edited sources of truth.
