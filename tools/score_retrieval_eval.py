from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def score(gold, response):
    by_qid = {x["qid"]: x for x in response["answers"]}
    results = []
    passed = 0

    for expected in gold["answers"]:
        qid = expected["qid"]
        actual = by_qid.get(qid)
        ok = True
        reasons = []

        if actual is None:
            ok = False
            reasons.append("missing answer")
        else:
            if actual.get("answer_status") != expected["expected_status"]:
                ok = False
                reasons.append("wrong answer_status")

            used = set(actual.get("record_ids", []))
            required = set(expected["expected_record_ids"])
            forbidden = set(expected["forbidden_record_ids"])

            if not required.issubset(used):
                ok = False
                reasons.append("missing required record")
            if used & forbidden:
                ok = False
                reasons.append("used forbidden decoy")

        if ok:
            passed += 1
        results.append({"qid": qid, "pass": ok, "reasons": reasons})

    total = len(gold["answers"])
    return {
        "schema": "minhtri-retrieval-eval-score/v1",
        "passed": passed,
        "total": total,
        "pass_rate": passed / total if total else 0,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True)
    parser.add_argument("--response", required=True)
    args = parser.parse_args()
    print(json.dumps(score(load(args.gold), load(args.response)), indent=2))


if __name__ == "__main__":
    main()
