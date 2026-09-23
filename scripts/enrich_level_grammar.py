#!/usr/bin/env python3
"""Enrich A1-C2 grammar inventories with reviewed GSE Grammar cross-check evidence."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
STRANDS_PATH = "data/reviewed/grammar-family-strands-v1.json"
GSE_PATH = "data/derived/gse-grammar-all.json"


def read(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def crosscheck_item(source: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    facts = source["source_facts"]
    other = facts.get("other_verbatim") or {}
    return {
        "evidence_id": source["record_id"],
        "source_text": source["source"]["source_text"],
        "published_level": mapping["source_level_codes"][0].upper(),
        "gse_score_or_range": facts.get("gse_score_or_range"),
        "mode": facts.get("mode_text"),
        "structure": other.get("structure"),
        "example": other.get("example"),
        "grammatical_categories": other.get("grammatical_categories"),
        "supercategory_codes": mapping["supercategory_codes"],
        "mapping_rule_ids": mapping["rule_ids"],
        "source_ref": {
            "source_id": source["source"].get("source_id"),
            "source_version": source["source"].get("source_version"),
            "location": source["source"].get("location"),
            "raw_file": source["source"].get("raw_file"),
            "source_file_sha256": source["source"].get("source_file_sha256"),
            "source_text_sha256": source["source"].get("source_text_sha256"),
        },
    }


def family_stage(family: dict[str, Any], level: str) -> dict[str, Any] | None:
    stage = next(
        (stage for stage in family["lifecycle"]["stages"] if stage["level"] == level),
        None,
    )
    if stage is None:
        return None
    return {
        "family_id": family["family_id"],
        "supercategory": family["supercategory"],
        "subcategory": family["subcategory"],
        "title": family["title"],
        "feature_count": stage["feature_count"],
        "evidence_status": stage["evidence_status"],
        "lifecycle_states": stage["lifecycle_states"],
        "first_productive_control_level": family["lifecycle"]["first_productive_control_level"],
        "consolidation_level": family["lifecycle"]["consolidation_level"],
    }


def main() -> None:
    reviewed = read(STRANDS_PATH)
    mappings = reviewed["gse_crosswalk"]
    families = reviewed["families"]
    gse_records = read(GSE_PATH)["records"]
    gse_by_id = {row["record_id"]: row for row in gse_records}

    if len(mappings) != 456 or len(gse_by_id) != 456:
        raise SystemExit(
            f"Expected 456 GSE Grammar records/crosswalk rows; got records={len(gse_by_id)} mappings={len(mappings)}"
        )
    mapped_ids = [row["source_record_id"] for row in mappings]
    if len(set(mapped_ids)) != 456 or set(mapped_ids) != set(gse_by_id):
        raise SystemExit("Reviewed GSE Grammar crosswalk is not one-to-one with all 456 source records")
    if len(families) != 91:
        raise SystemExit(f"Expected 91 reviewed grammar families, got {len(families)}")

    for level in LEVELS:
        path = ROOT / "curriculum" / "levels" / level / "grammar.json"
        grammar = json.loads(path.read_text(encoding="utf-8"))
        level_mappings = [row for row in mappings if row["source_level_codes"] == [level]]
        evidence = [crosscheck_item(gse_by_id[row["source_record_id"]], row) for row in level_mappings]
        stage_candidates = [family_stage(family, level) for family in families]
        stages = [stage for stage in stage_candidates if stage is not None]

        grammar["status"] = "canonical_egp_with_reviewed_gse_crosscheck_pending_inventory_lock"
        grammar["canonical_source"] = "English Grammar Profile"
        grammar["crosscheck_source"] = "Pearson GSE Grammar for adult learners 2023"
        grammar["crosscheck_policy"] = (
            "GSE Grammar is supporting/cross-check evidence mapped to reviewed grammar supercategories; "
            "it does not create a second independent target inventory."
        )
        grammar["grammar_family_policy"] = reviewed["feature_use_policy"]
        grammar["grammar_family_stage_policy"] = (
            "Only lifecycle stages explicitly present in the reviewed grammar-family source are copied; "
            "missing early-level stages are not invented."
        )
        grammar["counts"] = {
            "canonical_egp_features": len(grammar["items"]),
            "gse_crosscheck_records": len(evidence),
            "grammar_family_stages": len(stages),
            "source_evidenced_family_stages": sum(stage["feature_count"] > 0 for stage in stages),
        }
        grammar["gse_crosscheck_evidence"] = evidence
        grammar["grammar_family_stages"] = stages
        write(path, grammar)

        print(
            level.upper(),
            "EGP", len(grammar["items"]),
            "GSE-crosscheck", len(evidence),
            "family-stages", len(stages),
            "GSE-levels", dict(Counter(row["published_level"] for row in evidence)),
        )


if __name__ == "__main__":
    main()
