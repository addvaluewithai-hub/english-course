"""Controlled curriculum tags and one normalization decision."""

from __future__ import annotations

from dataclasses import dataclass


TAXONOMY_VERSION = "1.0.0"

SKILL_CODES = {
    "listening",
    "reading",
    "speaking",
    "writing",
    "viewing",
    "non_verbal",
    "language_system",
}

MODE_CODES = {
    "reception",
    "production",
    "interaction",
    "online_interaction",
    "mediation",
    "communicative_competence",
}

FUNCTION_CODES = {
    "comprehend_information",
    "follow_instructions",
    "locate_information",
    "describe",
    "give_information",
    "ask_for_information",
    "exchange_information",
    "introduce",
    "socialize",
    "express_preference",
    "express_feeling",
    "express_ability",
    "request",
    "respond_to_request_or_offer",
    "transact",
    "correspond",
    "complete_form",
    "clarify_or_repair",
    "infer_meaning",
    "mediate_information",
    "translate",
    "facilitate_interaction",
    "reproduce_language",
    "control_language_form",
}


@dataclass(frozen=True)
class TagDecision:
    """Interpretive tags kept separate from source facts."""

    skills: tuple[str, ...]
    modes: tuple[str, ...]
    functions: tuple[str, ...]
    ambiguities: tuple[str, ...] = ()

    def validate(self) -> None:
        groups = (
            ("skill", self.skills, SKILL_CODES),
            ("mode", self.modes, MODE_CODES),
            ("function", self.functions, FUNCTION_CODES),
        )
        for label, values, allowed in groups:
            if not values:
                raise ValueError(f"Normalization produced no {label} tags")
            unknown = set(values) - allowed
            if unknown:
                raise ValueError(f"Unknown {label} tags: {sorted(unknown)}")
            if len(values) != len(set(values)):
                raise ValueError(f"Duplicate {label} tags: {values}")
