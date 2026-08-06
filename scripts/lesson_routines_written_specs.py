"""Written candidates for the routines, time, and leisure partition."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["routines_time_leisure"],
    "reviewed_at": "2026-07-17T17:49:14+03:00",
}

WRITTEN_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.write_a_short_hobbies_and_likes_post",
        "outcome": outcome(
            "a simple personal message or online profile/post",
            "write about hobbies and likes or dislikes",
            "two or three very short factual sentences",
            "with dictionary or translation-tool access but without a completed model",
            "a reader can identify the activities and each stated preference",
            "In a fresh simple post, the learner can write two or three short sentences about hobbies and preferences.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.008", "anchor", "The objective directly anchors simple sentences about personal interests."),
            evidence("cefr.cv2020.p066.overall_written_production.01", "supporting", "Covers likes and dislikes; family and pets are already claimed in people work.", "partial"),
            evidence("cefr.cv2020.p083.correspondence.01", "supporting", "The descriptor adds a short correspondence or posting variant with dictionary support."),
            evidence("cefr.cv2020.p086.online_conversation_and_discussion.01", "supporting", "The descriptor adds the online-posting variant with translation-tool support."),
        ],
        "skill_codes": ["reading", "writing"],
        "mode_codes": ["production", "interaction", "online_interaction"],
        "function_codes": ["give_information", "correspond"],
        "normalization_rationale": "Message, profile, and online-post formats test the same brief hobbies-and-preferences product.",
        "mastery": mastery(
            "A fresh message, profile, or posting prompt with changed hobbies and preferences.",
            {
                "comprehension": "Identifies the required format and hobby or preference fields.",
                "outcome_performance": "Writes two or three intelligible sentences covering every required field.",
                "interaction_or_transfer": "Adapts the content to a new prompt and equivalent written format.",
                "control_or_repair": "Positive and negative preferences stay clear and one unclear item can be revised.",
            },
            ["A required hobby or preference is absent, reversed, or unintelligible."],
            ["Minor spelling or grammar errors that preserve every stated fact."],
            ["Dictionary or translation-tool support for individual words and formulaic expressions."],
            "Use a different format, hobbies, and preferences after a delay.",
            ["A complete generated post or sentence-level translation of the answer."],
        ),
        "scope": ["standard", "Two or three very short sentences in one personal written product."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["Tool support must be limited so the final text remains learner-produced."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.write_schedule_dates_and_times",
        "outcome": outcome(
            "a simple calendar, appointment, or event-entry task",
            "write the required dates and times",
            "one date and one time in digits and words",
            "with blank fields but without completed examples to copy",
            "a reader can record the intended schedule without ambiguity",
            "In a fresh schedule entry, the learner can write a date and time using digits and words.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.012", "anchor", "The objective anchors writing dates in digits and words."),
            evidence("gse.adult.2022.p37.018", "supporting", "The objective adds times in digits and words."),
        ],
        "skill_codes": ["writing"],
        "mode_codes": ["production"],
        "function_codes": ["give_information"],
        "normalization_rationale": "Date and time are linked fields in one usable schedule entry.",
        "mastery": mastery(
            "A fresh calendar or event entry with a changed date and time.",
            {
                "comprehension": "Matches the requested date and time to the correct fields.",
                "outcome_performance": "Writes both details in digits and words without changing their meaning.",
                "interaction_or_transfer": "Transfers the performance to a different simple schedule format.",
                "control_or_repair": "Spelling and notation remain unambiguous and one flagged detail can be corrected.",
            },
            ["A date or time is missing, materially wrong, or ambiguous."],
            ["Minor punctuation errors that do not alter the schedule."],
            ["Blank labelled fields and neutral instruction repetition."],
            "Use a different date, time, and schedule format after a delay.",
        ),
        "scope": ["focused", "One date and one time represented in digits and words."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["Use an explicitly labelled date convention to avoid locale ambiguity."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.write_simple_life_and_routine_sentences",
        "outcome": outcome(
            "a simple profile or typical-day writing prompt",
            "write about someone's life and routines",
            "three familiar facts or activities in clear short sentences",
            "with picture or keyword cues but without sentences to copy",
            "a reader can identify the person and main routine facts",
            "In a fresh simple prompt, the learner can write three short sentences about someone's life and routines.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p37.015", "anchor",
            "The objective directly anchors simple written sentences about someone's life and routines.",
        )],
        "skill_codes": ["writing"],
        "mode_codes": ["production"],
        "function_codes": ["give_information"],
        "normalization_rationale": "Three related life-and-routine facts form one small written profile product.",
        "mastery": mastery(
            "A fresh safe fictional-person or typical-day prompt with changed facts.",
            {
                "comprehension": "Identifies the person and required life or routine fields.",
                "outcome_performance": "Writes three intelligible sentences covering the required facts.",
                "interaction_or_transfer": "Adapts the writing to a different person or routine.",
                "control_or_repair": "Person and sequence meaning stay clear and one flagged sentence can be revised.",
            },
            ["The person is confused or fewer than three required facts are intelligible."],
            ["Minor spelling or grammar errors that preserve every fact."],
            ["Picture or keyword cues and fictional information."],
            "Use a new person and routine facts after a delay.",
        ),
        "scope": ["standard", "Three short sentences about one person's life or routine."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["Prompts should permit fictional answers and avoid sensitive routine disclosure."],
    },
]
