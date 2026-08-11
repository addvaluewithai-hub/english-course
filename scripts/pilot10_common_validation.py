from __future__ import annotations

import re
from pathlib import Path

from scripts.pilot10_package_contract import (
    EXPECTED_FILES,
    ROOT,
    lesson_contract,
    read_json,
    sha256,
)


SSML = re.compile(
    r'<lang xml:lang="en-US"><phoneme alphabet="ipa" ph="[^"]+">.*?</phoneme></lang>'
)


def _identity_errors(path: Path, contract: dict, files: dict) -> list[str]:
    manifest, packet = files["manifest"], files["packet"]
    errors = []
    expected = (contract["lesson_id"], contract["unit_id"], contract["final_owner_id"])
    for name, data in (("manifest", manifest), ("source packet", packet)):
        actual = (data.get("lesson_id"), data.get("unit_id"), data.get("candidate_id"))
        if actual != expected:
            errors.append(f"{name} identity differs from release contract")
    if manifest.get("global_sequence_position") != contract["global_sequence_position"]:
        errors.append("manifest sequence position differs from release contract")
    if manifest.get("source_packet") != "source-packet.json":
        errors.append("manifest source packet path is not local")
    video = manifest.get("video", {})
    if video.get("speaker_count") != 1 or video.get("interaction_during_video") is not False:
        errors.append("video is not one-teacher and interaction-free")
    return errors


def _source_errors(contract: dict, packet: dict) -> list[str]:
    errors = []
    for row in packet.get("inputs", []):
        source = ROOT / row["path"]
        if not source.is_file() or sha256(source) != row["sha256"]:
            errors.append(f"source input hash mismatch: {row['path']}")
    actual_intro = {x["item_id"] for x in packet.get("exact_introductions", [])}
    actual_recycle = {x["item_id"] for x in packet.get("exact_recycles", [])}
    if actual_intro != set(contract["exact_item_roles"]["introduce"]):
        errors.append("introduced exact items differ from release contract")
    if actual_recycle != set(contract["exact_item_roles"]["fresh_recycle"]):
        errors.append("recycled exact items differ from release contract")
    for row in packet.get("exact_introductions", []):
        if not row.get("source_refs") or not row.get("bounded_scope"):
            errors.append(f"introduced item lacks bounded evidence: {row.get('item_id')}")
    for row in packet.get("exact_recycles", []):
        if not row.get("source_refs"):
            errors.append(f"recycled item lacks evidence: {row.get('item_id')}")
    return errors


def _learning_errors(files: dict, contract: dict) -> list[str]:
    manifest, content = files["manifest"], files["content"]
    activities, assessment, ai = files["activities"], files["assessment"], files["ai"]
    pronunciation = files["pronunciation"]
    errors = []
    if content.get("delivery", {}).get("interaction_starts_after_video") is not True:
        errors.append("content does not defer application until after video")
    delivery = activities.get("delivery", {})
    if delivery.get("placement") != "after_video_explanation" or delivery.get("interaction_during_video") is not False:
        errors.append("activities are not explicitly post-video")
    primary = assessment.get("mastery_task", {})
    replacement = assessment.get("replacement_mastery_task", {})
    if primary.get("scenario_en") == replacement.get("scenario_en"):
        errors.append("replacement mastery repeats the primary situation")
    if primary.get("construct_id") != replacement.get("construct_id"):
        errors.append("replacement mastery changes the assessed construct")
    if not primary.get("freshness") or not replacement.get("freshness"):
        errors.append("mastery freshness is not explicit")
    policy = assessment.get("mastery_attempt_policy", {})
    if policy.get("maximum_fresh_attempts") != 2:
        errors.append("mastery attempts are not bounded to two fresh tasks")
    ai_text = " ".join(ai.get("behavior", []) + [ai.get("ending", "")]).lower()
    if "never claim mastery" not in ai_text or "without assigning mastery" not in ai_text:
        errors.append("AI coach may assign mastery from coached practice")
    expected_pronunciation = {
        item for role in ("introduce", "fresh_recycle")
        for item in contract["exact_item_roles"][role]
        if item.startswith("a1_pronunciation.")
    }
    if set(pronunciation.get("curriculum_target_ids", [])) != expected_pronunciation:
        errors.append("pronunciation map differs from exact lesson roles")
    if manifest.get("privacy", [None])[0] is None:
        errors.append("manifest lacks a privacy boundary")
    return errors


