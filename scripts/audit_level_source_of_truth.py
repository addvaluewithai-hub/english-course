#!/usr/bin/env python3
"""Audit A1-C2 source-of-truth inventories against their canonical inputs."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
CATEGORIES = ("words", "phrases", "grammar", "abilities", "pronunciation")
ABILITY_ROLES = (
    "include_for_spine",
    "supporting_evidence",
    "duplicate_or_overlap",
)


def read(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    report: dict = {"levels": {}, "cross_source": {}}

    for level in LEVELS:
        folder = ROOT / "curriculum" / "levels" / level
        manifest = read(str(folder.relative_to(ROOT) / "manifest.json"))
        level_report = {"counts": {}, "duplicate_item_ids": {}}
        for category in CATEGORIES:
            data = read(str(folder.relative_to(ROOT) / f"{category}.json"))
            items = data["items"]
            ids = [item.get("item_id") or item.get("claim_id") for item in items]
            duplicate_ids = sorted(k for k, n in Counter(ids).items() if k is not None and n > 1)
            level_report["counts"][category] = len(items)
            level_report["duplicate_item_ids"][category] = duplicate_ids
            if duplicate_ids:
                errors.append(f"{level}/{category}: duplicate item ids {duplicate_ids[:10]}")
            if len(items) != manifest["counts"][category]:
                errors.append(
                    f"{level}/{category}: manifest={manifest['counts'][category]} actual={len(items)}"
                )
        report["levels"][level] = level_report

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
    if set(inventory_phrase_ids) != source_phrase_ids or len(inventory_phrase_ids) != len(source_phrase_ids):
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

    ability_report: dict[str, dict] = {}
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

    print(json.dumps(report, indent=2))
    if errors:
        print("AUDIT ERRORS")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("AUDIT PASS")


if __name__ == "__main__":
    main()
