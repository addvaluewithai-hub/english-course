#!/usr/bin/env python3
"""Audit A1-C2 source-of-truth inventories against their canonical inputs."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
CATEGORIES = ("words", "phrases", "grammar", "abilities", "pronunciation")
ABILITY_ROLES = (
    "include_for_spine",
    "supporting_evidence",
    "duplicate_or_overlap",
)


def read(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def collect_claims(node: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if "claim_id" in node and "text" in node:
            out.append(node)
        else:
            for value in node.values():
                out.extend(collect_claims(value))
    elif isinstance(node, list):
        for value in node:
            out.extend(collect_claims(value))
    return out


def main() -> None:
    errors: list[str] = []
    report: dict[str, Any] = {"levels": {}, "cross_source": {}}

    for level in LEVELS:
        folder = ROOT / "curriculum" / "levels" / level
        manifest = read(str(folder.relative_to(ROOT) / "manifest.json"))
        level_report = {"counts": {}, "duplicate_item_ids": {}}
        for category in CATEGORIES:
            data = read(str(folder.relative_to(ROOT) / f"{category}.json"))
            items = data["items"]
            ids = [item.get("item_id") or item.get("claim_id") for item in items]
            duplicate_ids = sorted(
                key for key, count in Counter(ids).items() if key is not None and count > 1
            )
            level_report["counts"][category] = len(items)
            level_report["duplicate_item_ids"][category] = duplicate_ids
            if duplicate_ids:
                errors.append(f"{level}/{category}: duplicate item ids {duplicate_ids[:10]}")
            if len(items) != manifest["counts"][category]:
                errors.append(
                    f"{level}/{category}: manifest={manifest['counts'][category]} actual={len(items)}"
                )
        if manifest.get("lesson_design_authorized") is not False:
            errors.append(f"{level}: lesson design must remain locked during inventory review")
        report["levels"][level] = level_report

    # Oxford words: all normalized Oxford 3000 + 5000 entry records must appear once
    # across A1-C1. C2 intentionally uses Pearson instead of Oxford.
    oxford_sources = (
        read("data/derived/oxford-3000-all.json")["records"]
        + read("data/derived/oxford-5000-all.json")["records"]
    )
    oxford_word_ids = [row["record_id"] for row in oxford_sources]
    inventory_oxford_word_ids: list[str] = []
    for level in LEVELS[:-1]:
        inventory_oxford_word_ids.extend(
            row["source_ref"] for row in read(f"curriculum/levels/{level}/words.json")["items"]
        )
    report["cross_source"]["oxford_words"] = {
        "source_records": len(oxford_word_ids),
        "unique_source_records": len(set(oxford_word_ids)),
        "inventory_records": len(inventory_oxford_word_ids),
        "unique_inventory_records": len(set(inventory_oxford_word_ids)),
    }
    if len(oxford_word_ids) != 5322 or len(set(oxford_word_ids)) != 5322:
        errors.append("Oxford normalized source must contain 5322 unique entry records")
    if (
        len(inventory_oxford_word_ids) != len(oxford_word_ids)
        or set(inventory_oxford_word_ids) != set(oxford_word_ids)
    ):
        errors.append("Oxford A1-C1 words are not a one-to-one partition of all 5322 source records")

    # Oxford Phrase List must be partitioned exactly once across A1-C1.
    oxford_phrase_source = read("data/derived/oxford-phrase-list-online.json")
    source_phrase_ids = {row["record_id"] for row in oxford_phrase_source["records"]}
    inventory_phrase_ids: list[str] = []
    for level in LEVELS[:-1]:
        inventory_phrase_ids.extend(
            row["item_id"] for row in read(f"curriculum/levels/{level}/phrases.json")["items"]
        )
    report["cross_source"]["oxford_phrases"] = {
        "source": len(source_phrase_ids),
        "inventory": len(inventory_phrase_ids),
        "unique_inventory": len(set(inventory_phrase_ids)),
    }
    if (
        set(inventory_phrase_ids) != source_phrase_ids
        or len(inventory_phrase_ids) != len(source_phrase_ids)
    ):
        errors.append("Oxford A1-C1 phrases are not a one-to-one partition of the 750 source records")

    # Pearson C2: every source record must have exactly one primary lexical owner.
    c2_source = read("data/derived/gse-vocabulary-c2-gl.json")["records"]
    source_ids = {row["itemId"] for row in c2_source}
    word_owner_ids = {
        row["source_ref"]["item_id"]
        for row in read("curriculum/levels/c2/words.json")["items"]
    }
    phrase_rows = read("curriculum/levels/c2/phrases.json")["items"]
    direct_phrase_owner_ids = {
        row["source_ref"]["item_id"]
        for row in phrase_rows
        if row["subtype"] in {"source_phrase", "source_phrasal_verb"}
    }
    primary_ids = word_owner_ids | direct_phrase_owner_ids
    report["cross_source"]["pearson_c2"] = {
        "source_records": len(source_ids),
        "word_owners": len(word_owner_ids),
        "direct_phrase_owners": len(direct_phrase_owner_ids),
        "primary_owned": len(primary_ids),
        "collocations": sum(1 for row in phrase_rows if row["subtype"] == "collocation"),
    }
    if word_owner_ids & direct_phrase_owner_ids:
        errors.append("Pearson C2 source record has both word and direct-phrase ownership")
    if primary_ids != source_ids:
        errors.append(
            f"Pearson C2 primary ownership mismatch: missing={len(source_ids-primary_ids)} extra={len(primary_ids-source_ids)}"
        )

    # EGP: every source row must appear exactly once in the six grammar inventories.
    egp = read("data/derived/egp-all-levels.json")["records"]
    egp_rows = {row["_source"]["spreadsheet_row"] for row in egp}
    inventory_egp_rows: list[int] = []
    for level in LEVELS:
        inventory_egp_rows.extend(
            row["source_ref"]["spreadsheet_row"]
            for row in read(f"curriculum/levels/{level}/grammar.json")["items"]
        )
    inventory_egp_set = set(inventory_egp_rows)
    level_labels = Counter(str(row.get("Level")) for row in egp)
    report["cross_source"]["egp"] = {
        "source_records": len(egp),
        "inventory_records": len(inventory_egp_rows),
        "unique_inventory_rows": len(inventory_egp_set),
        "missing_rows": len(egp_rows - inventory_egp_set),
        "extra_rows": len(inventory_egp_set - egp_rows),
        "source_level_labels": dict(sorted(level_labels.items())),
    }
    if len(inventory_egp_rows) != len(inventory_egp_set):
        errors.append("EGP grammar inventory contains duplicate spreadsheet rows")
    if inventory_egp_set != egp_rows:
        errors.append(
            f"EGP grammar source not fully partitioned: source={len(egp_rows)} inventory={len(inventory_egp_set)} missing={len(egp_rows-inventory_egp_set)}"
        )

    # GSE Grammar is cross-check evidence, not a parallel target list. All 456 source
    # records must nevertheless be present exactly once through the reviewed crosswalk.
    grammar_review = read("data/reviewed/grammar-family-strands-v1.json")
    gse_grammar_source = read("data/derived/gse-grammar-all.json")["records"]
    gse_source_ids = {row["record_id"] for row in gse_grammar_source}
    reviewed_crosswalk = grammar_review["gse_crosswalk"]
    crosswalk_ids = [row["source_record_id"] for row in reviewed_crosswalk]
    inventory_gse_ids: list[str] = []
    family_stage_pairs: list[tuple[str, str]] = []
    for level in LEVELS:
        grammar = read(f"curriculum/levels/{level}/grammar.json")
        inventory_gse_ids.extend(
            row["evidence_id"] for row in grammar.get("gse_crosscheck_evidence", [])
        )
        stages = grammar.get("grammar_family_stages", [])
        if len(stages) != 91:
            errors.append(f"{level}: expected 91 grammar-family stages, got {len(stages)}")
        family_stage_pairs.extend((level, row["family_id"]) for row in stages)
    reviewed_family_ids = {row["family_id"] for row in grammar_review["families"]}
    report["cross_source"]["gse_grammar"] = {
        "source_records": len(gse_source_ids),
        "reviewed_crosswalk_records": len(crosswalk_ids),
        "unique_crosswalk_records": len(set(crosswalk_ids)),
        "inventory_crosscheck_records": len(inventory_gse_ids),
        "unique_inventory_crosscheck_records": len(set(inventory_gse_ids)),
        "grammar_families": len(reviewed_family_ids),
        "inventory_family_stages": len(family_stage_pairs),
    }
    if len(gse_source_ids) != 456:
        errors.append(f"Expected 456 GSE Grammar source records, got {len(gse_source_ids)}")
    if set(crosswalk_ids) != gse_source_ids or len(crosswalk_ids) != 456:
        errors.append("Reviewed GSE Grammar crosswalk is not one-to-one with all 456 source records")
    if set(inventory_gse_ids) != gse_source_ids or len(inventory_gse_ids) != 456:
        errors.append("Grammar inventories do not carry all 456 GSE Grammar cross-check records exactly once")
    expected_family_pairs = {(level, family_id) for level in LEVELS for family_id in reviewed_family_ids}
    if set(family_stage_pairs) != expected_family_pairs or len(family_stage_pairs) != len(expected_family_pairs):
        errors.append("Grammar inventories do not carry every reviewed family stage exactly once per A1-C2 level")

    # Abilities: every reviewed A1-C2 communicative assignment must have exactly one
    # explicit curriculum disposition; Pre-A1 remains intentionally outside the six folders.
    assignments = read("data/reviewed/communicative-tag-assignments-v1.json")["records"]
    valid_strands = {
        strand["strand_id"]
        for strand in read("data/reviewed/communicative-function-strands-v1.json")["strands"]
    }
    expected_by_level_role: dict[tuple[str, str], set[str]] = {}
    pre_a1 = 0
    for row in assignments:
        level_codes = row["source_level_codes"]
        if len(level_codes) != 1:
            errors.append(f"Ability source has non-singleton level assignment: {row['source_record_id']}")
            continue
        level = level_codes[0]
        if level == "pre_a1":
            pre_a1 += 1
            continue
        role = row["source_disposition"]
        if level not in LEVELS or role not in ABILITY_ROLES:
            errors.append(f"Unexpected ability level/role: {level}/{role}/{row['source_record_id']}")
            continue
        expected_by_level_role.setdefault((level, role), set()).add(row["source_record_id"])

    ability_report: dict[str, dict[str, int]] = {}
    inventory_total = 0
    for level in LEVELS:
        data = read(f"curriculum/levels/{level}/abilities.json")
        actual_groups = {
            "include_for_spine": data["items"],
            "supporting_evidence": data["supporting_evidence"],
            "duplicate_or_overlap": data["excluded_duplicate_or_overlap"],
        }
        level_counts: dict[str, int] = {}
        seen_ids: list[str] = []
        for role, items in actual_groups.items():
            actual_ids = {item["source_record_id"] for item in items}
            expected_ids = expected_by_level_role.get((level, role), set())
            level_counts[role] = len(items)
            inventory_total += len(items)
            seen_ids.extend(item["source_record_id"] for item in items)
            if actual_ids != expected_ids or len(actual_ids) != len(items):
                errors.append(
                    f"{level} ability {role} mismatch: expected={len(expected_ids)} actual={len(items)} unique={len(actual_ids)}"
                )
            for item in items:
                if not item.get("source_text"):
                    errors.append(f"{level} ability missing source text: {item['source_record_id']}")
                if not set(item.get("strand_ids", [])).issubset(valid_strands):
                    errors.append(f"{level} ability has unknown strand: {item['source_record_id']}")
                if item.get("published_level") != level.upper():
                    errors.append(f"{level} ability level mismatch: {item['source_record_id']}")
        if len(seen_ids) != len(set(seen_ids)):
            errors.append(f"{level} ability source record appears in multiple disposition buckets")
        ability_report[level] = level_counts

    expected_six_level_total = len(assignments) - pre_a1
    report["cross_source"]["abilities"] = {
        "reviewed_assignments_total": len(assignments),
        "pre_a1_intentionally_outside_six_levels": pre_a1,
        "expected_a1_c2_records": expected_six_level_total,
        "inventory_disposition_records": inventory_total,
        "by_level": ability_report,
        "valid_function_strands": len(valid_strands),
    }
    if inventory_total != expected_six_level_total:
        errors.append(
            f"Ability disposition coverage mismatch: expected={expected_six_level_total} actual={inventory_total}"
        )

    # Pronunciation: each of the 10 reviewed strands must have one stage in every A1-C2
    # level inventory. Pre-A1 support stays outside the six level folders.
    pronunciation_source = read("data/reviewed/pronunciation-progression-strands-v1.json")["strands"]
    pronunciation_strand_ids = {row["strand_id"] for row in pronunciation_source}
    expected_pron_pairs = {(level, strand_id) for level in LEVELS for strand_id in pronunciation_strand_ids}
    actual_pron_pairs: list[tuple[str, str]] = []
    for level in LEVELS:
        items = read(f"curriculum/levels/{level}/pronunciation.json")["items"]
        actual_pron_pairs.extend((level, row["strand_id"]) for row in items)
    report["cross_source"]["pronunciation"] = {
        "reviewed_strands": len(pronunciation_strand_ids),
        "expected_a1_c2_stages": len(expected_pron_pairs),
        "inventory_stages": len(actual_pron_pairs),
        "unique_inventory_stages": len(set(actual_pron_pairs)),
    }
    if len(pronunciation_strand_ids) != 10:
        errors.append(f"Expected 10 pronunciation strands, got {len(pronunciation_strand_ids)}")
    if set(actual_pron_pairs) != expected_pron_pairs or len(actual_pron_pairs) != len(expected_pron_pairs):
        errors.append("Pronunciation inventories do not contain exactly one stage per strand per A1-C2 level")

    # Exit profiles: all reviewed claims must be preserved exactly once in each level's
    # exit contract. These are the high-level cumulative contract, not granular abilities.
    exit_source = read("data/reviewed/level-exit-profiles-v1.json")["levels"]
    exit_source_by_level = {row["level"]: collect_claims(row) for row in exit_source}
    exit_claim_total = 0
    inventory_exit_total = 0
    exit_counts: dict[str, int] = {}
    for level in LEVELS:
        expected_claims = exit_source_by_level[level]
        expected_ids = [row["claim_id"] for row in expected_claims]
        actual_claims = read(f"curriculum/levels/{level}/exit_contract.json").get("exit_profile_claims", [])
        actual_ids = [row["claim_id"] for row in actual_claims]
        exit_claim_total += len(expected_ids)
        inventory_exit_total += len(actual_ids)
        exit_counts[level] = len(actual_ids)
        if len(expected_ids) != len(set(expected_ids)):
            errors.append(f"{level}: source exit profile contains duplicate claim IDs")
        if actual_ids != expected_ids:
            errors.append(
                f"{level}: exit contract claim IDs/order differ from reviewed exit profile: expected={len(expected_ids)} actual={len(actual_ids)}"
            )
    report["cross_source"]["exit_profiles"] = {
        "reviewed_claims": exit_claim_total,
        "inventory_claims": inventory_exit_total,
        "by_level": exit_counts,
    }
    if exit_claim_total != 102 or inventory_exit_total != 102:
        errors.append(
            f"Expected 102 reviewed exit claims preserved in contracts, got source={exit_claim_total} inventory={inventory_exit_total}"
        )

    print(json.dumps(report, indent=2))
    if errors:
        print("AUDIT ERRORS")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("AUDIT PASS")


if __name__ == "__main__":
    main()
