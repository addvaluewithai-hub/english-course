"""Create immutable lesson source packets for Unit 1 from the approved lesson map."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "units/unit-01-first-connections"
MANIFEST = UNIT / "unit-manifest.json"
LESSON_MAP = ROOT / "data/reviewed/a1-lesson-map.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_packet(lesson: dict, candidate: dict) -> dict:
    return {
        "schema_version": 1,
        "unit_id": "a1.unit01.first_connections.v0",
        "lesson_id": lesson["lesson_id"],
        "candidate_id": lesson["candidate_id"],
        "source_map": "data/reviewed/a1-lesson-map.json",
        "candidate_version": candidate["version"],
        "candidate_status": candidate["status"],
        "outcome": candidate["outcome"],
        "evidence_refs": candidate["evidence_refs"],
        "skill_codes": candidate["skill_codes"],
        "mode_codes": candidate["mode_codes"],
        "relationships": candidate["relationships"],
        "language_targets": candidate["language_targets"],
        "error_hypotheses": candidate["error_hypotheses"],
        "mastery": candidate["mastery"],
        "scope": candidate["scope"],
        "risks": candidate["risks"],
        "review": candidate["review"],
    }


def main() -> int:
    manifest = load(MANIFEST)
    lesson_map = load(LESSON_MAP)
    candidates = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    created = 0
    for lesson in manifest["lessons"]:
        if lesson["lesson_id"] == "U1-L01":
            continue
        candidate = candidates[lesson["candidate_id"]]
        if candidate["status"] != "approved_candidate":
            raise ValueError(f"candidate is not approved: {lesson['candidate_id']}")
        target = UNIT / "lessons" / lesson["lesson_id"].lower() / "source-packet.json"
        write(target, build_packet(lesson, candidate))
        created += 1
    print(f"Created {created} Unit 1 source packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
