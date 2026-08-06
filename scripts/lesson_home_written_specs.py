"""Written production candidates for home, objects, and descriptions."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["home_objects_descriptions"],
    "reviewed_at": "2026-07-17T18:51:30+03:00",
}

WRITTEN_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.write_a_simple_object_description",
        "outcome": outcome(
            "a label, listing, or short note about a familiar object",
            "write a basic object description",
            "the object's identity plus two visible colour, size, or shape features",
            "with the object or picture visible and limited field cues but without completed sentences",
            "a reader can identify the object and required features",
            "In a fresh simple writing task, the learner can describe a familiar object using visible features.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.007", "anchor", "The objective anchors model-supported written colour or size description."),
            evidence("gse.adult.2022.p37.019", "supporting", "A familiar object remains the common subject of the same short description."),
            evidence("cefr.cv2020.p067.creative_writing.03", "supporting", "Simple words and phrases about everyday-object features define acceptable A1 output."),
        ],
        "skill_codes": ["writing"],
        "mode_codes": ["production"],
        "function_codes": ["describe", "give_information"],
        "normalization_rationale": "Object identity and two visible features form one short reader-usable description.",
        "mastery": mastery(
            "A fresh familiar object or picture with changed visible features and purpose.",
            {
                "comprehension": "Identifies the object and features required by the writing prompt.",
                "outcome_performance": "Writes enough accurate information for a reader to identify the object.",
                "interaction_or_transfer": "Transfers the description to a new object and feature combination.",
                "control_or_repair": "Spelling and sentence control preserve identity and features; one flagged item can be revised.",
            },
            ["The object cannot be identified or a required feature is absent or reversed."],
            ["Minor spelling, article, or punctuation errors that preserve every feature."],
            ["The object or picture, limited field cues, and a non-answer-revealing format model."],
            "Use a different object, visible features, and writing purpose after a delay.",
        ),
        "scope": ["focused", "One object and two or three short descriptive statements."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["A format model may show layout but must not supply the target feature sentences."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.write_a_simple_room_description",
        "outcome": outcome(
            "an unfamiliar room picture or safe fictional room plan",
            "write what the room looks like and where things are",
            "two or three familiar things and their basic positions",
            "with picture or object-name cues but without completed sentences",
            "a reader can reconstruct the required room details",
            "In a fresh pictured-room task, the learner can write a very simple description of the room and object positions.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.017", "anchor", "The objective anchors fixed-expression writing about positions in a picture."),
            evidence("cefr.cv2020.p067.creative_writing.02", "supporting", "Very simple room description supplies the coherent setting for those positions."),
        ],
        "skill_codes": ["writing"],
        "mode_codes": ["production"],
        "function_codes": ["describe"],
        "normalization_rationale": "Room appearance and a few object positions are one small spatial description that a reader can reconstruct.",
        "mastery": mastery(
            "A fresh room picture or plan with changed familiar objects and positions.",
            {
                "comprehension": "Identifies the room details and positions requested by the prompt.",
                "outcome_performance": "Writes enough accurate statements for a reader to reconstruct all required details.",
                "interaction_or_transfer": "Transfers the description to a different room or plan.",
                "control_or_repair": "Position meaning stays clear and one flagged reversal can be revised.",
            },
            ["A required thing is omitted or placed in the wrong position."],
            ["Minor spelling or grammar errors that preserve the room layout."],
            ["Picture or object-name cues and neutral instruction repetition."],
            "Use a different room, objects, and positions after a delay.",
        ),
        "scope": ["focused", "One room and two or three object-position statements."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["The room prompt must not assume a culturally specific or affluent home layout."],
    },
]
