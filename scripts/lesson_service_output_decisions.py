"""Reviewed targets for opening food and service output candidates."""


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


SERVICE_OUTPUT_DECISIONS = {
    "lesson_candidate.state_a_basic_food_or_drink_preference": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar food and drink option words",
                "identify the preferred item among changed familiar options",
                ["gse.adult.2022.p23.014"],
            )],
            "phrases": [(
                "Basic fixed expressions for stating a food or drink preference",
                "express one unambiguous choice without a complete response model",
                ["gse.adult.2022.p23.014"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the preference expression and chosen item",
                "let the listener distinguish the preferred option",
                ["gse.adult.2022.p23.014"],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the objective specifies "
            "basic fixed expressions rather than a productive construction."
        ),
        "error": _error(
            "The learner names a familiar option but does not mark it as the preferred choice.",
            "The listener cannot distinguish a preference from merely naming an item.",
            "the choice-plus-preference demand in the fresh option set",
        ),
    },
    "lesson_candidate.ask_for_basic_food_or_drink": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar food, drink, and basic option words",
                "specify the intended item and required option in the changed exchange",
                [
                    "gse.adult.2022.p22.010",
                    "cefr.cv2020.p078.obtaining_goods_and_services.02",
                ],
            )],
            "phrases": [(
                "Basic expressions for asking for food or drink",
                "make a usable request and answer one server confirmation",
                [
                    "gse.adult.2022.p22.010",
                    "cefr.cv2020.p078.obtaining_goods_and_services.02",
                ],
            )],
            "pronunciation": [(
                "Intelligible delivery of the requested item and essential option",
                "let the listener provide the intended order",
                [
                    "gse.adult.2022.p22.010",
                    "cefr.cv2020.p078.obtaining_goods_and_services.02",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because both sources specify a "
            "limited request using basic expressions without naming a construction."
        ),
        "error": _error(
            "The learner makes a recognisable food or drink request but changes or omits the essential item option.",
            "The listener would provide a different order or need another content question.",
            "the item-and-option demand in the fresh service turn",
        ),
    },
    "lesson_candidate.ask_for_and_give_an_everyday_item": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar everyday item words",
                "request or select the correct visible item in changed partner roles",
                [
                    "gse.adult.2022.p22.021",
                    "gse.adult.2022.p22.028",
                    "gse.adult.2022.p23.011",
                ],
            )],
            "phrases": [(
                "Basic request and handover response expressions",
                "complete both partner roles across the fresh item exchange",
                [
                    "gse.adult.2022.p22.021",
                    "gse.adult.2022.p22.028",
                    "gse.adult.2022.p23.011",
                    "cefr.cv2020.p077.goal_oriented_co_operation.03",
                    "cefr.cv2020.p078.obtaining_goods_and_services.01",
                ],
            )],
            "pronunciation": [(
                "Intelligible delivery of the request and contrasting item name",
                "prevent the partner from handing over the wrong item",
                [
                    "gse.adult.2022.p22.021",
                    "gse.adult.2022.p22.028",
                    "gse.adult.2022.p23.011",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence names asking "
            "and giving with basic language but does not specify a construction."
        ),
        "error": _error(
            "The learner uses a suitable request or handover expression but asks for or gives the distractor item.",
            "The intended item does not change hands accurately.",
            "the item-identity demand across both roles in the fresh exchange",
        ),
    },
    "lesson_candidate.exchange_information_about_an_immediate_need": {
        "targets": {
            "grammar": [(
                "Simple question, answer, and statement frames about an immediate need",
                "ask or answer the changed partner turn with the required practical detail",
                [
                    "gse.adult.2022.p22.018",
                    "cefr.cv2020.p079.information_exchange.02",
                ],
            )],
            "vocabulary": [(
                "Familiar immediate-need and practical-detail words",
                "communicate what is needed and one essential changed detail",
                [
                    "gse.adult.2022.p22.018",
                    "gse.adult.2022.p23.017",
                    "cefr.cv2020.p079.information_exchange.02",
                ],
            )],
            "phrases": [(
                "Brief everyday expressions for describing needs and requesting information",
                "complete the bounded need-and-detail exchange without a dialogue model",
                [
                    "gse.adult.2022.p23.017",
                    "cefr.cv2020.p079.information_exchange.02",
                ],
            )],
            "pronunciation": [(
                "Intelligible delivery of the need and contrasting practical detail",
                "let the partner understand both essential fields",
                [
                    "gse.adult.2022.p22.018",
                    "gse.adult.2022.p23.017",
                ],
            )],
        },
        "decision_note": (
            "All four families stay within the simple questions, statements, immediate "
            "needs, and information request explicitly named by the evidence."
        ),
        "error": _error(
            "The learner communicates the immediate need but answers or requests a different practical detail from the partner's prompt.",
            "The need is known, but the bounded information exchange remains incomplete or inaccurate.",
            "the prompt-sensitive need-and-detail demand in the fresh exchange",
        ),
    },
}
