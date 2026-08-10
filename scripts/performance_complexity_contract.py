"""Mappings from reviewed exit claims to CEFR performance strands."""

from scripts.level_exit_profile_contract import OUTPUT as PROFILES
from scripts.source_disposition_contract import OUTPUT as DISPOSITIONS
from scripts.source_disposition_contract import ROOT


OUTPUT = ROOT / "data" / "reviewed" / "performance-complexity-strands-v1.json"
REPORT = ROOT / "docs" / "PERFORMANCE_COMPLEXITY_PROGRESSION_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "performance-complexity-strands.schema.json"
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
REVIEWED_AT = "2026-08-10T13:37:25+03:00"

STRANDS = {
    "listening_reception": ("Listening input complexity", "input", "reception.listening"),
    "reading_reception": ("Reading input complexity", "input", "reception.reading"),
    "speaking_production": ("Spoken output complexity", "output", "production.speaking"),
    "writing_production": ("Written output complexity", "output", "production.writing"),
    "oral_interaction": ("Oral interaction independence", "interaction", "interaction.oral"),
    "written_online_interaction": ("Written and online interaction", "interaction", "interaction.written_online"),
    "mediation": ("Mediation complexity", "interaction", "interaction.mediation"),
    "language_range": ("Language range", "language_control", "language_control.range"),
    "grammar": ("Grammatical control", "language_control", "language_control.grammar"),
    "vocabulary": ("Lexical range and control", "language_control", "language_control.vocabulary"),
    "pronunciation": ("Pronunciation and intelligibility", "language_control", "language_control.pronunciation"),
    "discourse": ("Discourse and cohesion", "language_control", "language_control.discourse"),
    "fluency": ("Fluency", "language_control", "language_control.fluency"),
    "communication_strategy": ("Communication strategy", "strategy", None),
    "sociolinguistic": ("Sociolinguistic appropriateness", "language_control", None),
}

STRATEGY_TEXT = {
    "a1": "Signal a basic problem and request simple repetition or clarification with support.",
    "a2": "Use simple clarification, repetition, gesture, and basic compensating phrases in routine situations.",
    "b1": "Keep going through circumlocution, checking, confirmation, and repair on familiar topics.",
    "b2": "Paraphrase, manage turns, and repair most breakdowns while sustaining an independent exchange.",
    "c1": "Reformulate flexibly, manage interaction, and resolve ambiguity with little disruption.",
    "c2": "Backtrack, restructure, and repair so smoothly that difficulty is unobtrusive.",
}

SOCIOLINGUISTIC_TEXT = {
    "a1": "Use basic greetings, leave-taking, thanks, and simple politeness formulas.",
    "a2": "Use common social conventions and routine polite language in predictable contexts.",
    "b1": "Use a wider neutral repertoire and common politeness conventions across familiar contexts.",
    "b2": "Select suitable formality and sustain social relationships without significant strain.",
    "c1": "Adapt register flexibly and interpret common idiomatic, cultural, and interpersonal signals.",
    "c2": "Handle register, connotation, humour, and sociocultural implications with precise sensitivity.",
}
