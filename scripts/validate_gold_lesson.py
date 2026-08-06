"""Validate the gold-lesson specification and lightweight prototype contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "gold/introduce-yourself"
PROTOTYPE = ROOT / "prototype/gold-lesson"
JSON_FILES = {
    name: GOLD / name
    for name in (
        "lesson-manifest.json", "content.json", "activities.json",
        "ai-contract.json", "assessment.json", "source-packet.json",
    )
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors() -> list[str]:
    errors: list[str] = []
    for name, path in JSON_FILES.items():
        if not path.is_file():
            errors.append(f"missing {name}")
    if errors:
        return errors
    files = {name: load(path) for name, path in JSON_FILES.items()}
    manifest = files["lesson-manifest.json"]
    packet = files["source-packet.json"]
    candidate = packet["candidate"]
    expected_id = manifest["candidate_id"]
    if packet["selected_candidate_id"] != expected_id or candidate["candidate_id"] != expected_id:
        errors.append("manifest and source packet select different candidates")
    if candidate["status"] != "approved_candidate":
        errors.append("gold lesson candidate is not approved")
    source_ids = {item["record_id"] for item in packet["source_records"]}
    ref_ids = {item["record_id"] for item in candidate["evidence_refs"]}
    if source_ids != ref_ids or len(source_ids) != 6:
        errors.append("source packet does not exactly preserve six candidate records")
    for record in packet["source_records"]:
        if record["source"]["source_text_sha256"] not in {
            ref["source_text_sha256"] for ref in candidate["evidence_refs"]
        }:
            errors.append(f"source hash mismatch for {record['record_id']}")
    expected_sections = {
        "video_explanation", "applied_questions", "guided_practice", "personal_plan",
        "ai_practice", "fresh_mastery", "teach_back_variant", "review",
    }
    if set(manifest["section_order"]) != expected_sections:
        errors.append("manifest does not cover the complete learning loop")
    video = manifest.get("video", {})
    if video.get("speaker_count") != 1 or video.get("interaction_during_video") is not False:
        errors.append("video must use one teacher and defer interaction")
    activities = files["activities.json"]["activities"]
    activity_ids = [item["id"] for item in activities]
    if len(activities) < 6 or len(activity_ids) != len(set(activity_ids)):
        errors.append("activities are missing or repeat ids")
    assessment = files["assessment.json"]
    if set(assessment["mastery_task"]["required"]) != set(manifest["scope"]["required_details"]):
        errors.append("mastery task and lesson scope require different details")
    if assessment["teach_back_variant"]["cannot_rescue_failed_mastery"] is not True:
        errors.append("teach-back may incorrectly rescue failed mastery")
    if files["ai-contract.json"]["turn_limit"] > 6:
        errors.append("AI practice exceeds the bounded turn limit")
    errors.extend(_prototype_errors())
    return errors


def _prototype_errors() -> list[str]:
    required = [
        "index.html", "README.md", "styles/foundation.css", "styles/lesson.css",
        "scripts/data.js", "scripts/checks.js", "scripts/views.js", "scripts/app.js",
    ]
    errors = [f"prototype missing {name}" for name in required if not (PROTOTYPE / name).is_file()]
    if errors:
        return errors
    index = (PROTOTYPE / "index.html").read_text(encoding="utf-8")
    for name in ("data.js", "checks.js", "views.js", "app.js"):
        if name not in index:
            errors.append(f"prototype does not load {name}")
    if "http://" in index or "https://" in index:
        errors.append("prototype unexpectedly depends on the network")
    for path in PROTOTYPE.rglob("*"):
        if path.is_file() and len(path.read_text(encoding="utf-8").splitlines()) > 200:
            errors.append(f"prototype file exceeds 200 lines: {path.name}")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("FAIL gold lesson")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS gold lesson and prototype contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
