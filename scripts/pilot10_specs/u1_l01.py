from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l01_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l01.basic_social_exchange",
    "critical_meaning": "The partner can recognise the opening, wellbeing response, fitting reaction, and close.",
    "primary": {
        "scenario_en": "You meet a new person before an evening class.",
        "scenario_ar": "تقابل شخص جديد قبل محاضرة مسائية.",
        "prompt_en": "Start the conversation, ask how the person is, react, and close.",
        "required": ["greeting", "wellbeing_question", "fitting_reaction", "closing"],
        "support": "Situation icon only; no dialogue, sentence frame, or answer-bearing model.",
        "freshness": "The time, partner, and reported feeling differ from practice.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "You meet a new volunteer at a community centre.",
        "scenario_ar": "تقابل متطوع جديد في مركز مجتمعي.",
        "prompt_en": "Open a short conversation, respond to how the person feels, and say goodbye.",
        "required": ["greeting", "wellbeing_question", "fitting_reaction", "closing"],
        "support": "Situation icon only; no dialogue, sentence frame, or answer-bearing model.",
        "freshness": "A new partner and feeling make this equivalent but not repeated.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L01",
    "goal_ar": "أن تبدأ محادثة اجتماعية قصيرة، ترد بما يناسب المعنى، وتنهيها بشكل طبيعي.",
    "scope": {
        "required_moves": ["greeting", "wellbeing question", "fitting response", "closing"],
        "performance": "one fresh four-move exchange",
        "time_hypothesis_minutes": "20-30",
    },
    "teach_back_summary": "One short contrast between a fitting and mismatched reaction.",
    "non_goals": [
        "Exchanging personal details",
        "Memorising one fixed dialogue",
        "Diagnosing emotion from intonation alone",
        "Accent removal",
    ],
    "prerequisites": [],
    "bounded_scope_notes": [
        "Use a small greeting, wellbeing, feeling, reaction, and closing repertoire.",
        "Introduce I'm as a frequent heard and optional spoken contraction.",
        "Practise /θ/ and /ð/ only in selected high-value social words.",
    ],
    "not_yet": [
        "personal-detail questions",
        "full present-be paradigm explanation",
        "free discussion of emotions",
    ],
    "content": {
        "situation": {
            "title_ar": "موقف اليوم",
            "prompt_ar": "تقابل شخص لأول مرة في مجموعة دراسة وتريد بدء كلام بسيط.",
            "success_ar": "تبدأ، تسأل عن الحال، ترد بما يناسب، ثم تنهي الكلام.",
        },
        "model": {
            "roles": ["new learner", "group member"],
            "lines": [
                "Hi. How are you?",
                "I'm good, thanks. And you?",
                "I'm great, thank you.",
                "Bye. See you soon.",
            ],
            "gist_question_ar": "ما الحركات الثلاث الكبيرة في المحادثة؟",
            "gist_answer": ["opening", "wellbeing exchange", "closing"],
        },
        "notice": [
            {"chunk": "Hi / Hello", "meaning_ar": "بداية بسيطة"},
            {"chunk": "How are you?", "meaning_ar": "سؤال عن الحال"},
            {"chunk": "I'm fine, thanks.", "meaning_ar": "رد إيجابي"},
            {"chunk": "Oh, I'm sorry.", "meaning_ar": "رد متعاطف على خبر غير جيد"},
            {"chunk": "Bye / See you soon.", "meaning_ar": "إنهاء الكلام"},
        ],
        "explanation_ar": [
            "الرد المناسب أهم من طول الرد.",
            "استخدم And you? لإعادة السؤال للطرف الآخر.",
            "I'm اختصار طبيعي لـ I am، والشكلان مقبولان.",
            "نطق thanks وthat's يجب أن يظل مفهومًا؛ لا نطلب تغيير اللهجة.",
        ],
        "toolkit": {
            "greetings": ["Hi.", "Hello.", "Good morning."],
            "wellbeing": ["How are you?", "I'm fine, thanks.", "I'm okay.", "I'm tired."],
            "reactions": ["That's good.", "Oh, I'm sorry.", "And you?"],
            "closings": ["Goodbye.", "Bye.", "See you soon."],
        },
        "pronunciation": [
            {"focus": "thanks / that's", "tip_ar": "مكان اللسان قريب؛ الفرق في وجود الصوت."},
            {"focus": "I'm", "tip_ar": "اسمعها كوحدة واحدة بدل فصل الكلمتين."},
            {"focus": "question versus response", "tip_ar": "اجعل السؤال يطلب دورًا جديدًا بوضوح."},
        ],
    },
    "activities": [
        {
            "id": "exchange_shape",
            "type": "order",
            "prompt_ar": "رتّب الحركات، وليس حوارًا محفوظًا.",
            "items": ["closing", "wellbeing exchange", "greeting"],
            "answer": ["greeting", "wellbeing exchange", "closing"],
        },
        {
            "id": "fitting_reaction",
            "type": "choice_set",
            "prompt_ar": "اختر الرد الذي يناسب الخبر.",
            "items": [
                {"prompt": "I'm great.", "options": ["That's good.", "I'm sorry."], "answer": 0},
                {"prompt": "I'm tired.", "options": ["Oh, I'm sorry.", "Great!"], "answer": 0},
            ],
        },
        {
            "id": "choose_close",
            "type": "choice",
            "prompt_ar": "اختر جملة تنهي المحادثة.",
            "options": ["How are you?", "See you soon.", "I'm okay."],
            "answer": 1,
        },
        {
            "id": "guided_exchange",
            "type": "production",
            "prompt_ar": "ابدأ مع شخصية خيالية، اسأل عن حالها، رد على الخبر، ثم اقفل الكلام.",
            "support": ["greeting", "question", "reaction", "closing"],
            "model_hidden": True,
        },
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L01",
        MASTERY,
        {
            "comprehension": "The reaction matches the partner's stated feeling.",
            "outcome_performance": "All four social moves are present and intelligible.",
            "context_transfer": "The exchange fits the new class setting without reciting the model.",
            "control_or_repair": "A key unclear social word can be repeated or repaired.",
        },
        "اشرح ليه That's good لا تناسب شخص قال I'm tired، واذكر رد مناسب.",
        [
            {"when": "next day", "task": "Respond to a different feeling and close."},
            {"when": "three days", "task": "Open a morning exchange with a new partner."},
            {"when": "seven days", "task": "Complete a fresh four-move social exchange."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L01",
        "Coach one short social exchange without writing it for the learner.",
        "Hi! How are you?",
        "ابدأ ورد بشكل طبيعي، ويمكنك استخدام شخصية خيالية.",
        [
            "Missing greeting or closing",
            "Reaction contradicts the stated feeling",
            "Key social chunk is unintelligible and unrepaired",
        ],
        [
            "Stay within greetings, basic feelings, reactions, and closings.",
            "Do not ask for personal details.",
            "Accept intelligible accent variation in dental sounds and contours.",
        ],
    ),
    "scene": "A calm adult evening class reception area. One warm teacher guides a first-contact exchange; the atmosphere is practical, safe, and encouraging, never childish or theatrical.",
    "sample_context": "Single Egyptian-Arabic teacher for adult beginners. Explain a believable first meeting, model both sides with subtle delivery changes but never create a second speaker. English is clear General American. The video contains no learner interaction; practice starts afterward.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {
        "schema_version": 2,
        "accent": "General American",
        "usage": "Production reference; transcript IPA remains the synthesis control.",
        "entries": [
            {"text": "thanks", "ipa": "/θæŋks/", "director_hint": "audible voiceless dental start"},
            {"text": "that's", "ipa": "/ðæts/", "director_hint": "audible voiced dental start"},
            {"text": "I'm", "ipa": "/aɪm/", "director_hint": "one smooth beat"},
            {"text": "How are you?", "ipa": "/haʊ ɑr juː/", "director_hint": "friendly question contour"},
        ],
        "curriculum_target_ids": [
            "a1_pronunciation.dental_fricatives",
            "a1_pronunciation.frequent_contractions",
            "a1_pronunciation.question_social_contours",
        ],
    },
    "asset_briefs": """# U1-L01 Asset Briefs

## Visuals

- Adult evening-class entrance with two neutral fictional learner cards.
- Four move icons: greeting, wellbeing, reaction, closing.
- Feeling cards for good, okay, tired, and sad; labels carry the meaning, not colour.

## Audio and accessibility

Use one teacher for explanation and model roles. Keep role changes subtle. Provide
captions, transcript, pause, replay, keyboard access, and reduced motion. Do not use
photos implying that a real person's emotional state was inferred from their face.
""",
    "video_readme": video_readme("U1-L01", "Start and End a Conversation"),
}
