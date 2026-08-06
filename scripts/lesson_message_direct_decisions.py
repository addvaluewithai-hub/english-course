"""Reviewed targets for direct message and visual-media candidates."""

try:
    from scripts.lesson_message_decision_helpers import error_hypothesis
except ModuleNotFoundError:
    from lesson_message_decision_helpers import error_hypothesis


MESSAGE_DIRECT_DECISIONS = {
    "lesson_candidate.leave_a_simple_whereabouts_and_return_message": {
        "targets": {
            "grammar": [(
                "Simple statements of whereabouts and return time",
                "write both required details for the changed fictional situation",
                ["cefr.cv2020.p084.notes_messages_and_forms.02"],
            )],
            "vocabulary": [(
                "Familiar place, activity, and clock-time words",
                "state the changed destination or activity and return time precisely",
                ["cefr.cv2020.p084.notes_messages_and_forms.02"],
            )],
            "phrases": [(
                "A short message pattern combining whereabouts and return information",
                "make the two practical details easy for the recipient to recover",
                ["cefr.cv2020.p084.notes_messages_and_forms.02"],
            )],
            "pronunciation": [],
        },
        "decision_note": (
            "Pronunciation is not assigned because the mastery task requires a written "
            "message; the other targets stay within the two source-required details."
        ),
        "error": error_hypothesis(
            "The message gives a destination or activity but omits or changes the return time.",
            "The recipient cannot know reliably when the writer will return.",
            "the two-detail written message demand in the fresh fictional situation",
        ),
    },
    "lesson_candidate.identify_a_headline_news_topic_from_visual_media": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar words or signs that identify a headline-news topic",
                "distinguish the changed familiar topic using wording and visuals",
                ["cefr.cv2020.p053.watching_tv_film_and_video.01"],
            )],
            "phrases": [(
                "Familiar phrases in a short headline-news summary",
                "link the summary wording to the correct familiar topic",
                ["cefr.cv2020.p053.watching_tv_film_and_video.01"],
            )],
            "pronunciation": [(
                "Receptive recognition of familiar spoken topic wording",
                "use the short audio-visual summary rather than visuals alone",
                ["cefr.cv2020.p053.watching_tv_film_and_video.01"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the descriptor requires recognition "
            "of familiar wording and topic, not control of a construction."
        ),
        "error": error_hypothesis(
            "The learner chooses a visually plausible topic that the familiar headline wording contradicts.",
            "The summary's actual familiar topic is misidentified.",
            "the combined wording-and-visual-evidence demand in the fresh summary",
        ),
    },
    "lesson_candidate.identify_a_product_in_a_short_video_advertisement": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar words or signs that identify an advertised product",
                "distinguish the changed familiar product from alternatives",
                ["cefr.cv2020.p053.watching_tv_film_and_video.01"],
            )],
            "phrases": [(
                "Familiar phrases in a short product advertisement",
                "connect the advertisement wording with the product shown",
                ["cefr.cv2020.p053.watching_tv_film_and_video.01"],
            )],
            "pronunciation": [(
                "Receptive recognition of familiar spoken product wording",
                "use the clip's audio-visual evidence to identify the product",
                ["cefr.cv2020.p053.watching_tv_film_and_video.01"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the descriptor requires product "
            "recognition from familiar wording and visual information."
        ),
        "error": error_hypothesis(
            "The learner names a prominent background object instead of the product supported by the familiar wording.",
            "The advertised product is materially misidentified.",
            "the combined wording-and-product-visual demand in the fresh fictional clip",
        ),
    },
    "lesson_candidate.react_politely_to_a_simple_online_post": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Simple positive and negative reaction words or signs",
                "express the required changed stance without reversing it",
                ["cefr.cv2020.p086.online_conversation_and_discussion.02"],
            )],
            "phrases": [(
                "Formulaic reactions and standard expressions of thanks and apology",
                "complete both turns of the changed polite online exchange",
                ["cefr.cv2020.p086.online_conversation_and_discussion.02"],
            )],
            "pronunciation": [],
        },
        "decision_note": (
            "No grammar target is assigned because the source specifies formulaic "
            "expressions and simple combinations; pronunciation is not assigned to the "
            "written online exchange."
        ),
        "error": error_hypothesis(
            "The learner posts the requested reaction but answers the follow-up with thanks when an apology is needed, or the reverse.",
            "The second turn does not fit the changed social context.",
            "the reaction-plus-contextual-follow-up demand in the closed fictional feed",
        ),
    },
}
