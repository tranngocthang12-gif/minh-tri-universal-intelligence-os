"""Local-only process supervisor for the secure read-only runtime plane.

This module is intentionally not exposed through MCP. It executes a fixed argv without
a shell, inherits secrets from the Owner-PC environment instead of persisting them, and
restarts a failed child with bounded exponential backoff.

It proves a supervision mechanism exists; actual tunnel persistence remains UNPROVEN
until deployed and observed on the Owner PC.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, Sequence

MIN_BACKOFF_SECONDS = 1.0
MAX_BACKOFF_SECONDS = 60.0


class SupervisorError(ValueError):
    pass


@dataclass
class SupervisorEvent:
    event: str
    restart_count: int
    returncode: int | None = None

    def as_dict(self) -> dict:
        return {
            "event": self.event,
            "restart_count": self.restart_count,
            "returncode": self.returncode,
        }


class ProcessSupervisor:
    """Supervise one fixed local process without shell expansion."""

    def __init__(
        self,
        argv: Sequence[str],
        *,
        min_backoff: float = MIN_BACKOFF_SECONDS,
        max_backoff: float = MAX_BACKOFF_SECONDS,
        sleep: Callable[[float], None] = time.sleep,
        popen_factory: Callable[..., subprocess.Popen] = subprocess.Popen,
        event_sink: Callable[[dict], None] | None = None,
    ):
        if not argv or not all(isinstance(x, str) and x for x in argv):
            raise SupervisorError("argv must be a non-empty sequence of strings")
        if min_backoff < 0 or max_backoff < min_backoff:
            raise SupervisorError("invalid backoff")
        self.argv = tuple(argv)
        self.min_backoff = float(min_backoff)
        self.max_backoff = float(max_backoff)
        self.sleep = sleep
        self.popen_factory = popen_factory
        self.event_sink = event_sink or (lambda event: None)

    def _emit(self, event: SupervisorEvent) -> None:
        self.event_sink(event.as_dict())

    def run(self, *, max_restarts: int | None = None) -> int:
        if max_restarts is not None and max_restarts < 0:
            raise SupervisorError("max_restarts cannot be negative")
        restarts = 0
        backoff = self.min_backoff

        while True:
            self._emit(SupervisorEvent("STARTING", restarts))
            process = self.popen_factory(
                list(self.argv),
                shell=False,
                stdin=None,
                stdout=None,
                stderr=None,
            )
            returncode = process.wait()
            self._emit(SupervisorEvent("EXITED", restarts, returncode))

            if returncode == 0:
                return 0
            if max_restarts is not None and restarts >= max_restarts:
                self._emit(SupervisorEvent("RESTART_LIMIT_REACHED", restarts, returncode))
                return returncode

            restarts += 1
            self._emit(SupervisorEvent("RESTARTING", restarts, returncode))
            self.sleep(backoff)
            backoff = min(self.max_backoff, max(self.min_backoff, backoff * 2 or 1.0))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="minhtri-runtime-supervisor",
        description=(
            "Local-only watchdog for the secure brain runtime. "
            "Secrets must come from the Owner-PC environment."
        ),
    )
    parser.add_argument("--max-restarts", type=int)
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Executable and arguments after --; no shell is used.",
    )
    args = parser.parse_args(argv)
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise SystemExit("missing supervised command")

    def emit(event: dict) -> None:
        print(json.dumps(event, sort_keys=True), flush=True)

    supervisor = ProcessSupervisor(command, event_sink=emit)
    return supervisor.run(max_restarts=args.max_restarts)


if __name__ == "__main__":
    raise SystemExit(main())
