"""Reception candidates for the home, objects, and descriptions partition."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["home_objects_descriptions"],
    "reviewed_at": "2026-07-17T18:51:30+03:00",
}

RECEPTION_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.match_visual_descriptions_to_familiar_things",
        "outcome": outcome(
            "short simple descriptions paired with unfamiliar pictures",
            "match each description to the pictured referent",
            "two or three familiar objects, people, or animals and visible features",
            "with visual support but without highlighted answer words",
            "every description is matched to the correct picture",
            "In a fresh visual task, the learner can match short descriptions to familiar objects, people, or animals.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p09.002", "anchor", "The objective anchors visually supported reading of everyday-object features."),
            evidence("gse.adult.2022.p09.003", "supporting", "The same visual matching task extends to short descriptions of objects, people, and animals."),
        ],
        "skill_codes": ["reading"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "Visible features and referent matching form one bounded reading judgment across familiar picture types.",
        "mastery": mastery(
            "A fresh set of short descriptions and visually distinct familiar referents.",
            {
                "comprehension": "Recognizes the visible features stated in each description.",
                "outcome_performance": "Matches every required description to the correct referent.",
                "interaction_or_transfer": "Transfers the matching to new pictures and feature combinations.",
            },
            ["A required description is matched to the wrong referent."],
            ["A non-required detail is overlooked after the referent is identified."],
            ["Clear pictures and neutral instruction repetition."],
            "Use different referents, colours, sizes, and descriptions after a delay.",
        ),
        "scope": ["focused", "Two or three short descriptions with clear visual support."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Pictures must make source-stated features visible without revealing the answer through labels."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.identify_objects_from_slow_spoken_clues",
        "outcome": outcome(
            "a small picture set or immediate surroundings",
            "identify familiar objects from spoken questions or descriptions",
            "two or three objects distinguished by clear visible features",
            "with slow clear delivery but without written labels",
            "each spoken clue is linked to the intended object",
            "In a fresh visual setting, the learner can identify familiar objects from slow spoken clues.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p14.008", "anchor", "The objective anchors understanding object questions in pictures or immediate surroundings."),
            evidence("gse.adult.2022.p15.013", "supporting", "Slow clear object descriptions provide equivalent identification clues."),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information", "locate_information"],
        "normalization_rationale": "Questions and descriptions are equivalent slow spoken clues serving one object-identification task.",
        "mastery": mastery(
            "A new picture set or familiar environment with changed objects and clues.",
            {
                "comprehension": "Distinguishes the feature or object requested by each clue.",
                "outcome_performance": "Selects every intended object accurately.",
                "interaction_or_transfer": "Succeeds with new objects and different clue wording.",
            },
            ["Selects the wrong object or cannot distinguish the requested feature."],
            ["Brief hesitation before an accurate selection."],
            ["Slow clear delivery and one replay of each complete clue."],
            "Use different familiar objects and clues after a delay.",
        ),
        "scope": ["focused", "Two or three familiar objects and slow spoken clues."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["The visual field must not require specialist object vocabulary."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.understand_where_things_or_people_are",
        "outcome": outcome(
            "a simple unfamiliar room or surroundings picture",
            "locate things or people from slow spoken statements",
            "two or three explicit positions in the visible scene",
            "with picture support but without a transcript",
            "every required referent is located correctly",
            "In a fresh pictured scene, the learner can understand slow statements about where things or people are.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p14.011", "anchor", "The objective directly anchors slow picture-supported statements about positions."),
            evidence(
                "cefr.cv2020.p051.understanding_announcements_and_instructions.02", "supporting",
                "The descriptor confirms slow, clear location statements about an object in the immediate environment.",
            ),
            evidence(
                "cefr.cv2020.p049.understanding_conversation_between_other_people.01", "supporting",
                "Covers the surroundings clause; people, family, and hobbies have prior partial owners, while school remains open.", "partial",
            ),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "Explicit positions in one visible set of surroundings support one listening-location judgment.",
        "mastery": mastery(
            "A fresh pictured room or immediate setting with changed referents and positions.",
            {
                "comprehension": "Recognizes the referent and position in each slow statement.",
                "outcome_performance": "Locates every required thing or person correctly.",
                "interaction_or_transfer": "Transfers to a new scene and changed positions.",
            },
            ["A required thing or person is placed in the wrong position."],
            ["Misses an optional scene detail not named in the statements."],
            ["Slow clear delivery, picture support, and one complete replay."],
            "Use a different pictured setting and positions after a delay.",
        ),
        "scope": ["focused", "One visible scene with two or three explicit positions."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Later school and place work must claim only their remaining clauses."],
    },
]
