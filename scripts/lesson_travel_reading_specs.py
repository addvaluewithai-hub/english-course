"""Reading candidates for the places, directions, and travel partition."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["places_directions_travel"],
    "reviewed_at": "2026-07-17T19:51:11+03:00",
}

READING_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.follow_simple_written_wayfinding_directions",
        "outcome": outcome(
            "a fresh simple map, store guide, or route note",
            "follow the written directions to a destination",
            "a short route from one named point to another",
            "with a simple plan but without a traced answer path",
            "the correct destination and route are selected",
            "In a fresh simple plan, the learner can follow short written directions to a destination.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p09.004", "anchor", "The objective directly anchors short written directions from one point to another."),
            evidence("cefr.cv2020.p056.reading_for_orientation.02", "supporting", "Store guides and lift directions provide an indoor wayfinding variant."),
            evidence("cefr.cv2020.p058.reading_instructions.01", "supporting", "The descriptor confirms short written directions from X to Y."),
        ],
        "skill_codes": ["reading"],
        "mode_codes": ["reception"],
        "function_codes": ["follow_instructions"],
        "normalization_rationale": "Route notes and store guides require the same bounded written-wayfinding judgment.",
        "mastery": mastery(
            "A new simple map or guide with changed start, destination, and route wording.",
            {
                "comprehension": "Recognizes the start, destination, and route moves.",
                "outcome_performance": "Selects the correct destination and follows the stated route.",
                "interaction_or_transfer": "Transfers the performance to a different plan and direction wording.",
            },
            ["The selected destination or an essential route move is wrong."],
            ["A harmless pause while checking the plan."],
            ["A clear plan and neutral instruction repetition."],
            "Use a different plan, route, and destination after a delay.",
        ),
        "scope": ["focused", "One short route with two or three explicit moves."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["The plan must not reveal the answer through colour or path highlighting."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.understand_simple_place_and_hotel_information",
        "outcome": outcome(
            "a short illustrated place description or basic hotel information card",
            "identify the essential place information",
            "two explicit facts such as a visible feature, facility, or meal time",
            "without translation or highlighted answer phrases",
            "every requested fact is identified accurately",
            "In fresh simple place information, the learner can identify two essential facts.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p09.006", "anchor", "The objective directly anchors understanding simple descriptions of places."),
            evidence("cefr.cv2020.p056.reading_for_orientation.03", "supporting", "Basic hotel information supplies a practical place-information variant."),
            evidence(
                "cefr.cv2020.p057.reading_for_information_and_argument.02", "supporting",
                "Covers the illustrated travel-text example; the other personal-interest examples are outside this partition.", "partial",
            ),
        ],
        "skill_codes": ["reading"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information", "locate_information"],
        "normalization_rationale": "Short place descriptions and hotel cards support one practical search for explicit place facts.",
        "mastery": mastery(
            "A fresh illustrated place or hotel card with changed facts and layout.",
            {
                "comprehension": "Recognizes which details describe the place or its basic services.",
                "outcome_performance": "Identifies every required explicit fact accurately.",
                "interaction_or_transfer": "Succeeds with a different place, layout, and fact set.",
            },
            ["A required place, facility, or time fact is missed or changed."],
            ["An optional descriptive detail is overlooked."],
            ["Relevant illustrations and neutral instruction repetition."],
            "Use a different place and information-card format after a delay.",
        ),
        "scope": ["focused", "One very short text and two explicit place facts."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Illustrations must support context without making the reading unnecessary."],
    },
]
