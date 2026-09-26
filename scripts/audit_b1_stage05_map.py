#!/usr/bin/env python3
"""Mechanically validate the reviewed B1 Stage-05 curriculum skeleton."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "curriculum/levels/b1/design-review/05-curriculum-map/curriculum-map.md"
EXPECTED_UNITS = 12
EXPECTED_LESSONS = 84
EXPECTED_ZERO_NEW = 16


def fail(message: str) -> None:
    raise SystemExit(f"B1 STAGE-05 AUDIT FAIL — {message}")


def main() -> None:
    text = MAP.read_text(encoding="utf-8")
    units = re.findall(r"^# Unit \d+ — ", text, flags=re.MULTILINE)
    lessons = re.findall(r"^### U\d+-L\d+ — ", text, flags=re.MULTILINE)
    transfer_zero = re.findall(
        r"^### U(?:1-L07|2-L07|3-L08|4-L09|5-L07|6-L07|7-L07|8-L07|9-L07|10-L06|11-L07) — ",
        text,
        flags=re.MULTILINE,
    )
    final_slots = re.findall(r"^### U12-L0[1-5] — ", text, flags=re.MULTILINE)

    if len(units) != EXPECTED_UNITS:
        fail(f"expected {EXPECTED_UNITS} units; found {len(units)}")
    if len(lessons) != EXPECTED_LESSONS:
        fail(f"expected {EXPECTED_LESSONS} lesson headings; found {len(lessons)}")
    if len(transfer_zero) + len(final_slots) != EXPECTED_ZERO_NEW:
        fail(
            f"expected {EXPECTED_ZERO_NEW} designated zero-new slots; "
            f"found {len(transfer_zero) + len(final_slots)}"
        )

    expected_ids = {
        *(f"U1-L{i:02d}" for i in range(1, 8)),
        *(f"U2-L{i:02d}" for i in range(1, 8)),
        *(f"U3-L{i:02d}" for i in range(1, 9)),
        *(f"U4-L{i:02d}" for i in range(1, 10)),
        *(f"U5-L{i:02d}" for i in range(1, 8)),
        *(f"U6-L{i:02d}" for i in range(1, 8)),
        *(f"U7-L{i:02d}" for i in range(1, 8)),
        *(f"U8-L{i:02d}" for i in range(1, 8)),
        *(f"U9-L{i:02d}" for i in range(1, 8)),
        *(f"U10-L{i:02d}" for i in range(1, 7)),
        *(f"U11-L{i:02d}" for i in range(1, 8)),
        *(f"U12-L{i:02d}" for i in range(1, 6)),
    }
    actual_ids = set(re.findall(r"^### (U\d+-L\d+) — ", text, flags=re.MULTILINE))
    if actual_ids != expected_ids:
        fail(f"lesson ID drift; missing={sorted(expected_ids - actual_ids)} extra={sorted(actual_ids - expected_ids)}")

    markers = (
        "Baseline shape emerging from manual mapping: **12 units / 84 lesson slots**",
        "**68 instructional / focused-retrieval slots**",
        "**11 unit-end fresh-transfer slots**",
        "**5 final integration / exit-evidence slots**",
        "designated zero-new slots: **16**",
        "**ACCEPTED AS THE BASELINE FOR STAGE 06 EXACT COVERAGE / LIFECYCLE MAPPING.**",
    )
    for marker in markers:
        if marker not in text:
            fail(f"required map marker missing: {marker}")

    print(
        "B1 STAGE-05 AUDIT PASS — 12 units / 84 lessons; "
        "16 designated zero-new transfer/integration slots"
    )


if __name__ == "__main__":
    main()
