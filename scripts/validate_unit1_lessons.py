"""Validate authored Unit 1 lesson packages and media-text invariants."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "units/unit-01-first-connections"
CONTRACT = UNIT / "lesson-package-contract.json"
MANIFEST = UNIT / "unit-manifest.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def package_errors(lesson: dict, required: list[str]) -> list[str]:
    lesson_id = lesson["lesson_id"]
    if lesson_id == "U1-L01":
        return []
    folder = UNIT / "lessons" / lesson_id.lower()
    errors = [f"{lesson_id} missing {name}" for name in required if not (folder / name).is_file()]
    if errors:
        return errors
    manifest = load(folder / "lesson-manifest.json")
    packet = load(folder / "source-packet.json")
    activities = load(folder / "activities.json")
    assessment = load(folder / "assessment.json")
    if manifest["candidate_id"] != lesson["candidate_id"] or packet["candidate_id"] != lesson["candidate_id"]:
        errors.append(f"{lesson_id} candidate traceability mismatch")
    if packet["candidate_status"] != "approved_candidate":
        errors.append(f"{lesson_id} source candidate is not approved")
    if manifest["video"]["speaker_count"] != 1 or manifest["video"]["interaction_during_video"]:
        errors.append(f"{lesson_id} video delivery contract mismatch")
    if activities["delivery"]["placement"] != "after_video_explanation":
        errors.append(f"{lesson_id} activities do not start after video")
    if assessment["decision"]["completion_is_mastery"]:
        errors.append(f"{lesson_id} completion incorrectly grants mastery")
    transcript = (folder / "video/transcript.txt").read_text(encoding="utf-8")
    if "Speaker 2:" in transcript or not transcript.startswith("Speaker 1:"):
        errors.append(f"{lesson_id} transcript is not single-teacher")
    for line_number, line in enumerate(transcript.splitlines(), 1):
        if not line.strip():
            continue
        if not line.startswith("Speaker 1:"):
            errors.append(f"{lesson_id} line {line_number} lacks Speaker 1 label")
            continue
        stripped = re.sub(r"<lang.*?</lang>", "", line)
        stripped = re.sub(r"^Speaker 1:\s*", "", stripped)
        stripped = re.sub(r"\[[^]]+\]", "", stripped)
        if re.search(r"[A-Za-z]", stripped):
            errors.append(f"{lesson_id} line {line_number} has unwrapped spoken English")
        fragments = re.findall(r"<lang.*?</lang>", line)
        for fragment in fragments:
            try:
                ET.fromstring(fragment)
            except ET.ParseError:
                errors.append(f"{lesson_id} line {line_number} has invalid SSML XML")
        if re.search(r"\b(?:شخصًا|موضوعًا)\b", line):
            errors.append(f"{lesson_id} line {line_number} uses artificial conversational tanween")
    return errors


def validation_errors(require_complete: bool = False) -> list[str]:
    contract = load(CONTRACT)
    unit = load(MANIFEST)
    errors: list[str] = []
    for lesson in unit["lessons"]:
        folder = UNIT / "lessons" / lesson["lesson_id"].lower()
        if lesson["lesson_id"] != "U1-L01" and not folder.is_dir():
            if require_complete:
                errors.append(f"{lesson['lesson_id']} package directory is missing")
            continue
        if lesson["lesson_id"] != "U1-L01" and not require_complete and not (folder / "lesson-manifest.json").is_file():
            packet_path = folder / "source-packet.json"
            if not packet_path.is_file() or load(packet_path).get("candidate_id") != lesson["candidate_id"]:
                errors.append(f"{lesson['lesson_id']} source-only scaffold is invalid")
            continue
        errors.extend(package_errors(lesson, contract["required_files"]))
    return errors


def main() -> int:
    errors = validation_errors(require_complete=True)
    if errors:
        print("FAIL Unit 1 lesson packages")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS Unit 1 lesson packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
