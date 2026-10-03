"""Read-only frozen ledger export for offline audit."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
from typing import Any

from .core import GateError, Ledger


class FrozenLedgerExportError(RuntimeError):
    pass


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def export_verified_ledger_snapshot(
    ledger_home: str | Path,
    output_dir: str | Path,
    *,
    runtime_flags: dict[str, Any],
) -> dict[str, Any]:
    """Freeze a verified copy without starting Brain or autonomy runtimes."""
    for key in ("autonomous_learning_runtime", "automatic_self_critique_runtime", "meta_learning_runtime"):
        if runtime_flags.get(key) is not False:
            raise FrozenLedgerExportError(f"{key} must be false during audit export")

    ledger = Ledger(Path(ledger_home))
    target = Path(output_dir)
    if target.exists():
        raise FrozenLedgerExportError("output_dir must not already exist")

    ledger.home.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(ledger.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise FrozenLedgerExportError("ledger writer is active; refusing audit export") from exc

    try:
        os.close(fd)
        _, count, head = ledger.verify()
        target.mkdir(parents=True)
        events_out = target / "events.jsonl"
        state_out = target / "state.json"
        shutil.copyfile(ledger.events, events_out)
        shutil.copyfile(ledger.snapshot, state_out)
        manifest = {
            "schema": "minhtri-frozen-ledger-export/v1",
            "event_count": count,
            "ledger_head": head,
            "events_sha256": _sha256_file(events_out),
            "state_sha256": _sha256_file(state_out),
            "brain_service_started": False,
            "autonomy_runtime_started": False,
            "source_mutated": False,
        }
        (target / "manifest.json").write_text(
            json.dumps(manifest, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return manifest
    finally:
        ledger.lock.unlink(missing_ok=True)
