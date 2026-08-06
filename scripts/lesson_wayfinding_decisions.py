"""Reviewed targets for the opening wayfinding candidates."""


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


WAYFINDING_DECISIONS = {
    "lesson_candidate.follow_simple_written_wayfinding_directions": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar written place, destination, and route-move words",
                "identify the named start, destination, and two or three written moves",
                [
                    "gse.adult.2022.p09.004",
                    "cefr.cv2020.p056.reading_for_orientation.02",
                    "cefr.cv2020.p058.reading_instructions.01",
                ],
            )],
            "phrases": [(
                "Short simple written directions linking one point to another",
                "follow the complete route rather than matching one isolated place word",
                [
                    "gse.adult.2022.p09.004",
                    "cefr.cv2020.p058.reading_instructions.01",
                ],
            )],
            "pronunciation": [],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence specifies "
            "written route comprehension without naming a construction; no pronunciation "
            "target is assigned because the fresh task is written reception."
        ),
        "error": _error(
            "The learner recognises the written start and destination but reverses or skips an essential route move.",
            "The selected route reaches the wrong destination.",
            "the ordered-move requirement in the fresh written route task",
        ),
    },
    "lesson_candidate.follow_slow_spoken_route_directions": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Familiar spoken route, place, and public-transport words",
                "identify the route moves and destination on the changed plan",
                ["gse.adult.2022.p15.004"],
            )],
            "phrases": [(
                "Short simple spoken directions from one point to another",
                "combine two or three slowly delivered moves into one complete route",
                [
                    "gse.adult.2022.p15.004",
                    "gse.adult.2022.p15.015",
                    "cefr.cv2020.p051.understanding_announcements_and_instructions.01",
                ],
            )],
            "pronunciation": [(
                "Recognition of ordered route words in slow clear speech",
                "distinguish each essential move without a transcript or traced path",
                [
                    "gse.adult.2022.p15.015",
                    "cefr.cv2020.p051.understanding_announcements_and_instructions.01",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the evidence supports "
            "following carefully delivered directions, not control of a named form; "
            "productive pronunciation is not mastery evidence."
        ),
        "error": _error(
            "The learner identifies the destination word but reverses or omits one spoken route move.",
            "The traced route does not follow the complete spoken directions.",
            "the destination-word versus ordered-route contrast in the listening task",
        ),
    },
    "lesson_candidate.follow_simple_directions_from_an_interlocutor": {
        "targets": {
            "grammar": [],
            "vocabulary": [(
                "Basic location and route-move words in directly addressed speech",
                "act on two or three directions involving familiar locations",
                [
                    "cefr.cv2020.p073.understanding_an_interlocutor.02",
                    "cefr.cv2020.p077.goal_oriented_co_operation.02",
                ],
            )],
            "phrases": [(
                "Short simple directions and instructions addressed carefully and slowly",
                "follow the interlocutor's complete direction sequence in the live task",
                [
                    "cefr.cv2020.p073.understanding_an_interlocutor.02",
                    "cefr.cv2020.p077.goal_oriented_co_operation.01",
                    "cefr.cv2020.p079.information_exchange.01",
                ],
            )],
            "pronunciation": [(
                "Recognition of location and move contrasts in careful slow delivery",
                "distinguish the ordered actions without a demonstrated route",
                [
                    "cefr.cv2020.p073.understanding_an_interlocutor.02",
                    "cefr.cv2020.p077.goal_oriented_co_operation.01",
                    "cefr.cv2020.p079.information_exchange.01",
                ],
            )],
        },
        "decision_note": (
            "No separate grammar target is assigned because the repeated descriptors "
            "support live direction following without naming a construction; the "
            "times-and-numbers clause remains outside this location-scoped target."
        ),
        "error": _error(
            "The learner acts on familiar location words but performs the interlocutor's moves in the wrong order.",
            "The live task ends at the wrong location despite partial word recognition.",
            "the word-recognition versus ordered-action demand in live direction following",
        ),
    },
    "lesson_candidate.exchange_basic_wayfinding_information": {
        "targets": {
            "grammar": [(
                "Basic questions for a route and short answers about where people or things are",
                "complete both reciprocal moves in the changed map information gap",
                ["gse.adult.2022.p23.009", "gse.adult.2022.p24.005"],
            )],
            "vocabulary": [(
                "Familiar destination, person, thing, and location words",
                "keep the requested destination and two referents distinct",
                ["gse.adult.2022.p23.009", "gse.adult.2022.p24.005"],
            )],
            "phrases": [(
                "A simple direction request referring to a map and limited location answers",
                "obtain the route and supply each required location without a dialogue model",
                ["gse.adult.2022.p23.009", "gse.adult.2022.p24.005"],
            )],
            "pronunciation": [(
                "Intelligible delivery of the destination and contrasting location words",
                "let the partner identify the requested route and each referent",
                ["gse.adult.2022.p23.009", "gse.adult.2022.p24.005"],
            )],
        },
        "decision_note": (
            "Targets stay limited to the source-supported map request and location "
            "answers; they do not require an extended route explanation or a fixed "
            "dialogue script."
        ),
        "error": _error(
            "The learner asks about one destination or referent but gives a location for another.",
            "The partners leave the information gap with a wrong route or location.",
            "the referent-to-location matching demand in the reciprocal map exchange",
        ),
    },
}
