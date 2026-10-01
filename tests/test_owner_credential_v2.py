import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from minhtri.owner import OwnerGateError, load_owner_config, require_owner


def v2(secret="test-secret", credential_id="cred-2", revoked=False, iterations=200000):
    salt = bytes.fromhex("00112233445566778899aabbccddeeff")
    verifier = hashlib.pbkdf2_hmac("sha256", secret.encode(), salt, iterations).hex()
    return {
        "version": 2, "scheme": "pbkdf2-sha256", "iterations": iterations,
        "salt": salt.hex(), "verifier": verifier,
        "credential_id": credential_id, "revoked": revoked,
    }


class OwnerCredentialV2(unittest.TestCase):
    def write(self, payload):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "owner.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_v2_correct_secret_passes(self):
        path = self.write({"owner_id": "test-owner", "credential": v2()})
        self.assertEqual(require_owner("test-owner", "test-secret", path), "test-owner")

    def test_v2_wrong_secret_fails(self):
        path = self.write({"owner_id": "test-owner", "credential": v2()})
        with self.assertRaises(OwnerGateError) as ctx:
            require_owner("test-owner", "wrong", path)
        self.assertEqual(ctx.exception.code, "OWNER_SECRET_MISMATCH")

    def test_revoked_fails_closed(self):
        path = self.write({"owner_id": "test-owner", "credential": v2(revoked=True)})
        with self.assertRaises(OwnerGateError):
            require_owner("test-owner", "test-secret", path)

    def test_unknown_scheme_fails_closed(self):
        cred = v2()
        cred["scheme"] = "unknown"
        path = self.write({"owner_id": "test-owner", "credential": cred})
        with self.assertRaises(OwnerGateError):
            load_owner_config(path)

    def test_below_minimum_iterations_fails(self):
        path = self.write({"owner_id": "test-owner", "credential": v2(iterations=1000)})
        with self.assertRaises(OwnerGateError):
            require_owner("test-owner", "test-secret", path)

    def test_dual_v1_v2_config_fails_no_fallback(self):
        path = self.write({
            "owner_id": "test-owner",
            "owner_secret_sha256": hashlib.sha256(b"test-secret").hexdigest(),
            "credential": v2(),
        })
        with self.assertRaises(OwnerGateError):
            load_owner_config(path)

    def test_v1_remains_explicitly_compatible_during_migration(self):
        path = self.write({
            "owner_id": "test-owner",
            "owner_secret_sha256": hashlib.sha256(b"test-secret").hexdigest(),
        })
        self.assertEqual(require_owner("test-owner", "test-secret", path), "test-owner")


if __name__ == "__main__":
    unittest.main()
