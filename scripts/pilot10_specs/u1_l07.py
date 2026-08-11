from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l07_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l07.simple_form_completion",
    "critical_meaning": "Every required fictional value is entered under the matching field and survives review.",
    "primary": {
        "scenario_en": "You register a fictional learner for a community class in a simulated form.",
        "scenario_ar": "تسجّل متعلمًا خياليًا في دورة مجتمعية داخل نموذج محاكي.",
        "prompt_en": "Enter the required values, choose country and nationality, check, and submit.",
        "required": ["first_name", "last_name", "country", "nationality", "date_of_birth", "email", "review_before_submit"],
        "support": "Field labels and interface instructions only; no prefilled answers.",
        "freshness": "The person, layout, field order, month, and selection controls differ from practice.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "You complete a simulated volunteer form for a different fictional person.",
        "scenario_ar": "تكمل نموذج تطوع محاكي لشخص خيالي مختلف.",
        "prompt_en": "Transfer the same detail types, check the new layout, and submit.",
        "required": ["first_name", "last_name", "country", "nationality", "date_of_birth", "email", "review_before_submit"],
        "support": "Field labels and interface instructions only; no prefilled answers.",
        "freshness": "New values and controls preserve the construct without repeating the first form.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L07",
    "goal_ar": "أن تنقل بيانات خيالية إلى نموذج بسيط، تنفذ التعليمات، وتراجع قبل الإرسال.",
    "scope": {"required_actions": ["enter", "select", "choose", "check", "submit"], "performance": "one fresh simulated form", "time_hypothesis_minutes": "25-35"},
    "teach_back_summary": "Explain the difference between a field label, a value, and an action instruction.",
    "non_goals": ["Real registration", "Passwords or payment data", "Complex account creation"],
    "prerequisites": ["U1-L04", "U1-L06"],
    "bounded_scope_notes": [
        "Recognise common fields and execute enter, choose/select, check, and submit in a simulation.",
        "Retrieve and write the required month in a fresh date.",
        "Recycle country versus nationality and ask for one missing detail when needed.",
        "Use digital-object vocabulary only to understand the simple task environment.",
    ],
    "not_yet": ["real account credentials", "payment submission", "complex validation errors"],
    "content": {
        "situation": {"title_ar": "موقف اليوم", "prompt_ar": "تنقل بيانات شخصية خيالية من بطاقة إلى نموذج محاكي.", "success_ar": "كل قيمة في خانتها، والتعليمات منفذة، والمراجعة تمت قبل الإرسال."},
        "model": {
            "person": "Maya Hassan",
            "fields": {"first_name": "Maya", "last_name": "Hassan", "country": "Jordan", "nationality": "Jordanian", "date_of_birth": "14 March 1997"},
            "gist_question_ar": "ما الفرق بين اسم الخانة والتعليمة والقيمة؟",
            "gist_answer": ["field tells what", "instruction tells action", "value is entered data"],
        },
        "notice": [
            {"chunk": "Enter your first name.", "action": "type value"},
            {"chunk": "Select your nationality.", "action": "choose from list"},
            {"chunk": "Check your details.", "action": "review"},
            {"chunk": "Submit the form.", "action": "send simulated form"},
        ],
        "explanation_ar": [
            "عنوان الخانة يحدد نوع المعلومة، والتعليمة تحدد الفعل، والقيمة هي ما تضعه.",
            "البلد والجنسية قيمتان مرتبطتان لكنهما ليستا الخانة نفسها.",
            "راجع اكتمال الخانات وصحة النوع وترتيب الأرقام والتاريخ.",
            "استخدم بيانات خيالية ولا تدخل كلمة سر أو بطاقة حقيقية في التدريب.",
        ],
        "toolkit": {
            "objects": ["phone", "computer", "laptop", "screen", "website"],
            "actions": ["enter", "write", "choose", "select", "click", "check", "complete", "submit"],
            "fields": ["first name", "last name", "country", "nationality", "email", "date of birth"],
            "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        },
        "pronunciation": [],
    },
    "activities": [
        {"id": "action_meaning", "type": "match", "prompt_ar": "طابق التعليمة بالفعل المطلوب.", "pairs": [["Enter", "type"], ["Select", "choose"], ["Check", "review"], ["Submit", "send"]]},
        {"id": "month_capture", "type": "choice_set", "prompt_ar": "اختر الشهر المكتوب أو المسموع في تواريخ جديدة.", "months_required": 12},
        {"id": "field_transfer", "type": "simulated_form", "prompt_ar": "انقل بيانات شخصية خيالية إلى الخانات المناسبة.", "store_responses": False},
        {"id": "swapped_fields", "type": "edit", "prompt_ar": "أصلح البلد والجنسية والاسم الأول واسم العائلة إذا تبدلت.", "answer_reveal_after_attempt": True},
        {"id": "pre_submit_check", "type": "checklist", "prompt_ar": "راجع الاكتمال والنوع والترتيب ثم أرسل المحاكاة.", "submit_is_simulated": True},
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L07",
        MASTERY,
        {
            "comprehension": "Field labels and action prompts are interpreted correctly.",
            "outcome_performance": "All required values are entered accurately and submitted after review.",
            "context_transfer": "A changed layout and month are handled without fixed-position memory.",
            "control_or_repair": "A missing or swapped field is found and corrected before submit.",
        },
        "اشرح الفرق بين Enter your first name وSelect your nationality، وليه المراجعة قبل Submit مهمة.",
        [
            {"when": "next day", "task": "Complete four fields in a changed layout."},
            {"when": "three days", "task": "Repair swapped country and nationality values."},
            {"when": "seven days", "task": "Complete and check a fresh simulated form."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L07",
        "Coach simulated form completion without entering or retaining data for the learner.",
        "Read the first instruction and tell me which field it controls.",
        "اقرأ أول تعليمة وحدد الخانة قبل إدخال قيمة خيالية.",
        ["Value entered under wrong field", "Country and nationality swapped", "Submit before required review"],
        ["Use simulated fictional data only.", "Never request or store passwords, card numbers, or real contact details.", "Do not complete the form for the learner."],
        turn_limit=8,
    ),
    "scene": "A clean simulated registration screen on an adult learner's laptop. The teacher is calm and procedural. The interface contains fictional data and no commercial urgency or payment cues.",
    "sample_context": "One Egyptian-Arabic teacher explains a safe simulated form. General American English prompts are clear and natural. Model field, action, and value distinctions. Do not ask the learner to act during the video and never imply that real details are required.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {"schema_version": 2, "accent": "General American", "usage": "Production direction only; no pronunciation target is assessed.", "entries": [{"text": "Enter", "ipa": "/ˈɛntɚ/"}, {"text": "Select", "ipa": "/səˈlɛkt/"}, {"text": "Submit", "ipa": "/səbˈmɪt/"}], "curriculum_target_ids": []},
    "asset_briefs": """# U1-L07 Asset Briefs

Build a simulated form with semantic labels, explicit errors, keyboard focus, and a
non-networked submit action. Use real rendered text rather than text inside images.
Provide RTL/LTR handling, accessible error summaries, and no fields for passwords,
payment cards, or real participant data.
""",
    "video_readme": video_readme("U1-L07", "Complete a Simple Form"),
}
