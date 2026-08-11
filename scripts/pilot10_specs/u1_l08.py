from scripts.pilot10_spec_helpers import assessment, ai_contract, video_readme
from scripts.pilot10_specs.u1_l08_transcript import TRANSCRIPT


MASTERY = {
    "construct_id": "a1.u1.l08.connected_personal_profile",
    "critical_meaning": "A reader can identify the main person, related person or pet, and all required facts without referent confusion.",
    "primary": {
        "scenario_en": "A fictional learner needs a six-sentence profile for a class page.",
        "scenario_ar": "متعلم خيالي يحتاج نبذة من ست جمل لصفحة الدورة.",
        "prompt_en": "Write the profile from a fresh fact card and correct its one false detail.",
        "required": ["identity", "place_or_job", "present_fact", "family_or_pet", "have_or_has", "quantity_or_description", "and_or_but", "negative_correction"],
        "support": "Fact labels only; no complete sentence frames or model profile.",
        "freshness": "The person, relationships, facts, quantities, false detail, and order are new.",
        "safe_identity": True,
    },
    "replacement": {
        "scenario_en": "A fictional volunteer needs a short profile for a community board.",
        "scenario_ar": "متطوع خيالي يحتاج نبذة قصيرة للوحة مجتمعية.",
        "prompt_en": "Write an equivalent six-sentence profile and correct the changed false detail.",
        "required": ["identity", "place_or_job", "present_fact", "family_or_pet", "have_or_has", "quantity_or_description", "and_or_but", "negative_correction"],
        "support": "Fact labels only; no complete sentence frames or model profile.",
        "freshness": "A new person, family structure, pet, and correction preserve the construct.",
        "safe_identity": True,
    },
}


