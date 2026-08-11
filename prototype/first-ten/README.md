# First Ten Local Prototype

This dependency-free interface reads the actual first-ten release and package files
from the repository. Start an HTTP server at the repository root, then open:

`http://127.0.0.1:8765/prototype/first-ten/`

The interface stores only opened/practiced lesson IDs and Unit 1 review preview status
in browser local storage. It never stores activity or mastery answers. "Practiced" is
not a mastery decision.

The learner route is a simple end-user demo: video or placeholder, one application at
a time, a final challenge, controlled feedback, and the next lesson. Put optional local
videos in `media/` with names such as `U1-L01.mp4`; the matching lesson loads them
automatically. Without a video, the learner can continue through the placeholder.

Controlled lesson feedback is stored only in this browser and can be copied from the
home screen. Activity and challenge responses are never stored. The separate direct
route `observer.html` remains available for a later formal study, but is not shown in
the ordinary learner interface.
