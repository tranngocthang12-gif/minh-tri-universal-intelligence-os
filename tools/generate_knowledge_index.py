from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
META_RE = re.compile(r"<!-- MINHTRI_META\n(.*?)\nMINHTRI_META -->", re.S)


def build_index(root: Path = ROOT) -> dict:
    knowledge = root / "knowledge"
    atoms = []
    hubs = []

    for path in sorted(knowledge.glob("**/atoms/*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        atoms.append(
            {
                "id": record["id"],
                "domain": record["domain"],
                "record_type": record["record_type"],
                "class": record["class"],
                "status": record["status"],
                "path": path.relative_to(root).as_posix(),
                "statement": record["statement"],
            }
        )

    for path in sorted(knowledge.glob("**/concepts/*.md")):
        text = path.read_text(encoding="utf-8")
        match = META_RE.search(text)
        if not match:
            raise ValueError(f"Missing MINHTRI_META block: {path}")
        meta = json.loads(match.group(1))
        hubs.append(
            {
                "id": meta["id"],
                "domain": meta["domain"],
                "hub_type": meta["hub_type"],
                "status": meta["status"],
                "aliases": meta["aliases"],
                "depends_on_claims": meta["depends_on_claims"],
                "path": path.relative_to(root).as_posix(),
            }
        )

    return {
        "schema": "minhtri-knowledge-index/v1",
        "generated_from": {
            "atom_glob": "knowledge/**/atoms/*.json",
            "hub_glob": "knowledge/**/concepts/*.md",
        },
        "atoms": atoms,
        "hubs": hubs,
    }


def render_index(root: Path = ROOT) -> str:
    return json.dumps(build_index(root), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    target = KNOWLEDGE / "index.json"
    target.write_text(render_index(ROOT), encoding="utf-8")
    print(target)
