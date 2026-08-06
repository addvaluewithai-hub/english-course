"""Reception candidates for signs, visual media, and postcards."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE
    from scripts.lesson_message_spec_helpers import evidence, message_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE
    from lesson_message_spec_helpers import evidence, message_spec


RECEPTION_SPECS = [
    message_spec(
        candidate_id="lesson_candidate.understand_common_signs_notices_and_visual_instructions",
        situation="a common everyday place with a short sign, notice, or instruction and a visual cue",
        action="select its practical meaning or required action",
        content="familiar words or signs and one very basic instruction",
        success="the selected meaning or action matches the notice",
        statement="Given a fresh visually supported everyday sign, notice, or instruction, the learner can select its practical meaning or required action.",
        evidence_items=[
            evidence("gse.adult.2022.p09.005", "anchor", "The objective directly anchors understanding short notices, signs, and instructions with visual support."),
            evidence("cefr.cv2020.p056.reading_for_orientation.01", "supporting", "The descriptor supports recognising familiar words, signs, and basic phrases on everyday notices."),
        ],
        skill_codes=["reading"], mode_codes=["reception"],
        function_codes=["follow_instructions", "locate_information"],
        rationale="Recognition and acting on one short visually supported notice serve one everyday orientation purpose.",
        fresh_task="A changed set of common signs or notices with different visual cues and one required selection each.",
        level_2={
            "comprehension": "Recognises the familiar wording and visual cue that carry the practical meaning.",
            "outcome_performance": "Selects the correct meaning or required action for each fresh item.",
        },
        critical_failure="Selects a meaning or action that contradicts the notice.",
        permitted_support=["The visual support printed with the fresh notice."],
        delayed_probe="Use different everyday signs or notices and changed visual cues after a delay.",
        scope_rationale="Two or three short visually supported items with one practical decision each.",
        risks=["Use widely recognisable fictional or public signs; do not assume one country's symbol system."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
    message_spec(
        candidate_id="lesson_candidate.identify_a_headline_news_topic_from_visual_media",
        situation="a short simple headline-news summary with strong visual information",
        action="identify its familiar topic",
        content="recognisable words or signs, phrases, and the accompanying visuals",
        success="the chosen topic matches the summary",
        statement="From a fresh short headline-news summary with strong visual support, the learner can identify its familiar topic.",
        evidence_items=[evidence(
            "cefr.cv2020.p053.watching_tv_film_and_video.01", "anchor",
            "Covers the headline-news topic clause; advertised products are assigned to a separate fresh-task judgment.", "partial",
        )],
        skill_codes=["listening", "viewing"], mode_codes=["reception"],
        function_codes=["locate_information"],
        rationale="Headline-topic recognition is independently assessable from recognising advertised products.",
        fresh_task="A different short headline summary with changed familiar topic and visuals.",
        level_2={
            "comprehension": "Uses familiar wording and visual information to distinguish the topic.",
            "outcome_performance": "Selects or states the correct familiar topic.",
        },
        critical_failure="Chooses a topic contradicted by the headline summary and visuals.",
        permitted_support=["The source-provided visuals and one replay of the short summary."],
        delayed_probe="Use a new familiar headline topic and different visuals after a delay.",
        scope_rationale="One short summary and one topic decision.",
        risks=["Use fictional low-stakes summaries; avoid distressing or fast-changing news content."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
    message_spec(
        candidate_id="lesson_candidate.identify_a_product_in_a_short_video_advertisement",
        situation="a short simple video advertisement with clear product visuals and familiar wording",
        action="identify the advertised familiar product",
        content="recognisable words or signs, phrases, and the product image",
        success="the selected product matches the advertisement",
        statement="From a fresh short video advertisement, the learner can identify the advertised familiar product.",
        evidence_items=[evidence(
            "cefr.cv2020.p053.watching_tv_film_and_video.01", "anchor",
            "Covers the advertised-products clause; headline-news topic recognition has a separate partial claim.", "partial",
        )],
        skill_codes=["listening", "viewing"], mode_codes=["reception"],
        function_codes=["locate_information"],
        rationale="Product recognition has a distinct practical judgment from identifying a news topic.",
        fresh_task="A changed short video advertisement for a different familiar product.",
        level_2={
            "comprehension": "Uses the familiar wording and visual evidence to distinguish the product.",
            "outcome_performance": "Selects or names the product shown by the fresh advertisement.",
        },
        critical_failure="Identifies a product not supported by the advertisement.",
        permitted_support=["The clip's own audio-visual information and one replay."],
        delayed_probe="Use a different familiar product and short video advertisement after a delay.",
        scope_rationale="One short video advertisement and one product decision.",
        risks=["Use fictional brands and avoid persuasive claims, prices, or purchasing pressure."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
    message_spec(
        candidate_id="lesson_candidate.understand_a_short_simple_postcard_message",
        situation="a short simple postcard from a familiar person",
        action="identify its main message and one key detail",
        content="the postcard's overall everyday purpose and one explicit supporting detail",
        success="both the main message and detail match the postcard",
        statement="From a fresh short simple postcard, the learner can identify its main message and one key detail.",
        evidence_items=[evidence(
            "cefr.cv2020.p055.reading_correspondence.01", "anchor",
            "The descriptor directly anchors understanding short simple postcard messages.",
        )],
        skill_codes=["reading"], mode_codes=["reception"],
        function_codes=["comprehend_information"],
        rationale="Understanding an incoming postcard is independently assessable from composing one.",
        fresh_task="A new fictional sender, everyday purpose, and changed key detail.",
        level_2={
            "comprehension": "Identifies the postcard's overall everyday message and how the key detail supports it.",
            "outcome_performance": "Selects or states the correct main message and one key detail without a supplied interpretation.",
        },
        critical_failure="Misidentifies the main message or selects a detail contradicted by the postcard.",
        permitted_support=["A dictionary for isolated unfamiliar words if it does not reveal the answer."],
        delayed_probe="Use a different short postcard, purpose, and key detail after a delay.",
        scope_rationale="One very short postcard, its main message, and one key detail.",
        risks=["Use fictional senders, destinations, and contact details."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
]
