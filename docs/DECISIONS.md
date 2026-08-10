# Decisions and Open Questions

## Locked for the current discovery phase

- Audience: Arabic-speaking adults, starting at A1.
- Positioning: serious learning, not a streak-first casual game.
- Curriculum direction: source objectives first, units and lessons second.
- Source stack: GSE objectives, CEFR validation, English Grammar Profile, Pearson GSE
  grammar guide, and Oxford vocabulary.
- Lesson unit: one coherent measurable ability, not necessarily one source descriptor.
- First proof: one gold lesson before app architecture or mass production.
- Arabic baseline: clear Modern Standard Arabic.
- Mastery is required and is distinct from completion.

## LEARN-001 learner and language policy

- The primary learner is an Arabic-speaking adult entering the product at A1; no
  nationality, dialect, education, profession, or uniform prior exposure is assumed.
- English is the target and performance language. MSA is concise scaffolding for
  essential instructions, explanations, and important corrections.
- The earlier phrase “Egyptian-friendly clarity” is resolved as accessible, natural MSA,
  not permission to use Egyptian Arabic. The later live-teacher brief explicitly
  requires MSA and forbids Egyptian Arabic.
- Children, casual streak-first use, dialect localization, and foundational literacy
  instruction are outside the current promise and need separate evidence.
- The amount and timing of Arabic, cross-region MSA naturalness, and support for varying
  literacy remain learner-test questions.

## LEARN-002 mastery and progress policy

- Lesson completion is an experience event, not evidence of mastery.
- Demonstration requires all lesson-required criteria to pass together in a fresh task
  without a complete model or answer-revealing help; rubric dimensions are not averaged.
- The reusable dimensions are comprehension, outcome performance, interaction or
  transfer, and control or repair. Lessons mark applicability and define concrete
  source-linked evidence.
- Retention requires a delayed fresh demonstration. A failed later probe or recurring
  important weakness can move prior mastery to `needs review`.
- Teach-back may corroborate control or repair but cannot supply a missing rating or
  replace the communicative performance required by the outcome. Recognition items may
  diagnose weak evidence but cannot establish communicative performance.
- Exact retention timing, probe count, task-variant difficulty, and evaluator agreement
  remain gold-lesson and learner-test hypotheses, not production rules.

## LEARN-003 AI teacher and teach-back policy

- The AI teacher is a finite, goal-bounded lesson activity, not an open-ended chatbot;
  it asks or instructs one turn at a time and ends without starting another lesson.
- Practice correction handles one important issue at a time using the learner fragment,
  one natural correction, a brief MSA explanation when needed, and an immediate retry.
- The initial correction bound is one direct retry plus at most one scaffolded retry.
  If correction occurs during a final attempt, that attempt becomes practice and a new
  fresh variant is required before demonstration can be claimed.
- Lesson completion, the final mastery result, and teach-back evidence are reported
  separately. Teach-back may corroborate control or repair but never supplies a missing
  rating or replaces performance.
- Personal prompts must permit fictional answers and avoid sensitive data. Unsafe or
  crisis content pauses the lesson and evaluation under the documented safety boundary.
- Lesson teach-back frequency, post-performance placement, bounded retry sufficiency,
  and deeper unit synthesis remain gold-lesson and learner-test hypotheses.

## LEARN-004 learning-model gate

- The gold-lesson baseline uses fresh performance before teach-back. It must compare a
  matched post-performance teach-back variant with an omit variant.
- Teach-back evidence is recorded separately. It may corroborate control or repair but
  cannot supply a missing mastery rating or reverse a failed fresh performance.
- Lesson completion is reported only after the configured required experience finishes;
  early learner stop and safety interruption use distinct non-complete outcomes.
- A lesson authors a primary fresh task plus an equivalent replacement variant or
  bounded mutation rules. One replacement final attempt is the initial test hypothesis.
- Privacy minimization and construct-preserving accessibility are locked in
  `docs/PRIVACY_ACCESSIBILITY_POLICY.md` without designing production storage.
- Video is an optional, accessible input or explanation medium whose added value must be
  tested; watching it is never mastery evidence.
- Independent critique findings were resolved before the gate passed. Phase 2 may open
  for source-record schema work only; later gates remain locked.

## CUR-004 curriculum tag normalization

- Skill/domain, communication-mode, and communicative-function tags are controlled by
  `docs/CURRICULUM_TAG_TAXONOMY.md` and remain interpretations, never source facts.
- Channel-neutral CEFR competence descriptors use `language_system`; compound source
  actions may carry multiple supported tags without being split or rewritten.
