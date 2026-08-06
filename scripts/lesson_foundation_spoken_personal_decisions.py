"""Reviewed targets and error decisions for foundational spoken personal tasks."""

FOUNDATION_SPOKEN_PERSONAL_DECISIONS = {
    "lesson_candidate.give_short_self_introduction": {
        "targets": {
            "grammar": [("Simple first-person statements for identity, residence, role, and one personal detail", "connect the required details in a short self-introduction", ["gse.adult.2022.p22.009", "gse.adult.2022.p22.006", "gse.adult.2022.p22.023", "gse.adult.2022.p22.027", "cefr.cv2020.p063.sustained_monologue_describing_experience.01"])],
            "vocabulary": [("Name, origin, residence, role, family, and interest language", "supply the changed personal-detail categories required by the prompt", ["gse.adult.2022.p22.009", "gse.adult.2022.p22.006", "gse.adult.2022.p22.023", "gse.adult.2022.p22.027", "cefr.cv2020.p142.propositional_precision.01"])],
            "phrases": [("A short self-introduction opening and connected personal-detail statements", "make the speaker and each essential detail identifiable", ["gse.adult.2022.p22.009", "cefr.cv2020.p063.sustained_monologue_describing_experience.01"])],
            "pronunciation": [("Intelligible delivery of names, places, roles, and the selected personal detail", "preserve the essential identifying information without a written model", ["gse.adult.2022.p22.009", "cefr.cv2020.p142.propositional_precision.01"])],
        },
        "decision_note": "Targets retain the source examples as bounded personal-detail categories, not a fixed quota or script.",
        "error": {
            "error": "The learner swaps origin and residence or omits the field distinction when both are requested.",
            "impact": "The listener receives inaccurate or incomplete identifying information.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the origin-versus-residence task contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.exchange_personal_details_orally": {
        "targets": {
            "grammar": [("Direct personal-detail questions with short relevant answers", "ask for and supply each changed detail in the exchange", ["gse.adult.2022.p23.004", "gse.adult.2022.p23.008", "cefr.cv2020.p079.information_exchange.03", "cefr.cv2020.p080.interviewing_and_being_interviewed.01"])],
            "vocabulary": [("Name, age, origin, residence, role, people-known, and possession language", "understand and answer the selected personal-detail questions", ["gse.adult.2022.p23.004", "gse.adult.2022.p23.008", "cefr.cv2020.p079.information_exchange.03"])],
            "phrases": [("Short ask-and-answer personal-information turns", "complete both sides of the bounded information exchange", ["gse.adult.2022.p23.008", "cefr.cv2020.p079.information_exchange.03", "cefr.cv2020.p080.interviewing_and_being_interviewed.01"])],
            "pronunciation": [("Recognition and intelligible delivery of question words and personal-detail values", "keep the requested category and answer clear in slow direct turns", ["gse.adult.2022.p23.004", "cefr.cv2020.p080.interviewing_and_being_interviewed.01"])],
        },
        "decision_note": "Targets cover only the two or three personal-detail categories selected for a fresh bounded exchange.",
        "error": {
            "error": "The learner answers a different personal-detail category from the one asked, such as giving residence for an origin question.",
            "impact": "The partner cannot obtain the required information despite receiving a plausible personal detail.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the question-category contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
}
