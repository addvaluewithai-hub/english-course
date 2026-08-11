"""Build migrated gold-lesson manifests, learning content, and controls."""

from copy import deepcopy

from scripts.gold_v1_contract import CANDIDATE_ID, LESSON_ID, UNIT_ID


def manifest(legacy: dict, lesson: dict) -> dict:
    data = deepcopy(legacy)
    data.update({
        "schema_version": 2, "lesson_id": LESSON_ID, "unit_id": UNIT_ID,
        "global_sequence_position": lesson["global_sequence_position"],
        "status": "migrated_v1_qa_ready", "candidate_id": CANDIDATE_ID,
        "source_packet": "source-packet.json",
        "scope_sequence_ref": "data/reviewed/a1-scope-and-sequence-v1.json",
        "prototype_lineage": "gold/introduce-yourself",
    })
    data["title"] = lesson["title"]
    data["goal"]["en"] = lesson["outcome_statement"]
    data["prerequisites"] = ["U1-L01", "U1-L02"]
    data["curriculum_boundary"] = {
        "introduce": ["my + name only", "a/an + job", "basic statement order", "own country form"],
        "recycle": ["I/I'm", "present be affirmative", "identity and place labels"],
        "pronunciation": ["word stress in selected personal words", "short sense-group pauses"],
        "not_yet": ["full possessive system", "full article system", "systematic /ɪ/-/aɪ/ contrast"],
    }
    return data


def content(legacy: dict) -> dict:
    data = deepcopy(legacy)
    data["schema_version"] = 2
    data["curriculum_alignment"] = {
        "prior_learning": ["basic greetings", "heard I/I'm and present be", "identity/place labels"],
        "bounded_new_forms": ["My name is ...", "a/an + job", "short subject-first statements"],
        "personalized_lexis": "the learner's own country/nationality plus chosen role or interest",
        "pronunciation_targets": [
            "a1_pronunciation.lesson_critical_word_stress",
            "a1_pronunciation.sense_group_chunking",
        ],
        "explicit_non_goal": "No systematic live /lɪv/ versus /laɪv/ contrast at U1-L03.",
    }
    data["notice"].insert(1, {
        "chunk": "My name is Maya.", "meaning_ar": "اسمي مايا",
        "field": "name_alternative", "scope_note": "Introduce my with name only.",
    })
    data["explanation_ar"].insert(
        1, "My name is ... بديل طبيعي لـ I'm ...؛ هنا بنتعلم my مع name فقط، وباقي الملكية هتيجي بعدين."
    )
    data["explanation_ar"].insert(
        4, "مع الوظيفة نستخدم a أو an: I'm a designer. I'm an engineer."
    )
    data["pronunciation"] = [
        {"focus": "selected personal words", "tip_ar": "اسمع الجزء الأوضح في اسم البلد أو الوظيفة وقلّده داخل الكلمة.", "sample": "teacher, engineer, designer"},
        {"focus": "information groups", "tip_ar": "اتوقف وقفة قصيرة بين الجمل بدل ما تقول المقدمة كلها بنفس واحد.", "sample": "Hi, I'm Maya. | I'm from Jordan. | I live in Amman."},
    ]
    return data


def activities(legacy: dict) -> dict:
    data = deepcopy(legacy)
    data["schema_version"] = 2
    new_activity = {
        "id": "my_and_job_articles", "type": "choice_set",
        "prompt_ar": "اختر الجملة الطبيعية لكل معنى.",
        "items": [
            {"meaning_ar": "اسمي سارة", "options": ["My name is Sara.", "I name is Sara."], "answer": 0},
            {"meaning_ar": "أنا مهندس", "options": ["I'm a engineer.", "I'm an engineer."], "answer": 1},
        ],
        "feedback_ar": "استخدم My name is مع الاسم، وan قبل engineer.",
    }
    data["activities"].insert(2, new_activity)
    data["curriculum_rule"] = "Applied questions begin only after the video; mastery remains a fresh unsupported task."
    return data


def assessment(legacy: dict) -> dict:
    data = deepcopy(legacy)
    data["schema_version"] = 2
    data["lesson_id"] = LESSON_ID
    data["mastery_task"]["prior_lesson_support"] = "U1-L01 greetings and U1-L02 listening input may be recalled, but no complete introduction is shown."
    data["replacement_mastery_task"] = {
        "scenario_en": "You have just joined a local community event.",
        "scenario_ar": "انضممت الآن إلى فعالية محلية وتقابل شخصًا للمرة الأولى.",
        "prompt_en": "Introduce yourself in four or five short sentences.",
        "required": list(data["mastery_task"]["required"]),
        "support": "Field icons or labels only; no sentence frames or model.",
        "freshness": "The setting, listener, and field order differ from both practice and the primary task.",
        "safe_identity": True,
        "use_only_when": "The primary attempt became practice after answer-revealing correction or help.",
    }
    data["mastery_attempt_policy"] = {
        "maximum_fresh_attempts": 2,
        "replacement_required_after_answer_revealing_help": True,
        "second_failure_result": "practiced_or_needs_review_not_demonstrated",
    }
    for row in data["rubric"]:
        if row["dimension"] == "interaction_or_transfer":
            row["dimension"] = "context_transfer"
    return data


def ai_contract(legacy: dict) -> dict:
    data = deepcopy(legacy)
    data["schema_version"] = 2
    data["lesson_id"] = LESSON_ID
    data["curriculum_limits"] = [
        "Recycle I/I'm and present be; do not reteach the full paradigm.",
        "Teach my only in My name is and a/an only with selected jobs.",
        "Coach word stress and sense-group pauses; do not run a systematic vowel-contrast lesson.",
    ]
    return data


def pronunciation_map(legacy: dict) -> dict:
    data = deepcopy(legacy)
    data["schema_version"] = 2
    data["curriculum_target_ids"] = [
        "a1_pronunciation.lesson_critical_word_stress",
        "a1_pronunciation.sense_group_chunking",
    ]
    data["entries"] = [row for row in data["entries"] if row["text"] != "live (verb)"]
    data["entries"].extend([
        {"text": "teacher", "ipa": "/ˈtiːtʃɚ/", "director_hint": "TEA-cher"},
        {"text": "engineer", "ipa": "/ˌɛndʒəˈnɪr/", "director_hint": "engi-NEER"},
    ])
    return data
