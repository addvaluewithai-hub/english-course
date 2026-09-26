#!/usr/bin/env python3
"""Compact active teaching-load view from the already-built A2 semantic ledger.

NON-SEMANTIC / NON-DECISIONAL. This groups human-authored active roles only.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEM = ROOT / "curriculum/levels/a2/design-review/08-semantic-lock"
LEDGER = SEM / "generated/semantic-role-ledger.json"
OUT = SEM / "generated/active-load-aid.md"


def key(lid: str):
    m = re.fullmatch(r"U(\d+)-L(\d+)", lid)
    return tuple(map(int, m.groups())) if m else (999, 999)


def main() -> None:
    records = json.loads(LEDGER.read_text(encoding="utf-8"))["records"]
    by_lesson: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        if record["semantic_role"]["mastery_mode"] in {"productive", "interactive"}:
            by_lesson[record["lifecycle"]["introduce"][0]].append(record)

    lines = [
        "# A2 Active Load Aid",
        "",
        "Status: **GENERATED HUMAN-CRITIC AID — NON-DECISIONAL**",
        "",
        "This view hides receptive/support records and collapses productive grammar rows to distinct reviewed systems. It does not judge or move anything.",
        "",
    ]
    for lid in sorted(by_lesson, key=key):
        rows = by_lesson[lid]
        words = [x["label"] for x in rows if x["category"] == "word"]
        phrases = [x["label"] for x in rows if x["category"] == "phrase"]
        systems = sorted({x["grammar_system"] for x in rows if x["category"] == "grammar"})
        ability_homes = sorted({x["homes"][0] for x in rows if x["category"] == "ability"})
        formulaic = sum(1 for x in rows if x["semantic_role"]["control_scope"] == "formulaic")
        teaching_objects = len(words) + len(phrases) + len(systems) + len(ability_homes)
        lines += [
            f"## {lid} — approx teaching objects {teaching_objects}",
            "",
            f"- active ability homes ({len(ability_homes)}): {', '.join(ability_homes) if ability_homes else '—'}",
            f"- productive grammar systems ({len(systems)}): {', '.join(systems) if systems else '—'}",
            f"- active phrases ({len(phrases)}): {', '.join(phrases) if phrases else '—'}",
            f"- active words ({len(words)}): {', '.join(words) if words else '—'}",
            f"- formulaic active source records: {formulaic}",
            "",
        ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
