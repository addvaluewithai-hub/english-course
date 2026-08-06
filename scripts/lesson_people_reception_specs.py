"""Reception candidates for the people-and-relationships partition."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["people_relationships"],
    "reviewed_at": "2026-07-17T16:48:13+03:00",
}

RECEPTION_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.locate_people_names_in_dialogue",
        "outcome": outcome(
            "a short unfamiliar dialogue delivered slowly and clearly",
            "identify the people named",
            "one or two names needed to match speakers or people mentioned",
            "without a transcript or highlighted answer",
            "each requested name is matched to the correct person",
            "In a fresh slow dialogue, the learner can identify the people named without a transcript.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p14.007", "anchor",
            "Covers extracting people's names; the alternative place-name clause remains for the places partition.",
            "partial",
        )],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["locate_information"],
        "normalization_rationale": "People-name extraction has one bounded listening purpose; place-name extraction remains separate.",
        "mastery": mastery(
            "A fresh two-speaker dialogue naming one or two people, plus an equivalent replacement.",
            {
                "comprehension": "Recognizes which spoken items are people's names.",
                "outcome_performance": "Matches every requested name to the correct person.",
                "interaction_or_transfer": "Repeats the performance with different voices and names.",
            },
            ["A requested name is missed or assigned to the wrong person."],
            ["A harmless spelling approximation that still identifies the name."],
            ["Slow clear delivery and one replay of the complete dialogue."],
            "Use new voices and names after a delay.",
        ),
        "scope": ["focused", "One short dialogue and one or two people names."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Names must be acoustically distinct and culturally neutral."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.understand_talk_about_people_and_family",
        "outcome": outcome(
            "a short slow conversation between other people",
            "identify basic facts about a person or family",
            "who is discussed plus two clear family or personal facts",
            "without a transcript or translated model",
            "the facts are attributed to the correct person",
            "In a fresh slow conversation, the learner can identify basic facts about a person or family.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p049.understanding_conversation_between_other_people.01", "anchor",
            "Covers expressions about the person discussed and family; school, hobbies, and surroundings remain for later partitions.",
            "partial",
        )],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "The selected person-and-family clause supports one third-party listening judgment.",
        "mastery": mastery(
            "A new slow conversation about one person or family, with changed details.",
            {
                "comprehension": "Recognizes who the speakers are discussing.",
                "outcome_performance": "Identifies two essential stated facts and attributes them correctly.",
                "interaction_or_transfer": "Succeeds with new speakers and a different family context.",
            },
            ["Confuses the person or changes an essential relationship fact."],
            ["Misses an optional detail beyond the required pair."],
            ["Slow clear delivery and one complete replay."],
            "Use different speakers, people, and facts after a delay.",
        ),
        "scope": ["focused", "One short conversation and two essential facts."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["The audio must not require inference beyond explicit A1 expressions."],
    },
]
