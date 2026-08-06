"""Reviewed targets and error decisions for familiar-people spoken tasks."""

FAMILIAR_PEOPLE_OUTPUT_DECISIONS = {
    "lesson_candidate.describe_a_family_or_known_person": {
        "targets": {
            "grammar": [("Basic statements identifying people and relationships", "distinguish each person and the stated relationship", ["gse.adult.2022.p24.004", "cefr.cv2020.p062.overall_oral_production.01"])],
            "vocabulary": [("Basic family, relationship, and known-person words", "name the prompted people and one familiar fact about each", ["gse.adult.2022.p24.004", "cefr.cv2020.p062.overall_oral_production.01"])],
            "phrases": [("Simple phrases describing a family or known person", "give the required identities, relationships, and familiar facts", ["gse.adult.2022.p24.004", "cefr.cv2020.p062.overall_oral_production.01"])],
            "pronunciation": [("Intelligible delivery of person and relationship words", "keep the people and relationships distinguishable without a written model", ["gse.adult.2022.p24.004"])],
        },
        "decision_note": "Targets stay within the prompted family or known-person description; they do not impose a culturally fixed family structure.",
        "error": {
            "error": "The learner uses a plausible family word but assigns the relationship or familiar fact to the wrong person.",
            "impact": "The listener cannot distinguish the prompted people and relationships accurately.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the person-versus-relationship attribution demand; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.exchange_information_about_family_and_friends": {
        "targets": {
            "grammar": [("Basic factual questions with short relevant answers", "ask for and supply each required people fact", ["gse.adult.2022.p22.002", "gse.adult.2022.p23.013", "cefr.cv2020.p074.conversation.02", "cefr.cv2020.p079.information_exchange.03"])],
            "vocabulary": [("Family, known-person, relationship, role, and ownership words", "identify the person fact requested in each turn", ["gse.adult.2022.p22.002", "gse.adult.2022.p23.013", "gse.adult.2022.p24.007"])],
            "phrases": [("Short ask-and-answer turns about family, friends, and who has an item", "complete both sides of the bounded information exchange", ["gse.adult.2022.p22.002", "gse.adult.2022.p23.013", "gse.adult.2022.p24.007", "cefr.cv2020.p079.information_exchange.03"])],
            "pronunciation": [("Recognition and intelligible delivery of the requested people fact", "keep the question category and answer clear in slow direct turns", ["gse.adult.2022.p22.002", "cefr.cv2020.p074.conversation.02"])],
        },
        "decision_note": "Ownership stays one bounded factual turn; targets do not expand the exchange into a separate object lesson.",
        "error": {
            "error": "The learner answers about the right person but supplies a different fact category, such as relationship instead of ownership.",
            "impact": "The partner cannot obtain one of the required people facts despite receiving a plausible answer.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the question-category and person-attribution contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
}
