# ENGLOTTI — MASTER WORKFLOW CONTROL

> **One-file command center / نقطة الدخول الوحيدة لأي Agent جديد.**
>
> **Agent cold start:** If this file is attached to a new conversation and the user says "افتح" أو "كمل" أو يرسل الملف فقط، اقرأه كله، ثم نفّذ **STEP 0 → STEP 1 → STEP 2** من غير ما تطلب إعادة شرح المشروع. لا تسأل سؤالًا إلا لو فيه قرار مالك/ترخيص/تكلفة لا يمكن حسمه من الأدلة. نفّذ ما تسمح به الصلاحيات والأدلة، وسلّم نتيجة فعلية. لا تدّعِ تنفيذًا أو نجاحًا لم يحدث.
>
> **القاعدة الحاكمة:** هذا الملف هو **لوحة القيادة + تعليمات اختيار الخطوة التالية**. لكن بيانات المنهج المعتمدة موجودة في `english-course`، وكود التطبيق في `englishlive`، ومهام Practice في `speaking-practice`. لا تستخدم نسخة قديمة من لوحة القيادة بدل الرجوع للمصادر الحية.

## 0) CONTROL PANEL — الحالة التشغيلية

**آخر مراجعة للمعلومات من GitHub:** `2026-10-17` (Africa/Cairo).  
**المسار المرجعي المشترك:** `addvaluewithai-hub/english-course/ENGLOTTI_MASTER_WORKFLOW.md` على `main` بعد دمج PR التأسيس. **لا تستنتج حالة الدمج من هذا النص**؛ تحقّق مباشرة من GitHub في STEP 0. الملف قد يكون مرفقًا أو على فرع PR قبل ظهوره على `main`.

```yaml
control_version: 1
last_verified_date: 2026-10-17
shared_control_file_installed_in_repo: true  # verified on english-course/main 2026-10-17; reverify each session
primary_lane: LEARN                         # LEARN | PRACTICE
selected_level: A1
current_role: LESSON_REVIEWER               # LESSON_PRODUCER | LESSON_REVIEWER | FIVE_LESSON_REVIEWER | UNIT_REVIEWER | PRACTICE_REVIEWER | OWNER_DECISION_WAIT
current_step: OWNER_DECISION_WAIT
active_lesson: A1/U1-L01
active_lesson_title: "Hello. I'm …"
active_product_pr: https://github.com/addvaluewithai-hub/englishlive/pull/54
active_pr_state_at_verification: OPEN_DRAFT
owner_decision_required: true
owner_decision_topic: "12 U1-L01 source-scope rulings; 2 P1 pedagogical review fixes; explicit pilot02 paid TTS approval"
next_permitted_action: "Owner reviews 12-ID decision brief and P1 counterexamples; existing U1-L01 producer revises after rulings, then independent re-review. No paid TTS, semantic-lock edit, merge or U1-L02 without approvals."
next_not_yet_authorized_lesson: A1/U1-L02

learn_progress:                # canonical lesson status; verify on every start
  A1: {slots: 62, done: 0, in_progress: 1, not_started: 61, pilot_only: 0}
  A2: {slots: 83, done: 0, in_progress: 0, not_started: 83, pilot_only: 0}
  B1: {slots: 85, done: 0, in_progress: 0, not_started: 84, pilot_only: 1}
  B2: {slots: 95, done: 0, in_progress: 0, not_started: 95, pilot_only: 0}
  C1: {slots: null, blocked: true, reason: "lesson design not authorized"}
  C2: {slots: null, blocked: true, reason: "lesson design + commercial permission gates"}

learn_review_cycle:
  scope: A1
  review_every: 5
  review_batch: A1-BATCH-01
  canonical_lessons: [U1-L01, U1-L02, U1-L03, U1-L04, U1-L05]
  produced_with_evidence: 0     # fully authored/implemented drafts passing their local evidence checklist
  individually_ai_reviewed: 0
  group_ai_reviewed: false
  batch_verdict: NOT_DUE       # NOT_DUE | DUE | CHANGES_REQUESTED | APPROVED | OWNER_BLOCKED
  accepted_done_lessons: 0
  next_review_trigger: "Five lessons each produced AND independently lesson-reviewed; block lesson 6 until group review verdict."

practice_lane:
  mode: STANDBY                # separate workstream; NEVER treated as Learn lessons
  current_a1_core_missions: 8
  editorially_reviewed_core: 8
  production_runtime_mirrored_at_last_review: 5
  live_audio_publication_gates: PENDING
  automatic_five_lesson_trigger: false  # Practice is mission-based/nonlinear

release_policy:
  self_merge_or_self_deploy: false
  paid_audio_without_explicit_approval: false
  silent_change_to_locked_curriculum: false
  mark_done_without_owner_acceptance: false
```

