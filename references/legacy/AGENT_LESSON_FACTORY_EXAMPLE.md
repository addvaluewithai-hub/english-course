# Daily Lesson Factory — Agent Brief (منهج الإنسان)

You are an autonomous content agent. **Each scheduled run, you build exactly ONE
complete, high-quality lesson — end to end — then stop.** Next run, you build the
next one. Do not try to build more than one lesson per run.

Treat this like real teaching work: **research, outline, critique, rewrite, and only
then ship.** A shallow lesson is a failure even if it compiles. Quality over speed.

---

## 0. Project orientation

- **App root:** `C:\Users\yasse\OneDrive\Desktop\my projects\manhaj-al-insan`
- **Stack:** Next.js 16 (App Router) + React 19 + TypeScript + Tailwind v4. RTL, Arabic-first.
- **Run/verify:**
  - `npx tsc --noEmit` — type-check (must pass)
  - `npm run build` — production build with webpack (must pass; scripts use `--webpack` on purpose)
  - `npm run dev` — local server at http://localhost:3000 to eyeball the lesson
- **It is data-driven.** A lesson is a TypeScript module exporting a `LessonExperience`
  object (pure data). The Scene Engine renders it. You never touch the engine — you
  only add content (lesson modules, images, audio).

### Read these first, every run
- Schema (the contract): `src/lib/types/lesson.ts` and `src/lib/types/curriculum.ts`
- **Gold-standard examples** (match this quality bar): `src/lib/data/lessons/lesson_000_001.ts`,
  `lesson_000_002.ts`, `lesson_000_003.ts`
- The curriculum plan (titles/descriptions/skills per gate): `src/lib/data/curriculum.ts`
  (the `PARTS` array)
- What's already done: `src/lib/data/lessons/authored-ids.ts`

---

## 1. Pick the next lesson (deterministic)

Lessons are produced **in curriculum order**. Gate ids are `part_000` … `part_015`;
lesson ids are `lesson_<partNum>_<NN>` (e.g. `lesson_001_002`).

1. Open `src/lib/data/lessons/authored-ids.ts` — that array lists finished lessons.
2. Walk the curriculum in order (Gate 0 lessons, then Gate 1 lessons, …). The next
   lesson is the **first id not in that array**. Gate 0 (بوابة الرحلة) is fully done,
   so you start at `lesson_001_001` (Gate 2, العالم الذي نعيش فيه) and go forward.
3. In `curriculum.ts`, find that lesson's **title, description, and skills** (inside the
   matching `PARTS[i].lessons[j]`). That is your assignment for today. Also note the
   **gate's theme/colors** (`PARTS[i].colors`, `worldType`) so visuals fit the gate.

If every lesson is authored, stop and report "all lessons complete."

---

## 2. Research & think (do this before writing)

- Research the topic properly (use web search / your knowledge). Find the *core idea*,
  the most common misconception, 2–3 vivid real-world examples or analogies, and the
  one thing a learner must walk away understanding.
- Draft a scene-by-scene outline. Then **critique it**: Is the intro genuinely
  illuminating? Does each scene earn its place? Is there a misconception to correct? Are
  the questions making them *think*, not recall trivia? Rewrite the outline until it's
  strong.
- Audience: curious teens and adults (13+). Tone: calm, serious, warm, premium — never
  childish, never preachy. Arabic (فصحى مبسّطة).

---

## 3. Lesson structure & quality bar

A lesson is 8–12 scenes. **Follow this arc:**

1. **Intro scene — THE most important scene. It must carry real value.** This is not a
   title card. In the intro narration, *actually explain the whole topic*: the big
   question, why it matters, and the core idea in miniature — so that even someone who
   stopped after the intro would have learned something real. Open with a hook (a
   concrete image, a surprising fact, a question). This narration can be long
   (1–4 minutes of speech is fine). `completion.required: "manual"`.
2. **Then build interactivity and depth:** alternate explanation scenes with
   interactions. Use deep explanations, concrete examples, analogies, comparisons, and a
   misconception you correct head-on.
3. **End** with a reflection, a synthesizing `mini_challenge`, a `summary` that crystallizes
   the takeaways, and a `teaser` pointing to the next lesson (or next gate).

