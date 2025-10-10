Param([string]$EnvFile = ".env")

if (-not (Test-Path $EnvFile)) { throw "Missing $EnvFile" }

Get-Content $EnvFile | ForEach-Object {
  if ($_ -match '^\s*#') { return }
  if ($_ -match '^\s*$') { return }
  $k,$v = $_ -split '=',2
  [System.Environment]::SetEnvironmentVariable($k.Trim(), $v.Trim(), 'Process')
}
Write-Host "Loaded env from $EnvFile"
