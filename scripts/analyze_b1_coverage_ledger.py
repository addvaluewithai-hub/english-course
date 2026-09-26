#!/usr/bin/env python3
"""Report exact B1 lifecycle gaps from the generated Stage-06 ledger.

Read-only analysis. This script makes no curriculum or semantic decisions.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "curriculum/levels/b1/design-review/06-coverage-ledger/generated/coverage-ledger.json"
OUT = ROOT / "curriculum/levels/b1/design-review/06-coverage-ledger/generated/gap-attribution.md"


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    stages = ["practice", "fresh_retrieval", "recycle", "consolidate", "exit_verify"]
    lines = [
        "# B1 Stage-06 Lifecycle Gap Attribution",
        "",
        "Status: **GENERATED DIAGNOSTIC — NON-SEMANTIC**",
        "",
        "This file only identifies exact records whose generated provisional lifecycle is empty at a required stage.",
        "",
    ]
    total = 0
    for stage in stages:
        gaps = [r for r in data["records"] if not r["lifecycle"].get(stage)]
        total += len(gaps)
        lines += [f"## `{stage}` — {len(gaps)} gaps", ""]
        if not gaps:
            lines += ["None.", ""]
            continue
        lines += ["| Category | Item ID | Review/System | Homes | Intro | Label |", "|---|---|---|---|---|---|"]
        for r in gaps:
            review = r.get("grammar_system") or r.get("review_row") or ""
            homes = ", ".join(r.get("homes", []))
            intro = ", ".join(r["lifecycle"].get("introduce", []))
            label = str(r.get("label", "")).replace("|", "\\|")
            lines.append(f"| {r['category']} | `{r['item_id']}` | {review} | {homes} | {intro} | {label} |")
        lines.append("")
    lines += ["## Total", "", f"Required-stage gaps: **{total}**", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
