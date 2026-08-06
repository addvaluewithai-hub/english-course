"""Reviewed target and error decisions for foundational social contact."""

FOUNDATION_SOCIAL_DECISIONS = {
    "lesson_candidate.use_basic_everyday_polite_forms": {
        "targets": {
            "grammar": [],
            "vocabulary": [],
            "phrases": [("Please, thank you, and sorry as basic fixed polite forms", "match each form to request-softening, thanks, or apology", ["cefr.cv2020.p137.sociolinguistic_appropriateness.01"])],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar, vocabulary, or pronunciation target is assigned because the source supports a channel-neutral fixed-form repertoire distinguished by social purpose.",
        "error": {
            "error": "The learner uses a familiar polite form for the wrong purpose, such as thanks where an apology is needed.",
            "impact": "The turn no longer communicates the intended request-softening, thanks, or apology.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the three-way purpose contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.open_and_close_a_basic_social_exchange": {
        "targets": {
            "grammar": [("Short wellbeing question-and-answer frames", "ask how the other person is and understand the answer", ["gse.adult.2022.p22.013", "cefr.cv2020.p074.conversation.04"])],
            "vocabulary": [("Basic wellbeing and familiar-news words", "choose a reaction that fits the other person's news", ["gse.adult.2022.p22.013", "cefr.cv2020.p074.conversation.04"])],
            "phrases": [("Basic greeting, reaction, and leave-taking expressions", "complete the four social moves in their fitting places", ["gse.adult.2022.p23.012", "cefr.cv2020.p074.conversation.03", "cefr.cv2020.p137.sociolinguistic_appropriateness.01"])],
            "pronunciation": [("Intelligible delivery of short fixed social expressions", "keep each spoken move recognisable in the exchange", ["gse.adult.2022.p22.013", "gse.adult.2022.p23.012"])],
        },
        "decision_note": "All four target families are assigned only to the greeting, wellbeing, reaction, and farewell moves named by the candidate evidence.",
        "error": {
            "error": "The learner gives a positive reaction to negative news, or a negative reaction to positive news.",
            "impact": "The response contradicts the news and the short social exchange does not function appropriately.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the changed-news contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.respond_politely_to_an_introduction": {
        "targets": {
            "grammar": [],
            "vocabulary": [],
            "phrases": [("Basic fixed expressions acknowledging an introduction", "respond to the newly introduced person politely", ["gse.adult.2022.p24.003", "cefr.cv2020.p137.sociolinguistic_appropriateness.01"])],
            "pronunciation": [("Intelligible delivery of the short acknowledgement", "make the response recognisable to the introduced person", ["gse.adult.2022.p24.003"])],
        },
        "decision_note": "No separate grammar or vocabulary target is assigned because the sources specify a few basic fixed expressions rather than a productive pattern or lexical field.",
        "error": {
            "error": "The learner directs the acknowledgement to the introducer instead of the newly introduced person.",
            "impact": "The response does not clearly acknowledge the person who was introduced.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the addressee distinction in the task; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.introduce_another_person": {
        "targets": {
            "grammar": [("Simple third-person identity and job statements", "state whose name and job are being introduced", ["gse.adult.2022.p22.022", "gse.adult.2022.p23.005", "gse.adult.2022.p23.002"])],
            "vocabulary": [("Familiar common job names", "give the introduced person's source-supported role", ["gse.adult.2022.p22.022", "gse.adult.2022.p23.005"])],
            "phrases": [("A basic other-person introduction frame", "connect the correct name and familiar job in one introduction", ["gse.adult.2022.p22.022", "gse.adult.2022.p23.012", "cefr.cv2020.p074.conversation.03"])],
            "pronunciation": [("Intelligible delivery of the person's name and job", "let listeners identify both essential details", ["gse.adult.2022.p22.022", "gse.adult.2022.p23.005"])],
        },
        "decision_note": "Targets stay within the name, familiar-job, and introduction clauses explicitly cited by the candidate.",
        "error": {
            "error": "The learner uses a self-introduction frame or attaches the job to the wrong name.",
            "impact": "Listeners cannot reliably identify the introduced person and role.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the self-versus-other and name-versus-job contrasts; it is not a source fact and requires expert review and learner observation.",
        },
    },
}
