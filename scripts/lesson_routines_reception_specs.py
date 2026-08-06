"""Reception candidates for the routines, time, and leisure partition."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["routines_time_leisure"],
    "reviewed_at": "2026-07-17T17:49:14+03:00",
}

RECEPTION_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.understand_a_simple_meeting_arrangement",
        "outcome": outcome(
            "a fresh short message proposing a meeting",
            "identify the arrangement",
            "what to do plus when and where to meet",
            "without translation or highlighted answer cues",
            "all requested arrangement details are selected correctly",
            "In a fresh short message, the learner can identify what to do, when, and where to meet.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p09.010", "anchor", "The objective directly anchors when-and-where meeting details."),
            evidence("cefr.cv2020.p055.reading_correspondence.02", "supporting", "The descriptor adds the proposed-activity purpose and message context."),
        ],
        "skill_codes": ["reading"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "Activity, time, and place are inseparable fields in one meeting arrangement.",
        "mastery": mastery(
            "A new one- or two-sentence meeting proposal with changed activity, time, and place.",
            {
                "comprehension": "Recognizes that the message proposes a meeting.",
                "outcome_performance": "Identifies the activity, time, and place accurately.",
                "interaction_or_transfer": "Transfers to a different short-message format and arrangement.",
            },
            ["Any required activity, time, or place is missing or confused."],
            ["Minor uncertainty about an optional social phrase."],
            ["A simple layout and neutral instruction repetition."],
            "Use a different activity, time, place, and message format after a delay.",
        ),
        "scope": ["focused", "One short message with three linked arrangement fields."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Later place and message partitions must retain these full claims rather than duplicate them."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.understand_a_short_everyday_activity_text",
        "outcome": outcome(
            "a short simple phrase set or illustrated narrative about everyday activities",
            "identify the main activities and basic sequence",
            "two or three familiar actions",
            "without translation or answer highlighting",
            "the activities and any explicit order are identified correctly",
            "In a fresh short text, the learner can identify familiar everyday activities and their basic sequence.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p09.012", "anchor", "The objective anchors familiar everyday-activity phrases."),
            evidence("cefr.cv2020.p059.reading_as_a_leisure_activity.01", "supporting", "The descriptor adds a short illustrated narrative variant."),
        ],
        "skill_codes": ["reading"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "Phrase sets and illustrated narratives test the same bounded activity comprehension.",
        "mastery": mastery(
            "A fresh illustrated micro-narrative or phrase set with two or three familiar activities.",
            {
                "comprehension": "Recognizes the familiar activity language.",
                "outcome_performance": "Identifies each required activity and any explicit sequence.",
                "interaction_or_transfer": "Succeeds with changed actions and illustrations.",
            },
            ["A main activity is misunderstood or the explicit sequence is reversed."],
            ["An optional descriptive detail is missed."],
            ["Clear illustrations that support context without revealing the answer."],
            "Use different familiar activities and images after a delay.",
        ),
        "scope": ["focused", "Two or three familiar activities in a very short text."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Images must contextualize rather than make reading unnecessary."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.identify_spoken_time_and_date_details",
        "outcome": outcome(
            "a short slow announcement or exchange about a familiar event",
            "locate the essential schedule details",
            "a time to within five minutes and a date",
            "without a transcript or isolated answer cue",
            "every requested time and date is recorded accurately",
            "In fresh slow event information, the learner can identify the essential time and date details.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p14.003", "supporting", "Quarter-hour times are inside the required listening range."),
            evidence("gse.adult.2022.p14.004", "anchor", "The objective anchors time recognition to within five minutes."),
            evidence("gse.adult.2022.p14.015", "supporting", "The objective adds factual date recognition."),
            evidence("gse.adult.2022.p15.005", "supporting", "Covers event time; the place clause remains shared with place work.", "partial"),
            evidence("gse.adult.2022.p15.008", "supporting", "Covers times and dates; prices remain for service work.", "partial"),
            evidence("cefr.cv2020.p048.overall_oral_comprehension.02", "supporting", "Covers concrete time information; places remain shared with place work.", "partial"),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information", "locate_information"],
        "normalization_rationale": "Time and date are linked schedule fields located in one familiar-event listening task.",
        "mastery": mastery(
            "A fresh slow event announcement or exchange with changed date and time.",
            {
                "comprehension": "Recognizes which details are the event time and date.",
                "outcome_performance": "Records each requested time and date accurately.",
                "interaction_or_transfer": "Succeeds with a different voice, event, and schedule.",
            },
            ["A required time or date is missing or materially wrong."],
            ["A non-required place or price detail is missed."],
            ["Slow clear delivery and one replay of the complete input."],
            "Use a new event, speaker, date, and time after a delay.",
        ),
        "scope": ["standard", "One short input with two essential schedule details."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["Later place and service work must claim only their named clauses."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.understand_talk_about_leisure_preferences_and_abilities",
        "outcome": outcome(
            "a short slow conversation about familiar free-time activities",
            "identify preferences and abilities",
            "what one or two people like, dislike, can do, or cannot do",
            "without a transcript or translated model",
            "each preference or ability is attributed to the correct person",
            "In a fresh slow conversation, the learner can identify people's leisure preferences and abilities.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p14.009", "supporting", "The objective covers direct likes-and-dislikes questions."),
            evidence("gse.adult.2022.p14.014", "supporting", "The objective covers stated likes-and-dislikes information."),
            evidence("gse.adult.2022.p15.009", "anchor", "The objective anchors basic free-time information."),
            evidence("gse.adult.2022.p15.010", "supporting", "The objective adds free-time questions."),
            evidence("gse.adult.2022.p15.018", "supporting", "The objective adds slowly delivered can-or-cannot information."),
            evidence("cefr.cv2020.p049.understanding_conversation_between_other_people.01", "supporting", "Covers the hobbies clause; people/family is already claimed and school/surroundings remain open.", "partial"),
        ],
        "skill_codes": ["listening"],
        "mode_codes": ["reception"],
        "function_codes": ["comprehend_information"],
        "normalization_rationale": "Preferences, activities, and abilities form one bounded leisure-profile listening judgment.",
        "mastery": mastery(
            "A new slow conversation about one or two people's familiar leisure activities.",
            {
                "comprehension": "Distinguishes questions from statements and positive from negative meaning.",
                "outcome_performance": "Attributes every required preference and ability correctly.",
                "interaction_or_transfer": "Succeeds with different speakers, activities, and preferences.",
            },
            ["A like/dislike or can/cannot meaning is reversed or assigned to the wrong person."],
            ["An optional activity detail is missed."],
            ["Slow clear delivery and one complete replay."],
            "Use new speakers, activities, preferences, and abilities after a delay.",
        ),
        "scope": ["standard", "One short conversation and two or three profile facts."],
        "basic_support_ids": BASIC_RECEPTIVE,
        "risks": ["The input must avoid inferring preferences or abilities not explicitly stated."],
    },
]
