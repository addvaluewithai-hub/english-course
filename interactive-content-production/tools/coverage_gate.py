#!/usr/bin/env python3
"""Fail-closed content-coverage audit against actual canonical source + semantic locks.

  python3 interactive-content-production/tools/coverage_gate.py check A1 U1-L01
  python3 interactive-content-production/tools/coverage_gate.py ready A1 U1-L01

check: verifies exact source item set, locked role, source paths, decisions and evidence
       WITHOUT claiming pedagogical quality or passing an incomplete lesson.
ready: additionally blocks unresolved source/teaching concerns and missing active evidence.

No external packages, no writes, no source mutation.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED = {"teach", "contextual", "bounded", "escalate"}
REVIEW = {"reviewed", "needs-review"}
CATEGORIES = {"word", "phrase", "grammar", "ability", "pronunciation"}
ACTIVE = {"teach", "contextual", "bounded"}
PHRASE_ROLES = {"formulaic_productive_required", "productive_required", "receptive_required"}


def inputs(level: str, lesson: str):
    level = level.lower()
    d = ROOT / "curriculum" / "levels" / level
    manifest = json.loads((d / "manifest.json").read_text())
    if not manifest.get("lesson_design_authorized"):
        raise ValueError(f"{level}: lesson design not authorized")
    ledger_file = d / "design-review" / "06-coverage-ledger" / "generated" / "coverage-ledger.json"
    ledger = json.loads(ledger_file.read_text())
    source = {r["item_id"]: r for r in ledger["records"] if lesson in r["lifecycle"].get("introduce", [])}
    if len(source) != len(set(source)):
        raise ValueError("Duplicate canonical source item")
    roles = {}
    phrase_file = d / "semantic-lock" / "phrase-control-decisions.json"
    if phrase_file.exists():
        groups = json.loads(phrase_file.read_text())["role_groups"]
        for g in groups:
            for item_id in g["item_ids"]:
                if item_id in roles: raise ValueError(f"Duplicate semantic role: {item_id}")
                roles[item_id] = g["semantic_role"]
    word_file = d / "semantic-lock" / "word-control-decisions.json"
    word_policy = json.loads(word_file.read_text()) if word_file.exists() else None
    return source, roles, word_policy


def expected_role(item, roles, words):
    if item["category"] == "phrase":
        role = roles.get(item["item_id"])
        if role not in PHRASE_ROLES:
            raise ValueError("Phrase lacks locked explicit semantic role: " + item["item_id"])
        return role
    if item["category"] == "word" and words:
        word = item["label"]
        if word in words["grammar_owned"]["headwords"]: return "grammar_owned_required"
        if word in words["productive_promotion"]["headwords"]: return "productive_required"
        return words["default_pending_role"]["semantic_role"]
    # Ability/grammar/pronunciation require human semantic-role classification.
    # Never mistake a stage-6 ledger item for an independent productive target.
    return "role_requires_explicit_pedagogical_decision"


def audit(level, lesson, ready=False):
    source, roles, words = inputs(level, lesson)
    file = ROOT / "interactive-content-production" / "coverage" / level.upper() / (lesson + ".json")
    package = json.loads(file.read_text(encoding="utf-8"))
    assert package["level"] == level.upper() and package["lessonId"] == lesson, "Wrong lesson mapping"
    assert package["sourceRefs"]["ledger"].endswith("/coverage-ledger.json"), "Missing canonical ledger"
    actual = package["items"]
    ids = [r["sourceId"] for r in actual]
    assert len(ids) == len(set(ids)), "Duplicate item IDs in coverage map"
    assert set(ids) == set(source), f"Coverage lost/added canonical items: missing={sorted(set(source)-set(ids))} extra={sorted(set(ids)-set(source))}"
    problems = []
    for row in actual:
        item = source[row["sourceId"]]
        id = row["sourceId"]
        assert row["category"] == item["category"], f"{id}: category drift"
        assert row["label"] == item["label"], f"{id}: source label drift"
        assert row["semanticRole"] == expected_role(item, roles, words), f"{id}: semantic role drift"
        assert row["disposition"] in ALLOWED and row["review"] in REVIEW, f"{id}: invalid decision"
        assert len(row["rationale"].strip()) >= 30, f"{id}: missing meaningful rationale"
        assert isinstance(row["evidence"], list), f"{id}: missing evidence contract"
        if row["disposition"] == "teach" and row["semanticRole"] in {"productive_required", "formulaic_productive_required"}:
            if not any(e["kind"] == "productive-speaking" for e in row["evidence"]):
                problems.append(f"{id}: required productive target has no planned Speaking evidence")
        if row["disposition"] in ACTIVE and not row["evidence"]:
            problems.append(f"{id}: active source has no mapped lesson evidence")
        if row["disposition"] == "escalate":
            problems.append(f"{id}: scope/coverage conflict awaiting explicit review")
        if row["review"] != "reviewed":
            problems.append(f"{id}: pedagogical decision not yet reviewed")
        if row.get("approvalRef") and row["approvalRef"] == "auto-approved":
            raise AssertionError(f"{id}: fake approval reference")
    assert len(actual) == len(source), "Source count mismatch"
    required = ("sourceReview", "scriptCritique", "screenshotReview", "liveAudio", "speakingReview", "ownerAcceptance")
    quality = package.get("qualityGates", {})
    for gate in required:
        if quality.get(gate) != "accepted":
            problems.append("QA/owner gate not accepted: " + gate)
    result = {"level":level.upper(), "lessonId":lesson, "canonicalItems":len(source),
              "structuralValid":True, "ready":not problems, "blockers":problems}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if ready and problems:
        raise SystemExit(f"NOT READY: {len(problems)} unresolved curriculum/evidence decisions")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in {"check", "ready"}:
        raise SystemExit(__doc__)
    audit(sys.argv[2].upper(), sys.argv[3], sys.argv[1] == "ready")
