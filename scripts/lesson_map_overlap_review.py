"""Reviewed candidate-overlap dispositions for the LESSON-002 global audit."""

OVERLAP_DECISIONS = (
    (
        "resolved_merge",
        "identify_spoken_referents",
        (
            "lesson_candidate.identify_objects_from_slow_spoken_clues",
            "lesson_candidate.identify_familiar_referents_from_spoken_descriptions",
        ),
        "Merged as identify_familiar_referents_from_spoken_clues because one visual listening task and judgment cover every referent type.",
    ),
    (
        "resolved_merge",
        "complete_registration_forms",
        (
            "lesson_candidate.complete_personal_details_form",
            "lesson_candidate.complete_a_simple_travel_information_form",
        ),
        "Merged as complete_a_simple_information_form; the shared CEFR descriptor now has one full claim spanning its personal and travel-registration fields.",
    ),
    (
        "resolved_merge",
        "locate_spoken_names_places_times",
        (
            "lesson_candidate.locate_people_names_in_dialogue",
            "lesson_candidate.locate_place_and_time_in_slow_recordings",
        ),
        "Merged as locate_names_places_and_times_in_slow_recordings; the split GSE name/place objective now has one full claim.",
    ),
    (
        "resolved_merge",
        "describe_locations_orally",
        (
            "lesson_candidate.say_where_people_are",
            "lesson_candidate.describe_an_objects_position_orally",
        ),
        "Merged as describe_people_and_object_locations_orally because the same oral position task and mastery judgment apply.",
    ),
    (
        "resolved_merge",
        "relay_predictable_details",
        (
            "lesson_candidate.relay_personal_details_in_english",
            "lesson_candidate.relay_a_family_or_role_fact",
            "lesson_candidate.relay_a_time_or_place_detail",
        ),
        "Merged as relay_predictable_person_time_or_place_details because only the predictable detail type changes within one relay performance.",
    ),
    (
        "retain_distinct",
        "object_description_channels",
        (
            "lesson_candidate.describe_a_familiar_object_orally",
            "lesson_candidate.write_a_simple_object_description",
        ),
        "Speaking and writing require different fresh performances and mastery judgments.",
    ),
    (
        "retain_distinct",
        "request_and_offer_responses",
        (
            "lesson_candidate.agree_to_a_simple_request",
            "lesson_candidate.accept_a_simple_offer",
        ),
        "The pragmatic prompts differ and one response can be mastered while the other still fails.",
    ),
    (
        "retain_distinct",
        "spontaneous_and_rehearsed_introductions",
        (
            "lesson_candidate.introduce_another_person",
            "lesson_candidate.deliver_a_rehearsed_formal_introduction",
        ),
        "Interpersonal introduction and prepared audience delivery have different support conditions.",
    ),
    (
        "retain_distinct",
        "visual_media_purposes",
        (
            "lesson_candidate.identify_a_headline_news_topic_from_visual_media",
            "lesson_candidate.identify_a_product_in_a_short_video_advertisement",
        ),
        "News-topic recognition and advertisement-product recognition are separable purposes.",
    ),
    (
        "retain_distinct",
        "translation_channels",
        (
            "lesson_candidate.give_a_rough_oral_translation_of_everyday_sign_words",
            "lesson_candidate.translate_simple_written_phrases_with_a_dictionary",
        ),
        "Oral rough translation and dictionary-assisted written translation require different output evidence.",
    ),
)

MASTERY_ALIGNMENT_DECISIONS = (
    {
        "candidate_id": "lesson_candidate.follow_a_slow_everyday_service_exchange",
        "decision": "reception_only",
        "rationale": "The fresh task assesses understanding an exchange, so listening/reception tags now match the performance and interaction repair is not applicable.",
    },
    {
        "candidate_id": "lesson_candidate.leave_a_simple_whereabouts_and_return_message",
        "decision": "repair_required",
        "rationale": "The written-interaction task now requires rereading and correcting a materially wrong whereabouts or return-time detail.",
    },
)
