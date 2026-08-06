# Unit 1 content QA

Status: all automated content gates passed; 238 project tests passed on 2026-07-30.

## Automated gates

- Every selected candidate is approved and belongs to the identity cluster.
- The unit covers listening, speaking, reading, and writing.
- Every lesson package retains its exact candidate source packet.
- Every video is single-teacher and places all interaction after the video.
- Every spoken English span in lessons 2–8 uses an `en-US` wrapper and IPA phoneme.
- Transcript SSML fragments parse as XML and use only `Speaker 1` routing.
- Each lesson separates completion from fresh mastery and has delayed review.
- The unit mastery implements spoken contact, contact capture, and written follow-up.

## Human render checks still required per generated media file

- Listen for natural Egyptian Arabic and clean switching to General American English.
- Confirm markup and performance tags are silent.
- Reject mispronounced names, places, digits, `live`, or question words.
- Time captions against the approved final audio without changing transcript wording.
- Confirm pacing remains adult, clear, and non-childish.

Rendered audio and video are provider outputs; this repository holds the complete,
validated source package used to generate and review them.
