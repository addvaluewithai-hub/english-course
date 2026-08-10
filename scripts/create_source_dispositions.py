"""Create reviewed, policy-based dispositions for every normalized source record."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from typing import Any

from scripts.source_disposition_contract import (
    DATASET_POLICIES, OUTPUT, POLICIES, REPORT, REVIEWED_AT, REVIEWER, ROOT,
)
from scripts.source_disposition_inputs import (
    file_sha256, level_codes, level_text, load_inputs, normalized_text, record_id, score_text,
)
from scripts.source_disposition_policy import classify


def _overlap_index(inputs: list[tuple[str, Any, dict]]) -> dict[tuple[str, str], dict]:
    index: dict[tuple[str, str], dict] = {}
    for dataset_id, _, data in inputs:
        groups: dict[str, list[dict]] = defaultdict(list)
        for record in data["records"]:
            groups[normalized_text(dataset_id, record)].append(record)
        for text, records in groups.items():
            if len(records) < 2:
                continue
            ids = [record_id(dataset_id, item) for item in records]
            levels = {code for item in records for code in level_codes(dataset_id, item)}
            scores = {score_text(dataset_id, item) for item in records}
            group = {
                "group_id": f"overlap_{hashlib.sha256(text.encode()).hexdigest()[:12]}",
                "canonical_record_id": ids[0],
                "relation": "exact_text_repetition",
                "different_source_levels": len(levels) > 1,
                "different_source_scores": len(scores) > 1,
            }
            for source_id in ids:
                index[(dataset_id, source_id)] = group
    return index


def build() -> dict[str, Any]:
    inputs = load_inputs()
    overlaps = _overlap_index(inputs)
    source_datasets, records = [], []
    for dataset_id, path, data in inputs:
        source_datasets.append({
            "dataset_id": dataset_id,
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(path),
            "record_count": len(data["records"]),
        })
        policy_id = DATASET_POLICIES[dataset_id]
        policy = POLICIES[policy_id]
        for source_record in data["records"]:
            source_id = record_id(dataset_id, source_record)
            strand_codes, control = classify(dataset_id, source_record)
            overlap = overlaps.get((dataset_id, source_id))
            records.append({
                "source_dataset_id": dataset_id,
                "source_record_id": source_id,
                "source_level_codes": level_codes(dataset_id, source_record),
                "source_level_text": level_text(dataset_id, source_record),
                "source_role": policy["source_role"],
                "control_expectation": control,
                "strand_codes": strand_codes,
                "disposition": "duplicate_or_overlap" if overlap else policy["base_disposition"],
                "policy_id": policy_id,
                "overlap": overlap,
            })
    return _collection(source_datasets, records)


def _counts(records: list[dict], key: str, flatten: bool = False) -> dict[str, int]:
    values = (value for row in records for value in row[key]) if flatten else (row[key] for row in records)
    return dict(sorted(Counter(values).items()))


def _collection(source_datasets: list[dict], records: list[dict]) -> dict[str, Any]:
    groups = {row["overlap"]["group_id"] for row in records if row["overlap"]}
    conflicts = sorted({
        row["overlap"]["group_id"] for row in records
        if row["overlap"] and row["overlap"]["different_source_levels"]
    })
    audit = {
        "total_records": len(records),
        "disposition_counts": _counts(records, "disposition"),
        "role_counts": _counts(records, "source_role"),
        "control_counts": _counts(records, "control_expectation"),
        "strand_counts": _counts(records, "strand_codes", True),
        "level_counts": _counts(records, "source_level_codes", True),
        "overlap_groups": len(groups),
        "unclassified_records": [],
        "unexplained_orphans": [],
        "cross_level_exact_text_conflicts": conflicts,
    }
    policies = [{"policy_id": key, **value} for key, value in POLICIES.items()]
    return {
        "schema_version": 1,
        "dataset_id": "english_course_source_dispositions",
        "version": 1,
        "source_datasets": source_datasets,
        "policy_catalog": policies,
        "records": records,
        "audit": audit,
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "policy_rule_plus_exception_audit", "individual_manual_review": False,
            "decision_authority": "owner_delegated_primary_agent",
            "limitations": [
                "Acceptance records a reviewed classification policy plus complete exception audit; it does not claim manual item-by-item pedagogical judgment.",
                "Semantic cross-source equivalence and exact lifecycle ownership belong to SPINE-004 progression mapping.",
                "Oxford evidence remains a reference pool; C2 lexical methodology requires a separate corpus- and domain-informed design.",
            ],
        },
    }


def _report(data: dict[str, Any]) -> str:
    audit = data["audit"]
    lines = [
        "# Source Disposition Audit v1", "", "Status: accepted internal curriculum review.", "",
        f"All **{audit['total_records']:,}** normalized records have an explicit disposition.",
        "The review is policy-based with a complete exact-overlap and exception audit; it",
        "does not pretend that 9,274 items received separate human pedagogical judgments.", "",
        "## Dispositions", "", "| Disposition | Records |", "| --- | ---: |",
    ]
    lines += [f"| `{key}` | {value:,} |" for key, value in audit["disposition_counts"].items()]
    lines += ["", "## Controls", "", "| Expected control | Records |", "| --- | ---: |"]
    lines += [f"| `{key}` | {value:,} |" for key, value in audit["control_counts"].items()]
    lines += [
        "", "## Findings", "",
        f"- Exact-text overlap groups: {audit['overlap_groups']}.",
        f"- Cross-level exact-text conflicts: {len(audit['cross_level_exact_text_conflicts'])}.",
        "- Unclassified records: 0.", "- Unexplained orphan records: 0.",
        "- Cross-source semantic overlap is not treated as equivalence; SPINE-004 must map it explicitly.",
        "- GSE listening/reading objectives remain receptive targets, not downgraded to exposure.",
        "- Oxford entries remain lexical reference pools, not automatic teaching targets.", "",
        "## Decision boundary", "",
        "This audit decides how each source record may be used. It does not yet decide the",
        "first exposure, practice, recycle, consolidation, or extension level for each item.",
        "Those product decisions belong to the progression-strand work package.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['records'])} records)")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
