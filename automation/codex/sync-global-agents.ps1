[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet("Check", "Install")]
    [string]$Mode = "Check",

    [switch]$BackupExisting,

    [string]$CodexHome
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$sourcePath = Join-Path $repoRoot "agent-config\codex\AGENTS.global.md"

if (-not $CodexHome) {
    if ($env:CODEX_HOME) {
        $CodexHome = $env:CODEX_HOME
    }
    else {
        $CodexHome = Join-Path $HOME ".codex"
    }
}

$targetPath = Join-Path $CodexHome "AGENTS.md"
$overridePath = Join-Path $CodexHome "AGENTS.override.md"

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
    throw "Canonical source not found: $sourcePath"
}

$sourceHash = Get-Sha256 -Path $sourcePath
$targetExists = Test-Path -LiteralPath $targetPath -PathType Leaf
$overrideExists = Test-Path -LiteralPath $overridePath -PathType Leaf
$targetHash = if ($targetExists) { Get-Sha256 -Path $targetPath } else { $null }

if ($Mode -eq "Check") {
    $targetState = if (-not $targetExists) {
        "MISSING"
    }
    elseif ($targetHash -eq $sourceHash) {
        "IN_SYNC"
    }
    else {
        "OUT_OF_SYNC"
    }

    if ($overrideExists) {
        Write-Output "SHADOWED override=$overridePath target_state=$targetState target=$targetPath source_sha256=$sourceHash"
        exit 3
    }

    if ($targetState -eq "MISSING") {
        Write-Output "MISSING target=$targetPath source_sha256=$sourceHash"
        exit 1
    }

    if ($targetState -eq "IN_SYNC") {
        Write-Output "IN_SYNC target=$targetPath sha256=$sourceHash"
        exit 0
    }

    Write-Output "OUT_OF_SYNC target=$targetPath target_sha256=$targetHash source_sha256=$sourceHash"
    exit 2
}

if ($targetExists -and $targetHash -eq $sourceHash) {
    if ($overrideExists) {
        Write-Warning "AGENTS.override.md exists and takes precedence over AGENTS.md: $overridePath"
    }
    Write-Output "ALREADY_IN_SYNC target=$targetPath sha256=$sourceHash"
    exit 0
}

if ($targetExists -and -not $BackupExisting) {
    throw "Refusing to overwrite differing existing file: $targetPath. Re-run with -BackupExisting after reviewing the file."
}

if ($PSCmdlet.ShouldProcess($targetPath, "Install handbook global Codex instructions")) {
    New-Item -ItemType Directory -Path $CodexHome -Force | Out-Null

    if ($targetExists) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backupPath = "$targetPath.backup-$timestamp"
        Copy-Item -LiteralPath $targetPath -Destination $backupPath
        Write-Output "BACKUP path=$backupPath"
    }

    Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Force

    $installedHash = Get-Sha256 -Path $targetPath
    if ($installedHash -ne $sourceHash) {
        throw "Post-install verification failed for $targetPath"
    }

    if ($overrideExists) {
        Write-Warning "Installed AGENTS.md is currently shadowed by AGENTS.override.md: $overridePath"
    }

    Write-Output "INSTALLED target=$targetPath sha256=$installedHash"
}
