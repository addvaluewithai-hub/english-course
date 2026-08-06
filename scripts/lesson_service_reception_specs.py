"""Reception candidates for food, shopping, and services."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE
    from scripts.lesson_service_spec_helpers import evidence, service_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE
    from lesson_service_spec_helpers import evidence, service_spec


RECEPTION_SPECS = [
    service_spec(
        candidate_id="lesson_candidate.identify_a_price_in_slow_spoken_service_information",
        situation="a short slow shop dialogue or announcement",
        action="identify the stated price",
        content="the correct cost and item or service",
        success="the price is matched to the intended item or service",
        statement="In fresh slow service speech, the learner can identify how much one item or service costs.",
        evidence_items=[
            evidence("gse.adult.2022.p15.007", "anchor", "The objective directly anchors locating a price in a short slow dialogue."),
            evidence("gse.adult.2022.p15.008", "supporting", "Covers the prices clause; the existing routine candidate owns times and dates.", "partial"),
            evidence("cefr.cv2020.p051.understanding_announcements_and_instructions.03", "supporting", "Covers the shop-price example; the existing travel candidate owns station figures and times.", "partial"),
        ],
        skill_codes=["listening"], mode_codes=["reception"],
        function_codes=["comprehend_information", "locate_information"],
        rationale="Dialogue and announcement variants require the same bounded price-identification judgment.",
        fresh_task="A new short shop recording with a changed item, price, and distractor number.",
        level_2={
            "comprehension": "Distinguishes the price from another spoken number.",
            "outcome_performance": "Matches the correct price to the intended item or service.",
            "interaction_or_transfer": "Succeeds with a changed voice, item, and price.",
        },
        critical_failure="The price or associated item is wrong.",
        permitted_support=["One neutral replay at the same slow, clear speed."],
        delayed_probe="Use a different shop context, item, and price after a delay.",
        scope_rationale="One short recording and one price-to-item decision.",
        risks=["Recordings must distinguish currency and decimal conventions clearly."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
    service_spec(
        candidate_id="lesson_candidate.follow_a_slow_everyday_service_exchange",
        situation="a short slow exchange in a shop, cafe, or similar service setting",
        action="identify what the customer needs and the service response",
        content="the requested item or service and one explicit response detail",
        success="both sides of the exchange are understood accurately",
        statement="In a fresh slow everyday service exchange, the learner can understand the concrete need and response.",
        evidence_items=[
            evidence("gse.adult.2022.p15.019", "anchor", "The objective anchors following slow everyday shopping and eating-out transactions."),
            evidence("cefr.cv2020.p049.understanding_conversation_between_other_people.02", "supporting", "The shop customer-salesperson example supplies third-party dialogue evidence."),
            evidence("cefr.cv2020.p073.understanding_an_interlocutor.01", "supporting", "The descriptor supports clear slow expressions satisfying concrete needs."),
            evidence("cefr.cv2020.p074.conversation.01", "supporting", "The separately published conversation descriptor supports repeated concrete-need language."),
        ],
        skill_codes=["listening", "speaking"], mode_codes=["reception", "interaction"],
        function_codes=["comprehend_information", "transact"],
        rationale="Shop, cafe, and similar exchanges share one receptive judgment: understand a concrete need and response.",
        fresh_task="A new two-turn service exchange with a changed need, item, and response.",
        level_2={
            "comprehension": "Identifies the concrete need and the service response.",
            "outcome_performance": "Selects or states both essential exchange details accurately.",
            "interaction_or_transfer": "Succeeds in a different familiar service setting.",
        },
        critical_failure="The need or service response is misunderstood.",
        permitted_support=["Slow clear delivery and one repetition without paraphrasing the answer."],
        delayed_probe="Use different speakers, service setting, and concrete need after a delay.",
        scope_rationale="One short exchange with two essential meaning details.",
        risks=["Visible pictures must not reveal the dialogue meaning without listening."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
    service_spec(
        candidate_id="lesson_candidate.find_key_details_in_a_simple_advertisement_or_leaflet",
        situation="a simple advertisement, event leaflet, or service brochure",
        action="locate the requested practical details",
        content="two explicit details such as the offer, cost, date, place, or departure time",
        success="every requested detail is located and copied or selected accurately",
        statement="In a fresh simple advertisement or leaflet, the learner can find two important practical details.",
        evidence_items=[evidence(
            "cefr.cv2020.p056.reading_for_orientation.04", "anchor",
            "The descriptor directly anchors locating important offer, cost, date, place, or departure details.",
        )],
        skill_codes=["reading"], mode_codes=["reception"],
        function_codes=["locate_information"],
        rationale="These short public texts require the same explicit-information search despite different layouts.",
        fresh_task="A new simple public text with changed layout, offer, and practical details.",
        level_2={
            "comprehension": "Recognizes where the requested practical details appear.",
            "outcome_performance": "Reports both requested details without changing them.",
            "interaction_or_transfer": "Succeeds with a different text type and layout.",
        },
        critical_failure="A requested cost, date, place, time, or offer detail is missed or changed.",
        permitted_support=["A clear layout and neutral repetition of the search instruction."],
        delayed_probe="Use a different advertisement or leaflet and detail pair after a delay.",
        scope_rationale="One short text and two explicit practical details.",
        risks=["The layout must remain simple without highlighting the answers."],
        basic_support_ids=BASIC_RECEPTIVE,
        clusters=["food_shopping_services", "messages_signs_forms"],
    ),
]
