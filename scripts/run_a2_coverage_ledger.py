#!/usr/bin/env python3
"""Run the A2 ledger after mechanically applying explicit human lifecycle additions."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import build_a2_coverage_ledger as ledger

ROOT = Path(__file__).resolve().parents[1]
A2 = ROOT / "curriculum/levels/a2/design-review/06-coverage-ledger"
BASE = A2 / "lifecycle-plan.json"
OVERRIDES = A2 / "manual-source-overrides.json"
MERGED = Path("/tmp/a2-lifecycle-plan-merged.json")


def find_family(plan: dict, home: str) -> dict:
    if home.startswith("C"):
        return plan["capabilities"][home]
    if home.startswith("X"):
        return plan["cross_cutting"][home]
    return plan["lexical_sets"][home]


def main() -> None:
    plan = json.loads(BASE.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    merged = copy.deepcopy(plan)

    for home, stages in overrides.get("family_lifecycle_additions", {}).items():
        target = find_family(merged, home)
        for stage, lesson_ids in stages.items():
            if stage not in target or not isinstance(target[stage], list):
                raise ValueError(f"cannot add lifecycle stage {home}.{stage}")
            target[stage] = list(dict.fromkeys([*target[stage], *lesson_ids]))

    MERGED.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger.PLAN_PATH = MERGED
    ledger.main()


if __name__ == "__main__":
    main()