**Variety is required** — do not make every interaction a `single_choice`. Across the
lesson use a mix from: `single_choice`, `multiple_choice`, `drag_drop` (categorize),
`ordering`, `slider` (opinion/confidence), `reflection` (saved to the journal),
`ai_feedback` (open answer graded by the app's AI endpoint), `mini_challenge`.

**Every scene has narration** (`narration.script` + `showCaptions: true`,
`autoPlay: true`). The transcript is shown to the learner and highlighted while the
audio plays, and interactions are visible *while* the narration plays — so you may put
an interaction and an explanation in the same scene.

**Hard audio rule:** the TTS free tier is **10 requests/day**. Each scene with narration
= one audio clip = one request. So **keep narration scenes ≤ 9 per lesson** (leave a
buffer). Clips may be long (aim 30s–4min each; avoid >5min to stay under the per-minute
token limit). One lesson's audio must fit in one day.

Accessibility is built in (captions, reduced motion, keyboard nav). Just always set
`showCaptions: true`.

---

## 4. Authoring the module

Create `src/lib/data/lessons/lesson_<partNum>_<NN>.ts`, exporting a `const` named
`lesson_<partNum>_<NN>` typed `LessonExperience`. Copy the shape from
`lesson_000_001.ts`. Key fields per scene: `id`, `type`, `templateId`, `title`,
`narration {script, autoPlay, showCaptions}`, optional `visual {background, objects}`,
optional `animation {timeline}`, optional `interaction`, `completion`, `transition`.

Set the lesson's `partId/stageId/unitId/order` to match the ids in `curriculum.ts`
(`stage_<partNum>`, `unit_<partNum>_001`, order = the lesson's `orderIndex`).

**Templates** (set `templateId`) pick the layout: `cinematic_intro_parallax` (stack),
`narrated_explanation_cards` (row), `two_concept_comparison` (compare),
`three_choice_question` / `drag_to_categories` / `ordering_steps` / `reflection_scene`
(interaction-focused), `summary_scene` (stack). Backgrounds: `starfield`,
`parallax_layers` (with gradient layers), `gradient`, `image`. Use the gate's colors.

### Register it (two small edits — do NOT edit the engine or the curriculum builder)
1. `src/lib/data/lessons/index.ts`: add `import { lesson_xxx } from "./lesson_xxx";`
   and add `lesson_xxx,` to the `AUTHORED_LESSONS` object.
2. `src/lib/data/lessons/authored-ids.ts`: add `"lesson_xxx"` to the array.
   (This auto-flips the lesson's `hasFullContent` → it shows the "تجربة كاملة" badge and
   becomes fully playable. No other edits needed.)

---

## 5. Images & graphics (you can generate images — use them)

You have image-generation capability. Use it to make studying clearer — diagrams,
illustrative scenes, metaphors, simple labeled visuals.

- **Save to** `public/images/lesson_<partNum>_<NN>/<name>.png` (or `.webp`).
- **Reference in a scene** as an object:
  ```ts
  { id: "img1", type: "image", url: "/images/lesson_001_001/scale.png",
    text: "تعليق اختياري تحت الصورة", style: "glow" }
  ```
  or as a full-bleed background: `visual.background = { type: "image", url: "/images/.../bg.png" }`.
- **Style:** match the app — deep cosmic dark theme, indigo/violet/gold accents, calm and
  premium, clean and uncluttered. Prefer conceptual/illustrative over busy.
- **Do NOT bake Arabic text into generated images** (models render Arabic poorly).
  Keep words as scene `objects` (`heading`/`paragraph`/`text_card`) over or beside the
  image. Wordless or English-label-free visuals only.
- Keep files reasonably small (target < ~600 KB each). 1–4 images per lesson is plenty.

---

## 6. Generate the narration audio

Audio is **pre-generated and cached** (never generated at runtime). Pipeline:

1. After the lesson module is written and registered, run:
   ```bash
   npm run tts -- 10
   ```
   This finds every narration script not yet generated (i.e. your new lesson's), calls
   Gemini TTS, writes `public/audio/<hash>.wav`, and updates
   `src/lib/data/audio-manifest.json`. It is **paced (3/min), resumable, and skips
   existing clips**, so it only generates the new lesson.
2. If it prints a **429** (quota/rate), stop — it saves progress. Wait and rerun
   `npm run tts -- 10` later; it resumes. (Daily limit is 10 requests; that's why a
   lesson must have ≤ 9 narration scenes.)
3. Voice is `GEMINI_TTS_VOICE` in `.env.local` (default `Charon`). Don't change it unless
   asked.

The runtime matches each scene's script to its `.wav` via a hash
(`src/lib/audio/hash.ts`); any clip not yet generated falls back to browser TTS, so the
lesson is never broken — but your job is to generate all of them.

---

## 7. Verify (must pass before you're done)

Run in order:
1. `npx tsc --noEmit` → no errors.
2. `npm run tts -- 10` → all this lesson's clips generated (or resumed to completion).
3. `npm run build` → succeeds (run AFTER tts so the manifest is bundled).
4. `npm run dev`, open `http://localhost:3000/lesson/lesson_<partNum>_<NN>`, and confirm:
   the intro plays with real voice, the transcript shows + highlights while playing,
   interactions work, images load, and you can reach the end. Then stop the dev server.

If anything fails, fix it before finishing. Never leave the repo in a non-building state.

---

## 8. Definition of done (one run)

- One new lesson module, registered in both `index.ts` and `authored-ids.ts`.
- 8–12 well-crafted scenes; intro genuinely teaches the topic; varied interactions.
- ≤ 9 narration scenes; **all** their audio generated into `public/audio` + manifest.
- 1–4 supporting images in `public/images/lesson_xxx/` where they aid understanding.
- `tsc` clean, `build` clean, lesson plays correctly in `dev`.
- Optional: `git add -A && git commit -m "lesson: <id> — <title>"` if the repo uses git.

Then **stop**. Do not start the next lesson. The schedule will wake you again tomorrow.

---

## 9. Guardrails / gotchas

- Build/dev scripts intentionally use `--webpack` (the ASCII path is fine; keep webpack).
- Don't import app modules with a `.ts` extension outside `scripts/` (Next's typecheck
  rejects it). Inside lesson modules use the existing `import type { LessonExperience }
  from "@/lib/types/lesson"` style.
- Don't edit the Scene Engine (`src/components/scene-engine/*`), the curriculum builder
  logic, or `package.json` scripts. You add content only.
- Keep secrets in `.env.local` (gitignored). Never print API keys.
- Use the gate's own colors/worldType for visual cohesion — each gate is its own "world".
- TPM safety: if very long narration triggers 429s, lower `TTS_RPM` to `2` in `.env.local`
  temporarily, or split an over-long scene into two (still ≤ 9 narration scenes total).
