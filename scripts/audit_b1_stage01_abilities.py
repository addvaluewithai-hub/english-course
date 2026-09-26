#!/usr/bin/env python3
"""Validate B1 Stage-01 ability accounting without making semantic decisions.

The human-authored final-capability-map.md is authoritative for grouping and
boundaries. This script only checks mechanical invariants: every generated
review-aid row 1..249 appears exactly once in a Source-review rows declaration,
no unknown row is introduced, expected family counts are present, and the
Stage-01 completion marker remains explicit.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "curriculum/levels/b1/design-review/01-abilities"
AID = BASE / "generated/ability-review-aid.md"
FINAL = BASE / "final-capability-map.md"
EXPECTED_ROWS = set(range(1, 250))
EXPECTED_CAPABILITIES = 20
EXPECTED_CROSS_CUTTING = 7


def fail(message: str) -> None:
    raise SystemExit(f"B1 STAGE-01 AUDIT FAIL — {message}")


def main() -> None:
    aid = AID.read_text(encoding="utf-8")
    final = FINAL.read_text(encoding="utf-8")

    aid_rows = {
        int(value)
        for value in re.findall(r"^\|\s*(\d+)\s*\|\s*`gse\.", aid, flags=re.MULTILINE)
    }
    if aid_rows != EXPECTED_ROWS:
        missing = sorted(EXPECTED_ROWS - aid_rows)
        extra = sorted(aid_rows - EXPECTED_ROWS)
        fail(f"generated review aid row drift; missing={missing} extra={extra}")

    declarations = re.findall(r"^\*\*Source-review rows:\*\*\s*([^\n]+)", final, flags=re.MULTILINE)
    if not declarations:
        fail("no Source-review rows declarations found")

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

    capabilities = re.findall(r"^## C\d{2} — ", final, flags=re.MULTILINE)
    cross_cutting = re.findall(r"^## X\d{2} — ", final, flags=re.MULTILINE)
    if len(capabilities) != EXPECTED_CAPABILITIES:
        fail(f"expected {EXPECTED_CAPABILITIES} capability families; found {len(capabilities)}")
    if len(cross_cutting) != EXPECTED_CROSS_CUTTING:
        fail(f"expected {EXPECTED_CROSS_CUTTING} cross-cutting requirements; found {len(cross_cutting)}")

    required_markers = (
        "Required ability inventory reviewed manually: **249 / 249**",
        "Capability-mapped required rows: **195**",
        "Cross-cutting required rows: **54**",
        "Silent exclusions: **0**",
        "Orphans: **0**",
        "**PASS — B1 Stage 1 is complete for phrase review.**",
    )
    for marker in required_markers:
        if marker not in final:
            fail(f"required completion marker missing: {marker}")

    print(
        "B1 STAGE-01 AUDIT PASS — 249/249 rows accounted once; "
        "20 capability families + 7 cross-cutting requirements; 0 orphans/duplicates"
    )


if __name__ == "__main__":
    main()
