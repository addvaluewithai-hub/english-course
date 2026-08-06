"""Reviewed target and error decisions for foundational reading reception."""

READING_RECEPTION_DECISIONS = {
    "lesson_candidate.follow_short_written_everyday_instructions": {
        "targets": {
            "grammar": [("Verb-led positive instruction clauses", "recognise each required action and its order", ["gse.adult.2022.p09.008", "gse.adult.2022.p09.013"])],
            "vocabulary": [("Familiar task action verbs and concrete task nouns", "identify the actions and objects needed for the stated task", ["gse.adult.2022.p09.008", "gse.adult.2022.p09.013"])],
            "phrases": [("Two- or three-step short written instructions", "follow the complete bounded sequence rather than isolated words", ["gse.adult.2022.p09.008", "gse.adult.2022.p09.013"])],
            "pronunciation": [],
        },
        "decision_note": "No pronunciation target is assigned because the cited performance is written reception; audio support must not become mastery evidence.",
        "error": {
            "error": "The learner recognises the action words but reverses or skips a written step.",
            "impact": "The required straightforward task is not completed in the stated order.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the task's order contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.understand_common_signs_notices_and_visual_instructions": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Familiar names, sign words, and everyday place labels", "recognise the practical meaning in a common everyday situation", ["gse.adult.2022.p09.005", "cefr.cv2020.p056.reading_for_orientation.01"])],
            "phrases": [("Very basic notice and instruction phrases", "select the required action rather than merely recognise a symbol", ["gse.adult.2022.p09.005", "cefr.cv2020.p056.reading_for_orientation.01"])],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar or pronunciation target is assigned: the sources support visually aided recognition of familiar sign language, not oral production or a named grammar feature.",
        "error": {
            "error": "The learner chooses from the visual symbol alone and ignores a contrasting English sign word or phrase.",
            "impact": "The selected practical meaning or action can be wrong even when the place is familiar.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the visual-versus-text task contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.match_visual_descriptions_to_familiar_things": {
        "targets": {
            "grammar": [("Basic descriptive sentences linking a referent to a visible feature", "use the whole sentence to distinguish the pictured referent", ["gse.adult.2022.p09.002", "gse.adult.2022.p09.003"])],
            "vocabulary": [("Familiar object, person, and animal nouns with colour and size words", "match the source-supported visible features", ["gse.adult.2022.p09.002", "gse.adult.2022.p09.003"])],
            "phrases": [],
            "pronunciation": [],
        },
        "decision_note": "No phrases or pronunciation target is assigned because the cited task is sentence-level visual reading; a phrase list or audio contrast would add unsupported demands.",
        "error": {
            "error": "The learner matches on a familiar noun but misses the colour, size, or other distinguishing feature.",
            "impact": "Two familiar referents are confused and the description is not fully understood.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the source's visible-feature contrast; it is not a source fact and requires expert review and learner observation.",
        },
    },
    "lesson_candidate.locate_written_personal_details": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Common personal-detail labels such as name, age, nationality, and address", "locate the requested value in a short profile or form-like text", ["gse.adult.2022.p09.009"])],
            "phrases": [("Short personal-detail label-and-value combinations", "connect each requested field to the correct written detail", ["gse.adult.2022.p09.009"])],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar or pronunciation target is assigned because the source supports limited written detail extraction rather than a form-production pattern or spoken performance.",
        "error": {
            "error": "The learner copies a nearby personal value under the wrong requested label.",
            "impact": "The selected details no longer identify the person accurately.",
            "basis": "Candidate-specific hypothesis for Arabic-speaking A1 adults based on the label-to-value discrimination required by the fresh task; it is not a source fact and needs expert and learner validation.",
        },
    },
}
