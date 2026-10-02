import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from minhtri.mcp_readonly import (
    BRAIN_HOME_ENV,
    BrainMCPConfigError,
    READONLY_TOOL_NAMES,
    resolve_brain_home,
)


class DedicatedReadonlyMCPContract(unittest.TestCase):
    def test_tool_allowlist_is_exactly_readonly_brain_surface(self):
        self.assertEqual(
            READONLY_TOOL_NAMES,
            ("brain.verify", "brain.recovery_packet"),
        )
        self.assertNotIn("ledger.apply", READONLY_TOOL_NAMES)

    def test_brain_home_is_fixed_from_process_environment(self):
        with tempfile.TemporaryDirectory() as td:
            with patch.dict(os.environ, {BRAIN_HOME_ENV: td}, clear=False):
                self.assertEqual(resolve_brain_home(), Path(td).resolve())

    def test_missing_brain_home_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(BrainMCPConfigError):
                resolve_brain_home()


if __name__ == "__main__":
    unittest.main()
