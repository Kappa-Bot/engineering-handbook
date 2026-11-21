[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$catalogPath = Join-Path $repoRoot "machine-readable\catalog.yaml"
$sourcesPath = Join-Path $repoRoot "machine-readable\sources.yaml"
$skillBundlePath = Join-Path $repoRoot "agent-config\codex\skills\engineering-handbook\bundle.json"
$errors = New-Object System.Collections.Generic.List[string]
$requiredSourceFields = @(
    'id', 'title', 'tier', 'kind', 'url', 'canonical_language', 'applies_to',
    'status', 'last_verified', 'review_due', 'volatility', 'reuse'
)
$knownSourceFields = $requiredSourceFields + @('license', 'revision', 'version')

function Add-IntegrityError {
    param([Parameter(Mandatory = $true)][string]$Message)
    $errors.Add($Message)
}

function Normalize-Scalar {
    param([AllowNull()][string]$Value)
    if ($null -eq $Value) { return $null }
    $normalized = $Value.Trim()
    if (($normalized.StartsWith('"') -and $normalized.EndsWith('"')) -or
        ($normalized.StartsWith("'") -and $normalized.EndsWith("'"))) {
        if ($normalized.Length -ge 2) {
            return $normalized.Substring(1, $normalized.Length - 2)
        }
    }
    return $normalized
}

function Read-SimpleRegistryItems {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$RootKey
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Registry not found: $Path"
    }

    $lines = Get-Content -LiteralPath $Path
    if (-not ($lines -match ('^' + [regex]::Escape($RootKey) + ':\s*$'))) {
        throw "Registry root '$RootKey' not found: $Path"
    }

    $items = @()
    $current = $null
    $duplicateSourceFields = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)

    foreach ($line in $lines) {
        if ($line -match '^\s{2}- id:\s*(.+?)\s*$') {
            if ($null -ne $current) {
                $items += $current
            }
            $current = @{}
            $current['id'] = Normalize-Scalar $Matches[1]
            $duplicateSourceFields.Clear()
            continue
        }

        if ($null -ne $current -and $line -match '^\s{4}([A-Za-z0-9_-]+):\s*(.*?)\s*$') {
            $key = $Matches[1]
            if ($RootKey -ceq 'sources') {
                $knownKey = $key.ToLowerInvariant()
                if ($knownSourceFields -ccontains $knownKey -and $current.ContainsKey($key)) {
                    if ($duplicateSourceFields.Add($knownKey)) {
                        Add-IntegrityError ("duplicate-source-field:{0}:{1}" -f $current['id'], $knownKey)
                    }
                    # The sequence entry owns the ID for subsequent reference diagnostics.
                    if ($knownKey -ceq 'id') { continue }
                }
            }
            $current[$key] = Normalize-Scalar $Matches[2]
        }
    }

    if ($null -ne $current) {
        $items += $current
    }

    return @($items)
}

function Get-FrontMatter {
    param([Parameter(Mandatory = $true)][string]$Path)

    $lines = @(Get-Content -LiteralPath $Path)
    if ($lines.Count -lt 3 -or $lines[0].Trim() -ne '---') {
        return $null
    }

    $values = @{}
    $keys = @{}
    $seenIdentity = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    $duplicateIdentity = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    $closed = $false

    for ($i = 1; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line.Trim() -eq '---') {
            $closed = $true
            break
        }

        if ($line -match '^([A-Za-z0-9_-]+):\s*(.*?)\s*$') {
            $key = $Matches[1]
            if (@('id', 'kind', 'status') -ccontains $key -and -not $seenIdentity.Add($key)) {
                [void]$duplicateIdentity.Add($key)
            }
            $keys[$key] = $true
            $values[$key] = Normalize-Scalar $Matches[2]
        }
    }

    if (-not $closed) {
        Add-IntegrityError ("unterminated-frontmatter:{0}" -f $Path)
        return $null
    }

    return [pscustomobject]@{
        Keys = $keys
        Values = $values
        DuplicateIdentity = $duplicateIdentity
    }
}

function Get-DeclaredSourceReferences {
    param([string]$Content)

    $front = [regex]::Match($Content, '\A---[^\S\r\n]*\r?\n(?<body>.*?)\r?\n---(?:[^\S\r\n]*(?:\r?\n|\z))', 'Singleline')
    $declarations = [regex]::Matches($front.Groups['body'].Value,
        '^sources:[ \t]*(?<value>[^\r\n]*)(?<items>(?:\r?\n[ \t]*-[ \t]+[^\r\n]+)*)', 'Multiline')
    if ($declarations.Count -ne 1) {
        return @{ Valid = ($declarations.Count -eq 0); Ids = @() }
    }
    $value = $declarations[0].Groups['value'].Value.Trim()
    $items = $declarations[0].Groups['items'].Value
    if ($items) {
        if ($value) { return @{ Valid = $false; Ids = @() } }
        $members = [regex]::Matches($items, '^[ \t]*-[ \t]+([^\r\n]+)', 'Multiline') |
            ForEach-Object { $_.Groups[1].Value }
    }
    elseif ($value.StartsWith('[') -and $value.EndsWith(']')) {
        $inner = $value.Substring(1, $value.Length - 2).Trim()
        $members = @()
        if ($inner) {
            if ($inner.EndsWith(',')) { $inner = $inner.Substring(0, $inner.Length - 1) }
            $members = $inner.Split(',')
        }
    }
    elseif ($value) {
        $members = @($value)
    }
    else {
        return @{ Valid = $false; Ids = @() }
    }

    $ids = @()
    foreach ($member in $members) {
        $reference = Normalize-Scalar $member
        if ($reference -notmatch '^[^\s\x22\x27\[\]{},:]+$') {
            return @{ Valid = $false; Ids = @() }
        }
        $ids += $reference
    }
    return @{ Valid = $true; Ids = $ids }
}

