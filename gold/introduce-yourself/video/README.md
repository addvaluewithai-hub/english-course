# Video test — Introduce Yourself

This directory is the approved one-teacher Gemini TTS test package for lesson 1.

## Paste order

1. Paste `scene.txt` into **Scene**.
2. Paste `sample-context.txt` into **Sample Context**.
3. Paste `transcript.txt` into **Text**.
4. Assign one warm Arabic-capable voice to `Speaker 1`.

The video contains all explanation and modeling. Learner interaction begins only after the video and uses the questions in `../activities.json`.

## Pronunciation

- Every spoken English span in the transcript has an `en-US` language wrapper and IPA pronunciation.
- SSML markup and bracketed performance tags must remain silent.
- `pronunciation-map.json` is the compact production reference.
- Reject a take if markup is spoken, `live` is pronounced `/laɪv/` in `I live in`, or English keeps an Arabic accent after code-switching.

## Arabic editorial rule for this test

The teacher uses natural Egyptian Arabic. Avoid artificial case-ending tanween in conversational phrases: write `شخص جديد` and `موضوع يقدر`, while retaining established natural forms such as `مثلًا`.
