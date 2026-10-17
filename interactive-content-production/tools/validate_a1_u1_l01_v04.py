#!/usr/bin/env python3
"""Validate the EDITORIAL U1-L01 v04 trial. This is NOT source approval or live lesson QA.

Usage: python3 interactive-content-production/tools/validate_a1_u1_l01_v04.py
Requires only the Python 3 standard library; intentionally checks negative fixtures too.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "coverage" / "A1"
P = SRC / "U1-L01-NATURAL-FIRST-CONTACT-v04.CANDIDATE.json"
M = SRC / "U1-L01-v04-36-SOURCE-DECISION-MATRIX.CANDIDATE.json"
C = SRC / "U1-L01.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(package: dict, matrix: dict, canonical: dict) -> list[str]:
    errors: list[str] = []
    def require(ok: bool, label: str) -> None:
        if not ok:
            errors.append(label)

    require(not package.get("releaseAuthorized"), "NOT RELEASE AUTHORIZED")
    require(not package.get("audio", {}).get("purchaseApproved"), "NO PAID AUDIO AUTHORIZATION")
    require(not package.get("audio", {}).get("approved"), "NO APPROVED WAV")

    source_rows = canonical["items"]
    proposed_rows = matrix["rows"]
    source_ids = [r["sourceId"] for r in source_rows]
    proposed_ids = [r["sourceId"] for r in proposed_rows]
    require(len(source_ids) == len(set(source_ids)) == 36, "canonical 36 unique")
    require(set(source_ids) == set(proposed_ids) and len(proposed_ids) == 36, "exact 36 source IDs")
    roles = {r["sourceId"]: r["semanticRole"] for r in source_rows}
    dispositions = {r["sourceId"]: r["disposition"] for r in source_rows}
    for row in proposed_rows:
        sid = row["sourceId"]
        require(row["sourceSemanticRole"] == roles.get(sid), "unchanged semantic role: " + sid)
        require(row["sourceDisposition"] == dispositions.get(sid), "unchanged disposition: " + sid)
        require(row["sourceOwnerRuling"] == ("REQUIRED" if dispositions.get(sid) == "escalate" else "UNCHANGED"), "source owner ruling: " + sid)
        require(not row.get("ledgerLifecycleAmended"), "ledger untouched: " + sid)
        if row["proposal"] == "rehome_candidate":
            require(row["evidenceBeatId"] is None and row["evidenceStatus"] == "NOT_TAUGHT_IN_V04", "no fake rehome teaching: " + sid)
    require(sum(r["sourceOwnerRuling"] == "REQUIRED" for r in proposed_rows) == 12, "12 escalations unresolved")
    require(sum(r["proposal"] == "rehome_candidate" for r in proposed_rows) == 7, "7 proposed rehomes, not enacted")

    turns = package["sourceDialogue"]["turns"]
    require(len(turns) == 8, "eight short English source turns")
    require([t["id"] for t in turns] == [f"t{x:02}" for x in range(1, 9)], "ordered source turn IDs")
    require([t["speaker"] for t in turns] == ["Maya", "Leo"] * 4, "two turn-taking speakers")
    source_text = " ".join(t["text"].lower() for t in turns)
    for required in ("good morning", "what's your name", "how are you", "pretty good", "really good", "thank you", "excited", "feeling"):
        require(required in source_text, "natural core exact term: " + required)

    clips = package["clips"]
    clip_by_id = {x["clipId"]: x for x in clips}
    require(len(clip_by_id) == len(clips), "unique clip IDs")
    turn_index = {t["id"]: n for n, t in enumerate(turns)}
    for clip in clips:
        require(clip["startTurn"] in turn_index and clip["endTurn"] in turn_index, "clip turns exist: " + clip["clipId"])
        if clip["startTurn"] in turn_index and clip["endTurn"] in turn_index:
            require(turn_index[clip["startTurn"]] <= turn_index[clip["endTurn"]], "clip ordered: " + clip["clipId"])
        require(clip.get("startMs") is None and clip.get("endMs") is None and not clip.get("approved"), "no invented sound timing: " + clip["clipId"])
    require(clip_by_id.get("full-conversation", {}).get("startTurn") == "t01" and
            clip_by_id.get("full-conversation", {}).get("endTurn") == "t08", "full contains all turns")
    wellbeing = clip_by_id.get("wellbeing", {})
    if wellbeing.get("startTurn") in turn_index and wellbeing.get("endTurn") in turn_index:
        part = " ".join(t["text"].lower() for t in turns[turn_index[wellbeing["startTurn"]]:turn_index[wellbeing["endTurn"]]+1])
        require("pretty good" in part and "really good" in part, "wellbeing clip includes both replies")
    require(clip_by_id.get("how-are-you-question", {}).get("startTurn") == "t03" and
            clip_by_id.get("how-are-you-question", {}).get("endTurn") == "t03", "single-turn pronunciation clip")

    beats = [b for s in package["scenes"] for b in s["beats"]]
    names = [s["id"] + "/" + b["beatId"] for s in package["scenes"] for b in s["beats"]]
    require(len(names) == len(set(names)) == 22, "22 unique content beats")
    require(all(b.get("teacherSpeech") and b.get("boardStateId") and b.get("kind") for b in beats), "fully authored beat records")
    require(all(b.get("audioClipId") in clip_by_id for b in beats if b.get("audioClipId")), "all beat clips have source")
    board = package["boardStates"]
    by_board = {x["boardStateId"]: x for x in board}
    require(len(board) == len(by_board) == 22, "22 distinct board states")
    require(set(by_board) == {b["boardStateId"] for b in beats}, "all board states correspond to beats")
    require(all(b.get("visualIntent") and b.get("altText") and b.get("portrait") and b.get("landscape") and not b.get("implemented") for b in board), "explicit planned accessibility and honest implementation states")

    quizzes = [s["assessment"] for s in package["scenes"] if s["assessment"]["kind"] == "deterministic-mc"]
    require(len(quizzes) == 5, "5 authored MC questions")
    positions = []
    for quiz in quizzes:
        ids = [o["id"] for o in quiz["options"]]
        require(len(ids) == len(set(ids)) == 3, "three distinct choices: " + quiz["questionId"])
        require(quiz["correctOptionId"] in ids, "correct answer present: " + quiz["questionId"])
        positions.append(ids.index(quiz["correctOptionId"]) if quiz["correctOptionId"] in ids else -1)
        require(bool(quiz.get("promptAr") and quiz.get("correctFeedbackAr")), "authored question and correct feedback: " + quiz["questionId"])
        wrong = set(ids) - {quiz["correctOptionId"]}
        require(set(quiz.get("wrongFeedbackByOptionAr", {})) == wrong, "exact wrong feedback for each distractor: " + quiz["questionId"])
        require(all(o.get("misconception") and o.get("text") for o in quiz["options"]), "distinct rationale for each option: " + quiz["questionId"])
        require(not any("placeholder" in str(v).lower() for v in quiz.values()), "no feedback placeholders: " + quiz["questionId"])
    require(positions == [2, 0, 1, 2, 0], "balanced explicit MC key positions")

    first = package["scenes"][0]
    require(first["id"] == "s01-first-listen" and first["beats"][0]["beatId"] == "neutral-instruction", "neutral first listen")
    preaudio = first["beats"][0]["teacherSpeech"].lower()
    require(not any(word in preaudio for word in ("english class", "كلاس", "مدرسة", "زميل", "meet", "class", "انجليزي")), "no gist spoiler in pre-audio speech")
    require(first["beats"][1].get("audioClipId") == "full-conversation" and first["beats"][1].get("transcriptVisibility") == "hidden", "actual full listening before quiz")
    require(first["assessment"]["evidenceIntent"].get("requireActuallyHeardAudio"), "quiz requires actual heard audio")
    reading = next(s for s in package["scenes"] if s["id"] == "s04-reading-note")
    require("Introduce yourself" in reading["beats"][0].get("readText", "") and "people" in reading["beats"][0]["readText"], "independent note contains target reading")
    require(reading["beats"][0].get("teacherMustNotReadNoteUntilAfterAnswer"), "reading note must not be read before independent attempt")
    speaking = next(s for s in package["scenes"] if s["id"] == "s07-new-speaking")
    target_ids = speaking["assessment"]["separateProductiveEvidence"]["requiredSourceIds"]
    require(len(target_ids) == len(set(target_ids)) == 7, "7 individual productive targets")
    require(speaking["assessment"]["separateProductiveEvidence"]["doNotAutoAwardOnLessonCompletion"], "avoid auto-awarding seven exact items")
    require(speaking["assessment"]["separateProductiveEvidence"]["trackActualLearnerTurnIds"], "productive proof linked to learner turns")

    known = {(s["id"], b["beatId"]) for s in package["scenes"] for b in s["beats"]}
    for row in proposed_rows:
        if row["evidenceBeatId"] is not None:
            require((row["evidenceSceneId"], row["evidenceBeatId"].split("/")[-1]) in known, "source row evidence beat exists: " + row["sourceId"])
    return errors


def main() -> None:
    p, m, c = load(P), load(M), load(C)
    failures = check(p, m, c)
    if failures:
        raise SystemExit("FAIL: v04 candidate: " + "; ".join(failures))
    print("PASS: v04 structural trial (36 source IDs / 12 owner gates / 22 exact authored beats / 22 board specs / 5 MC + distinct feedback / no paid audio)")
    for label, corrupt in [
        ("all answers first", lambda v: [s["assessment"]["options"].sort(key=lambda o: 0 if o["id"] == s["assessment"]["correctOptionId"] else 1) for s in v["scenes"] if s["assessment"]["kind"] == "deterministic-mc"]),
        ("missing wrong-option feedback", lambda v: v["scenes"][0]["assessment"]["wrongFeedbackByOptionAr"].clear()),
        ("premature first-listen answer hint", lambda v: v["scenes"][0]["beats"][0].update(teacherSpeech="هم رايحين English class")),
        ("fabricated source audio timestamps", lambda v: v["clips"][0].update(startMs=100, endMs=200, approved=True)),
    ]:
        modified = copy.deepcopy(p)
        corrupt(modified)
        assert check(modified, m, c), "negative fixture was wrongly accepted: " + label
        print("PASS negative fixture:", label)


if __name__ == "__main__":
    main()
