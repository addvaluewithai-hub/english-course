#!/usr/bin/env python3
"""Run the A2 ledger after mechanically applying explicit human scheduling overlays.

Stage 06 is the frozen reviewed assignment layer. Stage 08.5 exact critic moves are
applied *after* that assignment so moving one item cannot shift unrelated records
inside a round-robin family window.
"""
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
CRITIC_OVERRIDES = A2_REVIEW / "08.5-role-aware-critic/overrides.json"
ABILITY_AID = A2_REVIEW / "01-abilities/generated/ability-review-aid.md"
PHRASE_AID = A2_REVIEW / "02-phrases/generated/phrase-review-aid.md"
GRAMMAR_AID = A2_REVIEW / "03-grammar/generated/grammar-review-aid.md"
WORD_AID = A2_REVIEW / "04-words/generated/word-review-aid.md"
MERGED = Path("/tmp/a2-lifecycle-plan-merged.json")


def find_family(plan: dict, home: str) -> dict:
    if home.startswith("C"):
        return plan["capabilities"][home]
    if home.startswith("X"):
        return plan["cross_cutting"][home]
    return plan["lexical_sets"][home]


def dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def table_row_ids(path: Path, expected_count: int) -> dict[int, str]:
    """Resolve review-aid table row numbers to the exact ID in column two."""
    result: dict[int, str] = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|")
    for line in path.read_text(encoding="utf-8").splitlines():
        m = rx.match(line)
        if m:
            result[int(m.group(1))] = m.group(2)
    expected = set(range(1, expected_count + 1))
    if set(result) != expected:
        missing = sorted(expected - set(result))
        extra = sorted(set(result) - expected)
        raise ValueError(
            f"review aid {path} must expose exact rows 1..{expected_count}; "
            f"missing={missing[:20]} extra={extra[:20]}"
        )
    return result


def ability_row_item_ids() -> dict[int, str]:
    """Resolve frozen ability review rows to exact internal ability item IDs."""
    source_by_row = table_row_ids(ABILITY_AID, 269)
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


def grammar_row_item_ids() -> dict[int, str]:
    """Resolve grammar review rows -> EGP spreadsheet rows -> exact item IDs."""
    review_to_sheet: dict[int, int] = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|")
    for line in GRAMMAR_AID.read_text(encoding="utf-8").splitlines():
        m = rx.match(line)
        if m:
            review_to_sheet[int(m.group(1))] = int(m.group(2))
    if set(review_to_sheet) != set(range(1, 292)):
        raise ValueError("A2 grammar review aid must expose exact rows 1..291")

    items = json.loads((ROOT / "curriculum/levels/a2/grammar.json").read_text(encoding="utf-8"))["items"]
    item_by_sheet = {int(x["source_ref"]["spreadsheet_row"]): x["item_id"] for x in items}
    missing = sorted(set(review_to_sheet.values()) - set(item_by_sheet))
    if missing:
        raise ValueError(f"grammar review spreadsheet rows missing canonical items: {missing[:20]}")
    return {row: item_by_sheet[sheet] for row, sheet in review_to_sheet.items()}


def resolve_review_row_overrides(
    row_overrides: dict[str, str],
    row_to_item: dict[int, str],
    *,
    label: str,
) -> dict[str, str]:
    resolved: dict[str, str] = {}
    for raw_row, lesson_id in row_overrides.items():
        row = int(raw_row)
        if row not in row_to_item:
            raise ValueError(f"unknown A2 {label} review row: {raw_row}")
        resolved[row_to_item[row]] = lesson_id
    return resolved


