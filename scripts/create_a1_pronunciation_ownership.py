"""Build exact A1 pronunciation targets, risks, and provisional owners."""

from __future__ import annotations

import copy
import json
from collections import Counter, defaultdict

from scripts.a1_pronunciation_ownership_contract import (
    INPUTS, OUTPUT, PROGRESSION, REPORT, REVIEWED_AT, REVIEWER, ROOT, WORKLIST,
)
from scripts.a1_pronunciation_ownership_report import render
from scripts.a1_pronunciation_target_catalog import TARGETS
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _targets(progression: dict) -> list[dict]:
    strands = {row["strand_id"]: row for row in progression["strands"]}
    rows = []
    for source in TARGETS:
        row = copy.deepcopy(source)
        stage = next(item for item in strands[row["strand_id"]]["stages"] if item["level"] == "a1")
        row["source_refs"] = stage["representative_cefr_evidence_ids"]
        row["level_expectation"] = stage["expectation"]
        row["review"] = {"status": "accepted_for_a1_reconciliation", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT}
        rows.append(row)
    return rows


def _risk_rows(progression: dict, targets: list[dict]) -> list[dict]:
    owners = defaultdict(list)
    for target in targets:
        for risk_id in target["arabic_risk_hypothesis_ids"]:
            owners[risk_id].append(target["target_id"])
    rows = []
    for source in progression["arabic_learner_risk_hypotheses"]:
        target_ids = sorted(owners[source["risk_id"]])
        rows.append({
            "risk_id": source["risk_id"], "strand_id": source["strand_id"],
            "statement": source["statement"], "universality": source["universality"],
            "validation_route": source["validation_route"], "selected_target_ids": target_ids,
            "disposition": "selected_monitor_target" if target_ids else "monitor_if_observed_not_pre_taught",
            "rationale": "Target only after task impact or learner observation; never infer need from Arabic identity alone."
            if target_ids else "No current high-value A1 outcome justifies pre-teaching; never infer the need from identity, and add support only if observed.",
        })
    return rows


def _candidate_rows(worklist: dict, targets: list[dict]) -> list[dict]:
    ownership = defaultdict(list)
    for target in targets:
        for location in [target["introduction_location"]] + target["recycle_locations"]:
            if location.startswith("lesson_candidate."):
                ownership[location].append(target["target_id"])
    rows = []
    for candidate in worklist["candidates"]:
        legacy = candidate["current_language_targets"]["pronunciation"]
        if legacy:
            rows.append({
                "candidate_id": candidate["candidate_id"], "legacy_pronunciation_targets": legacy,
                "exact_target_ids": sorted(set(ownership[candidate["candidate_id"]])),
            })
    return rows


def build() -> dict:
    progression, worklist = _load(PROGRESSION), _load(WORKLIST)
    targets = _targets(progression)
    risks = _risk_rows(progression, targets)
    candidates = _candidate_rows(worklist, targets)
    known_candidates = {row["candidate_id"] for row in worklist["candidates"]}
    known_strands = {row["strand_id"] for row in progression["strands"]}
    known_risks = {row["risk_id"] for row in progression["arabic_learner_risk_hypotheses"]}
    locations = {value for row in targets for value in [row["introduction_location"]] + row["recycle_locations"]}
    used_strands = {row["strand_id"] for row in targets}
    used_risks = {risk_id for row in targets for risk_id in row["arabic_risk_hypothesis_ids"]}
    expected_candidates = {
        row["candidate_id"] for row in worklist["candidates"]
        if row["current_language_targets"]["pronunciation"]
    }
    covered_candidates = {row["candidate_id"] for row in candidates if row["exact_target_ids"]}
    risk_counts = Counter(row["disposition"] for row in risks)
    return {
        "schema_version": 1, "dataset_id": "a1_pronunciation_ownership", "version": 1,
        "inputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)} for path in INPUTS],
        "policy": {
            "goal": "Maximise intelligibility, accurate key-detail transfer, listening recognition, and successful repair; never remove an accent.",
            "reference_model": "General American broad IPA supports consistent course models and SSML authoring but is not an imitation target.",
            "variation": "Accept stable intelligible English varieties and learner pronunciations when the intended word, contrast, and interaction remain clear.",
            "risk_use": "Arabic-learner risks are dialect-sensitive hypotheses requiring observation; they are not facts about an individual learner.",
        },
        "targets": targets, "risk_dispositions": risks, "candidate_ownership": candidates,
        "audit": {
            "target_count": len(targets), "strand_count": len(used_strands),
            "control_status_counts": dict(sorted(Counter(row["control_status"] for row in targets).items())),
            "arabic_risk_hypothesis_count": len(risks), "risk_disposition_counts": dict(sorted(risk_counts.items())),
            "legacy_pronunciation_candidate_count": len(expected_candidates),
            "uncovered_pronunciation_candidate_ids": sorted(expected_candidates - covered_candidates),
            "uncovered_strand_ids": sorted(known_strands - used_strands),
            "unknown_strand_ids": sorted(used_strands - known_strands),
            "unknown_risk_ids": sorted(used_risks - known_risks),
            "unknown_candidate_location_ids": sorted(value for value in locations if value.startswith("lesson_candidate.") and value not in known_candidates),
            "targets_without_source_refs": sorted(row["target_id"] for row in targets if not row["source_refs"]),
            "targets_without_recycle_locations": sorted(row["target_id"] for row in targets if not row["recycle_locations"]),
            "examples_without_reference_ipa": sorted(row["target_id"] for row in targets if any(not item["reference_ipa"] for item in row["course_examples"])),
            "final_lesson_decisions_made": 0,
        },
        "review": {
            "status": "accepted_exact_pronunciation_pass", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "statement": "All A1 pronunciation strands, current targets, and Arabic-learner hypotheses now have bounded intelligibility decisions, evidence, examples, owners, recycling, mastery, tolerance, and later-level limits.",
        },
    }


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['targets'])} targets; {len(data['risk_dispositions'])} risks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
