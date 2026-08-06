"""Reviewed pedagogical sequence bands for the A1 lesson map."""

SEQUENCE_BANDS = [
    {
        "band_id": "foundation_and_personal_exchange",
        "rationale": (
            "Begin with short supported reception, basic social language, and personal "
            "information tasks that provide reusable A1 task familiarity."
        ),
        "candidate_ids": [
            "lesson_candidate.follow_short_written_everyday_instructions",
            "lesson_candidate.understand_common_signs_notices_and_visual_instructions",
            "lesson_candidate.match_visual_descriptions_to_familiar_things",
            "lesson_candidate.identify_familiar_referents_from_spoken_clues",
            "lesson_candidate.locate_names_places_and_times_in_slow_recordings",
            "lesson_candidate.identify_spoken_time_and_date_details",
            "lesson_candidate.locate_written_personal_details",
            "lesson_candidate.understand_spoken_personal_introductions",
            "lesson_candidate.understand_spoken_contact_details",
            "lesson_candidate.use_basic_everyday_polite_forms",
            "lesson_candidate.open_and_close_a_basic_social_exchange",
            "lesson_candidate.give_short_self_introduction",
            "lesson_candidate.exchange_personal_details_orally",
            "lesson_candidate.complete_a_simple_information_form",
            "lesson_candidate.write_short_personal_profile",
            "lesson_candidate.exchange_personal_details_in_writing",
            "lesson_candidate.understand_a_short_simple_postcard_message",
            "lesson_candidate.write_a_short_message_to_a_friend",
            "lesson_candidate.respond_politely_to_an_introduction",
            "lesson_candidate.introduce_another_person",
        ],
    },
    {
        "band_id": "familiar_people_routines_and_home",
        "rationale": (
            "Extend the same bounded reception and production patterns across familiar "
            "people, routines, time, objects, and home contexts."
        ),
        "candidate_ids": [
            "lesson_candidate.understand_talk_about_people_and_family",
            "lesson_candidate.describe_a_family_or_known_person",
            "lesson_candidate.exchange_information_about_family_and_friends",
            "lesson_candidate.write_simple_people_profile_cards",
            "lesson_candidate.understand_a_short_everyday_activity_text",
            "lesson_candidate.understand_talk_about_leisure_preferences_and_abilities",
            "lesson_candidate.describe_a_simple_everyday_routine",
            "lesson_candidate.give_a_simple_leisure_profile",
            "lesson_candidate.exchange_routine_and_preference_information",
            "lesson_candidate.understand_a_simple_meeting_arrangement",
            "lesson_candidate.give_an_event_date_and_time",
            "lesson_candidate.write_schedule_dates_and_times",
            "lesson_candidate.write_simple_life_and_routine_sentences",
            "lesson_candidate.write_a_short_hobbies_and_likes_post",
            "lesson_candidate.describe_common_weather",
            "lesson_candidate.understand_where_things_or_people_are",
            "lesson_candidate.describe_people_and_object_locations_orally",
            "lesson_candidate.describe_a_familiar_object_orally",
            "lesson_candidate.exchange_visible_object_information",
            "lesson_candidate.exchange_basic_information_about_a_home",
            "lesson_candidate.write_a_simple_object_description",
            "lesson_candidate.write_a_simple_room_description",
            "lesson_candidate.understand_outline_of_an_illustrated_short_story",
            "lesson_candidate.deliver_a_rehearsed_formal_introduction",
            "lesson_candidate.state_how_a_simple_work_made_them_feel",
        ],
    },
    {
        "band_id": "navigation_services_and_practical_messages",
        "rationale": (
            "Apply established literal-detail and exchange patterns to directions, travel, "
            "services, immediate needs, and practical form or message tasks."
        ),
        "candidate_ids": [
            "lesson_candidate.follow_simple_written_wayfinding_directions",
            "lesson_candidate.follow_slow_spoken_route_directions",
            "lesson_candidate.follow_simple_directions_from_an_interlocutor",
            "lesson_candidate.exchange_basic_wayfinding_information",
            "lesson_candidate.understand_simple_place_and_hotel_information",
            "lesson_candidate.understand_outline_of_a_simple_guided_tour",
            "lesson_candidate.identify_key_details_in_a_slow_station_announcement",
            "lesson_candidate.buy_a_basic_public_transport_ticket",
            "lesson_candidate.check_in_at_a_hotel",
            "lesson_candidate.find_key_details_in_a_simple_advertisement_or_leaflet",
            "lesson_candidate.identify_a_price_in_slow_spoken_service_information",
            "lesson_candidate.follow_a_slow_everyday_service_exchange",
            "lesson_candidate.state_a_basic_food_or_drink_preference",
            "lesson_candidate.ask_for_basic_food_or_drink",
            "lesson_candidate.ask_for_and_give_an_everyday_item",
            "lesson_candidate.exchange_information_about_an_immediate_need",
            "lesson_candidate.ask_for_basic_practical_help",
            "lesson_candidate.handle_basic_price_and_quantity_information",
            "lesson_candidate.describe_a_simple_problem_to_a_health_professional",
            "lesson_candidate.complete_a_very_simple_online_purchase_or_application",
            "lesson_candidate.leave_a_simple_whereabouts_and_return_message",
        ],
    },
    {
        "band_id": "media_and_mediation",
        "rationale": (
            "Move to visually supported media and bounded mediation only after the map has "
            "offered the relevant literal-detail and everyday-context scaffolds."
        ),
        "candidate_ids": [
            "lesson_candidate.identify_a_headline_news_topic_from_visual_media",
            "lesson_candidate.identify_a_product_in_a_short_video_advertisement",
            "lesson_candidate.react_politely_to_a_simple_online_post",
            "lesson_candidate.relay_predictable_person_time_or_place_details",
            "lesson_candidate.relay_names_numbers_and_prices_from_slow_speech",
            "lesson_candidate.convey_simple_information_from_a_sign_or_notice",
            "lesson_candidate.give_a_rough_oral_translation_of_everyday_sign_words",
            "lesson_candidate.translate_simple_written_phrases_with_a_dictionary",
        ],
    },
    {
        "band_id": "bounded_social_collaboration",
        "rationale": (
            "Close with short interpersonal and collaborative moves that benefit from the "
            "earlier social, instruction-following, and repair experience."
        ),
        "candidate_ids": [
            "lesson_candidate.agree_to_a_simple_request",
            "lesson_candidate.accept_a_simple_offer",
            "lesson_candidate.follow_simple_game_or_activity_instructions",
            "lesson_candidate.show_basic_sympathy_during_a_problem_or_disagreement",
            "lesson_candidate.show_interest_and_welcome_an_idea",
            "lesson_candidate.invite_input_and_check_understanding_in_a_simple_task",
            "lesson_candidate.share_an_idea_and_ask_what_others_think",
        ],
    },
]


def reviewed_sequence() -> list[str]:
    """Flatten the reviewed bands without implying fixed unit boundaries."""
    return [
        candidate_id
        for band in SEQUENCE_BANDS
        for candidate_id in band["candidate_ids"]
    ]