def main() -> None:
    plan = json.loads(BASE.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    critic = (
        json.loads(CRITIC_OVERRIDES.read_text(encoding="utf-8"))
        if CRITIC_OVERRIDES.exists()
        else {"scheduling": {}}
    )
    critic_schedule = critic.get("scheduling", {})
    merged = copy.deepcopy(plan)

    # Frozen human-approved Stage-06 family introduction windows.
    for home, lesson_ids in overrides.get("family_intro_replacements", {}).items():
        find_family(merged, home)["introduce"] = dedupe(lesson_ids)
    for home, lesson_ids in overrides.get("family_intro_additions", {}).items():
        target = find_family(merged, home)
        target["introduce"] = dedupe([*target["introduce"], *lesson_ids])

    # Frozen Stage-06 reviewed grammar-system windows.
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

    # Exact Stage-06 grammar review-row moves remain part of the frozen base.
    for review_row, lesson_id in overrides.get("grammar_review_row_intro_overrides", {}).items():
        merged["grammar_review_row_intro_overrides"][str(review_row)] = lesson_id

    # Exact Stage-06 ability routing is mechanically joined to internal item IDs.
    row_to_ability = ability_row_item_ids()
    ability_exact = merged.setdefault("_resolved_source_intro_overrides", {}).setdefault("ability", {})
    for raw_row, lesson_id in overrides.get("ability_review_row_intro_overrides", {}).items():
        row = int(raw_row)
        if row not in row_to_ability:
            raise ValueError(f"unknown A2 ability review row: {raw_row}")
        ability_exact[row_to_ability[row]] = lesson_id

    # Stage-06 later lifecycle evidence additions.
    for home, stages in overrides.get("family_lifecycle_additions", {}).items():
        target = find_family(merged, home)
        for stage, lesson_ids in stages.items():
            if stage not in target or not isinstance(target[stage], list):
                raise ValueError(f"cannot add lifecycle stage {home}.{stage}")
            target[stage] = dedupe([*target[stage], *lesson_ids])

    # Stage 08.5 may add later evidence after moving an exact item. These additions
    # alter lifecycle evidence only; they do not change semantic homes.
    for home, stages in critic_schedule.get("family_lifecycle_additions", {}).items():
        target = find_family(merged, home)
        for stage, lesson_ids in stages.items():
            if stage not in target or not isinstance(target[stage], list):
                raise ValueError(f"cannot add Stage-08.5 lifecycle stage {home}.{stage}")
            target[stage] = dedupe([*target[stage], *lesson_ids])

    # Build the effective Stage-06 source override file. Stage-08.5 exact moves are
    # deliberately NOT inserted here because balanced_assignment would then shift
    # unrelated records. They are applied post-assignment below.
    effective_overrides = copy.deepcopy(overrides)
    source_overrides = effective_overrides.setdefault("source_intro_overrides", {})
    source_overrides.setdefault("ability", {}).update(ability_exact)
    effective_overrides_path = Path("/tmp/a2-manual-source-overrides-effective.json")
    effective_overrides_path.write_text(
        json.dumps(effective_overrides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Resolve the later human critic rows to exact IDs. Applying these through a
    # build_record wrapper preserves every unrelated Stage-06 assignment.
    critic_exact: dict[str, dict[str, str]] = {
        "phrase": resolve_review_row_overrides(
            critic_schedule.get("phrase_review_row_intro_overrides", {}),
            table_row_ids(PHRASE_AID, 176),
            label="phrase",
        ),
        "grammar": resolve_review_row_overrides(
            critic_schedule.get("grammar_review_row_intro_overrides", {}),
            grammar_row_item_ids(),
            label="grammar",
        ),
        "word": resolve_review_row_overrides(
            critic_schedule.get("word_review_row_intro_overrides", {}),
            table_row_ids(WORD_AID, 871),
            label="word",
        ),
    }

    original_build_record = ledger.build_record

    def build_record_with_stage_08_5(
        category: str,
        item: dict,
        label: str,
        homes: list[str],
        intro: str,
        effective_plan: dict,
        order: dict[str, int],
        extra: dict | None = None,
    ) -> dict:
        override = critic_exact.get(category, {}).get(item["item_id"])
        if override is not None:
            intro = override
        return original_build_record(category, item, label, homes, intro, effective_plan, order, extra)

    MERGED.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger.PLAN_PATH = MERGED
    ledger.OVERRIDES_PATH = effective_overrides_path
    ledger.build_record = build_record_with_stage_08_5
    ledger.main()


if __name__ == "__main__":
    main()
