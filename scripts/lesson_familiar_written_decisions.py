"""Reviewed targets and error decisions for familiar written tasks."""


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


FAMILIAR_WRITTEN_DECISIONS = {
    "lesson_candidate.write_simple_people_profile_cards": {
        "targets": {
            "grammar": [("Simple statements linking each person to a possession, family, pet, or job fact", "keep every written fact attached to the correct profile-card person", ["gse.adult.2022.p37.005", "cefr.cv2020.p066.overall_written_production.01"])],
            "vocabulary": [("Familiar jobs, family, pets, and possession words", "supply the changed fact fields and spell the required common job names accurately", ["gse.adult.2022.p37.005", "gse.adult.2022.p37.014", "cefr.cv2020.p066.overall_written_production.01"])],
            "phrases": [("Brief person-and-fact profile statements", "make two or three people distinguishable to the reader", ["gse.adult.2022.p37.005", "cefr.cv2020.p066.overall_written_production.01"])],
            "pronunciation": [],
        },
        "decision_note": "No pronunciation target is assigned because the profile cards and job-spelling evidence require written performance.",
        "error": _error(
            "The learner attaches a job, possession, family, or pet fact to the wrong person, or spells the required job so it cannot be identified.",
            "The reader builds an inaccurate profile or cannot identify a required job.",
            "the person-to-fact and usable job-spelling distinctions in the profile cards",
        ),
    },
    "lesson_candidate.write_a_short_hobbies_and_likes_post": {
        "targets": {
            "grammar": [("Simple positive and negative hobby or preference statements", "preserve whether each changed activity is liked or disliked", ["gse.adult.2022.p37.008", "cefr.cv2020.p066.overall_written_production.01", "cefr.cv2020.p083.correspondence.01", "cefr.cv2020.p086.online_conversation_and_discussion.01"])],
            "vocabulary": [("Common hobbies and basic preference words", "name each activity and preference required by the post", ["gse.adult.2022.p37.008", "cefr.cv2020.p083.correspondence.01", "cefr.cv2020.p086.online_conversation_and_discussion.01"])],
            "phrases": [("Formulaic hobby and likes-or-dislikes expressions in a short sentence series", "complete the message or post without a generated sentence-level answer", ["cefr.cv2020.p083.correspondence.01", "cefr.cv2020.p086.online_conversation_and_discussion.01"])],
            "pronunciation": [],
        },
        "decision_note": "No pronunciation target is assigned because the outcome is written; dictionary or translation support stays below complete-sentence generation.",
        "error": _error(
            "The learner reverses a like and dislike or leaves an activity without a clear preference.",
            "The reader records the wrong preference or cannot identify it.",
            "the positive-versus-negative preference contrast in the written post",
        ),
    },
    "lesson_candidate.write_schedule_dates_and_times": {
        "targets": {
            "grammar": [],
            "vocabulary": [("Date and time words paired with their digit forms", "represent the changed schedule details in both required forms", ["gse.adult.2022.p37.012", "gse.adult.2022.p37.018"])],
            "phrases": [("Paired date-and-time schedule entries in digits and words", "keep both representations unambiguous and equivalent", ["gse.adult.2022.p37.012", "gse.adult.2022.p37.018"])],
            "pronunciation": [],
        },
        "decision_note": "No separate grammar or pronunciation target is assigned because the cited task assesses equivalent written date and time representations.",
        "error": _error(
            "The learner writes digit and word forms that represent different dates or times, or places one detail in the wrong field.",
            "The reader records an ambiguous or incorrect schedule.",
            "the form-equivalence and field-matching requirements of the schedule entry",
        ),
    },
    "lesson_candidate.write_simple_life_and_routine_sentences": {
        "targets": {
            "grammar": [("Simple statements keeping one person linked to their life and routine facts", "make all three changed facts belong clearly to the prompted person", ["gse.adult.2022.p37.015"])],
            "vocabulary": [("Familiar daily activities and basic life facts", "supply the three prompt fields without importing unsupported detail", ["gse.adult.2022.p37.015"])],
            "phrases": [("A short series of life-and-routine sentences", "produce a coherent small written profile rather than isolated labels", ["gse.adult.2022.p37.015"])],
            "pronunciation": [],
        },
        "decision_note": "No pronunciation target is assigned because the source and mastery task require written sentences; fictional people remain permitted.",
        "error": _error(
            "The learner shifts to a different person so an activity or life fact has no clear owner.",
            "The reader cannot reconstruct one person's life and routine accurately.",
            "the person-to-routine mapping required across the three written sentences",
        ),
    },
    "lesson_candidate.write_a_simple_object_description": {
        "targets": {
            "grammar": [("Basic descriptive statements linking a familiar object to visible features", "combine the changed object identity with its required colour, size, or shape facts", ["gse.adult.2022.p37.007", "gse.adult.2022.p37.019", "cefr.cv2020.p067.creative_writing.03"])],
            "vocabulary": [("Familiar object names plus basic colour, size, and shape words", "identify the object and every prompted visible feature", ["gse.adult.2022.p37.007", "gse.adult.2022.p37.019", "cefr.cv2020.p067.creative_writing.03"])],
            "phrases": [("Short object-identification and feature-description phrases", "make the shown object identifiable without copying completed sentences", ["gse.adult.2022.p37.007", "cefr.cv2020.p067.creative_writing.03"])],
            "pronunciation": [],
        },
        "decision_note": "No pronunciation target is assigned because this is written description; a source-permitted model may show form but not the fresh answer sentences.",
        "error": _error(
            "The learner names the object but reverses or omits a required visible feature.",
            "The reader identifies the wrong object or records an inaccurate feature.",
            "the object-identity and visible-feature contrast in the fresh description",
        ),
    },
    "lesson_candidate.write_a_simple_room_description": {
        "targets": {
            "grammar": [("Simple position statements connecting familiar things to places in a room", "preserve each changed object and spatial relation", ["gse.adult.2022.p37.017", "cefr.cv2020.p067.creative_writing.02"])],
            "vocabulary": [("Basic room, familiar-object, and position words", "name the prompted things and where they are", ["gse.adult.2022.p37.017", "cefr.cv2020.p067.creative_writing.02"])],
            "phrases": [("A few fixed expressions describing object positions in a room", "let the reader reconstruct the pictured or fictional layout", ["gse.adult.2022.p37.017", "cefr.cv2020.p067.creative_writing.02"])],
            "pronunciation": [],
        },
        "decision_note": "No pronunciation target is assigned because the source task is written; the room may be fictional and must remain culturally neutral.",
        "error": _error(
            "The learner assigns a position to the wrong object or reverses the spatial relation.",
            "The reader reconstructs a different room layout.",
            "the object-versus-position mapping required by the pictured-room task",
        ),
    },
}
