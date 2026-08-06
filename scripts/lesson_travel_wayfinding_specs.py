"""Interactive wayfinding candidates for the travel partition."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["places_directions_travel"],
    "reviewed_at": "2026-07-17T19:51:11+03:00",
}

WAYFINDING_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.follow_simple_directions_from_an_interlocutor",
        "outcome": outcome(
            "a live map or simple location task with a cooperative interlocutor",
            "follow carefully delivered directions",
            "two or three basic moves involving familiar locations",
            "with slow speech and clarification but without a demonstrated route",
            "the learner acts on the directions in the stated order",
            "In a fresh live location task, the learner can follow simple directions from an interlocutor.",
        ),
        "evidence": [
            evidence("cefr.cv2020.p073.understanding_an_interlocutor.02", "anchor", "The descriptor anchors understanding an interlocutor and following short directions."),
            evidence("cefr.cv2020.p077.goal_oriented_co_operation.01", "supporting", "The distinct scale placement confirms the same move in goal-oriented cooperation."),
            evidence("cefr.cv2020.p079.information_exchange.01", "supporting", "The distinct scale placement confirms the same move in information exchange."),
            evidence(
                "cefr.cv2020.p077.goal_oriented_co_operation.02", "supporting",
                "Covers acting on instructions involving locations; times and numbers retain their prior partial owner.", "partial",
            ),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["follow_instructions"],
        "normalization_rationale": "The repeated descriptors are distinct scale evidence for one live direction-following performance.",
        "mastery": mastery(
            "A new live map or location task with changed directions and roles.",
            {
                "comprehension": "Distinguishes the ordered location moves addressed to them.",
                "outcome_performance": "Acts on every required direction in order.",
                "interaction_or_transfer": "Responds to the interlocutor's fresh directions rather than a memorized route.",
                "control_or_repair": "Uses or responds to one simple clarification when needed.",
            },
            ["A required move is omitted, reversed, or reaches the wrong location."],
            ["Harmless hesitation before the correct move."],
            ["Slow clear delivery, a simple plan, and neutral repetition."],
            "Use a different plan, interlocutor, and route after a delay.",
        ),
        "scope": ["standard", "Two or three live directions in one location task."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["The three identical wordings remain separate scale records and are not treated as duplicates."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.exchange_basic_wayfinding_information",
        "outcome": outcome(
            "a fresh map-based information gap",
            "ask for directions and answer basic location questions",
            "one destination and two familiar people or things",
            "with a map and short question cues but without a dialogue model",
            "both speakers obtain the required locations and route",
            "In a fresh map information gap, the learner can ask for directions and answer basic location questions.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p23.009", "anchor", "The objective anchors limited answers about locations of people or things."),
            evidence("gse.adult.2022.p24.005", "anchor", "The objective adds asking for simple directions with a map or plan."),
        ],
        "skill_codes": ["speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information", "request"],
        "normalization_rationale": "Asking for a route and answering location questions are reciprocal moves in one map information gap.",
        "mastery": mastery(
            "A new paired map gap with changed destinations, referents, and roles.",
            {
                "comprehension": "Recognizes which destination or referent the partner asks about.",
                "outcome_performance": "Asks for the route and gives each required location clearly.",
                "interaction_or_transfer": "Responds to the partner's actual map and changed roles.",
                "control_or_repair": "Keeps locations distinct and repairs one signalled mix-up.",
            },
            ["A required location or route request is absent or points to the wrong place."],
            ["Minor form errors when the location remains clear."],
            ["A simple map and short question-type cues."],
            "Use a different map, destination, referents, and roles after a delay.",
        ),
        "scope": ["standard", "One direction request and two short location answers."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Question cues must not contain completed learner turns."],
    },
]
