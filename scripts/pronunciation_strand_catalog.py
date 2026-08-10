"""English-specific intelligibility sequence across A1-C2."""

PRONUNCIATION_STRANDS = {
    "sound_perception": {
        "title": "Sound perception and word recognition", "control": "a1", "consolidate": "a2", "prerequisites": [],
        "expectations": {
            "a1": "Distinguish selected high-value sounds, word boundaries, names, numbers, and learnt chunks in very clear speech.",
            "a2": "Recognise selected contrasts and familiar words across routine voices and generally clear delivery.",
            "b1": "Use phonological cues to recognise familiar connected speech despite regular variation and first-language influence.",
            "b2": "Resolve most sound, stress, and reduction variation in standard familiar and field-related input.",
            "c1": "Track a full range of phonological cues across accents, speed, register, and complex discourse.",
            "c2": "Interpret fine phonological detail, marked delivery, and subtle prosodic meaning across demanding input.",
        },
    },
    "consonant_clarity": {
        "title": "Consonant contrasts and place or manner clarity", "control": "a1", "consolidate": "b1", "prerequisites": ["sound_perception"],
        "expectations": {
            "a1": "Produce selected high-impact consonant contrasts clearly enough in names, numbers, key nouns, verbs, and chunks.",
            "a2": "Maintain selected contrasts in routine phrases and short sentences, with repetition available when needed.",
            "b1": "Keep consonant distinctions generally intelligible in connected familiar-topic speech despite regular mispronunciation.",
            "b2": "Sustain consonant clarity throughout extended speech so accent has little effect on understanding.",
            "c1": "Control consonant detail flexibly across speed, register, unfamiliar words, and complex purposes.",
            "c2": "Use precise articulation deliberately where it supports subtle contrast, emphasis, or rhetorical effect.",
        },
    },
    "vowel_clarity": {
        "title": "Vowel contrasts and reduced vowels", "control": "a1", "consolidate": "b1", "prerequisites": ["sound_perception"],
        "expectations": {
            "a1": "Produce selected meaning-changing vowel contrasts in a bounded learnt repertoire with modelling and repair.",
            "a2": "Maintain selected vowel contrasts in routine words and phrases and begin recognising common unstressed vowels.",
            "b1": "Keep vowel quality sufficiently distinct in connected familiar-topic speech despite noticeable accent.",
            "b2": "Use stable stressed vowels and functional reductions so pronunciation remains intelligible throughout.",
            "c1": "Control vowel quality and reduction flexibly across rate, prominence, register, and unfamiliar language.",
            "c2": "Adjust vowel and reduction detail precisely when it contributes to nuance, contrast, or performance effect.",
        },
    },
    "syllable_shape": {
        "title": "Syllable shape, consonant clusters, and word endings", "control": "a1", "consolidate": "a2", "prerequisites": ["consonant_clarity"],
        "expectations": {
            "a1": "Preserve selected final consonants and simple clusters when they carry essential word identity or meaning.",
            "a2": "Produce common initial and final clusters without additions or losses that disrupt routine understanding.",
            "b1": "Maintain word shape across longer familiar-topic stretches while self-correcting important cluster problems.",
            "b2": "Preserve syllable structure reliably at natural speed, including less familiar and field-related words.",
            "c1": "Handle complex word shapes flexibly across connected, formal, and rapid speech.",
            "c2": "Use precise syllable shaping and deliberate simplification only when context and style make it appropriate.",
        },
    },
    "grammatical_endings": {
        "title": "Audible grammatical endings", "control": "a1", "consolidate": "b1", "prerequisites": ["syllable_shape"],
        "expectations": {
            "a1": "Make selected plural, possessive, and simple verb endings audible when omission changes immediate meaning.",
            "a2": "Distinguish common -s and -ed forms in routine production and recognise their main pronunciation patterns.",
            "b1": "Preserve grammatical endings consistently enough in connected speech for time, number, and ownership to remain clear.",
            "b2": "Integrate endings naturally into clusters and connected speech without loss of grammatical information.",
            "c1": "Control subtle morphological sound detail flexibly across complex and rapid language.",
            "c2": "Use grammatical sound detail precisely while varying reduction appropriately for style and emphasis.",
        },
    },
    "word_stress": {
        "title": "Word stress and stress-sensitive recognition", "control": "a1", "consolidate": "b1", "prerequisites": ["sound_perception"],
        "expectations": {
            "a1": "Place recognisable stress in selected names, numbers, nationalities, jobs, and other lesson-critical words.",
            "a2": "Use expected stress in a wider routine repertoire and notice stress changes in common related words.",
            "b1": "Maintain generally intelligible word stress across familiar connected speech and repair important errors.",
            "b2": "Control stress reliably in broad general and field-related vocabulary, including many derived words.",
            "c1": "Use word stress flexibly across unfamiliar, technical, and morphologically complex language.",
            "c2": "Manipulate normal and contrastive lexical stress precisely for meaning and stylistic effect.",
        },
    },
    "prominence_rhythm": {
        "title": "Sentence prominence and rhythm", "control": "a2", "consolidate": "b2", "prerequisites": ["word_stress"],
        "expectations": {
            "a1": "Notice and imitate prominence inside short learnt chunks without a natural-rhythm mastery demand.",
            "a2": "Highlight key content words and reduce some predictable function words in routine short utterances.",
            "b1": "Use prominence to keep main information clear in connected familiar-topic speech.",
            "b2": "Use prominence and rhythm consistently to support focus, contrast, turn structure, and intelligibility.",
            "c1": "Shift prominence flexibly to organise complex ideas, stance, correction, and audience attention.",
            "c2": "Shape rhythm and prominence precisely for subtle meaning, rhetorical design, and interpersonal effect.",
        },
    },
    "connected_speech": {
        "title": "Connected-speech perception and production", "control": "a2", "consolidate": "b2", "prerequisites": ["syllable_shape", "prominence_rhythm"],
        "expectations": {
            "a1": "Recognise a small set of frequent linked or reduced forms inside familiar, very clear chunks.",
            "a2": "Understand common routine linking and reductions and use selected forms without losing key words.",
            "b1": "Process familiar connected speech and use linking or reduction that supports rather than obscures meaning.",
            "b2": "Handle common connected-speech processes at a natural pace with intelligibility throughout.",
            "c1": "Adapt linking, assimilation, elision, and reduction flexibly across rate and register.",
            "c2": "Use or resist connected-speech processes deliberately for precision, clarity, style, and audience.",
        },
    },
    "intonation_stance": {
        "title": "Intonation, interaction, and stance", "control": "a2", "consolidate": "b2", "prerequisites": ["prominence_rhythm"],
        "expectations": {
            "a1": "Use recognisable contours in a few learnt greetings, questions, checks, and polite responses.",
            "a2": "Use basic contours for statements, questions, continuation, politeness, and routine turn-taking.",
            "b1": "Use intonation to signal main intent, involvement, contrast, and completion in familiar interaction.",
            "b2": "Control intonation consistently enough to support viewpoint, stance, turn management, and social meaning.",
            "c1": "Interpret and produce nuanced intonation flexibly across complex social and professional interaction.",
            "c2": "Use fine intonational choices precisely for implication, humour, tact, ambiguity, and rhetorical effect.",
        },
    },
    "chunking_monitoring_repair": {
        "title": "Chunking, pausing, monitoring, and pronunciation repair", "control": "a1", "consolidate": "b1", "prerequisites": ["word_stress"],
        "expectations": {
            "a1": "Deliver short learnt sense groups, pause safely, and repeat or spell a key item when not understood.",
            "a2": "Group short sentences into clear units and use repetition, slower delivery, or rewording in routine repair.",
            "b1": "Chunk connected familiar-topic speech and monitor or repair pronunciation without abandoning the message.",
            "b2": "Manage pausing and repair smoothly enough to sustain extended independent interaction.",
            "c1": "Restructure complex delivery flexibly and resolve phonological ambiguity with little disruption.",
            "c2": "Backtrack, rechunk, and adjust articulation or prosody so smoothly that difficulty is unobtrusive.",
        },
    },
}
