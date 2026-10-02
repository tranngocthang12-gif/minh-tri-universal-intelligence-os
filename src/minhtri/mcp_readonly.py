"""Dedicated MCP boundary for the local MINH TRI brain.

The server exposes exactly two read-only tools over MCP:
- brain.verify
- brain.recovery_packet

The brain path is fixed when the process starts. Remote MCP callers cannot select a
filesystem path and no mutation, shell, or arbitrary file tool is registered.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .brain_readonly import BrainReader

BRAIN_HOME_ENV = "MINHTRI_BRAIN_HOME"
READONLY_TOOL_NAMES = ("brain.verify", "brain.recovery_packet")


class BrainMCPConfigError(ValueError):
    pass


def resolve_brain_home() -> Path:
    value = os.environ.get(BRAIN_HOME_ENV)
    if not value:
        raise BrainMCPConfigError(f"{BRAIN_HOME_ENV} is required")
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise BrainMCPConfigError("configured brain home is not a directory")
    return path


def build_server(fixed_home: str | Path):
    """Build an MCP server whose brain path is fixed before any remote request."""
    try:
        from mcp.server.mcpserver import MCPServer
    except ModuleNotFoundError as exc:
        raise BrainMCPConfigError(
            "MCP runtime dependency missing; install package extra: [mcp]"
        ) from exc

    home = Path(fixed_home).expanduser().resolve()
    reader = BrainReader(home)
    server = MCPServer(
        name="minh-tri-local-brain-readonly",
        title="MINH TRI Local Brain Read-Only",
        description="Read-only access to the verified MINH TRI local brain ledger.",
        instructions=(
            "Only brain.verify and brain.recovery_packet are exposed. "
            "No mutation, shell, filesystem, or caller-selected brain path."
        ),
        version="0.1.0",
    )

    @server.tool(
        name="brain.verify",
        description="Verify the fixed local brain and return event_count and head.",
    )
    def brain_verify() -> dict[str, Any]:
        return reader.verify()

    @server.tool(
        name="brain.recovery_packet",
        description=(
            "Return verified bootstrap state from the fixed local brain: "
            "head, active focus, and optional lesson matches."
        ),
    )
    def brain_recovery_packet(
        query: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        return reader.recovery_packet(query=query, limit=limit)

    return server


def main() -> int:
    server = build_server(resolve_brain_home())
    server.run("stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
