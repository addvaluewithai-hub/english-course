"""Reusable contract checks for the migrated A1 v1 gold lesson."""

import json
import re

from scripts.gold_v1_contract import (
    CANDIDATE_ID, LESSON_ID, OUTPUT, QA_OUTPUT, QA_REPORT,
    REQUIRED_INTRODUCTIONS, REQUIRED_RECYCLES, ROOT, UNIT_ID,
)
from scripts.gold_v1_qa_report import build_qa, render
from scripts.migrate_gold_to_a1_v1 import build_outputs
from scripts.source_disposition_inputs import file_sha256


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _determinism_errors() -> list[str]:
    errors: list[str] = []
    expected = build_outputs()
    actual_files = {
        path.relative_to(OUTPUT).as_posix() for path in OUTPUT.rglob("*") if path.is_file()
    }
    if actual_files != set(expected):
        errors.append("package file set differs from the 12 generated contract files")
    for relative, value in expected.items():
        path = OUTPUT / relative
        if not path.is_file():
            continue
        actual = _load(path) if isinstance(value, dict) else path.read_text(encoding="utf-8")
        if actual != value:
            errors.append(f"generated output is stale: {relative}")
    return errors


def _identity_errors(files: dict) -> list[str]:
    manifest, packet = files["manifest"], files["packet"]
    errors: list[str] = []
    expected = (LESSON_ID, UNIT_ID, CANDIDATE_ID)
    for name, data in (("manifest", manifest), ("packet", packet)):
        actual = (data["lesson_id"], data["unit_id"], data["candidate_id"])
        if actual != expected:
            errors.append(f"{name} does not identify final U1-L03")
    if manifest["global_sequence_position"] != 3:
        errors.append("gold lesson is not global sequence position 3")
    if manifest["prerequisites"] != ["U1-L01", "U1-L02"]:
        errors.append("gold lesson prerequisites do not preserve the two prior lessons")
    if manifest["source_packet"] != "source-packet.json":
        errors.append("manifest does not select the v2 source packet")
    video = manifest["video"]
    if video["speaker_count"] != 1 or video["interaction_during_video"] is not False:
        errors.append("video must remain one-teacher and interaction-free")
    return errors


def _traceability_errors(packet: dict) -> list[str]:
    errors: list[str] = []
    for row in packet["inputs"]:
        path = ROOT / row["path"]
        if not path.is_file() or file_sha256(path) != row["sha256"]:
            errors.append(f"source input hash mismatch: {row['path']}")
    introductions = {row["item_id"] for row in packet["exact_introductions"]}
    recycles = {row["item_id"] for row in packet["exact_recycles"]}
    if introductions != REQUIRED_INTRODUCTIONS:
        errors.append("source packet does not own the seven locked introductions")
    if recycles != REQUIRED_RECYCLES:
        errors.append("source packet does not own the three locked recycles")
    for row in packet["exact_introductions"] + packet["exact_recycles"]:
        if not row["source_refs"]:
            errors.append(f"exact item lacks evidence: {row['item_id']}")
    if any(not row.get("bounded_scope") for row in packet["exact_introductions"]):
        errors.append("an introduced exact item lacks a bounded first-lesson scope")
    return errors


def _learning_errors(files: dict) -> list[str]:
    content, activities = files["content"], files["activities"]
    assessment, ai, pronunciation = files["assessment"], files["ai"], files["pronunciation"]
    errors: list[str] = []
    targets = set(content["curriculum_alignment"]["pronunciation_targets"])
    if targets != set(pronunciation["curriculum_target_ids"]):
        errors.append("content and pronunciation map select different exact targets")
    if any(row["text"] == "live (verb)" for row in pronunciation["entries"]):
        errors.append("removed systematic live contrast remains in pronunciation map")
    ids = {row["id"] for row in activities["activities"]}
    if "my_and_job_articles" not in ids:
        errors.append("bounded my and a/an application is missing")
    if not content["delivery"]["interaction_starts_after_video"]:
        errors.append("content allows interaction during the explanation video")
    if activities["delivery"]["interaction_during_video"] is not False:
        errors.append("activities are not explicitly deferred until after video")
    support = (assessment["mastery_task"]["support"] + " " +
               assessment["mastery_task"]["prior_lesson_support"]).lower()
    if "no sentence frames or model" not in support or "no complete introduction" not in support:
        errors.append("fresh mastery support may reveal an answer-bearing model")
    if assessment["lesson_id"] != LESSON_ID:
        errors.append("assessment retains a stale lesson id")
    ai_text = " ".join(ai["behavior"] + [ai["ending"]]).lower()
    if "never claim mastery" not in ai_text or "without assigning mastery" not in ai_text:
        errors.append("AI contract may assign mastery from coached practice")
    return errors


