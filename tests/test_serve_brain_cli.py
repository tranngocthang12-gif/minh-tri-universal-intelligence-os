import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from minhtri.cli import main
from minhtri.core import Ledger


class ServeBrainCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "brain"
        Ledger(self.home).init()

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_token_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            code = main(["--home", str(self.home), "serve-brain"])
        self.assertEqual(code, 2)

    @patch("minhtri.cli.BrainHTTPHost")
    def test_serve_brain_uses_fixed_home_and_read_only_status(self, host_cls):
        instance = host_cls.return_value
        instance.url = "http://127.0.0.1:8765/v1/brain"
        instance.serve_forever.side_effect = KeyboardInterrupt
        out = io.StringIO()
        with patch.dict(os.environ, {"MINHTRI_BRAIN_TOKEN": "x" * 40}, clear=True):
            with self.assertRaises(KeyboardInterrupt):
                with redirect_stdout(out):
                    main(["--home", str(self.home), "serve-brain", "--port", "8765"])
        host_cls.assert_called_once_with(self.home, "x" * 40, host="127.0.0.1", port=8765)
        self.assertIn('"write_capability": false', out.getvalue().lower())


if __name__ == "__main__":
    unittest.main()
