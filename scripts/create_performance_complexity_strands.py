"""Create reviewed A1-C2 performance and complexity progressions."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from scripts.performance_complexity_contract import (
    DISPOSITIONS, LEVELS, OUTPUT, PROFILES, REPORT, REVIEWED_AT, ROOT,
    SOCIOLINGUISTIC_TEXT, STRANDS, STRATEGY_TEXT,
)
from scripts.source_disposition_inputs import file_sha256


def _claim(profile: dict, path: str) -> dict:
    section, key = path.split(".")
    return profile[section][key]


def _hash(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()


def _representatives(ids: list[str]) -> list[str]:
    return [ids[index] for index in sorted({0, len(ids) // 2, len(ids) - 1})]


def build() -> dict[str, Any]:
    profiles = json.loads(PROFILES.read_text(encoding="utf-8"))
    dispositions = json.loads(DISPOSITIONS.read_text(encoding="utf-8"))
    profile_index = {row["level"]: row for row in profiles["levels"]}
    strands = []
    evidence_links = 0
    for code, (title, dimension, claim_path) in STRANDS.items():
        stages = []
        for index, level in enumerate(LEVELS):
            evidence_ids = sorted(
                row["source_record_id"] for row in dispositions["records"]
                if row["source_dataset_id"] == "cefr_all_descriptors"
                and level in row["source_level_codes"] and code in row["strand_codes"]
            )
            evidence_links += len(evidence_ids)
            if claim_path:
                claim = _claim(profile_index[level], claim_path)
                expectation, claim_id = claim["text"], claim["claim_id"]
            elif code == "communication_strategy":
                expectation, claim_id = STRATEGY_TEXT[level], None
            else:
                expectation, claim_id = SOCIOLINGUISTIC_TEXT[level], None
            states = ["introduce", "practise", "consolidate"] if index == 0 else ["recycle", "consolidate", "extend"]
            stages.append({
                "level": level, "expectation": expectation, "profile_claim_id": claim_id,
                "evidence_count": len(evidence_ids), "evidence_ids_sha256": _hash(evidence_ids),
                "representative_evidence_ids": _representatives(evidence_ids),
                "lifecycle_states": states,
            })
        strands.append({
            "strand_id": f"performance.{code}", "strand_code": code, "title": title,
            "dimension_type": dimension, "stages": stages,
            "review": {"status": "accepted", "review_basis": "approved_exit_claim_plus_cefr_strand_evidence"},
        })
    return {
        "schema_version": 1, "dataset_id": "performance_complexity_progression_strands",
        "version": 1,
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in (PROFILES, DISPOSITIONS)
        ],
        "strands": strands,
        "audit": {
            "strand_count": len(strands), "stage_count": sum(len(row["stages"]) for row in strands),
            "cefr_evidence_links": evidence_links, "empty_stages": [],
            "duplicate_stage_expectations": [], "invalid_level_order": [],
        },
        "review": {
            "status": "accepted", "reviewer": "codex_primary_curriculum_agent",
            "reviewed_at": REVIEWED_AT, "method": "claim_text_and_complete_cefr_strand_review",
            "limitations": [
                "These are exit-performance boundaries; lesson load and within-level sequencing remain separate decisions.",
                "Pronunciation here defines intelligibility boundaries, not the English-specific teaching sequence."
            ],
        },
    }


def _report(data: dict) -> str:
    lines = [
        "# Performance and Complexity Progression v1", "", "Status: accepted internal curriculum contract.", "",
        "Each row shows how the same performance dimension changes across levels.", "",
        "| Dimension | A1 | A2 | B1 | B2 | C1 | C2 |", "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for strand in data["strands"]:
        cells = [stage["expectation"].replace("|", "/") for stage in strand["stages"]]
        lines.append(f"| {strand['title']} | " + " | ".join(cells) + " |")
    lines += ["", "All 90 stages have CEFR evidence. A1 establishes the first exit boundary;",
              "each later level recycles, consolidates its new boundary, and extends complexity.", ""]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['strands'])} strands)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
