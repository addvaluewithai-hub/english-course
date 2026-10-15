# QA report — one per product PR/lesson

- Lesson ID / revision: `<id@revision>`
- Product commit / preview host: `<SHA + URL>`
- Playwright run/artifact URL: `<link or not run>`
- QA owner and date: `<actual reviewer/date>`
- Evidence state: `NOT CAPTURED | CAPTURED NOT INSPECTED | INSPECTED WITH DEFECTS | RECHECKED | HUMAN ACCEPTED`

## Coverage by viewport

| Viewport | Scenes / authored beats | Unanswered MC | Wrong MC + feedback | Correct MC + feedback | Hints/error | Final Speaking | Screenshots actually viewed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 320x640 | not captured | — | — | — | — | — | no |
| 400x860 | not captured | — | — | — | — | — | no |
| 1280x900 | not captured | — | — | — | — | — | no |

## Browser test findings

- Console/page errors: `not tested`
- Horizontal overflow: `not tested`
- Board internal scroll, offstage text, visual overlap: `not tested`
- Small labels / buttons smaller than touch target: `not tested`
- Arabic/English bidi and font loading: `not tested`
- Premature answer reveal: `not tested`
- Interrupted narration and rapid navigation: `not tested`
- Wrong answer marked wrong, correct explanation, progression: `not tested`
- Otti covers lesson content: `not tested`
- Full lesson content vs curriculum role contract: `not tested`

## Defect ledger

| ID | Severity | Exact scene/beat/state/viewport | Observed defect | Before screenshot | Fix/commit | After screenshot | Reinspected by/date/status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QA-001 | — | — | — | — | — | — | OPEN (example only) |

## Live-only gate (not replaceable by screenshots)

- Authored vs actual Otti speech review: `not performed`
- Wrong choice spoken explanation: `not performed`
- Quiz → feedback → next audio overlap: `not performed`
- Voice permission / interruption / reconnect: `not performed`
- Final Speaking with weak/incoherent and strong answers: `not performed`
- Actual learner feedback: `not performed`

## Conclusion

- Technical build/validation: `NOT TESTED`
- Screenshots generated: `NO`
- Screenshots opened and critiqued: `NO`
- Defects repaired and visually rechecked: `NO`
- Live audio tested: `NO`
- Owner accepted: `NO`
- Ready to merge/deploy: `NO — pending explicit product approval`
