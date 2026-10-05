from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_packet(root: Path = ROOT) -> dict:
    questions = load_json(root / "eval" / "retrieval" / "v1" / "questions.json")
    decoys = load_json(root / "eval" / "retrieval" / "v1" / "decoys.json")
    index = load_json(root / "knowledge" / "index.json")
    return {
        "schema": "minhtri-retrieval-eval-packet/v1",
        "set_id": questions["set_id"],
        "questions": questions["items"],
        "instructions": questions["instructions"],
        "knowledge_snapshot": {
            "atoms": index["atoms"],
            "hubs": index["hubs"],
        },
        "decoys": decoys["records"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.write_text(json.dumps(build_packet(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
