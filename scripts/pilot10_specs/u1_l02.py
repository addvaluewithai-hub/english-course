from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l02_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l02.spoken_introduction_comprehension",
    "critical_meaning": "Required personal details are recovered and attributed to the correct person.",
    "primary": {
        "scenario_en": "A new member sends a short voice introduction to a study group.",
        "scenario_ar": "عضو جديد يرسل تقديم صوتي قصير لمجموعة دراسة.",
        "prompt_en": "Listen without a transcript and record the person's name and three details.",
        "required": ["correct_person", "name", "three_personal_details"],
        "support": "Two complete plays and blank field labels only; no transcript or answer-bearing image.",
        "freshness": "The voice, person, places, role, and detail order differ from all models.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "A colleague introduces a new fictional teammate in a voice note.",
        "scenario_ar": "زميل يقدّم عضو فريق خيالي جديد في رسالة صوتية.",
        "prompt_en": "Listen without a transcript and identify the person and three facts.",
        "required": ["correct_person", "name", "three_personal_details"],
        "support": "Two complete plays and blank field labels only; no transcript or answer-bearing image.",
        "freshness": "A third-person introduction changes speaker, referent, and all details.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L02",
    "goal_ar": "أن تفهم تقديم صوتي جديد وتلتقط المعلومات الأساسية من غير نص مكتوب.",
    "scope": {
        "required_details": ["person", "name", "three personal facts"],
        "performance": "two full listens without transcript",
        "time_hypothesis_minutes": "20-30",
    },
    "teach_back_summary": "Explain how I, he, or she identifies whose information follows.",
    "non_goals": [
        "Producing a complete self-introduction",
        "Understanding every word",
        "Fast reduced speech",
        "Full productive control of all personal pronouns",
    ],
    "prerequisites": ["U1-L01"],
    "bounded_scope_notes": [
        "Introduce present be in clear identity, state, role, and location chunks.",
        "Use I, he, and she to establish reference; other pronouns remain supported exposure.",
        "Recognise I'm, he's, and she's in slow connected speech.",
        "Recognise country, city, and familiar place labels as information types.",
    ],
    "not_yet": [
        "full pronoun paradigm production",
        "present-simple third-person instruction",
        "unsupported fast or noisy listening",
    ],
    "content": {
        "situation": {
            "title_ar": "موقف اليوم",
            "prompt_ar": "تسمع رسالة صوتية من عضو جديد وتحتاج معرفة الشخص وأهم تفاصيله.",
            "success_ar": "تعرف الشخص وتستخرج ثلاث معلومات من غير ترجمة كل كلمة.",
        },
        "model": {
            "speaker": "Alex",
            "lines": [
                "Hi. I'm Alex.",
                "I'm from Canada.",
                "I live in Cairo.",
                "I'm an engineer.",
            ],
            "gist_question_ar": "من الشخص، وما أنواع المعلومات التي قالها؟",
            "gist_answer": ["Alex", "origin", "residence", "role"],
        },
        "notice": [
            {"chunk": "I'm Alex.", "meaning_ar": "المتكلم يذكر اسمه", "referent": "I"},
            {"chunk": "He's from Egypt.", "meaning_ar": "المعلومة عن رجل مذكور", "referent": "he"},
            {"chunk": "She's a teacher.", "meaning_ar": "المعلومة عن امرأة مذكورة", "referent": "she"},
            {"chunk": "country / city", "meaning_ar": "نوع المكان المطلوب"},
        ],
        "explanation_ar": [
            "في السماع الأول التقط الشخص والموضوع، وفي الثاني التقط التفاصيل.",
            "I تعني أن المتكلم يتحدث عن نفسه؛ he وshe يربطان المعلومة بشخص مذكور.",
            "I'm وhe's وshe's اختصارات شائعة يجب التعرف عليها كوحدة.",
            "وجود معلومة صحيحة مع الشخص الخطأ يُعد خطأ معنى أساسي.",
        ],
        "toolkit": {
            "self_signals": ["I'm …", "I'm from …", "I'm in …"],
            "other_person_signals": ["This is …", "He's …", "She's …"],
            "detail_types": ["name", "country", "city", "job"],
        },
        "pronunciation": [
            {"focus": "I'm", "tip_ar": "اسمعها كوحدة واحدة تدل على I am."},
            {"focus": "he's / she's", "tip_ar": "الصوت الأخير جزء من is هنا، وليس كلمة جديدة."},
        ],
    },
    "activities": [
        {
            "id": "gist_before_detail",
            "type": "two_pass_listening",
            "prompt_ar": "في المرة الأولى اختر الشخص والموضوع؛ في الثانية املأ التفاصيل.",
            "first_pass_fields": ["person", "topic"],
            "second_pass_fields": ["name", "origin", "location", "role"],
            "transcript_hidden": True,
        },
        {
            "id": "referent_match",
            "type": "choice_set",
            "prompt_ar": "لمن تخص المعلومة؟",
            "items": [
                {"prompt": "I'm from Canada.", "options": ["speaker", "Omar"], "answer": 0},
                {"prompt": "This is Omar. He's a student.", "options": ["speaker", "Omar"], "answer": 1},
            ],
        },
        {
            "id": "contraction_meaning",
            "type": "match",
            "prompt_ar": "طابق الاختصار بالمعنى الكامل.",
            "pairs": [["I'm", "I am"], ["He's", "He is"], ["She's", "She is"]],
        },
        {
            "id": "guided_fresh_listen",
            "type": "listening_capture",
            "prompt_ar": "اسمع رسالة جديدة مرتين وسجل الاسم وثلاث تفاصيل.",
            "fields": ["name", "detail_1", "detail_2", "detail_3"],
            "transcript_hidden": True,
            "answer_reveal_after_attempt": True,
        },
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L02",
        MASTERY,
        {
            "comprehension": "The correct person and requested detail types are understood.",
            "outcome_performance": "The name and three essential facts are recovered accurately.",
            "context_transfer": "Details are captured from a new voice and changed order without a transcript.",
            "control_or_repair": "A second full listen is used without guessing or changing attribution.",
        },
        "اشرح إزاي I وhe وshe بيساعدوك تعرف المعلومة تخص مين.",
        [
            {"when": "next day", "task": "Capture three facts from a new self-introduction."},
            {"when": "three days", "task": "Identify the referent in a third-person introduction."},
            {"when": "seven days", "task": "Complete a new two-pass introduction capture."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L02",
        "Coach listening strategy and attribution without revealing the transcript before the attempt.",
        "Listen to this introduction once for the person, then once for details.",
        "اسمع أول مرة للشخص، والمرة الثانية للتفاصيل.",
        [
            "Required detail attributed to the wrong person",
            "Guessing an unheard place or role",
            "Transcript or complete answer requested before the attempt",
        ],
        [
            "Do not require spoken production of the full pronoun paradigm.",
            "Do not reveal the transcript before the listening attempt ends.",
            "Keep voices clear and connected, not word-by-word dictation.",
        ],
    ),
    "scene": "A quiet adult study-group chat viewed as a voice-message moment. The teacher is calm and analytical, helping the learner listen for people and details without turning the scene into a grammar lecture.",
    "sample_context": "One Egyptian-Arabic teacher for adult A1 learners. Model self-introduction and third-person introduction with the same teacher voice and subtle role shifts. Use clear General American English, natural contractions, and two-pass listening strategy. No learner questions occur inside the video.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {
        "schema_version": 2,
        "accent": "General American",
        "usage": "Production reference; accept intelligible stable varieties.",
        "entries": [
            {"text": "I'm", "ipa": "/aɪm/", "director_hint": "one smooth beat"},
            {"text": "he's", "ipa": "/hiːz/", "director_hint": "clear final z"},
            {"text": "she's", "ipa": "/ʃiːz/", "director_hint": "clear sh and final z"},
        ],
        "curriculum_target_ids": ["a1_pronunciation.frequent_contractions"],
    },
    "asset_briefs": """# U1-L02 Asset Briefs

## Visuals

- Fictional voice-message cards with no waveform-only meaning.
- Person, country, city, and role field icons.
- A referent line connecting I to the speaker and he/she to a named fictional person.

## Audio and accessibility

Provide separate fresh audio clips for practice and mastery. Never show the transcript
before the scored capture. Captions remain available on the explanation video, while
the listening task has replay controls and an accessible post-attempt transcript.
""",
    "video_readme": video_readme("U1-L02", "Understand an Introduction"),
}
