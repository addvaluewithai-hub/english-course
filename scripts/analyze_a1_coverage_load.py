#!/usr/bin/env python3
"""Explain A1 introduction load by manually reviewed curriculum home.

This is diagnostic only. It never assigns or changes semantic homes.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "curriculum/levels/a1/design-review"
PLAN_PATH = REVIEW / "06-coverage-ledger/lifecycle-plan.json"
OVERRIDES_PATH = REVIEW / "06-coverage-ledger/manual-source-overrides.json"
LEDGER_PATH = REVIEW / "06-coverage-ledger/generated/coverage-ledger.json"
MAP_PATH = REVIEW / "05-curriculum-map/curriculum-map.md"
OUT_PATH = REVIEW / "06-coverage-ledger/generated/load-attribution.md"


def extend_unique(target: list, values: list) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def merged_plan() -> dict:
    base = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    ov = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    result = deepcopy(base)
    for group, families in ov.get("family_stage_additions", {}).items():
        for family_id, stages in families.items():
            for stage, lesson_ids in stages.items():
                extend_unique(result[group][family_id].setdefault(stage, []), lesson_ids)
    for group, families in ov.get("family_replacements", {}).items():
        for family_id, replacement in families.items():
            result[group][family_id] = replacement
    return result


def lesson_order() -> dict[str, int]:
    text = MAP_PATH.read_text(encoding="utf-8")
    seen = []
    for lid in re.findall(r"\|\s*(U\d+-L\d+)\s*\|", text):
        if lid not in seen:
            seen.append(lid)
    return {lid: i for i, lid in enumerate(seen)}


def family(plan: dict, home: str) -> dict:
    if home.startswith("C"):
        return plan["capabilities"][home]
    if home.startswith("X"):
        return plan["cross_cutting"][home]
    return plan["lexical_sets"][home]


def chosen_home(record: dict, plan: dict, order: dict[str, int]) -> str:
    homes = record["homes"]
    return min(homes, key=lambda h: min(order[x] for x in family(plan, h)["introduce"]))


def main() -> None:
    plan = merged_plan()
    order = lesson_order()
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    per_lesson = defaultdict(lambda: defaultdict(Counter))
    labels = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for record in ledger["records"]:
        lesson = record["lifecycle"]["introduce"][0]
        category = record["category"]
        if category in {"word", "ability"}:
            home = chosen_home(record, plan, order)
        else:
            home = record["homes"][0] if record["homes"] else "UNMAPPED"
        per_lesson[lesson][category][home] += 1
        labels[lesson][category][home].append(record["label"])

    lines = [
        "# A1 Introduction Load Attribution",
        "",
        "Diagnostic only. Counts show which already-reviewed semantic home generated each introduction; this file makes no curriculum decisions.",
        "",
    ]
    for lesson in sorted(order, key=order.get):
        total = sum(sum(c.values()) for c in per_lesson[lesson].values())
        words = sum(per_lesson[lesson]["word"].values())
        abilities = sum(per_lesson[lesson]["ability"].values())
        grammar = sum(per_lesson[lesson]["grammar"].values())
        phrases = sum(per_lesson[lesson]["phrase"].values())
        if not (words > 24 or abilities > 8 or grammar > 8 or phrases > 14 or total > 42):
            continue
        lines += [f"## {lesson} — total {total}", ""]
        for category in ("ability", "phrase", "grammar", "word", "pronunciation"):
            counter = per_lesson[lesson][category]
            if not counter:
                continue
            lines.append(f"### {category} — {sum(counter.values())}")
            for home, count in counter.most_common():
                sample = ", ".join(f"`{x}`" for x in labels[lesson][category][home][:12])
                lines.append(f"- **{home}: {count}** — {sample}")
            lines.append("")

    OUT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(OUT_PATH)


if __name__ == "__main__":
    main()
