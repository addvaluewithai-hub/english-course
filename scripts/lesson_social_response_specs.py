"""Personal-response and sympathy candidates for social contact."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN
    from scripts.lesson_social_spec_helpers import evidence, social_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN
    from lesson_social_spec_helpers import evidence, social_spec


RESPONSE_SPECS = [
    social_spec(
        candidate_id="lesson_candidate.use_basic_everyday_polite_forms",
        situation="short everyday social turns requiring please, thank you, or sorry",
        action="choose and use the fitting basic polite form",
        content="one request-softening, thanks, and apology response across changed turns",
        success="each polite form matches the social purpose of its turn",
        statement="In fresh short everyday turns, the learner can use basic forms such as please, thank you, and sorry for the intended social purpose.",
        evidence_items=[evidence(
            "cefr.cv2020.p137.sociolinguistic_appropriateness.01", "anchor",
            "Covers the please, thank-you, and sorry clause; greetings, farewells, and introductions are assigned elsewhere.", "partial",
        )],
        skill_codes=["language_system"], mode_codes=["communicative_competence"],
        function_codes=["socialize"],
        rationale="The three fixed forms are a compact sociolinguistic set distinguished by one judgment: matching form to purpose.",
        fresh_task="Changed low-stakes turns that each require request-softening, thanks, or apology.",
        level_2={
            "comprehension": "Identifies the polite purpose required by each turn.",
            "outcome_performance": "Uses a fitting basic polite form for every purpose.",
            "interaction_or_transfer": "Matches the forms to changed turns rather than reciting a fixed order.",
            "control_or_repair": "Replaces one socially mismatched form after a neutral signal.",
        },
        critical_failure="A missing or mismatched form changes the intended polite purpose.",
        permitted_support=["A neutral label for the purpose, not the expression itself."],
        delayed_probe="Use different request, thanks, and apology turns after a delay.",
        scope_rationale="Three very short turns distinguished by social purpose.",
        risks=["Accept natural A1 variants and avoid culture-specific formality assumptions."],
        basic_support_ids=BASIC_SPOKEN, scope_band="standard",
    ),
    social_spec(
        candidate_id="lesson_candidate.state_how_a_simple_work_made_them_feel",
        situation="a brief response to a simple picture, story, song excerpt, or other safe creative work",
        action="state how the work made them feel in the configured spoken or written channel",
        content="one clear basic feeling linked to the work",
        success="the response names a feeling as a personal reaction to the work",
        statement="After a fresh simple creative work, the learner can state in a configured spoken or written response how it made them feel.",
        evidence_items=[
            evidence("gse.adult.2022.p23.010", "supporting", "The objective supports the spoken realization of a very basic feeling statement."),
            evidence("cefr.cv2020.p107.expressing_a_personal_response_to_creative_texts.01", "anchor", "The descriptor anchors stating how a work made the learner feel without fixing oral versus written realization."),
        ],
        skill_codes=["speaking", "writing"], mode_codes=["mediation"],
        function_codes=["express_feeling"],
        rationale="One configured response channel preserves the source ambiguity while keeping one feeling judgment.",
        fresh_task="A different simple safe work and a declared spoken or written response channel.",
        level_2={
            "comprehension": "Understands that a personal feeling about the work is requested.",
            "outcome_performance": "States one intelligible basic feeling as a reaction to the work.",
            "interaction_or_transfer": "Responds to a changed work rather than repeating the practice response.",
        },
        critical_failure="The response gives no feeling or is unrelated to the work.",
        permitted_support=["A non-answering reminder that the response must name a feeling."],
        delayed_probe="Use a different simple work and configured channel after a delay.",
        scope_rationale="One simple work and one brief feeling response in one channel.",
        risks=["Use safe, accessible works and accept differing personal reactions."],
        basic_support_ids=BASIC_SPOKEN,
    ),
    social_spec(
        candidate_id="lesson_candidate.show_basic_sympathy_during_a_problem_or_disagreement",
        situation="a short exchange where someone has a simple problem or two people disagree",
        action="recognise the difficulty and use a memorised expression of sympathy",
        content="the problem or disagreement cue and one fitting supportive expression",
        success="the response acknowledges the difficulty without taking over the situation",
        statement="In a fresh simple exchange, the learner can recognise a problem or disagreement and show basic sympathy with a memorised expression.",
        evidence_items=[evidence(
            "cefr.cv2020.p117.facilitating_communication_in_delicate_situations_and_disagreements.01", "anchor",
            "The descriptor directly anchors recognising a problem or disagreement and indicating sympathy.",
        )],
        skill_codes=["listening", "speaking"], mode_codes=["mediation"],
        function_codes=["facilitate_interaction"],
        rationale="Recognition and one sympathetic response are the two inseparable moves in the descriptor.",
        fresh_task="A different low-stakes fictional problem or disagreement and changed speaker.",
        level_2={
            "comprehension": "Recognises whether the exchange contains a problem or disagreement.",
            "outcome_performance": "Uses a simple memorised expression that indicates sympathy.",
            "interaction_or_transfer": "Selects a fitting response for the changed difficulty.",
            "control_or_repair": "Repairs a response that sounds dismissive after a neutral signal.",
        },
        critical_failure="The learner misses the difficulty or gives a dismissive or contradictory response.",
        permitted_support=["One replay of the short exchange."],
        delayed_probe="Use a different low-stakes problem or disagreement after a delay.",
        scope_rationale="One short difficulty cue and one memorised sympathetic response.",
        risks=["Keep scenarios low-stakes; safety or crisis content pauses the lesson and evaluation."],
        basic_support_ids=BASIC_SPOKEN,
        clusters=["social_contact_collaboration", "communication_strategies"],
    ),
]
