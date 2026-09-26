#!/usr/bin/env python3
"""Mechanically validate B1 Stage-4.5 constraint coverage.

Human curriculum judgments live in the Stage-4.5 review. This script checks only
frozen identifiers/counts and required handoff markers; it does not infer homes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B1 = ROOT / "curriculum/levels/b1"
REVIEW = B1 / "design-review/04.5-pronunciation-exit-carry-forward/review.md"
PRON = B1 / "pronunciation.json"
B1_EXIT = B1 / "exit_contract.json"
A2_EXIT = ROOT / "curriculum/levels/a2/exit_contract.json"

EXPECTED_PRON_IDS = {
    "pronunciation.sound_perception.b1",
    "pronunciation.consonant_clarity.b1",
    "pronunciation.vowel_clarity.b1",
    "pronunciation.syllable_shape.b1",
    "pronunciation.grammatical_endings.b1",
    "pronunciation.word_stress.b1",
    "pronunciation.prominence_rhythm.b1",
    "pronunciation.connected_speech.b1",
    "pronunciation.intonation_stance.b1",
    "pronunciation.chunking_monitoring_repair.b1",
}


def fail(message: str) -> None:
    raise SystemExit(f"B1 STAGE-4.5 AUDIT FAIL — {message}")


def main() -> None:
    pron = json.loads(PRON.read_text(encoding="utf-8"))
    b1_exit = json.loads(B1_EXIT.read_text(encoding="utf-8"))
    a2_exit = json.loads(A2_EXIT.read_text(encoding="utf-8"))
    review = REVIEW.read_text(encoding="utf-8")

    actual_pron = {item["item_id"] for item in pron.get("items", [])}
    if actual_pron != EXPECTED_PRON_IDS:
        fail(f"pronunciation IDs drift; missing={sorted(EXPECTED_PRON_IDS - actual_pron)} extra={sorted(actual_pron - EXPECTED_PRON_IDS)}")

    if b1_exit.get("level") != "B1":
        fail("B1 exit contract level mismatch")
    if a2_exit.get("status") != "semantic_inventory_locked_v1":
        fail("A2 is no longer the expected locked prerequisite state")
    if (a2_exit.get("semantic_lock") or {}).get("lesson_design_authorized") is not True:
        fail("A2 prerequisite semantic/design lock is not authorized")

    p_sections = re.findall(r"^## P\d{2} — ", review, flags=re.MULTILINE)
    cf_sections = re.findall(r"^## CF\d{2} — ", review, flags=re.MULTILINE)
    if len(p_sections) != 10:
        fail(f"expected 10 pronunciation review sections; found {len(p_sections)}")
    if len(cf_sections) != 15:
        fail(f"expected 15 A2 carry-forward review sections; found {len(cf_sections)}")

    markers = (
        "Current architecture: **20 capability families + 8 cross-cutting requirements**",
        "All **10 / 10** strands have natural capability homes.",
        "No standalone pronunciation unit is required by the evidence.",
        "**ACCEPTED FOR STAGE 05 CURRICULUM / LESSON MAPPING.**",
        "A2: **locked prerequisite/retrieval; no silent edits**",
        "abilities: **249 / 249 reviewed**",
        "phrases: **175 / 175 reviewed**",
        "grammar: **338 / 338 reviewed into 59 usable systems/infrastructure families**",
        "words: **809 / 809 exact primary homes, 0 orphans**",
        "pronunciation: **10 / 10 reviewed with natural homes**",
    )
    for marker in markers:
        if marker not in review:
            fail(f"required Stage-4.5 marker missing: {marker}")

    required_assessments = {
        "An unscripted familiar problem",
        "A connected narrative",
        "A reasoned response in more than one context",
    }
    actual_assessments = {x.get("text") for x in b1_exit.get("assessment_requirements", [])}
    if not required_assessments <= actual_assessments:
        fail(f"B1 assessment contract drift: {sorted(actual_assessments)}")

    print(
        "B1 STAGE-4.5 AUDIT PASS — 10/10 pronunciation strands; "
        "15 A2 carry-forward branches; B1 exit evidence markers intact"
    )


if __name__ == "__main__":
    main()
