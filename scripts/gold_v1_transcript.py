"""Deterministically adapt the owner-approved transcript to its U1-L03 position."""


def migrate_transcript(source: str) -> str:
    lines = source.splitlines()
    expected_open = "Speaker 1: [WARM] أهلًا بيك في أول درس."
    if lines[0] != expected_open:
        raise ValueError("legacy transcript opening changed")
    lines[0] = "Speaker 1: [WARM] أهلًا بيك في درس جديد."

    model_prompt = "Speaker 1: اسمع النموذج ده أولًا."
    prompt_index = lines.index(model_prompt)
    prior = (
        "Speaker 1: إنت سمعت شكل تقديم بسيط في الدرس اللي فات. "
        "دلوقتي هنستخدمه عشان تبني تقديمك بنفسك."
    )
    lines[prompt_index + 1:prompt_index + 1] = ["", prior]

    live_start = next(
        index for index, line in enumerate(lines)
        if 'ph="lɪv">live</phoneme></lang>' in line
    )
    live_end = next(
        index for index, line in enumerate(lines[live_start:], start=live_start)
        if '[CLEAR, NATURAL PACE]' in line and 'I live in Amman.' in line
    )
    live_note = [
        "Speaker 1: كلمة <lang xml:lang=\"en-US\"><phoneme alphabet=\"ipa\" ph=\"lɪv\">live</phoneme></lang> هنا معناها \"أعيش\". اسمعها داخل الجملة وقلّدها كوحدة، من غير ما نحولها لقاعدة أصوات كبيرة دلوقتي.",
        "",
        "Speaker 1: [CLEAR, NATURAL PACE] <lang xml:lang=\"en-US\"><phoneme alphabet=\"ipa\" ph=\"aɪ lɪv ɪn əˈmɑːn\">I live in Amman.</phoneme></lang>",
    ]
    lines[live_start:live_end + 1] = live_note

    engineer_index = next(
        index for index, line in enumerate(lines)
        if "I'm an engineer.</phoneme>" in line
    )
    stress_note = [
        "",
        "Speaker 1: لاحظ إن الكلمات الطويلة فيها جزء أوضح شوية. اسمع:",
        "",
        "Speaker 1: [CLEARLY] <lang xml:lang=\"en-US\"><phoneme alphabet=\"ipa\" ph=\"ˈtiːtʃɚ | ˌɛndʒəˈnɪr | dɪˈzaɪnɚ\">teacher, engineer, designer.</phoneme></lang>",
        "",
        "Speaker 1: مش محتاج تحفظ علامة النبر. اسمع الكلمة كوحدة وقلّد الجزء الأوضح.",
    ]
    lines[engineer_index + 1:engineer_index + 1] = stress_note
    return "\n".join(lines).rstrip() + "\n"