function Test-RequiredFields {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Item,
        [Parameter(Mandatory = $true)][string[]]$Fields,
        [Parameter(Mandatory = $true)][string]$Label
    )

    foreach ($field in $Fields) {
        if (-not $Item.ContainsKey($field) -or [string]::IsNullOrWhiteSpace([string]$Item[$field])) {
            Add-IntegrityError ("missing-field:{0}:{1}" -f $Label, $field)
        }
    }
}

function Test-ReviewDates {
    param(
        [hashtable]$Fields,
        [string]$Subject,
        [string]$Id,
        [switch]$SkipBlank
    )

    $reviewDates = @{}
    foreach ($field in @('last_verified', 'review_due')) {
        if (-not $Fields.ContainsKey($field)) { continue }
        $value = [string]$Fields[$field]
        if ($SkipBlank -and [string]::IsNullOrWhiteSpace($value)) { continue }
        $parsed = [datetime]::MinValue
        if ([datetime]::TryParseExact($value, 'yyyy-MM-dd', [cultureinfo]::InvariantCulture,
                [System.Globalization.DateTimeStyles]::None, [ref]$parsed)) {
            $reviewDates[$field] = $parsed
        }
        else {
            Add-IntegrityError ("invalid-{0}-date:{1}:{2}" -f $Subject, $Id, $field)
        }
    }
    if ($reviewDates.ContainsKey('last_verified') -and $reviewDates.ContainsKey('review_due') -and
        $reviewDates['review_due'] -lt $reviewDates['last_verified']) {
        Add-IntegrityError ("{0}-review-precedes-verification:{1}" -f $Subject, $Id)
    }
}

try {
    $catalogItems = @(Read-SimpleRegistryItems -Path $catalogPath -RootKey 'documents')
    $sourceItems = @(Read-SimpleRegistryItems -Path $sourcesPath -RootKey 'sources')
}
catch {
    Write-Error $_
    exit 1
}

$catalogIds = @{}
$catalogPaths = @{}
$sourceIds = @{}

foreach ($item in $catalogItems) {
    Test-RequiredFields -Item $item -Fields @('id', 'kind', 'path', 'status', 'applies_to') -Label 'catalog'

    $id = [string]$item['id']
    $path = [string]$item['path']

    if ($catalogIds.ContainsKey($id)) {
        Add-IntegrityError ("duplicate-catalog-id:{0}" -f $id)
    }
    else {
        $catalogIds[$id] = $true
    }

    if ($catalogPaths.ContainsKey($path)) {
        Add-IntegrityError ("duplicate-catalog-path:{0}" -f $path)
    }
    else {
        $catalogPaths[$path] = $true
    }

    $fullPath = Join-Path $repoRoot ($path.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        Add-IntegrityError ("missing-catalog-path:{0}:{1}" -f $id, $path)
        continue
    }

    if ([System.IO.Path]::GetExtension($fullPath) -ieq '.md') {
        $frontMatter = Get-FrontMatter -Path $fullPath
        $kind = [string]$item['kind']
        $requiresNormativeMetadata = @('governance', 'policy', 'standard', 'pattern', 'playbook', 'reference') -contains $kind
        $isDecision = $kind -eq 'decision' -or $path.StartsWith('decisions/', [StringComparison]::Ordinal)

        if ($isDecision -and $kind -cne 'decision') {
            Add-IntegrityError ("catalog-kind-mismatch:{0}:{1}:decision" -f $id, $kind)
        }
        if ($requiresNormativeMetadata -or $isDecision) {
            if ($null -eq $frontMatter) {
                Add-IntegrityError ("missing-frontmatter:{0}:{1}" -f $id, $path)
            }
            else {
                $requiredKeys = @('status')
                if ($requiresNormativeMetadata) {
                    $requiredKeys = @('id', 'kind', 'status', 'owner', 'version', 'applies_to', 'sources', 'last_verified', 'review_due')
                }
                foreach ($requiredKey in $requiredKeys) {
                    if (-not $frontMatter.Keys.ContainsKey($requiredKey)) {
                        Add-IntegrityError ("missing-frontmatter-field:{0}:{1}" -f $id, $requiredKey)
                    }
                }

                foreach ($key in @('id', 'kind', 'status')) {
                    if ($frontMatter.DuplicateIdentity.Contains($key)) {
                        Add-IntegrityError ("duplicate-frontmatter-identity:{0}:{1}" -f $id, $key)
                    }
                }

                if ($requiresNormativeMetadata -and $item['status'] -ceq 'active') {
                    Test-ReviewDates -Fields $frontMatter.Values -Subject document -Id $id
                }

                if ($frontMatter.Values.ContainsKey('id') -and $frontMatter.Values['id'] -ne $id) {
                    Add-IntegrityError ("frontmatter-id-mismatch:{0}:{1}" -f $id, $frontMatter.Values['id'])
                }
                if ($frontMatter.Values.ContainsKey('kind') -and $frontMatter.Values['kind'] -ne $kind) {
                    Add-IntegrityError ("frontmatter-kind-mismatch:{0}:{1}:{2}" -f $id, $frontMatter.Values['kind'], $kind)
                }
                if ($frontMatter.Values.ContainsKey('status') -and $frontMatter.Values['status'] -ne $item['status']) {
                    Add-IntegrityError ("frontmatter-status-mismatch:{0}:{1}:{2}" -f $id, $frontMatter.Values['status'], $item['status'])
                }
            }
        }
    }
}

