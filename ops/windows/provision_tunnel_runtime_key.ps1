$ErrorActionPreference = 'Stop'

$local = Join-Path $env:LOCALAPPDATA 'MINH_TRI'
$sealed = Join-Path $local 'tunnel.runtime.dpapi'
New-Item -ItemType Directory -Force -Path $local | Out-Null

Write-Host 'PASTE TUNNEL RUNTIME API KEY, THEN PRESS ENTER:' -ForegroundColor Cyan
$secure = Read-Host -AsSecureString
if ($null -eq $secure) { throw 'BLOCKED_EMPTY_TUNNEL_KEY' }

$encrypted = ConvertFrom-SecureString $secure
if ([string]::IsNullOrWhiteSpace($encrypted)) { throw 'BLOCKED_DPAPI_SEAL_FAILED' }
$tmp = $sealed + '.tmp'
Set-Content -Path $tmp -Value $encrypted -Encoding utf8NoBOM
Move-Item -Force $tmp $sealed

$principal = "$env:USERDOMAIN\$env:USERNAME"
& icacls $sealed /inheritance:r /grant:r "$principal:(R,W)" | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'BLOCKED_SECRET_ACL_FAILED' }

[pscustomobject]@{ status='TUNNEL_RUNTIME_KEY_DPAPI_PROVISIONED'; sealed_path=$sealed; plaintext_persisted=$false; scope='CURRENT_USER_DPAPI' } | ConvertTo-Json -Compress
