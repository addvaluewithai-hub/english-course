from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l09_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l09.written_personal_detail_exchange",
    "critical_meaning": "Each message fulfils its request or response purpose and keeps every fictional detail accurate.",
    "primary": {
        "scenario_en": "A fictional class partner messages you before the first session.",
        "scenario_ar": "زميل خيالي يراسلك قبل أول محاضرة.",
        "prompt_en": "Reply with two requested details, ask for one missing detail, confirm it, and close.",
        "required": ["relevant_two_detail_reply", "one_missing_detail_question", "confirmation", "closing"],
        "support": "Message-purpose icons only; no complete frames or model exchange.",
        "freshness": "The request, missing field, values, and message order differ from practice.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "A fictional volunteer coordinator starts a different short message exchange.",
        "scenario_ar": "منسق متطوعين خيالي يبدأ تبادل رسائل مختلفًا.",
        "prompt_en": "Provide the changed requested details, retrieve one missing detail, confirm, and close.",
        "required": ["relevant_two_detail_reply", "one_missing_detail_question", "confirmation", "closing"],
        "support": "Message-purpose icons only; no complete frames or model exchange.",
        "freshness": "A new role, request, field, and values keep the interaction equivalent and fresh.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L09",
    "goal_ar": "أن ترد على طلب بيانات كتابة وتسأل عن معلومة ناقصة داخل تبادل قصير.",
    "scope": {"required_moves": ["read purpose", "relevant reply", "follow-up question", "confirmation", "close"], "performance": "one fresh simulated written exchange", "time_hypothesis_minutes": "25-35"},
    "teach_back_summary": "Explain why a grammatically correct message can still fail its communicative purpose.",
    "non_goals": ["New grammar", "Long email writing", "Real messaging accounts", "Real personal data"],
    "prerequisites": ["U1-L04", "U1-L06", "U1-L08"],
    "bounded_scope_notes": [
        "Integrate previously taught personal-detail questions, replies, spelling repair, and short coordination.",
        "Select content by message purpose; do not add a new exact language-system target.",
        "Use a simulated exchange and fictional data only.",
    ],
    "not_yet": ["extended correspondence", "formal email conventions", "unmoderated real online interaction"],
    "content": {
        "situation": {"title_ar": "موقف اليوم", "prompt_ar": "تقرأ رسالة خيالية، ترد بما طُلب، وتسأل عن المعلومة الناقصة.", "success_ar": "كل رسالة تحقق غرضها، وكل البيانات محفوظة بدقة."},
        "model": {
            "incoming": "Hi! What's your name, and where are you from?",
            "reply": "Hi! I'm Omar, and I'm from Egypt.",
            "follow_up": "Where do you live?",
            "gist_question_ar": "ما الذي طلبته الرسالة وما الذي قدمه الرد؟",
            "gist_answer": ["name", "origin"],
        },
        "notice": [
            {"move": "request", "example": "Where do you live?"},
            {"move": "reply", "example": "I live in Amman."},
            {"move": "repair", "example": "Can you spell your last name, please?"},
            {"move": "confirm", "example": "Yes, that's right."},
            {"move": "close", "example": "Thanks. See you in class."},
        ],
        "explanation_ar": [
            "حدد هل دورك طلب معلومة أم تقديمها قبل الكتابة.",
            "رد فقط على التفاصيل المطلوبة، ثم اسأل عن الناقص.",
            "الجملة الصحيحة لغويًا قد تفشل لو لم تجب عن غرض الرسالة.",
            "استخدم التأكيد أو التهجئة عندما تكون الدقة مهمة.",
        ],
        "toolkit": {
            "requests": ["What's your name?", "Where are you from?", "Where do you live?", "What's your job?"],
            "replies": ["I'm …", "I'm from …", "I live in …", "I'm a …"],
            "repair_and_close": ["Can you spell that?", "Is that …?", "Yes, that's right.", "Thanks. See you in class."],
        },
        "pronunciation": [],
    },
    "activities": [
        {"id": "request_or_reply", "type": "classify", "prompt_ar": "حدد هل الرسالة تطلب معلومة أم تقدمها.", "classes": ["request", "reply"]},
        {"id": "relevance_repair", "type": "edit", "prompt_ar": "أصلح ردًا صحيح الكلمات لكنه لا يجيب عن المطلوب.", "critical_rule": "message purpose"},
        {"id": "missing_detail", "type": "choice", "prompt_ar": "اختر سؤال المتابعة الذي يطلب المعلومة الناقصة.", "answer_reveal_after_attempt": True},
        {"id": "simulated_exchange", "type": "written_interaction", "prompt_ar": "أكمل تبادلًا خياليًا: رد، اسأل، أكد، واقفل.", "real_network": False, "store_responses": False, "model_hidden": True},
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L09",
        MASTERY,
        {
            "comprehension": "The incoming request and missing detail are identified correctly.",
            "outcome_performance": "Reply, question, confirmation, and closing complete the exchange accurately.",
            "context_transfer": "The learner adapts to a changed request and field without copying the model.",
            "control_or_repair": "A written detail is confirmed or repaired without changing its value.",
        },
        "اشرح إزاي رسالة صحيحة في القواعد ممكن تبقى رد غير مناسب، وادّي مثال قصير.",
        [
            {"when": "next day", "task": "Reply to a changed two-detail request."},
            {"when": "three days", "task": "Ask for and confirm a missing fictional detail."},
            {"when": "seven days", "task": "Complete a fresh four-move written exchange."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L09",
        "Coach one simulated written exchange without composing messages for the learner.",
        "Hi! What's your name, and where are you from?",
        "اقرأ المطلوب ورد بمعلومات خيالية، ثم اسأل عن التفصيلة الناقصة.",
        ["Reply omits a requested detail", "Question asks for an already supplied detail", "Confirmation changes spelling or value"],
        ["No real accounts or personal details.", "Do not introduce new grammar.", "Do not supply a complete replacement message before retry."],
        turn_limit=8,
    ),
    "scene": "A safe simulated class-message interface with fictional participants. The teacher is concise and adult, focusing on message purpose and accuracy rather than social-media performance.",
    "sample_context": "One Egyptian-Arabic teacher explains written request, reply, follow-up, confirmation, and close. Read General American English naturally as message text. No real account or learner interaction occurs in the video; the simulation starts afterward.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {"schema_version": 2, "accent": "General American", "usage": "Synthesis reference only; no pronunciation target is assessed.", "entries": [{"text": "Can you spell your last name, please?", "ipa": "/kæn ju spɛl jɚ læst neɪm pliːz/"}], "curriculum_target_ids": []},
    "asset_briefs": """# U1-L09 Asset Briefs

Use an offline simulated message thread with fictional identities and explicit message
purpose labels in practice only. Support keyboard navigation, screen readers, RTL/LTR
text, non-colour status, and no network requests or retained content. Fresh mastery
must hide complete frames and use a changed request.
""",
    "video_readme": video_readme("U1-L09", "Exchange Details in Writing"),
}
