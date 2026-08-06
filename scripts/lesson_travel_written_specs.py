"""Written travel candidate specifications."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome


WRITTEN_SPECS = [{
    "candidate_cluster_ids": ["places_directions_travel"],
    "reviewed_at": "2026-07-17T19:51:11+03:00",
    "candidate_id": "lesson_candidate.complete_a_simple_travel_information_form",
    "outcome": outcome(
        "a fresh simple arrival or travel-information form",
        "complete the required travel fields",
        "a bounded set such as destination, arrival date, or transport detail",
        "with clear field labels and safe fictional data but without a completed model",
        "every required field contains usable matching information",
        "In a fresh simple travel form, the learner can enter the required travel information accurately.",
    ),
    "evidence": [
        evidence("gse.adult.2022.p37.011", "anchor", "The objective directly anchors completing a simple form requiring travel information."),
        evidence(
            "cefr.cv2020.p084.notes_messages_and_forms.01", "supporting",
            "Covers arrival-in-country and hotel-registration fields; the full personal-form claim retains its prior owner.", "partial",
        ),
    ],
    "skill_codes": ["reading", "writing"],
    "mode_codes": ["production"],
    "function_codes": ["complete_form"],
    "normalization_rationale": "Reading travel labels and entering matching details are one individual written-production task; the shared CEFR scale context does not make this candidate a live exchange.",
    "mastery": mastery(
        "A new travel form with changed layout, field order, and safe fictional details.",
        {
            "comprehension": "Matches each field label to the required travel detail.",
            "outcome_performance": "Completes every required field with usable consistent information.",
            "interaction_or_transfer": "Transfers the performance to a different simple travel-form layout.",
            "control_or_repair": "Dates, names, and numbers remain unambiguous and one flagged field can be corrected.",
        },
        ["A required field is blank, misplaced, or changes an essential travel detail."],
        ["A harmless capitalization or spacing variation."],
        ["Clear labels, safe fictional details, and neutral instruction repetition."],
        "Use a different form type, layout, and fictional journey after a delay.",
    ),
    "scope": ["standard", "One short form with four or five familiar travel fields."],
    "basic_support_ids": BASIC_WRITTEN,
    "risks": ["The form must not request real passport, booking, or immigration information."],
}]
