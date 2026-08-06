"""Mediation candidates for short signs, notices, posters, and programmes."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN
    from scripts.lesson_message_spec_helpers import evidence, message_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN
    from lesson_message_spec_helpers import evidence, message_spec


MEDIATION_SPECS = [
    message_spec(
        candidate_id="lesson_candidate.convey_simple_information_from_a_sign_or_notice",
        situation="a short very simple sign, notice, poster, or programme in declared Language A",
        action="convey its predictable information in declared Language B",
        content="one or two immediate-interest details",
        success="the listener receives the same practical details without a material change",
        statement="From a fresh very simple sign, notice, poster, or programme in Language A, the learner can convey one or two predictable details in Language B.",
        evidence_items=[
            evidence("cefr.cv2020.p101.processing_text_in_speech_or_sign.01", "anchor", "The descriptor directly anchors conveying predictable information from short signs, notices, posters, and programmes in Language B."),
            evidence(
                "cefr.cv2020.p092.overall_mediation.01", "supporting",
                "Covers the convey-simple-predictable-information clause; showing interest in an idea remains for social-contact reconciliation.", "partial",
            ),
        ],
        skill_codes=["reading", "speaking"], mode_codes=["mediation"],
        function_codes=["mediate_information"],
        rationale="Both claims support one source-to-listener transfer of immediate practical information.",
        fresh_task="A different source type with changed immediate-interest details and declared languages.",
        level_2={
            "comprehension": "Identifies the one or two practical details in the Language A source.",
            "outcome_performance": "Conveys those details in Language B without a material change.",
            "interaction_or_transfer": "Transfers details from a changed source rather than reciting a memorised explanation.",
        },
        critical_failure="Omits or materially changes a required practical detail.",
        permitted_support=["A bilingual dictionary for isolated words if the source details remain unmarked."],
        delayed_probe="Use another source type, changed details, and declared language pair after a delay.",
        scope_rationale="One short source and one or two predictable details.",
        risks=["Declare Language A and Language B; do not imply exact translation or collect real movement data."],
        basic_support_ids=BASIC_SPOKEN,
        clusters=["messages_signs_forms", "communication_strategies"],
    ),
    message_spec(
        candidate_id="lesson_candidate.give_a_rough_oral_translation_of_everyday_sign_words",
        situation="simple everyday words or phrases on a sign, notice, poster, programme, or leaflet in declared Language A",
        action="provide a simple rough oral translation in declared Language B",
        content="one or two familiar practical words or phrases",
        success="the listener receives their usable everyday meaning",
        statement="From fresh familiar words or phrases on an everyday written item in Language A, the learner can give a simple rough oral translation in Language B.",
        evidence_items=[evidence(
            "cefr.cv2020.p104.translating_a_written_text_in_speech_or.01", "anchor",
            "The descriptor directly anchors rough oral translation of everyday words and phrases encountered on common written items.",
        )],
        skill_codes=["reading", "speaking"], mode_codes=["mediation"],
        function_codes=["translate"],
        rationale="Rough oral translation is a distinct performance from relaying selected practical information.",
        fresh_task="Different familiar words or phrases, a changed written-item type, and a declared language pair.",
        level_2={
            "comprehension": "Recognises the familiar everyday words or phrases in Language A.",
            "outcome_performance": "Gives a usable rough oral translation in Language B without reversing the meaning.",
            "interaction_or_transfer": "Handles changed words or phrases rather than repeating the practice set.",
        },
        critical_failure="The rough translation reverses or obscures the practical everyday meaning.",
        permitted_support=["A bilingual dictionary for one isolated word if it does not supply the full response."],
        delayed_probe="Use different familiar words or phrases and a changed written item after a delay.",
        scope_rationale="One or two short familiar words or phrases and one oral response.",
        risks=["Declare both languages and label the result rough; do not claim professional translation accuracy."],
        basic_support_ids=BASIC_SPOKEN,
        clusters=["messages_signs_forms", "communication_strategies"],
    ),
]