### معنى الأرقام (مهم جدًا)

- **`slots`:** عدد الدروس الرسمية المسجلة في المنهج؛ **مش** دروس منتجة.
- **`produced_with_evidence`:** درس له محتوى تعليمي وتنفيذ قابل للفحص وأدلة QA فردية فعلية؛ قد يظل Draft، ولا يعني أنه منشور.
- **`individually_ai_reviewed`:** عدد الدروس التي حصلت فعلًا على `LESSON_REVIEW_PASS` من مراجع مستقل، مع أدلة وإصلاحات لازمة منفذة؛ لا يعني أن الطالب أتقنه أو أن صاحب المشروع وافق عليه.
- **`group_ai_reviewed`:** المراجع فحص **الخمسة كمنظومة واحدة**، وليس خمس مراجعات منفصلة.
- **`done`:** فقط القيمة الموجودة في صف الدرس بملف Status بعد أدلة متكاملة و**اعتماد صريح من المالك**. Pilot وDraft وCI ناجح ≠ Done.
- **`blocked`:** توقف مبرر؛ **ليس** تصريحًا بتخطي الدرس أو اختيار درس لاحق.
- احسب أرقام اللوحة من GitHub في كل جلسة؛ لا تزود عدادًا اعتمادًا على كلام سابق أو توقع أو عدد PRs.

## 1) REPOS — مين صاحب إيه؟

