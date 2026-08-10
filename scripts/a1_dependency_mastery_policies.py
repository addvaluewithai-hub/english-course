"""Reviewed safeguards and construct-revision actions for A1 reconciliation."""

REVISION_ACTIONS = {
    "ambiguous_language_direction": "Declare the input and output language pair for mastery.",
    "assessment_channel_ambiguous": "Choose one mastery response channel and treat the other as transfer.",
    "channel_or_mode_mismatch": "Assess only the declared construct or add the genuinely required skill and mode.",
    "compound_scope": "Choose one bounded mastery family or split the candidate before authoring.",
    "label_outcome_mismatch": "Rename and narrow the task to the observable A1 comprehension claim.",
    "prepared_text_support_contradiction": "Allow learner-prepared notes, not a supplied complete answer model.",
}

EXIT_ANCHORS = {
    "listening_reception": (
        "understand_spoken_personal_introductions",
        "understand_spoken_contact_details",
        "understand_talk_about_leisure_preferences_and_abilities",
        "follow_slow_spoken_route_directions",
        "identify_key_details_in_a_slow_station_announcement",
    ),
    "reading_reception": (
        "locate_written_personal_details",
        "understand_a_simple_meeting_arrangement",
        "understand_common_signs_notices_and_visual_instructions",
        "find_key_details_in_a_simple_advertisement_or_leaflet",
    ),
    "speaking_production": (
        "give_short_self_introduction",
        "describe_a_family_or_known_person",
        "describe_a_simple_everyday_routine",
        "handle_basic_price_and_quantity_information",
    ),
    "writing_production": (
        "complete_a_simple_information_form",
        "write_short_personal_profile",
        "write_simple_life_and_routine_sentences",
        "write_a_simple_room_description",
    ),
    "oral_interaction": (
        "exchange_personal_details_orally",
        "exchange_routine_and_preference_information",
        "exchange_basic_wayfinding_information",
        "check_in_at_a_hotel",
        "ask_for_basic_food_or_drink",
        "ask_for_basic_practical_help",
    ),
    "written_online_interaction": (
        "exchange_personal_details_in_writing",
        "write_a_short_message_to_a_friend",
        "complete_a_very_simple_online_purchase_or_application",
        "react_politely_to_a_simple_online_post",
    ),
    "mediation": (
        "relay_predictable_person_time_or_place_details",
        "convey_simple_information_from_a_sign_or_notice",
        "invite_input_and_check_understanding_in_a_simple_task",
        "show_interest_and_welcome_an_idea",
    ),
}


def candidate_id(short_id: str) -> str:
    return f"lesson_candidate.{short_id}"
