#!/usr/bin/env python3
"""Validate B2 Stage-08 candidate semantic/control evidence without claiming human approval."""
from __future__ import annotations
import argparse, json, re
from collections import Counter
from pathlib import Path

EXPECTED={"ability":270,"phrase":125,"grammar":243,"word":1427,"pronunciation":10}
TOTAL=2075
VALID_MASTERY={"productive","receptive","interactive","integrated_support"}
VALID_SCOPE={"generative","bounded_pattern","formulaic","contextual","quality_constraint"}
VALID_EXIT={"independent_possible","integrated_required","support_condition"}


def normalized(text: str) -> str:
    return text.replace(",", "")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("ledger",type=Path)
    ap.add_argument("report",type=Path)
    ap.add_argument("lesson_attribution",type=Path)
    ap.add_argument("active_load",type=Path)
    a=ap.parse_args()
    data=json.loads(a.ledger.read_text(encoding="utf-8"))
    records=data.get("records",[])
    if len(records)!=TOTAL: raise SystemExit(f"Stage-08 record count {len(records)} != {TOTAL}")
    if Counter(r["category"] for r in records)!=Counter(EXPECTED): raise SystemExit("Stage-08 category accounting drift")
    ids=[r["item_id"] for r in records]
    if len(set(ids))!=TOTAL: raise SystemExit("Stage-08 duplicate exact item IDs")
    if data.get("automation_inferred_semantic_roles")!=0: raise SystemExit("Stage-08 must report zero automation-inferred roles")
    if data.get("candidate_semantic_orphans")!=0: raise SystemExit("Stage-08 semantic orphans must be zero")
    if data.get("owner_human_approval_pending") is not True: raise SystemExit("Stage-08 candidate must preserve owner approval pending")
    for r in records:
        role=r.get("semantic_role",{})
        if role.get("mastery_mode") not in VALID_MASTERY: raise SystemExit(f"invalid mastery role {r['item_id']}")
        if role.get("control_scope") not in VALID_SCOPE: raise SystemExit(f"invalid scope {r['item_id']}")
        if role.get("exit_evidence") not in VALID_EXIT: raise SystemExit(f"invalid exit role {r['item_id']}")
        if "pending_stage_8" in json.dumps(role): raise SystemExit(f"pending role survived Stage-08 expansion: {r['item_id']}")
        if r.get("semantic_decision_source")!="explicit_ai_assisted_stage08_candidate_owner_approval_pending": raise SystemExit(f"invalid decision source {r['item_id']}")
        if len(r.get("lifecycle",{}).get("introduce",[]))!=1: raise SystemExit(f"lifecycle introduction changed for {r['item_id']}")
    report=a.report.read_text(encoding="utf-8")
    report_n=normalized(report)
    for marker in ("2075","candidate semantic orphans: **0**","automation-inferred semantic roles: **0**","OWNER HUMAN APPROVAL PENDING","lesson-design authorization changed: **no**"):
        if marker.lower() not in report_n.lower(): raise SystemExit(f"Stage-08 report missing marker: {marker}")
    attr=a.lesson_attribution.read_text(encoding="utf-8")
    headings=re.findall(r"^## (U\d+-L\d+)$",attr,re.M)
    if len(headings)!=95 or len(set(headings))!=95: raise SystemExit(f"Stage-08 attribution must cover 95 unique lessons, got {len(headings)}")
    attr_n=normalized(attr)
    for marker in ("exact records: **2075 / 2075**","zero-new slots unchanged: **18 / 18**"):
        if marker not in attr_n: raise SystemExit(f"Stage-08 attribution missing {marker}")
    active=a.active_load.read_text(encoding="utf-8")
    rows=re.findall(r"^\| (U\d+-L\d+) \|",active,re.M)
    if len(rows)!=95 or len(set(rows))!=95: raise SystemExit(f"active-load aid must cover 95 unique lessons, got {len(rows)}")
    if "Stage 8.5 must interpret" not in active: raise SystemExit("active-load aid must preserve mandatory Stage 8.5 gate")
    forbidden=("human semantic review complete","lesson_design_authorized: true","owner human approval complete")
    blob=(report+attr+active).lower()
    for f in forbidden:
        if f.lower() in blob: raise SystemExit(f"premature Stage-08 claim: {f}")
    print("B2 STAGE-08 SEMANTIC CANDIDATE VALIDATION PASS")
    print("records=2075 roles_complete=2075 orphans=0 lessons=95 zero_new=18 owner_approval_pending=true")

if __name__=="__main__": main()
