"""Reviewed target and error decisions for familiar-context reading reception."""

FAMILIAR_READING_DECISIONS = {
    "lesson_candidate.understand_a_short_everyday_activity_text": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Familiar everyday activity words", "identify the activities represented in a short text", ["gse.adult.2022.p09.012", "cefr.cv2020.p059.reading_as_a_leisure_activity.01"])],
            "phrases": [("Simple activity phrases and short illustrated narrative sentences", "connect each written activity to the basic event sequence", ["gse.adult.2022.p09.012", "cefr.cv2020.p059.reading_as_a_leisure_activity.01"])],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar or pronunciation target is assigned because the evidence names simple activity phrases and illustrated reading, not a required construction or spoken performance.",
        "error": {
            "error": "The learner identifies the pictured activities but reverses or invents their written sequence.",
            "impact": "The selected activity outline does not match the short text.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the image-versus-written-sequence contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.understand_a_simple_meeting_arrangement": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Familiar activity, time, and meeting-place words", "classify every required arrangement detail", ["gse.adult.2022.p09.010", "cefr.cv2020.p055.reading_correspondence.02"])],
            "phrases": [("Short simple meeting-proposal messages", "identify what to do plus when and where to meet", ["gse.adult.2022.p09.010", "cefr.cv2020.p055.reading_correspondence.02"])],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar or pronunciation target is assigned because the sources specify extracting a written arrangement, not control of one construction or speech.",
        "error": {
            "error": "The learner finds all three arrangement details but swaps the activity, time, or place into the wrong field.",
            "impact": "The learner cannot use the meeting proposal accurately.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the three-field arrangement contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.understand_outline_of_an_illustrated_short_story": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Familiar people, place, and action words in a short illustrated story", "identify the main situation across text and images", ["cefr.cv2020.p059.reading_as_a_leisure_activity.02"])],
            "phrases": [("Short image-supported story sentences", "recover the basic event outline without treating images as the complete answer", ["cefr.cv2020.p059.reading_as_a_leisure_activity.02"])],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar or pronunciation target is assigned because the descriptor supports outline reading with images but does not name a form or oral channel.",
        "error": {
            "error": "The learner chooses an outline from the pictures alone that conflicts with a simple sentence in the story.",
            "impact": "The main situation or event order is misread despite the intended image support.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the image-support-versus-text-relevance contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
}
