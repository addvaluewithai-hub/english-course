#!/usr/bin/env python3
"""Validate the owner-approved B2 Stage-9 curriculum-design authorization gate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B2 = ROOT / "curriculum/levels/b2"
AUTH = B2 / "design-review/09-authorization-gate/authorization.json"
MANIFEST = B2 / "manifest.json"
EXIT = B2 / "exit_contract.json"
RECONCILED = B2 / "design-review/08.5-role-reconciliation/generated/reconciled-semantic-role-ledger.json"

AUTH_STATUS = "human_lesson_design_authorization_reviewed_locked_v1"
SEM_STATUS = "owner_approved_stage08_candidate_plus_stage08_5_reconciliation_locked_v1"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    auth = load(AUTH)
    manifest = load(MANIFEST)
    exit_contract = load(EXIT)
    reconciled = load(RECONCILED)

    require(auth.get("status") == AUTH_STATUS, "Stage-9 authorization status drift")
    require(auth.get("lesson_design_authorized") is True, "Stage-9 lesson design must be authorized")
    require(auth.get("delivery_content_production_authorized") is False, "Stage-9 must not authorize delivery/media production")
    require(auth.get("human_review_queue") == 0, "Stage-9 human review queue must be zero")
    require(auth.get("owner_approval", {}).get("explicit") is True, "Stage-9 owner approval must be explicit")
    require(auth.get("owner_approval", {}).get("approved_on") == "2026-10-01", "Stage-9 owner approval date drift")
    require(auth.get("architecture") == {"units":13,"lesson_slots":95,"zero_new_transfer_exit_slots":18}, "Stage-9 architecture drift")

    evidence = auth.get("evidence_blobs", [])
    require(len(evidence) >= 9, "Stage-9 evidence blob set is unexpectedly small")
    seen = set()
    for item in evidence:
        rel = item.get("path")
        expected = item.get("git_blob_sha")
        require(isinstance(rel, str) and rel, "Stage-9 evidence path missing")
        require(rel not in seen, f"duplicate Stage-9 evidence path: {rel}")
        seen.add(rel)
        path = ROOT / rel
        require(path.exists(), f"Stage-9 evidence file missing: {rel}")
        actual = git_blob_sha(path)
        require(actual == expected, f"Stage-9 evidence blob drift: {rel} {actual} != {expected}")

    require(manifest.get("status") == "semantic_design_lock_reviewed_lesson_design_authorized", "B2 manifest authorization status drift")
    require(manifest.get("lesson_design_authorized") is True, "B2 manifest lesson_design_authorized must be true")
    require(manifest.get("delivery_content_production_authorized") is False, "B2 manifest delivery production must remain false")
    require(manifest.get("counts") == {"words":1427,"phrases":125,"grammar":243,"abilities":270,"pronunciation":10}, "B2 manifest source counts drift")
    require(manifest.get("semantic_lock", {}).get("status") == SEM_STATUS, "B2 manifest semantic lock status drift")
    require(manifest.get("semantic_lock", {}).get("human_review_queue") == 0, "B2 manifest semantic review queue must be zero")
    require(manifest.get("semantic_lock", {}).get("total_primary_items") == 2075, "B2 manifest semantic total drift")
    require(manifest.get("authorization_gate", {}).get("status") == AUTH_STATUS, "B2 manifest authorization gate drift")
    require(manifest.get("authorization_gate", {}).get("architecture") == {"units":13,"lesson_slots":95}, "B2 manifest architecture drift")

    require(exit_contract.get("status") == "semantic_inventory_locked_v1", "B2 exit contract must be semantically locked")
    require(exit_contract.get("semantic_lock", {}).get("status") == SEM_STATUS, "B2 exit semantic lock status drift")
    require(exit_contract.get("semantic_lock", {}).get("lesson_design_authorized") is True, "B2 exit contract lesson design must be authorized")
    require(exit_contract.get("semantic_lock", {}).get("human_review_queue") == 0, "B2 exit semantic review queue must be zero")
    require(exit_contract.get("authorization_gate", {}).get("status") == AUTH_STATUS, "B2 exit authorization gate drift")
    require(exit_contract.get("delivery_content_production_authorized") is False, "B2 exit delivery production must remain false")
    require(exit_contract.get("principles", {}).get("completion_is_not_mastery") is True, "completion-is-not-mastery invariant lost")
    require(exit_contract.get("principles", {}).get("retention_requires_later_fresh_evidence") is True, "fresh-evidence invariant lost")

    obligations = exit_contract.get("inventory_obligations", {})
    expected_obligations = {
        "words": "semantic_lock_v1: 369 productive/contextual; 849 receptive/contextual; 209 integrated_support",
        "phrases": "semantic_lock_v1: 92 productive/formulaic; 33 receptive/contextual",
        "grammar": "semantic_lock_v1: 165 productive rows; 78 integrated_support rows",
        "abilities": "semantic_lock_v1: 141 productive; 44 interactive; 82 receptive; 3 integrated_support, with mediation source mode preserved",
        "pronunciation": "semantic_lock_v1: 1 receptive; 9 integrated_support; intelligibility-first",
    }
    require(obligations == expected_obligations, "B2 exit semantic inventory obligation drift")

    require(reconciled.get("record_count") == 2075, "Stage-8.5 reconciled ledger record count drift")
    require(reconciled.get("candidate_semantic_orphans") == 0, "Stage-8.5 semantic orphan drift")
    require(reconciled.get("automation_inferred_semantic_roles") == 0, "Stage-8.5 automation semantic role drift")
    stage85 = reconciled.get("stage_08_5", {})
    require(stage85.get("applied_exact_grammar_row_moves") == 18, "Stage-8.5 exact move count drift")
    require(stage85.get("semantic_roles_changed") == 0, "Stage-8.5 semantic roles changed")
    require(stage85.get("semantic_homes_changed") == 0, "Stage-8.5 semantic homes changed")
    require(stage85.get("zero_new_slots") == 18, "Stage-8.5 zero-new count drift")

    gates = auth.get("gate_conditions", {})
    require(gates.get("exact_semantic_roles") == "2075/2075", "Stage-9 semantic-role gate drift")
    require(gates.get("coverage_lifecycle_gaps") == 0, "Stage-9 lifecycle gaps must be zero")
    require(gates.get("later_fresh_retrieval_gaps") == 0, "Stage-9 fresh retrieval gaps must be zero")
    require(gates.get("later_exit_verification_gaps") == 0, "Stage-9 exit verification gaps must be zero")
    require(gates.get("zero_new_transfer_exit_slots") == "18/18", "Stage-9 zero-new gate drift")
    require(gates.get("lesson_briefs") == "95/95", "Stage-9 brief gate drift")
    require(gates.get("rolling_unit_critics") == "13/13", "Stage-9 unit critic gate drift")
    require(gates.get("b1_prerequisite_unchanged") is True, "Stage-9 must preserve locked B1 prerequisite")
    require(gates.get("delivery_media_gate_remains_separate") is True, "Stage-9 must preserve separate delivery gate")

    print("B2 STAGE-09 AUTHORIZATION VALIDATION PASS")
    print("records=2075 human_review_queue=0 lesson_design_authorized=true delivery_content_production_authorized=false units=13 lessons=95 zero_new=18")


if __name__ == "__main__":
    main()
