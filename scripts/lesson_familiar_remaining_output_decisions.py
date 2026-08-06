"""Reviewed targets for the remaining familiar output and mediation tasks."""


def _error(error: str, impact: str, demand: str) -> dict[str, str]:
    return {
        "error": error,
        "impact": impact,
        "basis": (
            "Candidate-specific hypothesis for Arabic-speaking A1 adults based on "
            f"{demand}; it is not a source fact and requires expert review and "
            "learner observation."
        ),
    }


FAMILIAR_REMAINING_OUTPUT_DECISIONS = {
    "lesson_candidate.describe_common_weather": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Basic words for common weather conditions",
                "name the one or two conditions shown in the changed situation",
                ["gse.adult.2022.p23.018"],
            )],
            "phrases": [(
                "A brief current-weather description using the required condition words",
                "turn the lexical evidence into one understandable spoken description",
                ["gse.adult.2022.p23.018"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the contrasting weather-condition words",
                "prevent the listener from identifying a different condition",
                ["gse.adult.2022.p23.018"],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the source specifies basic "
            "weather words, not a grammatical construction; the range stays at one or "
            "two common conditions."
        ),
        "error": _error(
            "The learner uses a familiar weather word that contradicts the pictured condition.",
            "The listener identifies a different current condition from the prompt.",
            "the condition-word versus visible-weather mapping in the fresh description",
        ),
    },
    "lesson_candidate.deliver_a_rehearsed_formal_introduction": {
        "targets": {
            "grammar": [],
            "vocabulary": [],
            "phrases": [(
                "One very short prepared statement formally introducing another person",
                "make the person and purpose of the audience statement clear",
                ["cefr.cv2020.p066.addressing_audiences.01"],
            )],
            "pronunciation": [(
                "Intelligible rehearsed delivery of the very short identifying statement",
                "preserve whom the learner is introducing while using the permitted text",
                ["cefr.cv2020.p066.addressing_audiences.01"],
            )],
        },
        "decision_note": (
            "No separate grammar or vocabulary target is assigned because the descriptor "
            "defines a prepared statement and delivery condition, not a grammatical or "
            "lexical set; the learner-prepared text remains permitted."
        ),
        "error": _error(
            "The learner delivers a fluent prepared line but assigns the name or role to the wrong person.",
            "The audience identifies the introduced person or their role incorrectly.",
            "the person-to-role attribution required by the formal audience statement",
        ),
    },
    "lesson_candidate.state_how_a_simple_work_made_them_feel": {
        "targets": {
            "grammar": [(
                "A basic personal feeling statement linked to the work",
                "make the response a reaction to the changed work rather than an unrelated feeling",
                [
                    "gse.adult.2022.p23.010",
                    "cefr.cv2020.p107.expressing_a_personal_response_to_creative_texts.01",
                ],
            )],
            "vocabulary": [(
                "Basic feeling words suitable for a simple personal response",
                "name one intelligible reaction to the work",
                [
                    "gse.adult.2022.p23.010",
                    "cefr.cv2020.p107.expressing_a_personal_response_to_creative_texts.01",
                ],
            )],
            "phrases": [(
                "A brief expression stating how the work made the learner feel",
                "complete the personal-response function in the configured channel",
                ["cefr.cv2020.p107.expressing_a_personal_response_to_creative_texts.01"],
            )],
            "pronunciation": [],
        },
        "decision_note": (
            "No required pronunciation target is assigned because the source preserves "
            "spoken-or-written channel ambiguity; each fresh task declares one channel."
        ),
        "error": _error(
            "The learner names a feeling but does not connect it to the work, or describes the work without a personal reaction.",
            "The response does not demonstrate how the work made the learner feel.",
            "the work-description versus personal-feeling distinction in the mediation task",
        ),
    },
}
