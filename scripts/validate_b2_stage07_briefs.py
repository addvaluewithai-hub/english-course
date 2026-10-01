#!/usr/bin/env python3
"""Validate structural invariants of the B2 Stage-07 authoring-brief candidate."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "curriculum/levels/b2/design-review"
LEDGER = REVIEW / "06-coverage-ledger/generated/coverage-ledger.json"
CRITIC = REVIEW / "06-coverage-ledger/load-critic.json"

EXPECTED_ZERO_NEW = {
    "U1-L07", "U2-L07", "U3-L07", "U4-L08", "U5-L08", "U6-L07",
    "U7-L07", "U8-L07", "U9-L08", "U10-L07", "U11-L08", "U12-L08",
    "U13-L01", "U13-L02", "U13-L03", "U13-L04", "U13-L05", "U13-L06",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("briefs", type=Path)
    args = ap.parse_args()

    md = args.briefs.read_text(encoding="utf-8")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    critic = json.loads(CRITIC.read_text(encoding="utf-8"))
    warning_count = critic.get("warning_count")

    lesson_ids = re.findall(r"^###\s+(U\d+-L\d+)\s+[—-]\s+", md, flags=re.M)
    if len(lesson_ids) != 95 or len(set(lesson_ids)) != 95:
        raise SystemExit(f"Stage-07 brief headings must be 95 unique lessons, got {len(lesson_ids)} / {len(set(lesson_ids))}")

    intro_counts: dict[str, int] = {lid: 0 for lid in lesson_ids}
    for rec in ledger["records"]:
        intro = rec["lifecycle"]["introduce"]
        if len(intro) != 1:
            raise SystemExit(f"invalid Stage-06 intro ownership for {rec['item_id']}: {intro}")
        lid = intro[0]
        if lid not in intro_counts:
            raise SystemExit(f"ledger introduction references lesson absent from Stage-07 briefs: {lid}")
        intro_counts[lid] += 1

    zero_new = {lid for lid, n in intro_counts.items() if n == 0}
    if zero_new != EXPECTED_ZERO_NEW:
        raise SystemExit(f"Stage-07 zero-new set mismatch: {sorted(zero_new ^ EXPECTED_ZERO_NEW)}")

    instructional_fields = (
        "**Foreground capability evidence:**",
        "**Foreground phrase/chunk evidence:**",
        "**Foreground grammar systems:**",
        "**Lexical/content treatment:**",
        "**Embedded/support and prerequisites:**",
        "**Fresh retrieval path for today's new records:**",
        "**Provisional exit path for today's new records:**",
    )

    sections = re.split(r"(?=^###\s+U\d+-L\d+\s+[—-]\s+)", md, flags=re.M)
    parsed: dict[str, str] = {}
    for sec in sections:
        m = re.match(r"^###\s+(U\d+-L\d+)\s+[—-]\s+", sec)
        if m:
            parsed[m.group(1)] = sec

    for lid in lesson_ids:
        sec = parsed[lid]
        common = [
            "**Primary communicative/evidence outcome:**",
            "**Exact new-source load:**",
            "**Semantic / grammar boundary:**",
            "**Stage-6 load critic:**",
        ]
        for field in common:
            if field not in sec:
                raise SystemExit(f"{lid} missing required Stage-07 field {field}")
        if lid in EXPECTED_ZERO_NEW:
            for field in ("**Foreground core:**", "**Embedded/support:**", "**Prerequisites / recycled B1:**", "**Pronunciation / cross-cutting:**", "**Fresh retrieval rule:**"):
                if field not in sec:
                    raise SystemExit(f"{lid} zero-new brief missing {field}")
            if "**ZERO-NEW SLOT.**" not in sec:
                raise SystemExit(f"{lid} is zero-new but not explicitly marked")
            if not re.search(r"\*\*Exact new-source load:\*\* abilities 0 \| phrases 0 \| grammar 0 \| words 0 \| pronunciation 0 \| total 0\.", sec):
                raise SystemExit(f"{lid} zero-new exact load is not all zero")
        else:
            for field in instructional_fields:
                if field not in sec:
                    raise SystemExit(f"{lid} instructional brief missing {field}")

    warning_rows = critic.get("accepted_warnings", [])
    if warning_count != 31 or len(warning_rows) != warning_count:
        raise SystemExit(f"expected reconciled 31-row Stage-06 warning set, got count={warning_count} rows={len(warning_rows)}")
    for row in warning_rows:
        needle = f"{row['category']} {row['count']} > {row['limit']}"
        if needle not in parsed[row["lesson"]]:
            raise SystemExit(f"Stage-07 brief lost documented warning: {row['lesson']} {needle}")

    rolling = re.findall(r"^#### Rolling adversarial critic — Unit (\d+)$", md, flags=re.M)
    if rolling != [str(i) for i in range(1, 14)]:
        raise SystemExit(f"Stage-07 rolling unit critics missing or out of order: {rolling}")

    if "# Whole-level Stage-7 adversarial critic" not in md:
        raise SystemExit("missing whole-level Stage-7 adversarial critic")
    for required in (
        "lesson briefs: **95 / 95**",
        "**2,075 / 2,075**",
        "**18 / 18 protected**",
        f"**{warning_count} / {warning_count}**",
        "retain 13 units / 95 slots provisionally",
        "pending Stage 8",
    ):
        if required not in md:
            raise SystemExit(f"whole-level Stage-7 critic missing invariant: {required}")

    forbidden = (
        "lesson_design_authorized`: **true**",
        "human semantic review complete",
        "all words are productive",
        "all grammar is productive",
    )
    low = md.lower()
    for phrase in forbidden:
        if phrase.lower() in low:
            raise SystemExit(f"forbidden premature Stage-7 claim: {phrase}")

    print("B2 STAGE-07 BRIEF VALIDATION PASS")
    print(f"lesson_briefs=95 exact_records=2075 zero_new=18 warning_rows={warning_count} unit_critics=13")
    print("semantic/control roles remain pending Stage 8; owner human approval remains required")


if __name__ == "__main__":
    main()
