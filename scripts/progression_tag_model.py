"""All-level communicative tag contract used by the vertical spine."""

from __future__ import annotations

from dataclasses import dataclass


TAXONOMY_VERSION = "2.0.0"

SKILL_CODES = {
    "listening", "reading", "speaking", "writing", "viewing", "non_verbal",
    "language_system",
}

MODE_CODES = {
    "reception", "production", "interaction", "online_interaction", "mediation",
    "communicative_competence", "plurilingual_pluricultural",
}

FUNCTION_CODES = {
    "comprehend_information", "follow_instructions", "locate_information",
    "interpret_attitude_or_implication", "describe", "narrate", "give_information",
    "ask_for_information", "exchange_information", "introduce", "socialize",
    "express_preference", "express_feeling", "express_ability", "express_opinion",
    "request", "respond_to_request_or_offer", "offer_or_invite", "transact", "correspond", "complete_form",
    "clarify_or_repair", "infer_meaning", "explain", "justify_or_argue",
    "compare", "evaluate", "summarize", "synthesize", "speculate_or_hypothesize",
    "advise_or_recommend", "negotiate_or_resolve", "present_or_address_audience",
    "report_or_review", "analyze_or_criticize", "mediate_information", "translate",
    "facilitate_interaction", "reproduce_language", "control_language_form",
    "manage_discourse",
}


@dataclass(frozen=True)
class ProgressionTagDecision:
    skills: tuple[str, ...]
    modes: tuple[str, ...]
    functions: tuple[str, ...]
    rule_ids: tuple[str, ...]

    def validate(self) -> None:
        groups = (
            ("skill", self.skills, SKILL_CODES),
            ("mode", self.modes, MODE_CODES),
            ("function", self.functions, FUNCTION_CODES),
        )
        for label, values, allowed in groups:
            if not values:
                raise ValueError(f"no {label} tags")
            unknown = set(values) - allowed
            if unknown:
                raise ValueError(f"unknown {label} tags: {sorted(unknown)}")
            if len(values) != len(set(values)):
                raise ValueError(f"duplicate {label} tags")
        if not self.rule_ids:
            raise ValueError("tag decision needs an auditable rule id")


def decision(
    skills: set[str], modes: set[str], functions: set[str], rules: set[str]
) -> ProgressionTagDecision:
    result = ProgressionTagDecision(
        tuple(sorted(skills)), tuple(sorted(modes)), tuple(sorted(functions)), tuple(sorted(rules))
    )
    result.validate()
    return result
