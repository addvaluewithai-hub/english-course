"""Reviewed targets for the next navigation and travel-action candidates."""


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


NAVIGATION_ACTION_DECISIONS = {
    "lesson_candidate.relay_predictable_person_time_or_place_details": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Predictable personal, role, time, and place detail words",
                "preserve two or three essential details in the English relay",
                [
                    "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01",
                    "cefr.cv2020.p095.relaying_specific_information_in_speech_or_sign.01",
                ],
            )],
            "phrases": [(
                "Very simple English relay frames with limited formulation help",
                "communicate the supplied details without receiving a complete rendering",
                [
                    "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01",
                    "cefr.cv2020.p095.relaying_specific_information_in_speech_or_sign.01",
                ],
            )],
            "pronunciation": [(
                "Intelligible delivery of contrasting names, roles, times, and places",
                "let the English listener record every relayed detail accurately",
                [
                    "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01",
                    "cefr.cv2020.p095.relaying_specific_information_in_speech_or_sign.01",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the mediation descriptors "
            "specify predictable information and formulation help without naming a construction."
        ),
        "error": _error(
            "The learner produces an intelligible English relay but changes which person, time, or place one detail belongs to.",
            "The listener records at least one essential detail inaccurately.",
            "the detail-preservation demand across the supported two-language relay",
        ),
    },
    "lesson_candidate.follow_simple_game_or_activity_instructions": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar spoken action, time, number, and order words",
                "distinguish every required action and condition in the changed activity",
                [
                    "gse.adult.2022.p15.003",
                    "cefr.cv2020.p077.goal_oriented_co_operation.02",
                    "gse.adult.2022.p14.006",
                ],
            )],
            "phrases": [(
                "Short simple command and instruction frames",
                "act on the complete two- or three-command sequence in order",
                ["gse.adult.2022.p15.003", "gse.adult.2022.p14.006"],
            )],
            "pronunciation": [(
                "Recognition of contrasting action, time, and number words in slow speech",
                "respond without a transcript or demonstration of every answer",
                ["cefr.cv2020.p077.goal_oriented_co_operation.02", "gse.adult.2022.p14.006"],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence supports acting "
            "on commands and instructions but does not name a construction."
        ),
        "error": _error(
            "The learner recognises the action word but misses its stated time, count, or place in the sequence.",
            "A required action is performed with the wrong condition or in the wrong order.",
            "the action-plus-condition demand in the fresh spoken instruction sequence",
        ),
    },
    "lesson_candidate.buy_a_basic_public_transport_ticket": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar destination and basic ticket-detail words",
                "specify the intended ticket clearly enough for it to be issued",
                ["gse.adult.2022.p22.011"],
            )],
            "phrases": [(
                "Basic fixed expressions for buying a public-transport ticket",
                "make the request and answer one changed clerk turn without a dialogue model",
                ["gse.adult.2022.p22.011"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the destination and contrasting ticket detail",
                "prevent the clerk from issuing a different ticket",
                ["gse.adult.2022.p22.011"],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the objective specifies basic "
            "fixed expressions rather than a grammatical construction."
        ),
        "error": _error(
            "The learner uses a suitable ticket-buying expression but omits or changes the destination or required ticket detail.",
            "The clerk would issue the wrong ticket or cannot complete the transaction.",
            "the two-essential-field demand in the fresh ticket transaction",
        ),
    },
    "lesson_candidate.check_in_at_a_hotel": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar booking-name and basic requested-detail words",
                "identify the fictional booking and supply the requested information",
                ["gse.adult.2022.p22.025"],
            )],
            "phrases": [(
                "A few basic fixed expressions for hotel check-in",
                "open the check-in and answer one changed receptionist turn",
                ["gse.adult.2022.p22.025"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the booking name and requested detail",
                "let the receptionist identify the booking and continue check-in",
                ["gse.adult.2022.p22.025"],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the objective specifies a few "
            "basic fixed expressions rather than a grammatical construction."
        ),
        "error": _error(
            "The learner gives the fictional booking name but supplies a different detail from the one the receptionist requested.",
            "The booking cannot be confirmed or check-in cannot continue accurately.",
            "the prompt-sensitive booking-detail demand in the fresh hotel role-play",
        ),
    },
}
