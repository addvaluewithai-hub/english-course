"""Reviewed targets for the remaining travel-reception candidates."""


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


TRAVEL_RECEPTION_DECISIONS = {
    "lesson_candidate.understand_simple_place_and_hotel_information": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar place, feature, facility, and service-time words",
                "identify two explicit facts in the changed place or hotel text",
                [
                    "gse.adult.2022.p09.006",
                    "cefr.cv2020.p056.reading_for_orientation.03",
                    "cefr.cv2020.p057.reading_for_information_and_argument.02",
                ],
            )],
            "phrases": [(
                "Very simple place descriptions and basic hotel-information statements",
                "read each requested fact from the text rather than infer it from pictures",
                [
                    "gse.adult.2022.p09.006",
                    "cefr.cv2020.p056.reading_for_orientation.03",
                ],
            )],
            "pronunciation": [],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence supports "
            "understanding place descriptions and hotel facts without naming a "
            "construction; no pronunciation target is assigned because mastery is "
            "written reception."
        ),
        "error": _error(
            "The learner uses the illustration to guess the place but misses or changes one explicit facility, feature, or service-time fact.",
            "One of the two required facts is inaccurate.",
            "the text-versus-picture evidence demand in the fresh reading task",
        ),
    },
    "lesson_candidate.understand_outline_of_a_simple_guided_tour": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar words naming the place, feature, and one main fact",
                "identify what the very slow guided explanation is mainly about",
                ["cefr.cv2020.p051.understanding_as_a_member_of_a_live.01"],
            )],
            "phrases": [(
                "Very simple explanatory language in a predictable guided setting",
                "connect the tour topic with one explicit main fact",
                ["cefr.cv2020.p051.understanding_as_a_member_of_a_live.01"],
            )],
            "pronunciation": [(
                "Recognition of topic and main-fact words in very slow, clearly paused speech",
                "understand the outline without a transcript",
                ["cefr.cv2020.p051.understanding_as_a_member_of_a_live.01"],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the single descriptor "
            "specifies outline comprehension and delivery conditions without naming a "
            "construction; pronunciation remains receptive recognition only."
        ),
        "error": _error(
            "The learner identifies the visible tour location but attaches the wrong spoken main fact to it.",
            "The selected outline does not match the explanation.",
            "the topic-plus-main-fact demand in the predictable guided setting",
        ),
    },
    "lesson_candidate.identify_key_details_in_a_slow_station_announcement": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Spoken time and number expressions in a station announcement",
                "identify the requested time and one other clearly stated figure",
                ["cefr.cv2020.p051.understanding_announcements_and_instructions.03"],
            )],
            "phrases": [(
                "Slow clear loudspeaker announcement frames containing figures and times",
                "assign each heard numerical detail to the requested role",
                ["cefr.cv2020.p051.understanding_announcements_and_instructions.03"],
            )],
            "pronunciation": [(
                "Recognition of contrasting spoken times and figures in slow clear delivery",
                "record both numerical details accurately without a transcript",
                ["cefr.cv2020.p051.understanding_announcements_and_instructions.03"],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the descriptor specifies "
            "reception of figures and times rather than a construction; targets stay "
            "within numerical details and do not invent platform recognition."
        ),
        "error": _error(
            "The learner hears both numerical values but assigns the time and the other figure to the wrong roles.",
            "The requested station details are recorded inaccurately.",
            "the value-to-role matching demand in the slow announcement",
        ),
    },
}
