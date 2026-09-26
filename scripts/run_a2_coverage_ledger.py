#!/usr/bin/env python3
"""Run the A2 ledger after mechanically applying explicit human scheduling overlays."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import build_a2_coverage_ledger as ledger

ROOT = Path(__file__).resolve().parents[1]
A2_REVIEW = ROOT / "curriculum/levels/a2/design-review"
A2 = A2_REVIEW / "06-coverage-ledger"
BASE = A2 / "lifecycle-plan.json"
OVERRIDES = A2 / "manual-source-overrides.json"
ABILITY_AID = A2_REVIEW / "01-abilities/generated/ability-review-aid.md"
MERGED = Path("/tmp/a2-lifecycle-plan-merged.json")


def find_family(plan: dict, home: str) -> dict:
    if home.startswith("C"):
        return plan["capabilities"][home]
    if home.startswith("X"):
        return plan["cross_cutting"][home]
    return plan["lexical_sets"][home]


def dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def ability_row_item_ids() -> dict[int, str]:
    """Resolve the frozen review-row numbers to exact internal ability item IDs.

    The human decision file uses stable review rows because they are what Stage 01
    was manually reviewed against. This helper performs only the mechanical join
    row -> source_record_id -> internal ability item_id; it makes no curriculum decision.
    """
    source_by_row: dict[int, str] = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|")
    for line in ABILITY_AID.read_text(encoding="utf-8").splitlines():
        m = rx.match(line)
        if m:
            source_by_row[int(m.group(1))] = m.group(2)
    if set(source_by_row) != set(range(1, 270)):
        raise ValueError("A2 ability review aid must expose exact rows 1..269")

    items = json.loads((ROOT / "curriculum/levels/a2/abilities.json").read_text(encoding="utf-8"))["items"]
    item_by_source = {
        x["source_record_id"]: x["item_id"]
        for x in items
        if x.get("curriculum_role") == "include_for_spine"
    }
    missing = sorted(set(source_by_row.values()) - set(item_by_source))
    if missing:
        raise ValueError(f"ability review sources missing from required inventory: {missing[:20]}")
    return {row: item_by_source[source] for row, source in source_by_row.items()}


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

    # Exact grammar review-row moves are human-authored. They override the older
    # Stage-06 row placement without changing system identity or semantics.
    for review_row, lesson_id in overrides.get("grammar_review_row_intro_overrides", {}).items():
        merged["grammar_review_row_intro_overrides"][str(review_row)] = lesson_id

    # Exact ability review-row moves are likewise human-authored. Translate the
    # reviewed row mechanically to the internal item ID consumed by the base builder.
    row_to_item = ability_row_item_ids()
    ability_exact = merged.setdefault("_resolved_source_intro_overrides", {}).setdefault("ability", {})
    for raw_row, lesson_id in overrides.get("ability_review_row_intro_overrides", {}).items():
        row = int(raw_row)
        if row not in row_to_item:
            raise ValueError(f"unknown A2 ability review row: {raw_row}")
        ability_exact[row_to_item[row]] = lesson_id

    # Later lifecycle evidence additions discovered by exact audit.
    for home, stages in overrides.get("family_lifecycle_additions", {}).items():
        target = find_family(merged, home)
        for stage, lesson_ids in stages.items():
            if stage not in target or not isinstance(target[stage], list):
                raise ValueError(f"cannot add lifecycle stage {home}.{stage}")
            target[stage] = dedupe([*target[stage], *lesson_ids])

    # The base builder reads exact source overrides from manual-source-overrides.json.
    # Point it at a deterministic temporary copy that includes only the mechanically
    # resolved ability IDs plus the original explicit phrase/grammar/word decisions.
    effective_overrides = copy.deepcopy(overrides)
    source_overrides = effective_overrides.setdefault("source_intro_overrides", {})
    source_overrides.setdefault("ability", {}).update(ability_exact)
    effective_overrides_path = Path("/tmp/a2-manual-source-overrides-effective.json")
    effective_overrides_path.write_text(
        json.dumps(effective_overrides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    MERGED.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger.PLAN_PATH = MERGED
    ledger.OVERRIDES_PATH = effective_overrides_path
    ledger.main()


if __name__ == "__main__":
    main()
