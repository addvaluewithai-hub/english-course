#!/usr/bin/env python3
"""Add a lexical/content-bank layer to the A1 performance cluster spine.

Performance clusters answer: what can the learner do?
Content banks answer: where does required language naturally live?

The layer is intentionally separate so every source-of-truth item can receive a teaching
home without inventing a communicative ability for every noun/adjective. Existing reviewed
cluster homes are preserved. Previously orphaned lexical items are assigned by explicit,
auditable semantic rules; low-confidence fallbacks remain visible in the report.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
A1 = ROOT / "curriculum/levels/a1"
OUT = A1 / "curriculum-map"


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


BANKS = {
    "identity_personal_information": "Names, personal details, identity, origin and basic roles.",
    "people_relationships": "People, family, relationships, jobs and social description.",
    "home_objects_descriptions": "Home, rooms, everyday objects and visible description.",
    "routines_time_leisure": "Daily routines, time, frequency, leisure and recurring activities.",
    "food_shopping_services": "Food, drink, prices, shopping, ordering and everyday services.",
    "places_directions_travel": "Places, geography, transport, movement, travel and directions.",
    "messages_signs_forms": "Forms, written messages, signs, texts and basic information media.",
    "social_contact_collaboration": "Greetings, reactions, politeness, invitations and collaboration.",
    "communication_strategies": "Repair, clarification, checking meaning and managing communication.",
    "language_foundations": "Function words, grammatical forms and language-system building blocks.",
    "study_work_learning": "School, study, work, professions, learning activities and institutions.",
    "arts_media_culture": "Arts, music, media, entertainment, culture and creative activity.",
    "health_body_wellbeing": "Body, health, physical condition, exercise and wellbeing.",
    "nature_animals_environment": "Animals, plants, natural world, weather and environment.",
    "description_opinion_comparison": "General describing, evaluation, qualities, preferences and comparison.",
    "thinking_actions_information": "General actions, processes, thinking, information and change.",
    "numbers_quantity_measurement": "Numbers, amounts, measurement, scale and quantitative expressions.",
}

# Explicit candidate classification for words that had no reviewed lexical home in the old design.
# These sets are architecture candidates, not dictionary-sense claims.
WORD_SETS = {
    "people_relationships": set("actor actress baby dad dancer farmer member model mum policeman scientist singer teenager visitor writer".split()),
    "study_work_learning": set("career classroom company exam geography interview practice project science skill subject teach test university".split()),
    "arts_media_culture": set("art article artist band blog cd club culture dancing dialogue dvd guitar history magazine movie newspaper paint painting photograph piano programme reader reading song theatre title writing".split()),
    "food_shopping_services": set("beer butter carrot cheese chocolate cooking cream diet dish ice onion pepper potato shopping tomato wine".split()) | {"ice cream"},
    "health_body_wellbeing": set("body die exercise fat feeling health healthy nose".split()),
    "nature_animals_environment": set("air cow elephant fire flower land lion mountain mouse natural pig plant sheep snake space star tree world".split()),
    "places_directions_travel": set("bike boat east kilometre local mile north ride south vacation west".split()),
    "routines_time_leisure": set("ago future midnight moment never often once relax spend still twice usually".split()),
    "numbers_quantity_measurement": set("cent century metre million thousand".split()),
    "description_opinion_comparison": set("amazing angry better bored common cool correct dangerous excited exciting extra famous fantastic fast full hard important interest interested kind main modern negative perfect personal popular positive possible poor pretty quick quickly quite real really rich similar slow special strong success terrible useful wonderful".split()),
    "thinking_actions_information": set("add become begin beginning believe break build change climb compare create cut decide describe description design difference discuss draw enjoy even ever explain fact fall fill final fly forget grow guess happen hate hope however imagine improve include introduce join just know laugh let lie life line maybe miss mistake move object only opinion pair paper paragraph part plan point prefer prepare present probably reason remember report result rule section sell share show situation style talk together type win yeah".split()),
    "messages_signs_forms": set("chart online telephone".split()),
    "home_objects_descriptions": set("boot machine umbrella upstairs downstairs".split()),
}

PHRASE_PREFIX_RULES = [
    (("at home", "in bed", "on the floor", "over there"), "home_objects_descriptions"),
    (("at school", "in class", "in school", "at university", "high school", "go to school"), "study_work_learning"),
    (("at work", "go to work", "work as", "work for", "work hard", "work together", "work with"), "study_work_learning"),
    (("for lunch", "pay for", "how much", "too much"), "food_shopping_services"),
    (("at the weekend", "have fun", "on holiday", "on the beach", "swimming pool"), "routines_time_leisure"),
    (("at the moment", "at the same time", "for a long time", "for a moment", "for the first time", "last time", "next time", "right now", "this morning", "this time", "once a", "x times a"), "routines_time_leisure"),
    (("in the north", "in the street", "town centre", "car park", "go back", "go home", "go into", "go out", "come into", "out of", "on the left"), "places_directions_travel"),
    (("good morning", "no problem", "oh yes", "see you", "welcome to", "would like", "would you like"), "social_contact_collaboration"),
    (("phone call", "on the phone", "speak to", "talk about", "listen to", "look at", "look for", "find out"), "communication_strategies"),
    (("family member", "live with", "each other", "he or she", "his or her", "someone else"), "people_relationships"),
    (("a few", "a little", "a lot", "a lot of", "lots of", "millions of", "thousands of", "more than"), "numbers_quantity_measurement"),
    (("good at", "bad for", "good for", "important for", "in my opinion", "pretty good", "really good", "really like", "really enjoy", "too long", "kind of", "this kind of"), "description_opinion_comparison"),
    (("because of", "in fact", "such as", "differences between", "think about", "think of", "know how", "plan for", "it is important"), "thinking_actions_information"),
]


def explicit_word_bank(headword: str) -> str | None:
    h = headword.lower()
    for bank, words in WORD_SETS.items():
        if h in words:
            return bank
    return None


def phrase_rule_bank(phrase: str) -> str | None:
    p = phrase.lower().replace("…", "").strip()
    for prefixes, bank in PHRASE_PREFIX_RULES:
        if any(p.startswith(prefix) for prefix in prefixes):
            return bank
    return None


def main() -> None:
    cluster_map = read(OUT / "cluster-map-v0.json")
    mappings = cluster_map["item_mappings"]

    word_by_headword: dict[str, dict[str, Any]] = {}
    fallback_words = []
    for row in mappings["words"]:
        homes = list(row["candidate_cluster_ids"])
        if row["mapping_basis"] == "grammar_owned_cross_cutting":
            homes = ["language_foundations"]
            basis = "grammar_owned_to_language_foundations"
        elif homes:
            basis = "preserved_reviewed_natural_home"
        else:
            bank = explicit_word_bank(row["headword"])
            if bank:
                homes = [bank]
                basis = "explicit_semantic_bank_rule"
            else:
                homes = ["thinking_actions_information"]
                basis = "general_high_utility_fallback_needs_review"
                fallback_words.append(row["item_id"])
        row["content_bank_ids"] = homes
        row["content_bank_basis"] = basis
        word_by_headword[row["headword"].lower()] = row

    fallback_phrases = []
    for row in mappings["phrases"]:
        homes = list(row["candidate_cluster_ids"])
        if homes:
            basis = "preserved_reviewed_natural_home"
        else:
            bank = None
            source_headword = (row.get("source_headword") or "").lower()
            owner = word_by_headword.get(source_headword)
            if owner:
                owner_homes = owner.get("content_bank_ids", [])
                if owner_homes and owner.get("content_bank_basis") != "general_high_utility_fallback_needs_review":
                    bank = owner_homes[0]
                    basis = "inherits_nonfallback_source_headword_bank"
            if not bank:
                bank = phrase_rule_bank(row["phrase"])
                basis = "explicit_phrase_pattern_rule" if bank else "general_high_utility_fallback_needs_review"
            if not bank:
                bank = "thinking_actions_information"
                fallback_phrases.append(row["item_id"])
            homes = [bank]
        row["content_bank_ids"] = homes
        row["content_bank_basis"] = basis

    for row in mappings["grammar"]:
        homes = list(row["candidate_cluster_ids"])
        if not homes:
            guide = (row.get("guideword") or "").lower()
            cando = (row.get("can_do") or "").lower()
            text = guide + " " + cando
            if "best friend" in text:
                homes = ["people_relationships"]
            elif "time" in text and "soon" in text:
                homes = ["routines_time_leisure"]
            else:
                homes = ["language_foundations"]
            basis = "explicit_grammar_orphan_rule"
        else:
            basis = "preserved_reviewed_natural_home"
        row["content_bank_ids"] = homes
        row["content_bank_basis"] = basis

    for row in mappings["abilities"]:
        row["performance_cluster_ids"] = list(row["candidate_cluster_ids"])

    bank_items = {bank: {"words": [], "phrases": [], "grammar": []} for bank in BANKS}
    for kind in ("words", "phrases", "grammar"):
        for row in mappings[kind]:
            for bank in row["content_bank_ids"]:
                if bank not in bank_items:
                    bank_items[bank] = {"words": [], "phrases": [], "grammar": []}
                bank_items[bank][kind].append(row["item_id"])

    banks = []
    for bank_id, description in BANKS.items():
        items = bank_items.get(bank_id, {"words": [], "phrases": [], "grammar": []})
        banks.append({
            "bank_id": bank_id,
            "description": description,
            "counts": {k: len(v) for k, v in items.items()},
            "item_ids": items,
        })

    report = {
        "schema_version": 1,
        "level": "A1",
        "status": "content_bank_v0_needs_architecture_review",
        "lesson_design_authorized": False,
        "architecture": {
            "performance_spine": "119 required abilities mapped to reviewed capability clusters",
            "language_coverage_lane": "900 words + 199 phrases + 109 EGP features mapped to content banks",
            "lesson_design_rule": "Future lessons must combine a performance purpose with bounded language-bank load; neither lane may silently drop items.",
        },
        "coverage": {
            "words": {"total": len(mappings["words"]), "with_bank": sum(bool(r["content_bank_ids"]) for r in mappings["words"]), "fallback_needs_review": len(fallback_words)},
            "phrases": {"total": len(mappings["phrases"]), "with_bank": sum(bool(r["content_bank_ids"]) for r in mappings["phrases"]), "fallback_needs_review": len(fallback_phrases)},
            "grammar": {"total": len(mappings["grammar"]), "with_bank": sum(bool(r["content_bank_ids"]) for r in mappings["grammar"])},
            "abilities": {"total": len(mappings["abilities"]), "with_performance_cluster": sum(bool(r["performance_cluster_ids"]) for r in mappings["abilities"])},
        },
        "bank_loads": sorted([
            {"bank_id": b["bank_id"], **b["counts"], "total_language_refs": sum(b["counts"].values())}
            for b in banks
        ], key=lambda x: (-x["total_language_refs"], x["bank_id"])),
        "fallback_review": {
            "word_ids": fallback_words,
            "phrase_ids": fallback_phrases,
            "note": "Fallback items are covered structurally but need a better natural home before unit sequencing is locked.",
        },
        "next_gate": "No units yet. First reduce fallback items and resolve overloaded/ambiguous banks; then create unit architecture and lesson-load limits.",
    }

    payload = {
        "schema_version": 1,
        "level": "A1",
        "status": report["status"],
        "lesson_design_authorized": False,
        "content_banks": banks,
        "item_mappings": mappings,
        "principles": {
            "performance_and_language_are_parallel_inputs": True,
            "every_language_item_has_a_bank": True,
            "bank_assignment_is_not_lesson_assignment": True,
            "fallback_is_visible_not_silent": True,
            "unit_count_not_precommitted": True,
        },
    }

    write(OUT / "content-banks-v0.json", payload)
    write(OUT / "content-bank-report-v0.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
