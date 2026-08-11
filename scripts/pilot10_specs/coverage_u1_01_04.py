from scripts.pilot10_specs.coverage_helpers import evidence as e


COVERAGE = {
    "U1-L01": {
        "lexical.basic_feelings": e("introduce", "I'm tired.", ["fitting_reaction", "guided_exchange"], "Choose a fitting feeling or reaction in the fresh exchange."),
        "lexical.greeting_wellbeing_closing": e("introduce", "Hi. How are you?", ["exchange_shape", "choose_close", "guided_exchange"], "Complete all four social moves."),
        "a1_pronunciation.dental_fricatives": e("introduce", "thanks", ["fitting_reaction", "guided_exchange"], "Repair only if the selected social word loses meaning."),
        "a1_pronunciation.frequent_contractions": e("introduce", "I'm.", ["fitting_reaction", "guided_exchange"], "Recognise I'm and allow either contracted or full production."),
        "a1_pronunciation.question_social_contours": e("introduce", "How are you?", ["exchange_shape", "guided_exchange"], "The partner recognises the question and turn opening."),
    },
    "U1-L02": {
        "grammar.be_affirmative": e("introduce", "I'm Alex.", ["gist_before_detail", "referent_match", "guided_fresh_listen"], "Recover identity, role, and location from fresh be chunks."),
        "grammar.personal_pronouns": e("introduce", "I, he, she", ["referent_match", "guided_fresh_listen"], "Attribute each detail to the correct speaker or named person."),
        "lexical.identity_place_labels": e("introduce", "country", ["gist_before_detail", "guided_fresh_listen"], "Capture origin and location as the requested detail types."),
        "a1_pronunciation.frequent_contractions": e("fresh_recycle", "he's", ["contraction_meaning", "guided_fresh_listen"], "Recognise clear fresh I'm, he's, or she's chunks."),
    },
    "U1-L04": {
        "grammar.be_questions": e("introduce", "Are you a teacher?", ["short_answer_check", "guided_information_gap"], "Ask or answer a fresh identity or origin check."),
        "grammar.information_question_frames": e("introduce", "Where do you live?", ["question_to_field", "guided_information_gap"], "Retrieve the intended missing detail."),
        "lexical.familiar_jobs": e("introduce", "teacher, doctor, nurse", ["short_answer_check", "guided_information_gap"], "Use the fitting supplied or personally required job."),
        "lexical.personal_question_frames": e("introduce", "What's your name?", ["question_to_field", "guided_information_gap"], "Select four fitting questions for the new gap."),
        "lexical.contact_repair_frames": e("introduce", "Can you spell that?", ["repair_choice", "guided_information_gap"], "Use one repair if a key detail is unclear."),
        "a1_pronunciation.spelling_sound_verification": e("introduce", "M-O-N-A", ["repair_choice", "guided_information_gap"], "Spell or verify a fresh unclear name."),
        "a1_pronunciation.key_information_prominence": e("introduce", "My NAME is MONA.", ["guided_information_gap"], "Make the corrected detail prominent without shouting."),
        "a1_pronunciation.pronunciation_repair": e("introduce", "Please say that again.", ["repair_choice", "guided_information_gap"], "Repeat, slow, or spell a key item after a signal."),
        "a1_pronunciation.question_social_contours": e("fresh_recycle", "What's your name?", ["question_to_field", "guided_information_gap"], "A partner identifies the fresh utterance as a question."),
    },
}
