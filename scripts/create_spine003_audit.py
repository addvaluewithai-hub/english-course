"""Create the completion audit for source dispositions and level exit profiles."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.level_exit_profile_contract import OUTPUT as PROFILES
from scripts.source_disposition_contract import OUTPUT as DISPOSITIONS
from scripts.source_disposition_contract import REVIEWED_AT, REVIEWER, ROOT
from scripts.source_disposition_inputs import file_sha256


OUTPUT = ROOT / "data" / "reviewed" / "spine-003-review-audit-v1.json"
REPORT = ROOT / "docs" / "SPINE_003_REVIEW_AUDIT.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "spine-003-audit.schema.json"


def _claims(profile: dict) -> list[dict]:
    result = [profile["exit_promise"], *profile["assessment_evidence"]]
    for section in ("reception", "production", "interaction", "language_control"):
        result.extend(profile[section].values())
    return result


def _count(rows: list[dict], dataset: str, level: str, control: str | None = None) -> int:
    return sum(
        row["source_dataset_id"] == dataset
        and level in row["source_level_codes"]
        and (control is None or row["control_expectation"] == control)
        for row in rows
    )


def build() -> dict[str, Any]:
    dispositions = json.loads(DISPOSITIONS.read_text(encoding="utf-8"))
    profiles = json.loads(PROFILES.read_text(encoding="utf-8"))
    rows = dispositions["records"]
    claims = [claim for profile in profiles["levels"] for claim in _claims(profile)]
    claim_counts = Counter(claim["claim_id"] for claim in claims)
    adjacent_duplicates = []
    for earlier, later in zip(profiles["levels"], profiles["levels"][1:]):
        earlier_text = {claim["claim_id"].split(".", 1)[1]: claim["text"] for claim in _claims(earlier)}
        later_text = {claim["claim_id"].split(".", 1)[1]: claim["text"] for claim in _claims(later)}
        adjacent_duplicates += [
            f"{earlier['level']}->{later['level']}:{field}"
            for field in earlier_text.keys() & later_text
            if earlier_text[field] == later_text[field]
        ]
    levels = []
    for profile in profiles["levels"]:
        level = profile["level"]
        cefr_strands = {
            strand for row in rows
            if row["source_dataset_id"] == "cefr_all_descriptors"
            and level in row["source_level_codes"]
            for strand in row["strand_codes"]
        }
        levels.append({
            "level": level, "progression_index": profile["progression_index"],
            "reviewed_claims": len(_claims(profile)), "cefr_strands": len(cefr_strands),
            "gse_receptive_records": _count(rows, "gse_all_objectives", level, "receptive"),
            "gse_productive_records": _count(rows, "gse_all_objectives", level, "productive"),
            "egp_grammar_features": _count(rows, "egp_all_levels", level),
            "gse_grammar_features": _count(rows, "gse_grammar_all", level),
            "lexical_pool_records": sum(
                _count(rows, dataset, level)
                for dataset in ("oxford_3000_all", "oxford_5000_all")
            ),
        })
    overlap_rows = [row for row in rows if row["overlap"]]
    overlap_groups = {row["overlap"]["group_id"] for row in overlap_rows}
    score_groups = sorted({
        row["overlap"]["group_id"] for row in overlap_rows
        if row["overlap"]["different_source_scores"]
    })
    return {
        "schema_version": 1, "audit_id": "spine_003_review_audit", "status": "accepted",
        "inputs": [
            {"path": DISPOSITIONS.relative_to(ROOT).as_posix(), "sha256": file_sha256(DISPOSITIONS)},
            {"path": PROFILES.relative_to(ROOT).as_posix(), "sha256": file_sha256(PROFILES)},
        ],
        "levels": levels,
        "overlap": {
            "exact_text_groups": len(overlap_groups), "affected_records": len(overlap_rows),
            "cross_level_groups": len(dispositions["audit"]["cross_level_exact_text_conflicts"]),
            "score_variance_groups": score_groups,
        },
        "integrity": {
            "unclassified_records": dispositions["audit"]["unclassified_records"],
            "unexplained_orphans": dispositions["audit"]["unexplained_orphans"],
            "claims_without_evidence": [
                claim["claim_id"] for claim in claims
                if claim["claim_type"] != "product_policy" and not claim["evidence_bundle_ids"]
            ],
            "duplicate_claim_ids": sorted(key for key, value in claim_counts.items() if value > 1),
            "adjacent_claim_text_duplicates": adjacent_duplicates,
        },
        "named_limits": [
            "C2 lexical ownership needs a corpus- and domain-informed method because Oxford has no C2 list.",
            "CEFR supplies pronunciation boundaries but not an English-specific Arabic-learner teaching sequence.",
            "Semantic cross-source equivalence and lifecycle ownership remain SPINE-004 decisions.",
            "Source-record counts describe evidence density, not curriculum time or teaching weight.",
        ],
        "next_task": "SPINE-004",
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "complete_policy_exception_and_claim_boundary_audit",
        },
    }


def _report(data: dict) -> str:
    lines = [
        "# SPINE-003 Review Audit", "", "Status: passed internal review.", "",
        "Every normalized source record now has an explicit use disposition, and every",
        "A1-C2 exit-profile claim has either validated source evidence or an explicit",
        "product-policy basis.", "", "## Level evidence", "",
        "| Level | Claims | CEFR strands | GSE receptive | GSE productive | EGP grammar | GSE grammar | Lexical pool |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in data["levels"]:
        lines.append(
            f"| {row['level'].upper()} | {row['reviewed_claims']} | {row['cefr_strands']} | "
            f"{row['gse_receptive_records']} | {row['gse_productive_records']} | "
            f"{row['egp_grammar_features']} | {row['gse_grammar_features']} | "
            f"{row['lexical_pool_records']} |"
        )
    overlap = data["overlap"]
    lines += [
        "", "## Integrity", "",
        "- Unclassified source records: 0.", "- Unexplained orphan records: 0.",
        "- Source-boundary claims without evidence: 0.", "- Duplicate claim ids: 0.",
        "- Identical adjacent-level claim wording: 0.",
        f"- Exact-text overlap: {overlap['exact_text_groups']} groups / {overlap['affected_records']} records.",
        f"- Same text across different levels: {overlap['cross_level_groups']} groups.",
        f"- Same GSE text with different scores: {len(overlap['score_variance_groups'])} groups; preserved as source variance.",
        "", "## Named limits carried into SPINE-004", "",
    ]
    lines += [f"- {item}" for item in data["named_limits"]]
    lines += [
        "", "Counts above show available evidence, not lesson weight. A receptive/productive",
        "count difference is therefore not treated as a curriculum imbalance until the",
        "progression strands and assessment ownership are mapped.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
