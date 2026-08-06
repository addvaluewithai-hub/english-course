"""Transaction candidates for food, shopping, and services."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, BASIC_WRITTEN
    from scripts.lesson_service_spec_helpers import evidence, service_spec
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, BASIC_WRITTEN
    from lesson_service_spec_helpers import evidence, service_spec


TRANSACTION_SPECS = [
    service_spec(
        candidate_id="lesson_candidate.handle_basic_price_and_quantity_information",
        situation="a simple staffed purchase with visible familiar items",
        action="exchange the required price and quantity information",
        content="the intended item, quantity, and cost",
        success="the intended quantity and cost are mutually understood",
        statement="In a fresh simple purchase, the learner can handle the intended quantity and cost.",
        evidence_items=[
            evidence("gse.adult.2022.p22.007", "supporting", "The objective supports giving basic price information."),
            evidence("gse.adult.2022.p22.029", "supporting", "The objective separately supports saying a cost with basic language."),
            evidence("cefr.cv2020.p078.obtaining_goods_and_services.03", "anchor", "The descriptor anchors handling numbers, quantities, cost, and time in a service transaction."),
            evidence("cefr.cv2020.p079.information_exchange.05", "supporting", "The descriptor supports limited expression of numbers, quantities, and cost."),
        ],
        skill_codes=["listening", "speaking"], mode_codes=["interaction", "production"],
        function_codes=["exchange_information", "give_information", "transact"],
        rationale="Item, quantity, and cost are interdependent fields in one bounded purchase judgment.",
        fresh_task="A new purchase role-play with changed item, quantity, price, and clerk turn.",
        level_2={
            "comprehension": "Understands the clerk's quantity or price question and confirmation.",
            "outcome_performance": "Communicates the intended item, quantity, and cost accurately.",
            "interaction_or_transfer": "Responds to changed figures in a fresh transaction.",
            "control_or_repair": "Repairs one signalled number, quantity, or price mismatch.",
        },
        critical_failure="The item, quantity, or cost is missing or materially wrong.",
        permitted_support=["Visible item cues and a price list without a completed dialogue."],
        delayed_probe="Use a different item, quantity, price, and clerk prompt after a delay.",
        scope_rationale="One purchase with one item, one quantity, and one cost.",
        risks=["Use one clearly stated currency and avoid ambiguous decimal formatting."],
        basic_support_ids=BASIC_SPOKEN,
    ),
    service_spec(
        candidate_id="lesson_candidate.describe_a_simple_problem_to_a_health_professional",
        situation="a low-stakes basic health-professional exchange",
        action="state the problem and answer one simple follow-up question",
        content="the affected area or simple symptom and a yes-or-no response",
        success="the professional understands the basic problem and answer",
        statement="In a fresh basic health exchange, the learner can state a simple problem and answer one question.",
        evidence_items=[evidence(
            "cefr.cv2020.p080.interviewing_and_being_interviewed.02", "anchor",
            "The descriptor directly anchors stating a problem and answering a simple health-professional question, with gesture support.",
        )],
        skill_codes=["listening", "non_verbal", "speaking"], mode_codes=["interaction"],
        function_codes=["exchange_information"],
        rationale="The problem statement and one follow-up answer form one bounded health interview performance.",
        fresh_task="A changed fictional low-stakes symptom card and one new professional question.",
        level_2={
            "comprehension": "Understands the professional's simple direct question.",
            "outcome_performance": "States the basic problem and gives the intended answer.",
            "interaction_or_transfer": "Responds to the fresh follow-up rather than reciting a monologue.",
            "control_or_repair": "Uses words, gesture, or body language to repair one unclear detail.",
        },
        critical_failure="The affected area, simple problem, or answer is materially misunderstood.",
        permitted_support=["A fictional symptom cue, clear slow speech, repetition, and natural gesture."],
        delayed_probe="Use a different fictional low-stakes problem and question after a delay.",
        scope_rationale="One basic problem statement and one simple follow-up answer.",
        risks=["This is language practice, not diagnosis; exclude emergencies, advice, and real medical data."],
        basic_support_ids=BASIC_SPOKEN,
    ),
    service_spec(
        candidate_id="lesson_candidate.complete_a_very_simple_online_purchase_or_application",
        situation="a safe simulated online purchase or application",
        action="complete the required basic fields and submit the intended request",
        content="fictional name and contact details plus one purchase or application choice",
        success="all required fields match the fictional task card",
        statement="In a fresh simulated form, the learner can complete a very simple online purchase or application.",
        evidence_items=[evidence(
            "cefr.cv2020.p087.goal_oriented_online_transactions_and_collaboration.01", "anchor",
            "The descriptor directly anchors a simple online purchase or application using basic personal fields.",
        )],
        skill_codes=["reading", "writing"], mode_codes=["online_interaction"],
        function_codes=["complete_form", "transact"],
        rationale="Basic fields and one selection form a single submit-ready online transaction.",
        fresh_task="A new simulated form with changed field order, fictional details, and selection.",
        level_2={
            "comprehension": "Matches each required field to the fictional task information.",
            "outcome_performance": "Enters every required field and intended selection accurately.",
            "interaction_or_transfer": "Transfers the information to a different simple form layout.",
            "control_or_repair": "Corrects one field highlighted only as inconsistent or incomplete.",
        },
        critical_failure="A required field or intended purchase/application choice is missing or wrong.",
        permitted_support=["A fictional profile card and ordinary form labels without prefilled answers."],
        delayed_probe="Use a different simulated form and fictional profile after a delay.",
        scope_rationale="One short form with basic personal fields and one selection.",
        risks=["Never request real contact, payment, identity, account, or purchase data."],
        basic_support_ids=BASIC_WRITTEN,
        clusters=["food_shopping_services", "messages_signs_forms"],
    ),
]
