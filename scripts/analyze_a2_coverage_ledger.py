#!/usr/bin/env python3
"""Produce compact human-critic views from the generated A2 coverage ledger."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "curriculum/levels/a2/design-review/06-coverage-ledger/generated/coverage-ledger.json"
OUT = ROOT / "curriculum/levels/a2/design-review/06-coverage-ledger/generated/gap-attribution.md"


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    records = data["records"]
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
            label = str(r.get("label", "")).replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| {r['category']} | `{r['item_id']}` | {label} | {', '.join(missing)} |"
            )
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:100]))


if __name__ == "__main__":
    main()
