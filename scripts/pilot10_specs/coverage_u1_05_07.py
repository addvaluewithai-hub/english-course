from scripts.pilot10_specs.coverage_helpers import evidence as e


COVERAGE = {
    "U1-L05": {
        "lexical.numbers_zero_to_hundred": e("introduce", "forty-two, one hundred", ["teen_ty", "number_range", "phone_grouping", "guided_contact_capture"], "Preserve a fresh age and every phone digit."),
        "lexical.days_of_week": e("introduce", "Monday, Tuesday, Wednesday", ["day_match", "guided_contact_capture"], "Retrieve the correct day from a fresh contact message."),
        "a1_pronunciation.name_number_segmentation": e("introduce", "five five five | zero one", ["phone_grouping", "guided_contact_capture"], "Segment and preserve fresh digit groups."),
        "a1_pronunciation.high_vowel_contrasts": e("introduce", "three", ["number_range", "phone_grouping"], "Repair only when a key digit changes."),
        "a1_pronunciation.teen_ty_stress": e("introduce", "thirteen or thirty?", ["teen_ty", "guided_contact_capture"], "Distinguish the fresh age or request confirmation."),
        "a1_pronunciation.compound_chunk_stress": e("introduce", "phone number", ["guided_contact_capture"], "Recognise the field-introducing chunk in fresh audio."),
        "lexical.contact_repair_frames": e("fresh_recycle", "Can you spell that?", ["guided_contact_capture"], "Use one fitting check instead of guessing."),
        "a1_pronunciation.spelling_sound_verification": e("fresh_recycle", "K-H-A-L-I-L", ["guided_contact_capture"], "Verify a changed fictional name when needed."),
        "a1_pronunciation.dental_fricatives": e("fresh_recycle", "Thursday", ["day_match", "guided_contact_capture"], "Repair only if the number or day becomes unclear."),
    },
    "U1-L06": {
        "lexical.personal_detail_labels": e("introduce", "First name.", ["label_meaning", "field_value", "wrong_row_repair", "changed_layout"], "Retrieve each requested value from its correct fresh field."),
    },
    "U1-L07": {
        "lexical.months": e("introduce", "January, February, March", ["month_capture", "field_transfer"], "Retrieve and enter the fresh required month."),
        "lexical.digital_objects": e("introduce", "phone, computer, laptop", ["action_meaning", "field_transfer"], "Recognise the simulated digital task environment."),
        "lexical.form_digital_actions": e("introduce", "Submit the form.", ["action_meaning", "pre_submit_check"], "Execute enter/select/check/submit in the fresh simulation."),
        "lexical.form_fields": e("introduce", "Enter your first name.", ["field_transfer", "swapped_fields"], "Enter each changed value under the matching field."),
        "lexical.online_form_frames": e("introduce", "Check your details.", ["action_meaning", "pre_submit_check"], "Follow fresh prompts without real submission."),
        "lexical.personal_detail_labels": e("fresh_recycle", "last name", ["field_transfer", "swapped_fields"], "Supply and transfer changed fictional details."),
        "lexical.own_country_nationality": e("fresh_recycle", "Jordanian", ["field_transfer", "swapped_fields"], "Distinguish and enter a fresh country/nationality pair."),
        "lexical.personal_question_frames": e("fresh_recycle", "What's your email address?", ["field_transfer"], "Use the fitting question only when a simulated detail is missing."),
    },
}
