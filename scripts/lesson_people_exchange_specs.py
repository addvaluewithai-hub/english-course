"""Interaction and mediation candidates for people and relationships."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["people_relationships"],
    "reviewed_at": "2026-07-17T16:48:13+03:00",
}

EXCHANGE_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.exchange_information_about_family_and_friends",
        "outcome": outcome(
            "a short predictable conversation about family or friends",
            "ask and answer basic factual questions",
            "two or three facts such as relationship, familiar role, or who has an item",
            "with slow clear turns but without a dialogue model",
            "both speakers obtain the requested information through relevant turns",
            "In a fresh predictable conversation, the learner can ask and answer basic questions about family or friends.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p22.002", "anchor", "The objective directly anchors limited questions and answers about family and friends."),
            evidence("gse.adult.2022.p23.013", "supporting", "People-known questions are an equivalent variant of the same exchange."),
            evidence("gse.adult.2022.p24.007", "supporting", "Stating who an item belongs to is one bounded factual answer in the exchange."),
            evidence(
                "cefr.cv2020.p074.conversation.02", "supporting",
                "Covers the predictable family-topic conversation; home-country and school examples remain for adjacent partitions.", "partial",
            ),
            evidence(
                "cefr.cv2020.p079.information_exchange.03", "supporting",
                "Covers people-known questions and answers; personal details and residence are claimed in identity, while possessions remain for home work.", "partial",
            ),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information", "give_information"],
        "normalization_rationale": "Relationship, role, and limited ownership facts are predictable turns in one people-information exchange.",
        "mastery": mastery(
            "A fresh family-or-friends information gap with two or three required facts.",
            {
                "comprehension": "Understands slow direct questions about the required people facts.",
                "outcome_performance": "Asks and answers enough relevant questions to exchange every required fact.",
                "interaction_or_transfer": "Responds to the partner's actual information rather than reciting a script.",
                "control_or_repair": "Keeps people and ownership references intelligible and handles simple repair when needed.",
            },
            ["The exchange fails because a required fact is neither requested nor supplied."],
            ["Harmless hesitation or minor form errors when the partner can respond."],
            ["Slow clear delivery, one neutral repetition, and fictional people."],
            "Use new people, relationships, and facts after a delay.",
        ),
        "scope": ["standard", "Two or three short question-answer pairs about known people."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Ownership is limited to one factual turn and must not expand into a separate object lesson."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.relay_a_family_or_role_fact",
        "outcome": outcome(
            "a simple supported situation where a family relationship or job is given in Arabic",
            "relay the essential fact in English",
            "who the person is plus one relationship or familiar job",
            "with limited word or phrase support but without a complete English model",
            "an English listener identifies the correct person and fact",
            "In a fresh supported mediation situation, the learner can relay a basic family or role fact in English.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01", "anchor",
            "Covers one family or familiar-role example of very simple predictable information; personal details are claimed in identity and broader information remains open.",
            "partial",
        )],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["mediation"],
        "function_codes": ["mediate_information"],
        "normalization_rationale": "Relaying one relationship or role fact is independently assessable from the personal-detail mediation child.",
        "mastery": mastery(
            "A fresh two-language introduction or check-in with a different family or role fact.",
            {
                "comprehension": "Identifies the correct person and fact in the Arabic input.",
                "outcome_performance": "Relays the relationship or role in simple intelligible English without changing it.",
                "interaction_or_transfer": "Adapts to a different person and informal context.",
                "control_or_repair": "Uses limited formulation help appropriately and repairs one signalled people-reference error.",
            },
            ["Relays the wrong person, relationship, or role."],
            ["Minor language errors that leave the relayed fact clear."],
            ["Limited words or phrase stems for formulation, as the source permits."],
            "Use a new person, fact, and context after a delay.",
            ["A complete English rendering or sentence-by-sentence model."],
        ),
        "scope": ["focused", "One predictable family or familiar-role fact."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Arabic input and formulation help require later construct-validity review."],
    },
]
