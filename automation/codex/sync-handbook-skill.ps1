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

$SkillsHome = [System.IO.Path]::TrimEndingDirectorySeparator([System.IO.Path]::GetFullPath($SkillsHome))
$targetDir = Join-Path $SkillsHome "engineering-handbook"
$installManifestName = "install-manifest.json"

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Read-UnambiguousManifestText {
    param([Parameter(Mandatory = $true)][string]$Path)

    $content = [string](Get-Content -LiteralPath $Path -Raw)
    $settings = [Newtonsoft.Json.Linq.JsonLoadSettings]::new()
    $settings.DuplicatePropertyNameHandling = [Newtonsoft.Json.Linq.DuplicatePropertyNameHandling]::Error
    $reader = [Newtonsoft.Json.JsonTextReader]::new([System.IO.StringReader]::new($content))
    # Match the existing ConvertFrom-Json default so valid optional metadata remains supported.
    $reader.MaxDepth = 1024
    try {
        [void][Newtonsoft.Json.Linq.JToken]::Load($reader, $settings)
    }
    catch {
        throw "Invalid or ambiguous JSON in $installManifestName."
    }
    finally {
        $reader.Close()
    }
    return $content
}

function Get-TargetStamp {
    param([string]$Path = $targetDir)
    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }
    $item = Get-Item -LiteralPath $Path -Force
    if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
        throw "Refusing a linked skill target: $Path"
    }
    $manifestPath = Join-Path $Path $installManifestName
    $manifestHash = ""
    if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
        $manifest = Read-UnambiguousManifestText -Path $manifestPath | ConvertFrom-Json
        if ($manifest.schema_version -eq 2) {
            throw "Enrolled Handbook target: use handbook_update.py doctor/preflight; reconcile enrollment before manual replacement."
        }
        $manifestHash = Get-Sha256 -Path $manifestPath
    }
    return "$($item.CreationTimeUtc.Ticks)|$($item.LastWriteTimeUtc.Ticks)|$($item.Attributes)|$manifestHash"
}

function Move-Installation {
    param([string]$From, [string]$To)
    if (Test-Path -LiteralPath $From -PathType Container) {
        [System.IO.Directory]::Move($From, $To)
    }
    else {
        [System.IO.File]::Move($From, $To)
    }
}

