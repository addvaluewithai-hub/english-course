"""Interaction and mediation candidates for routines, time, and leisure."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["routines_time_leisure"],
    "reviewed_at": "2026-07-17T17:49:14+03:00",
}

EXCHANGE_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.follow_simple_game_or_activity_instructions",
        "outcome": outcome(
            "a familiar game or simple group activity",
            "act on basic spoken instructions",
            "two or three commands involving a familiar action, time, or number",
            "with slow clear delivery but without demonstration of every answer",
            "the required actions are completed in the stated order",
            "In a fresh familiar activity, the learner can act on basic spoken instructions in order.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p15.003", "anchor", "The objective directly anchors spoken game or sport commands."),
            evidence("cefr.cv2020.p077.goal_oriented_co_operation.02", "supporting", "Covers instructions involving times and numbers; locations remain shared with place work.", "partial"),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["reception", "interaction"],
        "function_codes": ["follow_instructions"],
        "normalization_rationale": "A short command sequence and the learner's actions form one observable cooperation task.",
        "mastery": mastery(
            "A fresh familiar activity with two or three changed commands.",
            {
                "comprehension": "Distinguishes the required actions, times, or numbers.",
                "outcome_performance": "Completes every required action in the stated order.",
                "interaction_or_transfer": "Responds to new commands rather than imitating a memorized sequence.",
                "control_or_repair": "Requests or uses one simple clarification when needed.",
            },
            ["A required action is omitted, reversed, or performed at the wrong stated time or count."],
            ["Harmless hesitation before a correct action."],
            ["Slow clear delivery and one neutral repetition."],
            "Use different familiar commands and order after a delay.",
        ),
        "scope": ["focused", "Two or three basic commands in one familiar activity."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Physical actions must be accessible and have an equivalent response route."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.exchange_routine_and_preference_information",
        "outcome": outcome(
            "a short direct conversation about daily or free-time life",
            "ask and answer predictable questions",
            "two or three routine, sport, food, or leisure preference facts",
            "with slow clear turns and optional question cues but without a dialogue model",
            "both speakers obtain the requested facts through relevant turns",
            "In a fresh short conversation, the learner can exchange routine and preference information.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p23.016", "anchor", "The objective anchors answers about daily activities or routines with model support."),
            evidence("cefr.cv2020.p075.informal_discussion_with_friends.01", "supporting", "The descriptor adds direct exchange of likes and dislikes."),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information", "express_preference"],
        "normalization_rationale": "Routine and preference questions are adjacent predictable turns in one basic get-to-know-you exchange.",
        "mastery": mastery(
            "A fresh information gap requiring two or three routine or preference facts.",
            {
                "comprehension": "Understands slow direct questions about familiar activities and preferences.",
                "outcome_performance": "Asks or answers enough relevant questions to exchange every required fact.",
                "interaction_or_transfer": "Responds to the partner's actual information rather than reciting a script.",
                "control_or_repair": "Keeps positive and negative meaning clear and handles simple repair when needed.",
            },
            ["A required fact is not exchanged or a like/dislike meaning is reversed."],
            ["Harmless hesitation or minor form errors when the partner can respond."],
            ["Slow clear delivery and short question cues rather than completed answers."],
            "Use new activities, preferences, and question roles after a delay.",
        ),
        "scope": ["standard", "Two or three short question-answer pairs."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["A model may support question form but must not supply the learner's answers."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.relay_a_time_or_place_detail",
        "outcome": outcome(
            "a supported situation where a simple schedule detail is given in Arabic",
            "relay the essential detail in English",
            "one predictable time or place fact",
            "with limited word or phrase support but without a complete English model",
            "an English listener records the correct detail",
            "In a fresh supported mediation situation, the learner can relay a simple time or place detail in English.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p095.relaying_specific_information_in_speech_or_sign.01", "anchor",
            "The descriptor directly anchors relaying predictable time-or-place information.",
        )],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["mediation"],
        "function_codes": ["mediate_information"],
        "normalization_rationale": "One time or place fact is a single bounded mediation judgment with equivalent variants.",
        "mastery": mastery(
            "A fresh two-language schedule or meeting detail with a changed time or place.",
            {
                "comprehension": "Identifies the essential time or place in the Arabic input.",
                "outcome_performance": "Relays the detail in simple intelligible English without changing it.",
                "interaction_or_transfer": "Adapts to a different detail and familiar context.",
                "control_or_repair": "Uses limited formulation help appropriately and repairs one signalled detail error.",
            },
            ["Relays the wrong time or place."],
            ["Minor language errors that leave the detail clear."],
            ["Limited words or phrase stems for formulation, as the source permits."],
            "Use a new time or place and context after a delay.",
            ["A complete English rendering or sentence-by-sentence model."],
        ),
        "scope": ["focused", "One predictable time or place fact."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Arabic input and formulation help require later construct-validity review."],
    },
]
