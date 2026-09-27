#!/usr/bin/env python3
"""Run the B1 exact lifecycle ledger with reviewed scheduling overlays.

NON-SEMANTIC wrapper. Stage 06 remains the frozen family/system scheduling base.
Stage 08.5 may add exact human critic moves after that base assignment so fixing one
record cannot mechanically reshuffle unrelated records. Automation only validates
and applies declared moves, then delegates to `build_b1_coverage_ledger.py`.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import build_b1_coverage_ledger as ledger

ROOT = Path(__file__).resolve().parents[1]
B1_REVIEW = ROOT / "curriculum/levels/b1/design-review"
STAGE06 = B1_REVIEW / "06-coverage-ledger"
BASE = STAGE06 / "lifecycle-plan.json"
OVERRIDES = STAGE06 / "manual-source-overrides.json"
CRITIC = B1_REVIEW / "08.5-role-aware-critic/overrides.json"
MERGED = Path("/tmp/b1-lifecycle-plan-merged.json")


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
    critic = json.loads(CRITIC.read_text(encoding="utf-8")) if CRITIC.exists() else {"scheduling": {}}
    merged = copy.deepcopy(plan)

    for home, lesson_ids in overrides.get("family_intro_replacements", {}).items():
        find_family(merged, home)["introduce"] = dedupe(lesson_ids)
    for home, lesson_ids in overrides.get("family_intro_additions", {}).items():
        target = find_family(merged, home)
        target["introduce"] = dedupe([*target["introduce"], *lesson_ids])

    for system, lesson_ids in overrides.get("grammar_system_intro_replacements", {}).items():
        if system not in merged["grammar_system_intro"]:
            raise ValueError(f"unknown B1 grammar system intro replacement: {system}")
        merged["grammar_system_intro"][system] = dedupe(lesson_ids)
    for system, lesson_ids in overrides.get("grammar_system_intro_additions", {}).items():
        if system not in merged["grammar_system_intro"]:
            raise ValueError(f"unknown B1 grammar system intro addition: {system}")
        merged["grammar_system_intro"][system] = dedupe([
            *merged["grammar_system_intro"][system], *lesson_ids
        ])

    for home, stages in overrides.get("family_lifecycle_additions", {}).items():
        target = find_family(merged, home)
        for stage, lesson_ids in stages.items():
            if stage not in target or not isinstance(target[stage], list):
                raise ValueError(f"cannot add B1 lifecycle stage {home}.{stage}")
            target[stage] = dedupe([*target[stage], *lesson_ids])

    scheduling = critic.get("scheduling", {})
    ability_moves = {int(k): v for k, v in scheduling.get("ability_review_row_intro_overrides", {}).items()}
    phrase_moves = {int(k): v for k, v in scheduling.get("phrase_review_row_intro_overrides", {}).items()}
    grammar_moves = {int(k): v for k, v in scheduling.get("grammar_review_row_intro_overrides", {}).items()}
    word_moves = dict(scheduling.get("word_item_intro_overrides", {}))

    curriculum_text = ledger.text(B1_REVIEW / "05-curriculum-map/curriculum-map.md")
    allowed_lessons = set(ledger.lesson_ids(curriculum_text))
    if len(allowed_lessons) != 85:
        raise ValueError(f"B1 Stage-08.5 scheduling expected 85 lesson IDs, got {len(allowed_lessons)}")
    for group, moves in (
        ("ability", ability_moves),
        ("phrase", phrase_moves),
        ("grammar", grammar_moves),
        ("word", word_moves),
    ):
        bad_targets = sorted({lesson for lesson in moves.values() if lesson not in allowed_lessons})
        if bad_targets:
            raise ValueError(f"B1 Stage-08.5 {group} move references unknown lesson(s): {bad_targets}")

    original_build_record = ledger.build_record
    applied_ability: set[int] = set()
    applied_phrase: set[int] = set()
    applied_grammar: set[int] = set()
    applied_word: set[str] = set()

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
        row = int(extra["review_row"]) if extra and "review_row" in extra else None
        override = None
        if category == "ability" and row in ability_moves:
            override = ability_moves[row]
            applied_ability.add(row)
        elif category == "phrase" and row in phrase_moves:
            override = phrase_moves[row]
            applied_phrase.add(row)
        elif category == "grammar" and row in grammar_moves:
            override = grammar_moves[row]
            applied_grammar.add(row)
        elif category == "word" and item["item_id"] in word_moves:
            override = word_moves[item["item_id"]]
            applied_word.add(item["item_id"])
        if override is not None:
            intro = override
        record = original_build_record(category, item, label, homes, intro, effective_plan, order, extra)
        if override is not None:
            record["stage_08_5_scheduling_override"] = True
        return record

    MERGED.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger.PLAN_PATH = MERGED
    ledger.build_record = build_record_with_stage_08_5
    ledger.main()

    expected_applied = {
        "ability": set(ability_moves),
        "phrase": set(phrase_moves),
        "grammar": set(grammar_moves),
        "word": set(word_moves),
    }
    actual_applied = {
        "ability": applied_ability,
        "phrase": applied_phrase,
        "grammar": applied_grammar,
        "word": applied_word,
    }
    for category in expected_applied:
        if expected_applied[category] != actual_applied[category]:
            raise ValueError(
                f"B1 Stage-08.5 {category} scheduling application mismatch: "
                f"expected={sorted(expected_applied[category])} actual={sorted(actual_applied[category])}"
            )


if __name__ == "__main__":
    main()
