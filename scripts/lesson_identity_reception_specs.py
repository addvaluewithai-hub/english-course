"""Reception candidates for identity and personal information."""

try:
    from scripts.lesson_identity_spec_helpers import (
        BASIC_RECEPTIVE,
        evidence,
        mastery,
        outcome,
    )
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import (
        BASIC_RECEPTIVE,
        evidence,
        mastery,
        outcome,
    )


RECEPTION_SPECS = [
    {
        "candidate_id": "lesson_candidate.locate_written_personal_details",
        "outcome": outcome(
            "a short unfamiliar profile, card, or form-like text",
            "locate requested personal details",
            "two or three details such as name, age, nationality, or address",
            "without highlighted answers or a translated model",
            "the selected details identify the person accurately",
            "In a fresh short text, the learner can locate requested personal details without answer-revealing support.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p09.009", "anchor",
            "The objective directly anchors limited extraction of personal details.",
        )],
        "skill_codes": ["reading"],
        "mode_codes": ["reception"],
        "function_codes": ["locate_information"],
        "normalization_rationale": "One short source and one set of requested fields support a single reception judgment.",
        "mastery": mastery(
            "An unseen short profile or card with an equivalent replacement text.",
            {
                "comprehension": "Identifies which personal details the prompt requests.",
                "outcome_performance": "Selects the requested details without changing their essential meaning.",
                "interaction_or_transfer": "Repeats the performance with a new person and layout.",
            },
            ["A requested identity detail is missing or attributed to the wrong person."],
            ["A harmless formatting difference that preserves the detail."],
            ["Neutral instruction repetition in MSA without translating the source text."],
            "Use a new profile with different details after a delay.",
        ),
        "scope": ["focused", "One short text and two or three requested details."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": [],
    },
    {
        "candidate_id": "lesson_candidate.understand_spoken_personal_introductions",
        "outcome": outcome(
            "a short clear introduction of oneself or another person",
            "identify the main personal information",
            "name plus two basic details such as age, origin, residence, or role",
            "without a transcript or translated model",
            "the listener matches the essential details to the correct person",
            "In a fresh clear introduction, the learner can identify the speaker's main personal information without a transcript.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p14.001", "anchor", "The objective anchors understanding information in self-introductions."),
            evidence("gse.adult.2022.p15.014", "supporting", "The same task family also covers a simple introduction of another person."),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "Self-introduction and third-person introduction differ only in speaker framing, not purpose or assessment.",
        "mastery": mastery(
            "A fresh short introduction spoken slowly and clearly, plus one equivalent replacement.",
            {
                "comprehension": "Recognizes that the audio introduces a particular person.",
                "outcome_performance": "Identifies the name and at least two stated personal details correctly.",
                "interaction_or_transfer": "Performs on an equivalent introduction with a different speaker and details.",
            },
            ["Confuses the person or changes an essential stated detail."],
            ["Misses one optional detail beyond the required set."],
            ["One replay of the complete audio; neutral instruction repetition."],
            "Use a new speaker and different personal details after a delay.",
        ),
        "scope": ["focused", "One short introduction and three essential details."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Audio speed and clarity must stay within the source conditions."],
    },
    {
        "candidate_id": "lesson_candidate.understand_spoken_contact_details",
        "outcome": outcome(
            "a short simple telephone exchange or recorded message",
            "identify a person's name and phone number",
            "the contact details needed to return or record the call",
            "without a transcript or visible number",
            "the name and number are recorded accurately enough to use",
            "In a fresh short phone context, the learner can identify and record a name and phone number without a transcript.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p14.005", "anchor", "The objective directly anchors identifying a caller's name and phone number."),
            evidence("gse.adult.2022.p15.011", "supporting", "A recorded-message variant supports the same phone-number purpose."),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["locate_information", "comprehend_information"],
        "normalization_rationale": "Live-message and recorded-message variants require the same bounded contact-detail performance.",
        "mastery": mastery(
            "A fresh short call or message containing one name and one phone number.",
            {
                "comprehension": "Recognizes which spoken items are the caller's contact details.",
                "outcome_performance": "Records the required name and phone number accurately.",
                "interaction_or_transfer": "Succeeds with a new voice and number pattern.",
            },
            ["The recorded number cannot be used because a digit is missing or changed."],
            ["Nonessential punctuation or spacing in the written number."],
            ["One replay of the complete audio; a neutral field label for name and phone."],
            "Use a different caller and number after a delay.",
        ),
        "scope": ["focused", "One name and one phone number in a short audio."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Number length and delivery must remain realistic but A1-bounded."],
    },
]