- The one CEFR personal-response descriptor that does not fix oral versus written
  realization retains both supported channels and an explicit ambiguity.
- Candidate clusters, units, lessons, and objective-to-descriptor equivalence remain
  deferred. The normalized tags are audit aids, not curriculum structure.

## CUR-005 candidate unit map

- The earlier exact seven-unit proposal is not supported: only 58 of 120 included GSE
  objectives fit it naturally; 35 overlap its boundaries and 27 would be forced.
- Eight topical or functional candidate-unit clusters and two cross-cutting support
  bands are retained for the `CUR-006` audit. This is not a final unit count or order.
- Generic language foundations, repair, mediation, translation, and facilitation remain
  cross-cutting instead of being forced into the old Simple Communication unit.
- Compound source records may map to multiple clusters without being split or rewritten.
- Objective-to-descriptor equivalence, prerequisites, balance, final units, and lessons
  remain deferred.

## Hypotheses to test

- Seven proposed A1 units cover all source objectives cleanly.
- A lesson usually takes 20-45 minutes.
- Video belongs near the start of every lesson.
- Short lesson teach-back plus deep unit teach-back is useful without becoming tedious.
- One lesson image or one image per key situation is sufficient.
- `Introduce Yourself` is the best gold lesson.

## Explicitly deferred

- Final number and names of A1 units.
- Final number of A1 lessons.
- Production database and PostgreSQL schema.
- Final screen sequence and exercise engine.
- Audio, video, and image providers.
- Full A1 content generation.

## Questions for gold-lesson research

- Do beginners understand the MSA explanations naturally?
- Does video improve understanding enough to justify its time and production cost?
- Can the learner demonstrate the ability without a visible model?
- Is teach-back useful or repetitive?
- Which mistakes deserve interruption, and which should be ignored?
- What evidence is enough to mark an ability demonstrated and retained?

## GOLD-002 single-teacher video revision

- The gold-lesson explanation test uses one teacher speaking directly to the learner;
  the two-speaker podcast concept is dropped for this test.
- All learner interaction begins after the video. The video contains the situation,
  models, meaning contrast, and pronunciation explanation; post-video work moves from
  comprehension to application and fresh production.
- By explicit user direction, this gold-video test uses natural Egyptian Arabic. This
  is a scoped learner-test variant and does not silently replace the course-wide MSA
  baseline before evidence is collected.
- Spoken English uses General American pronunciation with inline language and IPA
  markup for the selected Gemini test workflow.
- Egyptian transcript editing avoids artificial case-ending tanween in conversational
  phrases (`شخص جديد`, `موضوع يقدر`) while retaining natural established forms such as
  `مثلًا`.

## Owner acceptance and Unit 1 content start

- On 2026-07-30, the product owner accepted the revised gold lesson and its generated
  voice as the reference experience and explicitly directed work to begin on Unit 1.
- This is a product acceptance decision, not evidence from an external learner pilot.
  The missing pilot evidence remains a named risk rather than being reported as passed.
- Unit 1 is bounded as `First Connections`: eight approved identity and personal-
  information candidates covering listening, speaking, reading, writing, oral
  interaction, and written interaction.
- The identity-mediation candidate is deferred because it has a required prerequisite
  outside the selected unit boundary. Cross-cutting politeness, repair, number, spoken,
  written, and language-control supports remain embedded without claiming extra lesson
  mastery.

## CUR-006 curriculum coverage gate

- All 218 included reviewed records remain traceable and mapped; the retained duplicated
  GSE page-15 row is the only exclusion and keeps its page, hash, and exact reason.
- Three repeated-wording groups are reconciled. The GSE repetition has one canonical
  included record; two CEFR repetitions remain distinct because the same published
  wording occurs under different scales and physical pages.
- No strict order among topical clusters is source-proven. Basic language control and
  interaction repair are cross-cutting support dependencies that must be available
  alongside relevant Phase 3 abilities, not standalone units imposed by the audit.
- The 120 included GSE objectives are speaking-heavy (54) and reading-light (14).
  Granular objective gaps remain visible in four candidate clusters, while combined
  GSE and CEFR evidence covers all four core skills in every candidate cluster.
- Phase 2 passes. Phase 3 lesson normalization may open with the candidate unit count,
  unit order, lesson outcomes, and objective-to-descriptor equivalence still unresolved.

## LESSON-001 lesson-sized ability contract

- A lesson candidate is one coherent, observable real-life performance, not a topic,
  grammar point, source sentence, screen sequence, or fixed duration.
- Merge candidates only when one fresh task and one mastery judgment can validly cover
  all parts at A1; split when parts can be mastered independently or need different
  valid assessments, prerequisites, or situations.
