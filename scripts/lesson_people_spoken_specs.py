"""Spoken production candidates for people and relationships."""

try:
    from scripts.lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import BASIC_SPOKEN, evidence, mastery, outcome


COMMON = {
    "candidate_cluster_ids": ["people_relationships"],
    "reviewed_at": "2026-07-17T16:48:13+03:00",
}

SPOKEN_SPECS = [
    {
        **COMMON,
        "candidate_id": "lesson_candidate.say_where_people_are",
        "outcome": outcome(
            "a simple check-in or picture-based location update",
            "say where the learner and other people are",
            "two or three people with familiar basic locations",
            "with names or picture cues but without complete sentences to copy",
            "a listener can locate each required person",
            "In a fresh simple location update, the learner can say where they and other people are.",
        ),
        "evidence": [evidence(
            "gse.adult.2022.p22.001", "anchor",
            "The objective directly anchors limited statements about where self and other people are.",
        )],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["give_information"],
        "normalization_rationale": "Self and other-person locations are parallel statements in one bounded update.",
        "mastery": mastery(
            "A fresh check-in list, picture, or simple whereabouts update.",
            {
                "comprehension": "Understands which people require a location update.",
                "outcome_performance": "States a usable familiar location for every required person.",
                "interaction_or_transfer": "Adapts the statements to new people and locations.",
                "control_or_repair": "Location meaning stays intelligible and one signalled mix-up can be repaired.",
            },
            ["A required person is omitted or assigned the wrong location."],
            ["Minor form errors that preserve who is where."],
            ["Names or picture cues and neutral instruction repetition."],
            "Use different people and familiar locations after a delay.",
        ),
        "scope": ["focused", "Two or three short location statements."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Later place work must not duplicate this full anchor."],
    },
    {
        **COMMON,
        "candidate_cluster_ids": ["people_relationships", "social_contact_collaboration"],
        "reviewed_at": "2026-07-17T22:52:27+03:00",
        "candidate_id": "lesson_candidate.introduce_another_person",
        "outcome": outcome(
            "a simple social or group introduction",
            "introduce another person",
            "the person's name and familiar job title",
            "with a name card but without a complete spoken model",
            "listeners can identify the person and role",
            "In a fresh social situation, the learner can introduce another person by name and familiar job title.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p22.022", "anchor", "The objective directly anchors a basic name-and-job introduction."),
            evidence("gse.adult.2022.p23.005", "supporting", "Stating a familiar common job is a required move in the same introduction."),
            evidence("gse.adult.2022.p23.002", "supporting", "The broader objective confirms a basic introduction of another person."),
            evidence(
                "gse.adult.2022.p23.012", "supporting",
                "Covers the make-an-introduction clause; greeting and leave-taking are assigned to a social exchange.", "partial",
            ),
            evidence(
                "cefr.cv2020.p074.conversation.03", "supporting",
                "Covers the make-an-introduction clause; greeting and leave-taking are assigned to a social exchange.", "partial",
            ),
        ],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["introduce", "give_information"],
        "normalization_rationale": "The sources converge on one short introduction; name and job keep the performance concrete and assessable.",
        "mastery": mastery(
            "A fresh group, workplace, or class introduction using a safe fictional person.",
            {
                "comprehension": "Identifies which person and role must be introduced.",
                "outcome_performance": "Gives the correct name and familiar job title in an intelligible introduction.",
                "interaction_or_transfer": "Introduces a different person in an equivalent context.",
                "control_or_repair": "Repairs one signalled name or job mix-up without a model.",
            },
            ["The listener cannot identify the person or their job."],
            ["Minor article or hesitation errors that preserve the introduction."],
            ["A name card and fictional information."],
            "Use a new person, job, and introduction context after a delay.",
        ),
        "scope": ["focused", "One basic introduction containing a name and job."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Job choices must stay familiar and A1-bounded."],
    },
    {
        **COMMON,
        "candidate_id": "lesson_candidate.describe_a_family_or_known_person",
        "outcome": outcome(
            "a simple family photo or prompt about people the learner knows",
            "give a basic spoken description",
            "who two or three people are and one familiar fact about each",
            "with picture or relationship cues but without a complete model",
            "a listener can distinguish the people and relationships",
            "In a fresh prompted situation, the learner can describe a family or known person in a basic way.",
        ),
        "evidence": [
            evidence("gse.adult.2022.p24.004", "anchor", "The objective directly anchors prompted basic talk about family."),
            evidence(
                "cefr.cv2020.p062.overall_oral_production.01", "supporting",
                "Covers simple isolated phrases about people; the places clause remains for the places partition.", "partial",
            ),
        ],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["describe", "give_information"],
        "normalization_rationale": "A small family or known-person description is one prompted monologic performance.",
        "mastery": mastery(
            "A fresh family image or safe fictional people card with changed relationships.",
            {
                "comprehension": "Understands which people and relationships to describe.",
                "outcome_performance": "Identifies each required person and gives one clear familiar fact.",
                "interaction_or_transfer": "Describes different people from a new prompt.",
                "control_or_repair": "Relationship meaning stays clear and one signalled mix-up can be repaired.",
            },
            ["People or relationships are confused so the listener cannot distinguish them."],
            ["Isolated phrases or minor grammar errors that preserve all facts."],
            ["Picture and relationship cues; fictional people."],
            "Use a new image and relationship set after a delay.",
        ),
        "scope": ["standard", "Two or three people and one familiar fact about each."],
        "basic_support_ids": BASIC_SPOKEN,
        "risks": ["Prompts must not imply a culturally fixed family structure."],
    },
]
