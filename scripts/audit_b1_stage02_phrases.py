#!/usr/bin/env python3
"""Validate B1 Stage-02 phrase accounting without making semantic decisions."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "curriculum/levels/b1/design-review/02-phrases"
AID = BASE / "generated/phrase-review-aid.md"
FINAL = BASE / "phrase-review.md"
EXPECTED_ROWS = set(range(1, 176))
EXPECTED_CAPABILITY_HOMES = 127
EXPECTED_CROSS_HOMES = 48


def fail(message: str) -> None:
    raise SystemExit(f"B1 STAGE-02 AUDIT FAIL — {message}")


def main() -> None:
    aid = AID.read_text(encoding="utf-8")
    final = FINAL.read_text(encoding="utf-8")

    aid_rows = {
        int(value)
        for value in re.findall(r"^\|\s*(\d+)\s*\|\s*`oxford\.phrase\.", aid, flags=re.MULTILINE)
    }
    if aid_rows != EXPECTED_ROWS:
        fail(
            f"generated phrase aid drift; missing={sorted(EXPECTED_ROWS - aid_rows)} "
            f"extra={sorted(aid_rows - EXPECTED_ROWS)}"
        )

    declarations = re.findall(r"^Rows?:\s*\*\*([^*]+)\*\*", final, flags=re.MULTILINE)
    assigned: list[int] = []
    for declaration in declarations:
        assigned.extend(int(value) for value in re.findall(r"\d+", declaration))

    counts = Counter(assigned)
    assigned_set = set(assigned)
    missing = sorted(EXPECTED_ROWS - assigned_set)
    extra = sorted(assigned_set - EXPECTED_ROWS)
    duplicates = sorted(row for row, count in counts.items() if count != 1)
    if missing or extra or duplicates:
        fail(f"row accounting mismatch; missing={missing} extra={extra} duplicates={duplicates}")

    markers = (
        "Total B1 phrases reviewed: **175 / 175**",
        f"Primary homes inside capability families: **{EXPECTED_CAPABILITY_HOMES}**",
        f"Primary homes in cross-cutting requirements: **{EXPECTED_CROSS_HOMES}**",
        "Orphans: **0**",
        "Silent exclusions: **0**",
        "New top-level capabilities created by phrase evidence: **0**",
        "**ACCEPTED FOR STAGE 03 GRAMMAR REVIEW.**",
    )
    for marker in markers:
        if marker not in final:
            fail(f"required completion marker missing: {marker}")

    print(
        "B1 STAGE-02 AUDIT PASS — 175/175 phrases accounted once; "
        "127 capability homes + 48 cross-cutting homes; 0 orphans/duplicates"
    )


if __name__ == "__main__":
    main()
