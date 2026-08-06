"""Reviewed targets and error decisions for familiar routine and time speech."""

FAMILIAR_ROUTINE_OUTPUT_DECISIONS = {
    "lesson_candidate.describe_a_simple_everyday_routine": {
        "targets": {
            "grammar": [("A prepared series of simple sentences about everyday life", "express three activities as one understandable routine", ["cefr.cv2020.p063.sustained_monologue_describing_experience.02"])],
            "vocabulary": [("Familiar everyday activity words", "name the three activities required by the changed prompt", ["cefr.cv2020.p063.sustained_monologue_describing_experience.02"])],
            "phrases": [("Basic phrases linking activities into a clear routine sequence", "make the main routine and order followable", ["cefr.cv2020.p063.sustained_monologue_describing_experience.02"])],
            "pronunciation": [("Intelligible delivery of the key activities and their order", "preserve the routine without sentences to copy", ["cefr.cv2020.p063.sustained_monologue_describing_experience.02"])],
        },
        "decision_note": "The source supports advance preparation and a series of simple sentences; planning cues must not become a script.",
        "error": {
            "error": "The learner names all three activities but leaves their intended order unclear or contradictory.",
            "impact": "The listener cannot follow the main routine as a sequence.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the activity-versus-sequence demand; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.give_a_simple_leisure_profile": {
        "targets": {
            "grammar": [("Can and can't for basic activity ability", "state the prompted ability or lack of ability without reversing it", ["gse.adult.2022.p23.006"])],
            "vocabulary": [("Familiar leisure activities and basic preference words", "identify the activity, preference, and ability on the changed profile", ["gse.adult.2022.p23.006", "gse.adult.2022.p23.015"])],
            "phrases": [("Simple statements of likes, dislikes, ability, and inability", "give both required facts about the person", ["gse.adult.2022.p23.006", "gse.adult.2022.p23.015"])],
            "pronunciation": [("Intelligible contrast between can and can't", "keep the positive or negative ability meaning clear", ["gse.adult.2022.p23.006"])],
        },
        "decision_note": "The target combines only one stated preference and one related ability from a safe fictional-person profile.",
        "error": {
            "error": "The learner names the activity correctly but reverses either the like/dislike or can/can't meaning.",
            "impact": "The listener receives the opposite preference or ability from the prompt.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the paired positive-versus-negative contrasts; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.exchange_routine_and_preference_information": {
        "targets": {
            "grammar": [("Simple routine and preference questions with short relevant answers", "ask for and supply each required fact in the exchange", ["gse.adult.2022.p23.016", "cefr.cv2020.p075.informal_discussion_with_friends.01", "gse.adult.2022.p24.006"])],
            "vocabulary": [("Familiar routine, sport, food, and leisure words", "identify the activity and preference category in each turn", ["gse.adult.2022.p23.016", "cefr.cv2020.p075.informal_discussion_with_friends.01", "gse.adult.2022.p24.006"])],
            "phrases": [("Short questions and answers about daily activities, habits, likes, and dislikes", "exchange every required fact through relevant turns", ["gse.adult.2022.p23.016", "cefr.cv2020.p075.informal_discussion_with_friends.01", "gse.adult.2022.p24.006"])],
            "pronunciation": [("Recognition and intelligible delivery of routine and preference contrasts", "keep the requested activity and positive or negative answer clear", ["cefr.cv2020.p075.informal_discussion_with_friends.01", "gse.adult.2022.p24.006"])],
        },
        "decision_note": "A model may support question form, as one GSE objective permits, but cannot supply the learner's answers.",
        "error": {
            "error": "The learner gives a plausible activity answer but misses whether the partner asked about a routine or a preference.",
            "impact": "One required fact is not exchanged, or a like/dislike meaning becomes inaccurate.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the routine-versus-preference question contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.give_an_event_date_and_time": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Days, months, clock times, and familiar time expressions", "supply the date and time fields required by the event prompt", ["gse.adult.2022.p22.003", "gse.adult.2022.p22.014", "gse.adult.2022.p22.016", "gse.adult.2022.p22.019"])],
            "phrases": [("Standard day-and-month dates, five-minute or quarter-hour times, and lexicalised time phrases", "make the intended event date and time recordable", ["gse.adult.2022.p22.003", "gse.adult.2022.p22.014", "gse.adult.2022.p22.016", "gse.adult.2022.p22.019", "cefr.cv2020.p079.information_exchange.04"])],
            "pronunciation": [("Intelligible contrasts among dates, clock times, and lexicalised time phrases", "prevent the listener from recording the wrong event detail", ["gse.adult.2022.p22.003", "gse.adult.2022.p22.014", "gse.adult.2022.p22.019"])],
        },
        "decision_note": "No separate grammar target is assigned because the sources specify date formats, clock times, and lexicalised phrases rather than a grammatical construction.",
        "error": {
            "error": "The learner gives the correct numbers but swaps the date, clock time, or relative-time field.",
            "impact": "The listener records an event at the wrong date or time.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the date-versus-time field contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
}
