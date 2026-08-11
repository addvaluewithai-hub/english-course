from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l05_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l05.spoken_contact_detail_capture",
    "critical_meaning": "Name, age, phone digits, and day are preserved without transposition or guessing.",
    "primary": {
        "scenario_en": "A fictional club member leaves a contact voice message.",
        "scenario_ar": "عضو خيالي في نادٍ يترك رسالة ببيانات التواصل.",
        "prompt_en": "Record the name, age, phone number, and available day from the message.",
        "required": ["name", "age_0_100", "phone_digit_order", "day_of_week"],
        "support": "Two full plays and blank labels only; no transcript, digits, or answer-bearing waveform.",
        "freshness": "All details, voice, grouping, teen/ty contrast, and day differ from practice.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "A fictional course applicant leaves changed contact details.",
        "scenario_ar": "متقدم خيالي لدورة يترك بيانات مختلفة.",
        "prompt_en": "Capture the new name, age, phone number, and day accurately.",
        "required": ["name", "age_0_100", "phone_digit_order", "day_of_week"],
        "support": "Two full plays and blank labels only; no transcript, digits, or answer-bearing waveform.",
        "freshness": "New speaker, values, grouping, and day preserve the construct without repeating answers.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L05",
    "goal_ar": "أن تسجل اسم وعمر ورقم هاتف ويوم من رسالة صوتية جديدة بدقة.",
    "scope": {
        "required_details": ["name", "number 0-100", "phone number", "day"],
        "performance": "two listens with optional repair, no transcript",
        "time_hypothesis_minutes": "30-40",
    },
    "teach_back_summary": "Explain why thirteen/thirty or grouped phone digits can change recorded meaning.",
    "non_goals": ["Arithmetic", "Large numbers", "Fast dictation", "Real phone-number collection"],
    "prerequisites": ["U1-L04"],
    "bounded_scope_notes": [
        "Retrieve numbers 0-100; preserve individual digit order in phone numbers.",
        "Recognise and retrieve all seven day names in a fresh contact message.",
        "Use grouping, selected high-vowel contrasts, and teen/ty stress only to preserve key detail.",
        "Recycle spelling, repair, and selected dental sounds in names, three, and Thursday.",
    ],
    "not_yet": ["dates and months", "prices and arithmetic", "unrestricted fast number strings"],
    "content": {
        "situation": {
            "title_ar": "موقف اليوم",
            "prompt_ar": "رسالة صوتية تعطي اسمًا وعمرًا ورقم هاتف ويومًا مناسبًا.",
            "success_ar": "تسجل كل تفصيلة في خانتها وبنفس الترتيب.",
        },
        "model": {
            "speaker": "Sara Khalil",
            "fields": {"age": 30, "phone": "555-01-19", "day": "Thursday"},
            "gist_question_ar": "ما أنواع التفاصيل الأربع؟",
            "gist_answer": ["name", "age", "phone", "day"],
        },
        "notice": [
            {"chunk": "My name is …", "field": "name"},
            {"chunk": "I'm thirty.", "field": "age"},
            {"chunk": "My phone number is …", "field": "phone"},
            {"chunk": "Call me on Thursday.", "field": "day"},
        ],
        "explanation_ar": [
            "رقم الهاتف يُسجل رقمًا رقمًا؛ العدد الآخر يُفهم كوحدة.",
            "قسّم الأرقام الطويلة إلى مجموعات قصيرة من غير تغيير ترتيبها.",
            "في teen/ty استمع للكلمة كاملة والنبر، ثم اطلب تأكيدًا عند الشك.",
            "zero وoh قد يعنيان صفرًا في رقم الهاتف.",
        ],
        "toolkit": {
            "digits": ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
            "number_landmarks": ["thirteen/thirty", "fifteen/fifty", "forty-two", "one hundred"],
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "repair": ["Can you spell that?", "Please say that again.", "Thirteen or thirty?"],
        },
        "pronunciation": [
            {"focus": "grouping", "tip_ar": "قسّم الهاتف إلى مجموعات مسموعة قصيرة."},
            {"focus": "teen versus ty", "tip_ar": "استمع لمكان الجزء الأوضح وطول الصوت الأخير."},
            {"focus": "three / six", "tip_ar": "حافظ على وضوح الرقم واصلحه لو فُهم كرقم آخر."},
            {"focus": "phone number", "tip_ar": "اسمع العبارة كوحدة مع وضوح الكلمة الأولى."},
        ],
    },
    "activities": [
        {"id": "teen_ty", "type": "listening_choice", "prompt_ar": "اختر العدد المسموع.", "contrasts": [["thirteen", "thirty"], ["fifteen", "fifty"]]},
        {"id": "number_range", "type": "dictation", "prompt_ar": "سجل أعدادًا جديدة من صفر إلى مئة.", "items": [6, 13, 30, 42, 50, 100]},
        {"id": "phone_grouping", "type": "capture", "prompt_ar": "اسمع مجموعات هاتف واكتب كل رقم بالترتيب.", "transcript_hidden": True},
        {"id": "day_match", "type": "listening_choice", "prompt_ar": "اختر اليوم المذكور من أيام متجاورة.", "transcript_hidden": True},
        {"id": "guided_contact_capture", "type": "listening_capture", "prompt_ar": "اسمع رسالة خيالية وسجل الاسم والعمر والهاتف واليوم.", "fields": ["name", "age", "phone", "day"], "model_hidden": True},
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L05",
        MASTERY,
        {
            "comprehension": "Each heard detail is assigned to the correct field.",
            "outcome_performance": "Name, age, every phone digit, and day are accurate.",
            "context_transfer": "Changed grouping and a new teen/ty value are handled without a transcript.",
            "control_or_repair": "Uncertain key detail is replayed or checked rather than guessed.",
        },
        "اشرح الفرق بين تسجيل رقم هاتف وفهم عدد مثل forty-two، واذكر طريقة تأكد واحدة.",
        [
            {"when": "next day", "task": "Capture a changed phone number and day."},
            {"when": "three days", "task": "Distinguish a new teen/ty age pair."},
            {"when": "seven days", "task": "Capture all four fields from a new voice message."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L05",
        "Coach accurate contact-detail listening and repair without revealing the transcript.",
        "Listen once for the fields and once for the exact details.",
        "اسمع مرة لنوع الخانات ومرة للقيم الدقيقة.",
        ["Digit order changes", "Teen/ty number changes", "Wrong day selected", "Unheard detail is guessed"],
        ["Do not expose real phone numbers.", "Do not turn the task into arithmetic.", "Accept pronunciation variation unless a key number or day is lost."],
    ),
    "scene": "A quiet adult learning desk with a fictional voice message and blank contact card. The mood is focused and practical; accuracy matters, but the teacher remains patient and non-alarmist.",
    "sample_context": "One Egyptian-Arabic teacher models contact-detail listening. English uses clear General American at a natural A1 pace, with honest grouping and teen/ty contrast. The teacher may model both a message and repair, but asks the learner nothing during the video.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {
        "schema_version": 2,
        "accent": "General American",
        "usage": "Meaning-preserving reference; request repair only when a key detail changes.",
        "entries": [
            {"text": "phone number", "ipa": "/ˈfoʊn ˌnʌmbɚ/", "director_hint": "familiar compound chunk"},
            {"text": "three / six", "ipa": "/θriː/ /sɪks/", "director_hint": "keep key vowel categories clear"},
            {"text": "thirteen / thirty", "ipa": "/ˌθɝˈtiːn/ /ˈθɝti/", "director_hint": "final versus first prominence"},
            {"text": "Thursday", "ipa": "/ˈθɝzdeɪ/", "director_hint": "clear day as a whole"},
        ],
        "curriculum_target_ids": [
            "a1_pronunciation.name_number_segmentation",
            "a1_pronunciation.high_vowel_contrasts",
            "a1_pronunciation.teen_ty_stress",
            "a1_pronunciation.compound_chunk_stress",
            "a1_pronunciation.spelling_sound_verification",
            "a1_pronunciation.dental_fricatives",
        ],
    },
    "asset_briefs": """# U1-L05 Asset Briefs

Use fictional audio cards and four labelled fields: name, age, phone, day. Visual number
groups must preserve order without revealing answers before listening. Provide replay,
speed-neutral repeat, captions for the explanation only, accessible post-attempt text,
keyboard entry, and no storage of real names or phone numbers.
""",
    "video_readme": video_readme("U1-L05", "Hear Names and Phone Numbers"),
}
