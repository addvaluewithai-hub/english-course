"""Written and online interaction candidates for the message partition."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_WRITTEN
    from scripts.lesson_message_spec_helpers import evidence, message_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_WRITTEN
    from lesson_message_spec_helpers import evidence, message_spec


INTERACTION_SPECS = [
    message_spec(
        candidate_id="lesson_candidate.react_politely_to_a_simple_online_post",
        situation="a simple online post or its safe embedded media followed by one short comment",
        action="post a short positive or negative reaction and answer the follow-up politely",
        content="a positive or negative reaction plus a standard expression of thanks or apology",
        success="both responses fit the post and follow-up comment",
        statement="In a fresh simple online exchange, the learner can post a short reaction and answer one follow-up with thanks or apology.",
        evidence_items=[evidence(
            "cefr.cv2020.p086.online_conversation_and_discussion.02", "anchor",
            "The descriptor anchors a short positive or negative reaction followed by a standard thanks-or-apology response.",
        )],
        skill_codes=["reading", "writing"], mode_codes=["online_interaction"],
        function_codes=["correspond", "socialize"],
        rationale="The reaction and one polite follow-up form one bounded online exchange and one interaction judgment.",
        fresh_task="A new low-stakes post or safe embedded-media card, changed reaction stance, and different follow-up comment.",
        level_2={
            "comprehension": "Understands the post, requested stance, and follow-up comment.",
            "outcome_performance": "Posts the requested short reaction and an appropriate thanks or apology.",
            "interaction_or_transfer": "Responds to the changed follow-up rather than repeating a fixed pair.",
            "control_or_repair": "Keeps formulaic wording clear enough to preserve the intended reaction and politeness.",
        },
        critical_failure="The reaction reverses the required stance or the follow-up response is inappropriate.",
        permitted_support=["Neutral interface cues and isolated-word lookup that do not supply a reaction, thanks, or apology."],
        delayed_probe="Use a different post, stance, and follow-up comment after a delay.",
        scope_rationale="One short reaction and one short polite follow-up response.",
        risks=["Use a closed fictional feed and inert media cards; collect no account, profile, live link, or personal data."],
        basic_support_ids=BASIC_WRITTEN,
        scope_band="standard",
    ),
]
