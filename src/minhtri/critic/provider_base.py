"""Provider interface for external critic channels."""
from __future__ import annotations

from typing import Any, Protocol


class ExternalCriticProvider(Protocol):
    def critique(self, packet: dict[str, Any]) -> dict[str, Any]:
        """Return PENDING, RECORDED, or CRITIC_RUN_INVALID metadata."""
        ...
