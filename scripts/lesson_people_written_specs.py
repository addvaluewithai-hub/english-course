"""Written production and interaction candidates for people and relationships."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_WRITTEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["people_relationships"],
    "reviewed_at": "2026-07-17T16:48:13+03:00",
}

WRITTEN_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.write_simple_people_profile_cards",
        "outcome": outcome(
            "simple profile cards for family, friends, or safe fictional people",
            "write brief factual statements about the people",
            "two or three people, familiar job names, and one family, pet, or possession fact",
            "with field or picture cues but without completed sentences to copy",
            "a reader can distinguish each person and the required facts",
            "In fresh simple profile cards, the learner can write basic facts about people using familiar job names accurately.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.005", "anchor", "The objective anchors simple written sentences about what self and other people have."),
            evidence("gse.adult.2022.p37.014", "supporting", "Accurate familiar job names are a required profile-card field across changed variants."),
            evidence(
                "cefr.cv2020.p066.overall_written_production.01", "supporting",
                "Covers family and pet information; likes and dislikes remain for the routines partition.", "partial",
            ),
        ],
        "skill_codes": ["writing"],
        "mode_codes": ["production"],
        "function_codes": ["give_information", "reproduce_language"],
        "normalization_rationale": "Job spelling and simple family, pet, or possession facts are necessary fields in one small people-profile product.",
        "mastery": mastery(
            "A fresh set of two or three people cards with changed jobs and facts.",
            {
                "comprehension": "Matches each prompt field to the correct person and fact type.",
                "outcome_performance": "Writes usable statements for every person with accurate familiar job names and facts.",
                "interaction_or_transfer": "Transfers the performance to new people, jobs, and fact categories.",
                "control_or_repair": "Spelling and sentence control preserve identity and one flagged field can be revised.",
            },
            ["A person is confused, a required fact is absent, or a job spelling is unusable."],
            ["Minor punctuation or grammar errors that preserve every fact."],
            ["Field or picture cues and fictional people."],
            "Use different people, common jobs, and facts after a delay.",
        ),
        "scope": ["standard", "Two or three short profile cards with one sentence each."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["A later lexical review must define which common jobs form the A1 practice range."],
    },
    {
        **COMMON,
        "candidate_cluster_ids": ["people_relationships", "messages_signs_forms"],
        "candidate_id": "lesson_candidate.write_a_short_message_to_a_friend",
        "outcome": outcome(
            "a short note, email, post, postcard, or text-message context with a friend",
            "write a very simple message",
            "one clear piece of information or one direct question",
            "with a purpose cue but without a completed message model",
            "the friend can identify the information or respond to the question",
            "In a fresh friend-to-friend context, the learner can write a short simple message that gives information or asks a question.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p37.016", "anchor", "The objective anchors short simple notes, emails, and postings to friends."),
            evidence("cefr.cv2020.p083.correspondence.02", "supporting", "The descriptor adds a postcard as another short simple friend-message format."),
            evidence("cefr.cv2020.p083.correspondence.03", "supporting", "The descriptor supplies the bounded information-or-question purpose."),
        ],
        "skill_codes": ["reading", "writing"],
        "mode_codes": ["interaction"],
        "function_codes": ["correspond"],
        "normalization_rationale": "The formats are equivalent variants of one brief friend-message purpose.",
        "mastery": mastery(
            "A fresh note, post, email, postcard, or text prompt requiring one information move or question.",
            {
                "comprehension": "Identifies the friend, purpose, and whether information or a question is required.",
                "outcome_performance": "Writes a short message whose information or question is clear and usable.",
                "interaction_or_transfer": "Responds to the actual context and transfers to an equivalent message format.",
                "control_or_repair": "Spelling and sentence control preserve the message; one unclear item can be clarified.",
            },
            ["The reader cannot identify the information or question."],
            ["Minor punctuation or grammar errors that do not change the message."],
            ["A purpose cue, fictional information, and neutral instruction repetition."],
            "Use a different friend, purpose, and message format after a delay.",
        ),
        "scope": ["focused", "One very short message with one information move or question."],
        "basic_support_ids": BASIC_WRITTEN,
        "risks": ["Message format remains a task variant, not a reason to duplicate these full anchors."],
    },
]
