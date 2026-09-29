"""One-command offline demonstration of four simulated AI Commons participants."""

import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.arena import ArenaService
from minhtri.core import Ledger


def command(command_type, **data):
    return {"type": command_type, "data": data}


def main():
    project = Path(__file__).resolve().parent
    home = Path(tempfile.mkdtemp(prefix="minhtri-arena-")) / "brain"
    core = Ledger(home)
    core.init()
    for name in ("01-domain-youtube", "02-goal-youtube"):
        core.apply(json.loads((project / "examples" / f"{name}.json").read_text(encoding="utf-8")))

    arena = ArenaService(home, project)
    arena.init()
    for n in range(1, 5):
        arena.apply(command("register_participant", id=f"simulated{n}", family_id=f"testfamily{n}",
                            model=f"offline-example-{n}", version="demo", adapter="MANUAL",
                            capabilities=["PROPOSE", "CRITIQUE", "ADJUDICATE"]))

    goal_id = "youtube-pilot"
    task = arena.apply(command(
        "open_task", id="sample_task", goal_id=goal_id,
        brief="Compare two hypothetical ways to measure a content experiment",
        acceptance="State a falsifiable claim and independent criticism",
        allowed_evidence_ids=[],
        expires_at=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    ))["state"]["tasks"]["sample_task"]
    fingerprint = task["fingerprint"]
    arena.apply(command("submit_proposal", id="proposal1", task_id="sample_task",
                        participant_id="simulated1", task_fingerprint=fingerprint,
                        claim="Compare the two measurements on the same synthetic cohort",
                        alternative="Use separate cohorts", uncertainties=["No real outcome was measured"],
                        evidence_ids=[], discriminating_test="Predefine and compare error on held-out data",
                        method_ref="offline-demo-v1"))
    for n, verdict in ((2, "NO_MATERIAL_DEFECT_FOUND"), (3, "CHALLENGE")):
        arena.apply(command("submit_critique", id=f"critique{n}", proposal_id="proposal1",
                            participant_id=f"simulated{n}", task_fingerprint=fingerprint,
                            verdict=verdict, reason="The synthetic example cannot settle the real-world outcome",
                            evidence_ids=[], test="Run a preregistered read-only pilot"))
    receipt = arena.apply(command("submit_adjudication", id="decision1", proposal_id="proposal1",
                                  participant_id="simulated4", task_fingerprint=fingerprint,
                                  critique_ids=["critique2", "critique3"], outcome="HOLD",
                                  reason="An open challenge requires a real, independent test"))
    arena.ledger.verify()
    print(json.dumps({"phase": receipt["state"]["phase"], "participants": 4,
                      "brain_revision": task["brain_revision"],
                      "brain_fingerprint": task["brain_fingerprint"],
                      "runtime_state_head": task["runtime_state_head"],
                      "task_fingerprint": fingerprint,
                      "adjudication": receipt["state"]["adjudications"]["decision1"]["outcome"],
                      "canonical_lessons": len(core.verify()[0]["lessons"]),
                      "demo_home": str(home)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
