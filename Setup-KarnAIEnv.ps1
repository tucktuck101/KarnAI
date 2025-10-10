# Setup-KarnAIEnv.ps1
$ErrorActionPreference = 'Stop'

function Write-File([string]$Path, [string]$Content) {
  $dir = Split-Path -Parent $Path
  if ($dir -and -not (Test-Path $dir)) { New-Item -Type Directory -Path $dir -Force | Out-Null }
  Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8 -Force
}

# 1) .env (no secrets)
if (-not (Test-Path ".env")) {
  $sqlHost = Read-Host "SQL server (localhost, .\SQLEXPRESS, or (localdb)\MSSQLLocalDB)"
  $sqlPort = Read-Host "SQL port (blank for named instance)"
  $sqlDb   = Read-Host "Database name"
  $sqlUser = Read-Host "SQL username (blank for Windows auth)"
  @"
SQLSERVER_SERVER=$sqlHost
SQLSERVER_PORT=$sqlPort
SQLSERVER_DB=$sqlDb
SQLSERVER_USER=$sqlUser
"@ | Set-Content -Encoding UTF8 .env
}

# 2) examples and ignore
Write-File ".env.example" @"
SQLSERVER_SERVER=localhost
SQLSERVER_PORT=1433
SQLSERVER_DB=KarnAI
SQLSERVER_USER=
# Password is NOT stored. You will be prompted if SQL auth is used.
"@
if (Test-Path ".gitignore") {
  if (-not (Select-String -Path .gitignore -SimpleMatch ".env" -Quiet)) { Add-Content .gitignore "`n.env" }
} else {
  Set-Content .gitignore ".env"
}

# 3) loader
New-Item -Type Directory -Force -Path scripts | Out-Null
Write-File "scripts/Set-KarnAIEnv.ps1" @"
Param([string]\$EnvFile = ".env")
if (-not (Test-Path \$EnvFile)) { throw "Missing \$EnvFile" }
Get-Content \$EnvFile | ForEach-Object {
  if (\$_ -match '^\s*#') { return }
  if (\$_ -match '^\s*$') { return }
  \$k,\$v = \$_ -split '=',2
  [System.Environment]::SetEnvironmentVariable(\$k.Trim(), \$v.Trim(), 'Process')
}
Write-Host "Loaded env from \$EnvFile"
"@

# 4) sqlcmd helpers (Windows auth if SQLSERVER_USER is empty; otherwise prompt for password)
New-Item -Type Directory -Force -Path etl/bin | Out-Null

Write-File "etl/bin/sqlcmd_all.ps1" @"
Param([string]\$Path)
\$ErrorActionPreference = 'Stop'
. scripts/Set-KarnAIEnv.ps1
function Get-ConnArgs {
  \$server = \$Env:SQLSERVER_SERVER
  \$db     = \$Env:SQLSERVER_DB
  \$user   = \$Env:SQLSERVER_USER
  if ([string]::IsNullOrWhiteSpace(\$user)) {
    return @('-S', \$server, '-d', \$db, '-E', '-b)
  } else {
    \$pwd = Read-Host -AsSecureString "SQL password for '\$user'"
    \$b   = [Runtime.InteropServices.Marshal]::SecureStringToBSTR(\$pwd)
    try { \$plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(\$b) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR(\$b) }
    return @('-S', \$server, '-d', \$db, '-U', \$user, '-P', \$plain, '-b)
  }
}
function Invoke-SqlFile { param([string]\$FilePath); Write-Host "Running \$FilePath"; & sqlcmd (Get-ConnArgs) -i \$FilePath }
if (Test-Path \$Path -PathType Container) {
  Get-ChildItem -Path \$Path -Recurse -Filter *.sql | Sort-Object FullName | ForEach-Object { Invoke-SqlFile -FilePath \$_.FullName }
} else {
  Invoke-SqlFile -FilePath \$Path
}
"@

Write-File "etl/bin/run_dim_merges.ps1" @"
Param([string]\$Folder = 'etl/sql/merge/dims')
\$ErrorActionPreference = 'Stop'
. scripts/Set-KarnAIEnv.ps1
function Get-ConnArgs {
  \$server = \$Env:SQLSERVER_SERVER
  \$db     = \$Env:SQLSERVER_DB
  \$user   = \$Env:SQLSERVER_USER
  if ([string]::IsNullOrWhiteSpace(\$user)) {
    return @('-S', \$server, '-d', \$db, '-E', '-b)
  } else {
    \$pwd = Read-Host -AsSecureString "SQL password for '\$user'"
    \$b   = [Runtime.InteropServices.Marshal]::SecureStringToBSTR(\$pwd)
    try { \$plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(\$b) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR(\$b) }
    return @('-S', \$server, '-d', \$db, '-U', \$user, '-P', \$plain, '-b)
  }
}
function Invoke-SqlFile { param([string]\$FilePath); Write-Host "Running \$FilePath"; & sqlcmd (Get-ConnArgs) -i \$FilePath }
Get-ChildItem -Path \$Folder -Filter *.sql | Sort-Object FullName | ForEach-Object { Invoke-SqlFile -FilePath \$_.FullName }
"@

Write-Host "Env + helpers created. Next:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/Set-KarnAIEnv.ps1"
Write-Host "  sqlcmd test (Windows auth): sqlcmd -S $Env:SQLSERVER_SERVER -d $Env:SQLSERVER_DB -E -Q 'SELECT DB_NAME();'"
Write-Host "  or run: powershell -ExecutionPolicy Bypass -File etl\bin\sqlcmd_all.ps1 etl\sql\staging\005_stg_catalog.sql"
