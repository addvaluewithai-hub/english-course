"""Spoken and written output candidates for identity information."""

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


OUTPUT_SPECS = [
    {
        "candidate_id": "lesson_candidate.give_short_self_introduction",
        "outcome": outcome(
            "a first meeting or short personal profile prompt",
            "give a short connected self-introduction",
            "name, origin, residence or role, and one family or interest detail",
            "with field cues but without a complete model",
            "a listener can identify the learner and the required details",
            "In a fresh first-meeting situation, the learner can give a short self-introduction with essential personal details without a complete model.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p22.009", "anchor", "The objective anchors key information in a basic self-introduction."),
            evidence("gse.adult.2022.p22.006", "supporting", "Residence and one family detail are bounded parts of the same introduction."),
            evidence("gse.adult.2022.p22.023", "supporting", "One hobby or interest is an optional required detail in the same task family."),
            evidence("gse.adult.2022.p22.027", "supporting", "A simple residence statement is elicited within the introduction."),
            evidence("cefr.cv2020.p063.sustained_monologue_describing_experience.01", "supporting", "The candidate covers self-description, role, and residence in one short performance."),
            evidence("cefr.cv2020.p142.propositional_precision.01", "supporting", "The candidate applies the descriptor's basic personal-detail precision."),
        ],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["introduce", "describe", "give_information"],
        "normalization_rationale": "The details are natural moves in one bounded self-introduction and can be judged in one fresh performance.",
        "mastery": mastery(
            "A first meeting, voice profile, or group introduction with changed field cues.",
            {
                "comprehension": "Understands which personal details the situation requires.",
                "outcome_performance": "Gives a coherent short introduction containing all required detail categories.",
                "interaction_or_transfer": "Adapts the introduction to a fresh situation or fictional safe identity.",
                "control_or_repair": "Essential details remain intelligible and one important breakdown can be repaired after a neutral signal.",
            },
            ["The listener cannot identify the speaker or two required details are absent."],
            ["Minor article, agreement, or hesitation errors that do not obscure meaning."],
            ["Short field cues; permission to use fictional personal information."],
            "Use a different first-meeting context and changed required details after a delay.",
        ),
        "scope": ["standard", "Four or five short connected statements serving one introduction."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Keep the required detail set small; examples in the sources are not a quota."],
    },
    {
        "candidate_id": "lesson_candidate.complete_personal_details_form",
        "outcome": outcome(
            "a simple unfamiliar registration or contact form",
            "complete the required personal-information fields",
            "a bounded set such as name, nationality, address, age, and one date",
            "with clear field labels but without a completed example",
            "the form contains usable details in the correct fields",
            "In a fresh simple form, the learner can enter required personal details accurately without a completed model.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.001", "anchor", "The objective directly anchors completing a simple personal-details form."),
            evidence("cefr.cv2020.p084.notes_messages_and_forms.01", "supporting", "The candidate uses the descriptor's bounded personal fields and registration context."),
        ],
        "skill_codes": ["reading", "writing"],
        "mode_codes": ["production"],
        "function_codes": ["complete_form"],
        "normalization_rationale": "Reading field labels and entering matching details are one individual written-production task; the CEFR scale context does not make this candidate a live exchange.",
        "mastery": mastery(
            "A fresh simple registration form with rearranged labels and safe fictional details permitted.",
            {
                "comprehension": "Matches each requested field to the correct type of personal detail.",
                "outcome_performance": "Completes all required fields with usable, internally consistent details.",
                "interaction_or_transfer": "Transfers the ability to a different simple form layout.",
                "control_or_repair": "Spelling and number/date forms preserve the essential details; one flagged field can be corrected.",
            },
            ["A required field is blank, in the wrong place, or changes the person's identity detail."],
            ["A harmless capitalization or spacing variation."],
            ["Clear field labels; fictional details; neutral explanation of the task purpose."],
            "Use a different form type and layout after a delay.",
        ),
        "scope": ["standard", "One simple form with five or six familiar fields."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["Field labels must be A1-readable and culturally neutral."],
    },
    {
        "candidate_id": "lesson_candidate.write_short_personal_profile",
        "outcome": outcome(
            "a short profile request for oneself or a safe fictional person",
            "write a few connected sentences introducing the person",
            "name, residence, role, and one family or interest detail",
            "with topic cues but without copying a complete model",
            "a reader can identify the person and all required details",
            "In a fresh profile context, the learner can write a few basic sentences introducing a person without copying a model.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.004", "anchor", "The objective anchors a prompted written self-introduction."),
            evidence("gse.adult.2022.p37.010", "supporting", "Family and residence statements fit the same short personal profile."),
            evidence(
                "cefr.cv2020.p067.creative_writing.01", "supporting",
                "Covers simple phrases and sentences about self, residence, and role; broader imaginary-person coverage remains for an adjacent partition.",
                "partial",
            ),
        ],
        "skill_codes": ["writing"],
        "mode_codes": ["production"],
        "function_codes": ["give_information", "describe"],
        "normalization_rationale": "The source statements form one bounded personal-profile purpose; the broader creative-writing clause is explicitly split.",
        "mastery": mastery(
            "A new profile card, introduction post, or short application paragraph with changed cues.",
            {
                "comprehension": "Understands the person and detail categories required by the prompt.",
                "outcome_performance": "Writes a few linked sentences containing every required personal detail.",
                "interaction_or_transfer": "Uses the ability for a fresh self or fictional profile.",
                "control_or_repair": "Sentence and spelling control keep each detail clear; one important issue can be revised after a neutral signal.",
            },
            ["The profile omits the person's identity or two required detail categories."],
            ["Minor punctuation or grammar errors that preserve every essential detail."],
            ["Topic cues; a safe fictional identity; neutral instruction repetition."],
            "Use a different profile purpose and changed detail set after a delay.",
        ),
        "scope": ["standard", "Three to five short sentences about one person."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["The unclaimed imaginary-person clause needs reconciliation in the people partition."],
    },
]
