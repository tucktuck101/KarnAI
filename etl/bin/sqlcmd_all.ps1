Param([string]\)
\Stop = 'Stop'
. scripts/Set-KarnAIEnv.ps1
function Get-ConnArgs {
  \ = \
  \     = \
  \   = \
  if ([string]::IsNullOrWhiteSpace(\)) {
    return @('-S', \, '-d', \, '-E', '-b')
  } else {
    \D:\devprojects\KarnAI\KarnAI = Read-Host -AsSecureString "SQL password for '\'"
    \   = [Runtime.InteropServices.Marshal]::SecureStringToBSTR(\D:\devprojects\KarnAI\KarnAI)
    try { \ = [Runtime.InteropServices.Marshal]::PtrToStringAuto(\) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR(\) }
    return @('-S', \, '-d', \, '-U', \, '-P', \, '-b')
  }
}
function Invoke-SqlFile { param([string]\) Write-Host "Running \"; & sqlcmd (Get-ConnArgs) -i \ }
if (Test-Path \ -PathType Container) {
  Get-ChildItem -Path \ -Recurse -Filter *.sql | Sort-Object FullName | ForEach-Object { Invoke-SqlFile -FilePath \.FullName }
} else {
  Invoke-SqlFile -FilePath \
}
