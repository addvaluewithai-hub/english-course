"""Reviewed targets and error decisions for familiar home and object speech."""


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


FAMILIAR_HOME_SPOKEN_DECISIONS = {
    "lesson_candidate.describe_people_and_object_locations_orally": {
        "targets": {
            "grammar": [("Basic location statements for people and objects", "state each prompted location without changing its referent", ["gse.adult.2022.p22.001", "gse.adult.2022.p22.008"])],
            "vocabulary": [("Familiar people, objects, and basic location or position words", "identify who or what is in each changed position", ["gse.adult.2022.p22.001", "gse.adult.2022.p22.008"])],
            "phrases": [("Short statements saying where a person or object is", "make every required location usable by the listener", ["gse.adult.2022.p22.001", "gse.adult.2022.p22.008"])],
            "pronunciation": [("Intelligible contrasts among people, objects, and positions", "prevent a listener from assigning a location to the wrong referent", ["gse.adult.2022.p22.001", "gse.adult.2022.p22.008"])],
        },
        "decision_note": "People and object locations share one bounded oral position task; later place-direction language is not added here.",
        "error": _error(
            "The learner names the right place but assigns it to the wrong person or object, or reverses the position relation.",
            "The listener locates a required referent incorrectly.",
            "the referent-versus-position mapping required by the fresh scene",
        ),
    },
    "lesson_candidate.describe_a_familiar_object_orally": {
        "targets": {
            "grammar": [("Basic descriptive statements connecting an object with visible features", "combine the identity and required features into an understandable description", ["gse.adult.2022.p22.015", "gse.adult.2022.p24.001", "cefr.cv2020.p063.sustained_monologue_giving_information.01"])],
            "vocabulary": [("Familiar object names plus basic shape, colour, and size words", "identify the changed object and its visible features", ["gse.adult.2022.p22.015", "gse.adult.2022.p24.001", "cefr.cv2020.p063.sustained_monologue_giving_information.01"])],
            "phrases": [("Basic naming and visible-feature description phrases", "make the shown object identifiable without a prepared script", ["gse.adult.2022.p24.001", "cefr.cv2020.p063.sustained_monologue_giving_information.01"])],
            "pronunciation": [("Intelligible delivery of the object name and contrasting features", "preserve the intended shape, colour, and size", ["gse.adult.2022.p22.015", "cefr.cv2020.p063.sustained_monologue_giving_information.01"])],
        },
        "decision_note": "The sources support prepared basic description, but preparation cannot become a complete model for the fresh object.",
        "error": _error(
            "The learner names the object but reverses or omits a required visible feature.",
            "The listener cannot identify the intended object or records the wrong feature.",
            "the object-identity and visible-feature contrast in the show-and-tell task",
        ),
    },
    "lesson_candidate.exchange_visible_object_information": {
        "targets": {
            "grammar": [("Simple object questions with short relevant answers", "ask for and supply the requested colour, size, or quantity fact", ["gse.adult.2022.p22.004", "gse.adult.2022.p22.026", "gse.adult.2022.p23.003", "cefr.cv2020.p079.information_exchange.06"])],
            "vocabulary": [("Familiar objects, colours, sizes, and countable numbers", "identify the requested object and visible fact in each turn", ["gse.adult.2022.p22.004", "gse.adult.2022.p22.026", "gse.adult.2022.p23.003", "cefr.cv2020.p079.information_exchange.06"])],
            "phrases": [("Basic colour, size, and how-many question-answer turns", "exchange every prompted visible fact without a dialogue model", ["gse.adult.2022.p22.004", "gse.adult.2022.p22.026", "gse.adult.2022.p23.003", "cefr.cv2020.p079.information_exchange.06"])],
            "pronunciation": [("Intelligible contrasts among colour, size, and number answers", "keep each visible fact attached to the correct object", ["gse.adult.2022.p22.004", "gse.adult.2022.p23.003", "cefr.cv2020.p079.information_exchange.06"])],
        },
        "decision_note": "Quantity remains visually countable; the three fields are parallel facts in one bounded picture gap.",
        "error": _error(
            "The learner gives a plausible feature or number but answers for the wrong object or question type.",
            "A requested fact is exchanged inaccurately or remains missing.",
            "the object-versus-feature question contrast in the visual information gap",
        ),
    },
    "lesson_candidate.exchange_basic_information_about_a_home": {
        "targets": {
            "grammar": [("Basic home and possession questions with short relevant answers", "ask for and supply each safe fictional or real home fact", ["gse.adult.2022.p22.017", "cefr.cv2020.p079.information_exchange.03"])],
            "vocabulary": [("Familiar rooms, home things, and possession words", "identify the home or possession fact requested in each turn", ["gse.adult.2022.p22.017", "cefr.cv2020.p079.information_exchange.03"])],
            "phrases": [("Short ask-and-answer turns about a home and things someone has", "complete both sides of the bounded home-information exchange", ["gse.adult.2022.p22.017", "cefr.cv2020.p079.information_exchange.03"])],
            "pronunciation": [("Intelligible delivery of room, thing, and ownership contrasts", "keep the home facts and possessor clear", ["gse.adult.2022.p22.017", "cefr.cv2020.p079.information_exchange.03"])],
        },
        "decision_note": "Safe fictional answers remain permitted, and prompts must not assume ownership, wealth, or private disclosure.",
        "error": _error(
            "The learner supplies the requested room or object but reverses who has it or which home it belongs to.",
            "The partner records an inaccurate home or possession fact.",
            "the home-fact and possession-owner mapping required by the exchange",
        ),
    },
}
