"""Crosswalk every existing broad candidate grammar target to exact items."""

from scripts.a1_grammar_egp_assignments_01 import g


P = "lesson_candidate."


CROSSWALK = {
    P + "understand_spoken_personal_introductions": g("be_affirmative", "personal_pronouns"),
    P + "give_short_self_introduction": g("be_affirmative", "present_simple_affirmative", "basic_clause_order", "possessive_forms"),
    P + "exchange_personal_details_orally": g("be_questions", "present_simple_questions", "information_question_frames"),
    P + "write_short_personal_profile": g("be_affirmative", "present_simple_affirmative", "possessive_forms", "coordination"),
    P + "exchange_personal_details_in_writing": g("be_questions", "present_simple_questions", "information_question_frames"),
    P + "describe_people_and_object_locations_orally": g("be_affirmative", "place_prepositions", "place_adverbs"),
    P + "introduce_another_person": g("be_affirmative", "present_simple_affirmative", "articles", "this_reference"),
    P + "exchange_information_about_family_and_friends": g("be_questions", "present_simple_questions", "have_possession", "information_question_frames"),
    P + "describe_a_family_or_known_person": g("be_affirmative", "have_possession", "possessive_forms", "adjective_patterns"),
    P + "write_simple_people_profile_cards": g("be_affirmative", "have_possession", "possessive_forms", "articles"),
    P + "write_a_short_message_to_a_friend": g("basic_clause_order", "present_simple_questions", "coordination"),
    P + "understand_talk_about_leisure_preferences_and_abilities": g("can_ability_possibility"),
    P + "give_a_simple_leisure_profile": g("present_simple_affirmative", "can_ability_possibility", "like_and_infinitive_patterns"),
    P + "exchange_routine_and_preference_information": g("present_simple_affirmative", "present_simple_questions", "frequency_adverbs"),
    P + "describe_a_simple_everyday_routine": g("present_simple_affirmative", "frequency_adverbs", "coordination"),
    P + "write_a_short_hobbies_and_likes_post": g("present_simple_affirmative", "present_simple_negative", "like_and_infinitive_patterns", "coordination"),
    P + "write_simple_life_and_routine_sentences": g("present_simple_affirmative", "personal_pronouns", "frequency_adverbs", "coordination"),
    P + "match_visual_descriptions_to_familiar_things": g("be_affirmative", "adjective_patterns", "basic_noun_phrase"),
    P + "understand_where_things_or_people_are": g("be_affirmative", "place_prepositions", "place_adverbs"),
    P + "describe_a_familiar_object_orally": g("be_affirmative", "adjective_patterns", "articles", "degree_adverbs"),
    P + "exchange_visible_object_information": g("be_questions", "adjective_patterns", "noun_number_quantity", "information_question_frames"),
    P + "exchange_basic_information_about_a_home": g("present_simple_questions", "have_possession", "there_is_are", "information_question_frames"),
    P + "write_a_simple_object_description": g("be_affirmative", "adjective_patterns", "basic_noun_phrase"),
    P + "write_a_simple_room_description": g("there_is_are", "place_prepositions", "basic_noun_phrase"),
    P + "exchange_basic_wayfinding_information": g("be_questions", "place_prepositions", "place_adverbs", "information_question_frames"),
    P + "exchange_information_about_an_immediate_need": g("be_questions", "present_simple_questions", "can_ability_possibility", "information_question_frames"),
    P + "describe_a_simple_problem_to_a_health_professional": g("be_affirmative", "present_simple_affirmative", "information_question_frames"),
    P + "leave_a_simple_whereabouts_and_return_message": g("be_affirmative", "will_commitments", "place_prepositions", "time_date_expressions"),
    P + "open_and_close_a_basic_social_exchange": g("be_questions", "information_question_frames"),
    P + "state_how_a_simple_work_made_them_feel": g("be_affirmative", "because_reasons", "past_simple_limited"),
    P + "share_an_idea_and_ask_what_others_think": g("present_simple_affirmative", "present_simple_questions", "information_question_frames"),
    P + "follow_short_written_everyday_instructions": g("imperatives"),
}
