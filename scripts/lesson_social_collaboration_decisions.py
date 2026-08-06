"""Reviewed targets for the final collaboration and facilitation candidates."""

try:
    from scripts.lesson_social_decision_helpers import error_hypothesis
except ModuleNotFoundError:
    from lesson_social_decision_helpers import error_hypothesis


SOCIAL_COLLABORATION_DECISIONS = {
    "lesson_candidate.invite_input_and_check_understanding_in_a_simple_task": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Simple task, contribution, and understanding-status words or signs",
                "track who should contribute and whether the changed task is understood",
                ["cefr.cv2020.p111.facilitating_collaborative_interaction_with_peers.01"],
            )],
            "phrases": [(
                "Prepared short phrases for inviting input and checking understanding both ways",
                "enable contribution and confirm shared understanding in the changed task",
                [
                    "cefr.cv2020.p111.facilitating_collaborative_interaction_with_peers.01",
                    "cefr.cv2020.p115.facilitating_pluricultural_space.01",
                ],
            )],
            "pronunciation": [(
                "Intelligible delivery of the invitation and understanding checks",
                "let peers distinguish the invitation, own-understanding signal, and check",
                ["cefr.cv2020.p111.facilitating_collaborative_interaction_with_peers.01"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the evidence specifies short, simple "
            "phrases prepared in advance rather than independent construction control."
        ),
        "error": error_hypothesis(
            "The learner invites a contribution and indicates personal understanding but does not check whether the peer understands.",
            "Participation opens, but the task can continue without shared understanding.",
            "the three-move facilitation demand in the changed simple task",
        ),
    },
    "lesson_candidate.show_interest_and_welcome_an_idea": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Simple words or signs that show interest in a familiar idea",
                "respond to the changed idea with relevant welcoming meaning",
                [
                    "cefr.cv2020.p092.overall_mediation.01",
                    "cefr.cv2020.p113.encouraging_conceptual_talk.01",
                    "cefr.cv2020.p115.facilitating_pluricultural_space.01",
                ],
            )],
            "phrases": [(
                "A brief interest expression paired with a congruent non-verbal signal",
                "make the welcoming response recognisable to the contributor",
                [
                    "cefr.cv2020.p113.encouraging_conceptual_talk.01",
                    "cefr.cv2020.p115.facilitating_pluricultural_space.01",
                ],
            )],
            "pronunciation": [(
                "Intelligible delivery of the interest expression when speech is used",
                "keep the spoken response congruent with the welcoming non-verbal signal",
                ["cefr.cv2020.p113.encouraging_conceptual_talk.01"],
            )],
        },
        "decision_note": (
            "No grammar target is assigned because the descriptors require simple words "
            "or signs and non-verbal signals; pronunciation applies only when speech is "
            "the configured language channel."
        ),
        "error": error_hypothesis(
            "The learner uses an interest word or sign while the accompanying non-verbal signal communicates rejection or disengagement.",
            "The contributor cannot reliably recognise a welcoming response.",
            "the congruent verbal-or-signed and non-verbal interest demand in the fresh exchange",
        ),
    },
    "lesson_candidate.share_an_idea_and_ask_what_others_think": {
        "targets": {
            "grammar": [(
                "A very simple prepared idea statement and opinion-inviting question frame",
                "express the changed idea and open a response turn without a complete model",
                ["cefr.cv2020.p111.collaborating_to_construct_meaning.01"],
            )],
            "vocabulary": [(
                "Very simple words or signs for one prepared idea",
                "make the contribution relevant to the changed low-stakes choice",
                ["cefr.cv2020.p111.collaborating_to_construct_meaning.01"],
            )],
            "phrases": [(
                "A short phrase for asking what another person thinks",
                "invite the peer to respond to the prepared idea",
                ["cefr.cv2020.p111.collaborating_to_construct_meaning.01"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the idea and opinion question when speech is used",
                "let the peer identify the idea and the invitation to respond",
                ["cefr.cv2020.p111.collaborating_to_construct_meaning.01"],
            )],
        },
        "decision_note": (
            "All four target families stay within the descriptor's prepared idea and "
            "opinion-question demand; pronunciation applies only when speech is used."
        ),
        "error": error_hypothesis(
            "The learner states a relevant prepared idea but ends without asking what the peer thinks.",
            "The contribution does not open the reciprocal response required by the task.",
            "the idea-plus-opinion-invitation demand in the fresh prepared discussion",
        ),
    },
}
