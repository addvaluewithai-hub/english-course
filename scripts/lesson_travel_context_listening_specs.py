"""Place-context and announcement listening candidates for travel."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["places_directions_travel"],
    "reviewed_at": "2026-07-17T19:51:11+03:00",
}

CONTEXT_LISTENING_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.identify_familiar_referents_from_spoken_descriptions",
        "outcome": outcome(
            "a fresh picture set of familiar objects, places, or people",
            "identify each referent from a short spoken description",
            "two or three referents distinguished by explicit familiar features",
            "without written descriptions or highlighted labels",
            "every description is linked to the intended referent",
            "In a fresh visual setting, the learner can identify familiar referents from short spoken descriptions.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p15.017", "anchor",
            "The objective directly anchors identifying objects, places, or people from spoken descriptions.",
        )],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["locate_information"],
        "normalization_rationale": "The referent types vary, but each item uses the same bounded description-to-referent judgment.",
        "mastery": mastery(
            "A new visual set with changed referents, features, and descriptions.",
            {
                "comprehension": "Recognizes the explicit features in each spoken description.",
                "outcome_performance": "Links every required description to the correct referent.",
                "interaction_or_transfer": "Transfers to new familiar referents and feature combinations.",
            },
            ["A required description is linked to the wrong referent."],
            ["A non-essential detail is missed after the referent is identified."],
            ["Clear pictures, slow delivery, and one complete replay."],
            "Use different referents, features, and a new voice after a delay.",
        ),
        "scope": ["focused", "Two or three short descriptions and clear visual referents."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Visual differences must reflect the spoken features without labels revealing the answer."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.understand_outline_of_a_simple_guided_tour",
        "outcome": outcome(
            "a very slow, clearly paused explanation in a predictable guided-tour setting",
            "identify the tour topic and main information",
            "the place or feature discussed plus one explicit fact",
            "with visual context but without a transcript",
            "the topic and main fact are identified correctly",
            "In a fresh predictable guided-tour setting, the learner can understand the outline of a very simple explanation.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p051.understanding_as_a_member_of_a_live.01", "anchor",
            "The descriptor directly anchors outline understanding in a very slow predictable guided-tour situation.",
        )],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "One tour topic and one explicit main fact form a bounded outline-comprehension judgment.",
        "mastery": mastery(
            "A new very short guided explanation with a changed place, speaker, and main fact.",
            {
                "comprehension": "Recognizes the place or feature being explained.",
                "outcome_performance": "Identifies the topic and one explicit main fact accurately.",
                "interaction_or_transfer": "Succeeds in a different predictable guided setting.",
            },
            ["The tour topic or required main fact is misunderstood."],
            ["A secondary descriptive detail is missed."],
            ["Very slow delivery, long pauses, and relevant visual context."],
            "Use a different guided setting, speaker, and fact after a delay.",
        ),
        "scope": ["focused", "One very short explanation with one main fact."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["The input must remain predictable and must not depend on cultural background knowledge."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.identify_key_details_in_a_slow_station_announcement",
        "outcome": outcome(
            "a fresh very short public-transport announcement",
            "identify the required numerical details",
            "one time and one other clearly stated figure",
            "with slow clear delivery but without a transcript",
            "both requested details are recorded accurately",
            "In a fresh slow station announcement, the learner can identify a time and another key figure.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p051.understanding_announcements_and_instructions.03", "anchor",
            "Covers figures and times in the railway-station example; shop-price use remains for service work.", "partial",
        )],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["locate_information"],
        "normalization_rationale": "A time and one other figure are parallel concrete details in one short transport announcement.",
        "mastery": mastery(
            "A new slow station announcement with changed time, figure, and voice.",
            {
                "comprehension": "Recognizes which spoken items are the requested numerical details.",
                "outcome_performance": "Records the required time and figure accurately.",
                "interaction_or_transfer": "Succeeds with a different announcement and numerical values.",
            },
            ["A required time or figure is missing or materially wrong."],
            ["A non-required station phrase is missed."],
            ["Slow clear delivery and one replay of the complete announcement."],
            "Use a different announcement, time, figure, and voice after a delay.",
        ),
        "scope": ["focused", "One short announcement and two numerical details."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Do not invent platform recognition unless the source-supported figure is explicitly presented."],
    },
]
