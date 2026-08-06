"""Interaction candidates for home, objects, and descriptions."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["home_objects_descriptions"],
    "reviewed_at": "2026-07-17T18:51:30+03:00",
}

EXCHANGE_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.exchange_visible_object_information",
        "outcome": outcome(
            "a picture-based information gap about familiar objects",
            "ask and answer basic object questions",
            "colour, size, or quantity facts for two or three visible objects",
            "with picture or question-type cues but without a dialogue model",
            "both speakers obtain every requested object fact",
            "In a fresh visual information gap, the learner can exchange basic colour, size, and quantity facts about objects.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p22.004", "anchor", "The objective anchors answering simple colour or size questions about objects."),
            evidence("gse.adult.2022.p22.026", "anchor", "The objective adds asking simple colour or size questions."),
            evidence("gse.adult.2022.p23.003", "supporting", "How-many questions are a parallel object-information move in the same visual gap."),
            evidence("cefr.cv2020.p079.information_exchange.06", "supporting", "Naming and asking about object colours confirms the two-way exchange."),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information"],
        "normalization_rationale": "Colour, size, and quantity are equivalent visible fields exchanged through one short object information gap.",
        "mastery": mastery(
            "A fresh paired picture gap with changed objects, features, and question roles.",
            {
                "comprehension": "Understands which object fact the partner requests.",
                "outcome_performance": "Asks and answers enough relevant questions to exchange every required fact.",
                "interaction_or_transfer": "Responds to the partner's actual picture and changed question roles.",
                "control_or_repair": "Keeps colour, size, and quantity meaning clear and repairs one signalled mix-up.",
            },
            ["A required fact is not exchanged or is assigned to the wrong object."],
            ["Minor form errors or hesitation when the partner can still respond."],
            ["Picture cues and question-type labels without completed questions or answers."],
            "Use new objects, features, quantities, and partner roles after a delay.",
        ),
        "scope": ["standard", "Two or three objects and three short question-answer turns."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Quantity must remain visually countable and A1-bounded."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.exchange_basic_information_about_a_home",
        "outcome": outcome(
            "a short conversation comparing a safe real or fictional home",
            "ask for and give basic home information",
            "two or three facts about rooms, familiar things, or possessions",
            "with topic cues and fictional-answer permission but without a dialogue model",
            "both speakers obtain the requested home facts",
            "In a fresh short conversation, the learner can exchange basic information about a home and familiar possessions.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p22.017", "anchor", "The objective directly anchors asking for and giving very basic home information."),
            evidence(
                "cefr.cv2020.p079.information_exchange.03", "supporting",
                "Covers the things-they-have clause; personal details, residence, and people-known clauses have prior partial owners.", "partial",
            ),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information"],
        "normalization_rationale": "Rooms, familiar things, and possession facts are adjacent fields in one bounded home-information exchange.",
        "mastery": mastery(
            "A fresh home-information gap using safe real or fictional details.",
            {
                "comprehension": "Understands which home or possession facts the partner requests.",
                "outcome_performance": "Asks for and gives every required fact clearly enough to record.",
                "interaction_or_transfer": "Responds to the actual partner information and changed prompts.",
                "control_or_repair": "Keeps ownership and home facts clear and repairs one signalled misunderstanding.",
            },
            ["A required home fact is absent or ownership is reversed."],
            ["Minor form errors that preserve the rooms, things, and ownership facts."],
            ["Topic cues, fictional-answer permission, and neutral instruction repetition."],
            "Use a different fictional home, possessions, and question roles after a delay.",
        ),
        "scope": ["standard", "Two or three home facts exchanged in short turns."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Prompts must not assume home ownership, room count, wealth, or disclosure of private living conditions."],
    },
]
