#!/usr/bin/env python3
"""Build granular A1-C2 ability inventories from reviewed CEFR/GSE assignments."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
ASSIGNMENTS_PATH = "data/reviewed/communicative-tag-assignments-v1.json"
STRANDS_PATH = "data/reviewed/communicative-function-strands-v1.json"
EXIT_PROFILES_PATH = "data/reviewed/level-exit-profiles-v1.json"
SOURCE_PATHS = {
    "cefr_all_descriptors": "data/derived/cefr-all-descriptors.json",
    "gse_all_objectives": "data/derived/gse-all-objectives.json",
}


def read(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect_claims(node: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if "claim_id" in node and "text" in node:
            out.append({
                key: node[key]
                for key in (
                    "claim_id",
                    "claim_type",
                    "text",
                    "evidence_bundle_ids",
                    "decision_refs",
                )
                if key in node
            })
        else:
            for value in node.values():
                out.extend(collect_claims(value))
    elif isinstance(node, list):
        for value in node:
            out.extend(collect_claims(value))
    return out


def source_indexes() -> dict[str, dict[str, dict[str, Any]]]:
    indexes: dict[str, dict[str, dict[str, Any]]] = {}
    for dataset_id, path in SOURCE_PATHS.items():
        records = read(path)["records"]
        index = {record["record_id"]: record for record in records}
        if len(index) != len(records):
            raise SystemExit(f"Duplicate source record IDs in {dataset_id}")
        indexes[dataset_id] = index
    return indexes


def ability_record(
    assignment: dict[str, Any],
    source_record: dict[str, Any],
    role: str,
) -> dict[str, Any]:
    source = source_record["source"]
    facts = source_record["source_facts"]
    return {
        "item_id": f"ability.{assignment['source_dataset_id']}.{assignment['source_record_id']}",
        "source_dataset_id": assignment["source_dataset_id"],
        "source_record_id": assignment["source_record_id"],
        "source_kind": source_record["record_kind"],
        "source_text": source["source_text"],
        "published_level": assignment["source_level_codes"][0].upper(),
        "source_level_text": facts.get("level_text"),
        "gse_score_or_range": facts.get("gse_score_or_range"),
        "skill_codes": assignment["skill_codes"],
        "mode_codes": assignment["mode_codes"],
        "function_codes": assignment["function_codes"],
        "strand_ids": [f"function.{code}" for code in assignment["function_codes"]],
        "curriculum_role": role,
        "rule_ids": assignment["rule_ids"],
        "source_ref": {
            "source_id": source.get("source_id"),
            "source_version": source.get("source_version"),
            "location": source.get("location"),
            "raw_file": source.get("raw_file"),
            "source_file_sha256": source.get("source_file_sha256"),
            "source_text_sha256": source.get("source_text_sha256"),
        },
    }


def stage_summaries(strands: list[dict[str, Any]], level: str) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for strand in strands:
        stage = next(
            (stage for stage in strand["lifecycle"]["stages"] if stage["level"] == level),
            None,
        )
        if stage is None:
            continue
        summaries.append({
            "strand_id": strand["strand_id"],
            "function_code": strand["function_code"],
            "title": strand["title"],
            "curriculum_intent": strand["curriculum_intent"],
            "evidence_count": stage["evidence_count"],
            "evidence_status": stage["evidence_status"],
            "control_expectation": stage["control_expectation"],
            "lifecycle_states": stage["lifecycle_states"],
        })
    return summaries


def main() -> None:
    assignment_data = read(ASSIGNMENTS_PATH)
    assignments = assignment_data["records"]
    strands = read(STRANDS_PATH)["strands"]
    profiles = {row["level"]: row for row in read(EXIT_PROFILES_PATH)["levels"]}
    indexes = source_indexes()

    if len(assignments) != 2274:
        raise SystemExit(f"Expected 2274 reviewed communicative assignments, got {len(assignments)}")
    if any(len(row["source_level_codes"]) != 1 for row in assignments):
        raise SystemExit("Ability builder requires exactly one reviewed source level per assignment")

    for level in LEVELS:
        level_assignments = [
            row for row in assignments if row["source_level_codes"] == [level]
        ]
        role_groups: dict[str, list[dict[str, Any]]] = {
            "include_for_spine": [],
            "supporting_evidence": [],
            "duplicate_or_overlap": [],
        }
        for assignment in level_assignments:
            role = assignment["source_disposition"]
            if role not in role_groups:
                raise SystemExit(f"Unknown communicative disposition {role!r}")
            dataset_id = assignment["source_dataset_id"]
            record_id = assignment["source_record_id"]
            try:
                source_record = indexes[dataset_id][record_id]
            except KeyError as exc:
                raise SystemExit(f"Unresolved ability source {dataset_id}:{record_id}") from exc
            role_groups[role].append(ability_record(assignment, source_record, role))

        required = role_groups["include_for_spine"]
        supporting = role_groups["supporting_evidence"]
        duplicates = role_groups["duplicate_or_overlap"]
        stages = stage_summaries(strands, level)
        role_counts = Counter(row["source_disposition"] for row in level_assignments)

        level_dir = ROOT / "curriculum" / "levels" / level
        write(level_dir / "abilities.json", {
            "schema_version": 1,
            "level": level.upper(),
            "category": "abilities",
            "inventory_semantics": "new_at_level",
            "status": "reviewed_granular_source_assignments_v1",
            "canonical_sources": ["CEFR Companion Volume 2020", "Pearson GSE Adult General English 2022"],
            "reviewed_assignment_source": ASSIGNMENTS_PATH,
            "function_strand_source": STRANDS_PATH,
            "counts": {
                "required_items": len(required),
                "supporting_evidence_items": len(supporting),
                "excluded_duplicate_or_overlap_items": len(duplicates),
                "reviewed_source_records_at_level": len(level_assignments),
                "function_strand_stages": len(stages),
            },
            "items": required,
            "supporting_evidence": supporting,
            "excluded_duplicate_or_overlap": duplicates,
            "function_stages": stages,
        })

        contract = read(str((level_dir / "exit_contract.json").relative_to(ROOT)))
        claims = collect_claims(profiles[level])
        contract["exit_profile_source"] = EXIT_PROFILES_PATH
        contract["exit_profile_claims"] = claims
        contract["ability_inventory"] = {
            "required_new_at_level": len(required),
            "supporting_evidence_at_level": len(supporting),
            "excluded_duplicates_at_level": len(duplicates),
            "reviewed_source_records_at_level": len(level_assignments),
            "required_items_file": "abilities.json",
            "exit_obligation": "cumulative_required_abilities_through_level",
        }
        write(level_dir / "exit_contract.json", contract)

        manifest = read(str((level_dir / "manifest.json").relative_to(ROOT)))
        manifest["counts"]["abilities"] = len(required)
        manifest["ability_evidence_counts"] = {
            "required": len(required),
            "supporting": len(supporting),
            "excluded_duplicate_or_overlap": len(duplicates),
            "reviewed_total": len(level_assignments),
            "function_stages": len(stages),
        }
        manifest["ability_inventory_status"] = "reviewed_granular_source_assignments_v1"
        write(level_dir / "manifest.json", manifest)

        print(
            level.upper(),
            "required", len(required),
            "supporting", len(supporting),
            "duplicates", len(duplicates),
            "total", len(level_assignments),
            "roles", dict(role_counts),
        )


if __name__ == "__main__":
    main()
