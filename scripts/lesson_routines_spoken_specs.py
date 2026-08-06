"""Spoken production candidates for routines, time, and leisure."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["routines_time_leisure"],
    "reviewed_at": "2026-07-17T17:49:14+03:00",
}

SPOKEN_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.give_an_event_date_and_time",
        "outcome": outcome(
            "a simple scheduling or event-information prompt",
            "give the relevant date and time",
            "day and month, a clock time, and one familiar time phrase",
            "with a calendar cue but without complete sentences to copy",
            "a listener can record the intended date and time accurately",
            "In a fresh scheduling situation, the learner can give an event date and time accurately.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p22.003", "anchor", "The objective anchors telling time to within five minutes."),
            evidence("gse.adult.2022.p22.014", "supporting", "The objective adds day-and-month date formats."),
            evidence("gse.adult.2022.p22.016", "supporting", "Quarter-hour times are included in the required range."),
            evidence("gse.adult.2022.p22.019", "supporting", "The objective adds familiar lexicalised time phrases."),
            evidence("cefr.cv2020.p079.information_exchange.04", "supporting", "The descriptor independently supports lexicalised time indications in exchange."),
        ],
        "skill_codes": ["listening", "speaking"],
        "mode_codes": ["production", "interaction"],
        "function_codes": ["give_information", "exchange_information"],
        "normalization_rationale": "Date and time are inseparable information fields in one scheduling response.",
        "mastery": mastery(
            "A fresh scheduling prompt with a changed date, clock time, and event.",
            {
                "comprehension": "Identifies which event needs a date and time.",
                "outcome_performance": "States the intended day, month, clock time, and familiar time phrase accurately.",
                "interaction_or_transfer": "Responds to the actual prompt and transfers across clock and lexicalised forms.",
                "control_or_repair": "Repairs one signalled date or time ambiguity without a model.",
            },
            ["The listener records a materially different date or time."],
            ["Minor form errors that do not make the schedule ambiguous."],
            ["A blank calendar cue and neutral request repetition."],
            "Use a different event, date, and time after a delay.",
        ),
        "scope": ["standard", "One event response with a date, clock time, and familiar time phrase."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Variant design must avoid locale-dependent numeric-date ambiguity."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.give_a_simple_leisure_profile",
        "outcome": outcome(
            "a basic profile prompt about a safe fictional person",
            "describe leisure preferences and abilities",
            "one like or dislike and one activity the person can or cannot do",
            "with picture or activity cues but without a complete model",
            "a listener can identify both the preference and ability",
            "In a fresh profile, the learner can describe a person's leisure preference and ability.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p23.006", "anchor", "The objective anchors can-or-cannot statements about basic activities."),
            evidence("gse.adult.2022.p23.015", "supporting", "The objective adds a simple like-or-dislike description."),
        ],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["describe", "express_ability", "express_preference"],
        "normalization_rationale": "A preference and a related ability are two bounded fields in one leisure profile.",
        "mastery": mastery(
            "A fresh fictional-person card with changed activities, preference, and ability.",
            {
                "comprehension": "Matches each cue to preference or ability meaning.",
                "outcome_performance": "States one clear preference and one clear can-or-cannot fact.",
                "interaction_or_transfer": "Describes a different person and activity set.",
                "control_or_repair": "Positive and negative meanings stay clear and one mix-up can be repaired.",
            },
            ["A like/dislike or can/cannot meaning is reversed or omitted."],
            ["Minor form errors when both facts remain intelligible."],
            ["Picture or activity cues and fictional information."],
            "Use a new person, activities, preference, and ability after a delay.",
        ),
        "scope": ["focused", "Two linked statements about one person's leisure profile."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Activities must remain familiar and safe for adult A1 learners."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.describe_a_simple_everyday_routine",
        "outcome": outcome(
            "a prepared prompt about a typical day",
            "describe a simple everyday routine",
            "three familiar activities in an understandable sequence",
            "with keyword or picture planning cues but without sentences to copy",
            "a listener can follow the main routine and order",
            "In a fresh prepared prompt, the learner can describe a simple everyday routine.",
        ),
        "evidence": [evidence(
            "cefr.cv2020.p063.sustained_monologue_describing_experience.02", "anchor",
            "The descriptor directly anchors a prepared series of simple sentences about everyday life.",
        )],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["describe"],
        "normalization_rationale": "Three sequenced daily activities form one prepared monologic performance.",
        "mastery": mastery(
            "A fresh typical-day prompt requiring three changed familiar activities.",
            {
                "comprehension": "Understands the requested day or routine context.",
                "outcome_performance": "Describes three relevant activities in an understandable sequence.",
                "interaction_or_transfer": "Adapts the description to a different day or fictional routine.",
                "control_or_repair": "Key time or sequence meaning remains clear and one signalled mix-up can be repaired.",
            },
            ["Fewer than three relevant activities are given or their order is unusable."],
            ["Pauses or minor grammar errors that preserve the routine."],
            ["Keyword or picture planning cues and brief preparation time."],
            "Use a different day and activity sequence after a delay.",
        ),
        "scope": ["standard", "Three simple routine sentences prepared in advance."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Preparation support must not become a complete script."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.describe_common_weather",
        "outcome": outcome(
            "a familiar weather image or simple situation",
            "describe the weather",
            "one or two common current conditions",
            "with visual context but without a spoken model",
            "a listener can identify the intended conditions",
            "In a fresh familiar situation, the learner can describe one or two common weather conditions.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p23.018", "anchor",
            "The objective directly anchors basic words for common weather conditions.",
        )],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["describe"],
        "normalization_rationale": "A brief current-weather description is independently assessable from routines and scheduling.",
        "mastery": mastery(
            "A fresh weather image or situation with one or two changed common conditions.",
            {
                "comprehension": "Recognizes which visible conditions need description.",
                "outcome_performance": "Names the intended common conditions intelligibly.",
                "interaction_or_transfer": "Transfers to a different image or familiar context.",
                "control_or_repair": "Repairs one signalled condition-word mix-up.",
            },
            ["The stated condition contradicts the prompt or is unintelligible."],
            ["A minor form error that preserves the weather meaning."],
            ["A clear weather image and neutral instruction repetition."],
            "Use different common conditions and context after a delay.",
        ),
        "scope": ["focused", "One or two familiar weather conditions."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Later vocabulary review must define the small common-weather range."],
    },
]
