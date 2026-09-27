#!/usr/bin/env python3
"""Validate B1 lesson briefs against the exact reconciled lifecycle ledger."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "curriculum/levels/b1/design-review"
BRIEFS = REVIEW / "07-lesson-briefs/lesson-briefs.md"
MAP = REVIEW / "05-curriculum-map/curriculum-map.md"
LEDGER = REVIEW / "06-coverage-ledger/generated/coverage-ledger.json"

ZERO_NEW = {
    "U1-L07","U2-L07","U3-L08","U4-L09","U5-L07","U6-L07","U7-L07","U8-L07",
    "U9-L07","U10-L07","U11-L07","U12-L01","U12-L02","U12-L03","U12-L04","U12-L05",
}


def fail(message: str) -> None:
    raise SystemExit(f"B1 STAGE-07 AUDIT FAIL — {message}")


def lesson_ids(text: str) -> list[str]:
    return re.findall(r"^## (U\d+-L\d+) — ", text, flags=re.MULTILINE)


def main() -> None:
    briefs = BRIEFS.read_text(encoding="utf-8")
    curriculum = MAP.read_text(encoding="utf-8")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    map_ids = re.findall(r"^### (U\d+-L\d+) — ", curriculum, flags=re.MULTILINE)
    brief_ids = lesson_ids(briefs)
    if len(map_ids) != 85 or len(set(map_ids)) != 85:
        fail(f"Stage-05 map expected 85 unique lessons; found {len(map_ids)}/{len(set(map_ids))}")
    if brief_ids != map_ids:
        missing = [x for x in map_ids if x not in brief_ids]
        extra = [x for x in brief_ids if x not in map_ids]
        fail(f"brief lesson sequence mismatch; missing={missing} extra={extra}")

    if len(re.findall(r"^### Unit \d+ rolling critic$", briefs, flags=re.MULTILINE)) != 12:
        fail("expected exactly 12 rolling unit critics")
    if "# Whole-level Stage-07 adversarial critic" not in briefs:
        fail("whole-level critic missing")

    chunks = re.split(r"(?=^## U\d+-L\d+ — )", briefs, flags=re.MULTILINE)[1:]
    if len(chunks) != 85:
        fail(f"expected 85 brief chunks; found {len(chunks)}")
    for chunk in chunks:
        lid = re.match(r"## (U\d+-L\d+) — ", chunk).group(1)
        for field in (
            "- **Outcome:**",
            "- **Foreground candidate:**",
            "- **Embedded/support candidate:**",
            "- **Boundary:**",
            "- **Retrieval/evidence:**",
            "- **Exact introductions:**",
        ):
            if field not in chunk:
                fail(f"{lid} missing required field {field}")

    counts: dict[str, Counter] = {lid: Counter() for lid in map_ids}
    for record in ledger["records"]:
        intro = record["lifecycle"]["introduce"][0]
        counts[intro][record["category"]] += 1
        counts[intro]["total"] += 1

    rx = re.compile(
        r"^- \*\*Exact introductions:\*\* abilities \*\*(\d+)\*\* · phrases \*\*(\d+)\*\* · "
        r"grammar \*\*(\d+)\*\* · words \*\*(\d+)\*\* · pronunciation \*\*(\d+)\*\* · total \*\*(\d+)\*\*\.$",
        flags=re.MULTILINE,
    )
    parsed: dict[str, tuple[int, int, int, int, int, int]] = {}
    for chunk in chunks:
        lid = re.match(r"## (U\d+-L\d+) — ", chunk).group(1)
        m = rx.search(chunk)
        if not m:
            fail(f"{lid} exact-introduction line does not match required format")
        parsed[lid] = tuple(map(int, m.groups()))

    for lid in map_ids:
        c = counts[lid]
        expected = (c["ability"], c["phrase"], c["grammar"], c["word"], c["pronunciation"], c["total"])
        if parsed[lid] != expected:
            fail(f"{lid} brief load {parsed[lid]} != exact ledger load {expected}")

    if set(ZERO_NEW) != {lid for lid in map_ids if counts[lid]["total"] == 0}:
        fail("zero-new lesson set drifted from the 16 locked transfer/integration slots")

    for marker in (
        "**STAGE 07 CLOSED — 85 / 85 BRIEF CANDIDATES COMPLETE; 12 / 12 UNIT ROLLING CRITICS COMPLETE; WHOLE-LEVEL CRITIC COMPLETE; 12-UNIT / 85-LESSON ARCHITECTURE RETAINED.**",
        "Structural changes at Stage 07: **0**.",
        "New source introductions in designated zero-new slots: **0**.",
        "A2 modifications: **0**.",
        "U10-L02 **passes the Stage-08.5 role-aware load review**",
        "## 12. Semantic lock is now reconciled",
        "Stage 08 + Stage 08.5 are now closed across all **1,581** exact B1 source records.",
    ):
        if marker not in briefs:
            fail(f"required reconciled brief marker missing: {marker}")

    print(
        "B1 STAGE-07/08.5 BRIEF AUDIT PASS — 85/85 briefs match exact reconciled loads; "
        "12/12 rolling critics + whole-level critic present; 16/16 zero-new slots protected; "
        "role-aware feedback markers closed"
    )


if __name__ == "__main__":
    main()
