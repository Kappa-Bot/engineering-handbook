---
id: pb-codex-global-adoption
kind: playbook
status: active
owner: engineering
version: "0.1"
applies_to:
  - codex
  - developer-workstations
sources:
  - src-openai-codex-agents
last_verified: 2026-08-15
review_due: 2026-11-15
---

# Codex Global Instructions Adoption

## Purpose

Install and verify the handbook's small global Codex instruction artifact without creating a second source of truth or silently overwriting workstation-specific content.

The canonical source is:

`agent-config/codex/AGENTS.global.md`

The installed runtime artifact is:

`$CODEX_HOME/AGENTS.md`, or `~/.codex/AGENTS.md` when `CODEX_HOME` is unset.

The installed file is a copy. It MUST NOT be edited as the authoritative version. General changes belong in the handbook source and are then re-synchronized.

## Why explicit synchronization

Foundation intentionally avoids symlinks, background updaters, package installers, and managed-device infrastructure. An explicit sync step is portable, observable, reversible, and easy to replace later if scale justifies stronger distribution.

## Preconditions

- Run from a local checkout of `Kappa-Bot/engineering-handbook`.
- Use PowerShell (`pwsh` recommended; Windows PowerShell is acceptable if the script runs correctly in the local environment).
- Update the checkout to the handbook revision you intend to adopt before synchronizing.

## 1. Check current state

From the repository root:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check
```

Expected states:

- `IN_SYNC`: installed file exists and its SHA-256 equals the canonical source.
- `MISSING`: no global `AGENTS.md` exists at the resolved Codex home.
- `OUT_OF_SYNC`: a global file exists but differs from the handbook source.

`MISSING` and `OUT_OF_SYNC` return a non-zero exit code so the check can later be reused by automation without changing its semantics.

## 2. Preview installation

If the target is missing:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install -WhatIf
```

If the target exists and differs, explicitly allow a backup:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install -BackupExisting -WhatIf
```

The script refuses to overwrite a differing existing file unless `-BackupExisting` is supplied.

## 3. Install

For a missing target:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install
```

For a differing target:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install -BackupExisting
```

Backups are created beside the target using the form:

`AGENTS.md.backup-YYYYMMDD-HHmmss`

## 4. Verify file synchronization

Run the check again:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check
```

Do not claim adoption is complete unless this check reports `IN_SYNC`.

## 5. Verify Codex runtime discovery

Codex builds its instruction chain when a run/session starts, so start a new Codex session after installation.

A simple runtime probe is:

```powershell
codex --ask-for-approval never "Summarize the current instructions."
```

Confirm that the response reflects the global working agreements and, inside a consumer repository, the repo-local `AGENTS.md` additions/overrides as applicable.

Runtime behavior is governed by Codex's own instruction-discovery semantics. The handbook does not redefine that precedence.

## Rollback

If a backup was created:

1. close/restart Codex sessions that may have loaded the current file;
2. move the current `AGENTS.md` aside or remove it if it is known to be the handbook-installed copy;
3. restore the desired `AGENTS.md.backup-*` file to `AGENTS.md`;
4. start a new Codex session and verify the resulting instruction chain.

Do not delete backups until the workstation behavior has been validated.

## Testing without touching the real Codex home

The script accepts `-CodexHome` for isolated testing:

```powershell
$tempCodexHome = Join-Path $env:TEMP "engineering-handbook-codex-test"
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install -CodexHome $tempCodexHome
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check -CodexHome $tempCodexHome
Remove-Item -Recurse -Force $tempCodexHome
```

This override is for verification or unusual setups. Normal usage should allow the script to resolve `CODEX_HOME` or the default `~/.codex` location.

## Definition of done for adoption

Adoption is complete for a workstation only when:

- the installed target is `IN_SYNC` with the handbook source;
- any pre-existing differing target was preserved before replacement;
- a new Codex session has been started;
- runtime discovery has been observed rather than assumed.
