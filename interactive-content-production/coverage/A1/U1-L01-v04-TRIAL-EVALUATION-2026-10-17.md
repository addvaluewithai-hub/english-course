# U1-L01 — v04 trial evaluation: **natural core, separate evidence, no instructions change yet**

**Status:** **EDITORIAL_TRIAL_STRUCTURAL_PASS / PEDAGOGICAL_AND_RUNTIME_QA_PENDING** (2026-10-17). This is the author's own internal check, **not independent LESSON_REVIEW_PASS or owner approval**. The owner authorized testing a repair to **this first lesson**, and explicitly said **do not update instructions for future lessons until the repaired lesson turns out well**. Accordingly, neither canonical production instructions nor Stage-06/07 source locks are changed in this trial.

## The actual new core audio (8 turns, 54 whitespace-separated words)

```text
Maya: Good morning! I'm Maya. What's your name?
Leo: Hi! My name is Leo.
Maya: Nice to meet you, Leo. How are you?
Leo: Pretty good, thanks. I'm feeling excited about our English class. And you?
Maya: Really good, thank you. I'm excited, too.
Leo: Great! Is this your first class?
Maya: Yes, it is. See you inside!
Leo: See you, Maya!
```

**Why this story is improved:** Two people greet before a first English class, exchange names and wellbeing, one expresses excitement, and they part naturally. There is no cat-photo detour, unexplained negative `be`, vocabulary-forcing advice request or unnecessary new character. All five locked formulaic target phrases and the two potentially productive lexical items (`excited`, `feeling`) occur naturally. **Hearing them remains only exposure, not seven proven learner utterances.**

## What the complete v04 authored trial actually includes

- **Single JSON candidate:** [`U1-L01-NATURAL-FIRST-CONTACT-v04.CANDIDATE.json`](U1-L01-NATURAL-FIRST-CONTACT-v04.CANDIDATE.json) has **7 modular scenes, 22 exact Egyptian-Arabic teacher speech beats, 22 distinct board states with portrait/landscape/alt text, 5 complete ID-keyed MCs with distinct feedback for every wrong option**, a new printed reading card, one short teacher-spoken `I'm tired today` alternate wellbeing line, a supported-but-not-overclaimed pronunciation attempt, and final real Speaking with **7 separately observed productive targets**. It also contains a five-clip proposal (all null timestamps, unapproved WAV) and an audio/PCM/board/mic **event contract**. Board SVGs/React code **have not been implemented or captured**; timestamps/word sync still require actual audio. The code is **an editorial package**, not a drop-in EnglishLive runtime schema.
- **Source decision matrix:** [`U1-L01-v04-36-SOURCE-DECISION-MATRIX.CANDIDATE.json`](U1-L01-v04-36-SOURCE-DECISION-MATRIX.CANDIDATE.json) explicitly covers **all 36 unchanged IDs**. For the original **12 owner-escalated items**, this trial proposes **5 provisionally retained** (independent reading objective, `excited` productive, `feeling` productive, `tired` receptive, `yourself` receptive) and **7 re-home candidates** (negative `be`, `advice`, `afraid`, `its`, `nothing`, `photograph`, `sad`). **NO re-home is actually approved or made.** Stage-06 contains current `introduce: U1-L01` and earlier/later practice/retrieval; moving any item requires an owner-reviewed complete lifecycle/lesson-load change, not silent omission.
- **Repeatable regression test source:** [`validate_a1_u1_l01_v04.py`](../../tools/validate_a1_u1_l01_v04.py) contains Python stdlib tests and four negative fixtures (all answers first, missing wrong feedback, pre-listen spoiler, invented audio timestamps). **The Python file was committed but not executed in a checkout/CI in this session**. An equivalent **live connector-sourced JavaScript structural audit was executed**, with **zero rule violations and 4/4 negative mutations detected**. These are NOT listening or learning tests.

## v03 vs v04 — what demonstrably changed

