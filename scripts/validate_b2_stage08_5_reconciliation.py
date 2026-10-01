#!/usr/bin/env python3
"""Validate B2 Stage-8.5 role-aware lifecycle reconciliation evidence."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

TOTAL = 2075
EXPECTED = {"ability":270,"phrase":125,"grammar":243,"word":1427,"pronunciation":10}
EXPECTED_MOVES = 18
EXPECTED_ZERO_NEW = 18


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline", type=Path)
    ap.add_argument("ledger", type=Path)
    ap.add_argument("report", type=Path)
    ap.add_argument("brief_amendments", type=Path)
    ap.add_argument("active_load", type=Path)
    args = ap.parse_args()

    baseline = load(args.baseline)
    data = load(args.ledger)
    records = data.get("records", [])
    if len(records) != TOTAL or len({r["item_id"] for r in records}) != TOTAL:
        raise SystemExit("Stage-8.5 exact record count/uniqueness drift")
    if Counter(r["category"] for r in records) != Counter(EXPECTED):
        raise SystemExit("Stage-8.5 category count drift")
    if data.get("stage_08_5", {}).get("applied_exact_grammar_row_moves") != EXPECTED_MOVES:
        raise SystemExit("Stage-8.5 exact move count drift")
    if data.get("stage_08_5", {}).get("semantic_roles_changed") != 0:
        raise SystemExit("Stage-8.5 changed semantic roles")
    if data.get("stage_08_5", {}).get("semantic_homes_changed") != 0:
        raise SystemExit("Stage-8.5 changed semantic homes")
    if data.get("stage_08_5", {}).get("zero_new_slots") != EXPECTED_ZERO_NEW:
        raise SystemExit("Stage-8.5 zero-new count drift")
    if data.get("stage_08_5", {}).get("owner_human_approval_pending") is not True:
        raise SystemExit("Stage-8.5 must preserve owner approval pending")

    b = {r["item_id"]:r for r in baseline["records"]}
    moved = 0
    for r in records:
        old = b.get(r["item_id"])
        if old is None:
            raise SystemExit(f"Stage-8.5 introduced unknown record {r['item_id']}")
        if r["semantic_role"] != old["semantic_role"]:
            raise SystemExit(f"Stage-8.5 semantic-role drift {r['item_id']}")
        if r.get("homes") != old.get("homes"):
            raise SystemExit(f"Stage-8.5 semantic-home drift {r['item_id']}")
        if r["lifecycle"]["introduce"] != old["lifecycle"]["introduce"]:
            moved += 1
            if "stage_08_5_reconciliation" not in r:
                raise SystemExit(f"moved record lacks explicit reconciliation metadata {r['item_id']}")
        if not r["lifecycle"].get("fresh_retrieval"):
            raise SystemExit(f"missing fresh retrieval {r['item_id']}")
        if not r["lifecycle"].get("exit_verify"):
            raise SystemExit(f"missing exit verify {r['item_id']}")
    if moved != EXPECTED_MOVES:
        raise SystemExit(f"Stage-8.5 moved exact records {moved} != {EXPECTED_MOVES}")

    report = args.report.read_text(encoding="utf-8")
    required_report = [
        "2,075", "explicit exact grammar review-row moves applied: **18**",
        "semantic/control roles changed in Stage 8.5: **0**",
        "zero-new transfer/exit slots preserved: **18 / 18**",
        "CANDIDATE PASS", "OWNER HUMAN APPROVAL PENDING",
    ]
    for marker in required_report:
        if marker.lower() not in report.lower():
            raise SystemExit(f"Stage-8.5 report missing marker: {marker}")

    amend = args.brief_amendments.read_text(encoding="utf-8")
    if amend.count("MOVE OUT grammar review row") != EXPECTED_MOVES:
        raise SystemExit("Stage-8.5 brief overlay MOVE OUT count drift")
    if amend.count("MOVE IN grammar review row") != EXPECTED_MOVES:
        raise SystemExit("Stage-8.5 brief overlay MOVE IN count drift")
    if "AUTHORITATIVE CANDIDATE OVERLAY" not in amend:
        raise SystemExit("Stage-8.5 brief overlay authority marker missing")

    active = args.active_load.read_text(encoding="utf-8")
    rows = re.findall(r"^\| (U\d+-L\d+) \|", active, re.M)
    if len(rows) != 95 or len(set(rows)) != 95:
        raise SystemExit(f"Stage-8.5 active-load table must cover 95 lessons, got {len(rows)}")
    m = re.search(r"^\| U6-L04 \|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", active, re.M)
    if not m:
        raise SystemExit("Stage-8.5 active-load audit missing U6-L04")
    productive_grammar_rows = int(m.group(5))
    if productive_grammar_rows != 4:
        raise SystemExit(f"U6-L04 reconciled productive grammar rows {productive_grammar_rows} != 4")

    forbidden = ("lesson_design_authorized: true", "owner human approval complete", "human semantic review complete")
    blob = (report + amend + active).lower()
    for marker in forbidden:
        if marker.lower() in blob:
            raise SystemExit(f"premature Stage-8.5 claim: {marker}")

    print("B2 STAGE-08.5 RECONCILIATION VALIDATION PASS")
    print("records=2075 exact_moves=18 zero_new=18 semantic_roles_changed=0 U6-L04_productive_grammar=4 owner_approval_pending=true")


if __name__ == "__main__":
    main()
