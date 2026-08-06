"""Interaction and mediation candidates for identity information."""

try:
    from scripts.lesson_identity_spec_helpers import (
        BASIC_SPOKEN,
        BASIC_WRITTEN,
        evidence,
        mastery,
        outcome,
    )
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import (
        BASIC_SPOKEN,
        BASIC_WRITTEN,
        evidence,
        mastery,
        outcome,
    )


EXCHANGE_SPECS = [
    {
        "candidate_id": "lesson_candidate.exchange_personal_details_orally",
        "outcome": outcome(
            "a short first-meeting or simple interview exchange",
            "ask and answer direct questions about personal details",
            "two or three details such as name, origin, residence, age, or role",
            "with slow clear questions but without a dialogue model",
            "both people obtain the required information through relevant turns",
            "In a fresh short exchange, the learner can ask and answer direct personal-detail questions without a dialogue model.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p23.004", "anchor", "The objective anchors asking simple questions about another person."),
            evidence("gse.adult.2022.p23.008", "supporting", "The same exchange elicits both giving and receiving personal details."),
            evidence(
                "cefr.cv2020.p079.information_exchange.03", "supporting",
                "Covers questions about self, another person, and residence; people-known and possession examples remain for adjacent partitions.",
                "partial",
            ),
            evidence("cefr.cv2020.p080.interviewing_and_being_interviewed.01", "supporting", "Slow direct interview questions are an equivalent bounded exchange variant."),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information"],
        "normalization_rationale": "Asking and answering are reciprocal moves serving one exchange and one interaction judgment.",
        "mastery": mastery(
            "A first meeting, check-in interview, or peer information-gap with a fresh partner profile.",
            {
                "comprehension": "Understands slow direct questions about the required personal details.",
                "outcome_performance": "Asks and answers enough relevant questions to exchange every required detail.",
                "interaction_or_transfer": "Responds to the partner's actual turns rather than reciting a fixed script.",
                "control_or_repair": "Maintains intelligible meaning and uses or responds to simple repair when needed.",
            },
            ["The exchange fails because required information is neither asked for nor supplied."],
            ["Harmless hesitation or minor form errors when the partner can respond."],
            ["Slow clear delivery; one neutral repetition; fictional details."],
            "Use a new partner profile and changed required details after a delay.",
        ),
        "scope": ["standard", "A bounded exchange of two or three question-answer pairs."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Questions must remain direct and non-idiomatic as the CEFR condition requires."],
    },
    {
        "candidate_id": "lesson_candidate.exchange_personal_details_in_writing",
        "outcome": outcome(
            "a short message or simple written information request",
            "ask for or pass on personal details in writing",
            "two requested details in a brief comprehensible message",
            "with a clear purpose but without a completed message model",
            "the reader can identify the request or the supplied details",
            "In a fresh short written exchange, the learner can ask for or pass on basic personal details without copying a model.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p082.overall_written_interaction.01", "anchor",
            "The descriptor directly anchors asking for or passing on personal details in writing.",
        )],
        "skill_codes": ["reading", "writing"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information"],
        "normalization_rationale": "A brief request and reply are variants of one written personal-information exchange.",
        "mastery": mastery(
            "A fresh direct message, chat-like note, or short reply with changed details.",
            {
                "comprehension": "Identifies whether the prompt requires a request or a reply.",
                "outcome_performance": "Writes a brief message that clearly asks for or supplies the required details.",
                "interaction_or_transfer": "The message responds to the actual written context and transfers to an equivalent variant.",
                "control_or_repair": "Spelling and sentence control preserve the details; an unclear item can be clarified in a follow-up." ,
            },
            ["The reader cannot tell what detail is requested or supplied."],
            ["Minor punctuation or grammar errors that do not change the request or detail."],
            ["A purpose cue; fictional personal details; neutral instruction repetition."],
            "Use a different message purpose and different details after a delay.",
        ),
        "scope": ["focused", "One brief message or request-reply pair about two details."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["Later map review must decide whether request and reply need separate variants, not separate lessons."],
    },
    {
        "candidate_id": "lesson_candidate.relay_personal_details_in_english",
        "outcome": outcome(
            "a simple supported situation where another person's details are given in Arabic",
            "relay the essential personal details in English",
            "two or three predictable details such as name, nationality, residence, or role",
            "with limited word or phrase support but without a complete English model",
            "an English listener receives the correct person's essential details",
            "In a fresh supported mediation situation, the learner can relay another person's basic details in English without a complete model.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01", "anchor",
            "Covers relaying other people's personal details; other predictable information remains for later mediation mapping.",
            "partial",
        )],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["mediation"],
        "function_codes": ["mediate_information"],
        "normalization_rationale": "Personal-detail mediation is independently assessable, so the broader descriptor is split by information purpose.",
        "mastery": mastery(
            "A fresh two-language introduction or check-in where a different person's details must be relayed.",
            {
                "comprehension": "Identifies the correct person and essential details in the Arabic input.",
                "outcome_performance": "Relays all required details in simple intelligible English without changing them.",
                "interaction_or_transfer": "Adapts the details to a new person and mediation context.",
                "control_or_repair": "Uses limited formulation help appropriately and repairs one signalled identity-detail error.",
            },
            ["Relays a detail for the wrong person or changes an essential detail."],
            ["Minor language errors that leave every relayed detail clear."],
            ["Limited words or phrase stems for formulation, as the source condition permits."],
            "Use a new person, details, and informal context after a delay.",
            ["A complete English rendering or sentence-by-sentence model."],
        ),
        "scope": ["focused", "Two or three predictable details about one person."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["The Arabic input and formulation help need expert review for construct validity."],
    },
]
