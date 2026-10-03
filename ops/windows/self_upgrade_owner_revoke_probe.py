"""Owner-PC integrated self-upgrade revoke proof without PowerShell script execution.

The Python process invokes PowerShell with -Command only to unseal the existing DPAPI
Owner secret in memory. It does not change Windows ExecutionPolicy and never prints or
persists the plaintext secret.

Run from the canonical repository root on the Owner PC.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from minhtri.owner import config_path, load_owner_config
from minhtri.self_upgrade_runtime import SelfUpgradeSession
from minhtri.upgrade_lease import DEFAULT_UPGRADE_SCOPES, LeaseRevokedError, issue_upgrade_lease


def unseal_owner_secret() -> str:
    sealed = Path(os.environ["LOCALAPPDATA"]) / "MINH_TRI" / "owner.secret.dpapi"
    if not sealed.is_file():
        raise RuntimeError("BLOCKED_OWNER_DPAPI_SECRET_MISSING")

    env = os.environ.copy()
    env["MINHTRI_SEALED_OWNER_SECRET_PATH"] = str(sealed)
    script = r"""
$enc=(Get-Content -Raw $env:MINHTRI_SEALED_OWNER_SECRET_PATH).Trim()
if([string]::IsNullOrWhiteSpace($enc)){throw 'BLOCKED_EMPTY_DPAPI_SECRET'}
$sec=ConvertTo-SecureString $enc
$b=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
try {[Runtime.InteropServices.Marshal]::PtrToStringBSTR($b)}
finally {if($b -ne [IntPtr]::Zero){[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b)}}
"""
    proc = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", script],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    secret = proc.stdout.rstrip("\r\n")
    if not secret:
        raise RuntimeError("BLOCKED_OWNER_DPAPI_UNSEAL_EMPTY")
    return secret


def main() -> int:
    secret = ""
    try:
        cfg = load_owner_config(config_path(None))
        owner_id = cfg["owner_id"]
        secret = unseal_owner_secret()

        lease = issue_upgrade_lease(
            actor=owner_id,
            secret=secret,
            duration_seconds=60,
            parent_generation="GEN-CURRENT",
            target_generation="GEN-OWNER-PC-REVOKE-PROOF",
            scope=DEFAULT_UPGRADE_SCOPES,
        )
        session = SelfUpgradeSession(lease)
        session.owner_revoke(
            actor=owner_id,
            secret=secret,
            reason="owner-pc-integrated-revoke-proof",
        )

        marker: list[str] = []
        blocked = False
        try:
            session.guarded_mutation(lambda: marker.append("MUTATED_AFTER_REVOKE"))
        except LeaseRevokedError:
            blocked = True

        if marker or not blocked:
            raise RuntimeError("OWNER_REVOKE_PROOF_FAILED")

        result = {
            "status": "PASS_OWNER_REVOKE_E2E",
            "lease_id": lease.lease_id,
            "owner_id": owner_id,
            "runtime_status": session.guard.status,
            "post_revoke_mutation_blocked": blocked,
            "automatic_renewal": False,
            "automatic_candidate_promotion": False,
            "automatic_verified_promotion": False,
            "execution_policy_changed": False,
            "plaintext_secret_persisted": False,
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    finally:
        secret = ""


if __name__ == "__main__":
    raise SystemExit(main())