function Assert-LocalPaths {
    param([string[]]$Paths)
    foreach ($directory in $Paths) {
        $item = Get-Item -LiteralPath $directory -Force
        $resolved = (Resolve-Path -LiteralPath $directory).ProviderPath
        if ($resolved -ne $directory -or ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            throw "Refusing a skill operation through a linked directory: $directory"
        }
    }
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

function Assert-BundleFreshness {
    param([Parameter(Mandatory = $true)][string]$References)

    $compatibilityReceipt = "handbook-python-compatible"
    $versionCheck = @"
import sys
if sys.version_info < (3, 10):
    raise SystemExit(2)
print('$compatibilityReceipt')
"@
    $python = $null
    $candidates = Get-Command -Name python, python3 -CommandType Application -All -ErrorAction SilentlyContinue
    foreach ($candidate in $candidates) {
        try {
            $result = & $candidate.Source -I -B -c $versionCheck 2>&1
            if ($LASTEXITCODE -eq 0 -and ($result -join [Environment]::NewLine) -ceq $compatibilityReceipt) {
                $python = $candidate
                break
            }
        }
        catch {
            # This application could not serve as the compiler interpreter.
            continue
        }
    }
    if (-not $python) {
        throw "Python 3.10 or later is required to verify the Handbook corpus."
    }

    $verifier = Join-Path $PSScriptRoot "handbook_update.py"
    $result = & $python.Source -I -B -X utf8 $verifier verify-bundle --references $References 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Handbook corpus verification failed. Rebuild or use a verified checkout. $($result -join ' ')"
    }
    $receipt = ConvertFrom-Json -InputObject ($result -join [Environment]::NewLine) -AsHashtable -NoEnumerate
    if ($receipt -isnot [System.Collections.IDictionary] -or
        $receipt["status"] -isnot [string] -or $receipt["freshness_verification"] -isnot [string] -or
        $receipt["status"] -cne "VERIFIED" -or $receipt["freshness_verification"] -cne "local_recompile") {
        throw "The Handbook verifier did not return a successful freshness receipt."
    }
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
        $entryPath = [string]$entry
        if ($entryPath -eq '' -or $entryPath.Contains('\') -or
            ($entryPath -ne '.' -and $entryPath -match '(?:^|/)\.(?:/|$)|//|/$')) {
            throw "Noncanonical skill bundle include: $entryPath"
        }
        $candidate = Join-Path $repoRoot (Convert-ToNativePath -RelativePath $entryPath)

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

    # Running the router locally must not turn interpreter caches into canonical
    # sources or change the installed bundle according to workstation history.
    return @($paths | Where-Object { $_ -notmatch '(^|/)__pycache__(/|$)|\.py[co]$' } | Sort-Object -Unique)
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

    return $expected.ToArray()
}

function Add-ManifestValidationDetails {
    param(
        [Parameter(Mandatory = $true)][object[]]$ExpectedFiles,
        [Parameter(Mandatory = $true)][hashtable]$SourceHashes,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.Generic.List[string]]$Details
    )

    $manifestPath = Join-Path $targetDir $installManifestName
    if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
        $Details.Add("missing:$installManifestName")
        return
    }

    try {
        $manifest = Read-UnambiguousManifestText -Path $manifestPath | ConvertFrom-Json -AsHashtable -NoEnumerate
    }
    catch {
        $Details.Add("invalid:$installManifestName")
        return
    }
    if ($manifest -isnot [System.Collections.IDictionary]) {
        $Details.Add("invalid:$installManifestName")
        return
    }

    $version = $manifest['schema_version']
    $canonicalRepositories = @(
        "Kappa-Bot/engineering-handbook",
        "https://github.com/Kappa-Bot/engineering-handbook.git"
    )
    if (($version -isnot [int] -and $version -isnot [long]) -or $version -ne 1 -or
        $manifest['skill_name'] -isnot [string] -or $manifest['skill_name'] -cne "engineering-handbook" -or
        $manifest['source_repository'] -isnot [string] -or
        $canonicalRepositories -cnotcontains $manifest['source_repository']) {
        $Details.Add("mismatch:$installManifestName")
        return
    }

    $rows = $manifest['files']
    if ($rows -isnot [array]) {
        $Details.Add("invalid-manifest-files")
        return
    }

    $manifestEntries = @{}
    foreach ($entry in $rows) {
        if ($entry -isnot [System.Collections.IDictionary] -or
            $entry['install_path'] -isnot [string] -or [string]::IsNullOrWhiteSpace($entry['install_path']) -or
            $entry['source_path'] -isnot [string] -or $entry['sha256'] -isnot [string]) {
            $Details.Add("invalid-manifest-entry")
            continue
        }
        $key = $entry['install_path']
        if ($manifestEntries.ContainsKey($key)) {
            $Details.Add("duplicate-manifest-entry:$key")
            continue
        }
        $manifestEntries[$key] = $entry
    }

    foreach ($item in $ExpectedFiles) {
        if (-not $manifestEntries.ContainsKey($item.InstallPath)) {
            $Details.Add("manifest-missing:$($item.InstallPath)")
            continue
        }

        $entry = $manifestEntries[$item.InstallPath]
        $expectedHash = $SourceHashes[$item.InstallPath]
        if ($entry['install_path'] -cne $item.InstallPath -or
            $entry['source_path'] -cne $item.SourceRelativePath -or
            ($entry['sha256']).ToLowerInvariant() -ne $expectedHash) {
            $Details.Add("manifest-mismatch:$($item.InstallPath)")
        }
    }

    foreach ($key in $manifestEntries.Keys) {
        if (-not ($ExpectedFiles.InstallPath -contains $key)) {
            $Details.Add("manifest-unexpected:$key")
        }
    }
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
    $allowed = @{}
    $sourceHashes = @{}

    foreach ($item in $ExpectedFiles) {
        $allowed[$item.InstallPath] = $true
        $sourceHashes[$item.InstallPath] = Get-Sha256 -Path $item.SourcePath
        $installedPath = Join-Path $targetDir (Convert-ToNativePath -RelativePath $item.InstallPath)

        if (-not (Test-Path -LiteralPath $installedPath -PathType Leaf)) {
            $details.Add("missing:$($item.InstallPath)")
            continue
        }

        if ((Get-Sha256 -Path $installedPath) -ne $sourceHashes[$item.InstallPath]) {
            $details.Add("changed:$($item.InstallPath)")
        }
    }

    $allowed[$installManifestName] = $true

    foreach ($file in Get-ChildItem -LiteralPath $targetDir -File -Recurse -Force) {
        $relative = Get-RelativePathFromRoot -Root $targetDir -Path $file.FullName
        # The installed Python router generates the same disposable caches as
        # the canonical runtime. They are not installed-source drift either.
        if ($relative -match '(^|/)__pycache__(/|$)|\.py[co]$') { continue }
        if (-not $allowed.ContainsKey($relative)) {
            $details.Add("unexpected:$relative")
        }
    }

    Add-ManifestValidationDetails -ExpectedFiles $ExpectedFiles -SourceHashes $sourceHashes -Details $details

    if ($details.Count -eq 0) {
        return [pscustomobject]@{ State = "IN_SYNC"; Details = @(); SourceHashes = $sourceHashes }
    }

    return [pscustomobject]@{ State = "OUT_OF_SYNC"; Details = @($details) }
}

