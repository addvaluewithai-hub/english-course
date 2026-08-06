"""Simple collaboration and facilitation candidates."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN
    from scripts.lesson_social_spec_helpers import evidence, social_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN
    from lesson_social_spec_helpers import evidence, social_spec


COLLABORATION_SPECS = [
    social_spec(
        candidate_id="lesson_candidate.invite_input_and_check_understanding_in_a_simple_task",
        situation="a very simple prepared pair or group task",
        action="invite another contribution, indicate understanding, and check whether others understand",
        content="one invitation and a brief two-way understanding check",
        success="another person can contribute and the group confirms shared understanding",
        statement="During a fresh very simple task, the learner can invite input, indicate understanding, and check whether others understand.",
        evidence_items=[
            evidence("cefr.cv2020.p111.facilitating_collaborative_interaction_with_peers.01", "anchor", "The descriptor anchors the prepared invitation and two-way understanding check."),
            evidence("cefr.cv2020.p115.facilitating_pluricultural_space.01", "supporting", "Covers inviting a contribution and indicating understanding; welcoming interest is assigned elsewhere.", "partial"),
        ],
        skill_codes=["listening", "speaking"], mode_codes=["mediation"],
        function_codes=["facilitate_interaction"],
        rationale="The three short moves serve one goal: enabling participation and shared understanding in one task.",
        fresh_task="A changed very simple task, fictional peers, and different contribution order.",
        level_2={
            "comprehension": "Tracks whether a peer has contributed and understood the task.",
            "outcome_performance": "Invites input, indicates own understanding, and checks the peer's understanding.",
            "interaction_or_transfer": "Uses the moves at fitting points in the changed task.",
            "control_or_repair": "Repeats or repairs one check when the peer signals uncertainty.",
        },
        critical_failure="A peer is not invited or an understanding problem is left unchecked.",
        permitted_support=["A task card with roles but no prepared social phrases."],
        delayed_probe="Use a different simple task and changed participation order after a delay.",
        scope_rationale="One brief collaborative task with three short facilitation moves.",
        risks=["Fictional peers and tasks must not encode one culture's participation norms."],
        basic_support_ids=BASIC_SPOKEN, scope_band="standard",
        clusters=["social_contact_collaboration", "communication_strategies"],
    ),
    social_spec(
        candidate_id="lesson_candidate.show_interest_and_welcome_an_idea",
        situation="a simple exchange where another person contributes one familiar idea",
        action="show interest and a welcoming attitude with simple words or signs and a non-verbal signal",
        content="one relevant interest expression and one congruent non-verbal signal",
        success="the contributor can recognise that the idea was received with interest",
        statement="In a fresh simple exchange, the learner can welcome another person's idea using simple language and a congruent non-verbal signal.",
        evidence_items=[
            evidence("cefr.cv2020.p092.overall_mediation.01", "supporting", "Covers the show-interest-in-an-idea clause; information conveyance is assigned elsewhere.", "partial"),
            evidence("cefr.cv2020.p113.encouraging_conceptual_talk.01", "anchor", "The descriptor anchors simple verbal or signed and non-verbal interest in an idea."),
            evidence("cefr.cv2020.p115.facilitating_pluricultural_space.01", "supporting", "Covers the welcoming-attitude and interest clause; invitation and understanding checks are assigned elsewhere.", "partial"),
        ],
        skill_codes=["listening", "non_verbal", "speaking"], mode_codes=["mediation"],
        function_codes=["facilitate_interaction"],
        rationale="Simple language and a congruent non-verbal signal jointly express one observable welcoming response.",
        fresh_task="A different familiar idea, fictional contributor, and culturally neutral interaction setting.",
        level_2={
            "comprehension": "Recognises the contributor's basic idea.",
            "outcome_performance": "Uses simple language and a congruent signal to show interest.",
            "interaction_or_transfer": "Responds to the changed idea rather than giving an unrelated fixed reaction.",
            "control_or_repair": "Repairs a mismatched verbal or non-verbal response after a neutral signal.",
        },
        critical_failure="The response is absent, unrelated, or communicates rejection instead of interest.",
        permitted_support=["A replay or repetition of the contributed idea."],
        delayed_probe="Use a different familiar idea and contributor after a delay.",
        scope_rationale="One idea and one brief verbal-or-signed plus non-verbal response.",
        risks=["Accept culturally varied non-verbal signals when their welcoming meaning is clear."],
        basic_support_ids=BASIC_SPOKEN,
        clusters=["social_contact_collaboration", "communication_strategies"],
    ),
    social_spec(
        candidate_id="lesson_candidate.share_an_idea_and_ask_what_others_think",
        situation="a very simple prepared pair or group choice",
        action="state one idea and ask what another person thinks",
        content="one prepared basic idea and one opinion-inviting question",
        success="the other person can identify the idea and is invited to respond",
        statement="In a fresh very simple prepared discussion, the learner can express one idea and ask what another person thinks.",
        evidence_items=[evidence(
            "cefr.cv2020.p111.collaborating_to_construct_meaning.01", "anchor",
            "The descriptor directly anchors expressing a prepared idea and asking what others think.",
        )],
        skill_codes=["listening", "speaking"], mode_codes=["mediation"],
        function_codes=["facilitate_interaction"],
        rationale="The idea and opinion question form one contribution that opens shared meaning-making.",
        fresh_task="A changed simple choice with preparation time and a different fictional peer.",
        level_2={
            "comprehension": "Understands the simple choice and what idea is requested.",
            "outcome_performance": "States one relevant idea and asks what the peer thinks.",
            "interaction_or_transfer": "Adapts the idea and question to the changed choice.",
            "control_or_repair": "Clarifies the idea once if the peer signals non-understanding.",
        },
        critical_failure="No relevant idea is expressed or the peer is not invited to respond.",
        permitted_support=["Brief preparation time and a topic card without a model answer."],
        delayed_probe="Use a different simple choice and peer after a delay.",
        scope_rationale="One prepared idea and one short opinion question.",
        risks=["Use low-stakes choices with no sensitive personal disclosure."],
        basic_support_ids=BASIC_SPOKEN,
        clusters=["social_contact_collaboration", "communication_strategies"],
    ),
]
