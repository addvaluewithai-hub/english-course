"""Spoken production candidates for home, objects, and descriptions."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["home_objects_descriptions"],
    "reviewed_at": "2026-07-17T18:51:30+03:00",
}

SPOKEN_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.describe_a_familiar_object_orally",
        "outcome": outcome(
            "a simple show-and-tell with a familiar object or picture",
            "give a basic spoken description",
            "the object's identity plus visible shape, colour, or size features",
            "with the object visible and preparation time but without a complete model",
            "listeners can identify the object and its required features",
            "In a fresh show-and-tell, the learner can describe a familiar object using basic visible features.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p22.015", "anchor", "The objective anchors basic spoken colour or size description."),
            evidence("gse.adult.2022.p24.001", "supporting", "The objective confirms simple-language object description as the same performance."),
            evidence("cefr.cv2020.p063.sustained_monologue_giving_information.01", "supporting", "Naming an shown object and indicating shape and colour defines the prepared show-and-tell variant."),
        ],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["describe", "give_information"],
        "normalization_rationale": "Identity and two visible features are inseparable parts of one prepared object description.",
        "mastery": mastery(
            "A fresh familiar object or picture with changed visible features.",
            {
                "comprehension": "Understands which object and features must be described.",
                "outcome_performance": "Names the object and states enough accurate features for identification.",
                "interaction_or_transfer": "Describes a different object rather than repeating a memorized text.",
                "control_or_repair": "Feature meaning stays intelligible and one signalled mix-up can be repaired.",
            },
            ["The listener cannot identify the object or a required feature is reversed."],
            ["Minor form errors or pauses that preserve all visible-feature meaning."],
            ["The object or picture, brief preparation time, and neutral instruction repetition."],
            "Use a different object, shape, colour, and size after a delay.",
        ),
        "scope": ["focused", "One familiar object and two or three visible features."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Objects and features need later vocabulary review before lesson approval."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.describe_an_objects_position_orally",
        "outcome": outcome(
            "a simple unfamiliar room or picture",
            "say where a specified object is",
            "two or three objects and their basic positions",
            "with picture cues but without completed sentences to copy",
            "a listener can locate every required object",
            "In a fresh pictured scene, the learner can describe where specified objects are in a basic way.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p22.008", "anchor",
            "The objective directly anchors very basic spoken position descriptions.",
        )],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["describe"],
        "normalization_rationale": "Several parallel object positions in one visible scene form one bounded location update.",
        "mastery": mastery(
            "A fresh room or scene picture with changed objects and positions.",
            {
                "comprehension": "Identifies which objects require position statements.",
                "outcome_performance": "States a usable position for every required object.",
                "interaction_or_transfer": "Adapts the statements to a different scene.",
                "control_or_repair": "Position meaning stays intelligible and one signalled reversal can be repaired.",
            },
            ["A listener places a required object in the wrong location."],
            ["Minor form errors that preserve the spatial relation."],
            ["Picture and object-name cues; neutral instruction repetition."],
            "Use a different scene, objects, and positions after a delay.",
        ),
        "scope": ["focused", "Two or three basic position statements in one scene."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Later place-direction work must not duplicate this object-position anchor."],
    },
]
