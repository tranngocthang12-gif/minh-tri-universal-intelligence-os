import asyncio
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from minhtri.core import Ledger
from tests.support import ledger_apply, write_owner_config


class DedicatedMCPIntegration(unittest.TestCase):
    def test_real_mcp_runtime_exposes_only_readonly_tools(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            home = root / "brain"
            config = write_owner_config(root)
            ledger = Ledger(home)
            ledger.init()
            ledger_apply(
                ledger,
                {
                    "type": "register_domain",
                    "data": {
                        "id": "youtube",
                        "name": "YouTube",
                        "risk_class": "NORMAL",
                        "measurement_contract": "views",
                    },
                },
                config,
            )
            ledger_apply(
                ledger,
                {
                    "type": "record_source",
                    "data": {
                        "id": "src1",
                        "domain_id": "youtube",
                        "uri": "owner://focus",
                        "captured_at": "2026-10-01T00:00:00Z",
                        "kind": "FIRST_PARTY",
                        "rights_status": "CLEAR",
                    },
                },
                config,
            )
            ledger_apply(
                ledger,
                {
                    "type": "set_learning_focus",
                    "data": {
                        "id": "focus1",
                        "status": "ACTIVE",
                        "domain_id": "youtube",
                        "source_id": "src1",
                        "note": "chat quên, sổ không",
                        "expected_lesson": "recover continuity",
                        "uncertainty": "UNTESTED",
                    },
                },
                config,
            )
            result = asyncio.run(self._exercise_mcp(home))

        self.assertEqual(result["tools"], ["brain.verify", "brain.recovery_packet"])
        self.assertEqual(result["verify"]["status"], "VALID")
        self.assertEqual(result["verify"]["event_count"], 3)
        self.assertEqual(result["recovery"]["focus"]["domain_id"], "youtube")
        self.assertEqual(result["recovery"]["focus"]["note"], "chat quên, sổ không")
        self.assertTrue(result["mutation_rejected"])

    async def _exercise_mcp(self, home: Path) -> dict:
        env = dict(os.environ)
        env["MINHTRI_BRAIN_HOME"] = str(home)
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "minhtri.mcp_readonly"],
            env=env,
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                verify = await session.call_tool("brain.verify", {})
                recovery = await session.call_tool("brain.recovery_packet", {})
                mutation = await session.call_tool("ledger.apply", {})

        def decode(result):
            self.assertFalse(result.is_error)
            self.assertTrue(result.content)
            return json.loads(result.content[0].text)

        return {
            "tools": [tool.name for tool in tools.tools],
            "verify": decode(verify),
            "recovery": decode(recovery),
            "mutation_rejected": bool(mutation.is_error),
        }


if __name__ == "__main__":
    unittest.main()
