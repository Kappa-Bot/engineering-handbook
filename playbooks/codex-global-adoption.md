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

Codex checks `AGENTS.override.md` before `AGENTS.md` at global scope and uses the first non-empty file. Therefore a non-empty override can make an installed `AGENTS.md` inactive even when its content is byte-for-byte correct. The adoption check treats this explicitly as `SHADOWED`; an empty override is ignored for this purpose.

## Why explicit synchronization

Foundation intentionally avoids symlinks, background updaters, package installers, and managed-device infrastructure. An explicit sync step is portable, observable, reversible, and easy to replace later if scale justifies stronger distribution.

## Preconditions

- Run from a local checkout of `Kappa-Bot/engineering-handbook`.
- Use PowerShell (`pwsh` recommended; Windows PowerShell is acceptable if the script runs correctly in the local environment).
- Update the checkout to the handbook revision you intend to adopt before synchronizing.
- If a non-empty global `AGENTS.override.md` exists, understand why before changing or removing it. This workflow never edits that file.

## 1. Check current state

From the repository root:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check
```

Expected states:

- `IN_SYNC`: installed `AGENTS.md` exists, matches the canonical source, and no non-empty global override shadows it.
- `MISSING`: no global `AGENTS.md` exists at the resolved Codex home.
- `OUT_OF_SYNC`: a global `AGENTS.md` exists but differs from the handbook source.
- `SHADOWED`: a non-empty `AGENTS.override.md` exists, so Codex will prefer it over `AGENTS.md`; the output also reports the underlying target state.

Exit codes:

- `0`: `IN_SYNC`;
- `1`: `MISSING`;
- `2`: `OUT_OF_SYNC`;
- `3`: `SHADOWED`.

These non-zero states make the check reusable by future automation without changing its semantics.

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

A non-empty existing `AGENTS.override.md` is never modified. Installation may succeed while still warning that the new `AGENTS.md` is shadowed.

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

`AGENTS.md.backup-YYYYMMDD-HHmmssfff`

## 4. Verify file synchronization and activation

Run the check again:

```powershell
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check
```

Do not claim workstation adoption is complete unless this check reports `IN_SYNC`. `SHADOWED` means the installed file may be correct but is not the active global instruction source.

## 5. Verify Codex runtime discovery

Codex builds its instruction chain when a run/session starts, so start a new Codex session after installation or any override change.

A simple runtime probe documented by Codex is:

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
4. leave any pre-existing `AGENTS.override.md` untouched unless its owner deliberately decides otherwise;
5. start a new Codex session and verify the resulting instruction chain.

Do not delete backups until the workstation behavior has been validated.

## Testing without touching the real Codex home

The script accepts `-CodexHome` for isolated testing:

```powershell
$tempCodexHome = Join-Path $env:TEMP "engineering-handbook-codex-test"
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Install -CodexHome $tempCodexHome
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check -CodexHome $tempCodexHome
Remove-Item -Recurse -Force $tempCodexHome
```

To test override detection:

```powershell
$tempCodexHome = Join-Path $env:TEMP "engineering-handbook-codex-test"
New-Item -ItemType Directory -Force $tempCodexHome | Out-Null
Set-Content -Path (Join-Path $tempCodexHome "AGENTS.override.md") -Value "temporary override"
pwsh -File .\automation\codex\sync-global-agents.ps1 -Mode Check -CodexHome $tempCodexHome
```

The expected state is `SHADOWED` with exit code `3`. A zero-byte override should not shadow the global `AGENTS.md`.

## Definition of done for adoption

Adoption is complete for a workstation only when:

- the installed target is `IN_SYNC` with the handbook source;
- no non-empty global `AGENTS.override.md` shadows the installed source unless that shadowing is intentionally the desired runtime behavior;
- any pre-existing differing target was preserved before replacement;
- a new Codex session has been started;
- runtime discovery has been observed rather than assumed.
