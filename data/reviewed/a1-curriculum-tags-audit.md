# A1 Skill, Mode, and Function Normalization Audit

## Scope and boundary

- Task: `CUR-004`.
- Inputs: 121 reviewed Pearson GSE evidence rows and 98 reviewed CEFR descriptors.
- Controlled taxonomy: `docs/CURRICULUM_TAG_TAXONOMY.md`, version 1.0.0.
- Review identity and time: `cur_004_primary`, `2026-07-16T02:50:11+03:00`.
- Output fields: `interpretation.skill_codes`, `mode_codes`, and `function_codes` in
  both the derived and reviewed GSE/CEFR collections.

No source text, source fact, locator, hash, inclusion/exclusion decision, or candidate
cluster was changed. These tags are interpretations for Phase 2 comparison; they do not
define units, lessons, prerequisites, or final learner outcomes.

## Coverage and counts

All 219 records have at least one controlled skill/domain, mode, and function tag.
The 121 GSE evidence rows retain one reviewed duplicate exclusion, which receives the
same descriptive tags as its canonical source occurrence but remains excluded.

GSE skill totals are Reading 14, Listening 34, Speaking 54, and Writing 19. Normalized
mode totals are reception 48, production 44, and interaction 29.

CEFR normalized mode totals exactly preserve the extracted source-mode distribution:
reception 24, production 11, interaction 30, online interaction 3, mediation 15, and
communicative competence 15. CEFR skill/domain tags may be multiple per descriptor;
their totals are listening 45, reading 29, speaking 41, writing 19, viewing 3,
non-verbal 6, and channel-neutral language system 15.

Across both sources, every controlled function is assigned only where the source action
supports it. Multi-function records retain explicit compound actions, such as
introduction plus social contact, online purchase plus form completion, or overall
mediation plus facilitation.

## Review performed

- Checked every GSE Speaking record with its assigned mode and function. Question
  answers, information exchanges, requests, social responses, and transactions are
  interaction; statements, descriptions, introductions without a required response,
  and reproduction are production.
- Checked every CEFR descriptor with its source mode, skill hierarchy, scale, text, and
  assigned tags. Record-level actions override broad scale names when needed, such as
  locating prices in an announcement rather than following instructions.
- Corrected mediation channel inheritance so tags retain the input and output channels
  supported by each descriptor and add non-verbal only when the text explicitly names
  gesture, body language, or non-verbal signals.
- Kept communicative-competence descriptors channel-neutral under `language_system`
  rather than inventing a speaking-only or writing-only claim.
- Preserved the GSE source-duplicate ambiguities. Added one normalization ambiguity to
  the CEFR personal-response descriptor because it does not specify oral versus written
  realization; both supported productive channels are tagged.
- At `CUR-004` acceptance, all candidate clusters remained empty. `CUR-005` subsequently
  populated them under the separate candidate-map contract without changing these tags.

## Validation result

- Before/after evidence digests for each of the four collections were unchanged.
- Both registered raw-source SHA-256 hashes were rechecked and remain unchanged.
- All three source-record schemas pass Draft 2020-12 checking.
- All four derived/reviewed collections pass structural and semantic provenance
  validation, and all reviewed records remain accepted with no error issue.
- Twenty-four tests pass, including controlled-code coverage, evidence preservation,
  idempotence, ambiguity retention, extraction completeness, and raw-page provenance.
- Python byte-compilation passes. All normalization logic and test files remain below
  the project's preferred 200-line limit.

## Remaining boundary

The controlled tags make the two evidence sources comparable but do not resolve
objective-to-descriptor equivalence. `CUR-005` tested candidate clusters and the earlier
seven-unit hypothesis; final units and the remaining coverage audit stay deferred.
