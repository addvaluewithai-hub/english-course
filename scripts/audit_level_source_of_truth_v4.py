#!/usr/bin/env python3
"""Strict source coverage audit plus reviewed A1/A2 lesson-design authorization gates.

v3 remains the historical source-coverage audit. This wrapper validates explicit
reviewed authorization for A1 and A2, keeps B1-C2 locked, then delegates unchanged
coverage checks while masking only v3's retired assumption that every level manifest
must keep lesson design locked.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import audit_level_source_of_truth_v3 as v3

ROOT = Path(__file__).resolve().parents[1]
LOCKED_LEVELS = ("b1", "b2", "c1", "c2")


def load(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def audit_authorization() -> None:
    errors: list[str] = []

    # A1 reviewed semantic authorization.
    a1_report = load("curriculum/levels/a1/semantic-lock/semantic-lock-report.json")
    a1_manifest = load("curriculum/levels/a1/manifest.json")
    a1_contract = load("curriculum/levels/a1/exit_contract.json")

    if a1_report.get("status") != "semantic_lock_reviewed_locked_v1":
        errors.append("A1 semantic lock is not reviewed_locked_v1")
    if a1_report.get("summary", {}).get("human_review_queue") != 0:
        errors.append("A1 semantic review queue is not zero")
    if a1_report.get("lesson_design_authorized") is not True:
        errors.append("A1 semantic report does not authorize lesson design")
    if a1_manifest.get("lesson_design_authorized") is not True:
        errors.append("A1 manifest does not authorize lesson design")
    if a1_manifest.get("delivery_content_production_authorized") is not False:
        errors.append("A1 curriculum authorization must not authorize delivery production")
    if a1_contract.get("status") != "semantic_inventory_locked_v1":
        errors.append("A1 exit contract is not semantically locked")
    if a1_contract.get("semantic_lock", {}).get("lesson_design_authorized") is not True:
        errors.append("A1 exit contract does not reflect semantic authorization")

    # A2 reviewed Stage-9 authorization. The declaration is the human decision;
    # manifest/contract are deterministic generated reflections of that decision.
    a2_auth = load(
        "curriculum/levels/a2/design-review/10-authorization-gate/authorization.json"
    )
    a2_manifest = load("curriculum/levels/a2/manifest.json")
    a2_contract = load("curriculum/levels/a2/exit_contract.json")

    if a2_auth.get("status") != "human_lesson_design_authorization_reviewed_locked_v1":
        errors.append("A2 Stage-9 authorization is not reviewed/locked")
    if a2_auth.get("lesson_design_authorized") is not True:
        errors.append("A2 Stage-9 declaration does not authorize lesson design")
    if a2_auth.get("delivery_content_production_authorized") is not False:
        errors.append("A2 Stage-9 declaration must not authorize delivery production")
    if a2_auth.get("human_review_queue") != 0:
        errors.append("A2 Stage-9 human review queue is not zero")
    if a2_auth.get("architecture") != {"units": 12, "lesson_slots": 83}:
        errors.append("A2 Stage-9 architecture is not locked at 12 units / 83 lessons")

    if a2_manifest.get("status") != "semantic_design_lock_reviewed_lesson_design_authorized":
        errors.append("A2 manifest does not reflect reviewed Stage-9 authorization status")
    if a2_manifest.get("lesson_design_authorized") is not True:
        errors.append("A2 manifest does not authorize lesson design")
    if a2_manifest.get("delivery_content_production_authorized") is not False:
        errors.append("A2 curriculum authorization must not authorize delivery production")
    if a2_manifest.get("semantic_lock", {}).get("human_review_queue") != 0:
        errors.append("A2 manifest semantic review queue is not zero")

    if a2_contract.get("status") != "semantic_inventory_locked_v1":
        errors.append("A2 exit contract is not semantically locked")
    if a2_contract.get("semantic_lock", {}).get("lesson_design_authorized") is not True:
        errors.append("A2 exit contract does not reflect lesson-design authorization")
    if a2_contract.get("semantic_lock", {}).get("human_review_queue") != 0:
        errors.append("A2 exit contract semantic review queue is not zero")
    if a2_contract.get("delivery_content_production_authorized") is not False:
        errors.append("A2 exit contract must keep delivery production unauthorized")

    # Later levels remain locked until they independently satisfy the same process.
    for level in LOCKED_LEVELS:
        other = load(f"curriculum/levels/{level}/manifest.json")
        if other.get("lesson_design_authorized") is not False:
            errors.append(f"{level}: lesson design must remain locked")

    if errors:
        print("AUTHORIZATION ERRORS")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print(
        "AUTHORIZATION PASS — A1 and A2 reviewed lesson-design gates are locked; "
        "delivery production remains unauthorized; B1-C2 remain locked"
    )


def main() -> None:
    audit_authorization()
    original_load = v3.load

    def v3_compat_load(path: str) -> dict[str, Any]:
        data = original_load(path)
        if path in {
            "curriculum/levels/a1/manifest.json",
            "curriculum/levels/a2/manifest.json",
        }:
            data = dict(data)
            data["lesson_design_authorized"] = False
        return data

    v3.load = v3_compat_load
    v3.main()


if __name__ == "__main__":
    main()
