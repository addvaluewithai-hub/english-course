"""Reviewed targets for message mediation and translation candidates."""

try:
    from scripts.lesson_message_decision_helpers import error_hypothesis
except ModuleNotFoundError:
    from lesson_message_decision_helpers import error_hypothesis


MESSAGE_MEDIATION_DECISIONS = {
    "lesson_candidate.relay_names_numbers_and_prices_from_slow_speech": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Names, numbers, prices, and very simple immediate-interest details",
                "identify and list every requested value in the changed oral source",
                ["cefr.cv2020.p095.relaying_specific_information_in_writing.01"],
            )],
            "phrases": [],
            "pronunciation": [(
                "Receptive discrimination of very slow, clear articulation with repetition",
                "recover the requested values without changing them in writing",
                ["cefr.cv2020.p095.relaying_specific_information_in_writing.01"],
            )],
        },
        "decision_note": (
            "Grammar and phrases are not assigned because the descriptor requires "
            "source-faithful listing of discrete values, not a productive construction "
            "or phrase pattern."
        ),
        "error": error_hypothesis(
            "The learner hears the requested values but swaps a name, number, or price between list entries.",
            "Language B preserves the item types but assigns at least one wrong value.",
            "the value-preserving written relay demand from changed slow speech",
        ),
    },
    "lesson_candidate.convey_simple_information_from_a_sign_or_notice": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Simple predictable words or signs carrying immediate-interest details",
                "identify the one or two practical details in the changed Language A item",
                [
                    "cefr.cv2020.p101.processing_text_in_speech_or_sign.01",
                    "cefr.cv2020.p092.overall_mediation.01",
                ],
            )],
            "phrases": [(
                "Short sign, notice, poster, or programme phrases",
                "convey the selected practical information in declared Language B",
                [
                    "cefr.cv2020.p101.processing_text_in_speech_or_sign.01",
                    "cefr.cv2020.p092.overall_mediation.01",
                ],
            )],
            "pronunciation": [(
                "Intelligible spoken delivery of the selected Language B details",
                "let the listener recover the same practical information",
                ["cefr.cv2020.p101.processing_text_in_speech_or_sign.01"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the evidence requires conveying "
            "predictable information but names no productive construction."
        ),
        "error": error_hypothesis(
            "The learner adds a plausible place, time, or action that is not present in the Language A item.",
            "The listener receives materially changed practical information.",
            "the source-faithful selected-detail transfer demand in the fresh item",
        ),
    },
    "lesson_candidate.give_a_rough_oral_translation_of_everyday_sign_words": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Simple everyday words or signs on common written items",
                "recover their usable practical meaning in the changed Language A item",
                ["cefr.cv2020.p104.translating_a_written_text_in_speech_or.01"],
            )],
            "phrases": [(
                "Simple everyday written phrases on signs, notices, posters, programmes, or leaflets",
                "give a rough Language B rendering without reversing the phrase meaning",
                ["cefr.cv2020.p104.translating_a_written_text_in_speech_or.01"],
            )],
            "pronunciation": [(
                "Intelligible oral delivery of the rough Language B rendering",
                "make the practical everyday meaning usable for the listener",
                ["cefr.cv2020.p104.translating_a_written_text_in_speech_or.01"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the descriptor names simple words, "
            "signs, and phrases rather than a required construction."
        ),
        "error": error_hypothesis(
            "The learner renders familiar words separately but loses a negative or prohibitive meaning carried by the whole phrase.",
            "The rough oral translation can prompt the opposite practical action.",
            "the whole-phrase meaning demand in the changed everyday written item",
        ),
    },
    "lesson_candidate.translate_simple_written_phrases_with_a_dictionary": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Dictionary-supported selection of simple everyday word or sign meanings",
                "choose a meaning that fits the changed familiar Language A context",
                [
                    "cefr.cv2020.p101.processing_text_in_writing.01",
                    "cefr.cv2020.p104.translating_a_written_text_in_writing.01",
                ],
            )],
            "phrases": [(
                "Dictionary-supported written rendering of simple familiar phrases",
                "convey the practical phrase meaning in declared Language B",
                [
                    "cefr.cv2020.p101.processing_text_in_writing.01",
                    "cefr.cv2020.p104.translating_a_written_text_in_writing.01",
                ],
            )],
            "pronunciation": [],
        },
        "decision_note": (
            "No grammar target is assigned because the evidence requires meaning "
            "selection and phrase rendering, not a named construction; pronunciation "
            "is not assigned to the written task."
        ),
        "error": error_hypothesis(
            "The learner selects the first dictionary meaning even though it does not fit the familiar phrase context.",
            "The written Language B rendering obscures or reverses the practical meaning.",
            "dictionary-supported contextual meaning selection",
            source_note=(
                "CEFR explicitly notes that the appropriate meaning may not always be selected."
            ),
        ),
    },
}
