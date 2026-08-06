"""Reviewed target and error decision for postcard reception."""

POSTCARD_RECEPTION_DECISION = {
    "lesson_candidate.understand_a_short_simple_postcard_message": {
        "targets": {
            "grammar": [],
            "vocabulary": [],
            "phrases": [
                (
                    "Short simple postcard messages carrying one main everyday point and an explicit detail",
                    "identify the whole message rather than an isolated familiar word",
                    ["cefr.cv2020.p055.reading_correspondence.01"],
                )
            ],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar, vocabulary, or pronunciation target is assigned because the descriptor fixes the short postcard genre and comprehension demand but not a topic, named form, or spoken channel.",
        "error": {
            "error": "The learner selects a familiar postcard word as the main message even though another explicit detail changes the overall meaning.",
            "impact": "The stated main message and supporting detail do not form an accurate reading of the postcard.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the whole-message-versus-isolated-word contrast; it is not a source fact and requires expert review and learner observation.",
        },
    }
}
