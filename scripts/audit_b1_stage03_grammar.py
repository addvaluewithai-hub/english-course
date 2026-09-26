#!/usr/bin/env python3
"""Validate B1 Stage-03 grammar accounting without making curriculum decisions."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "curriculum/levels/b1/design-review/03-grammar"
AID = BASE / "generated/grammar-review-aid.md"
FINAL = BASE / "grammar-review.md"
EXPECTED_ROWS = set(range(1, 339))
EXPECTED_SYSTEMS = 59


def fail(message: str) -> None:
    raise SystemExit(f"B1 STAGE-03 AUDIT FAIL — {message}")


def expand_rows(spec: str) -> list[int]:
    values: list[int] = []
    for token in re.split(r",\s*", spec.strip().rstrip(". ")):
        token = token.strip()
        if not token:
            continue
        match = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", token)
        if match:
            start, end = map(int, match.groups())
            values.extend(range(start, end + 1))
            continue
        if token.isdigit():
            values.append(int(token))
            continue
        fail(f"cannot parse review-row token: {token!r}")
    return values


def main() -> None:
    aid = AID.read_text(encoding="utf-8")
    final = FINAL.read_text(encoding="utf-8")

    aid_rows = {
        int(value)
        for value in re.findall(r"^\|\s*(\d+)\s*\|\s*\d+\s*\|", aid, flags=re.MULTILINE)
    }
    if aid_rows != EXPECTED_ROWS:
        fail(
            f"generated grammar aid drift; missing={sorted(EXPECTED_ROWS - aid_rows)} "
            f"extra={sorted(aid_rows - EXPECTED_ROWS)}"
        )

    declarations = re.findall(r"^\*\*Review rows?:\*\*\s*([^\n]+)", final, flags=re.MULTILINE)
    if len(declarations) != EXPECTED_SYSTEMS:
        fail(f"expected {EXPECTED_SYSTEMS} grammar row declarations; found {len(declarations)}")

    assigned: list[int] = []
    for declaration in declarations:
        assigned.extend(expand_rows(declaration))

    counts = Counter(assigned)
    assigned_set = set(assigned)
    missing = sorted(EXPECTED_ROWS - assigned_set)
    extra = sorted(assigned_set - EXPECTED_ROWS)
    duplicates = sorted(row for row, count in counts.items() if count != 1)
    if missing or extra or duplicates:
        fail(f"row accounting mismatch; missing={missing} extra={extra} duplicates={duplicates}")

    systems = re.findall(r"^## G\d{2} — ", final, flags=re.MULTILINE)
    if len(systems) != EXPECTED_SYSTEMS:
        fail(f"expected {EXPECTED_SYSTEMS} G systems; found {len(systems)}")

    markers = (
        "Canonical B1 EGP rows reviewed: **338 / 338**",
        "Manual usable systems / infrastructure families: **59**",
        "Source rows silently excluded: **0**",
        "Orphans: **0**",
        "Cross-cutting architecture changes: **+1** (`X08 — reference-building, noun-phrase expansion and substitution`)",
        "Architecture after Stage 03: **20 top-level capabilities + 8 cross-cutting requirements**.",
        "**ACCEPTED FOR STAGE 04 WORD / LEXICAL-CONTENT REVIEW.**",
    )
    for marker in markers:
        if marker not in final:
            fail(f"required completion marker missing: {marker}")

    print(
        "B1 STAGE-03 AUDIT PASS — 338/338 EGP rows accounted once; "
        "59 reviewed systems; architecture 20 capabilities + 8 cross-cutting"
    )


if __name__ == "__main__":
    main()
