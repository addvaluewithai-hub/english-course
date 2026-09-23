#!/usr/bin/env python3
"""Strict A1-C2 coverage audit with intentional Pre-A1 exclusions."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
ROLES = ("include_for_spine", "supporting_evidence", "duplicate_or_overlap")


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


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> None:
    errors: list[str] = []
    report: dict[str, Any] = {"levels": {}, "coverage": {}}

    # Per-level integrity and manifest counts.
    for level in LEVELS:
        manifest = read(f"curriculum/levels/{level}/manifest.json")
        if manifest.get("lesson_design_authorized") is not False:
            fail(errors, f"{level}: lesson_design_authorized must remain false")
        counts: dict[str, int] = {}
        for category in ("words", "phrases", "grammar", "abilities", "pronunciation"):
            data = read(f"curriculum/levels/{level}/{category}.json")
            items = data["items"]
            ids = [item.get("item_id") or item.get("claim_id") for item in items]
            if len([x for x in ids if x is not None]) != len(set(x for x in ids if x is not None)):
                fail(errors, f"{level}/{category}: duplicate primary IDs")
            counts[category] = len(items)
            if manifest["counts"][category] != len(items):
                fail(errors, f"{level}/{category}: manifest count mismatch")
        report["levels"][level] = counts

    # Oxford words: 5322 normalized records exactly once across A1-C1.
    oxford = read("data/derived/oxford-3000-all.json")["records"] + read("data/derived/oxford-5000-all.json")["records"]
    source_word_ids = [r["record_id"] for r in oxford]
    inventory_word_ids = [r["source_ref"] for level in LEVELS[:-1] for r in read(f"curriculum/levels/{level}/words.json")["items"]]
    report["coverage"]["oxford_words"] = {"source": len(source_word_ids), "inventory": len(inventory_word_ids), "unique_inventory": len(set(inventory_word_ids))}
    if len(source_word_ids) != 5322 or len(set(source_word_ids)) != 5322 or inventory_word_ids.__len__() != 5322 or set(inventory_word_ids) != set(source_word_ids):
        fail(errors, "Oxford words are not a one-to-one 5322-record A1-C1 partition")

    # Oxford phrases: current official 750 exactly once across A1-C1.
    source_phrase_ids = {r["record_id"] for r in read("data/derived/oxford-phrase-list-online.json")["records"]}
    inventory_phrase_ids = [r["item_id"] for level in LEVELS[:-1] for r in read(f"curriculum/levels/{level}/phrases.json")["items"]]
    report["coverage"]["oxford_phrases"] = {"source": len(source_phrase_ids), "inventory": len(inventory_phrase_ids), "unique_inventory": len(set(inventory_phrase_ids))}
    if len(source_phrase_ids) != 750 or len(inventory_phrase_ids) != 750 or set(inventory_phrase_ids) != source_phrase_ids:
        fail(errors, "Oxford phrases are not a one-to-one 750-record A1-C1 partition")

    # Pearson C2: 623 primary records split into 609 lexical + 14 direct phrase owners;
    # 27 collocations are attached secondary phrase/chunk evidence.
    c2_source_ids = {r["itemId"] for r in read("data/derived/gse-vocabulary-c2-gl.json")["records"]}
    c2_words = read("curriculum/levels/c2/words.json")["items"]
    c2_phrases = read("curriculum/levels/c2/phrases.json")["items"]
    c2_word_ids = {r["source_ref"]["item_id"] for r in c2_words}
    c2_direct_ids = {r["source_ref"]["item_id"] for r in c2_phrases if r["subtype"] in {"source_phrase", "source_phrasal_verb"}}
    c2_collocations = [r for r in c2_phrases if r["subtype"] == "collocation"]
    report["coverage"]["pearson_c2"] = {"source": len(c2_source_ids), "words": len(c2_word_ids), "direct_phrases": len(c2_direct_ids), "collocations": len(c2_collocations)}
    if len(c2_source_ids) != 623 or len(c2_word_ids) != 609 or len(c2_direct_ids) != 14 or len(c2_collocations) != 27 or (c2_word_ids | c2_direct_ids) != c2_source_ids or (c2_word_ids & c2_direct_ids):
        fail(errors, "Pearson C2 lexical ownership mismatch")

    # EGP: 1222 canonical features exactly once across A1-C2.
    egp_source = read("data/derived/egp-all-levels.json")["records"]
    egp_source_rows = {r["_source"]["spreadsheet_row"] for r in egp_source}
    egp_inventory_rows = [r["source_ref"]["spreadsheet_row"] for level in LEVELS for r in read(f"curriculum/levels/{level}/grammar.json")["items"]]
    report["coverage"]["egp"] = {"source": len(egp_source_rows), "inventory": len(egp_inventory_rows), "unique_inventory": len(set(egp_inventory_rows))}
    if len(egp_source_rows) != 1222 or len(egp_inventory_rows) != 1222 or set(egp_inventory_rows) != egp_source_rows:
        fail(errors, "EGP 1222-feature partition mismatch")

    # GSE Grammar: reviewed crosswalk covers all 456 source records; Pre-A1 stays outside
    # the six folders, while every A1-C2 crosscheck record appears once.
    grammar_review = read("data/reviewed/grammar-family-strands-v1.json")
    gse_source_ids = {r["record_id"] for r in read("data/derived/gse-grammar-all.json")["records"]}
    crosswalk = grammar_review["gse_crosswalk"]
    crosswalk_ids = [r["source_record_id"] for r in crosswalk]
    pre_a1_gse: set[str] = set()
    expected_gse: set[str] = set()
    for row in crosswalk:
        levels = row["source_level_codes"]
        if len(levels) != 1:
            fail(errors, f"GSE Grammar non-singleton level: {row['source_record_id']}")
            continue
        if levels[0] == "pre_a1":
            pre_a1_gse.add(row["source_record_id"])
        elif levels[0] in LEVELS:
            expected_gse.add(row["source_record_id"])
        else:
            fail(errors, f"GSE Grammar unexpected level {levels[0]}")
    inventory_gse = [r["evidence_id"] for level in LEVELS for r in read(f"curriculum/levels/{level}/grammar.json").get("gse_crosscheck_evidence", [])]
    family_ids = {r["family_id"] for r in grammar_review["families"]}
    family_pairs = [(level, r["family_id"]) for level in LEVELS for r in read(f"curriculum/levels/{level}/grammar.json").get("grammar_family_stages", [])]
    report["coverage"]["gse_grammar"] = {"source": len(gse_source_ids), "pre_a1": len(pre_a1_gse), "expected_a1_c2": len(expected_gse), "inventory": len(inventory_gse), "families": len(family_ids), "family_stages": len(family_pairs)}
    if len(gse_source_ids) != 456 or len(crosswalk_ids) != 456 or set(crosswalk_ids) != gse_source_ids:
        fail(errors, "GSE Grammar reviewed crosswalk is not one-to-one with 456 source records")
    if len(inventory_gse) != len(expected_gse) or set(inventory_gse) != expected_gse:
        fail(errors, f"GSE Grammar A1-C2 inventory mismatch: expected {len(expected_gse)}, got {len(inventory_gse)}")
    expected_pairs = {(level, family_id) for level in LEVELS for family_id in family_ids}
    if len(family_ids) != 91 or len(family_pairs) != 546 or set(family_pairs) != expected_pairs:
        fail(errors, "Grammar family stage coverage mismatch")

    # Communicative abilities: all 2274 reviewed assignments dispositioned, with 106 Pre-A1
    # intentionally outside the six folders and all A1-C2 records represented exactly once.
    assignments = read("data/reviewed/communicative-tag-assignments-v1.json")["records"]
    valid_strands = {s["strand_id"] for s in read("data/reviewed/communicative-function-strands-v1.json")["strands"]}
    expected: dict[tuple[str, str], set[str]] = {}
    pre_a1_abilities = 0
    for row in assignments:
        levels = row["source_level_codes"]
        if len(levels) != 1:
            fail(errors, f"Ability non-singleton level: {row['source_record_id']}")
            continue
        level = levels[0]
        if level == "pre_a1":
            pre_a1_abilities += 1
            continue
        role = row["source_disposition"]
        if level not in LEVELS or role not in ROLES:
            fail(errors, f"Ability unexpected level/role: {level}/{role}")
            continue
        expected.setdefault((level, role), set()).add(row["source_record_id"])
    actual_total = 0
    ability_counts: dict[str, dict[str, int]] = {}
    for level in LEVELS:
        data = read(f"curriculum/levels/{level}/abilities.json")
        buckets = {"include_for_spine": data["items"], "supporting_evidence": data["supporting_evidence"], "duplicate_or_overlap": data["excluded_duplicate_or_overlap"]}
        level_seen: list[str] = []
        ability_counts[level] = {}
        for role, items in buckets.items():
            ids = [r["source_record_id"] for r in items]
            actual_total += len(ids)
            level_seen.extend(ids)
            ability_counts[level][role] = len(ids)
            if set(ids) != expected.get((level, role), set()) or len(ids) != len(set(ids)):
                fail(errors, f"{level} ability {role} one-to-one mismatch")
            for item in items:
                if not item.get("source_text") or not set(item.get("strand_ids", [])).issubset(valid_strands):
                    fail(errors, f"{level} ability invalid provenance/strand: {item['source_record_id']}")
        if len(level_seen) != len(set(level_seen)):
            fail(errors, f"{level} ability appears in multiple disposition buckets")
    report["coverage"]["abilities"] = {"source": len(assignments), "pre_a1": pre_a1_abilities, "expected_a1_c2": len(assignments) - pre_a1_abilities, "inventory": actual_total, "strands": len(valid_strands), "by_level": ability_counts}
    if len(assignments) != 2274 or pre_a1_abilities != 106 or actual_total != 2168:
        fail(errors, "Communicative ability coverage totals mismatch")

    # Pronunciation: 10 reviewed strands x 6 level stages.
    pronunciation = read("data/reviewed/pronunciation-progression-strands-v1.json")["strands"]
    strand_ids = {s["strand_id"] for s in pronunciation}
    pairs = [(level, r["strand_id"]) for level in LEVELS for r in read(f"curriculum/levels/{level}/pronunciation.json")["items"]]
    expected_pron = {(level, strand) for level in LEVELS for strand in strand_ids}
    report["coverage"]["pronunciation"] = {"strands": len(strand_ids), "stages": len(pairs), "unique_stages": len(set(pairs))}
    if len(strand_ids) != 10 or len(pairs) != 60 or set(pairs) != expected_pron:
        fail(errors, "Pronunciation 10x6 stage coverage mismatch")

    # Exit contract: preserve all 102 reviewed claims, 17 per level.
    profiles = {row["level"]: collect_claims(row) for row in read("data/reviewed/level-exit-profiles-v1.json")["levels"]}
    exit_total = 0
    exit_counts: dict[str, int] = {}
    for level in LEVELS:
        expected_ids = [r["claim_id"] for r in profiles[level]]
        actual_ids = [r["claim_id"] for r in read(f"curriculum/levels/{level}/exit_contract.json").get("exit_profile_claims", [])]
        exit_counts[level] = len(actual_ids)
        exit_total += len(actual_ids)
        if actual_ids != expected_ids:
            fail(errors, f"{level}: exit-profile claim preservation mismatch")
    report["coverage"]["exit_profiles"] = {"inventory": exit_total, "by_level": exit_counts}
    if exit_total != 102 or any(count != 17 for count in exit_counts.values()):
        fail(errors, "Exit-profile 102-claim coverage mismatch")

    print(json.dumps(report, indent=2))
    if errors:
        print("AUDIT ERRORS")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("AUDIT PASS")


if __name__ == "__main__":
    main()
