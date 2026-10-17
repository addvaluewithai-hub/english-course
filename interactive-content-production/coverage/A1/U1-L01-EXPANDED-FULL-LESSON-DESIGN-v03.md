# U1-L01: expanded listening-first **full lesson** — editorial candidate v03

**Owner direction received (2026-10-17):** Try a longer, natural source conversation that contains and supports as much of the **canonical 36-ID load** as is pedagogically coherent **before** recommending transfer to later lessons. Produce the **whole lesson** (recording script + scripted Arabic teaching + substantive SVG board states + assessment + syncing + fresh speaking + QA), not only WAV. This is permission to **draft/redesign**, not acceptance of 12 unresolved exact source rulings, payment approval, product PR branch takeover or release.

**Status:** `EDITORIAL_CANDIDATE` — independent reviewer/authoring handoff; no owner signoff of exact lines/roles; no product build, paid media, screenshots, sound or learner QA carried out. This is new proposed material, NOT what PR #54 currently runs. Product implementation belongs to the **existing** EnglishLive producer of [Draft PR #54](https://github.com/addvaluewithai-hub/englishlive/pull/54). Do **not** create a competing claimed U1-L01 product PR or silently replace its six-turn `pilot02` request.

**Primary contract:** [Stage-07 U1-L01](https://github.com/addvaluewithai-hub/english-course/blob/main/curriculum/levels/a1/design-review/07-lesson-briefs/lesson-briefs.md); [36-item coverage](U1-L01.json); [editorial lesson contract](../../LESSON_CONTRACT.md); [12-ID owner brief](U1-L01-OWNER-DECISION-BRIEF-2026-10-17.md). Stage-07 core remains **greet, exchange names, basic wellbeing and polite closure**; this expanded first-day-class story adds **supporting** photo/feelings/advice context to reconcile the source ledger. Owner must still decide whether its extended scope and cognitive load are acceptable; no age, origin, job, numerical routines or extended new grammar chapter.

## 1. Two-speaker source: **18 turns / 140 English words**

The exact candidate English lines and producer-facing TTS request options are in **[`U1-L01-EXPANDED-DIALOGUE-v03.CANDIDATE.json`](U1-L01-EXPANDED-DIALOGUE-v03.CANDIDATE.json)**. Keep this JSON the single editable dialogue text; do not manually maintain a divergent TTS copy.

**Story, continuity and pacing**:

- **Act A, turns 01–07:** First meeting at the entrance to English class. Names, `Good morning`, `How are you?`, `pretty good`, `really good`, `thanks/thank you`, `feeling excited`, mild `afraid`, meeting `people`. No class teacher speaking (two voices only).
- **Act B, turns 08–12:** Leo says the teacher has asked them to `Introduce yourself`; Maya suggests a familiar personal topic. Leo holds a `photograph` of his cat Coco; `Its name is Coco`; Maya assumes Coco is `sad`, Leo corrects: `Coco isn't sad. Coco is tired`. This is a **meaningful negative be correction**, not eight disconnected grammar flashcards. The photo is a context prop, **not** an endorsed new productive objective.
- **Act C, turns 13–18:** Maya checks all is okay; Leo says `nothing is wrong`, asks for `advice`, hears a simple hello-and-smile tip, and says `I'm not afraid now. I'm feeling really good` before farewell. Recurring wellbeing supports narrative change, not a separate reaction-to-news lesson.

**Quality note:** At ~140 English words, a full first pass is demanding for absolute A1. Make the initial task **gist-only**, explicitly normalise not understanding every word, keep a voluntary replay and then divide into **three named short clips**. Teacher must not race through all 18 turns as a long lecture. Assess any excessive length with a first-time A1 learner; two alternate shorter source editions might be needed after review, not automatic trimming of canonical obligations.

### Stable authored clip map — candidate offsets, **NO milliseconds yet**

| Clip ID | Exact source turns | Pedagogical function | Playback rule |
| --- | --- | --- | --- |
| `full-conversation` | 01–18 | First exposure and later optional whole replay | No transcript or answer-bearing board before initial gist check |
| `first-contact` | 01–07 | Greetings, exchanging names and wellbeing | Spoken clip; then teach `I'm`, `What's your name?`, `How are you?` |
| `wellbeing-contrast` | 03–07 | Maya's `Really good` AND Leo's `Pretty good`, emotions | Fixes previous script/excerpt mismatch |
| `class-photograph` | 08–12 | `yourself`, `photograph`, `its`, `sad` vs `tired`, `isn't` | Show photo **only after** appropriate listening question |
| `advice-and-close` | 13–18 | `nothing`, `advice`, `I'm not afraid`, farewell | Natural ending; do not use a word quiz as proof of production |
| `leave-taking` | 16–18 | Politeness and goodbye replay on request | Exact reviewed boundaries only |

**Factory shape:** Maya = Aoede, Leo = Achird; 24kHz WAV, diarized actual-audio word transcript and VTT; Cloudinary approved URLs and audited clip bounds only after real delivery. Candidate metadata explicitly says **DO-NOT-DISPATCH**; any new request must use **new edition/job ID**, not overwrite `pilot02`. All transcript/turn/clip start and end times remain **unknown** until human-reviewed real rendered WAV. No guessed timestamps.

## 2. The complete teacher-led teaching sequence — **7 scenes**

These lines are **draft spoken Egyptian-Arabic narration** for Otti, to be read exactly by Gemini Live once authored. They are not on the product branch yet. Product can split as needed without losing semantic reveal order. Each scene has explicit visual and assessment behavior.

### S01 — `gist-first`: first listen (no spoilers)

- `s01-set`, Otti: **"هتسمع دلوقتي Maya وLeo بيتكلموا بالإنجليزي. مش مطلوب تفهم كل كلمة من أول مرة. ركّز في حاجة واحدة: Leo ورّى Maya إيه؟ وبعدها اختار من الصور."** Board **`B01-neutral`**: two neutral speaker silhouettes + playback readiness; **no class/cat/photo labels or dialogue summary**; trigger `full-conversation` **after** this narration drains.
- `s01-choice`, Otti: **"سمعت الحوار؟ اختار الحاجة اللي Leo ورّاها لـMaya. لو محتاج، اسمع التسجيل تاني."** Board **`B01-choice`** with *three plausible unmarked options*: `photo-of-cat` (correct), `photo-of-friend`, `class-book`; only after choice show the correct illustrative photo as feedback, never during pre-answer state.
- Right feedback: **"مظبوط؛ Leo قال photograph وبعدها cat. يعني ورّاها صورة لقطة. مش مطلوب تلتقط كل كلمة؛ المهم لقطت التفصيلة اللي بنسأل عنها."**
- Wrong feedback: **"الإجابة مش صورة لصاحب ولا كتاب. لما Leo قال photograph، كمل وقال It's my cat. خلّي بالك من الكلمة اللي بعد photograph؛ هنسمع الجزء ده تاني."** Preserve `incorrect` event; after feedback Otti may advance, but don't mark comprehension mastered.
- **P1 regression:** The first MC must NOT be solved by `s01-set`, `B01-neutral` or post-audio `s01-choice` without hearing the recorded words. Gist-only; no full transcript.

### S02 — `names-greetings`: basic first contact

- `s02-replay`, Otti: **"نرجع لأول الحوار. اسمع التحية والاسم والسؤال عن الاسم، وبعدين هنفك الجمل خطوة خطوة."** Board **`B02-neutral`** two speaker roles, no exact words before replay; play `first-contact`.
- `s02-greet`, Otti: **"Maya بدأت بـ Good morning؛ دي تحية الصبح. Leo رد Hi. ودي تحية عادية. الاتنين بيبدأوا تعارف لطيف."** Board **`B02-greet`** greeting lane with sunrise cue; `Good morning` appears now, not before replay.
- `s02-name`, Otti: **"Maya قالت I'm Maya، وLeo قال My name is Leo. الاتنين معناهم أنا اسمي… كلمة I'm اختصار I am. مش هنحفظ جدول am وis وare دلوقتي."** Board **`B02-names`** two person silhouettes linked to **I’m Maya** and **My name is Leo**.
- `s02-ask`, Otti: **"لو بتقابل حد لأول مرة تقول What's your name? وساعتها تدي اسمك أنت، مش حالة مزاجك. خلي الرد على قد السؤال."** Board **`B02-question`**, arrow from question mark to blank name slot.
- Check (changed person): **"Nora بتسألك What's your name? أنهي رد بيقول اسمك؟"** `I'm Omar.` (correct), `I'm okay, thanks.`, `Goodbye, Nora.` Wrong explanation distinguishes greeting/wellbeing/name; record MC as **receptive** only.

### S03 — `wellbeing-feelings`: contrast the two replies and feelings

- `s03-replay`, Otti: **"اسمع الجزء اللي فيه How are you؟ ركّز إن الردين مختلفين، وإن Leo قال إزاي حاسس في أول يوم."** Board **`B03-neutral`** question with two unlabelled answer speech bubbles; play `wellbeing-contrast` (03–07), **which actually contains both named replies**.
- `s03-answers`, Otti: **"How are you معناها إزيك؟ Leo قال Pretty good, thanks؛ كويس إلى حد كبير. Maya ردت Really good, thank you؛ كويس جدًا، شكرًا. الاتنين طبيعيين. وفيه ردود تانية زي I'm fine."** Board **`B03-replies`** two bubble lanes with `pretty good` and `really good`, not a ladder implying one answer is objectively better.
- `s03-feelings`, Otti: **"Leo قال I'm feeling excited، يعني أنا حاسس بحماس. وبعدين قال I'm a little afraid، يعني قلقان شوية. ممكن تكون متحمس وقلقان في نفس الوقت، خصوصًا أول يوم."** Board **`B03-feelings`** first-day emotional meter with two independent feelings, not a single mutually exclusive slider.
- `s03-sound`, Otti: **"اسمع نبرة How are you? فيها سؤال واهتمام. وجرب تقولها بنبرة سؤال، وبعدها قول Thank you بنبرة لطيفة. مجرد سماع الكلمتين مش معناه إنك قلتهم بنفسك."** Board **`B03-intonation`** rising question cue vs gentle statement cue; a real spoken attempt must be observed if pronunciation evidence claimed.
- Check (new setting): **"في أول يوم زميلك قال I'm excited, but a little afraid. هو حاسس بإيه؟"** `Happy to start but nervous too` (correct), `Only tired`, `Only sad`; this tests **receptive** meaning and must not substitute for productive `excited`.

### S04 — `photo-meaning`: a visual support, not an unrelated vocabulary dump

- `s04-replay`, Otti: **"دلوقتي اسمع الجزء اللي Leo فيه بيعرّف نفسه بحاجة بيحبها. هل القطة حزينة ولا تعبانة؟ اسمع الأول قبل ما تشوف الصورة."** Board **`B04-unrevealed`** neutral picture frame with non-identifying outline; play `class-photograph`.
- `s04-class-instruction`, Otti: **"المدرس قال Introduce yourself؛ يعني عرّف بنفسك. هنا Leo قال إنه ممكن يوري حاجة بيحبها. مش لازم تستخدم الكلمة دي في محادثتك النهائية، لكن مهم تفهم المطلوب منك."** Board **`B04-instruction`** teacher instruction text and learner silhouette, isolated English.
- `s04-photo`, Otti: **"Leo قال photograph يعني صورة، وأشار للقطة: It's my cat. Its name is Coco. خلي بالك: It's بمعنى it is، لكن its قبل name هنا معناها اسمها؛ مش لازم تدرس باب الملكية كامل النهاردة."** Board **`B04-photo`** new bespoke photo frame with stylised cat and visual caption; show the exact English text **only now**; distinguish `it's` versus `its` by written punctuation **not by claimed sound difference**.
- `s04-correction`, Otti: **"Maya افتكرت Coco sad يعني حزينة. Leo وضّح: Coco isn't sad. Coco is tired. يعني مش حزينة، لكنها تعبانة. دي جملة تصحيح حقيقية، مش تمرين تصريف."** Board **`B04-contrast`** incorrect assumption visibly crossed then real observation highlighted without color-only meaning.
- Check (fresh mini-situation): **"في صورة تانية فيه كلب نعسان. صاحبك قال It's sad، وإنت عارف إنه بس tired. أنهي تصحيح مناسب؟"** `It isn't sad; it's tired.` (correct), `It's sad and excited.`, `Its name is Sad.` Wrong feedback differentiates correction vs name. This is **contextual comprehension**, not certification of `its` or negative-`be` production.

### S05 — `advice-close`: meaning and polite finish

- `s05-replay`, Otti: **"في آخر الحوار Leo اتطمن وطلب مساعدة صغيرة. اسمع إيه المشكلة وإيه نصيحة Maya."** Board **`B05-neutral`** simple two-person exchange with empty issue/answer boxes; play `advice-and-close`.
- `s05-nothing`, Otti: **"Maya سألت Is everything okay? وLeo قال Nothing is wrong؛ يعني مفيش مشكلة. سمعنا nothing في جملة واحدة معناها واضح من الموقف، مش بنفتح درس طويل عن النفي."** Board **`B05-status`** "Is everything okay?" → "Nothing is wrong."
- `s05-advice`, Otti: **"Leo قال Can I ask for advice? يعني ممكن آخد نصيحة؟ Maya قالت Just say hello and smile؛ نصيحة بسيطة لأول يوم. مش مطلوب منك تقول advice في تدريب الكلام النهائي، لكن تفهمها لما تسمعها."** Board **`B05-tip`** situation → small tip → easier next move; visible relationship is *reason for advice*, not random cards.
- `s05-close`, Otti: **"وفي الآخر Leo قال Thank you! I'm not afraid now. I'm feeling really good، وودّعوا بعض. لاحظ الفرق بين قلق أول الحوار وراحته في الآخر."** Board **`B05-change`** before/after story arc with arrows from mild worry to comfort, replay safe after audio.
- Check (changed context): **"صاحبك قلقان قبل أول كلاس وطلب advice. أنهي جملة نصيحة بسيطة مناسبة؟"** `Say hello and introduce yourself.` (correct), `Tell everyone to go home.`, `Don't say your name.` Record receptive choice.

### S06 — `read-new-note`: separate *reading evidence* (not audio transcription)

New on-screen independent printed class note, **not read aloud verbatim by Otti before the learner answers**:

> **WELCOME TO ENGLISH CLASS**  
> Please write your name on the card.  
> Introduce yourself to one person.  
> Thank you!

- `s06-set`, Otti: **"دلوقتي مش هنسمع تسجيل. قدامك ورقة قصيرة جديدة من الكلاس. اقرأها بنفسك، وبعدها اختار المفروض تعمل إيه."** Board **`B06-note`** paper notice displayed legibly with accessible text, not an automatically voiced answer.
- Check: **"طبقًا للورقة، مطلوب تعمل إيه؟"** `Write your name and introduce yourself.` (correct), `Buy a notebook and leave.`, `Write your age and job.` Feedback quotes the two action clauses after choice. This checks *reading* separately; Otti reading the notice aloud beforehand invalidates independent reading evidence. Reading accessibility narration is allowed on demand, but annotate evidence as **supported**, not unaided.

### S07 — `fresh-speaking`: changed context and phrase-by-phrase truthfulness

- `s07-new-person`, Otti: **"دلوقتي هتقابل شخص جديد اسمه Sam في مكان تاني. من غير جمل ظاهرة على البورد، سلّم عليه، قل اسمك، اسأله عن حاله، ورد عليه بأدب، واختم الحوار بطريقتك. أنا Sam وهستنى كلامك."** Board **`B07-clear`** subtle empty conversation stage; no target transcript or answer-bearing examples.
- Otti (Live teacher) elicits **independent actual spoken turns**, repairs lightly in Arabic if necessary, accepts meaningful alternatives, and decides whether a real greeting/name/wellbeing/closing exchange happened. Repeating `Okay`, silence, `Bye` loops or reading back teacher lines **must not pass**.
- **Five exact productive phrase roles:** `Good morning`, `How are you?`, `pretty good`, `really good`, `Thank you`. Natural replies may use either `pretty good` OR `really good` but shouldn't unnaturally force both into the same turn. The product needs **separate changed-context opportunities**, e.g. first-day meeting, then "you just finished a nice short class—how do you feel now?" to elicit stronger `really good` in another turn. Keep two evidence channels:
  1. `communicationPassed`: meaningful encounter (real Live teacher judgement with learner turn count).
  2. `phraseEvidence[sourceId]`: **observed independently** / **supported** / **not-evidenced**. If a valid alternative was spoken, the encounter can pass but don't mark that exact locked phrase mastered; retrieve naturally later or seek explicit revised owner criterion.
- For two productive **words** `excited` and `feeling`, invite a normal after-class personal-feelings turn `I'm feeling excited` in a **different** setting; log independently spoken use, allow equivalents for social success without falsely filling those two exact-word slots. If the source owner decides to defer productive evidence, revise lifecycle/role only through owner-controlled source changes.
- Required counterexamples: silence, `Okay` alone, `Bye, bye, bye`, name-only, valid paraphrase, different wellbeing answer, one supported imitation, later fresh independent retry, microphone failure, interrupted Gemini reply.

## 3. Bespoke SVG/board production — **real design specs, product implementation pending**

**Important separation:** This Markdown is an **authored SVG storyboard/production specification**, **not a rendered SVG image or a verified EnglishLive React/SVG component**. Existing product bespoke art component is `src/lessonScenes/a1/A1FirstMeetingVisual.tsx`; the producer must implement new stateful semantics **there** and register in `src/qa/lessonQaVisuals.ts`. Don't add a second renderer to the curriculum repo.

| Semantic SVG state | Content/graphic meaning | Exact reveal | Portrait vs landscape / alt text |
| --- | --- | --- | --- |
| `B01-neutral` | Two blank speech outlines and an "ear"/play signal; no source item shown | Before full listening | Portrait two vertical avatars with a 44px play/replay tap area; landscape left/right. Alt: "Two unnamed speakers; listen before choosing." |
| `B02-greet` | Sunrise above Maya's speech bubble; Leo's Hi bubble connected by a greeting arrow | **After** `s02-greet` begins speaking | Small upright two-bubble flow; landscape side by side. Alt: "Maya greets Leo in the morning; Leo replies Hi." |
| `B02-names` | Identity cards show `I'm Maya` and `My name is Leo` beside connected people, not a grammar grid | After `s02-name` starts | Stack cards vertically / horizontally; independent English bidi isolation. |
| `B03-replies` | Two non-ranked speech bubbles: `pretty good` vs `really good`; question spans both | After source clip; only with `s03-answers` | Vertically adjacent answers / two columns. Alt: "Two natural replies to How are you?" |
| `B03-feelings` | Two simultaneous small state marks "excited" and "a little afraid" attached to same Leo node | After `s03-feelings` | Never show a mutually-exclusive emotional meter; both feelings may coexist. |
| `B03-intonation` | Rising pitch contour question vs steady thank-you contour | With Otti's spoken practice; no fake pitch analysis | Stroke patterns plus readable labels; reduced-motion static. |
| `B04-unrevealed` / `B04-photo` | Initially covered frame, later simple vector cat photo, labelled `its name is Coco` | Only **after** applicable listening assessment, during `s04-photo` | Photo not visible as MC answer ahead of time; portrait cat crop keeps caption outside art. Alt: "A photo of a cat named Coco." |
| `B04-contrast` | Maya's "sad?" misconception and Leo's correction "isn't sad → tired" as visibly sequential cards | `s04-correction` | Avoid color-only correctness; a crossed guess then an arrow to correction. |
| `B05-tip` | Small worry icon → Leo requests advice → Maya suggests a greeting → relief | Only with `s05-advice` | 3 vertical connected steps vs 3 horizontal; meaning-first icons, not emoji wallpaper. |
| `B05-change` | Leo at beginning "afraid" → later "not afraid" (same person, visual change) | During `s05-close` | Keep arrow labels short and visible at 320px. |
| `B06-note` | Printed independent welcome note with accessible selectable text alongside a simple paper/envelope SVG frame | Before reading question; no spoken textual answer | Text remains real HTML for selection/accessibility; svg only decorates semantic note. |
| `B07-clear` | Person Sam + attentive Otti with blank learner reply space | At final Speaking | No target words or progress-hint carrying hidden answers. |

**SVG semantic wireframe example** (designer reference; **not** product code): `greeting → name → wellbeing` appears incrementally as three nodes connected by arrows; before audio these exact captions are **not present**. Use art with `role="img"`, `aria-labelledby`, a meaningful `<title>`, no overflow, visible text labels. For photo: use simple path/ellipse cat illustration rather than external stock photos, with paper-frame geometry and a real text caption outside SVG for accessibility.

**Visual QA requirements:** 320×640, 400×860 and 1280×900; every scripted beat plus audio loading/playing, all MC question/correct/wrong, reading note, final Speaking/listening/complete, interrupted/error, overflow/Otti-safe-zone, RTL-English punctuation, low-height, touch targets. Build frame matrices from the registered lesson, **not a hand-curated subset**. Prior #54 green 156 frames relate to **old source** and cannot certify these new states.

## 4. Audio ↔ teaching ↔ SVG synchronization contract

```text
scene.enter
  -> Otti READ(speechId) + show non-spoiler board state
  -> Gemini Live PCM audible start/end
  -> wait until teacher PCM queue actually drains
  -> if beat.audioClipId: close learner mic BEFORE loading
      -> load audited WAV -> SEEK approved start -> audio playing
      -> turn badges/time-synced transcript from real word timestamps
         (full transcript hidden until first-listen response)
      -> end only after audible approved clip boundary
      -> hide playing UI / restore mic only when this scene allows it
  -> advance exactly ONE authored beat
  -> last beat -> question visible (no keyed reveal)
  -> board click -> store correct/incorrect
  -> Otti READ exact right/wrong explanation + wait for PCM drain
  -> scene advance
  -> final speaking Live turns -> teacher evidence audit -> completion tool
```

Stable IDs and timestamps must be source derived:
- **Dialogue** is the exact reviewed candidate JSON; **audio** generated once from an independently approved edition; **turn/clip milliseconds** are audited from that delivered WAV, never inferred by English word count.
- **Otti READ** is separate Gemini Live narration; no pre-rendered teacher recording is required by current architecture. Teacher lines are still explicitly authored and mapped beat-to-board.
- **SVG reveal** is linked to exact scene/beat/feedback state and audible teacher events; **no fake `setTimeout` pacing**. A spoken example cannot lead/lag a caption unpredictably without QA.
- **Transcript** initially hidden from first listen, then selectable after answering; during replay, only the word/turn actually heard is highlighted; never infer source-turn boundaries from arbitrary fixed durations.
- **Interruption / timeout / autoplay failure** keeps the lesson blocked, mic closed while media is loading/playing, offers retry; cannot count a clip as heard or trigger duplicate `next`.
- **Validation:** `approved:true` only if all clip bounds align with included turn bounds, turn order monotonic/non-overlapping, URLs secure and exact output edition matched; also manually audition on device for no spill/cropped phonemes.

## 5. Explicit source scope: all **12 previously escalated rows are addressed as candidates**, none silently approved

| Exact source ID | New proposed meaningful evidence | Scope/quality concern still requiring owner ruling |
| --- | --- | --- |
| `ability.gse_all_objectives.gse.adult.2022.a1.p09.007` | `S06` independent short printed welcome note + reading choice | Not proven by audio; reading check must remain unspoken/unaided |
| `egp.1741163708329x778951051617750700` | `T12` Coco **isn't** sad, `T16` I'm **not** afraid; `S04/S05` reasoned explanation | Bounded meaning only; avoid negative `be` conjugation lecture |
| `oxford.o3000.p01.012` advice | `T14–T15` authentic advice request and simple answer; `S05` recognition | Receptive, not required to produce the word |
| `oxford.o3000.p01.013` afraid | `T06/T16` nervous → reassured; `S03/S05` | Receptive understanding, not a feelings-table target |
| `oxford.o3000.p02.011` excited | `T04/T06` full dialogue + `S03`; candidate *different-context* spoken elicitation in `S07` | **Productive required**: narrative mentions ≠ learner-produced |
| `oxford.o3000.p02.034` feeling | `T04/T16` + `S03`, separate `S07` elicitation | **Productive required**, track observed wording accurately |
| `oxford.o3000.p02.160` its | `T10` "**Its** name is Coco", visible cat + text in `S04` | Receptive meaning; do not mistake `It's` for `its` or claim auditory phoneme contrast |
| `oxford.o3000.p03.007` nothing | `T14` "nothing is wrong", `S05` | Receptive phrase meaning; not an idiom-heavy grammar lesson |
| `oxford.o3000.p03.064` photograph | `T10/T11` physical cat photo and `S04` board | Receptive; keep photo only if story feels natural at A1 |
| `oxford.o3000.p03.136` sad | `T11/T12` assumption/correction with art | Receptive contrast |
| `oxford.o3000.p03.274` tired | `T12` correction with cat, `S04` | Receptive; not necessarily learner speech |
| `oxford.o3000.p04.100` yourself | `T08` quoted classroom instruction and `S06` printed instruction | Receptive comprehension, not reflexive pronoun chapter |

**Other 24 source IDs remain mandatory, not erased by focusing on the 12:** 7 additional ability rows are served by name/greeting, slow articulated full/replay, independent repetition/spoken evidence, and bounded social interaction; 5 productive phrase rows require their separate `S07` evidence ledger; 7 other grammar rows use identity/`I'm` chunks contextually without taxonomy drills; `be/people/thanks` have explicit `T01–T07`/teaching contexts; 2 pronunciation strands need real auditory recognition and actual spoken intonation evidence. `S06` alone does not satisfy every ability. The **authoritative 36-item coverage JSON is deliberately unchanged**; mapping `escalate` → `teach` and modifying immutable Stage-06 source/semantic slots require an owner-reviewed decision on **each** relevant item.

## 6. Producer handoff — exact product integration points

On [existing product PR #54](https://github.com/addvaluewithai-hub/englishlive/pull/54), after source/owner design acceptance, the **current producer** should synchronize:

1. `src/lessonScenes/a1/listeningAudioPilot.ts`: new 18 immutable turns/6 clip IDs, `approved:false` and **all times/URLs null** until actual paid job and media review. Old `pilot02` must not be used with expanded source.
2. `production/a1-u1-l01/gemini-tts-request.json`: replace only with **exact newly approved edition** from candidate, no job run without specific spend permission.
3. `src/lessonScenes/a1/listeningTeacherPilot.ts` and `listeningTeacherScript.ts`: 7 mapped scenes, teacher lines/boards, no spoiler before MC, feedback in both correct/wrong branches, fresh Speaking evidence.
4. `src/lessonScenes/a1/A1FirstMeetingVisual.tsx`, `src/qa/lessonQaVisuals.ts`, `src/qa/lessonQaRegistry.ts`: bespoke SVG states driven by actual stable beat IDs and auto-derived fixture cases; no duplicate app/player.
5. `src/audio/LessonAudioController.ts`, `src/lessonScenes/SceneLessonRuntime.ts`, `src/screens/SceneLessonScreen.tsx`: preserve PCM/audio/mic interruption gates; ensure board reveals and transcript visibility match sound.
6. `scripts/test-a1-listening-pilot.mjs`, `scripts/test-a1-content-coverage.mjs`, QA docs/ledger: tests below, screenshot artifacts and unresolved owner decisions.

**Acceptance matrix after actual implementation**:
- **Static**: 18 exact spoken lines match approved request, all source IDs mapped by named scene/beat, no extra productive word promoted, six named clips map existing turns, all new board IDs/visual states registered, no answers visible before first MC, independent written reading text.
- **Negative fixtures**: missing/unapproved recording; wrong URL; bad/out-of-order/overlapping/empty clip offsets; audio decoder/seek/autoplay error; interrupt during loading; Otti PCM overlap; duplicate end callbacks; wrong answer; timeout; missing mic permission; empty phrase evidence.
- **Audio**: original WAV listened to at normal/slower pace, proper Coco/Leo name pronunciation, `its`/ `it's` text alignment, no clip bleeding, reviewed source word timestamp/VTT and both-speaker diarization; timed turn UI exact, not mock-only.
- **Learning**: changed-context MC, A1 comprehension trial after full 18 turns, independent reading, two distinct wellbeing spoken contexts, strong and weak learner responses, real Live Otti repair, no scripted final answer visible.
- **Visual**: run lesson frames at all 3 viewports plus registered B1 regression; open/critique contact sheets and list before/after repaired defects. Old PR #54 screenshot run becomes historical.
- **Release**: `coverage_gate.py check` and eventually `ready` when source owner rulings + all six QA gates accepted; independent reviewer verdict then owner merge/deploy. **No gate considered passed by drafting this spec.**

## 7. Self-critique and immediate next decision

This draft deliberately demonstrates that **the 12 items can be placed in a coherent first-day-class encounter**, contradicting the earlier overly eager suggestion to relocate most of them. **But placement is not proof of learning**. 140 words + 18 turns may overload brand-new learners; the photograph of a cat, despite fitting `its/photograph/sad/tired`, could still be a narrative detour from *greeting/name/wellbeing*. `advice` may be more complex than needed; its presence is not a win if it distracts. `S06` adds genuine reading instead of pretending listening proves text recognition. Productive roles still require real fresh speech and may be unmet for perfectly acceptable learner paraphrases.

**Recommendation for editorial review:** approve or adjust this *source design* first (especially A1 story naturalness and length), then settle the **exact 12 semantic/lifecycle evidence decisions** in the existing review PR; hand confirmed texts/boards to the reserved U1-L01 product producer; approve a **specific final TTS edition + price cap** separately. Nothing in this spec requests starting U1-L02, paid synthesis, rewriting locked master data, claiming screenshots, or releasing a lesson.
