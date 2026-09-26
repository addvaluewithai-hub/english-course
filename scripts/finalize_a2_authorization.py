#!/usr/bin/env python3
"""Finalize A2 lesson-design authorization from one explicit human gate decision.

This script does not make semantic or pedagogical decisions. It validates the
human-reviewed Stage-9 declaration against pinned curriculum artifacts and then
restores the authorized manifest/exit-contract state after base regeneration.
Delivery/media production remains a separate, explicitly false gate.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
A2 = ROOT / "curriculum/levels/a2"
REVIEW = A2 / "design-review"
AUTH = REVIEW / "10-authorization-gate/authorization.json"

EXPECTED_COUNTS = {
    "ability": 269,
    "phrase": 176,
    "grammar": 291,
    "word": 871,
    "pronunciation": 10,
}
EXPECTED_TOTAL = 1617
EXPECTED_MASTERY = {
    "productive": 935,
    "interactive": 46,
    "receptive": 429,
    "integrated_support": 207,
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def validate_pinned_evidence(decision: dict[str, Any]) -> None:
    evidence = decision.get("evidence_blobs") or []
    if not evidence:
        raise ValueError("A2 authorization requires pinned evidence blobs")
    for item in evidence:
        rel = item["path"]
        expected = item["git_blob_sha"]
        path = ROOT / rel
        if not path.exists():
            raise ValueError(f"A2 authorization evidence missing: {rel}")
        actual = git_blob_sha(path)
        if actual != expected:
            raise ValueError(
                f"A2 authorization evidence drift for {rel}: {actual} != {expected}; "
                "human re-review is required before authorization can be restored"
            )


def validate_gate(decision: dict[str, Any]) -> None:
    if decision.get("level") != "A2":
        raise ValueError("A2 authorization declaration has wrong level")
    if decision.get("status") != "human_lesson_design_authorization_reviewed_locked_v1":
        raise ValueError("A2 authorization declaration is not reviewed/locked")
    if decision.get("lesson_design_authorized") is not True:
        raise ValueError("A2 Stage-9 declaration must explicitly authorize lesson design")
    if decision.get("delivery_content_production_authorized") is not False:
        raise ValueError("A2 lesson-design authorization must not authorize delivery/media production")
    if int(decision.get("human_review_queue", -1)) != 0:
        raise ValueError("A2 authorization requires human_review_queue = 0")

    architecture = decision.get("architecture") or {}
    if architecture != {"units": 12, "lesson_slots": 83}:
        raise ValueError(f"A2 authorization architecture drift: {architecture}")

    validate_pinned_evidence(decision)

    coverage = load(REVIEW / "06-coverage-ledger/generated/coverage-ledger.json")
    if coverage.get("level") != "A2" or coverage.get("lesson_count") != 83:
        raise ValueError("A2 coverage ledger architecture is not 83 lessons")
    if coverage.get("record_counts") != EXPECTED_COUNTS:
        raise ValueError(f"A2 coverage count drift: {coverage.get('record_counts')}")
    if len(coverage.get("records") or []) != EXPECTED_TOTAL:
        raise ValueError("A2 coverage ledger does not contain exactly 1,617 records")

    semantic = load(REVIEW / "08-semantic-lock/generated/semantic-role-ledger.json")
    if semantic.get("level") != "A2" or semantic.get("record_count") != EXPECTED_TOTAL:
        raise ValueError("A2 semantic ledger does not contain exactly 1,617 records")
    if semantic.get("category_counts") != EXPECTED_COUNTS:
        raise ValueError(f"A2 semantic category drift: {semantic.get('category_counts')}")
    if semantic.get("mastery_mode_counts") != EXPECTED_MASTERY:
        raise ValueError(f"A2 semantic mastery drift: {semantic.get('mastery_mode_counts')}")

    critic = (REVIEW / "08.5-role-aware-critic/critic-decisions-v1.md").read_text(encoding="utf-8")
    required_critic_markers = (
        "HUMAN CRITIC COMPLETE — ROLE-AWARE RECONCILIATION LOCKED",
        "role-aware hotspot queue manually reviewed",
        "Stage 08 + Stage 08.5 are closed",
    )
    for marker in required_critic_markers:
        if marker not in critic:
            raise ValueError(f"A2 Stage-08.5 lock marker missing: {marker}")

    briefs = (REVIEW / "09-lesson-briefs/lesson-briefs.md").read_text(encoding="utf-8")
    lesson_headings = re.findall(r"^## U\d+-L\d+ — ", briefs, flags=re.MULTILINE)
    unit_critics = re.findall(r"^### Unit \d+ rolling critic$", briefs, flags=re.MULTILINE)
    if len(lesson_headings) != 83:
        raise ValueError(f"A2 authorization requires 83 lesson briefs; found {len(lesson_headings)}")
    if len(unit_critics) != 12:
        raise ValueError(f"A2 authorization requires 12 rolling critics; found {len(unit_critics)}")
    if "CLOSED — Delivery Blueprint / Lesson Briefs complete and coherent at 83 / 83." not in briefs:
        raise ValueError("A2 whole-level Milestone-4 close marker is missing")


def main() -> None:
    if not AUTH.exists():
        print("A2 authorization declaration absent; base candidate state remains unchanged.")
        return

    decision = load(AUTH)
    validate_gate(decision)

    manifest = load(A2 / "manifest.json")
    contract = load(A2 / "exit_contract.json")

    manifest["lesson_design_authorized"] = True
    manifest["delivery_content_production_authorized"] = False
    manifest["delivery_gate_note"] = (
        "A2 curriculum lesson design and controlled authoring planning are authorized. "
        "Lesson-package/audio/image/video production remains governed by the separate "
        "delivery workstream and does not modify or bypass TEST-002."
    )
    manifest["semantic_lock"] = {
        "status": "human_semantic_decisions_v1_plus_stage_08_5_critic_locked",
        "report": "curriculum/levels/a2/design-review/08-semantic-lock/generated/semantic-role-report.md",
        "critic": "curriculum/levels/a2/design-review/08.5-role-aware-critic/critic-decisions-v1.md",
        "human_review_queue": 0,
        "total_primary_items": EXPECTED_TOTAL,
    }
    manifest["authorization_gate"] = {
        "status": decision["status"],
        "declaration": "curriculum/levels/a2/design-review/10-authorization-gate/authorization.json",
        "architecture": decision["architecture"],
    }
    manifest["status"] = "semantic_design_lock_reviewed_lesson_design_authorized"

    contract["status"] = "semantic_inventory_locked_v1"
    contract["inventory_obligations"] = {
        "words": "semantic_lock_v1: 500 productive/contextual; 317 receptive/contextual; 54 integrated_support",
        "phrases": "semantic_lock_v1: 118 productive/formulaic; 28 receptive/contextual; 30 integrated_support",
        "grammar": "semantic_lock_v1: 184 productive rows; 9 receptive rows; 98 integrated_support rows across 30 productive / 2 receptive / 14 support systems",
        "abilities": "semantic_lock_v1: 133 productive; 46 interactive; 74 receptive; 16 integrated_support",
        "pronunciation": "semantic_lock_v1: 1 receptive; 9 integrated_support",
    }
    contract["semantic_lock"] = {
        "status": "human_semantic_decisions_v1_plus_stage_08_5_critic_locked",
        "lesson_design_authorized": True,
        "human_review_queue": 0,
        "report": "curriculum/levels/a2/design-review/08-semantic-lock/generated/semantic-role-report.md",
        "critic": "curriculum/levels/a2/design-review/08.5-role-aware-critic/critic-decisions-v1.md",
        "completion_is_not_mastery": True,
        "receptive_does_not_imply_productive": True,
        "productive_does_not_imply_all_dictionary_senses": True,
    }
    contract["authorization_gate"] = {
        "status": decision["status"],
        "declaration": "curriculum/levels/a2/design-review/10-authorization-gate/authorization.json",
        "architecture": decision["architecture"],
    }
    contract["delivery_content_production_authorized"] = False
    contract["delivery_gate_note"] = manifest["delivery_gate_note"]

    write(A2 / "manifest.json", manifest)
    write(A2 / "exit_contract.json", contract)
    print(json.dumps({
        "status": manifest["status"],
        "lesson_design_authorized": True,
        "delivery_content_production_authorized": False,
        "human_review_queue": 0,
        "lesson_slots": 83,
    }, indent=2))


if __name__ == "__main__":
    main()
