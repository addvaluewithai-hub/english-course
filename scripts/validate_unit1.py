"""Validate the first-unit blueprint against the approved A1 lesson map."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "units/unit-01-first-connections"
MANIFEST = UNIT / "unit-manifest.json"
MASTERY = UNIT / "unit-mastery.json"
LESSON_MAP = ROOT / "data/reviewed/a1-lesson-map.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors() -> list[str]:
    errors: list[str] = []
    for path in (MANIFEST, MASTERY, LESSON_MAP):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        return errors

    manifest = load(MANIFEST)
    mastery = load(MASTERY)
    lesson_map = load(LESSON_MAP)
    approved = {
        item["candidate_id"]: item
        for item in lesson_map["candidates"]
        if item["status"] == "approved_candidate"
    }
    lessons = manifest["lessons"]
    ids = [item["lesson_id"] for item in lessons]
    candidates = [item["candidate_id"] for item in lessons]

    if manifest["lesson_count"] != len(lessons) or len(lessons) != 8:
        errors.append("unit must declare exactly its eight selected lessons")
    if len(ids) != len(set(ids)) or len(candidates) != len(set(candidates)):
        errors.append("unit repeats a lesson or candidate id")
    for candidate_id in candidates:
        candidate = approved.get(candidate_id)
        if not candidate:
            errors.append(f"candidate is not approved: {candidate_id}")
        elif "identity_personal_information" not in candidate["candidate_cluster_ids"]:
            errors.append(f"candidate is outside the identity cluster: {candidate_id}")

    covered_skills = {
        skill for candidate_id in candidates for skill in approved[candidate_id]["skill_codes"]
    }
    if covered_skills != {"listening", "reading", "speaking", "writing"}:
        errors.append("unit does not cover all four core skills")
    if not (ROOT / lessons[0]["content_path"]).is_dir():
        errors.append("gold reference path is missing")
    for lesson in lessons:
        content_path = lesson.get("content_path")
        if lesson.get("status") not in {"gold_reference_ready", "content_ready"}:
            errors.append(f"lesson is not content ready: {lesson['lesson_id']}")
        if not content_path or not (ROOT / content_path).is_dir():
            errors.append(f"lesson content path is missing: {lesson['lesson_id']}")
    if len(mastery["stations"]) != 3 or not mastery["passing_rule"]["require_all_stations"]:
        errors.append("unit mastery must retain all three fresh evidence stations")
    if mastery["passing_rule"]["completion_is_mastery"]:
        errors.append("unit completion incorrectly grants mastery")
    for name in ("unit-mastery-experience.json", "unit-review.json", "unit-accessibility.json"):
        if not (UNIT / name).is_file():
            errors.append(f"unit support file is missing: {name}")
    if not errors:
        experience = load(UNIT / "unit-mastery-experience.json")
        station_ids = {item["id"] for item in experience["stations"]}
        if station_ids != {"spoken_contact", "contact_capture", "written_follow_up"}:
            errors.append("unit mastery experience does not implement the three stations")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("FAIL Unit 1 blueprint")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS Unit 1 blueprint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
