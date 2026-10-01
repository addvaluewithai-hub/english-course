#!/usr/bin/env python3
"""Strict source coverage audit plus reviewed A1/A2/B1/B2 lesson-design gates.

v3 remains the historical source-coverage audit. This wrapper validates explicit
reviewed authorization for A1, A2, B1 and B2, keeps C1-C2 locked, then delegates the
unchanged source-coverage checks while masking only v3's retired assumption that
every level manifest must keep lesson design locked.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import audit_level_source_of_truth_v3 as v3

ROOT = Path(__file__).resolve().parents[1]
LOCKED_LEVELS = ("c1", "c2")


def load(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def audit_reviewed_level(
    level: str,
    auth_path: str,
    architecture: dict[str, int],
    errors: list[str],
) -> None:
    upper = level.upper()
    auth = load(auth_path)
    manifest = load(f"curriculum/levels/{level}/manifest.json")
    contract = load(f"curriculum/levels/{level}/exit_contract.json")

    if auth.get("status") != "human_lesson_design_authorization_reviewed_locked_v1":
        errors.append(f"{upper} Stage-9 authorization is not reviewed/locked")
    if auth.get("lesson_design_authorized") is not True:
        errors.append(f"{upper} Stage-9 declaration does not authorize lesson design")
    if auth.get("delivery_content_production_authorized") is not False:
        errors.append(f"{upper} Stage-9 declaration must not authorize delivery production")
    if auth.get("human_review_queue") != 0:
        errors.append(f"{upper} Stage-9 human review queue is not zero")
    auth_arch = auth.get("architecture", {})
    if {k: auth_arch.get(k) for k in architecture} != architecture:
        errors.append(f"{upper} Stage-9 architecture drift: {auth_arch}")

    if manifest.get("status") != "semantic_design_lock_reviewed_lesson_design_authorized":
        errors.append(f"{upper} manifest does not reflect reviewed Stage-9 authorization status")
    if manifest.get("lesson_design_authorized") is not True:
        errors.append(f"{upper} manifest does not authorize lesson design")
    if manifest.get("delivery_content_production_authorized") is not False:
        errors.append(f"{upper} curriculum authorization must not authorize delivery production")
    if manifest.get("semantic_lock", {}).get("human_review_queue") != 0:
        errors.append(f"{upper} manifest semantic review queue is not zero")
    if manifest.get("authorization_gate", {}).get("architecture") != architecture:
        errors.append(f"{upper} manifest authorization architecture drift")

    if contract.get("status") != "semantic_inventory_locked_v1":
        errors.append(f"{upper} exit contract is not semantically locked")
    if contract.get("semantic_lock", {}).get("lesson_design_authorized") is not True:
        errors.append(f"{upper} exit contract does not reflect lesson-design authorization")
    if contract.get("semantic_lock", {}).get("human_review_queue") != 0:
        errors.append(f"{upper} exit contract semantic review queue is not zero")
    if contract.get("delivery_content_production_authorized") is not False:
        errors.append(f"{upper} exit contract must keep delivery production unauthorized")
    if contract.get("authorization_gate", {}).get("architecture") != architecture:
        errors.append(f"{upper} exit-contract authorization architecture drift")


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

    audit_reviewed_level(
        "a2",
        "curriculum/levels/a2/design-review/10-authorization-gate/authorization.json",
        {"units": 12, "lesson_slots": 83},
        errors,
    )
    audit_reviewed_level(
        "b1",
        "curriculum/levels/b1/design-review/09-authorization-gate/authorization.json",
        {"units": 12, "lesson_slots": 85},
        errors,
    )
    audit_reviewed_level(
        "b2",
        "curriculum/levels/b2/design-review/09-authorization-gate/authorization.json",
        {"units": 13, "lesson_slots": 95},
        errors,
    )

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
        "AUTHORIZATION PASS — A1, A2, B1 and B2 reviewed lesson-design gates are locked; "
        "delivery production remains unauthorized; C1-C2 remain locked"
    )


def main() -> None:
    audit_authorization()
    original_load = v3.load

    def v3_compat_load(path: str) -> dict[str, Any]:
        data = original_load(path)
        if path in {
            "curriculum/levels/a1/manifest.json",
            "curriculum/levels/a2/manifest.json",
            "curriculum/levels/b1/manifest.json",
            "curriculum/levels/b2/manifest.json",
        }:
            data = dict(data)
            data["lesson_design_authorized"] = False
        return data

    v3.load = v3_compat_load
    v3.main()


if __name__ == "__main__":
    main()
