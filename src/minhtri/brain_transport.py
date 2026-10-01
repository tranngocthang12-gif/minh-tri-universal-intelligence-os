"""Pure request dispatcher for the read-only brain transport contract.

Network binding and caller authentication belong to the local/private transport host.
This module intentionally has no filesystem path parameter in remote requests and no
mutation method.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .brain_readonly import BrainReadError, BrainReader

PROTOCOL = "minhtri-brain-readonly/v1"
ALLOWED_METHODS = frozenset({"brain.verify", "brain.recovery_packet"})
MAX_QUERY_CHARS = 4096


class BrainTransportError(ValueError):
    pass


class BrainTransport:
    def __init__(self, fixed_home: str | Path):
        self._reader = BrainReader(Path(fixed_home))

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(request, dict) or set(request) != {"protocol", "method", "params"}:
            raise BrainTransportError("malformed request")
        if request["protocol"] != PROTOCOL:
            raise BrainTransportError("unsupported protocol")
        method = request["method"]
        params = request["params"]
        if method not in ALLOWED_METHODS or not isinstance(params, dict):
            raise BrainTransportError("method not allowed")
        try:
            if method == "brain.verify":
                if params:
                    raise BrainTransportError("brain.verify accepts no params")
                result = self._reader.verify()
            else:
                if set(params) - {"query", "limit"}:
                    raise BrainTransportError("unsupported recovery_packet params")
                query = params.get("query")
                if query is not None and (not isinstance(query, str) or len(query) > MAX_QUERY_CHARS):
                    raise BrainTransportError("query exceeds transport contract")
                result = self._reader.recovery_packet(query=query, limit=params.get("limit", 20))
        except BrainReadError as exc:
            raise BrainTransportError(str(exc)) from exc
        return {"protocol": PROTOCOL, "result": result}
