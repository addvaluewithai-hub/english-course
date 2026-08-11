from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l04_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l04.personal_detail_exchange",
    "critical_meaning": "Each question retrieves its intended detail and unclear key information is repaired.",
    "primary": {
        "scenario_en": "You meet a fictional class partner and need four details for a pair task.",
        "scenario_ar": "تقابل زميل خيالي وتحتاج أربع معلومات لمهمة ثنائية.",
        "prompt_en": "Ask for name, origin, residence, and job; answer the partner's changed questions.",
        "required": ["four_fitting_questions", "four_relevant_answers", "one_repair_if_needed"],
        "support": "Detail icons only; no full question or answer frames.",
        "freshness": "The partner, missing details, order, and repair need differ from practice.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "You welcome a fictional volunteer and complete a verbal contact check.",
        "scenario_ar": "ترحب بمتطوع خيالي وتراجع بياناته شفهيًا.",
        "prompt_en": "Exchange four changed personal details and repair one unclear name or job.",
        "required": ["four_fitting_questions", "four_relevant_answers", "one_repair_if_needed"],
        "support": "Detail icons only; no full question or answer frames.",
        "freshness": "The role, information gap, and repair target are new.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L04",
    "goal_ar": "أن تسأل وتجيب عن معلومات شخصية مباشرة وتصلح المعلومة غير الواضحة.",
    "scope": {
        "required_details": ["name", "origin", "residence", "job"],
        "performance": "one fresh two-way information gap with repair",
        "time_hypothesis_minutes": "30-40",
    },
    "teach_back_summary": "Explain the origin/residence question contrast and one repair choice.",
    "non_goals": ["A long interview", "Private real contact data", "Full question-system terminology"],
    "prerequisites": ["U1-L01", "U1-L02", "U1-L03"],
    "bounded_scope_notes": [
        "Use selected be questions and short answers for identity, job, and origin checks.",
        "Treat high-utility wh-questions as usable frames, not a full auxiliary lesson.",
        "Repair one unclear key detail by repetition, confirmation, or spelling.",
        "Use prominence only to highlight the corrected detail.",
    ],
    "not_yet": ["open-ended interviewing", "full do/does contrast", "complete alphabet instruction"],
    "content": {
        "situation": {
            "title_ar": "موقف اليوم",
            "prompt_ar": "تحتاج تبادل أربع معلومات مع زميل جديد، واسم واحد قد لا يكون واضحًا.",
            "success_ar": "كل سؤال يستخرج المعلومة المقصودة وأي سوء سماع يتم إصلاحه.",
        },
        "model": {
            "roles": ["Nina", "Mona"],
            "lines": ["What's your name?", "I'm Mona.", "Where are you from?", "I'm from Egypt."],
            "gist_question_ar": "أي معلومة طلبها كل سؤال؟",
            "gist_answer": ["name", "origin"],
        },
        "notice": [
            {"chunk": "What's your name?", "field": "name"},
            {"chunk": "Where are you from?", "field": "origin"},
            {"chunk": "Where do you live?", "field": "residence"},
            {"chunk": "What's your job?", "field": "job"},
            {"chunk": "Can you spell that?", "field": "repair_name"},
        ],
        "explanation_ar": [
            "اختر السؤال حسب المعلومة الناقصة، ولا تقدم فقرة كاملة بدل إجابة محددة.",
            "Are you ...? مناسب للتأكد، وتأتي معه إجابة قصيرة واضحة.",
            "طلب التكرار أو التهجئة مهارة تواصل، وليس فشلًا.",
            "في التصحيح اجعل التفصيلة المصححة أوضح من بقية الجملة من غير صراخ.",
        ],
        "toolkit": {
            "questions": ["What's your name?", "Where are you from?", "Where do you live?", "What's your job?"],
            "checks": ["Are you a teacher?", "Is that Mona?"],
            "repair": ["Can you spell that?", "Please say that again.", "Yes, that's right."],
            "jobs": ["teacher", "doctor", "nurse", "driver", "manager", "cook"],
        },
        "pronunciation": [
            {"focus": "letter names", "tip_ar": "استخدم اسم الحرف لتأكيد الاسم بدل تخمين صوته."},
            {"focus": "key detail", "tip_ar": "اجعل الاسم أو المعلومة المصححة أوضح فقط."},
            {"focus": "repair", "tip_ar": "أعد الجزء المهم أبطأ أو هجّئه إذا لم يصل."},
        ],
    },
    "activities": [
        {
            "id": "question_to_field",
            "type": "match",
            "prompt_ar": "طابق السؤال بالمعلومة التي يستخرجها.",
            "pairs": [["What's your name?", "name"], ["Where are you from?", "origin"], ["Where do you live?", "residence"], ["What's your job?", "job"]],
        },
        {
            "id": "short_answer_check",
            "type": "choice_set",
            "prompt_ar": "اختر الإجابة المناسبة لسؤال التأكد.",
            "items": [
                {"prompt": "Are you a nurse?", "options": ["Yes, I am.", "Yes, you are."], "answer": 0},
                {"prompt": "Are you from Jordan?", "options": ["No, I'm not.", "No, he isn't."], "answer": 0},
            ],
        },
        {
            "id": "repair_choice",
            "type": "choice",
            "prompt_ar": "لم تسمع الاسم. ماذا تقول؟",
            "options": ["Can you spell that?", "Where do you live?", "I'm a teacher."],
            "answer": 0,
        },
        {
            "id": "guided_information_gap",
            "type": "production",
            "prompt_ar": "اسأل شخصية خيالية عن أربع خانات وأجب عن أسئلتها. استخدم إصلاحًا واحدًا عند الحاجة.",
            "fields": ["name", "origin", "residence", "job", "repair"],
            "model_hidden": True,
        },
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L04",
        MASTERY,
        {
            "comprehension": "Questions and answers address the intended missing details.",
            "outcome_performance": "Four details are exchanged successfully in both directions.",
            "context_transfer": "The learner adapts to changed question order and partner details.",
            "control_or_repair": "One unclear key detail is checked, repeated, or spelled successfully.",
        },
        "اشرح الفرق بين Where are you from? وWhere do you live? واذكر طريقة إصلاح واحدة.",
        [
            {"when": "next day", "task": "Ask for two changed details and confirm one."},
            {"when": "three days", "task": "Repair a new unclear fictional name."},
            {"when": "seven days", "task": "Complete a new four-detail two-way exchange."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L04",
        "Coach a two-way personal-detail exchange without supplying the learner's questions.",
        "Hi! Ask me for the first detail you need.",
        "اسأل عن خانة واحدة في كل مرة، ويمكنك استخدام بيانات خيالية.",
        ["Question retrieves the wrong detail", "Answer does not address the question", "Unclear key detail is guessed rather than repaired"],
        ["Stay within the four selected personal-detail questions and one repair move.", "Do not request real private contact data.", "Accept intelligible contour and accent variation."],
        turn_limit=10,
    ),
    "scene": "An adult study-pair registration moment in a quiet learning space. The teacher is friendly and precise, treating clarification and spelling as normal communication rather than mistakes.",
    "sample_context": "One Egyptian-Arabic teacher models both roles of a short information-gap exchange. General American English is clear and natural, with key corrected details slightly prominent. No learner interaction inside the video; all questions follow it.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {
        "schema_version": 2,
        "accent": "General American",
        "usage": "Production reference; prominence serves meaning, not performance theatre.",
        "entries": [
            {"text": "What's your name?", "ipa": "/wʌts jɚ neɪm/", "director_hint": "friendly question"},
            {"text": "M-O-N-A", "ipa": "/ɛm oʊ ɛn eɪ/", "director_hint": "separate letter names"},
            {"text": "My NAME is MONA.", "ipa": "/maɪ ˈneɪm ɪz ˈmoʊnə/", "director_hint": "key detail prominent, not shouted"},
            {"text": "Please say that again.", "ipa": "/pliːz seɪ ðæt əˈɡɛn/", "director_hint": "polite repair"},
        ],
        "curriculum_target_ids": [
            "a1_pronunciation.spelling_sound_verification",
            "a1_pronunciation.key_information_prominence",
            "a1_pronunciation.pronunciation_repair",
            "a1_pronunciation.question_social_contours",
        ],
    },
    "asset_briefs": """# U1-L04 Asset Briefs

Use a fictional four-field information-gap card, question-purpose icons, and a repair
card showing repeat, confirm, and spell. Keep all personal data fictional. Any letter
animation must have a text alternative. Provide captions, transcript, replay, keyboard
access, and a second voice only for fresh post-video prompts—not for the teacher video.
""",
    "video_readme": video_readme("U1-L04", "Ask and Answer Personal Questions"),
}
