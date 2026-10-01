#!/usr/bin/env python3
"""Deterministically finalize the owner-approved B2 Stage-9 curriculum-design state.

This script changes authorization metadata only. It must not alter canonical B2 source
inventories, semantic roles, Stage-8.5 lifecycle moves, B1, or delivery/media gates.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B2 = ROOT / "curriculum/levels/b2"
AUTH = B2 / "design-review/09-authorization-gate/authorization.json"
MANIFEST = B2 / "manifest.json"
EXIT = B2 / "exit_contract.json"

AUTH_STATUS = "human_lesson_design_authorization_reviewed_locked_v1"
SEM_STATUS = "owner_approved_stage08_candidate_plus_stage08_5_reconciliation_locked_v1"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    auth = load(AUTH)
    if auth.get("status") != AUTH_STATUS:
        raise SystemExit("B2 Stage-9 authorization declaration is not locked")
    if auth.get("lesson_design_authorized") is not True:
        raise SystemExit("B2 Stage-9 declaration does not authorize lesson design")
    if auth.get("delivery_content_production_authorized") is not False:
        raise SystemExit("B2 Stage-9 must not authorize delivery/media production")
    if auth.get("human_review_queue") != 0:
        raise SystemExit("B2 Stage-9 human review queue must be zero")
    if auth.get("owner_approval", {}).get("explicit") is not True:
        raise SystemExit("B2 Stage-9 requires explicit owner approval")
    if auth.get("architecture") != {"units": 13, "lesson_slots": 95, "zero_new_transfer_exit_slots": 18}:
        raise SystemExit("B2 Stage-9 architecture declaration drift")

    manifest = load(MANIFEST)
    manifest["status"] = "semantic_design_lock_reviewed_lesson_design_authorized"
    manifest["lesson_design_authorized"] = True
    manifest["delivery_content_production_authorized"] = False
    manifest["delivery_gate_note"] = (
        "B2 curriculum lesson design and controlled authoring planning are authorized. "
        "Lesson-package/audio/image/video production remains governed by the separate "
        "delivery workstream and is not authorized by this curriculum-design gate."
    )
    manifest["semantic_lock"] = {
        "status": SEM_STATUS,
        "report": "curriculum/levels/b2/design-review/08-semantic-lock/generated/semantic-role-report.md",
        "critic": "curriculum/levels/b2/design-review/08.5-role-reconciliation/generated/role-aware-reconciliation-report.md",
        "human_review_queue": 0,
        "total_primary_items": 2075,
    }
    manifest["authorization_gate"] = {
        "status": AUTH_STATUS,
        "declaration": "curriculum/levels/b2/design-review/09-authorization-gate/authorization.json",
        "architecture": {"units": 13, "lesson_slots": 95},
    }
    write(MANIFEST, manifest)

    exit_contract = load(EXIT)
    exit_contract["status"] = "semantic_inventory_locked_v1"
    exit_contract["inventory_obligations"] = {
        "words": "semantic_lock_v1: 369 productive/contextual; 849 receptive/contextual; 209 integrated_support",
        "phrases": "semantic_lock_v1: 92 productive/formulaic; 33 receptive/contextual",
        "grammar": "semantic_lock_v1: 165 productive rows; 78 integrated_support rows",
        "abilities": "semantic_lock_v1: 141 productive; 44 interactive; 82 receptive; 3 integrated_support, with mediation source mode preserved",
        "pronunciation": "semantic_lock_v1: 1 receptive; 9 integrated_support; intelligibility-first",
    }
    exit_contract["semantic_lock"] = {
        "status": SEM_STATUS,
        "lesson_design_authorized": True,
        "human_review_queue": 0,
        "report": "curriculum/levels/b2/design-review/08-semantic-lock/generated/semantic-role-report.md",
        "critic": "curriculum/levels/b2/design-review/08.5-role-reconciliation/generated/role-aware-reconciliation-report.md",
        "completion_is_not_mastery": True,
        "receptive_does_not_imply_productive": True,
        "productive_does_not_imply_all_dictionary_senses": True,
        "mediation_source_mode_preserved": True,
    }
    exit_contract["authorization_gate"] = {
        "status": AUTH_STATUS,
        "declaration": "curriculum/levels/b2/design-review/09-authorization-gate/authorization.json",
        "architecture": {"units": 13, "lesson_slots": 95},
    }
    exit_contract["delivery_content_production_authorized"] = False
    exit_contract["delivery_gate_note"] = (
        "B2 curriculum lesson design and controlled authoring planning are authorized. "
        "Lesson-package/audio/image/video production remains governed by the separate "
        "delivery workstream and is not authorized by this curriculum-design gate."
    )
    write(EXIT, exit_contract)

    print("B2 STAGE-09 AUTHORIZATION FINALIZER PASS")
    print("lesson_design_authorized=true human_review_queue=0 delivery_content_production_authorized=false units=13 lessons=95")


if __name__ == "__main__":
    main()
