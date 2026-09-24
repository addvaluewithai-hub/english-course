#!/usr/bin/env python3
"""Strict source coverage audit plus the reviewed A1 semantic-authorization gate.

v3 remains the historical source-coverage audit. This wrapper validates the new A1
semantic lock explicitly, then delegates the unchanged coverage checks while masking
only v3's retired assumption that every level manifest must keep lesson design locked.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import audit_level_source_of_truth_v3 as v3

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")


def load(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def audit_authorization() -> None:
    errors: list[str] = []
    report = load("curriculum/levels/a1/semantic-lock/semantic-lock-report.json")
    manifest = load("curriculum/levels/a1/manifest.json")
    contract = load("curriculum/levels/a1/exit_contract.json")

    if report.get("status") != "semantic_lock_reviewed_locked_v1":
        errors.append("A1 semantic lock is not reviewed_locked_v1")
    if report.get("summary", {}).get("human_review_queue") != 0:
        errors.append("A1 semantic review queue is not zero")
    if report.get("lesson_design_authorized") is not True:
        errors.append("A1 semantic report does not authorize lesson design")
    if manifest.get("lesson_design_authorized") is not True:
        errors.append("A1 manifest does not authorize lesson design")
    if manifest.get("delivery_content_production_authorized") is not False:
        errors.append("A1 curriculum authorization must not authorize delivery production")
    if contract.get("status") != "semantic_inventory_locked_v1":
        errors.append("A1 exit contract is not semantically locked")
    if contract.get("semantic_lock", {}).get("lesson_design_authorized") is not True:
        errors.append("A1 exit contract does not reflect semantic authorization")

    for level in LEVELS[1:]:
        other = load(f"curriculum/levels/{level}/manifest.json")
        if other.get("lesson_design_authorized") is not False:
            errors.append(f"{level}: lesson design must remain locked")

    if errors:
        print("AUTHORIZATION ERRORS")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("AUTHORIZATION PASS — A1 semantic lock reviewed; A2-C2 remain locked")


def main() -> None:
    audit_authorization()
    original_load = v3.load

    def v3_compat_load(path: str) -> dict[str, Any]:
        data = original_load(path)
        if path == "curriculum/levels/a1/manifest.json":
            data = dict(data)
            data["lesson_design_authorized"] = False
        return data

    v3.load = v3_compat_load
    v3.main()


if __name__ == "__main__":
    main()
