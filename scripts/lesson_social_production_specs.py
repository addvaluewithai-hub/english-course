"""Prepared spoken-production candidates for social contact."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN
    from scripts.lesson_social_spec_helpers import evidence, social_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN
    from lesson_social_spec_helpers import evidence, social_spec


PRODUCTION_SPECS = [
    social_spec(
        candidate_id="lesson_candidate.deliver_a_rehearsed_formal_introduction",
        situation="briefly addressing a small class, group, or audience",
        action="use a very short prepared text to introduce another person formally",
        content="the person's name, role, and one clear formal introduction line",
        success="the audience can identify the person and purpose of the statement",
        statement="Using a very short prepared text in a fresh audience setting, the learner can deliver a rehearsed formal introduction of another person.",
        evidence_items=[evidence(
            "cefr.cv2020.p066.addressing_audiences.01", "anchor",
            "The descriptor directly anchors a very short rehearsed statement, here realised through its formal-introduction example.",
        )],
        skill_codes=["speaking"], mode_codes=["production"],
        function_codes=["give_information", "introduce"],
        rationale="Addressing an audience from a prepared text is distinct from an unrehearsed interpersonal introduction.",
        fresh_task="A different fictional person, role, audience, and learner-prepared very short text.",
        level_2={
            "comprehension": "Understands whom the statement introduces and to which audience.",
            "outcome_performance": "Delivers the short prepared introduction so the person and role are clear.",
            "interaction_or_transfer": "Prepares and delivers an equivalent statement for a different person.",
            "control_or_repair": "Recovers from one hesitation without changing the introduced details.",
        },
        critical_failure="The audience cannot identify the introduced person or their role.",
        permitted_support=["A very short learner-prepared text, as the source explicitly permits."],
        delayed_probe="Prepare and deliver a short introduction for a different person after a delay.",
        scope_rationale="One very short prepared audience statement.",
        risks=["Keep formality simple and do not equate one culture's delivery style with success."],
        basic_support_ids=BASIC_SPOKEN,
    ),
]
