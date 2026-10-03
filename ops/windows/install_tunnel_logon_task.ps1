$ErrorActionPreference = 'Stop'

$runtime = $PSScriptRoot
$launcher = Join-Path $runtime 'run_tunnel_unattended.ps1'
$sealed = Join-Path $env:LOCALAPPDATA 'MINH_TRI\tunnel.runtime.dpapi'
$taskName = 'MINH_TRI_Readonly_Tunnel'

if (!(Test-Path $launcher)) { throw 'BLOCKED_UNATTENDED_LAUNCHER_MISSING' }
if (!(Test-Path $sealed)) { throw 'BLOCKED_TUNNEL_DPAPI_SECRET_MISSING' }
$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $launcher + '"')
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $identity
$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
$task = Get-ScheduledTask -TaskName $taskName
$actions = @($task.Actions | ForEach-Object { [pscustomobject]@{ Execute=$_.Execute; Arguments=$_.Arguments } })
if (($actions | ConvertTo-Json -Compress) -match '(?i)api[_-]?key|token|secret') {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    throw 'BLOCKED_SECRET_MATERIAL_IN_TASK_ARGUMENTS'
}
[pscustomobject]@{ status='LOGON_TASK_INSTALLED'; task_name=$taskName; user=$identity; run_level='Limited'; trigger='AtLogOn'; secret_in_task_arguments=$false } | ConvertTo-Json -Compress