SPEC = {
    "lesson_id": "U1-L08",
    "goal_ar": "أن تكتب نبذة قصيرة مترابطة عن شخصية خيالية وعلاقة أو حيوان، مع حقائق واضحة.",
    "scope": {"required_length": "five to seven short sentences", "required_content": ["main person", "place or role", "family or pet", "connected facts", "one correction"], "time_hypothesis_minutes": "40-50"},
    "teach_back_summary": "Explain one subject-verb choice and why and differs from but.",
    "non_goals": ["A full family history", "Mandatory personal disclosure", "Complex tense use", "Long composition"],
    "prerequisites": ["U1-L03", "U1-L06", "U1-L07"],
    "bounded_scope_notes": [
        "Use present be negatives only to correct or deny a current fact.",
        "Use present simple for current facts and familiar actions with bounded third-person agreement.",
        "Use have/has, singular/plural quantity, compact noun phrases, and and/but/or inside one short profile.",
        "Select only family, personal-life, and pet words needed by the voluntary or fictional task.",
    ],
    "not_yet": ["past biography", "extended relationship disclosure", "complex noun phrases", "paragraph-level cohesion"],
    "content": {
        "situation": {"title_ar": "موقف اليوم", "prompt_ar": "تحول بطاقة حقائق خيالية إلى نبذة قصيرة يمكن للقارئ فهمها.", "success_ar": "الشخص والعلاقات والحقائق واضحة ومترابطة من غير كشف معلومات خاصة."},
        "model": {
            "speaker": "Salma",
            "lines": ["I'm Salma.", "I live in Doha, and I work in a clinic.", "I have one sister and two brothers.", "My sister is a teacher, but she isn't in Doha.", "She lives in Amman.", "I have a friendly cat."],
            "gist_question_ar": "من الشخص الرئيسي وما العلاقات والحقائق الأساسية؟",
            "gist_answer": ["Salma", "Doha", "clinic", "siblings", "sister in Amman", "cat"],
        },
        "notice": [
            {"chunk": "I live / she lives", "focus": "present fact and third-person agreement"},
            {"chunk": "I have / she has", "focus": "family or possession"},
            {"chunk": "one child / two children", "focus": "quantity and noun number"},
            {"chunk": "a friendly cat", "focus": "compact noun phrase"},
            {"chunk": "and / but / or", "focus": "add, contrast, choose"},
            {"chunk": "isn't / aren't / I'm not", "focus": "correct a false present fact"},
        ],
        "explanation_ar": [
            "حافظ على فاعل واضح في كل جملة حتى لا تختلط المعلومات.",
            "مع he/she/it راجع نهاية الفعل وhas؛ مع I/you/we/they استخدم الشكل الأساسي وhave.",
            "العدد يحدد المفرد أو الجمع، وبعض الكلمات مثل child/children تتغير.",
            "and للإضافة، but للتباين، وor للاختيار.",
            "النفي يصلح حقيقة خاطئة؛ ليس عنصرًا يجب حشره في كل نبذة.",
        ],
        "toolkit": {
            "family": ["parent", "mother", "father", "brother", "sister", "child", "children", "cousin", "partner"],
            "pets": ["dog", "cat", "bird", "fish", "horse"],
            "facts": ["I live …", "I work …", "I like …", "She lives …", "He works …"],
            "profile": ["This is my …", "I have …", "His/Her name is …", "He/She has …"],
        },
        "pronunciation": [],
    },
    "activities": [
        {"id": "subject_verb", "type": "choice_set", "prompt_ar": "اختر الفعل الذي يناسب الشخص.", "items": [{"prompt": "She ___ in Amman.", "options": ["live", "lives"], "answer": 1}, {"prompt": "I ___ a cat.", "options": ["have", "has"], "answer": 0}]},
        {"id": "quantity_phrase", "type": "build", "prompt_ar": "كوّن عبارات مفهومة من عدد ووصف واسم.", "targets": ["two brothers", "two children", "a friendly dog"]},
        {"id": "connector_meaning", "type": "choice_set", "prompt_ar": "اختر and أو but أو or حسب العلاقة.", "answer_reveal_after_attempt": True},
        {"id": "false_fact_repair", "type": "edit", "prompt_ar": "انفِ المعلومة الخاطئة ثم اكتب الحقيقة الصحيحة.", "requires_be_negative": True},
        {"id": "guided_profile_plan", "type": "fields", "prompt_ar": "جهّز كلمات ست خانات فقط، ثم اكتب من غير نموذج كامل.", "fields": ["person", "place_or_job", "present_fact", "family_or_pet", "quantity", "connection"], "allow_fictional": True},
    ],
    "mastery": MASTERY,
    "assessment": assessment(
        "U1-L08",
        MASTERY,
        {
            "comprehension": "All fact-card relationships and the false detail are understood.",
            "outcome_performance": "The profile communicates every required fact in five to seven sentences.",
            "context_transfer": "New people, quantities, relations, and facts are expressed without copying the model.",
            "control_or_repair": "Subject reference, key verb agreement, quantity, connector meaning, and negative correction remain clear.",
        },
        "اشرح ليه نقول I have لكن she has، واذكر الفرق بين and وbut بمثال قصير.",
        [
            {"when": "next day", "task": "Write four changed facts with have/has and quantity."},
            {"when": "three days", "task": "Correct a false profile fact and connect two ideas."},
            {"when": "seven days", "task": "Write a fresh six-sentence fictional profile."},
        ],
    ),
    "ai_contract": ai_contract(
        "U1-L08",
        "Coach a bounded profile without composing or rewriting it for the learner.",
        "Choose a fictional profile card and tell me the first fact in your own sentence.",
        "اختر بطاقة خيالية واكتب أول حقيقة بجملتك أنت.",
        ["Referent changes mid-profile", "Key third-person verb or have/has obscures meaning", "Quantity conflicts with noun", "Connector reverses the intended relation"],
        ["Never request real family disclosure.", "Correct one meaning-bearing issue per turn.", "Do not expand into past biography or a long composition."],
        turn_limit=8,
    ),
    "scene": "An adult community-class profile board with fictional fact cards. The mood is warm and respectful. The teacher treats family structures as optional and varied, with no assumption about marriage, children, or household.",
    "sample_context": "One Egyptian-Arabic teacher explains how short facts become a connected profile. Use General American English at a natural A1 pace. Model fictional families and pets inclusively. No learner interaction occurs in the video; writing begins afterward.",
    "transcript": TRANSCRIPT,
    "pronunciation_map": {"schema_version": 2, "accent": "General American", "usage": "Synthesis reference only; no pronunciation target is assessed.", "entries": [{"text": "family", "ipa": "/ˈfæməli/"}, {"text": "children", "ipa": "/ˈtʃɪldrən/"}, {"text": "have / has", "ipa": "/hæv/ /hæz/"}], "curriculum_target_ids": []},
    "asset_briefs": """# U1-L08 Asset Briefs

Use fictional fact cards representing varied adult lives without assuming marriage,
children, gender roles, or co-residence. Provide a six-field planning board, subject
tracking, and visible connector meaning. All writing controls need RTL/LTR support,
keyboard access, non-colour error cues, and no persistence of personal disclosures.
""",
    "video_readme": video_readme("U1-L08", "Write a Short Profile"),
}
