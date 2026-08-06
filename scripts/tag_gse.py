"""Deterministic normalized tags for Pearson GSE A1 objectives."""

from __future__ import annotations

try:
    from scripts.tag_model import TagDecision
except ModuleNotFoundError:
    from tag_model import TagDecision


SKILLS = {
    "Reading": ("reading",),
    "Listening": ("listening",),
    "Speaking": ("speaking",),
    "Writing": ("writing",),
}


def _reading_functions(text: str) -> set[str]:
    if "directions" in text or "instructions" in text:
        return {"follow_instructions"}
    if "extract personal details" in text:
        return {"locate_information"}
    return {"comprehend_information"}


def _listening_functions(text: str) -> set[str]:
    if any(word in text for word in ("instructions", "commands", "directions")):
        return {"follow_instructions"}
    if "transactions" in text:
        return {"transact"}
    locating = ("identify", "extract", "recognise", "key information")
    if any(word in text for word in locating):
        return {"locate_information"}
    return {"comprehend_information"}


def _speaking_functions(text: str) -> set[str]:
    tags: set[str] = set()
    if "introduc" in text:
        tags.add("introduce")
    if any(term in text for term in ("greet", "greeting", "leave-taking", "react to news", "politely")):
        tags.add("socialize")
    if "preference" in text or "likes and dislikes" in text:
        tags.add("express_preference")
    if "feeling" in text:
        tags.add("express_feeling")
    if "ability or lack of ability" in text or "can or can’t do" in text:
        tags.add("express_ability")
    if "accept offers" in text or "agree to simple requests" in text:
        tags.add("respond_to_request_or_offer")
    request_terms = (
        "ask for the spelling", "ask for a drink", "ask for help", "ask for things",
        "ask people for things", "ask for attention", "ask for simple directions",
        "make a few basic requests", "describe wants and needs",
    )
    if any(term in text for term in request_terms):
        tags.add("request")
    if any(term in text for term in ("buy tickets", "check into a hotel")):
        tags.add("transact")
    if "request information" in text:
        tags.add("ask_for_information")
    exchange_terms = (
        "ask and answer", "exchange personal", "ask basic questions", "ask simple questions",
        "answer simple questions", "ask for and give very basic information",
    )
    if any(term in text for term in exchange_terms):
        tags.add("exchange_information")
    if "repeat clearly spoken" in text or "read aloud" in text:
        tags.add("reproduce_language")
    if ("describe" in text and "describe wants and needs" not in text) or "talk about" in text:
        tags.add("describe")
    if "describe wants and needs" in text:
        tags.add("give_information")
    if "give people things" in text:
        tags.add("respond_to_request_or_offer")
    if not tags or any(term in text for term in ("say where", "tell the time", "give dates", "indicate time")):
        tags.add("give_information")
    return tags


def _writing_functions(text: str) -> set[str]:
    if "complete" in text and "form" in text:
        return {"complete_form"}
    if any(term in text for term in ("notes, emails", "postings to friends")):
        return {"correspond"}
    if "copy" in text or "spell" in text:
        return {"reproduce_language"}
    if "capital letters" in text or "punctuation" in text:
        return {"control_language_form"}
    if "describ" in text:
        return {"describe"}
    return {"give_information"}


def tag_gse(record: dict) -> TagDecision:
    skill = record["source_facts"]["skill_text"]
    text = record["source"]["source_text"].lower()
    if skill == "Reading":
        functions = _reading_functions(text)
    elif skill == "Listening":
        functions = _listening_functions(text)
    elif skill == "Speaking":
        functions = _speaking_functions(text)
    elif skill == "Writing":
        functions = _writing_functions(text)
    else:
        raise ValueError(f"Unsupported GSE source skill: {skill!r}")

    if skill in {"Reading", "Listening"}:
        modes = {"reception"}
    elif skill == "Writing" and "correspond" in functions:
        modes = {"interaction"}
    elif skill == "Speaking" and functions & {
        "ask_for_information", "exchange_information", "socialize", "request",
        "respond_to_request_or_offer", "transact",
    }:
        modes = {"interaction"}
    else:
        modes = {"production"}
    decision = TagDecision(SKILLS[skill], tuple(sorted(modes)), tuple(sorted(functions)))
    decision.validate()
    return decision
