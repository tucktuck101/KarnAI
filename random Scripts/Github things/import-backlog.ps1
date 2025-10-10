param(
  [Parameter(Mandatory = $true)]
  [string]$JsonPath,

  [Parameter(Mandatory = $true)]
  [string]$Repo, # e.g. "tucktuck101/karnai"

  [switch]$DryRun
)

# --- Auth check via gh CLI ---
$token = gh auth token 2>$null
if (-not $token) {
  Write-Error "GitHub CLI not authenticated. Run: gh auth login"
  exit 1
}

function Invoke-GitHubApi {
  param(
    [string]$Path,
    [ValidateSet("GET","POST","PATCH")] [string]$Method = "GET",
    [hashtable]$Body = $null
  )
  $args = @("api", "-X", $Method, $Path)
  if ($Body) {
    $json = ($Body | ConvertTo-Json -Depth 20)
    $args += @("--input", "-")
    $out = $json | gh @args
  } else {
    $out = gh @args
  }
  if ($LASTEXITCODE -ne 0) {
    throw "GitHub API call failed: $Path"
  }
  if ($out) { return $out | ConvertFrom-Json }
  return $null
}

# --- Labels bootstrap ---
$RequiredLabels = @(
  @{ name = "Epic";    color = "5319e7"; description = "High-level initiative" },
  @{ name = "Feature"; color = "1d76db"; description = "Deliverable capability" },
  @{ name = "Task";    color = "0e8a16"; description = "Actionable work item" }
)

function Ensure-Label {
  param([string]$Name, [string]$Color, [string]$Description)
  # Try fetch, else create
  $existing = gh api "repos/$Repo/labels/$Name" 2>$null | ConvertFrom-Json
  if ($LASTEXITCODE -eq 0 -and $existing) { return }
  Write-Host "Creating label: $Name"
  if ($DryRun) { return }
  Invoke-GitHubApi -Path "repos/$Repo/labels" -Method POST -Body @{
    name = $Name; color = $Color; description = $Description
  } | Out-Null
}

foreach ($lbl in $RequiredLabels) { Ensure-Label -Name $lbl.name -Color $lbl.color -Description $lbl.description }

# --- Utilities ---
function Find-IssueByKey {
  param([string]$Key)
  # Prefer searching in:title for speed; fall back to in:body for robustness
  $q = "repo:$Repo in:title `"$Key:`""
  $res = gh api "search/issues?q=$q&per_page=1" | ConvertFrom-Json
  if ($res.total_count -gt 0) { return $res.items[0].number }

  $q2 = "repo:$Repo in:body `\"KEY: $Key`""
  $res2 = gh api "search/issues?q=$q2&per_page=1" | ConvertFrom-Json
  if ($res2.total_count -gt 0) { return $res2.items[0].number }

  return $null
}

function New-Issue {
  param(
    [string]$Key,
    [string]$Title,
    [string]$Body,
    [string[]]$Labels
  )
  $displayTitle = "$Key: $Title"
  $existing = Find-IssueByKey -Key $Key
  if ($existing) {
    Write-Host "Skip (exists) $Key -> #$existing"
    return $existing
  }

  $fullBody = @"
<!--KEY: $Key -->
$Body
"@

  if ($DryRun) {
    Write-Host "[DryRun] Would create: $displayTitle [$($Labels -join ', ')]"
    return $null
  }

  $created = Invoke-GitHubApi -Path "repos/$Repo/issues" -Method POST -Body @{
    title  = $displayTitle
    body   = $fullBody
    labels = $Labels
  }
  Write-Host "Created $Key -> #$($created.number)"
  return $created.number
}

# --- Load JSON input ---
if (-not (Test-Path $JsonPath)) { Write-Error "File not found: $JsonPath"; exit 1 }
$data = Get-Content -Raw $JsonPath | ConvertFrom-Json

# Expect arrays: epics[], features[], tasks[]
$epics    = @($data.epics)    | Where-Object { $_ }
$features = @($data.features) | Where-Object { $_ }
$tasks    = @($data.tasks)    | Where-Object { $_ }

# Maps for parent linkage
$issueByKey = @{}

# --- Pass A: Epics ---
foreach ($e in $epics) {
  # Fields: key, title, cr_ref, wsjf, estimate, details (optional)
  $bodyLines = @()
  if ($e.cr_ref)     { $bodyLines += "CR: $($e.cr_ref)" }
  if ($e.details)    { $bodyLines += "Details: $($e.details)" } else { $bodyLines += "Details: TBD" }
  $bodyLines += "WSJF: $($e.wsjf   | ForEach-Object { if ($_){$_} else {1} })"
  $bodyLines += "Estimate: $($e.estimate | ForEach-Object { if ($_){$_} else {1} })"

  $num = New-Issue -Key $e.key -Title $e.title -Body ($bodyLines -join "`n") -Labels @("Epic")
  if ($num) { $issueByKey[$e.key] = $num }
}

# --- Pass B: Features ---
foreach ($f in $features) {
  # Fields: key, parent_key, title, cr_ref, wsjf, estimate, details
  $parent = $issueByKey[$f.parent_key]
  if (-not $parent) {
    Write-Warning "Parent not found for Feature $($f.key) (parent_key=$($f.parent_key)). Create Epics first."
    continue
  }
  $bodyLines = @("Parent: #$parent")
  if ($f.cr_ref)     { $bodyLines += "CR: $($f.cr_ref)" }
  if ($f.details)    { $bodyLines += "Details: $($f.details)" } else { $bodyLines += "Details: TBD" }
  $bodyLines += "WSJF: $($f.wsjf   | ForEach-Object { if ($_){$_} else {1} })"
  $bodyLines += "Estimate: $($f.estimate | ForEach-Object { if ($_){$_} else {1} })"

  $num = New-Issue -Key $f.key -Title $f.title -Body ($bodyLines -join "`n") -Labels @("Feature")
  if ($num) { $issueByKey[$f.key] = $num }
}

# --- Pass C: Tasks ---
foreach ($t in $tasks) {
  # Fields: key, parent_key, title, details, criteria[], wsjf, estimate
  $parent = $issueByKey[$t.parent_key]
  if (-not $parent) {
    Write-Warning "Parent not found for Task $($t.key) (parent_key=$($t.parent_key)). Create Features first."
    continue
  }
  $bodyLines = @("Parent: #$parent")
  $bodyLines += "Details: $($t.details | ForEach-Object { if ($_){$_} else {'TBD'} })"
  if ($t.criteria) {
    $bodyLines += "Acceptance Criteria:"
    foreach ($c in $t.criteria) { $bodyLines += "- $c" }
  } else {
    $bodyLines += "Acceptance Criteria:`n- TBD"
  }
  $bodyLines += "WSJF: $($t.wsjf   | ForEach-Object { if ($_){$_} else {1} })"
  $bodyLines += "Estimate: $($t.estimate | ForEach-Object { if ($_){$_} else {1} })"

  $num = New-Issue -Key $t.key -Title $t.title -Body ($bodyLines -join "`n") -Labels @("Task")
  if ($num) { $issueByKey[$t.key] = $num }
}

Write-Host "Done."
