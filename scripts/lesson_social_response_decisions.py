"""Reviewed targets for the final short social-response candidates."""

try:
    from scripts.lesson_social_decision_helpers import error_hypothesis
except ModuleNotFoundError:
    from lesson_social_decision_helpers import error_hypothesis


SOCIAL_RESPONSE_DECISIONS = {
    "lesson_candidate.agree_to_a_simple_request": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar words that signal a simple low-stakes request",
                "recognise the changed request before selecting an affirmative response",
                ["gse.adult.2022.p22.012"],
            )],
            "phrases": [(
                "Basic fixed expressions for agreeing to a simple request",
                "give a clear affirmative response rather than a refusal or uncertain reply",
                ["gse.adult.2022.p22.012"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the fixed agreement expression",
                "let the requester recognise the reply as agreement",
                ["gse.adult.2022.p22.012"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the objective specifies a few basic "
            "fixed expressions rather than a productive construction."
        ),
        "error": error_hypothesis(
            "The learner recognises the request but uses a fixed response that signals uncertainty or refusal.",
            "The requester cannot treat the response as agreement.",
            "the request-sensitive affirmative-response demand in the fresh turn",
        ),
    },
    "lesson_candidate.accept_a_simple_offer": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar words that signal a simple low-stakes offer",
                "recognise the changed offer before selecting an accepting response",
                ["gse.adult.2022.p23.001"],
            )],
            "phrases": [(
                "Basic fixed expressions for accepting a simple offer",
                "give a clear acceptance rather than a refusal or uncertain reply",
                ["gse.adult.2022.p23.001"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the fixed acceptance expression",
                "let the person making the offer recognise acceptance",
                ["gse.adult.2022.p23.001"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the objective specifies basic fixed "
            "expressions rather than a productive construction."
        ),
        "error": error_hypothesis(
            "The learner recognises the offer but uses a fixed response that signals uncertainty or refusal.",
            "The person making the offer cannot treat the response as acceptance.",
            "the offer-sensitive affirmative-response demand in the fresh turn",
        ),
    },
    "lesson_candidate.show_basic_sympathy_during_a_problem_or_disagreement": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Simple words that cue a problem or disagreement",
                "recognise the changed difficulty before choosing a sympathetic response",
                ["cefr.cv2020.p117.facilitating_communication_in_delicate_situations_and_disagreements.01"],
            )],
            "phrases": [(
                "Memorised simple expressions that indicate sympathy",
                "acknowledge the changed problem or disagreement without sounding dismissive",
                ["cefr.cv2020.p117.facilitating_communication_in_delicate_situations_and_disagreements.01"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the memorised sympathy expression",
                "let the other person recognise the response as supportive",
                ["cefr.cv2020.p117.facilitating_communication_in_delicate_situations_and_disagreements.01"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the descriptor names recognition and "
            "memorised simple expressions rather than a productive construction."
        ),
        "error": error_hypothesis(
            "The learner recognises the difficulty but selects a memorised expression that sounds dismissive or contradictory.",
            "The response fails to indicate sympathy in the changed exchange.",
            "the difficulty-sensitive sympathetic-response demand in the fresh exchange",
        ),
    },
}
