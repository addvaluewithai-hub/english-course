#!/usr/bin/env python3
"""Run the A1 coverage ledger builder with explicit manual schedule overrides.

The base lifecycle plan remains the reviewed architecture. This runner applies only
reviewed, explicit overrides from manual-source-overrides.json, invokes the deterministic
builder, then restores reviewed source files before exiting.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "curriculum/levels/a1/design-review/06-coverage-ledger/lifecycle-plan.json"
OVERRIDES = ROOT / "curriculum/levels/a1/design-review/06-coverage-ledger/manual-source-overrides.json"
WORD_REVIEW = ROOT / "curriculum/levels/a1/design-review/04-words/word-review.md"
BUILDER = ROOT / "scripts/build_a1_coverage_ledger.py"


def extend_unique(target: list, values: list) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def merge(base: dict, overrides: dict) -> dict:
    result = deepcopy(base)

    for lesson, rows in overrides.get("grammar_intro_additions", {}).items():
        extend_unique(result["grammar_intro"].setdefault(lesson, []), rows)
    for lesson, rows in overrides.get("grammar_intro_removals", {}).items():
        result["grammar_intro"][lesson] = [x for x in result["grammar_intro"].get(lesson, []) if x not in rows]

    for lesson, phrase_ids in overrides.get("phrase_intro_additions", {}).items():
        extend_unique(result["phrase_intro"].setdefault(lesson, []), phrase_ids)
    for lesson, phrase_ids in overrides.get("phrase_intro_removals", {}).items():
        result["phrase_intro"][lesson] = [x for x in result["phrase_intro"].get(lesson, []) if x not in phrase_ids]

    for home, labels in overrides.get("word_home_additions", {}).items():
        extend_unique(result["word_home_overrides"].setdefault(home, []), labels)

    for group, families in overrides.get("family_stage_additions", {}).items():
        if group not in result:
            raise KeyError(f"unknown plan group in family_stage_additions: {group}")
        for family_id, stages in families.items():
            if family_id not in result[group]:
                raise KeyError(f"unknown family in family_stage_additions: {group}.{family_id}")
            for stage, lesson_ids in stages.items():
                extend_unique(result[group][family_id].setdefault(stage, []), lesson_ids)

    for group, families in overrides.get("family_replacements", {}).items():
        if group not in result:
            raise KeyError(f"unknown plan group in family_replacements: {group}")
        for family_id, replacement in families.items():
            if family_id not in result[group]:
                raise KeyError(f"unknown family in family_replacements: {group}.{family_id}")
            result[group][family_id] = replacement

    return result


def load_builder():
    spec = importlib.util.spec_from_file_location("a1_coverage_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load A1 coverage ledger builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install_word_intro_overrides(builder, overrides: dict) -> None:
    manual = overrides.get("word_intro_label_overrides", {})
    if not manual:
        return

    original = builder.balanced_assign

    def patched(items: list, homes_by_id: dict, plan: dict, order: dict):
        assigned, primary = original(items, homes_by_id, plan, order)
        if not items or "headword_source" not in items[0]:
            return assigned, primary

        source_index = defaultdict(set)
        head_index = defaultdict(set)
        for item in items:
            if item.get("headword_source"):
                source_index[builder.canon(item["headword_source"])].add(item["item_id"])
            if item.get("headword"):
                head_index[builder.canon(item["headword"])].add(item["item_id"])

        seen = {}
        for lesson, labels in manual.items():
            if lesson not in order:
                raise ValueError(f"word intro override references unknown lesson: {lesson}")
            for label in labels:
                key = builder.canon(label)
                matches = source_index.get(key) or head_index.get(key) or set()
                if not matches:
                    raise ValueError(f"word intro override label not found: {label}")
                if len(matches) != 1:
                    raise ValueError(f"word intro override label is ambiguous: {label} -> {sorted(matches)}")
                item_id = next(iter(matches))
                if item_id in seen and seen[item_id] != lesson:
                    raise ValueError(
                        f"word intro override assigns {item_id} twice: {seen[item_id]} and {lesson}"
                    )
                seen[item_id] = lesson
                assigned[item_id] = lesson
        return assigned, primary

    builder.balanced_assign = patched


def main() -> int:
    base_plan_text = PLAN.read_text(encoding="utf-8")
    base_word_review_text = WORD_REVIEW.read_text(encoding="utf-8")
    base = json.loads(base_plan_text)
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    merged = merge(base, overrides)

    compatible_word_review = base_word_review_text.replace(
        "# Cross-domain high-frequency lexical pool",
        "# Remaining general high-frequency lexical material",
    )

    PLAN.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    WORD_REVIEW.write_text(compatible_word_review, encoding="utf-8")
    try:
        builder = load_builder()
        install_word_intro_overrides(builder, overrides)
        try:
            builder.main()
            return 0
        except SystemExit as exc:
            return int(exc.code or 0)
    finally:
        PLAN.write_text(base_plan_text, encoding="utf-8")
        WORD_REVIEW.write_text(base_word_review_text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