| Repo | دوره الحقيقي | إيه اللي تفتحه |
|---|---|---|
| [`addvaluewithai-hub/english-course`](https://github.com/addvaluewithai-hub/english-course) | **المنهج المرجعي، Semantic Locks، Lesson Briefs، أسماء الدروس وترتيبها، Status الستة، توجيه Agents، قرار مراجعة دفعة Learn** | `AGENTS.md`, `START_HERE.md`, `CURRENT_STATE.md`, `interactive-content-production/AGENTS.md`, `WORKFLOW.md`, `LESSON_CONTRACT.md`, `status/<LEVEL>.md`, `coverage/<LEVEL>/<LESSON>.json` |
| [`addvaluewithai-hub/englishlive`](https://github.com/addvaluewithai-hub/englishlive) | **تطبيق Englotti**، الشاشات، Otti Live، تشغيل Listening، Speaking، Playwright/Visual QA، أدلة التنفيذ | `AGENTS.md`, `README.md`, PR الدرس، ملفات `production/.../QA_STATUS.md` والـfixtures والتصوير والاختبارات |
| [`addvaluewithai-hub/speaking-practice`](https://github.com/addvaluewithai-hub/speaking-practice) | **Practice missions**: الحوارات الواقعية المعتمدة والـsemantic graphs والـcorrection/hints والمراجعة التحريرية | `README.md`, `docs/README.md`, `docs/AUTHORING_QA_V1.md`, `docs/PRACTICE_MAP_V1.md`, `docs/practice-map/<LEVEL>.md`, `missions/` |
| [`addvaluewithai-hub/gemini-tts`](https://github.com/addvaluewithai-hub/gemini-tts) | **مصنع الصوت المُسجَّل** عند الاحتياج وبعد الموافقة | job definition وWAV والتوقيتات الفعلية وVTT والمخرجات المعتمدة |

**حدود صارمة:** Learn لا يغيّر Practice بصمت؛ Practice يرجع إلى English Course لاختيار لغة مناسبة لكنه لا يكرر منهج Learn؛ EnglishLive لا يخترع عناصر منهج معتمدة. **النسخة المرجعية الحية لكل مجال أعلاه لها أولوية على ملخص هذا الملف.**

## 2) FIRST 60 SECONDS — تعليمات فتح الملف في محادثة جديدة

الـAgent ينفذ الخطوات بالترتيب. لا يستنتج دوره من عنوان المحادثة.

### STEP 0 — Verify / Sync

1. اقرأ هذا الملف كله أولًا. حدّد `primary_lane` و`current_role` و`active_lesson` و`current_step` من لوحة التحكم، **كتوقع مبدئي وليس حقيقة نهائية**.
2. افتح النسخ الحية لـ`AGENTS.md` في `english-course` و`englishlive`، و`README.md` الخاص بـ`speaking-practice`. افتح `ENGLOTTI_MASTER_WORKFLOW.md` من `english-course/main` **لو أصبح مثبتًا هناك**؛ لو موجود، ابدأ بالأحدث وقارن التغييرات، ولا تكتب فوق تغييرات Agent آخر.
3. افتح ملفات `interactive-content-production/status/{A1,A2,B1,B2,C1,C2}.md` واحسب `done/in-progress/claimed/review-needed/pilot-only/not-started` فعليًا. راجع الـmanifest و`delivery_content_production_authorized` لكل مستوى قبل أي إنتاج.
4. ابحث عن Open/Draft PRs للدرس النشط في **English Course وEnglishLive**. التحقق من الـStatus وحده غير كافٍ للحجز الآمن. راجع أحدث Commit وأدلة QA وأي Reviewer comments.
5. لو `primary_lane=PRACTICE`، اقرأ خريطة الـMissions وسجل مراجعاتها، ولا تستخدم `production_status.py next A1` لاختيار Mission لأن Practice **غير خطي**.
6. حدّث لوحة التحكم **في نسخة العمل** وفق الأدلة. كل عنصر لا يمكن التحقق منه يوضع `UNVERIFIED`؛ لا تُدّعِ أن الأرقام محدثة. لا تُغيّر الملف المشترك على `main` مباشرة أو تتجاوز PR approval.

**أوامر مساعدة عند وجود shell في `english-course`:**

```bash
python3 interactive-content-production/tools/production_status.py validate
python3 interactive-content-production/tools/production_status.py next A1
python3 interactive-content-production/tools/coverage_gate.py check A1 U1-L01
python3 interactive-content-production/tools/coverage_gate.py ready A1 U1-L01
```

الأوامر تتغير حسب المستوى والدرس. `next` قد يرجع `IN_FLIGHT_REVIEW`، و`ready` قد يفشل لأسباب تربوية/صوتية/اعتماد؛ **لا تعتبر ده Bug ولا تتحايل عليه**.

### STEP 1 — Choose ONE active role (الأولوية من فوق لتحت)

| الشرط الذي تكتشفه من GitHub | الدور القادم | المطلوب فورًا |
|---|---|---|
| قرار Semantic Lock/ترخيص/شراء صوت/اعتماد مالك مفقود ويمنع إكمال الدرس النشط | `LESSON_REVIEWER` مع `current_step=TRIAGE_OR_OWNER_DECISION` | تحليل الخيارات مع الأدلة ورفع قرار محدد للمالك؛ **لا تخترع الموافقة ولا تتخطى الدرس** |
| خمس دروس متتالية حصلت على `LESSON_REVIEW_PASS` مع أدلة كافية، ولا توجد مراجعة دفعة معتمدة | `FIVE_LESSON_REVIEWER` | أوقف فتح الدرس السادس؛ نفّذ بروتوكول STEP 5 |
| درس مكتمل الإنتاج لكنه ينتظر تقييمًا تربويًا مستقلًا | `LESSON_REVIEWER` | STEP 4 ثم verdict واضح |
| نهاية Unit وصلنا إليها ومراجعتها غير معتمدة | `UNIT_REVIEWER` | STEP 6؛ *إضافة* إلى مراجعة الخمسة وليست بديلًا |
| درس عليه PR/حجز مستمر | `LESSON_PRODUCER` أو `LESSON_REVIEWER` وفق المرحلة | استكمل **نفس** الدرس في حدود الحجز والصلاحيات؛ لا تفتح نسخة منافسة |
| الدرس السابق مقبول ولا توجد مراجعة دورية معلّقة أو حجز | `LESSON_PRODUCER` | اختَر أول درس غير منجز رسميًا من Status/`next`، ثم STEP 3 |
| المستخدم طلب Practice صراحةً أو غيّر `primary_lane` إلى `PRACTICE` | `PRACTICE_REVIEWER` أو منتج Mission حسب حالة المصدر | STEP 7، بمسار مستقل |

> **حل تعارض الأولويات:** سلامة الملكية/الصلاحيات أولًا. لا تفتح درسًا جديدًا فوق PR مفتوح محجوز. لو تعذر الاختيار بسبب نقص معلومة، اقرأ أكثر وقدّم تقريرًا محددًا بدل حدس. Agent جديد لا يستلم حجز Agent آخر تلقائيًا.

### STEP 2 — Act, do not only summarize

بعد تحديد الدور:

- نفّذ الخطوة الممكنة الآن: اقرأ المصدر المحدد، اعمل مراجعة فعلية، أصلح في Branch مسموح إن كان مأذونًا، أو جهّز Decision Brief مدعوم بالدليل لو يحتاج قرارًا من المالك.
- لا تُحوِّل كلمة "كمل" إلى إذن بإجراء Merge/Deploy أو دفع تكلفة API أو تغيير منهج Locked أو نشر دروس.
- اكتب Handoff في آخر الملف **عند العمل على نسخة قابلة للتحديث**، وحدّث حقول `current_role`, `current_step`, `active_lesson`, `next_permitted_action`, `learn_progress` و`learn_review_cycle` بعد التحقق.
- إذا الملف مرفق فقط داخل Chat أو لم يُدمج على `main` بعد، فالتحديث يظل **محليًا/في PR** ولا يصبح مرجعًا مشتركًا لبقية Agents. بعد التأسيس، حدّث نسخة GitHub المعتمدة عبر PR وHandoff. لا تدّعِ أنه متزامن قبل التحقق من الدمج.

## 3) ROLE: LESSON_PRODUCER — منتج درس واحد

**المدخل:** درس محدد في Status، Brief رسمي، Semantic Locks، Source/Coverage IDs، ولا يوجد حجز متضارب.  
**القراءة الملزمة:**

1. `english-course/AGENTS.md`, `START_HERE.md`, `CURRENT_STATE.md`.
2. `english-course/interactive-content-production/AGENTS.md`, `WORKFLOW.md`, `LESSON_CONTRACT.md`, `FRAME_QA.md`.
3. `english-course/.agents/skills/produce-interactive-english-lesson/SKILL.md`.
4. Status المستوى و`curriculum/levels/<level>/manifest.json` وLesson Brief المعتمد وSemantic Locks وCoverage Ledger ثم `coverage/<LEVEL>/<LESSON>.json`.
5. `englishlive/AGENTS.md`, Product PR وحالة تطبيق Otti والـQA إن وُجدت.

**الخطوات (حافظ على الترتيب):**

1. اعمل claim آمن للدرس في Status وDraft PR/Branch منفصل؛ راجع PRs أولًا. التزم بموافقات النشر والإنتاج المحدود.
2. راجع **كل Source ID بمعناه ودوره الحقيقي**: مطلوب إنتاجي؟ للفهم فقط؟ داعم؟ مؤجل بإذن؟ لا تضع عنصرًا غريبًا في الدرس لمجرد رفع العدد. أي تعارض يُصعَّد للمسؤول.
3. اكتب خطة تربوية متصلة: هدف الطالب، الموقف، Listening إذا مناسب للدرس، شرح Otti، Board/Beats، MC مع تفسير الصح والغلط، وفرصة Speaking مستقلة إذا مطلوبة. لا تجعل AI يرتجل المنهج.
4. في الصوت المسجّل استخدم Gemini TTS بالطلب/النسخة المراجعة فقط وبعد موافقة تكلفة/نطاق الإنتاج؛ راجع التسجيل الفعلي والتوقيتات `clipId`. Otti Live منفصل، وصوتاهما لا يتداخلان.
5. نفّذ الدرس في `englishlive` باستخدام النظام الحالي؛ اختبر تفاعل الطالب والـUI والصوت على أجهزة/أحجام مختلفة، لا تعتمد على Screenshot وحدها.
6. سجّل Evidence وفجوات حقيقية، ثم **سلّمه لمراجع درس مستقل STEP 4**؛ المنتج لا يمنح نفسه `LESSON_REVIEW_PASS`.
7. حدّث عداد `produced_with_evidence` فقط عندما تتوفر أدلة التعريف أعلاه، ولا تغيّر صف `done` قبل اعتماد المالك وإجراءات الـQA الإلزامية.

**تسليم المنتج:** Branch/PR + SHA + source mapping + script/audio refs + visual/contact sheets التي **فُتحت وفُحصت** + real Live test results + عيوب وأمور غير مجربة. فشل أي جزء لا يختفي وراء عبارة CI GREEN.

## 4) ROLE: LESSON_REVIEWER — مراجع ذكي لكل درس

**لا تحكم بالعدّ فقط.** راجع المصدر والتنفيذ كما يراه طالب حقيقي. حاول أن يكون Reviewer مستقلًا عن المنتج أو على الأقل بسياق/Checklists مستقلة مع Counterexamples.

1. طابق أهداف الـBrief وSemantic Locks والـCoverage Ledger مع ما يحدث فعلًا في شرح Otti/Listening/Board/MC/Speaking؛ سجل لكل Gap: Source ID، المشهد، أثر المشكلة، والدليل.
2. هل اللغة صحيحة وطبيعية ومناسبة لـCEFR؟ هل الأمثلة واضحة أم قفزات؟ هل المصطلحات معروضة في سياقها الصحيح؟ هل العناصر `receptive` تُعامَل غلط كـ`productive`؟ هل توجد عناصر مطلوبة سقطت؟
3. هل التقييم يقيس الهدف؟ **MC ≠ Speaking mastery**. جرّب الطالب الصامت، الإجابة الخاطئة، الإجابة البديلة الصحيحة، طالب يحتاج إعادة Listening، وطالب يتلقى Hint.
4. اسمع **التسجيل الفعلي** إن وُجد، وراقب Live Otti/الميكروفون/مقاطعات الصوت؛ عدم توفر الصوت يظل بند `NOT_TESTED`، مش PASS.
5. افتح حالات Screenshot الفعلية وعينة الحالات الأصلية على الموبايل الصغير والعادي والديسكتوب، لا تكتفِ بوجود ملفات.
6. اكتب ملاحظات إصلاح محددة، واطلب من Producer تعديلها؛ افحص الإصلاحات نفسها. اعتمد التحرير فقط لو نجح، واحتفظ ببوابات النشر/الصوت والمالك مستقلة.

**النتيجة:** واحدة من `LESSON_REVIEW_PASS` (مع حدود الاختبارات المعلنة)، `CHANGES_REQUESTED`، `BLOCKED_OWNER_DECISION`. اربط التقرير بالـPR وبهذا الملف. لا تُعرِّف `PASS` بأنه نشر نهائي.

## 5) ROLE: FIVE_LESSON_REVIEWER — المراجعة الذكية بعد كل 5 دروس

**قاعدة التشغيل:** راجع كل دفعة من **خمسة دروس متتالية في الترتيب الرسمي للمستوى** بعد أن تُنتج وتُراجع فرديًا. لا تجمع دروس A1 مع A2؛ ولا تعدّ الـPilot أو PR غير قابل للفحص درسًا مكتمل الإنتاج. عند إكمال خمسة، يجب التوقف قبل السادس حتى يصدر حكم دفعة واضح. لو خمسة لم يكتملوا، لا تضع `APPROVED`.

**أول دفعة A1:** `U1-L01, U1-L02, U1-L03, U1-L04, U1-L05`.  
**الدفعات التالية:** كل خمس خانات بالترتيب الرسمي، حتى إن عبرت حدود الوحدات. الدفعة الأخيرة في المستوى قد تكون أقل من خمسة. مراجعة نهاية الوحدة تُضاف ولا تُلغى.

**أسئلة Reviewer الإلزامية (لا يحلّها فحص JSON وحده):**

1. **Coverage عبر الخمسة:** هل كل Abilities / Phrases / Words / Grammar / Pronunciation المطلوب تقديمه هنا أُدخل بعمق مناسب ودور دلالي صحيح؟ هل شيء مهم سقط أو ظهر قبل ميعاده؟ أين دليل التعلّم، وأين مجرد تعرّض؟
2. **Progression:** هل في كل درس إضافة حقيقية مبنية على السابق؟ هل في قفزة صعوبة أو تكرار بلا فائدة؟ هل Student الانتقال بين مشاهد/دروس منطقي؟
3. **Retention & Retrieval:** هل رجعنا لما اتعلمه الطالب في درس سابق بشكل مفيد وفي سياق مختلف؟ هل يوجد اختبار نقل مستقل، لا مجرد تكرار الجملة المحفوظة؟
4. **Real communicative quality:** هل المواقف Listening طبيعية وOtti مدرس حقيقي مش فلاش كارد؟ هل Speaking يقيس استخدامًا جديدًا لا تلقينًا؟ هل الطالب يقدر يغلط ويتصلح من غير تعطيل؟
5. **Pedagogical consistency:** نبرة Otti، لغة الشرح المصرية، مستوى صعوبة الجمل، طول التسجيل، كثافة المعلومات، التدرج، التغذية الراجعة، واستخدام الصور البصرية.
6. **Evidence quality:** هل التقارير بنيت على مشاهدة/استماع/تفاعل فعلي؟ هل غابت تجارب على جهاز/Live provider؟ هل نجاح CI أُسيء تفسيره كتعلّم؟
7. **Adversarial pass:** اختبر حالات طالب A1 قوي وضعيف، رفض/صمت، بدائل صحيحة، Listening replay، MC wrong، انتقال Speaking، والتباس المصطلحات عبر الدروس الخمسة.

**مخرجات إجبارية:**

- تقرير واحد بعنوان `A1-BATCH-01 REVIEW`: لكل درس `PASS / FIX / BLOCKED` ومعه أقوى دليل.
- خريطة gaps/overlaps/tradeoffs عبر الدفعة، بعناصر source IDs وأماكن السكريبت والتفاعل والـPRs.
- قائمة إصلاحات ذات أولويات `P0/P1/P2`، لكل مشكلة Owner واضح وملف/Scene ومقياس إعادة الاختبار.
- `APPROVED` فقط بعد إعادة فحص الإصلاحات الحرجة وتوثيق الحدود. الموافقة البشرية والنشر/الصوت قرارات منفصلة.

**State transition:** `NOT_DUE → DUE → (CHANGES_REQUESTED ↔ RECHECK) → APPROVED` أو `OWNER_BLOCKED`. بعد `APPROVED` ومع عدم وجود Pending Unit/Owner gate يمكن البدء في الدرس السادس. إذا لم تنجح المراجعة، **لا تنتج الدرس التالي لتفادي تكرار نفس الخطأ**.

## 6) ROLE: UNIT_REVIEWER — مراجعة نهاية الوحدة

عند نهاية أي Unit رسمي، راجع هدف الوحدة ككل، وأداء Transfer الدرس الأخير إن وجد، وتغطية الأهداف عبر الوحدة. الدرس الخامس ليس بالضرورة آخر الوحدة؛ في A1 وحدة 1 تضم `U1-L01` حتى `U1-L07`، لذلك يوجد **Batch Review بعد L05** ثم **Unit Review بعد L07**. لا تفرض عدد دروس ثابتًا لكل وحدة. لو نتيجة وحدة/Batch متعارضة، لا تتجاوز الأشد خطورة.

## 7) PRACTICE LANE — منفصل لكن تحت نفس لوحة القيادة

- `speaking-practice` هو صاحب Mission map وAuthored canonical dialogue وsemantic graph وaccepted alternatives، وليس صاحب ترتيب دروس Learn.
- اقرأ `docs/README.md` ثم `docs/AUTHORING_QA_V1.md`, `docs/LANGUAGE_GROUNDING_AND_CANONICAL_DIALOGUE_V1.md`, وملفات الـMission المعني. ارجع للـEnglish Course لاختيار اللغة المناسبة دون فرض كل كلمات الدرس داخل Mission.
- افحص هدف المحادثة الحقيقي، السيناريو، الفروع، Level fit، التصحيحات، Dynamic Hints، Listening Preview، وأداء Gemini Live الحقيقي ببدائل وأخطاء وصمت/مقاطعات.
- حالة الثمانية A1 Core في آخر قراءة: محرَّرة ومراجَعة Editorially؛ ذلك **لا يعني** أن Gemini Live/audio والنشر أصبحا مكتملين.
- يمكن اعتماد **Batch Review لكل خمس Missions منتَجة** في Practice لاحقًا كسياسة مستقلة؛ لا تُعامل 5 Lessons و5 Missions كدفعة واحدة، ولا تفترض ترتيبًا دراسيًا خطيًا للـMissions.
- لا تغيّر `primary_lane` من LEARN إلى PRACTICE لمجرد إن درس Learn متوقف؛ اعرض سبب التوقف أولًا والتزم بأولوية المستخدم.

## 8) FIXED CHECKPOINTS & SELF-CRITIQUE

كل تسليم من أي Role يجب أن يجيب بأدلة لا بالثقة الذاتية:

- ما الحقائق المؤكدة؟ ما **غير مؤكد/غير مجرب**؟ ما الذي أخطأت فيه المراجعة الأولى وتم تصحيحه؟
- ما الحالات المضادة (counterexamples) التي قد تكسر حكمي؟ هل أعدت اختبارها بعد الإصلاح؟
- هل كل `Source Item` أخد دوره الصحيح، أم حوّلناه إلى فلاش كارد لمجرد إرضاء العد؟
- هل أدلتنا تثبت **جودة تعليم** أم مجرد جودة بناء/تصوير؟
- هل الإجراءات متوافقة مع `manifest`, Semantic Locks, owner approvals, open claims, scope، وترخيص المحتوى؟

الفحص الآلي مفيد للحفاظ على سلامة الأدلة والروابط وCI؛ لكنه **ليس الحكم النهائي على جودة الدرس**. والمراجعة الذكية نفسها قد تخطئ، لذلك لازم تفحص عينة مضادة، وتشرح حدودها، وتطلب قرار المالك عند تعارض المصدر.

## 9) HOW TO UPDATE THIS SINGLE FILE — تحديث الـControl بعد كل خطوة

**المالك الإداري للنسخة المشتركة:** `english-course/main`. لا تنشئ/تعدّل Main مباشرة؛ استخدم PR لإدراج الملف أول مرة ثم تحديثات منسقة عبر PRs مع مراجعة التعارضات. يجب أن تكون التحديثات متسقة مع ملفات Status والـPRs المقابلة.

في نهاية أي خطوة أو Handoff:

1. غيّر `last_verified_date` **فقط بعد GitHub verification**، لا بناءً على تاريخ فتح المحادثة.
2. حدّث العدادات من Status (لا تعدّ من ذاكرة المحادثة)؛ ثم حقول الدفعة من تقارير فعلية ومستقلة.
3. حدّث `current_role`, `current_step`, `active_lesson`, `active_product_pr`, `owner_decision_required`, `next_permitted_action`.
4. أضف سجلًا مقتضبًا لـ`HANDOFF LOG` أدناه: الأدلة/PR/commit، ما تم، ما لم يتم، مَن التالي، وما الذي يمنع الاستمرار.
5. إن لم تستطع تعديل نسخة GitHub المعتمدة، أعِد نسخة ملف محدثة كمرفق واذكر أنها **غير متزامنة**؛ لا تزعم أن باقي Agents سيرون التغيير.
6. بعد مراجعة الدفعة، ارجع مباشرة إلى `STEP 1` لاختيار الدور القادم، ولا تضف قرارات ضمنية.

**قاعدة تنازع التعديلات:** حدّث من أحدث `main` ثم تحقق من الـPRs والحجوزات قبل كل كتابة، ولا تعمل overwrite لتعديل Agent آخر. ملف Markdown مش lock موزع؛ Claims في Status/PR لازمة.

## 10) CURRENT NEXT ACTION — المهمة الفعلية عند أول فتح

**الحالة المؤكدة في 2026-10-17، وتتطلب إعادة التحقق:**

- `A1 U1-L01 — Hello. I'm …` على `englishlive` في **Draft PR [#54](https://github.com/addvaluewithai-hub/englishlive/pull/54)**؛ Status داخل `english-course` = `in-progress` وليس `done`.
- المصدر يحتوي **36 Source IDs**؛ خمسة Phrases مستهدفة معروفة في خطة المنتج، لكن توجد **12 قضية تحديد موضع/نطاق** لم يصدر بشأنها قرار المالك.
- اقرأ أولًا: [`interactive-content-production/coverage/A1/U1-L01-REVIEW.md`](https://github.com/addvaluewithai-hub/english-course/blob/main/interactive-content-production/coverage/A1/U1-L01-REVIEW.md)؛ ثم `coverage/A1/U1-L01.json` ثم [`production/a1-u1-l01/QA_STATUS.md`](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/production/a1-u1-l01/QA_STATUS.md) في فرع PR #54.
- **Decision Brief أُعدّ للمراجعة ولم يُعتمد بعد:** [`U1-L01-OWNER-DECISION-BRIEF-2026-10-17.md`](interactive-content-production/coverage/A1/U1-L01-OWNER-DECISION-BRIEF-2026-10-17.md). يراجع الـ12 عنصرًا واحدًا واحدًا، مع بدائل، أثر على lifecycle، ومشكلتين تربويتين P1 (تسريب إجابة أول Listening، ونقص دليل Speaking مستقل للـ5 productive phrases). القرار النهائي للمالك؛ لا تغيّر locked source وحدك.
- **Session 2 QA / لم تُعتمد:** [`U1-L01-INDEPENDENT-QA-RECHECK-2026-10-17.md`](interactive-content-production/coverage/A1/U1-L01-INDEPENDENT-QA-RECHECK-2026-10-17.md) يوضح تسريب جواب الـMC قبل **وبعد** تسجيل الاستماع، وعدم اتساق إعادة `wellbeing-exchange` مع شرح رد Maya، واختبارات حدود الصوت والـLive المطلوبة. Product PR #54 لم يتغير؛ لا تدّعي تنفيذ الإصلاحات.
- صوت Gemini TTS `pilot02` لم يتم توليده مدفوعًا عند آخر فحص؛ موافقة التكلفة، سماع WAV وفحص timestamps والتجارب الصوتية/الميكروفون الحقيقية لازمة. Visual QA وحده غير كافٍ.
- **الدور الآن:** `LESSON_REVIEWER` لتحديد الفجوات ورفع القرارات، لا `LESSON_PRODUCER` لدرس U1-L02، ولا `FIVE_LESSON_REVIEWER` لأننا لم ننتج خمسة.
- لما القرارات تتعتمد وتكمل أدلة الدرس الأول، ارجع لـ`STEP 1` وحدّث الحالة، ثم انتقل للدور التالي **حسب حالة GitHub الفعلية**.

## 11) HANDOFF LOG — سجل التسليم المتجدد

| Date | Role | Scope | Verified work / evidence | Next role and exact action | Blockers |
|---|---|---|---|---|---|
| 2026-10-17 | LESSON_REVIEWER (Session 2) | LEARN A1 / U1-L01 | Reverified PR #13 / #54 open Draft, zero owner comments/reviews, A1 U1-L01 in-progress. Independently inspected A1 teacher/audio script, clip manifest, controller and tests; authored [adversarial QA recheck](interactive-content-production/coverage/A1/U1-L01-INDEPENDENT-QA-RECHECK-2026-10-17.md): pre+post listening answer cue, wellbeing reply omitted from targeted replay, missing chronological timing validation checks. Product code untouched; real WAV/Live/screenshots not tested. | Existing U1-L01 producer fixes non-semantic P1 items and adds regression tests only within their claim; owner rules on 12 IDs + any paid TTS job; independent QA recheck follows. | 12 owner decisions, two P1 fixes, unapproved TTS, real device/audio/Live, Cloudflare preview failure uninvestigated. |
| 2026-10-17 | LESSON_REVIEWER | LEARN A1 / U1-L01 | GitHub verified all six production status files and manifests, Stage-06 lifecycle for 12 IDs, Stage-07 U1 briefs, EnglishLive Draft #54 @ `d9081dda`, source dialogue and product QA. Authored [12-ID owner brief](interactive-content-production/coverage/A1/U1-L01-OWNER-DECISION-BRIEF-2026-10-17.md) with alternative placements and 2 independent P1 pedagogical counterexamples; no source locks or product code changed. | `LESSON_REVIEWER` remains `OWNER_DECISION_WAIT`; owner rules on 12 IDs, producer fixes first-listen answer leak and productive Speaking evidence, separately approves/denies `pilot02` paid TTS; then independent recheck. | Owner scope rulings, paid TTS, real WAV/Live/audio, QA acceptance; PR #54 Draft. |
| 2026-10-17 | WORKFLOW_BOOTSTRAP | LEARN A1 | Verified the six status files, `english-course` agent workflow, `speaking-practice` QA docs, `englishlive` PR #54 and current QA ledger. This control file was prepared for a scoped GitHub PR; verify whether that PR was merged on `main` before treating it as a shared source. | `LESSON_REVIEWER` → read `U1-L01-REVIEW.md`, critique 12 scope decisions, prepare owner decision brief; do not skip U1-L01. | Owner decisions, paid TTS permission, live audio/Speaking and owner acceptance. |

### Handoff report template (every session)

```text
VERIFIED AT: [date, timezone, repo refs/commits]
LANE / LEVEL: [...]
ROLE / STEP: [...]
LESSON or BATCH: [...]
STATUS COUNTS: [done / in-progress / not-started / reviewed with evidence]
WHAT I READ: [exact source files + PR links]
WHAT I ACTUALLY DID: [changes, analysis, reviewed scenes/audio, tests]
WHAT IS NOT VERIFIED: [...]
COUNTEREXAMPLES / RECHECK: [...]
OWNER DECISIONS: [specific decisions only, or NONE]
NEXT ROLE: [...]
NEXT PERMITTED ACTION: [...]
CONTROL FILE SYNCED TO MAIN?: [YES with PR/SHA | NO: portable copy]
```

---

### Absolute operating principle

**The agent's job is to discover the actual current state, determine its role, perform the highest-priority authorized step, independently critique its work, record real evidence, update the central control state, and leave an exact next step.**

> في المحادثة الجديدة: **اقرأ الملف → راجع GitHub → اعرف دورك → اشتغل → راجع شغلك → حدّث الحالة → سلّم اللي بعدك**. لا تنتظر شرحًا جديدًا، ولا تتخطَّ بوابة قرار بشري أو تكلفة أو ملكية عمل.