| Check | v03 | v04 editorial trial | Interpretation |
| --- | --- | --- | --- |
| Recorded source | **18 turns / 140 words** | **8 turns / 54 words** | Focus changed from ledger-filled story to normal first contact |
| Original dialogue played across primary excerpts | **41 source-turn playbacks** (18 full + 7 intro + 5 wellbeing + 5 photo + 6 advice/closing) | **15** (8 full + 3 names + 3 wellbeing + 1 question pronunciation) | Less repetitive; still unknown real audible time |
| Primary story logic | abrupt cat/photo/advice detour | no subplot; greeting → name → wellbeing/excitement → farewell | Authorial reasoning only; novice study not yet done |
| Correct option positions | six of six position **1** | five questions, indices **2,0,1,2,0** (zero-based) | Static anti-pattern corrected; product must preserve visible order |
| Gist check | Turn-10 photograph detail disguised as gist | Actual purpose: two people meet before English class; **Arabic options** | Safer for A1, no class/meeting clue in pre-audio script/board |
| Teacher script/MC feedback | In prose, placeholders in manifest for all 6 MCs | Exact text at every beat plus correct/wrong per distractor in **one machine-readable package** | Better authoring handoff; still needs product adapter |
| Other lexical items | All shoved into a single audio recording | Only core words in source; small separate reading and wellbeing activities; 7 flagged for approved relocation | Honesty about coverage, but **7 source requirements still conflict** with current ledger |
| Board / sync | Descriptive storyboard and optimistic word-sync | 22 explicit semantic states + beat-event PCM contract, explicitly not real word-timed Live narration | Still only specification, no SVG/React/audio verification |
| Productive outcomes | All 7 source targets mapped to one beat | Fresh meeting plus changed occasions; separate evidence policy from communication pass | Still not observed with real students/Live Gemini |

### Structural checks performed in this run

Checked against live fetched candidate+matrix+original source JSON (not a stale cached summary):
- Exact 36 source IDs, semantic roles and dispositions preserved, 12 owner gates unwaived; 5 keep-trial / 7 rehome proposals explicitly marked non-authoritative.
- Eight sequential two-speaker source turns, all required five phrases and two productive words actually present; focused wellbeing clip contains **both** Leo's and Maya's named replies.
- Five distinct named clips with no fake approved WAV/URLs/time bounds; dedicated single-turn question replay.
- Seven scenes, 22 unique beats each with authored speech and valid planned board, and 22 nonempty accessibility/responsive board state specifications.
- Five complete answer-keyed MCs with positions `[2,0,1,2,0]`, authored positive and per-distractor spoken explanations; no class/meeting spoiler in first-listen teacher setup, audio required before answering.
- Independent reading note not read out first, seven productive proof slots linked to **actual learner turns** rather than automatically awarded on scene completion.
- Negative mutations detected for the four original P0-type defects listed above.

**Result of executed equivalent JavaScript validation: PASS, no failures; 4/4 negative fixtures rejected.** The committed Python checker was not locally/CI executed; do not represent that as a Python PASS.

## Deliberate new risks / blockers

1. **The source ledger still introduces all 12 at U1-L01**. This trial does not secretly make 7 disappear: `ready` must remain blocked pending owner scope/lifecycle approval, or rework to retain items with genuine evidence.
2. **Even a clean eight-turn recording is not yet listened to.** Required real Gemini factory output and quality/timing checks still not commissioned/approved. Source WAV, turn timings, transcript/VTT and clips cannot be verified by structural review.
3. **22 teacher beats/7 scenes could still feel heavy**, even with a 54-word core. Need real timed delivery and novice observation; may combine/truncate *teacher beats* once the meaningful coverage is accepted. Simply optimizing word count is not proof of good teaching.
4. **Reading card / simple tired reply / seven productive exact targets** are design hypotheses. A novice might not independently infer `yourself`, and a normal successful conversation may never elicit both `pretty good` and `really good`. Report exact output not mastered, or get approved retrieval timing.
5. **Actual SVG/React visuals and sync unavailable**. This v04 changes the required board states; prior EnglishLive #54 screenshots of old pilot cannot certify them.
6. **The critique is still not independent.** A distinct human/agent reviewer should assess: believable spoken interaction, first-listen difficulty, comprehension inference without boards, phrase evidence integrity, and learning time. Do not change other lesson-production instructions on self-assessed structural PASS.

## Clear decision tree after this trial

- If owner/editor accepts this **story and scene design**, settle 12 exact source rulings; update Stage-06 source lifecycle + briefs/coverage in authorized curriculum review only, then let **existing EnglishLive #54 producer** implement the v04 package and bespoke SVG boards against the real runtime.
- After implementation, run product tests and inspect deterministic state frames at 320×640, 400×860, 1280×900, actual two-speaker WAV, diarized transcript/VTT, audited clip boundaries, Gemini Otti PCM/mic interruptions, true reading and unscripted Speaking good/weak cases. Commission **exact new edition** only after owner authorizes its script/job/spend; do not use old `pilot02`.
- **Only if pedagogical and runtime evidence is strong** should we propose editing general production workflow instructions. That separate proposal should encode the validated "natural core → suitable evidence activity → explicit rehome decision" sequence and its QA gates; don't promote this unpublished candidate into a mandatory pattern for 62 lessons.

**Review verdict today: v04 is substantially more coherent and structurally auditable than v03, but `LESSON_REVIEW_PASS` and production-rule changes are NOT justified yet.**
