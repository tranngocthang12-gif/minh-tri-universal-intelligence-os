# MINH TRÍ — FOUNDATION GATE EXECUTION RUNBOOK — 2026-10-03

**Status:** CURRENT GATE ORDER / HISTORICAL COMMAND EXAMPLES / FAIL-CLOSED / OWNER-SECRET-SAFE  
**Purpose:** exact remaining work and commands after backlog cleanup.  
**Rule:** never paste live secrets into chat, GitHub, task arguments, command history, or evidence files.

## Gate 1 — Boot/reboot persistence

Historical preflight at 2026-10-03 14:01 +07:00:
- corrected `provision_tunnel_runtime_key.ps1` parsed cleanly on Owner PC;
- dedicated tunnel DPAPI secret was absent;
- `MINH_TRI_Readonly_Tunnel` logon task was absent;
- tunnel was live only for that session.

Newer remote observation at 2026-10-03 15:35 +07:00:
- read-only connector UNREACHABLE (`tunnel-client` not seen for 300 seconds);
- Desktop Commander offline;
- local task/process state cannot be inspected remotely;
- root cause remains UNKNOWN and persistence remains NOT_PROVEN.

### Historical/manual contingency

The command examples below are retained for break-glass/manual recovery provenance. Under the current One Door operating model, the AI seat should use authorized maintenance tooling directly when available and should not require the Owner to type these commands unless the Owner asks or the tooling cannot perform the required secure local action.

Historical command example:

```powershell
Set-Location 'C:\Users\trann\OneDrive\Desktop\minhtri-runtime-current'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\provision_tunnel_runtime_key.ps1
```

Paste the **current tunnel runtime API key only into that local secure prompt**. Do not paste it into chat.

Historical task-install example:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install_tunnel_logon_task.ps1
```

Historical/manual pre-reboot verification example:

```powershell
Get-ScheduledTask -TaskName 'MINH_TRI_Readonly_Tunnel' | Format-List TaskName,State
Get-ScheduledTaskInfo -TaskName 'MINH_TRI_Readonly_Tunnel' | Format-List LastRunTime,LastTaskResult
```

Promotion proof requires a controlled reboot/logon with **no manual tunnel launch**, followed by:
- tunnel health `/readyz = 200 ready`;
- `brain.verify = VALID`;
- `brain.recovery_packet = VALID`;
- same event_count/head across reads.

Do not reboot before the DPAPI secret and task both exist.

## Gate 2 — Old tunnel key revocation

This gate requires provider-side credential evidence. Local deletion is not proof of provider revocation.

Required evidence:
- identify every prior tunnel runtime key/credential;
- revoke obsolete credentials in the tunnel provider/control-plane account;
- capture provider-side status showing the obsolete credential is revoked/disabled;
- verify current tunnel still works using only the new restricted key.

No local command can truthfully substitute for provider-side revocation evidence.

## Gate 3 — Endpoint protection + BitLocker

Current observation:
- Defender engine enabled, but Defender realtime/behavior/NIS/on-access report OFF;
- McAfee is registered and framework host is running;
- McAfee realtime protection remains UNKNOWN;
- BitLocker query is access denied without admin rights.

Run from an **elevated** PowerShell on Owner PC:

```powershell
Get-BitLockerVolume -MountPoint 'C:' | Format-List MountPoint,VolumeStatus,ProtectionStatus,EncryptionPercentage,EncryptionMethod,LockStatus
manage-bde -status C:
Get-MpComputerStatus | Select-Object AMServiceEnabled,AntivirusEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled,NISEnabled,OnAccessProtectionEnabled
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | Select-Object displayName,productState,pathToSignedProductExe,pathToSignedReportingExe,timestamp
```

For McAfee realtime status, use a McAfee-native status source/UI/CLI if available. Do not infer realtime protection from framework service state alone.

## Gate 4 — Genuine fresh-seat validation

This cannot be proven from the current chat.

Open a genuinely separate ChatGPT chat and send only:

```text
FRESH-SEAT VALIDATION — MINH TRÍ

Do not use prior chat history, pasted expected head/count/focus values, or claims from another seat.
Bootstrap from live canonical GitHub main:
1. docs/PROJECT_STATE.json
2. the current Law Index it points to
3. the current Architecture it points to
4. docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md
5. docs/RECOVERY_MANIFEST.json

Then inspect the connected MINH TRI brain tool surface.
It must expose exactly:
- brain.verify
- brain.recovery_packet

Call both tools.
Report their raw bounded results and the exact toolset.
Do not mark PASS yourself.
```

A separate control read must then call `brain.verify` in the validation window. The canonical validator requires matching event_count/head and no mutation exposure.

## Gate 5 — Independent witness

GitHub is not sufficient because it shares project authority.

Required target:
- storage/provider authority independent from the Owner-PC local writer and GitHub write authority;
- separate credential boundary;
- externally preserved witness receipt/anchor;
- read-back verification against the local historical ledger prefix.

Until an independent provider/credential is selected and proven, keep this gate BLOCKED.

## Gate 6 — Real external critic

Required evidence package:
- frozen learning packet/target;
- external critic provider/model/run identifier;
- blind/revealed context mode;
- exact output hash;
- verdict/reason/missing evidence;
- independence receipt bounded to the actual execution environment.

Current tools do not expose a suitable independent external critic provider, so this remains blocked rather than simulated.

## Gate 7 — Empirical Learning Assurance v1.4 validation

Do not claim improvement from implementation or CI.

Run a comparative real-work trial:
1. choose one real Owner task and freeze inputs;
2. baseline arm: execute without v1.4 planning/traces/capsule;
3. v1.4 arm: use adaptive deliberation + grounded research traces + context capsule;
4. blind-score both outputs against the same predeclared rubric;
5. record errors, unsupported claims, citation defects, omissions, and task utility;
6. repeat across multiple real tasks before any promotion claim.

Research Adapter remains blocked until genuine fresh-seat PASS; do not bypass that gate for this experiment.

## Backlog

Backlog hygiene gate closed on 2026-10-03:
- learning PRs #85/#86/#87 carried forward and merged through #116;
- dependency PR #90 refreshed and merged through #117;
- no open PR remained at the completion of this cleanup.

## Required next sequence

1. Restore Owner-PC maintenance-plane reachability and inspect current DPAPI secret, Scheduled Task, process and health state.
2. If missing/broken, repair the secret-safe logon-task path without exposing secrets.
3. Controlled reboot persistence proof with no manual tunnel launch.
4. Provider-side old-key revocation evidence.
5. Admin/vendor endpoint protection + BitLocker evidence.
6. Genuine fresh-seat validation.
7. Independent witness authority.
8. Real external critic.
9. Empirical Learning Assurance v1.4 validation.

No gate is promoted from prose, code existence, or CI alone.


## Synchronization note — 2026-10-04

Fresh observation at sync time:
- Desktop Commander maintenance device: OFFLINE;
- tunnel-client: not seen by control plane for 300 seconds;
- Local Brain read connector: DOWN through the tunnel;
- Owner PC host power state: UNKNOWN.

Current DPAPI/task state cannot be re-read while maintenance is offline. Historical evidence says the DPAPI tunnel secret and hardened logon task were later provisioned/installed after the earliest preflight recorded above; this does not prove they still exist now and does not prove reboot persistence.
