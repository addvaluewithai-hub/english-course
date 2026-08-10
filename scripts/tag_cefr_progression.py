"""Deterministic all-level communicative tags for CEFR descriptors."""

from __future__ import annotations

from scripts.progression_tag_model import ProgressionTagDecision, decision


MODE_MAP = {
    "Reception": "reception", "Production": "production", "Interaction": "interaction",
    "Online interaction": "online_interaction", "Mediation": "mediation",
    "Communicative language competences": "communicative_competence",
    "Plurilingual and pluricultural competence": "plurilingual_pluricultural",
}


def _skills(mode: str, skill: str, scale: str) -> set[str]:
    direct = {
        "Oral comprehension": {"listening"}, "Audio-visual comprehension": {"listening", "viewing"},
        "Reading comprehension": {"reading"}, "Reception strategies": {"listening", "reading", "viewing"},
        "Oral production": {"speaking"}, "Written production": {"writing"},
        "Production strategies": {"speaking", "non_verbal"},
        "Oral interaction": {"listening", "speaking"}, "Written interaction": {"reading", "writing"},
        "Online interaction": {"reading", "writing"}, "Interaction strategies": {"listening", "speaking"},
        "Linguistic competence": {"language_system"}, "Sociolinguistic competence": {"language_system"},
        "Pragmatic competence": {"language_system"},
        "Plurilingual competence": {"listening", "reading", "speaking", "writing"},
        "Pluricultural competence": {"listening", "reading", "speaking", "non_verbal"},
    }
    if skill in direct:
        return direct[skill]
    if mode == "Mediation":
        if "in writing" in scale:
            return {"reading", "writing"}
        if "in speech" in scale:
            return {"listening", "reading", "speaking"}
        return {"listening", "reading", "speaking", "non_verbal"}
    raise ValueError(f"unsupported CEFR skill hierarchy: {mode!r} / {skill!r}")


def _reception(scale: str, text: str) -> tuple[set[str], str]:
    if "instructions" in scale.casefold() or "directions" in text:
        return {"follow_instructions"}, "cefr_scale_instructions"
    if "orientation" in scale.casefold() or any(term in text for term in ("find ", "locate", "pick out")):
        return {"locate_information"}, "cefr_scale_locate"
    if "inferring" in scale.casefold() or any(term in text for term in ("infer", "deduce", "from context")):
        return {"infer_meaning"}, "cefr_scale_inference"
    if any(term in text for term in ("implicit", "attitude", "irony", "sarcasm", "register shift", "undercurrent")):
        return {"interpret_attitude_or_implication"}, "cefr_text_implication"
    return {"comprehend_information"}, "cefr_reception_default"


def _advanced(text: str) -> tuple[set[str], set[str]]:
    rules = {
        "narrate": ("narrative", "recount", "story"), "explain": ("explain", "clarif"),
        "express_opinion": ("opinion", "viewpoint", "point of view"),
        "justify_or_argue": ("argument", "justify", "case in a debate", "support a position"),
        "compare": ("compare", "contrast"),
        "evaluate": ("evaluat", "advantages", "disadvantages"),
        "summarize": ("summaris", "summariz"),
        "synthesize": ("synthesi", "integrat"),
        "speculate_or_hypothesize": ("speculat", "hypothesi", "probability"),
        "advise_or_recommend": ("advice", "recommend", "suggestion"),
        "negotiate_or_resolve": ("negotiat", "compromise", "resolve", "disagreement"),
        "present_or_address_audience": ("audience", "presentation"),
        "report_or_review": ("report", "review"), "analyze_or_criticize": ("analys", "critic"),
        "manage_discourse": ("cohesive", "organisational pattern", "structure", "turntaking"),
    }
    functions, matched = set(), set()
    for function, terms in rules.items():
        if any(term in text for term in terms):
            functions.add(function)
            matched.add(f"cefr_text_{function}")
    return functions, matched


def _base(mode: str, scale: str, text: str) -> tuple[set[str], set[str]]:
    if mode == "reception":
        functions, rule = _reception(scale, text)
        return functions, {rule}
    if mode == "production":
        if scale == "Compensating":
            return {"clarify_or_repair"}, {"cefr_scale_compensating"}
        base = "describe" if "describ" in scale.casefold() or scale == "Creative writing" else "give_information"
        functions, rules = {base}, {f"cefr_production_{base}"}
    elif mode == "interaction":
        mapping = {
            "Asking for clarification": "clarify_or_repair", "Obtaining goods and services": "transact",
            "Correspondence": "correspond", "Notes, messages and forms": "correspond",
            "Information exchange": "exchange_information", "Interviewing and being interviewed": "exchange_information",
        }
        base = mapping.get(scale, "exchange_information")
        functions, rules = {base}, {f"cefr_interaction_{base}"}
    elif mode == "online_interaction":
        functions, rules = {"correspond"}, {"cefr_online_correspond"}
        if "transaction" in scale.casefold():
            functions.add("transact")
            rules.add("cefr_online_transact")
    elif mode == "mediation":
        if scale.startswith("Translating"):
            return {"translate"}, {"cefr_mediation_translate"}
        if any(scale.startswith(term) for term in ("Facilitating", "Collaborating", "Encouraging", "Managing")):
            return {"facilitate_interaction"}, {"cefr_mediation_facilitate"}
        functions, rules = {"mediate_information"}, {"cefr_mediation_information"}
    elif mode == "communicative_competence":
        return {"control_language_form"}, {"cefr_competence_control"}
    else:
        if "comprehension" in scale.casefold():
            return {"comprehend_information"}, {"cefr_plurilingual_comprehension"}
        return {"facilitate_interaction", "mediate_information"}, {"cefr_plurilingual_repertoire"}
    advanced, advanced_rules = _advanced(text)
    return functions | advanced, rules | advanced_rules


def tag_cefr_progression(record: dict) -> ProgressionTagDecision:
    facts = record["source_facts"]
    source_mode, source_skill, scale = facts["mode_text"], facts["skill_text"], facts["scale_text"]
    mode = MODE_MAP.get(source_mode)
    if not mode:
        raise ValueError(f"unsupported CEFR mode: {source_mode!r}")
    text = record["source"]["source_text"].casefold()
    functions, rules = _base(mode, scale, text)
    skills = _skills(source_mode, source_skill, scale)
    if any(term in text for term in ("non-verbal", "gesture", "body language")):
        skills.add("non_verbal")
        rules.add("cefr_explicit_non_verbal")
    return decision(skills, {mode}, functions, rules)
