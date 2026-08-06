"""Reviewed targets for the remaining food and service candidates."""


def _error(error: str, impact: str, demand: str) -> dict[str, str]:
    return {
        "error": error,
        "impact": impact,
        "basis": (
            "Candidate-specific hypothesis for Arabic-speaking A1 adults based on "
            f"{demand}; it is not a source fact and requires expert review and "
            "learner observation."
        ),
    }


SERVICE_REMAINING_DECISIONS = {
    "lesson_candidate.ask_for_basic_practical_help": {
        "targets": {
            "grammar": [],
            "vocabulary": [],
            "phrases": [(
                "Basic fixed expressions for asking for practical help",
                "make a recognisable help request in the changed safe situation",
                ["gse.adult.2022.p23.007"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the fixed help expression",
                "let the listener recognise that practical help is being requested",
                ["gse.adult.2022.p23.007"],
            )],
        },
        "decision_note": (
            "No separate grammar or vocabulary target is assigned because the source "
            "specifies basic fixed expressions without naming a construction or "
            "lexical field."
        ),
        "error": _error(
            "The learner signals a problem but does not make a recognisable request for help.",
            "The listener may notice difficulty but cannot tell that help is requested.",
            "the fixed-expression help-request demand in the fresh safe obstacle",
        ),
    },
    "lesson_candidate.handle_basic_price_and_quantity_information": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Numbers and familiar quantity and cost words",
                "distinguish the changed item quantity from its price",
                [
                    "gse.adult.2022.p22.007",
                    "gse.adult.2022.p22.029",
                    "cefr.cv2020.p078.obtaining_goods_and_services.03",
                    "cefr.cv2020.p079.information_exchange.05",
                ],
            )],
            "phrases": [(
                "Basic expressions for giving and checking quantity and cost",
                "exchange both required figures in the fresh staffed purchase",
                [
                    "gse.adult.2022.p22.007",
                    "gse.adult.2022.p22.029",
                    "cefr.cv2020.p078.obtaining_goods_and_services.03",
                    "cefr.cv2020.p079.information_exchange.05",
                ],
            )],
            "pronunciation": [(
                "Intelligible contrast between the spoken quantity and cost figures",
                "prevent the clerk from confusing how many with how much",
                [
                    "gse.adult.2022.p22.007",
                    "gse.adult.2022.p22.029",
                    "cefr.cv2020.p078.obtaining_goods_and_services.03",
                    "cefr.cv2020.p079.information_exchange.05",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence names "
            "numbers, quantities, and cost but no productive construction."
        ),
        "error": _error(
            "The learner gives recognisable figures but swaps or changes the intended quantity and cost.",
            "The purchase would use the wrong number of items or the wrong price.",
            "the two-field quantity-and-cost demand in the changed purchase",
        ),
    },
    "lesson_candidate.describe_a_simple_problem_to_a_health_professional": {
        "targets": {
            "grammar": [(
                "Simple problem statements and brief answers to direct questions",
                "state the changed problem and answer the professional's follow-up",
                ["cefr.cv2020.p080.interviewing_and_being_interviewed.02"],
            )],
            "vocabulary": [(
                "Basic affected-area and simple-problem words",
                "identify the intended fictional problem without diagnostic detail",
                ["cefr.cv2020.p080.interviewing_and_being_interviewed.02"],
            )],
            "phrases": [(
                "Simple expressions for stating a problem and answering one follow-up",
                "complete both turns of the bounded health-professional exchange",
                ["cefr.cv2020.p080.interviewing_and_being_interviewed.02"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the affected area and brief answer",
                "let speech and permitted gesture reinforce the intended message",
                ["cefr.cv2020.p080.interviewing_and_being_interviewed.02"],
            )],
        },
        "decision_note": (
            "All four target families stay within the source's simple problem "
            "statement, direct answer, and gesture-supported message boundary."
        ),
        "error": _error(
            "The learner identifies the fictional problem but gives a yes-or-no answer that contradicts the follow-up prompt.",
            "The professional receives a materially wrong answer about the basic problem.",
            "the problem-plus-follow-up demand in the fresh low-stakes exchange",
        ),
    },
    "lesson_candidate.complete_a_very_simple_online_purchase_or_application": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Basic personal-information and simple form-field labels",
                "match each fictional name or contact detail to the changed form field",
                ["cefr.cv2020.p087.goal_oriented_online_transactions_and_collaboration.01"],
            )],
            "phrases": [],
            "pronunciation": [],
        },
        "decision_note": (
            "No separate grammar or phrases target is assigned because the descriptor "
            "requires basic personal-information entries rather than sentence "
            "production; pronunciation is not assigned to this written form task."
        ),
        "error": _error(
            "The learner copies a fictional personal detail into the wrong labelled field.",
            "The submitted purchase or application contains materially mismatched information.",
            "the field-to-detail matching demand in the fresh simulated form",
        ),
    },
}
