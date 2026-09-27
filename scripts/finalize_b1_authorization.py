#!/usr/bin/env python3
"""Finalize B1 lesson-design authorization from one explicit human gate decision.

NON-SEMANTIC / NON-PEDAGOGICAL. This script validates the reviewed Stage-9
declaration against pinned B1 curriculum evidence, then restores the authorized
manifest/exit-contract state after base regeneration. Delivery/media production
remains a separate, explicitly false gate and TEST-002 is untouched.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
B1 = ROOT / "curriculum/levels/b1"
REVIEW = B1 / "design-review"
AUTH = REVIEW / "09-authorization-gate/authorization.json"

EXPECTED_COUNTS = {
    "ability": 249,
    "phrase": 175,
    "grammar": 338,
    "word": 809,
    "pronunciation": 10,
}
EXPECTED_TOTAL = 1581
EXPECTED_MASTERY = {
    "integrated_support": 316,
    "interactive": 57,
    "productive": 597,
    "receptive": 611,
}
ZERO_NEW = {
    "U1-L07","U2-L07","U3-L08","U4-L09","U5-L07","U6-L07","U7-L07","U8-L07",
    "U9-L07","U10-L07","U11-L07","U12-L01","U12-L02","U12-L03","U12-L04","U12-L05",
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
    if len(evidence) < 7:
        raise ValueError("B1 authorization requires the complete pinned evidence set")
    seen: set[str] = set()
    for item in evidence:
        rel = item["path"]
        expected = item["git_blob_sha"]
        if rel in seen:
            raise ValueError(f"duplicate B1 authorization evidence path: {rel}")
        seen.add(rel)
        path = ROOT / rel
        if not path.exists():
            raise ValueError(f"B1 authorization evidence missing: {rel}")
        actual = git_blob_sha(path)
        if actual != expected:
            raise ValueError(
                f"B1 authorization evidence drift for {rel}: {actual} != {expected}; "
                "human re-review is required before authorization can be restored"
            )


def validate_gate(decision: dict[str, Any]) -> None:
    if decision.get("level") != "B1":
        raise ValueError("B1 authorization declaration has wrong level")
    if decision.get("status") != "human_lesson_design_authorization_reviewed_locked_v1":
        raise ValueError("B1 authorization declaration is not reviewed/locked")
    if decision.get("lesson_design_authorized") is not True:
        raise ValueError("B1 Stage-9 declaration must explicitly authorize lesson design")
    if decision.get("delivery_content_production_authorized") is not False:
        raise ValueError("B1 lesson-design authorization must not authorize delivery/media production")
    if int(decision.get("human_review_queue", -1)) != 0:
        raise ValueError("B1 authorization requires human_review_queue = 0")
    if decision.get("architecture") != {"units": 12, "lesson_slots": 85}:
        raise ValueError(f"B1 authorization architecture drift: {decision.get('architecture')}")

    gate = decision.get("gate_conditions") or {}
    required_gate = {
        "exact_semantic_roles": "1581/1581",
        "semantic_orphans": 0,
        "automation_inferred_semantic_roles": 0,
        "human_review_queue": 0,
        "stage_08_5_exact_semantic_overrides": 85,
        "stage_08_5_exact_scheduling_corrections": 3,
        "coverage_lifecycle_gaps": 0,
        "zero_new_transfer_integration_slots": "16/16",
        "lesson_briefs": "85/85",
        "rolling_unit_critics": "12/12",
        "whole_level_critic": "closed",
        "structural_changes_after_role_aware_critic": 0,
        "architecture_retained": "12 units / 85 lesson slots",
        "mediation_source_mode_preserved": True,
        "pronunciation_intelligibility_only": True,
        "a2_prerequisite_unchanged": True,
    }
    for key, expected in required_gate.items():
        if gate.get(key) != expected:
            raise ValueError(f"B1 authorization gate condition drift: {key}={gate.get(key)!r} != {expected!r}")

    validate_pinned_evidence(decision)

    coverage = load(REVIEW / "06-coverage-ledger/generated/coverage-ledger.json")
    if coverage.get("level") != "B1" or coverage.get("lesson_count") != 85:
        raise ValueError("B1 coverage ledger architecture is not 85 lessons")
    if coverage.get("record_counts") != EXPECTED_COUNTS:
        raise ValueError(f"B1 coverage count drift: {coverage.get('record_counts')}")
    records = coverage.get("records") or []
    if len(records) != EXPECTED_TOTAL:
        raise ValueError("B1 coverage ledger does not contain exactly 1,581 records")

    # Exact lifecycle completeness and protected zero-new slots after Stage 08.5.
    required_later = ("practice", "fresh_retrieval", "recycle", "consolidate", "exit_verify")
    for stage in required_later:
        gaps = [x["item_id"] for x in records if not x["lifecycle"].get(stage)]
        if gaps:
            raise ValueError(f"B1 coverage lifecycle has {len(gaps)} {stage} gaps")
    intro_counts = Counter(x["lifecycle"]["introduce"][0] for x in records)
    if {lid for lid in ZERO_NEW if intro_counts[lid]}:
        raise ValueError("B1 designated zero-new transfer/integration slot received a new introduction")
    if len(ZERO_NEW) != 16:
        raise ValueError("B1 zero-new gate must contain exactly 16 locked slots")

    load_critic = load(REVIEW / "06-coverage-ledger/load-critic.json")
    if load_critic.get("status") != "human_stage06_load_critic_reviewed_v1":
        raise ValueError("B1 Stage-06 human load critic is not reviewed")
    reaudit = load_critic.get("stage_08_5_reaudit") or {}
    if reaudit.get("status") != "human_role_aware_feedback_reaudited_v1":
        raise ValueError("B1 Stage-08.5 coverage feedback re-audit is not closed")
    result = reaudit.get("result") or {}
    if result.get("required_lifecycle_gaps") != 0 or result.get("zero_new_transfer_violations") != 0:
        raise ValueError("B1 Stage-08.5 coverage re-audit has unresolved structural failures")
    if result.get("warning_count") != 15 or result.get("raw_warning_set_changed") is not False:
        raise ValueError("B1 reviewed raw warning set drifted after Stage-08.5 feedback")
    if result.get("architecture_changed") is not False:
        raise ValueError("B1 Stage-08.5 unexpectedly changed the locked architecture")

    semantic = load(REVIEW / "08-semantic-lock/generated/semantic-role-ledger.json")
    if semantic.get("level") != "B1" or semantic.get("record_count") != EXPECTED_TOTAL:
        raise ValueError("B1 semantic ledger does not contain exactly 1,581 records")
    if semantic.get("record_counts") != EXPECTED_COUNTS:
        raise ValueError(f"B1 semantic category drift: {semantic.get('record_counts')}")
    if semantic.get("mastery_counts") != EXPECTED_MASTERY:
        raise ValueError(f"B1 semantic mastery drift: {semantic.get('mastery_counts')}")
    if semantic.get("automation_inferred_semantic_roles") != 0 or semantic.get("human_semantic_orphans") != 0:
        raise ValueError("B1 semantic ledger has inferred roles or unresolved semantic orphans")
    applied = semantic.get("stage_08_5_applied") or {}
    if applied.get("total_exact_semantic_overrides") != 85:
        raise ValueError("B1 Stage-08.5 exact semantic override count is not 85")
    if (
        applied.get("word_to_receptive_count") != 67
        or applied.get("grammar_to_support_count") != 17
        or applied.get("phrase_to_receptive_count") != 1
    ):
        raise ValueError("B1 Stage-08.5 semantic override group counts drifted")

    critic = (REVIEW / "08.5-role-aware-critic/critic-decisions.md").read_text(encoding="utf-8")
    for marker in (
        "HUMAN CRITIC COMPLETE — STAGE 08 + STAGE 08.5 CLOSED",
        "human review queue is **0**",
        "Stage 08 + Stage 08.5 are closed. Milestone 3",
        "Retain 12 units / 85 lesson slots",
    ):
        if marker not in critic:
            raise ValueError(f"B1 Stage-08.5 close marker missing: {marker}")

    briefs = (REVIEW / "07-lesson-briefs/lesson-briefs.md").read_text(encoding="utf-8")
    lesson_headings = re.findall(r"^## U\d+-L\d+ — ", briefs, flags=re.MULTILINE)
    unit_critics = re.findall(r"^### Unit \d+ rolling critic$", briefs, flags=re.MULTILINE)
    if len(lesson_headings) != 85:
        raise ValueError(f"B1 authorization requires 85 lesson briefs; found {len(lesson_headings)}")
    if len(unit_critics) != 12:
        raise ValueError(f"B1 authorization requires 12 rolling critics; found {len(unit_critics)}")
    for marker in (
        "STAGE 07 COMPLETE; STAGE 08.5 FEEDBACK RECONCILED",
        "U10-L02 **passes the Stage-08.5 role-aware load review**",
        "## 12. Semantic lock is now reconciled",
        "Stage 08 + Stage 08.5 are now closed across all **1,581** exact B1 source records.",
    ):
        if marker not in briefs:
            raise ValueError(f"B1 reconciled brief marker missing: {marker}")


def main() -> None:
    if not AUTH.exists():
        print("B1 authorization declaration absent; base candidate state remains unchanged.")
        return

    decision = load(AUTH)
    validate_gate(decision)

    manifest = load(B1 / "manifest.json")
    contract = load(B1 / "exit_contract.json")

    manifest["lesson_design_authorized"] = True
    manifest["delivery_content_production_authorized"] = False
    manifest["delivery_gate_note"] = (
        "B1 curriculum lesson design and controlled authoring planning are authorized. "
        "Lesson-package/audio/image/video production remains governed by the separate "
        "delivery workstream and does not modify or bypass TEST-002."
    )
    manifest["semantic_lock"] = {
        "status": "human_semantic_decisions_v1_plus_stage_08_5_critic_locked",
        "report": "curriculum/levels/b1/design-review/08-semantic-lock/generated/semantic-role-report.md",
        "critic": "curriculum/levels/b1/design-review/08.5-role-aware-critic/critic-decisions.md",
        "human_review_queue": 0,
        "total_primary_items": EXPECTED_TOTAL,
    }
    manifest["authorization_gate"] = {
        "status": decision["status"],
        "declaration": "curriculum/levels/b1/design-review/09-authorization-gate/authorization.json",
        "architecture": decision["architecture"],
    }
    manifest["status"] = "semantic_design_lock_reviewed_lesson_design_authorized"

    contract["status"] = "semantic_inventory_locked_v1"
    contract["inventory_obligations"] = {
        "words": "semantic_lock_v1: 240 productive/contextual; 536 receptive/contextual; 33 integrated_support",
        "phrases": "semantic_lock_v1: 128 productive/formulaic; 6 receptive/contextual; 41 integrated_support",
        "grammar": "semantic_lock_v1: 128 productive rows; 2 receptive rows; 208 integrated_support rows",
        "abilities": "semantic_lock_v1: 101 productive; 57 interactive; 66 receptive; 25 integrated_support, with mediation source mode preserved",
        "pronunciation": "semantic_lock_v1: 1 receptive; 9 integrated_support; intelligibility-first",
    }
    contract["semantic_lock"] = {
        "status": "human_semantic_decisions_v1_plus_stage_08_5_critic_locked",
        "lesson_design_authorized": True,
        "human_review_queue": 0,
        "report": "curriculum/levels/b1/design-review/08-semantic-lock/generated/semantic-role-report.md",
        "critic": "curriculum/levels/b1/design-review/08.5-role-aware-critic/critic-decisions.md",
        "completion_is_not_mastery": True,
        "receptive_does_not_imply_productive": True,
        "productive_does_not_imply_all_dictionary_senses": True,
        "mediation_source_mode_preserved": True,
    }
    contract["authorization_gate"] = {
        "status": decision["status"],
        "declaration": "curriculum/levels/b1/design-review/09-authorization-gate/authorization.json",
        "architecture": decision["architecture"],
    }
    contract["delivery_content_production_authorized"] = False
    contract["delivery_gate_note"] = manifest["delivery_gate_note"]

    write(B1 / "manifest.json", manifest)
    write(B1 / "exit_contract.json", contract)
    print(json.dumps({
        "status": manifest["status"],
        "lesson_design_authorized": True,
        "delivery_content_production_authorized": False,
        "human_review_queue": 0,
        "lesson_slots": 85,
        "total_primary_items": EXPECTED_TOTAL,
    }, indent=2))


if __name__ == "__main__":
    main()
