"""Route and concrete-information listening candidates for travel."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["places_directions_travel"],
    "reviewed_at": "2026-07-17T19:51:11+03:00",
}

LISTENING_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.follow_slow_spoken_route_directions",
        "outcome": outcome(
            "a fresh simple street or transport plan",
            "follow slow spoken directions from a start to a destination",
            "two or three route moves on foot or public transport",
            "with a plan and one complete replay but without a traced route",
            "the stated route ends at the correct destination",
            "In a fresh simple plan, the learner can follow slow spoken route directions.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p15.004", "anchor", "The objective anchors directions on foot or by public transport."),
            evidence("gse.adult.2022.p15.015", "supporting", "The objective confirms slow, clear simple directions."),
            evidence("cefr.cv2020.p051.understanding_announcements_and_instructions.01", "supporting", "The descriptor confirms carefully delivered short directions."),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["follow_instructions"],
        "normalization_rationale": "Walking and public-transport variants use one route-following listening judgment.",
        "mastery": mastery(
            "A new plan with changed start, destination, voice, and route moves.",
            {
                "comprehension": "Recognizes the ordered route moves and destination.",
                "outcome_performance": "Traces or selects the complete stated route accurately.",
                "interaction_or_transfer": "Transfers to a new plan and changed delivery.",
            },
            ["An essential route move is reversed, omitted, or ends at the wrong destination."],
            ["Brief hesitation before an accurate route choice."],
            ["A clear plan, slow delivery, and one complete replay."],
            "Use a different plan, route, and voice after a delay.",
        ),
        "scope": ["focused", "One route with two or three spoken moves."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Public-transport vocabulary must remain familiar and visually supported."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.locate_place_and_time_in_slow_recordings",
        "outcome": outcome(
            "a short unfamiliar dialogue or recording about an everyday plan",
            "locate the named place and time",
            "one concrete place and one time needed for the plan",
            "with very slow clear delivery but without a transcript",
            "both requested details are recorded accurately",
            "In a fresh slow recording, the learner can identify a concrete place and time.",
        ),
        "evidence": [
            evidence(
                "gse.adult.2022.p14.007", "anchor",
                "Covers extracting place names; the people-name clause retains its prior partial owner.", "partial",
            ),
            evidence(
                "cefr.cv2020.p048.overall_oral_comprehension.02", "supporting",
                "Covers concrete place information; concrete time retains its prior partial owner.", "partial",
            ),
            evidence("cefr.cv2020.p052.understanding_audio_or_signed_media_and_recordings.01", "supporting", "The descriptor directly supports finding places and times in a slow short recording."),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["locate_information"],
        "normalization_rationale": "A place and time are linked concrete fields in one everyday-plan listening task.",
        "mastery": mastery(
            "A new short dialogue or recording with a changed place, time, and voice.",
            {
                "comprehension": "Distinguishes the requested place and time from other words.",
                "outcome_performance": "Records both concrete details accurately.",
                "interaction_or_transfer": "Succeeds with a different recording and everyday plan.",
            },
            ["The required place or time is absent or materially wrong."],
            ["A non-required name or social phrase is missed."],
            ["Very slow clear delivery and one replay of the complete input."],
            "Use a different place, time, voice, and context after a delay.",
        ),
        "scope": ["focused", "One short input and two concrete details."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Place names must be acoustically distinct and not require specialist knowledge."],
    },
]
