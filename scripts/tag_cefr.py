"""Deterministic normalized tags for CEFR Companion Volume A1 descriptors."""

from __future__ import annotations

try:
    from scripts.tag_model import TagDecision
except ModuleNotFoundError:
    from tag_model import TagDecision


MODE_MAP = {
    "Reception": "reception",
    "Production": "production",
    "Interaction": "interaction",
    "Online interaction": "online_interaction",
    "Mediation": "mediation",
    "Communicative language competences": "communicative_competence",
}

SKILL_MAP = {
    "Oral comprehension": ("listening",),
    "Audio-visual comprehension": ("listening", "viewing"),
    "Reading comprehension": ("reading",),
    "Reception strategies": ("listening", "reading", "viewing"),
    "Oral production": ("speaking",),
    "Written production": ("writing",),
    "Production strategies": ("speaking", "non_verbal"),
    "Oral interaction": ("listening", "speaking"),
    "Written interaction": ("reading", "writing"),
    "Online interaction": ("reading", "writing"),
    "Interaction strategies": ("listening", "speaking"),
    "Mediating concepts": ("listening", "speaking"),
    "Mediating communication": ("listening", "speaking"),
    "Linguistic competence": ("language_system",),
    "Sociolinguistic competence": ("language_system",),
    "Pragmatic competence": ("language_system",),
}


def _mediation_skills(scale: str) -> tuple[str, ...]:
    if scale.startswith("Translating a written text in speech"):
        return ("reading", "speaking")
    if scale == "Relaying specific information in speech or sign":
        return ("listening", "speaking")
    if scale == "Relaying specific information in writing":
        return ("listening", "writing")
    if scale == "Processing text in speech or sign":
        return ("reading", "speaking")
    if "in writing" in scale:
        return ("reading", "writing")
    if "personal response" in scale:
        return ("speaking", "writing")
    if "mediating a text" in scale.lower() or "processing text" in scale.lower():
        return ("reading", "speaking")
    return ("listening", "reading", "speaking", "non_verbal")


def _reception_function(scale: str, text: str) -> set[str]:
    if "instructions" in text or "directions" in text:
        return {"follow_instructions"}
    if "orientation" in scale:
        return {"locate_information"}
    if "cues and inferring" in scale:
        return {"infer_meaning"}
    locating = ("recognise", "pick out", "find", "where something is", "figures, prices and times")
    if any(term in text for term in locating):
        return {"locate_information"}
    return {"comprehend_information"}


def _production_function(scale: str) -> set[str]:
    if scale == "Compensating":
        return {"clarify_or_repair"}
    if "describing" in scale or scale == "Creative writing":
        return {"describe"}
    if scale == "Addressing audiences":
        return {"give_information", "introduce"}
    return {"give_information"}


def _interaction_function(scale: str, text: str) -> set[str]:
    if "instructions" in text and ("follow" in text or "act on" in text):
        return {"follow_instructions"}
    if scale == "Asking for clarification":
        return {"clarify_or_repair"}
    if scale == "Obtaining goods and services":
        return {"transact"}
    if scale == "Understanding an interlocutor":
        return {"comprehend_information"}
    if scale == "Goal-oriented co-operation":
        return {"follow_instructions"} if "instructions" in text else {"request"}
    if scale in {"Information exchange", "Interviewing and being interviewed"}:
        return {"exchange_information"}
    if scale == "Overall written interaction":
        return {"exchange_information"}
    if scale == "Correspondence":
        return {"correspond"}
    if scale == "Notes, messages and forms":
        return {"complete_form"} if "fill in" in text else {"correspond"}
    if scale == "Overall oral interaction":
        return {"exchange_information", "clarify_or_repair"}
    if scale == "Conversation":
        if text.startswith("can understand"):
            return {"comprehend_information"}
        if "introduction" in text:
            return {"introduce", "socialize"}
        if "how people are" in text:
            return {"socialize"}
        return {"exchange_information"}
    if scale == "Informal discussion (with friends)":
        return {"exchange_information", "express_preference"}
    return {"exchange_information"}


def _online_function(scale: str, text: str) -> set[str]:
    if scale == "Goal-oriented online transactions and collaboration":
        return {"transact", "complete_form"}
    tags = {"correspond"}
    if "reactions" in text:
        tags.add("socialize")
    return tags


def _mediation_function(scale: str, text: str) -> set[str]:
    if scale == "Overall mediation":
        return {"facilitate_interaction", "mediate_information"}
    if scale.startswith("Translating"):
        return {"translate"}
    if "copy out" in text:
        return {"reproduce_language"}
    if "personal response" in scale:
        return {"express_feeling"}
    facilitating = ("Facilitating", "Collaborating", "Encouraging")
    if scale.startswith(facilitating):
        return {"facilitate_interaction"}
    return {"mediate_information"}


def _competence_function(scale: str) -> set[str]:
    if scale == "Sociolinguistic appropriateness":
        return {"socialize"}
    if scale == "Propositional precision":
        return {"give_information"}
    if scale == "Fluency":
        return {"clarify_or_repair", "control_language_form"}
    return {"control_language_form"}


def tag_cefr(record: dict) -> TagDecision:
    facts = record["source_facts"]
    source_mode = facts["mode_text"]
    source_skill = facts["skill_text"]
    scale = facts["scale_text"]
    text = record["source"]["source_text"].lower()
    mode = MODE_MAP.get(source_mode)
    if not mode:
        raise ValueError(f"Unsupported CEFR source mode: {source_mode!r}")
    skills = SKILL_MAP.get(source_skill)
    if not skills and source_mode == "Mediation":
        skills = _mediation_skills(scale)
    if not skills:
        raise ValueError(f"Unsupported CEFR source skill: {source_skill!r}")
    if any(term in text for term in ("non-verbal", "gestures", "body language")):
        skills = tuple(sorted(set(skills) | {"non_verbal"}))

    function_resolvers = {
        "Reception": lambda: _reception_function(scale, text),
        "Production": lambda: _production_function(scale),
        "Interaction": lambda: _interaction_function(scale, text),
        "Online interaction": lambda: _online_function(scale, text),
        "Mediation": lambda: _mediation_function(scale, text),
        "Communicative language competences": lambda: _competence_function(scale),
    }
    ambiguities = ()
    if "personal response" in scale:
        ambiguities = (
            "The descriptor does not fix an oral or written realization; both productive channels are tagged.",
        )
    decision = TagDecision(
        tuple(sorted(skills)), (mode,), tuple(sorted(function_resolvers[source_mode]())), ambiguities
    )
    decision.validate()
    return decision
