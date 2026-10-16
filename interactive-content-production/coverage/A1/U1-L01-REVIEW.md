# A1 U1-L01 — Curriculum source-to-lesson review queue

**Status: BLOCKED for lesson completion / release; drafting can continue only within owner scope.**
This document is an *agent analysis*, not a modification to the semantic lock, lesson brief or coverage ledger.

The source ledger introduces **36** canonical elements in this lesson (8 abilities, 5 phrases, 8 grammar, 13 words, 2 pronunciation). Every source ID is traced in [U1-L01.json](U1-L01.json). The Python gate checks exact ledger membership and locked phrase/word control roles. The `ready` command remains deliberately red.

## Twelve identified source-scope conflicts that need curriculum owner review

| Class | Canonical source entries | What needs decision |
| --- | --- | --- |
| Ability | Can understand basic phrases in short, simple texts | Does this introductory listening-led lesson require a short *reading* comprehension beat, or is evidence deferred elsewhere? Do not claim listening tests verify reading. |
| Grammar | FORM: NEGATIVE DECLARATIVE WITH 'BE' | Brief asks minimum first-/second-person be chunks, not a negative grammar system. Confirm source ledger placement or bounded receptive use. |
| Words | advice, photograph, nothing, its, yourself | These are not naturally necessary for greeting/name/wellbeing; do not add unrelated words to force green coverage. Confirm later reallocation or explicit incidental exposure requirement. |
| Feelings / wellbeing | afraid, excited, feeling, sad, tired | Do these belong to a **short, age-appropriate wellbeing reply extension**, perhaps one optional contrast and a later review, or elsewhere? `excited` and `feeling` have level-wide productive roles, but that does not prove they must be independently produced in U1-L01. |

Until approved, these 12 items remain `escalate` in the mapping; the gate refuses `ready`. Do NOT silently classify them as mastered, waive them, rewrite their source IDs, or change the locked curriculum.

## Twenty-four other mapped decisions

- All **five fixed productive phrases** (`Good morning`, `How are you?`, `pretty good`, `really good`, `Thank you`) have source-accurate planned authored teaching and **Speaking evidence** in the product PR #54. This is a **plan**, not confirmation that a learner demonstrated each.
- The remaining words/grammar/abilities/pronunciation are mapped to meaningful teaching/Listening or bounded context, with source IDs and scene/beat references. Broader abilities (e.g. giving age and origin) remain bounded to the canonical brief's name first-contact scope; an owner's curriculum validation is still required.
- Every content-mapping change must re-run `coverage_gate.py check A1 U1-L01` and link QA. The `ready` command additionally requires all learning decisions and **six quality gates** `accepted`: source, script, actual screenshots, actual voice, final Speaking, owner acceptance.

## Real production evidence still outstanding

1. Owner/curriculum ruling for the conflicts above; approve corrected decisions and future retrieval plans if relocated.
2. Critique and authorize revised 6-turn Gemini TTS edition `pilot02` before paying for generation.
3. Produce the two-speaker WAV + actual word-aligned JSON + VTT, inspect/audit six turns and all clip boundaries.
4. Verify Otti PCM queue does not overlap recording or re-enable user microphone during playback; test real provider, interrupts, browser permission failures and echo.
5. Open and critique **all** A1 contact sheets on narrow/regular phone and desktop after the final code changes; simulate weak Speaking replies and test teacher repair.
6. Owner acceptance, release approval and only then status `done`.

**Owner decision needed:** confirm resolution or allowed bounded placement for the 12 source-scope conflicts, and approve the revised TTS job before any paid synthesis. The Factory Issue gateway is locked to learn-curriculums formats; use its generic workflow only.
