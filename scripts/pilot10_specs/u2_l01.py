from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u2_l01_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u2.l01.family_talk_comprehension",
    "critical_meaning": "Each relationship, name, and basic fact is attributed to the correct fictional person.",
    "primary": {
        "scenario_en": "A fictional classmate describes three people in a slow voice message.",
        "scenario_ar": "زميل خيالي يصف ثلاثة أشخاص في رسالة صوتية بطيئة.",
        "prompt_en": "Choose the correct people map and record two facts about each named person.",
        "required": ["three_correct_people", "relationships_or_people_words", "two_facts_each", "correct_attribution"],
        "support": "Two full plays and unlabeled fictional people visuals only; no transcript or answer labels.",
        "freshness": "New people, relationships, descriptions, pets, order, and voice differ from all models.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "A fictional neighbour describes a different small family group.",
        "scenario_ar": "جار خيالي يصف مجموعة عائلية مختلفة.",
        "prompt_en": "Select the new people map and record two facts for each person.",
        "required": ["three_correct_people", "relationships_or_people_words", "two_facts_each", "correct_attribution"],
        "support": "Two full plays and unlabeled fictional people visuals only; no transcript or answer labels.",
        "freshness": "Different relationships, descriptions, quantities, and order preserve the listening construct.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U2-L01",
    "goal_ar": "أن تفهم وصفًا صوتيًا بسيطًا لأشخاص أو عائلة وتنسب كل حقيقة للشخص الصحيح.",
    "scope": {"required_capture": ["person or relationship", "name", "two basic facts"], "performance": "three-person slow conversation or message without transcript", "time_hypothesis_minutes": "30-40"},
    "teach_back_summary": "Explain how a new relationship or name starts a new person card.",
    "non_goals": ["Personal family disclosure", "Judging personality from appearance", "Detailed physical description", "Fast multi-speaker audio"],
    "prerequisites": ["U1-L08"],
    "bounded_scope_notes": [
        "Introduce basic people words and evidence-supported appearance or manner descriptions for identification.",
        "Recycle only task-provided or voluntary family and personal-life vocabulary.",
        "Use /f/-/v/ and selected front/central vowels only where a key person, family word, or number could change.",
    ],
    "not_yet": ["free family interview", "detailed appearance production", "personality inference", "fast overlapping talk"],
    "content": {
        "situation": {"title_ar": "موقف اليوم", "prompt_ar": "تسمع شخصًا يصف أفرادًا خياليين وتحتاج ترتيب الحقائق.", "success_ar": "كل علاقة واسم ووصف أو عمل يظل مع صاحبه الصحيح."},
        "model": {
            "family_size": 5,
            "people": [
                {"relationship": "mother", "name": "Huda", "facts": ["doctor", "friendly"]},
                {"relationship": "brother", "name": "Karim", "facts": ["tall and quiet", "has a dog"]},
            ],
            "gist_question_ar": "من الشخصان المذكوران وما حقيقتان عن كل واحد؟",
        },
        "notice": [
            {"signal": "This is my mother.", "action": "open mother card"},
            {"signal": "Her name is Huda.", "action": "attach name to mother"},
            {"signal": "This is my brother Karim.", "action": "open brother card"},
            {"signal": "He's tall and quiet.", "action": "attach descriptions to Karim"},
        ],
        "explanation_ar": [
            "افتح بطاقة ذهنية جديدة عند علاقة أو اسم جديد.",
            "استخدم person/people وman/men وchild/children عندما لا تُذكر علاقة محددة.",
            "لا تستنتج صفات الشخصية من الصورة؛ اعتمد على ما قيل أو ظهر بوضوح في المهمة.",
            "اطلب في كل استماع اسمًا أو علاقة ثم حقيقتين، بدل مطاردة كل كلمة.",
        ],
        "toolkit": {
            "people": ["person", "people", "man", "woman", "adult", "child", "children"],
            "relationships": ["mother", "father", "brother", "sister", "cousin", "grandparent", "partner"],
            "descriptions": ["tall", "short", "young", "old", "friendly", "quiet", "busy", "funny", "nice", "blonde hair"],
        },
        "pronunciation": [
            {"focus": "f / v", "tip_ar": "حافظ على وضوح family/five وvery/seven عندما تتغير التفصيلة."},
            {"focus": "man / men", "tip_ar": "اسمع الكلمة مع العدد والسياق ولا تعتمد على حركة واحدة فقط."},
        ],
    },
    "activities": [
        {"id": "people_word", "type": "visual_choice", "prompt_ar": "اختر كلمة الشخص أو الجمع التي تناسب الصورة الخيالية.", "targets": ["person", "people", "man", "men", "child", "children"]},
        {"id": "evidence_only_description", "type": "choice_set", "prompt_ar": "اختر فقط الوصف الذي قاله الصوت أو يثبته النص، لا تخمّن الشخصية.", "answer_reveal_after_attempt": True},
        {"id": "sound_meaning", "type": "listening_choice", "prompt_ar": "ميّز التفصيلة المقصودة في كلمات مختارة.", "contrasts": [["five", "very"], ["man", "men"]]},
        {"id": "person_cards", "type": "two_pass_listening", "prompt_ar": "المرة الأولى للعلاقات، والثانية لحقيقتين عن كل شخص.", "transcript_hidden": True},
        {"id": "guided_map", "type": "listening_map", "prompt_ar": "اختر خريطة الأشخاص التي تحفظ كل حقيقة مع صاحبها.", "model_hidden": True},
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U2-L01",
        MASTERY,
        {
            "comprehension": "The people, relationships, and requested fact types are understood.",
            "outcome_performance": "Two accurate facts are recorded for each of three people.",
            "context_transfer": "A changed order, voice, and family structure are mapped without a transcript.",
            "control_or_repair": "No fact crosses to the wrong person; one replay is used instead of guessing.",
        },
        "اشرح إزاي اسم أو علاقة جديدة تعمل بطاقة شخص جديدة وتمنع خلط الحقائق.",
        [
            {"when": "next day", "task": "Map two people and two facts each."},
            {"when": "three days", "task": "Distinguish one changed people or sound detail."},
            {"when": "seven days", "task": "Map a fresh three-person family message."},
        ],
    ),
    "ai_contract": ai_contract(
        "U2-L01",
        "Coach person-and-fact listening without revealing the transcript or requesting family disclosure.",
        "Listen once for the people, then again for two facts about each.",
        "اسمع مرة للأشخاص، ومرة لحقيقتين عن كل شخص.",
        ["Fact attributed to wrong person", "Relationship confused with name", "Unheard personality guessed from a visual"],
        ["Use fictional people and never request learner family details.", "Do not reveal the transcript before capture.", "Repair sound only when a key person or fact is lost."],
    ),
    "scene": "A respectful adult class listens to a fictional family voice message beside simple neutral people cards. The mood is curious and organised, never sentimental, stereotyped, or invasive.",
    "sample_context": "One Egyptian-Arabic teacher models fictional family descriptions in clear General American English. Explain relationship signals, person cards, evidence-only descriptions, and two meaning-relevant sound contrasts. No learner interaction or real family request occurs in the video.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {
        "schema_version": 2,
        "accent": "General American",
        "usage": "Meaning-preserving reference; accept intelligible stable varieties.",
        "entries": [
            {"text": "five / very", "ipa": "/faɪv/ /ˈvɛri/", "director_hint": "voiceless versus voiced onset"},
            {"text": "family / seven", "ipa": "/ˈfæməli/ /ˈsɛvən/", "director_hint": "retain key consonant"},
            {"text": "man / men", "ipa": "/mæn/ /mɛn/", "director_hint": "meaning-bearing vowel contrast"},
        ],
        "curriculum_target_ids": ["a1_pronunciation.f_v_contrast", "a1_pronunciation.front_central_vowels"],
    },
    "asset_briefs": """# U2-L01 Asset Briefs

Use neutral fictional people cards and relationship lines without assuming one family
structure, ethnicity, religion, gender role, or co-residence. Personality words appear
only as supplied text or audio—not inferred from faces. Provide replay, post-attempt
transcript, keyboard access, text alternatives, and no personal-family data capture.
""",
    "video_readme": video_readme("U2-L01", "Understand Talk about Family"),
}
