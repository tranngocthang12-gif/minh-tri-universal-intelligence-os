"""Read-only recovery bridge for the local MINH TRÍ brain ledger.

This module deliberately exposes no mutation API. It replays/verifies the existing
ledger through the Tier-1 core and returns small machine-readable recovery records.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .core import GateError, Ledger, current_focus


class BrainReadError(GateError):
    """The local brain could not be read or verified safely."""


class BrainReader:
    """Read-only facade over a local ledger directory."""

    def __init__(self, home: str | Path):
        self.home = Path(home)

    def _verified(self) -> tuple[dict, int, str]:
        try:
            return Ledger(self.home).verify()
        except (GateError, OSError, ValueError) as exc:
            raise BrainReadError(f"BRAIN_VERIFY_FAILED: {exc}") from exc

    def verify(self) -> dict[str, Any]:
        """Return the verified head without exposing mutable state."""
        _, count, head = self._verified()
        return {
            "status": "VALID",
            "event_count": count,
            "head": head,
        }

    def get_head(self) -> dict[str, Any]:
        """Alias-shaped recovery record for bootstrap callers."""
        return self.verify()

    def get_current_focus(self) -> dict[str, Any]:
        """Return the current learning focus, or an explicit empty state."""
        state, count, head = self._verified()
        focus = current_focus(state)
        return {
            "status": "VALID",
            "event_count": count,
            "head": head,
            "focus": focus if focus is not None else "NO_ACTIVE_FOCUS",
        }

    def recovery_packet(self, query: str | None = None, limit: int = 20) -> dict[str, Any]:
        """Return bootstrap state from one verified ledger replay/head.

        Unlike composing get_head/get_current_focus/search_lessons calls, this method
        cannot mix records from different legitimate ledger heads.
        """
        if query is not None and (not isinstance(query, str) or not query.strip()):
            raise BrainReadError("query must be nonempty text when provided")
        if type(limit) is not int or not 1 <= limit <= 100:
            raise BrainReadError("limit must be an integer from 1 to 100")

        state, count, head = self._verified()
        focus = current_focus(state)
        matches = []
        if query is not None:
            needle = query.casefold()
            for lesson_id in sorted(state.get("lessons", {})):
                lesson = state["lessons"][lesson_id]
                haystack = " ".join(
                    str(lesson.get(key, ""))
                    for key in ("id", "statement", "limits", "status", "scope", "validation")
                ).casefold()
                if needle in haystack:
                    matches.append({
                        "id": lesson_id,
                        "statement": lesson.get("statement"),
                        "limits": lesson.get("limits"),
                        "status": lesson.get("status"),
                        "scope": lesson.get("scope"),
                        "validation": lesson.get("validation"),
                    })
                    if len(matches) >= limit:
                        break

        return {
            "status": "VALID",
            "event_count": count,
            "head": head,
            "focus": focus if focus is not None else "NO_ACTIVE_FOCUS",
            "lesson_query": query,
            "lesson_matches": matches,
        }

    def search_lessons(self, query: str, limit: int = 20) -> dict[str, Any]:
        """Search verified lesson records using deterministic case-insensitive text matching."""
        if not isinstance(query, str) or not query.strip():
            raise BrainReadError("query must be nonempty text")
        if type(limit) is not int or not 1 <= limit <= 100:
            raise BrainReadError("limit must be an integer from 1 to 100")

        state, count, head = self._verified()
        needle = query.casefold()
        matches = []
        for lesson_id in sorted(state.get("lessons", {})):
            lesson = state["lessons"][lesson_id]
            haystack = " ".join(
                str(lesson.get(key, ""))
                for key in ("id", "statement", "limits", "status", "scope", "validation")
            ).casefold()
            if needle in haystack:
                matches.append({
                    "id": lesson_id,
                    "statement": lesson.get("statement"),
                    "limits": lesson.get("limits"),
                    "status": lesson.get("status"),
                    "scope": lesson.get("scope"),
                    "validation": lesson.get("validation"),
                })
                if len(matches) >= limit:
                    break

        return {
            "status": "VALID",
            "event_count": count,
            "head": head,
            "query": query,
            "matches": matches,
        }
