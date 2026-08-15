[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet("Check", "Install")]
    [string]$Mode = "Check",

    [switch]$BackupExisting,

    [string]$SkillsHome
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$sourceSkillDir = Join-Path $repoRoot "agent-config\codex\skills\engineering-handbook"
$sourceSkillPath = Join-Path $sourceSkillDir "SKILL.md"
$bundlePath = Join-Path $sourceSkillDir "bundle.json"

if (-not $SkillsHome) {
    $SkillsHome = Join-Path $HOME ".agents\skills"
}

$targetDir = Join-Path $SkillsHome "engineering-handbook"
$installManifestName = "install-manifest.json"

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-RelativePathFromRoot {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    $pathFull = [System.IO.Path]::GetFullPath($Path)
    $prefix = $rootFull + [System.IO.Path]::DirectorySeparatorChar

    if (-not $pathFull.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Path is outside expected root: $pathFull"
    }

    return $pathFull.Substring($prefix.Length).Replace('\', '/')
}

function Convert-ToNativePath {
    param([Parameter(Mandatory = $true)][string]$RelativePath)
    return $RelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

function Get-BundledSourceFiles {
    if (-not (Test-Path -LiteralPath $sourceSkillPath -PathType Leaf)) {
        throw "Canonical skill source not found: $sourceSkillPath"
    }
    if (-not (Test-Path -LiteralPath $bundlePath -PathType Leaf)) {
        throw "Skill bundle manifest not found: $bundlePath"
    }

    $bundle = Get-Content -LiteralPath $bundlePath -Raw | ConvertFrom-Json
    if ($bundle.schema_version -ne 1 -or $bundle.skill_name -ne "engineering-handbook") {
        throw "Unsupported or mismatched skill bundle manifest: $bundlePath"
    }

    $paths = New-Object System.Collections.Generic.List[string]

    foreach ($entry in $bundle.include) {
        $candidate = Join-Path $repoRoot (Convert-ToNativePath -RelativePath ([string]$entry))

        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $paths.Add((Get-RelativePathFromRoot -Root $repoRoot -Path $candidate))
            continue
        }

        if (Test-Path -LiteralPath $candidate -PathType Container) {
            foreach ($file in Get-ChildItem -LiteralPath $candidate -File -Recurse) {
                $paths.Add((Get-RelativePathFromRoot -Root $repoRoot -Path $file.FullName))
            }
            continue
        }

        throw "Bundle include path does not exist: $entry"
    }

    return @($paths | Sort-Object -Unique)
}

function Get-ExpectedFiles {
    $expected = New-Object System.Collections.Generic.List[object]
    $expected.Add([pscustomobject]@{
        InstallPath = "SKILL.md"
        SourcePath = $sourceSkillPath
        SourceRelativePath = "agent-config/codex/skills/engineering-handbook/SKILL.md"
    })

    foreach ($relativePath in Get-BundledSourceFiles) {
        $sourcePath = Join-Path $repoRoot (Convert-ToNativePath -RelativePath $relativePath)
        $expected.Add([pscustomobject]@{
            InstallPath = "references/$relativePath"
            SourcePath = $sourcePath
            SourceRelativePath = $relativePath
        })
    }

    return @($expected)
}

function Get-InstallState {
    param([Parameter(Mandatory = $true)][object[]]$ExpectedFiles)

    if (-not (Test-Path -LiteralPath $targetDir)) {
        return [pscustomobject]@{ State = "MISSING"; Details = @("target missing") }
    }
    if (-not (Test-Path -LiteralPath $targetDir -PathType Container)) {
        return [pscustomobject]@{ State = "OUT_OF_SYNC"; Details = @("target exists but is not a directory") }
    }

    $details = New-Object System.Collections.Generic.List[string]
    $allowed = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)

    foreach ($item in $ExpectedFiles) {
        [void]$allowed.Add($item.InstallPath)
        $installedPath = Join-Path $targetDir (Convert-ToNativePath -RelativePath $item.InstallPath)

        if (-not (Test-Path -LiteralPath $installedPath -PathType Leaf)) {
            $details.Add("missing:$($item.InstallPath)")
            continue
        }

        if ((Get-Sha256 -Path $installedPath) -ne (Get-Sha256 -Path $item.SourcePath)) {
            $details.Add("changed:$($item.InstallPath)")
        }
    }

    [void]$allowed.Add($installManifestName)

    foreach ($file in Get-ChildItem -LiteralPath $targetDir -File -Recurse) {
        $relative = Get-RelativePathFromRoot -Root $targetDir -Path $file.FullName
        if (-not $allowed.Contains($relative)) {
            $details.Add("unexpected:$relative")
        }
    }

    if ($details.Count -eq 0) {
        return [pscustomobject]@{ State = "IN_SYNC"; Details = @() }
    }

    return [pscustomobject]@{ State = "OUT_OF_SYNC"; Details = @($details) }
}

