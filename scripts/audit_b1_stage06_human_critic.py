#!/usr/bin/env python3
"""Validate that B1 Stage-06 raw-load warnings were explicitly human-reviewed.

Mechanical load thresholds remain warnings. This gate accepts them only when the
current generated report exactly matches the pinned human critic; any drift fails.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "curriculum/levels/b1/design-review"
REPORT = REVIEW / "06-coverage-ledger/generated/coverage-report.md"
LOAD_CRITIC = REVIEW / "06-coverage-ledger/load-critic.json"
CRITIC_MD = REVIEW / "06-coverage-ledger/coverage-critic.md"
MAP = REVIEW / "05-curriculum-map/curriculum-map.md"


def fail(message: str) -> None:
    raise SystemExit(f"B1 STAGE-06 HUMAN CRITIC FAIL — {message}")


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def main() -> None:
    report = REPORT.read_text(encoding="utf-8")
    critic = json.loads(LOAD_CRITIC.read_text(encoding="utf-8"))
    critic_md = CRITIC_MD.read_text(encoding="utf-8")
    curriculum_map = MAP.read_text(encoding="utf-8")

    if critic.get("status") != "human_stage06_load_critic_reviewed_v1":
        fail("load critic status is not the reviewed Stage-06 declaration")
    actual_report_sha = git_blob_sha(REPORT)
    if actual_report_sha != critic.get("expected_coverage_report_git_blob_sha"):
        fail(
            "coverage report changed after human review; re-review required: "
            f"expected={critic.get('expected_coverage_report_git_blob_sha')} actual={actual_report_sha}"
        )

    required_report_markers = [
        "Source records expanded: **1581 / 1581**",
        "orphan source records: **0**",
        "records missing `practice`: **0**",
        "records missing `fresh_retrieval`: **0**",
        "records missing `recycle`: **0**",
        "records missing `consolidate`: **0**",
        "records missing `exit_verify`: **0**",
        "**PASS — all 16 designated transfer/integration slots are zero-new.**",
    ]
    for marker in required_report_markers:
        if marker not in report:
            fail(f"required exact-coverage marker missing: {marker}")

    warning_rx = re.compile(r"^- (U\d+-L\d+): (ability|phrase|grammar|word|pronunciation|total) = (\d+) > (\d+)$", re.MULTILINE)
    actual = [
        {"lesson": lesson, "category": category, "count": int(count), "limit": int(limit)}
        for lesson, category, count, limit in warning_rx.findall(report)
    ]
    expected = critic.get("accepted_warnings", [])
    if actual != expected:
        fail(f"raw-load warning set drifted; expected={expected} actual={actual}")

    arch = critic.get("architecture", {})
    if arch != {"units": 12, "lesson_slots": 85, "designated_zero_new_slots": 16, "decision": "retain"}:
        fail(f"unexpected architecture declaration: {arch}")
    units = re.findall(r"^# Unit \d+ — ", curriculum_map, flags=re.MULTILINE)
    lessons = re.findall(r"^### U\d+-L\d+ — ", curriculum_map, flags=re.MULTILINE)
    if len(units) != 12 or len(lessons) != 85:
        fail(f"Stage-05 architecture drift: units={len(units)} lessons={len(lessons)}")

    policy = critic.get("policy", {})
    for key in (
        "raw_source_rows_are_not_teaching_object_counts",
        "warning_thresholds_are_unchanged",
        "accepted_warnings_are_not_mastery_claims",
        "semantic_roles_must_reaudit_load_at_stage_08_5",
        "new_or_changed_warning_requires_human_rereview",
    ):
        if policy.get(key) is not True:
            fail(f"required human-load policy missing/false: {key}")

    for marker in (
        "**Retain the 12-unit / 85-slot Stage-05 architecture.**",
        "**STAGE 06 CLOSED FOR PROVISIONAL COVERAGE/LIFECYCLE DESIGN.**",
        "Stage 08.5 must re-audit",
        "Raw source rows are not equivalent to teaching objects.",
    ):
        if marker not in critic_md:
            fail(f"coverage critic marker missing: {marker}")

    print(
        "B1 STAGE-06 HUMAN CRITIC PASS — 1581/1581 exact records; 0 lifecycle gaps; "
        "16/16 zero-new protected; 15 raw-load warnings pinned and human-reviewed; 12/85 retained"
    )


if __name__ == "__main__":
    main()
