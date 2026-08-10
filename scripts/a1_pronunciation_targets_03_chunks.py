"""A1 pronunciation targets: prominence, connected forms, intonation, and repair."""

from scripts.a1_pronunciation_target_helpers import target


GUIDED = "receptive_with_guided_imitation"
BOTH = "receptive_and_productive"


TARGETS = (
    target("key_information_prominence", "prominence_rhythm", "Hear and highlight the key detail", GUIDED,
        "Notice and imitate prominence on the name, number, price, time, destination, item, or need that carries the contrast.",
        (("My NAME is Mona.", "/maɪ ˈneɪm ɪz ˈmoʊnə/"), ("It's FIFteen.", "/ɪts ˌfɪfˈtiːn/"), ("I need a TICKet.", "/aɪ niːd ə ˈtɪkɪt/")),
        "Equal prominence can hide which detail is new or corrected.",
        "exchange_personal_details_orally", ("exchange_routine_and_preference_information", "identify_familiar_referents_from_spoken_clues", "understand_where_things_or_people_are", "exchange_basic_wayfinding_information", "understand_outline_of_a_simple_guided_tour", "identify_key_details_in_a_slow_station_announcement", "identify_a_price_in_slow_spoken_service_information", "follow_a_slow_everyday_service_exchange", "state_a_basic_food_or_drink_preference", "exchange_information_about_an_immediate_need", "identify_a_headline_news_topic_from_visual_media", "identify_a_product_in_a_short_video_advertisement"),
        "After one model, highlight the changed detail in a fresh short contrast so the listener identifies it.",
        ("arabic_pronunciation.equal_prominence",),
        "Natural English rhythm, reductions, and native-like timing are not A1 mastery demands."),
    target("frequent_contractions", "connected_speech", "Recognise frequent contractions in clear chunks", GUIDED,
        "Recognise and optionally use the taught contracted forms without requiring fast or heavily reduced speech.",
        (("I'm", "/aɪm/"), ("you're", "/jʊr/"), ("he's", "/hiːz/"), ("it's", "/ɪts/"), ("what's", "/wʌts/"), ("don't", "/doʊnt/"), ("can't", "/kænt/"), ("I'd", "/aɪd/"), ("I'll", "/aɪl/")),
        "Failure to recognise a contraction can hide identity, negation, a question, a request, or a future commitment.",
        "understand_spoken_personal_introductions", ("understand_talk_about_leisure_preferences_and_abilities", "check_in_at_a_hotel", "open_and_close_a_basic_social_exchange"),
        "Identify the full meaning of a fresh clear contracted chunk and produce either the contracted or full intelligible form.", (),
        "Assimilation, elision, and fast casual reduction beyond the registered chunks wait."),
    target("question_social_contours", "intonation_stance", "Recognisable social and question contours", GUIDED,
        "Use or imitate a recognisable contour for a greeting, wh-question, yes/no check, and polite response while accepting variety.",
        (("How are you?", "/haʊ ɑr juː/"), ("Where is the station?", "/wɛr ɪz ðə ˈsteɪʃən/"), ("Is that right?", "/ɪz ðæt raɪt/"), ("Thank you.", "/ˈθæŋk juː/")),
        "A flat or mismatched contour can make a check sound like a statement or obscure turn completion.",
        "exchange_personal_details_orally", ("exchange_basic_wayfinding_information", "ask_for_basic_food_or_drink", "agree_to_a_simple_request", "accept_a_simple_offer", "open_and_close_a_basic_social_exchange", "respond_politely_to_an_introduction", "show_basic_sympathy_during_a_problem_or_disagreement", "invite_input_and_check_understanding_in_a_simple_task", "show_interest_and_welcome_an_idea", "share_an_idea_and_ask_what_others_think"),
        "A partner identifies the fresh utterance as greeting, question/check, or response without an answer-revealing script.", (),
        "No single universal rise/fall pattern or emotion-reading claim is imposed."),
    target("sense_group_chunking", "chunking_monitoring_repair", "Deliver short sense groups with safe pauses", BOTH,
        "Group a short learnt message into meaning units and pause between units rather than inside a key name, number, or phrase.",
        (("My name is Mona | I'm from Cairo.", "/maɪ ˈneɪm ɪz ˈmoʊnə | aɪm frəm ˈkaɪroʊ/"), ("One ticket to Giza | please.", "/wʌn ˈtɪkɪt tə ˈɡiːzə | pliːz/")),
        "An unsafe pause can split a name, number, destination, or request and change what the listener records.",
        "give_short_self_introduction", ("describe_people_and_object_locations_orally", "describe_a_family_or_known_person", "describe_a_simple_everyday_routine", "describe_a_familiar_object_orally", "buy_a_basic_public_transport_ticket", "check_in_at_a_hotel", "ask_for_basic_food_or_drink", "deliver_a_rehearsed_formal_introduction"),
        "Deliver a fresh two- or three-unit message with intelligible key details and pauses at meaning boundaries.", (),
        "Long-turn fluency and spontaneous discourse chunking wait."),
    target("pronunciation_repair", "chunking_monitoring_repair", "Repeat, slow, or spell a key item to repair", BOTH,
        "Notice a listener signal and repair the key item through slower repetition, contrast, or spelling.",
        (("Sorry—FIFteen.", "/ˈsɑri | ˌfɪfˈtiːn/"), ("Mona—M-O-N-A.", "/ˈmoʊnə/"), ("Please say that again.", "/pliːz seɪ ðæt əˈɡɛn/")),
        "Without repair, a correctable name, number, item, or place remains misunderstood.",
        "exchange_personal_details_orally", ("relay_predictable_person_time_or_place_details", "follow_simple_game_or_activity_instructions", "follow_simple_directions_from_an_interlocutor", "ask_for_and_give_an_everyday_item", "ask_for_basic_practical_help", "describe_a_simple_problem_to_a_health_professional", "convey_simple_information_from_a_sign_or_notice", "give_a_rough_oral_translation_of_everyday_sign_words"),
        "After a fresh misunderstanding signal, repair only the key detail until the partner selects it correctly.", (),
        "Repair success matters more than producing the reference model on the first attempt."),
)
