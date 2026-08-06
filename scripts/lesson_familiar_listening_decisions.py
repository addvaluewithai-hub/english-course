"""Reviewed target and error decisions for familiar-context listening reception."""

FAMILIAR_LISTENING_DECISIONS = {
    "lesson_candidate.understand_talk_about_people_and_family": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Basic person and family relationship words", "identify who is discussed and the required family facts", ["cefr.cv2020.p049.understanding_conversation_between_other_people.01"])],
            "phrases": [("Short expressions about a person and family", "attribute each explicit fact to the correct person", ["cefr.cv2020.p049.understanding_conversation_between_other_people.01"])],
            "pronunciation": [("Recognition of person and family expressions in slow clear conversation", "identify the required facts without a transcript", ["cefr.cv2020.p049.understanding_conversation_between_other_people.01"])],
        },
        "decision_note": "No separate grammar target is assigned because the descriptor supports slow clear expressions about people and family without naming a required construction.",
        "error": {
            "error": "The learner recognises a family expression but attributes it to the wrong person in the conversation.",
            "impact": "The resulting person or family facts are inaccurate.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the person-attribution demand; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.understand_talk_about_leisure_preferences_and_abilities": {
        "targets": {
            "grammar": [("Receptive contrast between can and can't", "distinguish an explicitly stated ability from inability", ["gse.adult.2022.p14.010", "gse.adult.2022.p15.018"])],
            "vocabulary": [("Familiar free-time activity words", "identify the leisure activity attached to each person", ["gse.adult.2022.p15.009", "gse.adult.2022.p15.010"])],
            "phrases": [("Basic questions and statements about likes, dislikes, free time, and ability", "separate each stated preference or ability and its owner", ["gse.adult.2022.p14.009", "gse.adult.2022.p14.014", "gse.adult.2022.p15.010", "gse.adult.2022.p15.018"])],
            "pronunciation": [("Recognition of can versus can't in slow clear sentences", "avoid reversing an ability judgment", ["gse.adult.2022.p14.010", "gse.adult.2022.p15.018"])],
        },
        "decision_note": "Targets stay receptive: the sources support understanding preferences, activities, and the can/can't contrast, not independent spoken production.",
        "error": {
            "error": "The learner hears the activity correctly but reverses a like/dislike or can/can't contrast.",
            "impact": "A person's explicit preference or ability is reported as its opposite.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the positive-versus-negative listening contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.understand_where_things_or_people_are": {
        "targets": {
            "grammar": [("Basic receptive location statements", "connect a named thing or person to the stated position", ["gse.adult.2022.p14.011", "cefr.cv2020.p051.understanding_announcements_and_instructions.02"])],
            "vocabulary": [("Familiar immediate-environment referents and position words", "locate the required thing or person in a pictured scene", ["gse.adult.2022.p14.011", "cefr.cv2020.p051.understanding_announcements_and_instructions.02"])],
            "phrases": [("Slow clear statements about where something or someone is", "use the complete location statement rather than the picture alone", ["gse.adult.2022.p14.011", "cefr.cv2020.p051.understanding_announcements_and_instructions.02"])],
            "pronunciation": [("Recognition of the referent and position in slow clear speech", "distinguish the intended location without written labels", ["gse.adult.2022.p14.011", "cefr.cv2020.p051.understanding_announcements_and_instructions.02"])],
        },
        "decision_note": "The people-and-surroundings CEFR clause remains supporting context; targets rely on the candidate's explicit immediate-location evidence and stay receptive.",
        "error": {
            "error": "The learner selects the named thing or person but ignores the spoken position contrast.",
            "impact": "The referent is placed in the wrong location in the pictured scene.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the referent-versus-position contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
}
