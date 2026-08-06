"""Travel transaction candidates."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["places_directions_travel"],
    "reviewed_at": "2026-07-17T19:51:11+03:00",
}

TRANSACTION_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.buy_a_basic_public_transport_ticket",
        "outcome": outcome(
            "a simple staffed public-transport ticket transaction",
            "buy the required ticket using fixed expressions",
            "destination and one basic ticket detail",
            "with a destination cue but without a complete dialogue model",
            "the clerk can issue the intended ticket",
            "In a fresh simple transport transaction, the learner can buy the intended ticket.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p22.011", "anchor",
            "The objective directly anchors buying public-transport tickets with basic fixed expressions.",
        )],
        "skill_codes": ["speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["transact"],
        "normalization_rationale": "Destination and one ticket detail serve one bounded purchase transaction.",
        "mastery": mastery(
            "A new role-play with a changed destination, clerk turn, and ticket detail.",
            {
                "comprehension": "Understands the clerk's basic question or confirmation.",
                "outcome_performance": "Requests enough information for the intended ticket to be issued.",
                "interaction_or_transfer": "Responds to the fresh clerk turn rather than reciting a script.",
                "control_or_repair": "Repairs one signalled destination or ticket-detail mix-up.",
            },
            ["The destination or required ticket detail is absent or wrong."],
            ["Minor form errors that do not change the requested ticket."],
            ["A destination cue and fixed-expression stems without completed turns."],
            "Use a different destination, ticket detail, and clerk prompt after a delay.",
        ),
        "scope": ["focused", "One short ticket transaction with two essential fields."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Ticket types and transport terms must remain familiar and culturally neutral."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.check_in_at_a_hotel",
        "outcome": outcome(
            "a simple hotel reception check-in",
            "complete the spoken check-in using fixed expressions",
            "the booking name and one basic requested detail",
            "with a safe fictional booking cue but without a dialogue model",
            "the receptionist can identify the booking and continue check-in",
            "In a fresh simple hotel situation, the learner can check in using basic fixed expressions.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p22.025", "anchor",
            "The objective directly anchors hotel check-in with a few basic fixed expressions.",
        )],
        "skill_codes": ["speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["transact"],
        "normalization_rationale": "Booking identification and one requested detail form one bounded check-in transaction.",
        "mastery": mastery(
            "A new hotel role-play with changed fictional booking details and receptionist turn.",
            {
                "comprehension": "Understands the receptionist's basic request or confirmation.",
                "outcome_performance": "Provides the booking name and required detail so check-in can continue.",
                "interaction_or_transfer": "Responds to the fresh receptionist turn rather than a memorized script.",
                "control_or_repair": "Repairs one signalled booking-detail mix-up.",
            },
            ["The booking cannot be identified or the required detail is wrong."],
            ["Minor form errors that preserve the booking information."],
            ["Safe fictional booking details and fixed-expression stems."],
            "Use a different hotel, booking detail, and receptionist prompt after a delay.",
        ),
        "scope": ["focused", "One short check-in with two essential fields."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Use fictional information and do not request real travel or identity data."],
    },
]
