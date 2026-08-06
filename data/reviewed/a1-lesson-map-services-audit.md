# A1 Lesson Map: Food, Shopping, and Services Partition Audit

Status: reviewed draft partition; `LESSON-002` remains in progress.

## Boundary

This partition reconciles all 30 assignments containing
`food_shopping_services`. It adds 13 lesson-sized draft candidates while retaining
the existing public-transport ticket owner and interaction-repair support owner. It
does not approve a final lesson count, unit boundary, global order, language target,
or gold lesson.

## Candidate decisions

- Reception separates locating one spoken price, following the meaning of a short
  service exchange, and finding explicit details in a simple advertisement or leaflet.
- Asking for food or drink, stating a food or drink preference, exchanging an everyday
  item, exchanging immediate-need information, and asking for practical help remain
  independently assessable outcomes.
- Numbers, quantities, and cost are kept together inside one bounded purchase because
  the fields must be mutually understood for that transaction to succeed.
- A low-stakes health-professional exchange remains separate from ordinary shopping
  and service work. It permits gesture but excludes diagnosis, advice, emergencies,
  and real health data.
- The online form uses only fictional information. The whereabouts message and written
  mediation task are retained as cross-cluster evidence instead of being forced into a
  shopping-only lesson.

## Shared evidence reconciliation

- The existing full ticket-purchase candidate retains
  `gse.adult.2022.p22.011`; no second service claim is added.
- Existing interaction-repair support retains
  `cefr.cv2020.p072.overall_oral_interaction.01`.
- `gse.adult.2022.p15.008` adds only its price clause beside the existing times-and-
  dates claim.
- `cefr.cv2020.p051.understanding_announcements_and_instructions.03` adds only its
  shop-price example beside the existing station figures-and-times claim.
- The same ask-and-give wording published under CEFR Goal-oriented co-operation and
  Obtaining goods and services remains as two distinct page-and-scale records.
- Advertisements and leaflets, online forms, the whereabouts message, practical help,
  and relayed service details carry explicit shared cluster ids for later partitions.

## Counts and balance

- Assignments reconciled: 30 of 30.
- New candidates: 13; new candidate evidence references: 28.
- Twenty-six reviewed record ids are newly cited; two prior records receive named
  price-only partial claims.
- Expanded map: 66 candidates, 152 candidate evidence references to 140 unique reviewed
  records, nine support records, and 149 unique cited included records overall.
- New candidates represent listening, reading, speaking, and writing plus reception,
  production, interaction, online interaction, and mediation.

## Critique and unresolved work

Every assignment has a non-context citation or retained support owner. No source record
becomes a duplicate full anchor, and every partial claim names its covered clause.
Candidate tags are supported by cited reviewed records, all mastery tasks use fresh
variants, and privacy-sensitive prompts require fictional data. No MSA text is
introduced in this data partition.

All candidates and the map remain `needs_review`. Grammar, vocabulary, phrases,
pronunciation, Arabic-speaker error hypotheses, time estimates, hard prerequisites,
successors, and final sequence remain empty or provisional until reviewed evidence and
later partitions justify them.

## Validation

- Lesson-map schema and semantic validation: pass.
- Service partition acceptance tests: 9 pass.
- Full project suite: 95 tests pass.
- Reviewed source collections, candidate map, curriculum audit, and lesson map: pass.
- Deterministic rebuild SHA-256:
  `62DC2D56207A341152FB4629DB1939D7B8C7504DC90838F65C0DAE1885C02199`.
- Python compilation, six authoritative raw-source hashes, and modular line limits:
  pass.

## Next bounded partition

Normalize the `messages_signs_forms` assignments, retaining full owners established by
earlier partitions and reconciling only uncited or named remaining clauses. Keep global
sequence and unit boundaries provisional.
