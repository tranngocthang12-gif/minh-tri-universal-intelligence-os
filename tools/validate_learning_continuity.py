"""Validate unaccepted learning registry; not an active-route or Owner receipt."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from minhtri.learning_continuity import (
    LearningContinuityError, read_json, validate_registry,
    validate_canonical_learning_route,
)

def main():
    try:
        index = validate_registry(read_json(ROOT / "state" / "learning_tracks.json"))
    except LearningContinuityError as exc:
        print("LEARNING_CONTINUITY_CANDIDATE_FAIL:", exc)
        return 1
    print("LEARNING_CONTINUITY_CANDIDATE_SCHEMA_PASS:", ",".join(sorted(index)))
    for track_id in sorted(index):
        try:
            task_id = validate_canonical_learning_route(ROOT, track_id)
        except LearningContinuityError as exc:
            print(f"LEARNING_ACTIVE_ROUTE_BLOCKED: {track_id}: {exc}")
            return 2
        print(f"LEARNING_ACTIVE_ROUTE_MATCHED_NOT_ACCEPTED: {track_id}: {task_id}")
    print("NOT proof of write authorization, knowledge correctness or Owner acceptance")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
