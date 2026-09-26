#!/usr/bin/env python3
"""Produce compact human-critic views from the generated A2 coverage ledger."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "curriculum/levels/a2/design-review/06-coverage-ledger/generated/coverage-ledger.json"
OUT = ROOT / "curriculum/levels/a2/design-review/06-coverage-ledger/generated/gap-attribution.md"
LESSON_OUT = ROOT / "curriculum/levels/a2/design-review/06-coverage-ledger/generated/lesson-intro-attribution.md"


def clean_label(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def lesson_sort_key(lesson_id: str) -> tuple[int, int]:
    unit, lesson = lesson_id.split("-")
    return int(unit[1:]), int(lesson[1:])


def build_gap_view(records: list[dict]) -> list[str]:
    stages = ("practice", "fresh_retrieval", "recycle", "consolidate", "exit_verify")
    gaps = defaultdict(list)
    for r in records:
        missing = [s for s in stages if not r["lifecycle"].get(s)]
        if missing:
            key = (tuple(r.get("homes", [])), r["lifecycle"]["introduce"][0])
            gaps[key].append((r, missing))

    lines = [
        "# A2 Coverage Gap Attribution",
        "",
        "Status: **GENERATED CRITIC AID — NON-SEMANTIC**",
        "",
        "This view groups exact records that lost a required later lifecycle stage after their manually",
        "approved introduction lesson. It does not propose a fix or infer a new home.",
        "",
    ]
    stage_counts = Counter()
    for r in records:
        for stage in stages:
            if not r["lifecycle"].get(stage):
                stage_counts[stage] += 1
    lines += ["## Missing-stage counts", ""]
    for stage in stages:
        lines.append(f"- `{stage}`: **{stage_counts[stage]}**")
    lines.append("")

    for (homes, intro), items in sorted(gaps.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        lines.append(f"## {intro} — {', '.join(homes)} — {len(items)} records")
        lines.append("")
        lines.append("| Category | Item ID | Label | Missing |")
        lines.append("|---|---|---|---|")
        for r, missing in items:
            lines.append(
                f"| {r['category']} | `{r['item_id']}` | {clean_label(r.get('label'))} | {', '.join(missing)} |"
            )
        lines.append("")
    return lines


def build_lesson_view(records: list[dict]) -> list[str]:
    by_lesson: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        for lesson_id in r.get("lifecycle", {}).get("introduce", []):
            by_lesson[lesson_id].append(r)

    lines = [
        "# A2 Lesson Introduction Attribution",
        "",
        "Status: **GENERATED HUMAN-CRITIC AID — NON-SEMANTIC / NON-DECISIONAL**",
        "",
        "This file exposes the exact source records first introduced in each lesson so a human reviewer can",
        "judge cognitive coherence. It does not choose homes, semantic roles, splits, merges or sequencing.",
        "",
    ]
    category_order = ("ability", "phrase", "grammar", "word", "pronunciation")
    for lesson_id in sorted(by_lesson, key=lesson_sort_key):
        items = by_lesson[lesson_id]
        counts = Counter(r["category"] for r in items)
        lines.append(
            f"## {lesson_id} — {len(items)} introductions "
            f"(A {counts['ability']} / P {counts['phrase']} / G {counts['grammar']} / W {counts['word']} / Pron {counts['pronunciation']})"
        )
        lines.append("")
        for category in category_order:
            cat_items = [r for r in items if r["category"] == category]
            if not cat_items:
                continue
            lines.append(f"### {category.title()} — {len(cat_items)}")
            lines.append("")
            for r in cat_items:
                homes = ", ".join(r.get("homes", []))
                suffix = f" — homes: {homes}" if homes else ""
                lines.append(f"- `{r['item_id']}` — {clean_label(r.get('label'))}{suffix}")
            lines.append("")
    return lines


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    records = data["records"]

    gap_lines = build_gap_view(records)
    lesson_lines = build_lesson_view(records)
    OUT.write_text("\n".join(gap_lines), encoding="utf-8")
    LESSON_OUT.write_text("\n".join(lesson_lines), encoding="utf-8")
    print("\n".join(gap_lines[:80]))
    print(f"Wrote lesson critic aid: {LESSON_OUT}")


if __name__ == "__main__":
    main()