foreach ($item in $sourceItems) {
    Test-RequiredFields -Item $item -Fields $requiredSourceFields -Label 'source'

    $id = [string]$item['id']
    if ($sourceIds.ContainsKey($id)) {
        Add-IntegrityError ("duplicate-source-id:{0}" -f $id)
    }
    else {
        $sourceIds[$id] = $true
    }

    $tier = if ($item.ContainsKey('tier')) { [string]$item['tier'] } else { $null }
    if ($null -ne $tier -and @('A', 'B', 'C', 'D') -notcontains $tier) {
        Add-IntegrityError ("invalid-source-tier:{0}:{1}" -f $id, $tier)
    }

    Test-ReviewDates -Fields $item -Subject source -Id $id -SkipBlank
}

$declaredSourceIds = [Collections.Generic.HashSet[string]]::new([string[]]@($sourceIds.Keys), [StringComparer]::Ordinal)
$sourceBearingKinds = @('governance', 'policy', 'standard', 'pattern', 'playbook', 'reference', 'decision')
foreach ($item in $catalogItems) {
    if ($sourceBearingKinds -notcontains [string]$item['kind']) {
        continue
    }

    $path = [string]$item['path']
    if ([System.IO.Path]::GetExtension($path) -ine '.md') {
        continue
    }

    $fullPath = Join-Path $repoRoot ($path.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        continue
    }

    [string]$content = Get-Content -LiteralPath $fullPath -Raw
    $reported = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($match in [regex]::Matches($content, '\bsrc-[a-z0-9][a-z0-9-]*\b')) {
        if (-not $sourceIds.ContainsKey($match.Value)) {
            Add-IntegrityError ("unknown-source-id:{0}:{1}" -f $item['id'], $match.Value)
            [void]$reported.Add($match.Value)
        }
    }
    $declared = Get-DeclaredSourceReferences -Content $content
    if (-not $declared.Valid) {
        Add-IntegrityError ("invalid-source-references:{0}" -f $item['id'])
    }
    foreach ($sourceId in $declared.Ids) {
        if (-not $declaredSourceIds.Contains($sourceId) -and $reported.Add($sourceId)) {
            Add-IntegrityError ("unknown-source-id:{0}:{1}" -f $item['id'], $sourceId)
        }
    }
}

if (-not (Test-Path -LiteralPath $skillBundlePath -PathType Leaf)) {
    Add-IntegrityError "missing-skill-bundle:agent-config/codex/skills/engineering-handbook/bundle.json"
}
else {
    try {
        $bundle = Get-Content -LiteralPath $skillBundlePath -Raw | ConvertFrom-Json
        if ($bundle.schema_version -ne 1 -or $bundle.skill_name -ne 'engineering-handbook') {
            Add-IntegrityError "invalid-skill-bundle-header"
        }

        foreach ($entry in @($bundle.include)) {
            $entryPath = [string]$entry
            $candidate = Join-Path $repoRoot ($entryPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
            if (-not (Test-Path -LiteralPath $candidate)) {
                Add-IntegrityError ("missing-skill-bundle-include:{0}" -f $entryPath)
            }
        }
    }
    catch {
        Add-IntegrityError ("invalid-skill-bundle-json:{0}" -f $_.Exception.Message)
    }
}

if ($errors.Count -gt 0) {
    foreach ($message in $errors) {
        Write-Output "ERROR $message"
    }
    Write-Output ("FAIL handbook-integrity errors={0}" -f $errors.Count)
    exit 1
}

Write-Output ("PASS handbook-integrity catalog={0} sources={1}" -f $catalogItems.Count, $sourceItems.Count)
exit 0