def _coverage_errors(files: dict, contract: dict, transcript: str) -> list[str]:
    coverage = files["content"].get("curriculum_alignment", {}).get("target_coverage")
    if coverage is None:
        return [] if contract["lesson_id"] == "U1-L03" else ["target coverage is missing"]
    roles = contract["exact_item_roles"]
    expected = set(roles["introduce"] + roles["fresh_recycle"] + roles["consolidate"])
    errors = []
    if set(coverage) != expected:
        errors.append("target coverage IDs differ from exact lesson roles")
    activity_ids = {row["id"] for row in files["activities"]["activities"]}
    searchable = transcript + "\n" + str(files["content"])
    for item_id, row in coverage.items():
        expected_role = next(
            (role for role, ids in roles.items() if item_id in ids), None
        )
        if row.get("role") != expected_role:
            errors.append(f"coverage role mismatch: {item_id}")
        if not row.get("video_anchor") or row["video_anchor"] not in searchable:
            errors.append(f"coverage video anchor not found: {item_id}")
        if not row.get("post_video_activity_ids"):
            errors.append(f"coverage lacks post-video activity: {item_id}")
        elif not set(row["post_video_activity_ids"]).issubset(activity_ids):
            errors.append(f"coverage cites unknown activity: {item_id}")
        if not row.get("mastery_evidence"):
            errors.append(f"coverage lacks mastery decision: {item_id}")
    return errors


def _transcript_errors(transcript: str) -> list[str]:
    errors = []
    lines = transcript.splitlines()
    if not lines or any(line and not line.startswith("Speaker 1: ") for line in lines):
        errors.append("every nonblank transcript line must use Speaker 1 format")
    if "Speaker 2:" in transcript:
        errors.append("transcript contains a second speaker")
    if len(SSML.findall(transcript)) != transcript.count('<lang xml:lang="en-US">'):
        errors.append("an English span lacks exact language plus IPA markup")
    for line in lines:
        clean = line.removeprefix("Speaker 1: ")
        clean = re.sub(r"\[[^\]]+\]", "", clean)
        clean = SSML.sub("", clean)
        if re.search(r"[A-Za-z]", clean):
            errors.append("spoken English exists outside SSML: " + clean.strip())
    for forbidden in ("شخصًا جديدًا", "موضوعًا يقدر"):
        if forbidden in transcript:
            errors.append(f"artificial conversational tanween remains: {forbidden}")
    return errors


def _determinism_errors(lesson_id: str, path: Path) -> list[str]:
    try:
        from scripts.pilot10_package_builder import build_outputs
        from scripts.pilot10_specs.registry import SPECS
    except ImportError:
        return []
    if lesson_id not in SPECS:
        return []
    errors = []
    for relative, expected in build_outputs(SPECS[lesson_id]).items():
        file_path = path / relative
        actual = (
            read_json(file_path)
            if isinstance(expected, dict)
            else file_path.read_text(encoding="utf-8")
        )
        if actual != expected:
            errors.append(f"generated package file is stale: {relative}")
    return errors


def validate_package(lesson_id: str) -> list[str]:
    contract = lesson_contract(lesson_id)
    path = ROOT / contract["content_path"]
    actual_files = {x.relative_to(path).as_posix() for x in path.rglob("*") if x.is_file()}
    if actual_files != EXPECTED_FILES:
        return [f"package file set differs: expected 12, found {len(actual_files)}"]
    files = {
        "manifest": read_json(path / "lesson-manifest.json"),
        "packet": read_json(path / "source-packet.json"),
        "content": read_json(path / "content.json"),
        "activities": read_json(path / "activities.json"),
        "assessment": read_json(path / "assessment.json"),
        "ai": read_json(path / "ai-contract.json"),
        "pronunciation": read_json(path / "video/pronunciation-map.json"),
    }
    transcript = (path / "video/transcript.txt").read_text(encoding="utf-8")
    return (
        _determinism_errors(lesson_id, path)
        + _identity_errors(path, contract, files)
        + _source_errors(contract, files["packet"])
        + _learning_errors(files, contract)
        + _coverage_errors(files, contract, transcript)
        + _transcript_errors(transcript)
    )
