#!/usr/bin/env python3
"""Build compact semantic-review context for pending A1 word decisions."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
A1 = ROOT / "curriculum/levels/a1"
LOCK = A1 / "semantic-lock"
LEDGER = A1 / "design-review/06-coverage-ledger/generated/coverage-ledger.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    compact = load(LOCK / "review-queue-compact.json")
    ledger = load(LEDGER)
    words = load(A1 / "words.json")

    pending_ids = {row["item_id"] for row in compact.get("pending", {}).get("words", [])}
    word_source = {row["item_id"]: row for row in words["items"]}
    word_ledger = {row["item_id"]: row for row in ledger["records"] if row["category"] == "word"}
    if pending_ids - set(word_source) or pending_ids - set(word_ledger):
        raise SystemExit("pending A1 word IDs do not reconcile to source inventory and coverage ledger")

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item_id in sorted(pending_ids):
        source = word_source[item_id]
        coverage = word_ledger[item_id]
        introductions = coverage.get("lifecycle", {}).get("introduce", [])
        intro = introductions[0] if introductions else "NO_INTRO"
        groups[intro].append({
            "item_id": item_id,
            "headword": source["headword"],
            "part_of_speech": source.get("part_of_speech"),
            "homes": coverage.get("homes", []),
            "introduce": introductions,
            "fresh_retrieval": coverage.get("lifecycle", {}).get("fresh_retrieval", []),
        })

    payload = {
        "schema_version": 1,
        "level": "A1",
        "pending_word_count": len(pending_ids),
        "grouping": "first_introduction_lesson",
        "group_counts": {key: len(rows) for key, rows in sorted(groups.items())},
        "groups": {key: rows for key, rows in sorted(groups.items())},
    }
    (LOCK / "word-review-context.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# A1 Pending Word Semantic Review Context",
        "",
        f"Pending words: **{len(pending_ids)}**",
        "",
        "Generated review aid only. Semantic decisions belong in reviewed decision files.",
    ]
    for lesson, rows in sorted(groups.items()):
        lines.extend(["", f"## {lesson} — {len(rows)}", "", "| Item ID | Headword | POS | Homes |", "| --- | --- | --- | --- |"])
        for row in rows:
            homes = ", ".join(row["homes"])
            lines.append(f"| `{row['item_id']}` | **{row['headword']}** | {row['part_of_speech'] or ''} | {homes} |")
    (LOCK / "word-review-context.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"pending_word_count": len(pending_ids), "group_counts": payload["group_counts"]}, indent=2))


if __name__ == "__main__":
    main()