- Source records remain immutable. Full, partial, supporting, and contextual coverage
  claims retain exact record, file, location, and hash provenance; no CEFR/GSE
  equivalence is implied.
- Required-before, helpful-before, successor, and concurrent-support relations are
  distinct. Source order does not establish a strict lesson or topical-cluster order.
- Scope bands describe performance load, not time. A complex candidate needs a
  no-split justification, and time remains a planning hypothesis.
- `docs/LESSON_SIZED_ABILITY_RULES.md` and its JSON Schema are approved inputs to
  `LESSON-002`; they do not approve a final lesson map, unit count, or sequence.

## LESSON-002 relationship and sequence review

- All 81 current candidates appear exactly once across five pedagogical sequence bands.
  The bands are a reviewed A1 learning hypothesis, not source-proven unit boundaries or
  a strict topical order.
- Five dependencies are `required_before` because the target would otherwise lack a
  necessary literal reception or baseline form skill. Each has an ordered reciprocal
  successor and the hard-dependency graph is acyclic.
- Forty-three `helpful_before` links record useful scaffolds without becoming hard
  gates. Cross-cutting language control and interaction repair remain concurrent support.
- Relationship evidence is limited to source records already cited by the linked pair;
  the order itself remains an interpretation and does not rewrite source facts.
- Language-target selection, labelled error decisions, candidate approval, final unit
  boundaries, and gold-lesson selection remain unresolved. Phase 4 stays locked.

## LESSON-002 foundational reception target review

- Nine candidates in the first pedagogical band now have reviewed source-linked
  language-target decisions: four reading-reception candidates and five
  listening-reception candidates.
- The partition records 24 target entries across grammar, vocabulary, phrases, and
  pronunciation. Each target reuses only evidence already declared by its candidate;
  an empty target family has an explicit not-assigned rationale.
- Nine candidate-specific learner-error decisions are labelled `hypothesis`. Their
  basis states that GSE and CEFR do not report the learner error and that Arabic-English
  expert review plus learner observation are still required.
- The remaining 72 candidates still need language-target and error decisions. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 foundational output and interaction target review

- Ten additional first-band candidates now have reviewed source-linked target and error
  decisions: four social-contact tasks, two spoken personal-information tasks, and four
  written personal-information or message tasks.
- The partition adds 29 target entries: seven grammar, seven vocabulary, ten phrase,
  and five pronunciation decisions. All 70 evidence usages reuse records already cited
  by the owning candidate; empty target families have explicit rationales.
- Ten candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not establish them, so Arabic-English expert review and learner
  observation remain required.
- Nineteen of 81 candidates now have explicit target/error decisions; 62 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 postcard and familiar-context reception target review

- Seven additional candidates now have reviewed source-linked target and error
  decisions: the remaining postcard reception task plus all six reception tasks in the
  familiar-people/routines/home sequence band.
- The partition adds 18 target entries: two grammar, six vocabulary, seven phrase, and
  three pronunciation decisions. All 32 evidence usages reuse 15 records already cited
  by their owning candidates; empty target families retain explicit rationales.
- Seven candidate-specific learner-error decisions remain labelled `hypothesis`. The
  source evidence does not report these learner errors, so Arabic-English expert review
  and learner observation remain required.
- Twenty-six of 81 candidates now have explicit target/error decisions; 55 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 familiar-people and routine output target review

- Six additional spoken or interactive candidates now have reviewed source-linked
  target and error decisions: two family/known-person tasks, three routine or leisure
  tasks, and one event date-and-time task.
- The partition adds 23 target entries: five grammar, six vocabulary, six phrase, and
  six pronunciation decisions. All 53 evidence usages reuse 18 records already cited
  by their owning candidates; the one empty grammar family has an explicit rationale.
- Six candidate-specific learner-error decisions remain labelled `hypothesis`. The
  source evidence does not report these learner errors, so Arabic-English expert review
  and learner observation remain required.
- Thirty-two of 81 candidates now have explicit target/error decisions; 49 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 familiar home, object, and location speech target review

- Four additional spoken or interactive candidates now have reviewed source-linked
  target and error decisions: people/object locations, familiar-object description,
  visible-object information exchange, and basic home-information exchange.
- The partition adds 16 target entries: four each for grammar, vocabulary, phrases,
  and pronunciation. All 41 evidence usages reuse 11 records already cited by their
  owning candidates.
- Four candidate-specific learner-error decisions remain labelled `hypothesis`. The
  source evidence does not report these learner errors, so Arabic-English expert review
  and learner observation remain required.
