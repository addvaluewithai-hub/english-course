"""Dialect-aware hypotheses for later specialist and learner validation."""

RISK_HYPOTHESES = (
    ("p_b_contrast", "consonant_clarity", "Some learners may merge English /p/ and /b/ in perception or production."),
    ("v_f_contrast", "consonant_clarity", "Some learners may merge English /v/ and /f/ in perception or production."),
    ("dental_fricatives", "consonant_clarity", "English /θ/ and /ð/ may be replaced by different stops or fricatives; patterns vary by Arabic dialect."),
    ("velar_nasal", "consonant_clarity", "Some learners may add /g/ after /ŋ/ or replace it in unfamiliar word positions."),
    ("high_vowel_contrasts", "vowel_clarity", "Contrasts such as /iː/-/ɪ/ and /uː/-/ʊ/ may need explicit perception and meaning-based practice."),
    ("front_central_vowels", "vowel_clarity", "English /æ/, /e/, /ʌ/, and related vowels may be mapped onto a smaller learner-specific set."),
    ("cluster_epenthesis", "syllable_shape", "Some learners may insert a vowel into unfamiliar initial or final consonant clusters."),
    ("final_cluster_reduction", "syllable_shape", "Final consonants or clusters may be reduced when several articulatory demands occur together."),
    ("s_ed_endings", "grammatical_endings", "Plural, third-person, possessive, and past endings may be omitted or given an extra syllable."),
    ("lexical_stress_transfer", "word_stress", "Stress may follow spelling or a familiar Arabic pattern rather than the English lexical pattern."),
    ("equal_prominence", "prominence_rhythm", "Function words may receive equal prominence, limiting English focus and rhythm cues."),
    ("spelling_driven_pronunciation", "sound_perception", "English spelling may encourage a stable letter-to-sound guess where pronunciation is irregular."),
)

VALIDATION_ROUTE = (
    "arabic_english_pronunciation_specialist_review",
    "dialect_aware_learner_observation",
)
