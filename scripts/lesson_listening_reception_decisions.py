"""Reviewed target and error decisions for foundational listening reception."""

LISTENING_RECEPTION_DECISIONS = {
    "lesson_candidate.identify_familiar_referents_from_spoken_clues": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Common people, place, and object words plus distinguishing descriptors", "identify the intended familiar referent", ["gse.adult.2022.p14.008", "gse.adult.2022.p15.013", "gse.adult.2022.p15.017"])],
            "phrases": [("Basic object questions and short spoken descriptions", "combine the clue words before selecting a referent", ["gse.adult.2022.p14.008", "gse.adult.2022.p15.013", "gse.adult.2022.p15.017"])],
            "pronunciation": [("Recognition of key referent and descriptor words in slow clear speech", "distinguish the essential clue without written labels", ["gse.adult.2022.p15.013", "gse.adult.2022.p15.017"])],
        },
        "decision_note": "No separate grammar target is assigned because the cited evidence supports understanding bounded questions and descriptions without naming a required grammar feature.",
        "error": {
            "error": "The learner selects the first familiar pictured noun and ignores the spoken distinguishing clue.",
            "impact": "The chosen person, place, or object does not match the complete description.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the noun-versus-descriptor task contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.locate_names_places_and_times_in_slow_recordings": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Concrete names, place words, and clock-time expressions", "classify and record the requested everyday details", ["gse.adult.2022.p14.007", "cefr.cv2020.p048.overall_oral_comprehension.02", "cefr.cv2020.p052.understanding_audio_or_signed_media_and_recordings.01"])],
            "phrases": [],
            "pronunciation": [("Segmentation of names, places, and times in very slow clear delivery", "pick out concrete details without a transcript", ["gse.adult.2022.p14.007", "cefr.cv2020.p052.understanding_audio_or_signed_media_and_recordings.01"])],
        },
        "decision_note": "No separate grammar or phrases target is assigned because the source-supported task is detail extraction across short familiar recordings, not control of one construction.",
        "error": {
            "error": "The learner hears a concrete detail but records it in the wrong name, place, or time slot.",
            "impact": "The extracted information cannot be used accurately in the fresh task.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the three-way detail classification; it is not a source fact and requires expert and learner validation.",
        },
    },
    "lesson_candidate.identify_spoken_time_and_date_details": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Clock-time and calendar-date language, including quarter-hour and five-minute detail", "identify the exact time or date in a familiar context", ["gse.adult.2022.p14.003", "gse.adult.2022.p14.004", "gse.adult.2022.p14.015", "gse.adult.2022.p15.005", "gse.adult.2022.p15.008"])],
            "phrases": [("Short spoken time and date expressions", "distinguish the requested factual detail from surrounding event information", ["gse.adult.2022.p14.003", "gse.adult.2022.p14.004", "gse.adult.2022.p14.015"])],
            "pronunciation": [("Recognition of exact time and date values in slow clear speech", "avoid reducing an exact detail to an approximate one", ["gse.adult.2022.p15.005", "gse.adult.2022.p15.008", "cefr.cv2020.p048.overall_oral_comprehension.02"])],
        },
        "decision_note": "No separate grammar target is assigned because the cited objectives specify factual time/date recognition, not production of a grammatical construction.",
        "error": {
            "error": "The learner records an approximate hour or day while missing the stated quarter-hour, five-minute, or date detail.",
            "impact": "The selected event detail is not accurate enough for the source-supported task.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the exact-versus-approximate contrast in the cited objectives; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.understand_spoken_personal_introductions": {
        "targets": {
            "grammar": [("Simple first- and third-person identity statements", "separate information about the speaker from information about another person", ["gse.adult.2022.p14.001", "gse.adult.2022.p15.014"])],
            "vocabulary": [("Name, age, origin, residence, and basic role language", "identify the main personal information in a short introduction", ["gse.adult.2022.p14.001", "gse.adult.2022.p15.014"])],
            "phrases": [("Simple self-introduction and other-person introduction statements", "connect each personal detail to the correct person", ["gse.adult.2022.p14.001", "gse.adult.2022.p15.014"])],
            "pronunciation": [("Recognition of key personal details in short clear introductions", "identify essential information without a transcript", ["gse.adult.2022.p14.001", "gse.adult.2022.p15.014"])],
        },
        "decision_note": "Targets are limited to receptive distinctions directly needed by the cited introduction tasks; productive accuracy is not mastery evidence here.",
        "error": {
            "error": "The learner attaches a third-person detail to the speaker, or a speaker detail to the person being introduced.",
            "impact": "The essential personal information is matched to the wrong person.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the self-versus-other introduction contrast; it is not a source fact and needs expert and learner validation.",
        },
    },
    "lesson_candidate.understand_spoken_contact_details": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Personal names and spoken phone-number digits", "record the contact details needed to return or log a call", ["gse.adult.2022.p14.005", "gse.adult.2022.p15.011"])],
            "phrases": [("Short telephone and recorded-message contact-detail frames", "locate the caller name and phone number in context", ["gse.adult.2022.p14.005", "gse.adult.2022.p15.011"])],
            "pronunciation": [("Discrimination and grouping of spoken name and phone-number detail", "produce a usable written record without seeing the number", ["gse.adult.2022.p14.005", "gse.adult.2022.p15.011"])],
        },
        "decision_note": "No separate grammar target is assigned because the cited performance depends on accurate contact-detail recognition, not control of a clause pattern.",
        "error": {
            "error": "The learner omits, substitutes, or groups a spoken phone-number digit incorrectly.",
            "impact": "The recorded contact detail is not accurate enough to use.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the exact digit-recording demand; it is not a source fact and requires expert and learner validation.",
        },
    },
}