- Thirty-six of 81 candidates now have explicit target/error decisions; 45 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 familiar written people, routine, and home target review

- Six additional written candidates now have reviewed source-linked target and error
  decisions: people profile cards, hobbies/preferences post, schedule date/time entry,
  life/routine sentences, familiar-object description, and room description.
- The partition adds 17 target entries: five grammar, six vocabulary, and six phrase
  decisions; pronunciation is explicitly not assigned because all six mastery tasks
  require written performance. All 37 evidence usages reuse 14 records already cited
  by their owning candidates.
- Six candidate-specific learner-error decisions remain labelled `hypothesis`. The
  source evidence does not report these learner errors, so Arabic-English expert review
  and learner observation remain required.
- Forty-two of 81 candidates now have explicit target/error decisions; 39 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 remaining familiar output and mediation target review

- The final three output or mediation candidates in the familiar-people/routines/home
  sequence band now have reviewed source-linked target and error decisions: common
  weather, a rehearsed formal introduction, and a personal response to a simple work.
- The partition adds eight target entries: one grammar, two vocabulary, three phrase,
  and two pronunciation decisions. All ten evidence usages reuse four records already
  cited by their owning candidates; unsupported target families have explicit reasons.
- Three candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not report these learner errors, so Arabic-English expert
  review and learner observation remain required.
- Forty-five of 81 candidates now have explicit target/error decisions; 36 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 opening wayfinding target review

- Four opening navigation/services candidates now have reviewed source-linked target and
  error decisions: written directions, slow spoken route directions, directions from an
  interlocutor, and a basic reciprocal wayfinding exchange.
- The partition adds 12 target entries: one grammar, four vocabulary, four phrase, and
  three pronunciation decisions. All 27 evidence usages reuse 12 records already cited
  by their owning candidates; unsupported target families have explicit reasons.
- Four candidate-specific learner-error decisions remain labelled hypothesis. The
  GSE/CEFR evidence does not report these learner errors, so Arabic-English expert
  review and learner observation remain required.
- Forty-nine of 81 candidates now have explicit target/error decisions; 32 remain. No
  candidate is approved, LESSON-002 remains in progress, and Phase 4 stays locked.

## LESSON-002 remaining travel-reception target review

- Three remaining travel-reception candidates now have reviewed source-linked target
  and error decisions: simple place/hotel information, guided-tour outline, and slow
  station-announcement details.
- The partition adds eight target entries: one vocabulary and one phrase decision for
  the written candidate, plus two vocabulary, two phrase, and two receptive
  pronunciation decisions for the listening candidates. All 11 evidence usages reuse
  five records already cited by their owning candidates; unsupported grammar and
  written-pronunciation families have explicit reasons.
- Three candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not report these learner errors, so Arabic-English expert
  review and learner observation remain required.
- Fifty-two of 81 candidates now have explicit target/error decisions; 29 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.
## LESSON-002 navigation/travel action target review

- Four additional navigation or travel-action candidates now have reviewed source-linked
  target and error decisions: predictable-detail relay, game/activity instructions,
  public-transport ticket purchase, and hotel check-in.
- The partition adds 12 target entries: four vocabulary, four phrase, and four
  pronunciation decisions. All 19 evidence usages reuse seven records already cited by
  their owning candidates; the four unsupported grammar families have explicit reasons.
- Four candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not report these learner errors, so Arabic-English expert
  review and learner observation remain required.
- Fifty-six of 81 candidates now have explicit target/error decisions; 25 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 opening service-reception target review

- Three additional food/shopping/services reception candidates now have reviewed
  source-linked target and error decisions: spoken price identification, slow everyday
  service-exchange comprehension, and advertisement or leaflet detail finding.
- The partition adds eight target entries: three vocabulary, three phrase, and two
  receptive pronunciation decisions. All 21 evidence usages reuse eight records
  already cited by their owning candidates; unsupported grammar and written-
  pronunciation families have explicit reasons.
- Three candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not report these learner errors, so Arabic-English expert
  review and learner observation remain required.
- Fifty-nine of 81 candidates now have explicit target/error decisions; 22 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 opening service output and interaction target review

- Four additional food/shopping/services candidates now have reviewed source-linked
  target and error decisions: stating a food or drink preference, asking for food or
  drink, asking for and giving an everyday item, and exchanging information about an
  immediate need.
- The partition adds 13 target entries: one grammar, four vocabulary, four phrase, and
  four pronunciation decisions. All 29 evidence usages reuse 11 records already cited
  by their owning candidates; the three unsupported grammar families have explicit
  reasons.
