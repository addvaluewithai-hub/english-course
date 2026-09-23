#!/usr/bin/env python3
"""Audit A1-C2 source-of-truth inventories against their canonical inputs."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
CATEGORIES = ("words", "phrases", "grammar", "abilities", "pronunciation")


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

    # EGP coverage diagnostic: every source row should appear exactly once in grammar inventories.
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

    print(json.dumps(report, indent=2))
    if errors:
        print("AUDIT ERRORS")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("AUDIT PASS")


if __name__ == "__main__":
    main()