def _transcript_errors(transcript: str) -> list[str]:
    errors: list[str] = []
    lines = transcript.splitlines()
    if any(line and not line.startswith("Speaker 1: ") for line in lines):
        errors.append("every nonblank transcript line must use Speaker 1 format")
    if "Speaker 2:" in transcript:
        errors.append("transcript contains more than one speaker")
    if "درس جديد" not in transcript or "أول درس" in transcript:
        errors.append("transcript retains stale first-lesson wording")
    if 'ph="laɪv"' in transcript:
        errors.append("transcript still teaches the out-of-sequence live contrast")
    if "teacher, engineer, designer." not in transcript:
        errors.append("selected word-stress model is missing")
    for required in ("شخص جديد", "موضوع يقدر", "مثلًا"):
        if required not in transcript:
            errors.append(f"required conversational Arabic form is missing: {required}")
    for forbidden in ("شخصًا جديدًا", "موضوعًا يقدر"):
        if forbidden in transcript:
            errors.append(f"artificial conversational tanween remains: {forbidden}")
    ssml = re.compile(
        r'<lang xml:lang="en-US"><phoneme alphabet="ipa" ph="[^"]+">.*?</phoneme></lang>'
    )
    if len(ssml.findall(transcript)) != transcript.count("<lang xml:lang="):
        errors.append("an English span lacks the exact lang plus phoneme wrapper")
    for line in lines:
        clean = line.removeprefix("Speaker 1: ")
        clean = re.sub(r"\[[^\]]+\]", "", clean)
        clean = ssml.sub("", clean)
        if re.search(r"[A-Za-z]", clean):
            errors.append("spoken English exists outside SSML: " + clean.strip())
    return errors


def _qa_errors() -> list[str]:
    if not QA_OUTPUT.is_file() or not QA_REPORT.is_file():
        return ["gold v1 QA artifacts are missing"]
    qa = _load(QA_OUTPUT)
    errors = []
    if qa != build_qa() or QA_REPORT.read_text(encoding="utf-8") != render(qa):
        errors.append("gold v1 QA artifacts are stale")
    if qa["audit"]["major_open"] or qa["audit"]["medium_open"]:
        errors.append("gold v1 QA has an open major or medium finding")
    if any(row["status"] != "resolved" for row in qa["findings"]):
        errors.append("gold v1 QA contains an unresolved finding")
    return errors


def validate() -> list[str]:
    required = build_outputs()
    missing = [name for name in required if not (OUTPUT / name).is_file()]
    if missing:
        return [f"missing package file: {name}" for name in missing]
    files = {
        "manifest": _load(OUTPUT / "lesson-manifest.json"),
        "packet": _load(OUTPUT / "source-packet.json"),
        "content": _load(OUTPUT / "content.json"),
        "activities": _load(OUTPUT / "activities.json"),
        "assessment": _load(OUTPUT / "assessment.json"),
        "ai": _load(OUTPUT / "ai-contract.json"),
        "pronunciation": _load(OUTPUT / "video/pronunciation-map.json"),
    }
    transcript = (OUTPUT / "video/transcript.txt").read_text(encoding="utf-8")
    return (_determinism_errors() + _identity_errors(files) +
            _traceability_errors(files["packet"]) + _learning_errors(files) +
            _transcript_errors(transcript) + _qa_errors())
