"""Map source records to curriculum roles without assigning lesson ownership."""

from __future__ import annotations

from typing import Any


LISTENING_PREFIXES = ("Overall oral comprehension", "Understanding conversation", "Understanding as a member", "Understanding announcements", "Understanding audio", "Watching TV")
READING_PREFIXES = ("Overall reading", "Reading ", "Identifying cues")
SPEAKING_PREFIXES = ("Overall oral production", "Sustained monologue", "Public announcements", "Addressing audiences")
WRITING_PREFIXES = ("Overall written production", "Creative writing", "Reports and essays")
STRATEGY_SCALES = {"Planning", "Compensating", "Monitoring and repair", "Turntaking", "Co-operating", "Asking for clarification"}
ORAL_INTERACTION_SCALES = {
    "Overall oral interaction", "Understanding an interlocutor", "Conversation",
    "Informal discussion (with friends)", "Formal discussion (meetings)",
    "Goal-oriented co-operation (cooking together, discussing a document, organising an event, etc.)",
    "Obtaining goods and services", "Information exchange",
    "Interviewing and being interviewed", "Using telecommunications",
}
WRITTEN_INTERACTION_PREFIXES = ("Overall written interaction", "Correspondence", "Notes, messages", "Online conversation", "Goal-oriented online")
MEDIATION_PREFIXES = (
    "Overall mediation", "Relaying", "Explaining data", "Processing text", "Translating",
    "Note-taking", "Expressing a personal response", "Analysis and criticism",
    "Collaborating", "Facilitating", "Encouraging", "Managing interaction",
    "Acting as an intermediary", "Breaking down", "Adapting language", "Linking to",
    "Streamlining", "Amplifying", "Building on plur", "Plurilingual",
)
LANGUAGE_SCALES = {
    "General linguistic range": ("language_range", "productive"),
    "Vocabulary range": ("vocabulary", "productive"),
    "Grammatical accuracy": ("grammar", "productive"),
    "Vocabulary control": ("vocabulary", "productive"),
    "Prosodic features": ("pronunciation", "productive"),
    "Sound articulation": ("pronunciation", "productive"),
    "Overall phonological control": ("pronunciation", "productive"),
    "Orthographic control": ("writing_production", "productive"),
    "Sociolinguistic appropriateness": ("sociolinguistic", "both"),
    "Flexibility": ("discourse", "productive"),
    "Thematic development": ("discourse", "productive"),
    "Coherence and cohesion": ("discourse", "productive"),
    "Propositional precision": ("discourse", "productive"),
    "Fluency": ("fluency", "productive"),
}


def _cefr_classification(record: dict[str, Any]) -> tuple[str, str]:
    scale = record["source_facts"]["scale_text"]
    if scale.startswith(LISTENING_PREFIXES):
        return "listening_reception", "receptive"
    if scale.startswith(READING_PREFIXES):
        return "reading_reception", "receptive"
    if scale.startswith(SPEAKING_PREFIXES):
        return "speaking_production", "productive"
    if scale.startswith(WRITING_PREFIXES):
        return "writing_production", "productive"
    if scale in STRATEGY_SCALES:
        return "communication_strategy", "both"
    if scale in ORAL_INTERACTION_SCALES:
        return "oral_interaction", "both"
    if scale.startswith(WRITTEN_INTERACTION_PREFIXES):
        return "written_online_interaction", "both"
    if scale.startswith(MEDIATION_PREFIXES):
        return "mediation", "both"
    if scale in LANGUAGE_SCALES:
        return LANGUAGE_SCALES[scale]
    raise ValueError(f"unclassified CEFR scale: {scale}")


def classify(dataset_id: str, record: dict[str, Any]) -> tuple[list[str], str]:
    if dataset_id == "cefr_all_descriptors":
        strand, control = _cefr_classification(record)
        return [strand], control
    if dataset_id == "gse_all_objectives":
        skill = record["source_facts"]["skill_text"].lower()
        control = "receptive" if skill in {"listening", "reading"} else "productive"
        return [f"{skill}_{'reception' if control == 'receptive' else 'production'}"], control
    if dataset_id in {"egp_all_levels", "gse_grammar_all"}:
        return ["grammar"], "productive"
    if dataset_id in {"oxford_3000_all", "oxford_5000_all"}:
        return ["lexical_pool"], "not_applicable"
    raise ValueError(f"unknown source dataset: {dataset_id}")
