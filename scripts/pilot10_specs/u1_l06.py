from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l06_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l06.written_personal_detail_location",
    "critical_meaning": "Each requested detail is copied from the correct person and field without transposition.",
    "primary": {
        "scenario_en": "You check a fictional member card before a class.",
        "scenario_ar": "تراجع بطاقة عضو خيالية قبل محاضرة.",
        "prompt_en": "Find the requested first name, last name, nationality, address, and phone number.",
        "required": ["first_name", "last_name", "nationality", "address", "phone_number"],
        "support": "Requested field labels only; no highlighting or answer-bearing translation.",
        "freshness": "The layout, person, values, and field order differ from practice.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "You locate details in a fictional volunteer profile written as short prose.",
        "scenario_ar": "تبحث عن بيانات في نبذة قصيرة لمتطوع خيالي.",
        "prompt_en": "Retrieve the same five detail types from the changed layout.",
        "required": ["first_name", "last_name", "nationality", "address", "phone_number"],
        "support": "Requested field labels only; no highlighting or answer-bearing translation.",
        "freshness": "A prose layout and new values test location rather than table memorisation.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L06",
    "goal_ar": "أن تجد البيانات الشخصية المطلوبة في بطاقة أو نبذة قصيرة من غير ترجمة كل النص.",
    "scope": {
        "required_fields": ["name", "age", "nationality", "address", "phone", "email", "date of birth"],
        "performance": "retrieve requested values from two changed layouts",
        "time_hypothesis_minutes": "20-30",
    },
    "teach_back_summary": "Explain why a correct value from the wrong field is still incorrect.",
    "non_goals": ["Writing a form", "Translating the full profile", "Using real personal data"],
    "prerequisites": ["U1-L05"],
    "bounded_scope_notes": [
        "Recognise personal-detail labels and retrieve the value attached to each one.",
        "Distinguish first name, last name, address, and email address.",
        "Preserve left-to-right order in English names, email addresses, and numbers.",
    ],
    "not_yet": ["form completion", "free profile writing", "complex document navigation"],
    "content": {
        "situation": {"title_ar": "موقف اليوم", "prompt_ar": "تحتاج معلومة محددة من بطاقة عضو خيالية.", "success_ar": "تجد القيمة الصحيحة من الخانة الصحيحة من غير ترجمة النص كله."},
        "model": {
            "profile": {"name": "Lina Haddad", "age": 29, "nationality": "Syrian", "address": "12 Green Street, Amman", "email": "lina.haddad@example.com"},
            "gist_question_ar": "ما أنواع المعلومات الموجودة؟",
            "gist_answer": ["name", "age", "nationality", "address", "email"],
        },
        "notice": [
            {"label": "First name", "meaning_ar": "الاسم الأول"},
            {"label": "Last name", "meaning_ar": "اسم العائلة"},
            {"label": "Address", "meaning_ar": "العنوان"},
            {"label": "Email address", "meaning_ar": "البريد الإلكتروني"},
            {"label": "Date of birth", "meaning_ar": "تاريخ الميلاد"},
        ],
        "explanation_ar": [
            "ابدأ بالخانة المطلوبة لا ببداية النص.",
            "القيمة الصحيحة من الخانة الخطأ لا تحقق المهمة.",
            "اقرأ القيم الإنجليزية من اليسار لليمين وحافظ على ترتيبها.",
            "غيّر استراتيجية البحث عندما يتحول الجدول إلى نبذة، ولا تحفظ مكانًا ثابتًا.",
        ],
        "toolkit": {"identity": ["name", "first name", "last name", "nationality"], "contact": ["address", "phone number", "email address"], "date": ["age", "date of birth"]},
        "pronunciation": [],
    },
    "activities": [
        {"id": "label_meaning", "type": "match", "prompt_ar": "طابق اسم الخانة بنوع المعلومة.", "pairs": [["First name", "given name"], ["Last name", "family name"], ["Email address", "email"]]},
        {"id": "field_value", "type": "lookup", "prompt_ar": "اقرأ الخانة المطلوبة ثم اختر القيمة الملاصقة لها.", "layout": "fictional_card", "answer_reveal_after_attempt": True},
        {"id": "wrong_row_repair", "type": "edit", "prompt_ar": "أصلح إجابات مأخوذة من صف صحيح لكن خانة خاطئة.", "critical_rule": "field-value alignment"},
        {"id": "changed_layout", "type": "lookup", "prompt_ar": "استخرج خمس بيانات من نبذة قصيرة غير مرتبة كجدول.", "layout": "short_prose", "model_hidden": True},
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L06",
        MASTERY,
        {
            "comprehension": "Each requested label is understood as the intended detail type.",
            "outcome_performance": "All five values are located and copied accurately.",
            "context_transfer": "The learner succeeds in a new layout without fixed-position cues.",
            "control_or_repair": "A field-value mismatch is detected and corrected.",
        },
        "اشرح ليه قيمة صحيحة من سطر غلط تعتبر إجابة غير صحيحة.",
        [
            {"when": "next day", "task": "Find three details in a new card."},
            {"when": "three days", "task": "Separate first and last name in a changed profile."},
            {"when": "seven days", "task": "Retrieve five details from a prose layout."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L06",
        "Coach field-directed reading without translating or highlighting the answer.",
        "Find the field first, then read only its value.",
        "حدّد اسم الخانة أولًا، وبعدها ابحث عن قيمتها.",
        ["Value taken from the wrong field", "Name order reversed", "Unrequested full-text translation"],
        ["Do not reveal the answer location before the attempt.", "Use fictional data only.", "Do not turn lookup into profile writing."],
    ),
    "scene": "A clean adult membership-card workspace with two fictional layouts. The mood is focused and low-pressure, with the teacher demonstrating visual search rather than reading every line aloud.",
    "sample_context": "One Egyptian-Arabic teacher for adult A1 readers. English field labels are pronounced clearly in General American inside the video. Explain left-to-right value order and field-value alignment. Do not ask learner questions during the video.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {"schema_version": 2, "accent": "General American", "usage": "Production direction only; no pronunciation target is assessed in this lesson.", "entries": [{"text": "email address", "ipa": "/ˈiːmeɪl ˈædrɛs/"}, {"text": "date of birth", "ipa": "/deɪt əv bɝθ/"}], "curriculum_target_ids": []},
    "asset_briefs": """# U1-L06 Asset Briefs

Create two fictional profiles: a labelled card and a short-prose layout. Use real text,
not generated text inside images. Preserve visible keyboard focus and explicit reading
direction. Labels, not colour or position alone, identify fields. Never use a real
person's name, address, phone number, or email.
""",
    "video_readme": video_readme("U1-L06", "Find Personal Details"),
}