function Assert-VerifiedInstalledTarget {
    param([hashtable]$SourceHashes, [string]$OriginalTargetStamp)

    Assert-LocalPaths -Paths @($targetDir)
    $remaining = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($path in $SourceHashes.Keys) {
        [void]$remaining.Add($path)
    }
    [void]$remaining.Add($installManifestName)

    foreach ($file in Get-ChildItem -LiteralPath $targetDir -File -Recurse -Force) {
        $relative = Get-RelativePathFromRoot -Root $targetDir -Path $file.FullName
        if ($relative -match '(^|/)__pycache__(/|$)|\.py[co]$') { continue }
        if (-not $remaining.Remove($relative)) {
            throw "Unexpected installed skill file during verification: $relative"
        }
        if ($file.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            throw "Refusing to certify a linked installed skill file: $relative"
        }
        if ($relative -cne $installManifestName -and (Get-Sha256 -Path $file.FullName) -ne $SourceHashes[$relative]) {
            throw "The installed skill file $relative changed during verification."
        }
    }
    if ($remaining.Count -gt 0) {
        throw "Installed skill files are missing after verification: $(($remaining | Sort-Object) -join ',')"
    }
    if ((Get-TargetStamp) -cne $OriginalTargetStamp) {
        throw "The skill target or its manifest changed during verification."
    }
}

$originalTarget = Get-TargetStamp
$expectedFiles = Get-ExpectedFiles
$state = Get-InstallState -ExpectedFiles $expectedFiles

