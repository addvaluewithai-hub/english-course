from scripts.pilot10_specs.coverage_helpers import evidence as e


COVERAGE = {
    "U1-L08": {
        "grammar.be_negative": e("introduce", "I'm not a doctor.", ["false_fact_repair", "guided_profile_plan"], "Correct one false present fact in the fresh profile."),
        "grammar.present_simple_affirmative": e("introduce", "I live, she lives", ["subject_verb", "guided_profile_plan"], "State fresh facts about self and another person."),
        "grammar.have_possession": e("introduce", "I have, he has, she has", ["subject_verb", "guided_profile_plan"], "Express a fresh family or pet fact with have/has."),
        "grammar.noun_number_quantity": e("introduce", "one child, two children", ["quantity_phrase", "guided_profile_plan"], "Match fresh quantity and noun number."),
        "grammar.basic_noun_phrase": e("introduce", "a friendly cat", ["quantity_phrase", "guided_profile_plan"], "Build a compact referent needed by the profile."),
        "grammar.coordination": e("introduce", "and, but, or", ["connector_meaning", "guided_profile_plan"], "Connect fresh facts without changing their relation."),
        "lexical.family_core": e("introduce", "mother, father, brother", ["quantity_phrase", "guided_profile_plan"], "Select only relationships needed by the fictional card."),
        "lexical.pets_animals": e("introduce", "dog, cat, bird", ["quantity_phrase", "guided_profile_plan"], "Name the relevant fresh pet or animal."),
        "lexical.extended_family_life": e("introduce", "parent, cousin, grandmother", ["guided_profile_plan"], "Use only a task-provided or voluntary relationship."),
        "lexical.family_profile_frames": e("introduce", "This is my", ["guided_profile_plan"], "Use the needed frame without copying a complete profile."),
        "grammar.basic_clause_order": e("fresh_recycle", "كل جملة لها فاعل واضح", ["false_fact_repair", "guided_profile_plan"], "Keep the subject and facts clear across the fresh profile."),
        "lexical.familiar_jobs": e("fresh_recycle", "teacher", ["guided_profile_plan"], "Use the changed fact-card job accurately."),
        "lexical.self_introduction_frames": e("fresh_recycle", "I'm Salma.", ["guided_profile_plan"], "Open the fresh profile without reciting the model."),
    },
    "U1-L09": {},
    "U2-L01": {
        "lexical.basic_people": e("introduce", "person, people, man, woman", ["people_word", "person_cards", "guided_map"], "Choose the people map and keep all people distinct."),
        "lexical.people_appearance_manner": e("introduce", "tall, short, young, old", ["evidence_only_description", "person_cards", "guided_map"], "Use only supplied descriptions to identify a fresh person."),
        "a1_pronunciation.f_v_contrast": e("introduce", "five, very, family, seven", ["sound_meaning", "guided_map"], "Repair only if a key person, family word, or number changes."),
        "a1_pronunciation.front_central_vowels": e("introduce", "man, men", ["people_word", "sound_meaning", "guided_map"], "Use context or repair to preserve the person/people distinction."),
        "lexical.family_core": e("fresh_recycle", "This is my mother.", ["person_cards", "guided_map"], "Map fresh core relationships to the right people."),
        "lexical.extended_family_life": e("fresh_recycle", "This is my cousin Layla.", ["person_cards", "guided_map"], "Map a supplied extended relationship without personal disclosure."),
    },
}
