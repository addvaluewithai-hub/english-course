"""Deterministic evidence rules for candidate curriculum clustering."""

from __future__ import annotations

import re
from typing import Any

try:
    from scripts.cluster_model import ordered_cluster_ids
except ModuleNotFoundError:
    from cluster_model import ordered_cluster_ids


TOPIC_PATTERNS = {
    "identity_personal_information": (
        "personal detail", "introduce themselves", "introducing themselves", "name, age",
        "own name", "nationality", "address", "phone number", "date of birth",
        "where they are from", "where they live", "personal details", "introduced to them",
    ),
    "people_relationships": (
        "family", "friends", "people they know", "other people", "job", "jobs",
        "people around", "belongs to", "another person", "names of people",
        "people and places",
    ),
    "routines_time_leisure": (
        "time of day", "times and dates", "times, and dates", "time and date",
        "times and places", "dates and times", "daily activ", "routine", "habit",
        "free time", "hobbies", "interests", "likes and dislikes", "likes/dislikes",
        "preference", "what people say they can", "ability", "weather", "game or sport",
        "next week", "last friday", "in november", "write dates", "write times",
        "give dates", "everyday activities", "daily activities", "life and routines",
        "times, locations", "everyday life", "everyday events", "when and where to meet",
    ),
    "home_objects_descriptions": (
        "everyday objects", "common objects", "descriptions of objects", "describe objects",
        "describe an object", "room looks like", "questions about objects",
        "number of objects", "numbers of objects", "objects in pictures",
        "position of something", "position of things", "where things", "things or people are",
        "about the home", "where they live", "immediate surroundings", "familiar object",
        "colour", "size", "in a picture", "surroundings",
    ),
    "places_directions_travel": (
        "direction", "directions", "from x to y", "public transport", "travel information",
        "landing card", "customs declaration", "check into a hotel", "hotel registration",
        "guided tour", "railway station", "where something is", "descriptions of places",
        "objects, places or people", "place, time", "places and times", "times and places",
        "location of people", "where they and other people are", "map or plan", "travel",
        "locations", "names of people or places", "hotel information", "where to find lifts",
        "when and where to meet",
    ),
    "food_shopping_services": (
        "price", "prices", "cost", "costs", "shopping", "shop)", "salesperson", "food",
        "drink", "buy tickets", "purchase", "transaction", "immediate personal needs",
        "immediate need", "simple needs", "wants and needs", "ask for things",
        "ask for help", "health professional", "does that hurt", "customer", "service",
    ),
    "messages_signs_forms": (
        "notice", "notices", "signs and notices", "postcard", "postcards",
        "simple message", "recorded message", "text message", "messages sent",
        "compose messages", "leave a message", "social media", "e-mail", "email",
        "online posting", "form", "application", "programme", "programmes", "poster",
        "posters", "leaflet", "leaflets", "brochure", "brochures", "advertisement",
        "advertisements", "written instructions", "correspondence", "when and where to meet",
    ),
    "social_contact_collaboration": (
        "greet", "greeting", "farewell", "leave-taking", "how they are", "react to news",
        "feeling", "introduced to someone", "introduce someone", "introduce people",
        "thank", "apology", "sorry", "polite", "offers", "agree to simple requests",
        "show interest", "welcoming attitude", "sympathy", "what others think",
        "introduced to them", "made them feel", "common greetings",
    ),
}

STRATEGY_FUNCTIONS = {
    "clarify_or_repair", "mediate_information", "translate", "facilitate_interaction",
}
FOUNDATION_FUNCTIONS = {"control_language_form", "infer_meaning", "reproduce_language"}


def contains_phrase(text: str, phrase: str) -> bool:
    """Match whole words at phrase edges, avoiding e.g. ``form`` in ``information``."""
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text) is not None


def choose_candidate_clusters(record: dict[str, Any]) -> list[str]:
    """Choose supported clusters from source wording and normalized functions."""
    interpretation = record["interpretation"]
    if interpretation["inclusion_status"] != "included":
        return []

    text = record["source"]["source_text"].casefold()
    functions = set(interpretation["function_codes"])
    selected: set[str] = set()

    for cluster_id, patterns in TOPIC_PATTERNS.items():
        if any(contains_phrase(text, pattern) for pattern in patterns):
            selected.add(cluster_id)

    if functions & {"correspond", "complete_form"}:
        selected.add("messages_signs_forms")
    if functions & STRATEGY_FUNCTIONS:
        selected.add("communication_strategies")
    if functions & FOUNDATION_FUNCTIONS:
        selected.add("language_foundations")
    if "socialize" in functions or "facilitate_interaction" in functions:
        selected.add("social_contact_collaboration")
    if "communicative_competence" in interpretation["mode_codes"]:
        selected.add("language_foundations")
    if "introduce" in functions and not selected & {
        "identity_personal_information", "people_relationships",
    }:
        selected.add("social_contact_collaboration")
    if "request" in functions and any(
        contains_phrase(text, phrase) for phrase in ("spelling", "attention", "help")
    ):
        selected.add("communication_strategies")
    if functions & {"transact", "request", "respond_to_request_or_offer"} and not selected:
        selected.add("food_shopping_services")
    if not selected:
        selected.add("language_foundations")

    return ordered_cluster_ids(selected)