if ($Mode -eq "Check") {
    if ($state.State -eq "IN_SYNC") {
        try {
            Assert-BundleFreshness -References (Join-Path $targetDir "references")
            Assert-VerifiedInstalledTarget -SourceHashes $state.SourceHashes -OriginalTargetStamp $originalTarget
        }
        catch {
            Write-Output "OUT_OF_SYNC target=$targetDir details=$($_.Exception.Message)"
            exit 2
        }
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
    Assert-BundleFreshness -References (Join-Path $targetDir "references")
    Assert-VerifiedInstalledTarget -SourceHashes $state.SourceHashes -OriginalTargetStamp $originalTarget
    Write-Output "ALREADY_IN_SYNC target=$targetDir references=$($expectedFiles.Count - 1)"
    exit 0
}

if ($originalTarget -and -not $BackupExisting) {
    throw "Refusing to replace existing skill directory: $targetDir. Re-run with -BackupExisting after reviewing it."
}

if (-not $PSCmdlet.ShouldProcess($targetDir, "Install Engineering Handbook user skill")) {
    Write-Output "PREVIEW target=$targetDir references=$($expectedFiles.Count - 1)"
    exit 0
}

New-Item -ItemType Directory -Path $SkillsHome -Force | Out-Null
Assert-LocalPaths -Paths @($SkillsHome)
$stagingDir = Join-Path $SkillsHome (".engineering-handbook.staging-" + [guid]::NewGuid().ToString("N"))
$backupPath = $null
$installedTarget = $null

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

    Assert-BundleFreshness -References (Join-Path $stagingDir "references")

    if ((Get-TargetStamp) -cne $originalTarget) {
        throw "The skill target changed during verification. Review the current installation before retrying."
    }
    if ($originalTarget) {
        $backupRoot = Join-Path (Split-Path -Parent $SkillsHome) "skill-backups"
        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
        Assert-LocalPaths -Paths @($SkillsHome, $targetDir, $backupRoot)
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmssfff"
        $candidateBackup = Join-Path $backupRoot "engineering-handbook.backup-$timestamp"
        if (Test-Path -LiteralPath $candidateBackup) {
            throw "Skill backup already exists: $candidateBackup"
        }
        Move-Installation -From $targetDir -To $candidateBackup
        $backupPath = $candidateBackup
        if ((Get-TargetStamp -Path $backupPath) -cne $originalTarget) {
            throw "The skill target changed while its backup was being moved."
        }
        Write-Output "BACKUP path=$backupPath"
    }

    Move-Installation -From $stagingDir -To $targetDir
    $installedTarget = Get-TargetStamp

    $installedState = Get-InstallState -ExpectedFiles $expectedFiles
    if ($installedState.State -ne "IN_SYNC") {
        throw "Post-install verification failed: $($installedState.Details -join ',')"
    }

    Write-Output "INSTALLED target=$targetDir references=$($expectedFiles.Count - 1)"
}
catch {
    if ($installedTarget -and (Test-Path -LiteralPath $targetDir)) {
        try {
            if ((Get-TargetStamp) -ceq $installedTarget) {
                $backupRoot = Join-Path (Split-Path -Parent $SkillsHome) "skill-backups"
                New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
                Assert-LocalPaths -Paths @($SkillsHome, $targetDir, $backupRoot)
                $recovery = Join-Path $backupRoot ("engineering-handbook.recovery-" + [guid]::NewGuid().ToString("N"))
                Move-Installation -From $targetDir -To $recovery
                Write-Warning "The unsuccessful activation was preserved at $recovery."
            }
        }
        catch {
            Write-Warning "The current skill target was preserved during recovery."
        }
    }
    if ($backupPath -and (Test-Path -LiteralPath $backupPath) -and -not (Test-Path -LiteralPath $targetDir)) {
        Assert-LocalPaths -Paths @($SkillsHome, $backupRoot, $backupPath)
        Move-Installation -From $backupPath -To $targetDir
    }
    throw
}
finally {
    if (Test-Path -LiteralPath $stagingDir) {
        $stage = Get-Item -LiteralPath $stagingDir -Force
        $resolved = (Resolve-Path -LiteralPath $stagingDir).ProviderPath
        if ($resolved -eq $stagingDir -and $stage.PSIsContainer -and
            -not ($stage.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            Remove-Item -LiteralPath $stagingDir -Recurse -Force
        }
    }
}
