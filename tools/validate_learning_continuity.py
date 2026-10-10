"""Validate unaccepted learning registry; not an active-route or Owner receipt."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from minhtri.learning_continuity import LearningContinuityError, read_json, validate_registry

def main():
    try:
        index = validate_registry(read_json(ROOT / "state" / "learning_tracks.json"))
    except LearningContinuityError as exc:
        print("LEARNING_CONTINUITY_CANDIDATE_FAIL:", exc)
        return 1
    print("LEARNING_CONTINUITY_CANDIDATE_SCHEMA_PASS:", ",".join(sorted(index)))
    print("Not a canonical active-route proof, application result or Owner acceptance")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
