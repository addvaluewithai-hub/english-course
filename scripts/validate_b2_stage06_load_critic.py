#!/usr/bin/env python3
"""Validate that the B2 Stage-06 raw warning set exactly matches the reviewed critic candidate.

This does not turn raw source-row counts into mastery or human approval. It only allows
CI to distinguish a known, explicitly documented provisional load-warning set from
new/unreviewed load drift. Any warning change fails closed.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRITIC = ROOT / "curriculum/levels/b2/design-review/06-coverage-ledger/load-critic.json"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_b2_stage06_load_critic.py <coverage-report.md>")
    report_path = Path(sys.argv[1])
    report = report_path.read_text(encoding="utf-8")
    critic = json.loads(CRITIC.read_text(encoding="utf-8"))

    required_markers = [
        "Source records expanded: **2075 / 2075**",
        "- duplicate primary item IDs: **0**",
        "- records missing `introduce`: **0**",
        "- records missing `practice`: **0**",
        "- records missing `fresh_retrieval`: **0**",
        "- records missing `recycle`: **0**",
        "- records missing `consolidate`: **0**",
        "- records missing `exit_verify`: **0**",
        "**PASS — all 18 designated zero-new slots are zero-new.**",
    ]
    missing = [x for x in required_markers if x not in report]
    if missing:
        raise SystemExit(f"B2 Stage-06 structural report markers missing: {missing}")

    found = []
    rx = re.compile(r"^- (U\d+-L\d+): ([a-z]+) = (\d+) > (\d+)$", re.MULTILINE)
    for lesson, category, count, limit in rx.findall(report):
        found.append({"lesson": lesson, "category": category, "count": int(count), "limit": int(limit)})

    expected = critic.get("accepted_warnings", [])
    key = lambda x: (x["lesson"], x["category"], int(x["count"]), int(x["limit"]))
    found_keys = sorted(key(x) for x in found)
    expected_keys = sorted(key(x) for x in expected)

    if len(found) != critic.get("warning_count"):
        raise SystemExit(f"B2 Stage-06 warning count drift: report={len(found)} critic={critic.get('warning_count')}")
    if found_keys != expected_keys:
        extra = sorted(set(found_keys) - set(expected_keys))
        missing_expected = sorted(set(expected_keys) - set(found_keys))
        raise SystemExit(f"B2 Stage-06 warning-set drift. new={extra} missing={missing_expected}")

    print("B2 STAGE-06 LOAD CRITIC CANDIDATE MATCH")
    print(f"source_records=2075 warnings={len(found)} zero_new_violations=0 lifecycle_gaps=0")
    print("thresholds remain unchanged; semantic roles and owner human approval remain pending")


if __name__ == "__main__":
    main()
