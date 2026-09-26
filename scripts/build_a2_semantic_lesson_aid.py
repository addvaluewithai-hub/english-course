#!/usr/bin/env python3
"""Render the exact A2 semantic-role ledger by introduction lesson for human critic.

NON-SEMANTIC: this script only groups already-human-authored roles. It must never
change or infer a semantic role or scheduling decision.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC = ROOT / "curriculum/levels/a2/design-review/08-semantic-lock"
LEDGER = SEMANTIC / "generated/semantic-role-ledger.json"
DEFAULT_OUTPUT = SEMANTIC / "generated/lesson-semantic-attribution.md"


def lesson_key(lid: str):
    m = re.fullmatch(r"U(\d+)-L(\d+)", lid)
    return tuple(map(int, m.groups())) if m else (999, 999)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args()

    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    records = data.get("records", [])
    if len(records) != 1617:
        raise ValueError(f"semantic ledger must contain 1617 records, got {len(records)}")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        intro = record["lifecycle"]["introduce"]
        if len(intro) != 1:
            raise ValueError(f"expected one introduction lesson: {record['item_id']} -> {intro}")
        grouped[intro[0]].append(record)

    lines = [
        "# A2 Lesson Semantic Attribution",
        "",
        "Status: **GENERATED HUMAN-CRITIC AID — NON-DECISIONAL**",
        "",
        "This file groups the exact Stage-08 semantic ledger by first-introduction lesson. It exposes already human-authored roles; it does not decide roles, move items or judge load.",
        "",
    ]

    role_order = ["productive", "interactive", "receptive", "integrated_support"]
    cat_order = ["ability", "phrase", "grammar", "word", "pronunciation"]

    for lid in sorted(grouped, key=lesson_key):
        lesson = grouped[lid]
        counts = {role: sum(1 for x in lesson if x["semantic_role"]["mastery_mode"] == role) for role in role_order}
        active = counts["productive"] + counts["interactive"]
        lines += [
            f"## {lid} — {len(lesson)} source introductions / {active} active",
            "",
            f"- productive: **{counts['productive']}**",
            f"- interactive: **{counts['interactive']}**",
            f"- receptive: **{counts['receptive']}**",
            f"- integrated support: **{counts['integrated_support']}**",
            "",
        ]
        for role in role_order:
            role_records = [x for x in lesson if x["semantic_role"]["mastery_mode"] == role]
            if not role_records:
                continue
            lines += [f"### {role.replace('_', ' ').title()} — {len(role_records)}", ""]
            for category in cat_order:
                cat_records = [x for x in role_records if x["category"] == category]
                if not cat_records:
                    continue
                lines += [f"**{category.title()} — {len(cat_records)}**", ""]
                for record in cat_records:
                    role_info = record["semantic_role"]
                    extra = ""
                    if category == "grammar":
                        extra = f" — system `{record['grammar_system']}`"
                    elif "review_row" in record:
                        extra = f" — review row {record['review_row']}"
                    lines.append(
                        f"- `{record['item_id']}` — {record['label']}{extra} — `{role_info['control_scope']}` / `{role_info['exit_evidence']}`"
                    )
                lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
