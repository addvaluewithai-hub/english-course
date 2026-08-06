"""Message and mediation candidates shared with service situations."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_WRITTEN
    from scripts.lesson_service_spec_helpers import evidence, service_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_WRITTEN
    from lesson_service_spec_helpers import evidence, service_spec


MESSAGE_SPECS = [
    service_spec(
        candidate_id="lesson_candidate.leave_a_simple_whereabouts_and_return_message",
        situation="a short note or message for a familiar person",
        action="state where the writer has gone and when they will return",
        content="a simple destination or activity and a return time",
        success="the reader knows both where the writer is and when they will return",
        statement="In a fresh simple note, the learner can say where they have gone and when they will return.",
        evidence_items=[evidence(
            "cefr.cv2020.p084.notes_messages_and_forms.02", "anchor",
            "The descriptor directly anchors a simple whereabouts and return-time message; shopping is one published example.",
        )],
        skill_codes=["reading", "writing"], mode_codes=["interaction"],
        function_codes=["correspond"],
        rationale="Whereabouts and return time jointly satisfy one practical message purpose.",
        fresh_task="A new recipient and changed fictional destination, activity, and return time.",
        level_2={
            "comprehension": "Understands which whereabouts and return details the recipient needs.",
            "outcome_performance": "Writes both the destination or activity and correct return time.",
            "interaction_or_transfer": "Adapts the message to a different recipient and situation.",
        },
        critical_failure="The whereabouts or return time is absent or materially wrong.",
        permitted_support=["A fictional situation card and a blank short-message format."],
        delayed_probe="Use a different recipient, destination, and return time after a delay.",
        scope_rationale="One very short message containing two essential details.",
        risks=["Use fictional whereabouts and times; never request real movement data."],
        basic_support_ids=BASIC_WRITTEN,
        clusters=["messages_signs_forms"],
    ),
    service_spec(
        candidate_id="lesson_candidate.relay_names_numbers_and_prices_from_slow_speech",
        situation="a very slow short oral service message in Language A",
        action="list the required details in Language B",
        content="two or three names, numbers, prices, or immediate-interest facts",
        success="every requested detail is transferred without changing its value",
        statement="From fresh very slow speech, the learner can list basic names, numbers, prices, or immediate facts in Language B.",
        evidence_items=[evidence(
            "cefr.cv2020.p095.relaying_specific_information_in_writing.01", "anchor",
            "The descriptor directly anchors written mediation of names, numbers, prices, and immediate information from slow oral text.",
        )],
        skill_codes=["listening", "writing"], mode_codes=["mediation"],
        function_codes=["mediate_information"],
        rationale="The listed details share one source-faithful transfer task without requiring added interpretation.",
        fresh_task="A new very slow oral message with changed details and order.",
        level_2={
            "comprehension": "Identifies each requested detail in the slow oral text.",
            "outcome_performance": "Lists every requested detail in Language B without value changes.",
            "interaction_or_transfer": "Transfers a changed detail set and order.",
        },
        critical_failure="A required name, number, price, or immediate fact is omitted or changed.",
        permitted_support=["Very slow clear articulation and repetition as allowed by the descriptor."],
        delayed_probe="Use a different short oral source and detail set after a delay.",
        scope_rationale="One short oral source and two or three copied meaning values.",
        risks=["Language A and Language B must be declared; do not imply translation equivalence beyond listed details."],
        basic_support_ids=BASIC_WRITTEN,
        clusters=["food_shopping_services", "communication_strategies"],
    ),
]