- Four candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not report these learner errors, so Arabic-English expert
  review and learner observation remain required.
- Sixty-three of 81 candidates now have explicit target/error decisions; 18 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 remaining food, shopping, and services target review

- Four remaining food/shopping/services candidates now have reviewed source-linked
  target and error decisions: basic practical help, price and quantity exchange, a
  bounded health-professional problem exchange, and a simulated simple online
  purchase or application.
- The partition adds ten target entries: one grammar, three vocabulary, three phrase,
  and three pronunciation decisions. All 19 evidence usages reuse seven records
  already cited by their owning candidates; unsupported target families have explicit
  reasons and the written online task has no pronunciation target.
- Four candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not report these learner errors, so Arabic-English expert
  review and learner observation remain required.
- Sixty-seven of 81 candidates now have explicit target/error decisions; 14 remain. No
  candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 remaining messages, signs, and forms target review

- Eight additional message, visual-media, and mediation candidates now have reviewed
  source-linked target and error decisions: whereabouts message, slow-speech detail
  relay, headline-topic and video-ad product identification, online-post reaction,
  sign/notice information conveyance, rough oral translation, and dictionary-assisted
  written translation.
- The partition adds 21 target entries: one grammar, eight vocabulary, seven phrase,
  and five pronunciation decisions. All 25 evidence usages reuse nine CEFR records
  already cited by their owning candidates; unsupported target families have explicit
  reasons and the three written-only tasks have no pronunciation target.
- Eight candidate-specific learner-error decisions remain labelled `hypothesis`. CEFR
  explicitly notes the written-translation risk of selecting an inappropriate meaning;
  the exact candidate error pattern and all other errors still require Arabic-English
  expert review and learner observation.
- Seventy-five of 81 candidates now have explicit target/error decisions; six remain.
  No candidate is approved, `LESSON-002` remains in progress, and Phase 4 stays locked.

## LESSON-002 final social-contact and collaboration target review

- The final six candidates now have reviewed source-linked target and error decisions:
  agreeing to a request, accepting an offer, showing sympathy, inviting input and
  checking understanding, welcoming an idea, and sharing an idea while asking what
  others think.
- The partition adds 19 target entries: one grammar, six vocabulary, six phrase, and
  six pronunciation decisions. All 23 evidence usages reuse eight GSE or CEFR records
  already cited by their owning candidates; five unsupported grammar families have
  explicit reasons.
- Six candidate-specific learner-error decisions remain labelled `hypothesis`. The
  GSE/CEFR evidence does not report these exact learner errors, so Arabic-English
  expert review and learner observation remain required.
- All 81 candidates now have explicit target/error decisions, but all remain
  `needs_review`. `LESSON-002` stays in progress, candidate approval is the next
  separate audit, and Phase 4 stays locked.

## Cross-level source-disposition contract v1

- Source use, learner control, and product lifecycle are separate decisions. A record
  now has a `source_role`, a `control_expectation`, and a use `disposition`; its first
  exposure, practice, recycle, consolidation, and extension levels remain SPINE-004
  product decisions.
- All 9,274 normalized records were reviewed through explicit dataset policies plus a
  complete exception and exact-overlap audit. This is accepted batch-policy review,
  not a false claim of 9,274 independent human pedagogical judgments.
- CEFR descriptors are level-boundary evidence; GSE objectives are granular
  communicative evidence; EGP and GSE Grammar are language-system evidence; Oxford
  entries are lexical reference pools rather than automatic targets.
- Exact-text repetition remains visible as 27 overlap groups affecting 55 records.
  Three GSE groups repeat the same objective at different scores; the variance is
  preserved and no score is silently selected as authoritative.

## A1-C2 level-exit profiles v1

- The six A1-C2 exit profiles are accepted as the internal curriculum boundary. Pre-A1
  remains diagnostic/remedial support and A2+/B1+/B2+ remain internal milestones.
- Each level has 17 reviewed claims: one synthesized exit promise, 13 source-boundary
  claims across reception, production, interaction, mediation, and language control,
  plus three fresh-performance policy claims. The complete set contains 102 claims.
- Source-boundary claims reference deterministic evidence bundles rather than entire
  source files. Product assessment claims reference the learning and mastery policy so
  sourced facts and product decisions remain distinct.
- C2 targets precise, effective communication; retained accent is acceptable when it
  does not reduce intelligibility or effectiveness. Native-speaker imitation and
  accent removal are not course goals.
- C2 lexical methodology, the English-specific pronunciation sequence for Arabic
  learners, semantic cross-source mapping, and item lifecycle ownership remain named
  SPINE-004 work rather than hidden gaps.
