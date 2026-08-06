"""Assemble the immutable source packet for the selected gold lesson."""

from __future__ import annotations

import copy
import json
from pathlib import Path

try:
    from scripts.lesson_map_io import DEFAULT_MAP_PATH, SOURCE_PATHS, load
except ModuleNotFoundError:
    from lesson_map_io import DEFAULT_MAP_PATH, SOURCE_PATHS, load


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "gold/introduce-yourself/source-packet.json"
CANDIDATE_ID = "lesson_candidate.give_short_self_introduction"


def build_packet() -> dict:
    lesson_map = load(DEFAULT_MAP_PATH)
    if lesson_map["status"] != "approved":
        raise ValueError("gold lesson selection requires an approved lesson map")
    candidates = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    candidate = copy.deepcopy(candidates[CANDIDATE_ID])
    records = {
        record["record_id"]: record
        for path in SOURCE_PATHS
        for record in load(path)["records"]
    }
    source_records = [
        copy.deepcopy(records[ref["record_id"]]) for ref in candidate["evidence_refs"]
    ]
    return {
        "schema_version": 1,
        "packet_id": "gold_lesson.introduce_yourself.sources.v1",
        "selected_candidate_id": CANDIDATE_ID,
        "lesson_map_id": lesson_map["map_id"],
        "lesson_map_version": lesson_map["version"],
        "selection_status": "selected",
        "candidate": candidate,
        "source_records": source_records,
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(build_packet(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {OUTPUT}")


if __name__ == "__main__":
    main()
