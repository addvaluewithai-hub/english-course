"""Reviewed targets for the opening food and service reception candidates."""


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


SERVICE_RECEPTION_DECISIONS = {
    "lesson_candidate.identify_a_price_in_slow_spoken_service_information": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar item, service, currency, and price words",
                "match the stated cost to the intended item or service",
                [
                    "gse.adult.2022.p15.007",
                    "gse.adult.2022.p15.008",
                    "cefr.cv2020.p051.understanding_announcements_and_instructions.03",
                ],
            )],
            "phrases": [(
                "Short simple spoken price statements in shop contexts",
                "locate the price in a changed dialogue or announcement",
                [
                    "gse.adult.2022.p15.007",
                    "cefr.cv2020.p051.understanding_announcements_and_instructions.03",
                ],
            )],
            "pronunciation": [(
                "Recognition of contrasting prices and other numbers in slow clear speech",
                "distinguish the price from the distractor number without a transcript",
                [
                    "gse.adult.2022.p15.007",
                    "gse.adult.2022.p15.008",
                    "cefr.cv2020.p051.understanding_announcements_and_instructions.03",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence names price "
            "reception in slow speech without specifying a construction; pronunciation "
            "is receptive number and price recognition only."
        ),
        "error": _error(
            "The learner recognises the spoken price but attaches it to the distractor item or service.",
            "The reported cost does not answer the requested price question accurately.",
            "the price-to-item matching demand in the fresh recording",
        ),
    },
    "lesson_candidate.follow_a_slow_everyday_service_exchange": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar words for concrete customer needs, items, and service responses",
                "identify the requested item or service and one response detail",
                [
                    "gse.adult.2022.p15.019",
                    "cefr.cv2020.p049.understanding_conversation_between_other_people.02",
                    "cefr.cv2020.p073.understanding_an_interlocutor.01",
                ],
            )],
            "phrases": [(
                "Everyday expressions for simple concrete needs and service transactions",
                "connect the customer need with the corresponding service response",
                [
                    "gse.adult.2022.p15.019",
                    "cefr.cv2020.p049.understanding_conversation_between_other_people.02",
                    "cefr.cv2020.p073.understanding_an_interlocutor.01",
                    "cefr.cv2020.p074.conversation.01",
                ],
            )],
            "pronunciation": [(
                "Recognition of essential need and response words in slow clear speech",
                "understand both sides after the permitted repetition without answer cues",
                [
                    "gse.adult.2022.p15.019",
                    "cefr.cv2020.p049.understanding_conversation_between_other_people.02",
                    "cefr.cv2020.p073.understanding_an_interlocutor.01",
                    "cefr.cv2020.p074.conversation.01",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence supports "
            "understanding everyday expressions and a transaction without naming a "
            "construction; pronunciation is receptive recognition only."
        ),
        "error": _error(
            "The learner identifies the customer's concrete need but assigns the service response to the wrong item or speaker.",
            "One essential side of the exchange is reported inaccurately.",
            "the need-and-response linkage in the fresh two-turn exchange",
        ),
    },
    "lesson_candidate.find_key_details_in_a_simple_advertisement_or_leaflet": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar offer, cost, date, place, and departure-time words",
                "locate the two requested practical details in the changed public text",
                ["cefr.cv2020.p056.reading_for_orientation.04"],
            )],
            "phrases": [(
                "Simple important information statements in advertisements and leaflets",
                "report each explicit detail without changing what it refers to",
                ["cefr.cv2020.p056.reading_for_orientation.04"],
            )],
            "pronunciation": [],
        },
        "decision_note": (
            "No separate grammar target is assigned because the descriptor names an "
            "information-search outcome without a construction; no pronunciation target "
            "is assigned because mastery is written reception."
        ),
        "error": _error(
            "The learner finds two prominent details but reports one under the wrong category, such as treating a departure time as an event date.",
            "At least one requested practical detail is inaccurate.",
            "the detail-to-label matching demand in the changed public text",
        ),
    },
}
