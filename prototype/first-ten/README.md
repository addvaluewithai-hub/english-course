# First Ten Local Prototype

This dependency-free interface reads the actual first-ten release and package files
from the repository. Start an HTTP server at the repository root, then open:

`http://127.0.0.1:8765/prototype/first-ten/`

The interface stores only opened/practiced lesson IDs and Unit 1 review preview status
in browser local storage. It never stores activity or mastery answers. "Practiced" is
not a mastery decision.

The learner route currently previews source content; final Gemini voice and video are
not rendered. `observer.html` is the de-identified longitudinal facilitator instrument.
It can be rehearsed with synthetic fixtures now, but real sessions must wait until all
ten videos are rendered, transcript-matched, and listened to.
