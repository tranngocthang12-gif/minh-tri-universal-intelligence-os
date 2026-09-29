"""Four-seat AI workcell coordination for MINH TRI.

This ledger preserves the Owner's original requirement that four real AI
participants contribute on the same frozen task while keeping model/provider
identity replaceable. It is SHADOW-only and grants no external authority.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .arena import ArenaService
from .core import GateError, Ledger, digest, identifier, need, ref, string


SEATS = ("S1", "S2", "S3", "S4")

WORKCELL_FIELDS = {
    "open_session": {
        "id", "arena_task_id", "task_fingerprint", "brain_revision", "brain_fingerprint",
        "architecture_law_sha256", "bootstrap_sha256",
    },
    "assign_slot": {"session_id", "seat_id", "participant_id", "family_id", "model", "version"},
    "replace_slot": {
        "session_id", "seat_id", "old_participant_id", "participant_id", "family_id",
        "model", "version", "reason",
    },
    "submit_blind": {
        "session_id", "seat_id", "participant_id", "contribution_ref", "contribution_sha256",
    },
    "freeze_blind": {"session_id"},
    "reveal": {"session_id"},
}


def initial_workcell_state() -> dict:
    return {"format_version": 1, "phase": "SHADOW", "sessions": {}}


def _hex(value: Any, length: int, label: str) -> str:
    if not isinstance(value, str) or len(value) != length or any(c not in "0123456789abcdef" for c in value):
        raise GateError(f"{label} must be a {length}-character lowercase hex digest")
    return value


def _session(state: dict, session_id: str) -> dict:
    return ref(state, "sessions", session_id)


def _seat(value: Any) -> str:
    if value not in SEATS:
        raise GateError("seat_id must be one of S1, S2, S3, S4")
    return value


def _slot_families(session: dict, exclude_seat: str | None = None) -> set[str]:
    return {
        slot["family_id"]
        for seat, slot in session["slots"].items()
        if slot is not None and seat != exclude_seat
    }


def _assigned_participants(session: dict, exclude_seat: str | None = None) -> set[str]:
    return {
        slot["participant_id"]
        for seat, slot in session["slots"].items()
        if slot is not None and seat != exclude_seat
    }


def workcell_evolve(state: dict, command: dict, at: str) -> dict:
    if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
        raise GateError("Command must contain exactly type and data object")
    kind, d = command["type"], copy.deepcopy(command["data"])
    if kind not in WORKCELL_FIELDS:
        raise GateError(f"Unknown workcell command: {kind}")
    extra = set(d) - WORKCELL_FIELDS[kind]
    if extra:
        raise GateError("Unexpected workcell fields: " + ", ".join(sorted(extra)))
    out = copy.deepcopy(state)
    if out["phase"] != "SHADOW":
        raise GateError("Only SHADOW workcell mode is implemented")

    if kind == "open_session":
        need(d, *WORKCELL_FIELDS[kind])
        session_id = identifier(d["id"], "workcell session ID")
        if session_id in out["sessions"]:
            raise GateError(f"Duplicate workcell session ID: {session_id}")
        identifier(d["arena_task_id"], "arena_task_id")
        _hex(d["task_fingerprint"], 64, "task_fingerprint")
        _hex(d["brain_revision"], 40, "brain_revision")
        for key in ("brain_fingerprint", "architecture_law_sha256", "bootstrap_sha256"):
            _hex(d[key], 64, key)
        d["slots"] = {seat: None for seat in SEATS}
        d["blind_contributions"] = {}
        d["replacement_history"] = []
        d["round_state"] = "BLIND_OPEN"
        d["opened_at"] = at
        out["sessions"][session_id] = d

    elif kind == "assign_slot":
        need(d, *WORKCELL_FIELDS[kind])
        session = _session(out, d["session_id"])
        if session["round_state"] != "BLIND_OPEN":
            raise GateError("Initial slot assignment is allowed only before blind freeze")
        seat = _seat(d["seat_id"])
        if session["slots"][seat] is not None:
            raise GateError("Workcell seat is already occupied")
        participant = identifier(d["participant_id"], "participant_id")
        family = identifier(d["family_id"], "family_id")
        if participant in _assigned_participants(session):
            raise GateError("One participant cannot occupy multiple workcell seats")
        if family in _slot_families(session):
            raise GateError("One provider family cannot occupy multiple independent workcell seats")
        model = string(d["model"], "model")
        version = string(d["version"], "version")
        session["slots"][seat] = {
            "participant_id": participant,
            "family_id": family,
            "model": model,
            "version": version,
            "assigned_at": at,
        }

    elif kind == "replace_slot":
        need(d, *WORKCELL_FIELDS[kind])
        session = _session(out, d["session_id"])
        seat = _seat(d["seat_id"])
        current = session["slots"][seat]
        if current is None or current["participant_id"] != d["old_participant_id"]:
            raise GateError("Replacement must name the current seat occupant")
        participant = identifier(d["participant_id"], "participant_id")
        family = identifier(d["family_id"], "family_id")
        if participant in _assigned_participants(session, seat):
            raise GateError("Replacement participant already occupies another seat")
        if family in _slot_families(session, seat):
            raise GateError("Replacement provider family already occupies another seat")
        reason = string(d["reason"], "reason")
        replacement = {
            "participant_id": participant,
            "family_id": family,
            "model": string(d["model"], "model"),
            "version": string(d["version"], "version"),
            "assigned_at": at,
        }
        session["replacement_history"].append({
            "seat_id": seat,
            "from": copy.deepcopy(current),
            "to": copy.deepcopy(replacement),
            "reason": reason,
            "round_state": session["round_state"],
            "at": at,
        })
        session["slots"][seat] = replacement
        if session["round_state"] == "BLIND_OPEN":
            session["blind_contributions"].pop(seat, None)
        else:
            replacement["joined_after_reveal"] = True

    elif kind == "submit_blind":
        need(d, *WORKCELL_FIELDS[kind])
        session = _session(out, d["session_id"])
        if session["round_state"] != "BLIND_OPEN":
            raise GateError("Blind contribution round is already frozen")
        seat = _seat(d["seat_id"])
        slot = session["slots"][seat]
        if slot is None or slot["participant_id"] != d["participant_id"]:
            raise GateError("Blind contribution must come from the current seat occupant")
        if seat in session["blind_contributions"]:
            raise GateError("Seat already has a frozen blind contribution")
        contribution_ref = string(d["contribution_ref"], "contribution_ref")
        contribution_hash = _hex(d["contribution_sha256"], 64, "contribution_sha256")
        session["blind_contributions"][seat] = {
            "participant_id": d["participant_id"],
            "family_id": slot["family_id"],
            "contribution_ref": contribution_ref,
            "contribution_sha256": contribution_hash,
            "submitted_at": at,
        }

    elif kind == "freeze_blind":
        need(d, *WORKCELL_FIELDS[kind])
        session = _session(out, d["session_id"])
        if session["round_state"] != "BLIND_OPEN":
            raise GateError("Blind round is not open")
        if any(session["slots"][seat] is None for seat in SEATS):
            raise GateError("Four occupied independent seats are required before blind freeze")
        if set(session["blind_contributions"]) != set(SEATS):
            raise GateError("Four blind contributions are required before blind freeze")
        families = {session["slots"][seat]["family_id"] for seat in SEATS}
        if len(families) != 4:
            raise GateError("Four distinct provider families are required for independent blind freeze")
        body = {
            "session_id": session["id"],
            "task_fingerprint": session["task_fingerprint"],
            "slots": session["slots"],
            "blind_contributions": session["blind_contributions"],
        }
        session["blind_round_fingerprint"] = digest(body)
        session["round_state"] = "BLIND_FROZEN"
        session["blind_frozen_at"] = at

    elif kind == "reveal":
        need(d, *WORKCELL_FIELDS[kind])
        session = _session(out, d["session_id"])
        if session["round_state"] != "BLIND_FROZEN":
            raise GateError("Reveal requires a four-of-four frozen blind round")
        session["round_state"] = "REVEALED"
        session["revealed_at"] = at

    return out


class FourSeatWorkcellService:
    """Binds four-seat coordination to the current Arena task and participant receipts."""

    def __init__(self, core_home: str | Path, brain_root: str | Path = ".", brain_revision: str | None = None):
        self.arena = ArenaService(core_home, brain_root, brain_revision)
        self.ledger = Ledger(Path(core_home) / "workcell", reducer=workcell_evolve, initial=initial_workcell_state)

    def init(self) -> None:
        self.arena.ledger.verify()
        self.ledger.init()

    def _arena_state(self) -> dict:
        return self.arena.ledger.verify()[0]

    def _participant_acknowledged(self, arena_state: dict, task: dict, participant_id: str) -> None:
        participant = ref(arena_state, "participants", participant_id)
        valid = [
            ack for ack in arena_state["acknowledgements"].values()
            if ack["task_id"] == task["id"]
            and ack["participant_id"] == participant_id
            and ack["task_fingerprint"] == task["fingerprint"]
        ]
        if not valid:
            raise GateError("Workcell participant must acknowledge the exact Arena Brain/Task packet first")
        if valid[-1]["brain_revision"] != task["brain_revision"] or valid[-1]["brain_fingerprint"] != task["brain_fingerprint"]:
            raise GateError("Workcell participant acknowledgement is stale")
        return participant

    def apply(self, command: dict) -> dict:
        if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
            raise GateError("Command must contain exactly type and data object")
        command = copy.deepcopy(command)
        kind, d = command["type"], command["data"]
        arena_state = self._arena_state()

        if kind == "open_session":
            if set(d) != {"id", "arena_task_id"}:
                raise GateError("open_session input has unexpected fields")
            packet = self.arena.task_packet(d["arena_task_id"])
            task = packet["task"]
            d.update({
                "task_fingerprint": task["fingerprint"],
                "brain_revision": task["brain_revision"],
                "brain_fingerprint": task["brain_fingerprint"],
                "architecture_law_sha256": task["architecture_law_sha256"],
                "bootstrap_sha256": task["bootstrap_sha256"],
            })
        elif kind in ("assign_slot", "replace_slot"):
            state = self.ledger.verify()[0]
            session = ref(state, "sessions", d.get("session_id"))
            task = ref(arena_state, "tasks", session["arena_task_id"])
            participant = self._participant_acknowledged(arena_state, task, d.get("participant_id"))
            if d.get("family_id") != participant["family_id"]:
                raise GateError("Workcell family_id must match the registered Arena participant family")
            if d.get("model") != participant["model"] or d.get("version") != participant["version"]:
                raise GateError("Workcell model/version must match the registered Arena participant")
        elif kind in ("submit_blind", "freeze_blind", "reveal"):
            state = self.ledger.verify()[0]
            session = ref(state, "sessions", d.get("session_id"))
            self.arena.task_packet(session["arena_task_id"])

        return self.ledger.apply(command)

    def status(self, session_id: str) -> dict:
        state, count, head = self.ledger.verify()
        session = ref(state, "sessions", session_id)
        return {
            "event_count": count,
            "head": head,
            "session_id": session_id,
            "round_state": session["round_state"],
            "occupied_seats": sum(1 for seat in SEATS if session["slots"][seat] is not None),
            "blind_contributions": len(session["blind_contributions"]),
            "blind_round_fingerprint": session.get("blind_round_fingerprint"),
        }

    def packet(self, session_id: str) -> dict:
        state, _, _ = self.ledger.verify()
        session = copy.deepcopy(ref(state, "sessions", session_id))
        arena_packet = self.arena.task_packet(session["arena_task_id"])
        return {"session": session, "arena_task_packet": arena_packet}
