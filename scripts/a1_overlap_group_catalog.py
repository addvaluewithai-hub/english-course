"""Reviewed overlap hypotheses to protect coverage during final candidate decisions."""

GROUPS = (
    ("personal_introductions", ("give_short_self_introduction", "introduce_another_person", "deliver_a_rehearsed_formal_introduction"), "Self, other-person, and rehearsed formal introductions share core identity language but differ in audience and support."),
    ("personal_profile_writing", ("write_short_personal_profile", "write_simple_people_profile_cards"), "Both write short factual people profiles with largely shared form and lexis."),
    ("generic_spoken_detail_location", ("understand_spoken_contact_details", "locate_names_places_and_times_in_slow_recordings", "identify_spoken_time_and_date_details", "identify_key_details_in_a_slow_station_announcement", "identify_a_price_in_slow_spoken_service_information"), "The same detail-segmentation and number-listening resources recur across distinct real-life contexts."),
    ("people_and_family_output", ("introduce_another_person", "describe_a_family_or_known_person", "write_simple_people_profile_cards"), "All express basic facts about another person across spoken and written channels."),
    ("routine_preference_cycle", ("understand_talk_about_leisure_preferences_and_abilities", "give_a_simple_leisure_profile", "exchange_routine_and_preference_information", "write_a_short_hobbies_and_likes_post"), "Reception, production, interaction, and online writing share preference and ability language."),
    ("routine_output_channels", ("describe_a_simple_everyday_routine", "write_simple_life_and_routine_sentences"), "The same routine outcome appears in spoken and written production."),
    ("schedule_time_cycle", ("understand_a_simple_meeting_arrangement", "identify_spoken_time_and_date_details", "give_an_event_date_and_time", "write_schedule_dates_and_times"), "Scheduling needs one multi-channel time/date progression rather than isolated ownership."),
    ("generic_referent_matching", ("match_visual_descriptions_to_familiar_things", "identify_familiar_referents_from_spoken_clues"), "Both are decontextualised matching strategies that need real-life task owners."),
    ("location_and_room_language", ("describe_people_and_object_locations_orally", "understand_where_things_or_people_are", "write_a_simple_room_description"), "The same basic position language spans reception and output."),
    ("object_description_channels", ("describe_a_familiar_object_orally", "write_a_simple_object_description"), "Visible-feature description is duplicated across spoken and written channels."),
    ("service_reception_and_purchase", ("identify_a_price_in_slow_spoken_service_information", "follow_a_slow_everyday_service_exchange", "handle_basic_price_and_quantity_information"), "Price and service reception should feed the integrated purchase outcome."),
    ("requests_and_immediate_needs", ("ask_for_basic_food_or_drink", "state_a_basic_food_or_drink_preference", "ask_for_and_give_an_everyday_item", "exchange_information_about_an_immediate_need", "ask_for_basic_practical_help"), "Several micro-requests share one immediate-needs interaction repertoire."),
    ("forms_and_online_transactions", ("complete_a_simple_information_form", "complete_a_very_simple_online_purchase_or_application"), "Both require accurate entry under labels; the online task adds a transaction choice."),
    ("visual_media_topic_recognition", ("identify_a_headline_news_topic_from_visual_media", "identify_a_product_in_a_short_video_advertisement"), "Both assess visual-supported topic or referent recognition in short video."),
    ("correspondence_input_output", ("write_a_short_message_to_a_friend", "understand_a_short_simple_postcard_message", "react_politely_to_a_simple_online_post"), "Short correspondence provides linked reception and response variants across paper and online contexts."),
    ("sign_comprehension_and_mediation", ("understand_common_signs_notices_and_visual_instructions", "convey_simple_information_from_a_sign_or_notice", "give_a_rough_oral_translation_of_everyday_sign_words", "translate_simple_written_phrases_with_a_dictionary"), "Sign comprehension, relay, and translation share source text but require explicit language direction and control."),
    ("fixed_social_responses", ("agree_to_a_simple_request", "accept_a_simple_offer", "respond_politely_to_an_introduction", "use_basic_everyday_polite_forms"), "These are important fixed moves best recycled inside fuller social and transaction outcomes."),
    ("collaboration_facilitation", ("show_basic_sympathy_during_a_problem_or_disagreement", "invite_input_and_check_understanding_in_a_simple_task", "show_interest_and_welcome_an_idea", "share_an_idea_and_ask_what_others_think"), "Four adjacent mediation candidates can form one coherent simple collaboration progression."),
    ("predictable_detail_mediation", ("relay_predictable_person_time_or_place_details", "relay_names_numbers_and_prices_from_slow_speech"), "Both relay already-learned predictable details and are natural synthesis evidence."),
)


def expand_id(short_id: str) -> str:
    return f"lesson_candidate.{short_id}"
