import json
from pathlib import Path
from tools.score_master_blueprint_recovery_v7 import score_response

ROOT = Path(__file__).resolve().parents[1]

def test_c7_attempt_deterministic_grade():
    response = json.loads((ROOT / "eval/recovery/v7/attempts/C7_response.json").read_text(encoding="utf-8"))
    result = score_response(response)
    assert result["status"] == "PASS", json.dumps(result, ensure_ascii=False, sort_keys=True)
