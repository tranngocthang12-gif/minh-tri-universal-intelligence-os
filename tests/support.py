import hashlib
import json
from contextlib import contextmanager
from pathlib import Path
from unittest import mock


TEST_OWNER = "test-owner"
TEST_SECRET = "test-secret"


def write_owner_config(root: str | Path) -> Path:
    path = Path(root) / "owner.json"
    path.write_text(json.dumps({
        "owner_id": TEST_OWNER,
        "owner_secret_sha256": hashlib.sha256(TEST_SECRET.encode("utf-8")).hexdigest(),
    }), encoding="utf-8")
    return path


@contextmanager
def owner_config(config: Path):
    with mock.patch("minhtri.owner.config_path", return_value=config):
        yield


def ledger_apply(ledger, command, config: Path):
    with owner_config(config):
        return ledger.apply(command, actor=TEST_OWNER, secret=TEST_SECRET)


def ledger_repair(ledger, config: Path):
    with owner_config(config):
        return ledger.repair_snapshot(actor=TEST_OWNER, secret=TEST_SECRET)
