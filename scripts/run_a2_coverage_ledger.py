#!/usr/bin/env python3
"""Run the A2 ledger after mechanically applying explicit human scheduling overlays."""
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


def dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def main() -> None:
    plan = json.loads(BASE.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    merged = copy.deepcopy(plan)

    # Human-approved family introduction windows. Replacements remove a poor
    # original scheduling window; additions broaden a valid home across natural lessons.
    for home, lesson_ids in overrides.get("family_intro_replacements", {}).items():
        find_family(merged, home)["introduce"] = dedupe(lesson_ids)
    for home, lesson_ids in overrides.get("family_intro_additions", {}).items():
        target = find_family(merged, home)
        target["introduce"] = dedupe([*target["introduce"], *lesson_ids])

    # Equivalent explicit scheduling overlays for reviewed grammar systems.
    for system, lesson_ids in overrides.get("grammar_system_intro_replacements", {}).items():
        if system not in merged["grammar_system_intro"]:
            raise ValueError(f"unknown grammar system intro replacement: {system}")
        merged["grammar_system_intro"][system] = dedupe(lesson_ids)
    for system, lesson_ids in overrides.get("grammar_system_intro_additions", {}).items():
        if system not in merged["grammar_system_intro"]:
            raise ValueError(f"unknown grammar system intro addition: {system}")
        merged["grammar_system_intro"][system] = dedupe([
            *merged["grammar_system_intro"][system], *lesson_ids
        ])

    # Later lifecycle evidence additions discovered by exact audit.
    for home, stages in overrides.get("family_lifecycle_additions", {}).items():
        target = find_family(merged, home)
        for stage, lesson_ids in stages.items():
            if stage not in target or not isinstance(target[stage], list):
                raise ValueError(f"cannot add lifecycle stage {home}.{stage}")
            target[stage] = dedupe([*target[stage], *lesson_ids])

    MERGED.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger.PLAN_PATH = MERGED
    ledger.main()


if __name__ == "__main__":
    main()