$expectedFiles = Get-ExpectedFiles
$state = Get-InstallState -ExpectedFiles $expectedFiles

if ($Mode -eq "Check") {
    if ($state.State -eq "IN_SYNC") {
        Write-Output "IN_SYNC target=$targetDir references=$($expectedFiles.Count - 1)"
        exit 0
    }

    if ($state.State -eq "MISSING") {
        Write-Output "MISSING target=$targetDir"
        exit 1
    }

    Write-Output "OUT_OF_SYNC target=$targetDir details=$($state.Details -join ',')"
    exit 2
}

if ($state.State -eq "IN_SYNC") {
    Write-Output "ALREADY_IN_SYNC target=$targetDir references=$($expectedFiles.Count - 1)"
    exit 0
}

if ((Test-Path -LiteralPath $targetDir) -and -not $BackupExisting) {
    throw "Refusing to replace existing skill directory: $targetDir. Re-run with -BackupExisting after reviewing it."
}

if (-not $PSCmdlet.ShouldProcess($targetDir, "Install Engineering Handbook user skill")) {
    Write-Output "PREVIEW target=$targetDir references=$($expectedFiles.Count - 1)"
    exit 0
}

New-Item -ItemType Directory -Path $SkillsHome -Force | Out-Null
$stagingDir = Join-Path $SkillsHome (".engineering-handbook.staging-" + [guid]::NewGuid().ToString("N"))
$backupPath = $null

try {
    New-Item -ItemType Directory -Path $stagingDir -Force | Out-Null

    foreach ($item in $expectedFiles) {
        $destination = Join-Path $stagingDir (Convert-ToNativePath -RelativePath $item.InstallPath)
        $destinationDir = Split-Path -Parent $destination
        New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
        Copy-Item -LiteralPath $item.SourcePath -Destination $destination -Force
    }

    $manifestEntries = foreach ($item in $expectedFiles) {
        [ordered]@{
            install_path = $item.InstallPath
            source_path = $item.SourceRelativePath
            sha256 = Get-Sha256 -Path $item.SourcePath
        }
    }

    $manifest = [ordered]@{
        schema_version = 1
        skill_name = "engineering-handbook"
        source_repository = "Kappa-Bot/engineering-handbook"
        generated_at = (Get-Date).ToUniversalTime().ToString("o")
        files = @($manifestEntries)
    }

    $manifestPath = Join-Path $stagingDir $installManifestName
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

    foreach ($item in $expectedFiles) {
        $stagedPath = Join-Path $stagingDir (Convert-ToNativePath -RelativePath $item.InstallPath)
        if ((Get-Sha256 -Path $stagedPath) -ne (Get-Sha256 -Path $item.SourcePath)) {
            throw "Staging verification failed: $($item.InstallPath)"
        }
    }

    if (Test-Path -LiteralPath $targetDir) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmssfff"
        $backupPath = "$targetDir.backup-$timestamp"
        Move-Item -LiteralPath $targetDir -Destination $backupPath
        Write-Output "BACKUP path=$backupPath"
    }

    Move-Item -LiteralPath $stagingDir -Destination $targetDir

    $installedState = Get-InstallState -ExpectedFiles $expectedFiles
    if ($installedState.State -ne "IN_SYNC") {
        throw "Post-install verification failed: $($installedState.Details -join ',')"
    }

    Write-Output "INSTALLED target=$targetDir references=$($expectedFiles.Count - 1)"
}
catch {
    if ($backupPath -and (Test-Path -LiteralPath $backupPath)) {
        if (Test-Path -LiteralPath $targetDir) {
            Remove-Item -LiteralPath $targetDir -Recurse -Force
        }
        Move-Item -LiteralPath $backupPath -Destination $targetDir
    }
    throw
}
finally {
    if (Test-Path -LiteralPath $stagingDir) {
        Remove-Item -LiteralPath $stagingDir -Recurse -Force
    }
}
