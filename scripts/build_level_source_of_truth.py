#!/usr/bin/env python3
"""Build reviewed level-inventory candidates from normalized and reviewed source data."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")


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
        "source_ref": {
            "dataset": "oxford_phrase_list_online",
            "href": record.get("href"),
        },
    }


def grammar_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": f"egp.{record['id']}",
        "super_category": clean(record.get("SuperCategory")),
        "sub_category": clean(record.get("SubCategory")),
        "guideword": clean(record.get("Guideword")),
        "can_do": clean(record.get("Can-do statement")),
        "lexical_range": clean(record.get("Lexical Range")),
        "published_level": clean(record.get("Level")),
        "source_ref": {
            "dataset": "egp_all_levels",
            "spreadsheet_row": record["_source"]["spreadsheet_row"],
        },
    }


def main() -> None:
    ox3 = read("data/derived/oxford-3000-all.json")["records"]
    ox5 = read("data/derived/oxford-5000-all.json")["records"]
    phrase_source = read("data/derived/oxford-phrase-list-online.json")
    phrases = phrase_source["records"]
    egp = read("data/derived/egp-all-levels.json")["records"]
    profiles = read("data/reviewed/level-exit-profiles-v1.json")["levels"]
    pronunciation = read("data/reviewed/pronunciation-progression-strands-v1.json")["strands"]
    profile_by_level = {x["level"]: x for x in profiles}

    if phrase_source["record_count"] != 750 or len(phrases) != 750:
        raise SystemExit("Current Oxford Phrase List snapshot must contain exactly 750 extracted rows")

    for level in LEVELS:
        folder = ROOT / "curriculum" / "levels" / level
        level_upper = level.upper()

        word_records: list[dict[str, Any]] = []
        if level in {"a1", "a2", "b1", "b2"}:
            word_records.extend(r for r in ox3 if level in r["interpretation"]["cefr_codes"])
        if level in {"b2", "c1"}:
            word_records.extend(r for r in ox5 if level in r["interpretation"]["cefr_codes"])
        words_status = (
            "extracted_pending_inventory_review"
            if level != "c2"
            else "blocked_pending_gse_vocabulary_extract"
        )
        write(folder / "words.json", {
            "schema_version": 1,
            "level": level_upper,
            "category": "words",
            "inventory_semantics": "new_at_level",
            "status": words_status,
            "items": [word_item(r) for r in word_records],
        })

        phrase_records = [r for r in phrases if r["level"].lower() == level]
        phrase_status = (
            "extracted_from_current_official_oxford_pending_inventory_review"
            if level != "c2"
            else "blocked_pending_gse_vocabulary_extract"
        )
        write(folder / "phrases.json", {
            "schema_version": 1,
            "level": level_upper,
            "category": "phrases",
            "inventory_semantics": "new_at_level",
            "status": phrase_status,
            "canonical_source": (
                "Oxford Phrase List online snapshot"
                if level != "c2"
                else "pending C2 lexical source"
            ),
            "source_sha256": phrase_source.get("source_sha256") if level != "c2" else None,
            "items": [phrase_item(r) for r in phrase_records],
        })

        grammar = [
            grammar_item(r)
            for r in egp
            if (clean(r.get("Level")) or "").lower() == level
        ]
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
            "inventory_semantics": {
                "level_files": "new_at_level",
                "exit_obligation": "cumulative_through_level",
            },
            "cumulative_levels": cumulative,
            "principles": {
                "completion_is_not_mastery": True,
                "retention_requires_later_fresh_evidence": True,
            },
            "inventory_obligations": {
                "words": words_status,
                "phrases": phrase_status,
                "grammar": "extracted_pending_inventory_review",
                "abilities": "reviewed_exit_profile_v1",
                "pronunciation": "reviewed_progression_v1",
            },
            "assessment_requirements": assessment,
        })

        blocking = []
        for name, state in {"words": words_status, "phrases": phrase_status}.items():
            if state.startswith("blocked_"):
                blocking.append(name)
        manifest = {
            "schema_version": 1,
            "level": level_upper,
            "status": "generated_pending_inventory_review",
            "source_of_truth_version": "v1",
            "inventory_semantics": "new_at_level_with_cumulative_exit_contract",
            "categories": ["words", "phrases", "grammar", "abilities", "pronunciation"],
            "lesson_design_authorized": False,
            "counts": {
                "words": len(word_records),
                "phrases": len(phrase_records),
                "grammar": len(grammar),
                "abilities": len(claims),
                "pronunciation": len(stages),
            },
            "blocking_categories": blocking,
        }
        write(folder / "manifest.json", manifest)


if __name__ == "__main__":
    main()
