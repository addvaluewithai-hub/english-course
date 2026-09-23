#!/usr/bin/env python3
"""Build reviewed level-inventory candidates from normalized and reviewed source data."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
C2_PHRASE_CATEGORIES = {"phrase", "phrasal verb"}
PEARSON_LICENSE_GATE = "commercial_permission_required"


def read(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def collect_claims(node: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if "claim_id" in node and "text" in node:
            out.append({
                k: node[k]
                for k in ("claim_id", "claim_type", "text", "evidence_bundle_ids", "decision_refs")
                if k in node
            })
        else:
            for value in node.values():
                out.extend(collect_claims(value))
    elif isinstance(node, list):
        for value in node:
            out.extend(collect_claims(value))
    return out


def word_item(record: dict[str, Any]) -> dict[str, Any]:
    facts = record["source_facts"]
    meta = facts["other_verbatim"]
    return {
        "item_id": record["record_id"],
        "headword": meta.get("headword"),
        "headword_source": meta.get("headword_source"),
        "part_of_speech": meta.get("part_of_speech"),
        "homograph_number": meta.get("homograph_number"),
        "qualifier": meta.get("qualifier"),
        "published_level": facts["level_text"],
        "source_ref": record["record_id"],
    }


def phrase_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": record["record_id"],
        "phrase": record["phrase"],
        "published_level": record["level"],
        "source_ref": {"dataset": "oxford_phrase_list_online", "href": record.get("href")},
    }


def c2_is_phrase(record: dict[str, Any]) -> bool:
    return bool(C2_PHRASE_CATEGORIES.intersection(record.get("grammaticalCategories") or []))


def c2_word_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": f"gse.vocab.{record['itemId']}",
        "expression": record.get("expression"),
        "definition": record.get("definition"),
        "example": record.get("example"),
        "grammatical_categories": record.get("grammaticalCategories") or [],
        "gse": record.get("gse"),
        "cefr": record.get("cefr"),
        "variants": record.get("variants") or [],
        "region": record.get("region"),
        "published_level": "C2",
        "source_ref": {
            "dataset": "pearson_gse_vocabulary_c2_general_learner",
            "item_id": record["itemId"],
        },
        "license_gate": PEARSON_LICENSE_GATE,
    }


def c2_phrase_items(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for record in records:
        categories = record.get("grammaticalCategories") or []
        if c2_is_phrase(record):
            subtype = "source_phrasal_verb" if "phrasal verb" in categories else "source_phrase"
            items.append({
                "item_id": f"gse.vocab.{record['itemId']}",
                "phrase": record.get("expression"),
                "subtype": subtype,
                "definition": record.get("definition"),
                "example": record.get("example"),
                "gse": record.get("gse"),
                "cefr": record.get("cefr"),
                "published_level": "C2",
                "independent_gse_score": True,
                "source_ref": {
                    "dataset": "pearson_gse_vocabulary_c2_general_learner",
                    "item_id": record["itemId"],
                },
                "license_gate": PEARSON_LICENSE_GATE,
            })
        for index, collocation in enumerate(record.get("collos") or [], start=1):
            text = collocation if isinstance(collocation, str) else None
            if not text:
                continue
            items.append({
                "item_id": f"gse.c2.collocation.{record['itemId']}.{index}",
                "phrase": text,
                "subtype": "collocation",
                "owner_item_id": record["itemId"],
                "owner_expression": record.get("expression"),
                "gse": record.get("gse"),
                "cefr": record.get("cefr"),
                "published_level": "C2",
                "level_inheritance": "owner_record",
                "independent_gse_score": False,
                "source_ref": {
                    "dataset": "pearson_gse_vocabulary_c2_general_learner",
                    "owner_item_id": record["itemId"],
                    "collocation_index": index,
                },
                "license_gate": PEARSON_LICENSE_GATE,
            })
    return items


def grammar_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": f"egp.{record['id']}",
        "super_category": clean(record.get("SuperCategory")),
        "sub_category": clean(record.get("SubCategory")),
        "guideword": clean(record.get("Guideword")),
        "can_do": clean(record.get("Can-do statement")),
        "lexical_range": clean(record.get("Lexical Range")),
        "published_level": clean(record.get("Level")),
        "source_ref": {"dataset": "egp_all_levels", "spreadsheet_row": record["_source"]["spreadsheet_row"]},
    }


def main() -> None:
    ox3 = read("data/derived/oxford-3000-all.json")["records"]
    ox5 = read("data/derived/oxford-5000-all.json")["records"]
    phrase_source = read("data/derived/oxford-phrase-list-online.json")
    phrases = phrase_source["records"]
    gse_c2_source = read("data/derived/gse-vocabulary-c2-gl.json")
    gse_c2 = gse_c2_source["records"]
    egp = read("data/derived/egp-all-levels.json")["records"]
    profiles = read("data/reviewed/level-exit-profiles-v1.json")["levels"]
    pronunciation = read("data/reviewed/pronunciation-progression-strands-v1.json")["strands"]
    profile_by_level = {x["level"]: x for x in profiles}

    if phrase_source["record_count"] != 750 or len(phrases) != 750:
        raise SystemExit("Current Oxford Phrase List snapshot must contain exactly 750 extracted rows")
    if gse_c2_source["record_count"] != 623 or len(gse_c2) != 623:
        raise SystemExit("Pearson C2 General Learner snapshot must contain exactly 623 records")

    for level in LEVELS:
        folder = ROOT / "curriculum" / "levels" / level
        level_upper = level.upper()

        if level == "c2":
            word_records = [r for r in gse_c2 if not c2_is_phrase(r)]
            word_items = [c2_word_item(r) for r in word_records]
            words_status = "extracted_from_official_gse_pending_inventory_review_and_license_gate"
        else:
            word_records: list[dict[str, Any]] = []
            if level in {"a1", "a2", "b1", "b2"}:
                word_records.extend(r for r in ox3 if level in r["interpretation"]["cefr_codes"])
            if level in {"b2", "c1"}:
                word_records.extend(r for r in ox5 if level in r["interpretation"]["cefr_codes"])
            word_items = [word_item(r) for r in word_records]
            words_status = "extracted_pending_inventory_review"
        write(folder / "words.json", {
            "schema_version": 1,
            "level": level_upper,
            "category": "words",
            "inventory_semantics": "new_at_level",
            "status": words_status,
            "canonical_source": "Pearson GSE Vocabulary C2 General Learner" if level == "c2" else "Oxford 3000/5000",
            "license_gate": PEARSON_LICENSE_GATE if level == "c2" else None,
            "items": word_items,
        })

        if level == "c2":
            phrase_items = c2_phrase_items(gse_c2)
            phrase_status = "extracted_from_official_gse_pending_inventory_review_and_license_gate"
            phrase_source_name = "Pearson GSE Vocabulary C2 General Learner"
            phrase_hash = gse_c2_source.get("normalized_records_sha256")
        else:
            phrase_records = [r for r in phrases if r["level"].lower() == level]
            phrase_items = [phrase_item(r) for r in phrase_records]
            phrase_status = "extracted_from_current_official_oxford_pending_inventory_review"
            phrase_source_name = "Oxford Phrase List online snapshot"
            phrase_hash = phrase_source.get("source_sha256")
        write(folder / "phrases.json", {
            "schema_version": 1,
            "level": level_upper,
            "category": "phrases",
            "inventory_semantics": "new_at_level",
            "status": phrase_status,
            "canonical_source": phrase_source_name,
            "source_sha256": phrase_hash,
            "license_gate": PEARSON_LICENSE_GATE if level == "c2" else None,
            "items": phrase_items,
        })

        grammar = [grammar_item(r) for r in egp if (clean(r.get("Level")) or "").lower() == level]
        write(folder / "grammar.json", {
            "schema_version": 1,
            "level": level_upper,
            "category": "grammar",
            "inventory_semantics": "new_at_level",
            "status": "extracted_pending_inventory_review",
            "canonical_source": "English Grammar Profile",
            "items": grammar,
        })

        profile = profile_by_level[level]
        claims = collect_claims(profile)
        write(folder / "abilities.json", {
            "schema_version": 1,
            "level": level_upper,
            "category": "abilities",
            "status": "reviewed_exit_profile_v1",
            "source_ref": "data/reviewed/level-exit-profiles-v1.json",
            "items": claims,
        })

        stages = []
        for strand in pronunciation:
            stage = next(s for s in strand["stages"] if s["level"] == level)
            stages.append({
                "item_id": f"{strand['strand_id']}.{level}",
                "strand_id": strand["strand_id"],
                "title": strand["title"],
                "expectation": stage["expectation"],
                "exit_boundary": stage["exit_boundary"],
                "control_focus": stage["control_focus"],
                "lifecycle_states": stage["lifecycle_states"],
                "profile_claim_id": stage["profile_claim_id"],
                "representative_cefr_evidence_ids": stage["representative_cefr_evidence_ids"],
            })
        write(folder / "pronunciation.json", {
            "schema_version": 1,
            "level": level_upper,
            "category": "pronunciation",
            "status": "reviewed_progression_v1",
            "source_ref": "data/reviewed/pronunciation-progression-strands-v1.json",
            "items": stages,
        })

        cumulative = [x.upper() for x in LEVELS[: LEVELS.index(level) + 1]]
        assessment = [x for x in claims if x["claim_type"] == "product_policy"]
        write(folder / "exit_contract.json", {
            "schema_version": 1,
            "level": level_upper,
            "status": "draft_pending_full_inventory_lock",
            "inventory_semantics": {"level_files": "new_at_level", "exit_obligation": "cumulative_through_level"},
            "cumulative_levels": cumulative,
            "principles": {"completion_is_not_mastery": True, "retention_requires_later_fresh_evidence": True},
            "inventory_obligations": {
                "words": words_status,
                "phrases": phrase_status,
                "grammar": "extracted_pending_inventory_review",
                "abilities": "reviewed_exit_profile_v1",
                "pronunciation": "reviewed_progression_v1",
            },
            "production_gates": [PEARSON_LICENSE_GATE] if level == "c2" else [],
            "assessment_requirements": assessment,
        })

        manifest = {
            "schema_version": 1,
            "level": level_upper,
            "status": "generated_pending_inventory_review",
            "source_of_truth_version": "v1",
            "inventory_semantics": "new_at_level_with_cumulative_exit_contract",
            "categories": ["words", "phrases", "grammar", "abilities", "pronunciation"],
            "lesson_design_authorized": False,
            "counts": {
                "words": len(word_items),
                "phrases": len(phrase_items),
                "grammar": len(grammar),
                "abilities": len(claims),
                "pronunciation": len(stages),
            },
            "blocking_categories": [],
            "production_gates": [PEARSON_LICENSE_GATE] if level == "c2" else [],
        }
        write(folder / "manifest.json", manifest)


if __name__ == "__main__":
    main()
