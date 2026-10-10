# PC Reconnect & Sync V1 — Owner authorized candidate

Status: CLASS S CANDIDATE. Owner authorized building reconnect + sync, **not** activating a new unattended task or protected merge without required CI and acceptance. Protected main remains FROZEN.

## Capability
The Python candidate (stdlib-only) pins GitHub **protected main**, reads a bounded manifest-selected set of canonical documents at one commit SHA, verifies each Git blob SHA and UTF-8/size, checks bootstrap/current/task route consistency, then can write a separate versioned copy in `minhtri-runtime-current/pc-reconnect-sync`. An atomic `current.json` pointer references the last locally verified snapshot; previous cache is verified before replacement and GitHub compare refuses rollback. Unmerged Draft PR changes are not copied. No downloaded file is run.

**Version 1 default: DRY RUN;** `--apply` needs a destination and is not automatically invoked. It does not write the GitHub repo, Tier-1 Local Brain, task registry, secrets, or any personal folder. Canonical authority remains protected GitHub main. Snapshot integrity is not independent proof of doctrinal truth, semantic mastery, actor identity or source authenticity. A `DONE` active-task pointer produces a warning, not a silent promotion.

## Scope, security and caveats
- Public GitHub API only, no authentication material. Current repo is public. If repo becomes private, stop; do not silently expand credential access.
- Cache location may contain **no symlink/junction**. Local permissions and external filesystem tampering are outside V1 scope. A local attacker may manipulate cache/pointer; this is NOT an adversarially authenticated device trust store.
- The cache stores plain copies of authorized public documents; no incoming code execution, automatic GitHub sync write, self-verified knowledge or unattended background runtime.
- Digest protection relies on TLS + GitHub REST + Git blob; it is NOT independent cryptographic signature verification or protected-main merge-receipt validation.
- Protected-main status and source identity from GitHub REST are trusted, not independently attested.
- Fixed bounded selection includes A172 as the latest completed Buddhist-thought checkpoint; no A173 Draft/PR artifact copied into the accepted cache.
- The `install_tunnel_logon_task.ps1` and `run_tunnel_unattended.ps1` on the Owner PC are pre-existing and separate. Live Task Scheduler had `MINH_TRI_Readonly_Tunnel` RUNNING; this is NOT reconnect-sync job installation or reboot persistence proof.
- The local runtime host remains noncanonical. Do not overwrite the Local Brain ledger and do not allow new PC-user data ingestion.

## Gates before activation
1. Exact-head CI and independent Class S review: route spoof, content hash spoof, path traversal, symlinks/junctions, rollback, partial writes, active-task status, private repo refusal, unauthorized learning paths, and GitHub outage fail-closed.
2. Correct all material findings and rerun exact-head tests.
3. Owner or designated independent acceptance + protected merge, then fresh-read main.
4. Staged *dry-run only* on Owner PC, compare fixed SHA/selected file hashes against GitHub.
5. Owner-authorized narrow local `--apply` smoke to **noncanonical cache**, verify pointer/rollback behavior; never mutate Local Brain or auto-merge.
6. Only then propose a separate scoped Windows logon-runner installation. An unattended scheduled task is NOT yet authorized/installed. Prove logon restart separately, with no boot-before-login promise.

## Ownership
Implementation contract: `src/minhtri/pc_reconnect_sync.py`
Selection contract: `config/pc_reconnect_sync_selection_v1.json`
Synthetic tests: `tests/test_pc_reconnect_sync.py`
GitHub protected main: single canonical memory.
PC mirror: disposable, verified, noncanonical.
