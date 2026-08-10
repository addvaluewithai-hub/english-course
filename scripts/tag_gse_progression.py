"""Deterministic all-level communicative tags for adult GSE objectives."""

from __future__ import annotations

from scripts.progression_tag_model import ProgressionTagDecision, decision


SKILLS = {"Reading": "reading", "Listening": "listening", "Speaking": "speaking", "Writing": "writing"}

ADVANCED_RULES = {
    "narrate": ("narrat", "recount", "tell a story", "sequence of events"),
    "explain": ("explain", "elaborat", "give reasons", "reason for"),
    "express_opinion": ("opinion", "point of view", "viewpoint", "personal view"),
    "justify_or_argue": ("justify", "argument", "argue", "defend a position", "make a case", "persuad"),
    "compare": ("compare", "contrast"),
    "evaluate": ("evaluat", "assess", "advantages and disadvantages"),
    "summarize": ("summaris", "summariz", "main points from"),
    "synthesize": ("synthesi", "integrate information", "collate information"),
    "speculate_or_hypothesize": ("speculat", "hypothesi", "likelihood", "predict", "possibilit"),
    "advise_or_recommend": ("advis", "recommend", "suggest a course", "make suggestions"),
    "negotiate_or_resolve": ("negotiat", "compromise", "resolve", "reach agreement", "conflict"),
    "present_or_address_audience": ("presentation", "address an audience", "give a talk"),
    "report_or_review": ("write a report", "produce a report", "write a review", "review of"),
    "analyze_or_criticize": ("analys", "analyz", "critic", "critique"),
    "manage_discourse": ("structure a", "organise a", "organize a", "link contribution", "conclude"),
}


def _advanced(text: str) -> tuple[set[str], set[str]]:
    functions, rules = set(), set()
    for function, terms in ADVANCED_RULES.items():
        if any(term in text for term in terms):
            functions.add(function)
            rules.add(f"gse_text_{function}")
    return functions, rules


def _reception(text: str) -> tuple[set[str], set[str]]:
    if any(term in text for term in ("instructions", "directions", "commands")):
        return {"follow_instructions"}, {"gse_reception_instructions"}
    if any(term in text for term in ("infer", "deduce", "work out", "from context")):
        return {"infer_meaning"}, {"gse_reception_inference"}
    if any(term in text for term in ("attitude", "intention", "implied", "implication", "irony", "sarcasm", "tone")):
        return {"interpret_attitude_or_implication"}, {"gse_reception_implication"}
    locating = ("identify", "find", "extract", "recognise", "recognize", "pick out", "locate", "specific information")
    if any(term in text for term in locating):
        return {"locate_information"}, {"gse_reception_locate"}
    return {"comprehend_information"}, {"gse_reception_default"}


def _productive_basics(skill: str, text: str) -> tuple[set[str], set[str]]:
    functions, rules = _advanced(text)
    simple_rules = {
        "introduce": ("introduc",), "socialize": ("greet", "thank", "apologi", "congratulat", "sympathy"),
        "express_preference": ("preference", "likes and dislikes", "prefer"),
        "express_feeling": ("feeling", "emotion"), "express_ability": ("ability", "can or can"),
        "request": ("ask for", "request "), "transact": ("buy ", "check into", "transaction"),
        "ask_for_information": ("request information", "ask a question", "ask basic question", "ask simple question", "seek confirmation"),
        "exchange_information": ("ask and answer", "exchange information", "interview", "discuss"),
        "respond_to_request_or_offer": ("accept offer", "accept an offer", "decline offer", "decline an offer", "respond to an offer", "agree to simple request"),
        "offer_or_invite": ("make an offer", "make offer", "invitation", "invite "),
        "complete_form": ("complete a form", "complete simple form", "complete a simple form", "complete a detailed form", "complete forms", "fill in"),
        "correspond": ("email", "message", "letter", "post online", "posting"),
        "reproduce_language": ("copy", "spell", "repeat", "read aloud"),
        "describe": ("describ",),
        "clarify_or_repair": ("clarify", "reformulat", "repair communication", "check that"),
        "mediate_information": ("pass on", "relay ", "for somebody else", "for someone else"),
        "translate": ("translat",),
        "facilitate_interaction": ("invite others to contribute", "facilitat", "encourage discussion"),
    }
    for function, terms in simple_rules.items():
        if any(term in text for term in terms):
            functions.add(function)
            rules.add(f"gse_text_{function}")
    if not functions:
        functions.add("give_information")
        rules.add(f"gse_{skill}_default")
    return functions, rules


def _interaction_mode(functions: set[str], text: str) -> bool:
    interactive = {
        "ask_for_information", "exchange_information", "socialize", "request",
        "respond_to_request_or_offer", "transact", "negotiate_or_resolve", "correspond",
    }
    terms = ("respond to", "reply", "conversation", "discussion", "interact", "interview")
    return bool(functions & interactive) or any(term in text for term in terms)


def tag_gse_progression(record: dict) -> ProgressionTagDecision:
    skill_text = record["source_facts"]["skill_text"]
    text = record["source"]["source_text"].casefold()
    skill = SKILLS.get(skill_text)
    if not skill:
        raise ValueError(f"unsupported GSE skill: {skill_text!r}")
    if skill_text in {"Reading", "Listening"}:
        functions, rules = _reception(text)
        modes = {"reception"}
    else:
        functions, rules = _productive_basics(skill, text)
        if functions & {"mediate_information", "translate", "facilitate_interaction"}:
            modes = {"mediation"}
        else:
            modes = {"interaction" if _interaction_mode(functions, text) else "production"}
    return decision({skill}, modes, functions, rules)
