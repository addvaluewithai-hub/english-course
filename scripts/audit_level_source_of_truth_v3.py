#!/usr/bin/env python3
"""Strict A1-C2 Source-of-Truth coverage audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
ROLES = ("include_for_spine", "supporting_evidence", "duplicate_or_overlap")


def load(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def claims(node: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if "claim_id" in node and "text" in node:
            out.append(node)
        else:
            for value in node.values():
                out.extend(claims(value))
    elif isinstance(node, list):
        for value in node:
            out.extend(claims(value))
    return out


def main() -> None:
    errors: list[str] = []
    report: dict[str, Any] = {"levels": {}, "coverage": {}}

    # Level files and manifest counts.
    for level in LEVELS:
        manifest = load(f"curriculum/levels/{level}/manifest.json")
        if manifest.get("lesson_design_authorized") is not False:
            errors.append(f"{level}: lesson design must remain locked")
        counts: dict[str, int] = {}
        for category in ("words", "phrases", "grammar", "abilities", "pronunciation"):
            rows = load(f"curriculum/levels/{level}/{category}.json")["items"]
            counts[category] = len(rows)
            ids = [row.get("item_id") or row.get("claim_id") for row in rows]
            ids = [value for value in ids if value is not None]
            if len(ids) != len(set(ids)):
                errors.append(f"{level}/{category}: duplicate primary IDs")
            if manifest["counts"][category] != len(rows):
                errors.append(f"{level}/{category}: manifest count mismatch")
        report["levels"][level] = counts

    # Oxford 3000 + 5000: exact 5322-record A1-C1 partition.
    oxford = load("data/derived/oxford-3000-all.json")["records"] + load("data/derived/oxford-5000-all.json")["records"]
    oxford_ids = [row["record_id"] for row in oxford]
    word_ids = [row["source_ref"] for level in LEVELS[:-1] for row in load(f"curriculum/levels/{level}/words.json")["items"]]
    report["coverage"]["oxford_words"] = {"source": len(oxford_ids), "inventory": len(word_ids), "unique": len(set(word_ids))}
    if len(oxford_ids) != 5322 or len(set(oxford_ids)) != 5322 or len(word_ids) != 5322 or set(word_ids) != set(oxford_ids):
        errors.append("Oxford word coverage mismatch")

    # Current official Oxford Phrase List: 750 records exactly once A1-C1.
    phrase_source = {row["record_id"] for row in load("data/derived/oxford-phrase-list-online.json")["records"]}
    phrase_ids = [row["item_id"] for level in LEVELS[:-1] for row in load(f"curriculum/levels/{level}/phrases.json")["items"]]
    report["coverage"]["oxford_phrases"] = {"source": len(phrase_source), "inventory": len(phrase_ids), "unique": len(set(phrase_ids))}
    if len(phrase_source) != 750 or len(phrase_ids) != 750 or set(phrase_ids) != phrase_source:
        errors.append("Oxford phrase coverage mismatch")

    # Pearson C2 primary lexical ownership.
    c2_source = {row["itemId"] for row in load("data/derived/gse-vocabulary-c2-gl.json")["records"]}
    c2_words = {row["source_ref"]["item_id"] for row in load("curriculum/levels/c2/words.json")["items"]}
    c2_phrase_rows = load("curriculum/levels/c2/phrases.json")["items"]
    c2_direct = {row["source_ref"]["item_id"] for row in c2_phrase_rows if row["subtype"] in {"source_phrase", "source_phrasal_verb"}}
    collocations = [row for row in c2_phrase_rows if row["subtype"] == "collocation"]
    report["coverage"]["pearson_c2"] = {"source": len(c2_source), "words": len(c2_words), "direct_phrases": len(c2_direct), "collocations": len(collocations)}
    if len(c2_source) != 623 or len(c2_words) != 609 or len(c2_direct) != 14 or len(collocations) != 27 or c2_words | c2_direct != c2_source or c2_words & c2_direct:
        errors.append("Pearson C2 ownership mismatch")

    # EGP canonical grammar: 1222 features exactly once.
    egp_source = {row["_source"]["spreadsheet_row"] for row in load("data/derived/egp-all-levels.json")["records"]}
    egp_inventory = [row["source_ref"]["spreadsheet_row"] for level in LEVELS for row in load(f"curriculum/levels/{level}/grammar.json")["items"]]
    report["coverage"]["egp"] = {"source": len(egp_source), "inventory": len(egp_inventory), "unique": len(set(egp_inventory))}
    if len(egp_source) != 1222 or len(egp_inventory) != 1222 or set(egp_inventory) != egp_source:
        errors.append("EGP coverage mismatch")

    # GSE Grammar cross-check: all 456 reviewed, with Pre-A1 intentionally outside six folders.
    grammar_review = load("data/reviewed/grammar-family-strands-v1.json")
    gse_source = {row["record_id"] for row in load("data/derived/gse-grammar-all.json")["records"]}
    crosswalk = grammar_review["gse_crosswalk"]
    crosswalk_ids = [row["source_record_id"] for row in crosswalk]
    pre_a1_gse: set[str] = set()
    expected_gse: set[str] = set()
    for row in crosswalk:
        level_codes = row["source_level_codes"]
        if len(level_codes) != 1:
            errors.append(f"GSE Grammar non-singleton level: {row['source_record_id']}")
        elif level_codes[0] == "pre_a1":
            pre_a1_gse.add(row["source_record_id"])
        elif level_codes[0] in LEVELS:
            expected_gse.add(row["source_record_id"])
        else:
            errors.append(f"GSE Grammar unexpected level: {level_codes[0]}")
    inventory_gse = [row["evidence_id"] for level in LEVELS for row in load(f"curriculum/levels/{level}/grammar.json").get("gse_crosscheck_evidence", [])]
    reviewed_stage_pairs = {
        (stage["level"], family["family_id"])
        for family in grammar_review["families"]
        for stage in family["lifecycle"]["stages"]
        if stage["level"] in LEVELS
    }
    inventory_stage_pairs = [
        (level, row["family_id"])
        for level in LEVELS
        for row in load(f"curriculum/levels/{level}/grammar.json").get("grammar_family_stages", [])
    ]
    report["coverage"]["gse_grammar"] = {
        "source": len(gse_source),
        "pre_a1": len(pre_a1_gse),
        "expected_a1_c2": len(expected_gse),
        "inventory_crosschecks": len(inventory_gse),
        "families": len(grammar_review["families"]),
        "reviewed_a1_c2_family_stages": len(reviewed_stage_pairs),
        "inventory_family_stages": len(inventory_stage_pairs),
    }
    if len(gse_source) != 456 or len(crosswalk_ids) != 456 or set(crosswalk_ids) != gse_source:
        errors.append("GSE Grammar source/crosswalk mismatch")
    if len(inventory_gse) != len(expected_gse) or set(inventory_gse) != expected_gse:
        errors.append(f"GSE Grammar A1-C2 crosscheck mismatch: expected={len(expected_gse)} actual={len(inventory_gse)}")
    if len(grammar_review["families"]) != 91 or len(reviewed_stage_pairs) != 528:
        errors.append("Reviewed grammar-family source changed unexpectedly")
    if len(inventory_stage_pairs) != 528 or set(inventory_stage_pairs) != reviewed_stage_pairs:
        errors.append("Grammar-family stage coverage mismatch")

    # Granular communicative abilities: 2274 reviewed records, 106 Pre-A1, 2168 explicit A1-C2 dispositions.
    assignments = load("data/reviewed/communicative-tag-assignments-v1.json")["records"]
    valid_strands = {row["strand_id"] for row in load("data/reviewed/communicative-function-strands-v1.json")["strands"]}
    expected: dict[tuple[str, str], set[str]] = {}
    pre_a1_abilities = 0
    for row in assignments:
        level_codes = row["source_level_codes"]
        if len(level_codes) != 1:
            errors.append(f"Ability non-singleton level: {row['source_record_id']}")
            continue
        level = level_codes[0]
        if level == "pre_a1":
            pre_a1_abilities += 1
            continue
        role = row["source_disposition"]
        if level not in LEVELS or role not in ROLES:
            errors.append(f"Ability unexpected level/role: {level}/{role}")
            continue
        expected.setdefault((level, role), set()).add(row["source_record_id"])
    actual_total = 0
    by_level: dict[str, dict[str, int]] = {}
    for level in LEVELS:
        data = load(f"curriculum/levels/{level}/abilities.json")
        buckets = {
            "include_for_spine": data["items"],
            "supporting_evidence": data["supporting_evidence"],
            "duplicate_or_overlap": data["excluded_duplicate_or_overlap"],
        }
        seen: list[str] = []
        by_level[level] = {}
        for role, rows in buckets.items():
            ids = [row["source_record_id"] for row in rows]
            by_level[level][role] = len(ids)
            actual_total += len(ids)
            seen.extend(ids)
            if len(ids) != len(set(ids)) or set(ids) != expected.get((level, role), set()):
                errors.append(f"{level} ability {role} mismatch")
            for row in rows:
                if not row.get("source_text") or not set(row.get("strand_ids", [])).issubset(valid_strands):
                    errors.append(f"{level} ability provenance/strand invalid: {row['source_record_id']}")
        if len(seen) != len(set(seen)):
            errors.append(f"{level}: ability appears in multiple disposition buckets")
    report["coverage"]["abilities"] = {"source": len(assignments), "pre_a1": pre_a1_abilities, "expected_a1_c2": len(assignments) - pre_a1_abilities, "inventory": actual_total, "strands": len(valid_strands), "by_level": by_level}
    if len(assignments) != 2274 or pre_a1_abilities != 106 or actual_total != 2168 or len(valid_strands) != 41:
        errors.append("Ability coverage totals mismatch")

    # Pronunciation: exact 10 strands x six level stages.
    pronunciation = load("data/reviewed/pronunciation-progression-strands-v1.json")["strands"]
    strand_ids = {row["strand_id"] for row in pronunciation}
    expected_pron = {(level, strand_id) for level in LEVELS for strand_id in strand_ids}
    actual_pron = [(level, row["strand_id"]) for level in LEVELS for row in load(f"curriculum/levels/{level}/pronunciation.json")["items"]]
    report["coverage"]["pronunciation"] = {"strands": len(strand_ids), "stages": len(actual_pron), "unique": len(set(actual_pron))}
    if len(strand_ids) != 10 or len(actual_pron) != 60 or set(actual_pron) != expected_pron:
        errors.append("Pronunciation coverage mismatch")

    # Exit contract: 102 reviewed claims, 17 per level, preserved exactly.
    profiles = {row["level"]: claims(row) for row in load("data/reviewed/level-exit-profiles-v1.json")["levels"]}
    exit_total = 0
    exit_counts: dict[str, int] = {}
    for level in LEVELS:
        expected_ids = [row["claim_id"] for row in profiles[level]]
        actual_ids = [row["claim_id"] for row in load(f"curriculum/levels/{level}/exit_contract.json").get("exit_profile_claims", [])]
        exit_counts[level] = len(actual_ids)
        exit_total += len(actual_ids)
        if actual_ids != expected_ids:
            errors.append(f"{level}: exit-profile claim mismatch")
    report["coverage"]["exit_profiles"] = {"inventory": exit_total, "by_level": exit_counts}
    if exit_total != 102 or any(count != 17 for count in exit_counts.values()):
        errors.append("Exit-profile coverage mismatch")

    print(json.dumps(report, indent=2))
    if errors:
        print("AUDIT ERRORS")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("AUDIT PASS")


if __name__ == "__main__":
    main()
