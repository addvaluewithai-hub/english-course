# A1 Manual Phrase Review

Status: **MANUAL REVIEW COMPLETE — READY FOR CRITIC**  
Stage: **02 — Phrases**  
Input: `curriculum/levels/a1/phrases.json`  
Oxford A1 phrases manually read: **199/199**

This is a manual semantic review. No automated clustering or string-matching result is authoritative here. Every Oxford A1 phrase was read and given a primary natural home, a cross-cutting role, or an architecture flag. A primary home is not an exclusive-use rule; phrases may later recycle across several capabilities.

## Review result

- Phrases with a natural primary home in the locked 21-capability map: **173**
- Phrases owned by existing cross-cutting possession/reference language: **3**
- Phrases that expose a new function/gap or require explicit later architectural treatment: **23**
- Phrases silently discarded: **0**

The main architecture signals are:
1. a substantial **simple opinion / evaluation / agreement / suggestion** cluster;
2. a smaller but clear **plans / future intention** cluster;
3. several **discourse/expansion** phrases that look cross-cutting rather than like a new capability;
4. one explicit **comparison** phrase that should be revisited with grammar evidence rather than creating a capability from one phrase alone.

# Primary phrase homes

## C01 — Meet, greet, and introduce people
Count: **15**

- `oxford.phrase.online.0112` — **bad news**
- `oxford.phrase.online.0314` — **Good morning**
- `oxford.phrase.online.0315` — **good news**
- `oxford.phrase.online.0319` — **Guess what…**
- `oxford.phrase.online.0346` — **How are you?**
- `oxford.phrase.online.0361` — **I'm sorry**
- `oxford.phrase.online.0516` — **Oh no!**
- `oxford.phrase.online.0518` — **Oh yes**
- `oxford.phrase.online.0579` — **pretty good**
- `oxford.phrase.online.0599` — **really good**
- `oxford.phrase.online.0622` — **See you**
- `oxford.phrase.online.0640` — **speak to sb**
- `oxford.phrase.online.0668` — **Thank you**
- `oxford.phrase.online.0720` — **welcome to sth**
- `oxford.phrase.online.0750` — **You're welcome**

Manual note: these phrases strengthen the decision to keep greeting, wellbeing, simple reaction, introductions and leave-taking inside one first-contact capability family.

## C02 — Exchange basic personal information
Count: **11**

- `oxford.phrase.online.0165` — **cell phone**
- `oxford.phrase.online.0177` — **come from…**
- `oxford.phrase.online.0247` — **find out**
- `oxford.phrase.online.0493` — **mobile phone**
- `oxford.phrase.online.0538` — **on the phone**
- `oxford.phrase.online.0567` — **phone call**
- `oxford.phrase.online.0568` — **phone number**
- `oxford.phrase.online.0635` — **someone else**
- `oxford.phrase.online.0729` — **work as sth**
- `oxford.phrase.online.0730` — **work for sb/sth**
- `oxford.phrase.online.0748` — **X years old**

Manual note: phone-related phrases are treated as personal/contact-information context, not as evidence for a separate telephone capability.

## C03 — Exchange information about family and friends
Count: **6**

- `oxford.phrase.online.0142` — **best friend**
- `oxford.phrase.online.0214` — **each other**
- `oxford.phrase.online.0236` — **family member**
- `oxford.phrase.online.0276` — **get married**
- `oxford.phrase.online.0317` — **grow up**
- `oxford.phrase.online.0470` — **live with sb**

## C04 — Exchange information about home and residence
Count: **3**

- `oxford.phrase.online.0079` — **at home**
- `oxford.phrase.online.0471` — **living room**
- `oxford.phrase.online.0685` — **there is**

`there is` will almost certainly cross-link to C10 and grammar review.

## C05 — Talk about preferences and interests
Count: **2**

- `oxford.phrase.online.0598` — **really enjoy**
- `oxford.phrase.online.0600` — **really like**

## C06 — Talk about routines and free-time activities
Count: **39**

- `oxford.phrase.online.0085` — **at school**
- `oxford.phrase.online.0100` — **at the weekend**
- `oxford.phrase.online.0104` — **at university**
- `oxford.phrase.online.0105` — **at work**
- `oxford.phrase.online.0225` — **every day**
- `oxford.phrase.online.0261` — **for lunch**
- `oxford.phrase.online.0273` — **get home**
- `oxford.phrase.online.0282` — **get ready**
- `oxford.phrase.online.0287` — **get up**
- `oxford.phrase.online.0300` — **go home**
- `oxford.phrase.online.0304` — **go out**
- `oxford.phrase.online.0306` — **go to bed**
- `oxford.phrase.online.0307` — **go to school**
- `oxford.phrase.online.0308` — **go to work**
- `oxford.phrase.online.0325` — **hard work**
- `oxford.phrase.online.0327` — **have fun**
- `oxford.phrase.online.0341` — **high school**
- `oxford.phrase.online.0350` — **How often…?**
- `oxford.phrase.online.0376` — **in bed**
- `oxford.phrase.online.0380` — **in class**
- `oxford.phrase.online.0409` — **in school**
- `oxford.phrase.online.0467` — **listen to sb/sth**
- `oxford.phrase.online.0524` — **on holiday**
- `oxford.phrase.online.0527` — **on television**
- `oxford.phrase.online.0529` — **on the beach**
- `oxford.phrase.online.0532` — **on the internet**
- `oxford.phrase.online.0544` — **on TV**
- `oxford.phrase.online.0545` — **once a…**
- `oxford.phrase.online.0571` — **play with sb/sth**
- `oxford.phrase.online.0641` — **spend time**
- `oxford.phrase.online.0644` — **stay in**
- `oxford.phrase.online.0653` — **swimming pool**
- `oxford.phrase.online.0711` — **TV show**
- `oxford.phrase.online.0718` — **wake up**
- `oxford.phrase.online.0731` — **work hard**
- `oxford.phrase.online.0735` — **work together**
- `oxford.phrase.online.0736` — **work with sb**
- `oxford.phrase.online.0744` — **X hours a day**
- `oxford.phrase.online.0745` — **X times a…**

Manual note: this is a dense phrase family, but density alone is not a reason to split the capability. Later lesson-load design will distribute these across contexts and recycling cycles.

## C07 — Talk about ability and inability
Count: **3**

- `oxford.phrase.online.0311` — **good at sth**
- `oxford.phrase.online.0456` — **know how**
- `oxford.phrase.online.0460` — **learn how to do sth**

## C08 — Understand simple descriptions and identify familiar referents
Count: **6**

- `oxford.phrase.online.0040` — **all over the world**
- `oxford.phrase.online.0054` — **around the world**
- `oxford.phrase.online.0411` — **in space**
- `oxford.phrase.online.0455` — **kind of sb/sth**
- `oxford.phrase.online.0478` — **look like sb/sth**
- `oxford.phrase.online.0691` — **this kind of…**

Manual note: C08 remains somewhat generic. Grammar and word review must still test whether it deserves top-level status or should become a receptive requirement spread across domain capabilities.

## C09 — Exchange basic information about objects
Count: **2**

- `oxford.phrase.online.0143` — **black and white**
- `oxford.phrase.online.0690` — **This is…**

## C10 — Talk about location and position
Count: **12**

- `oxford.phrase.online.0108` — **away from sb/sth**
- `oxford.phrase.online.0178` — **come into sth**
- `oxford.phrase.online.0301` — **go into sth**
- `oxford.phrase.online.0388` — **in front of**
- `oxford.phrase.online.0419` — **in the centre**
- `oxford.phrase.online.0420` — **in the country**
- `oxford.phrase.online.0435` — **in the north**
- `oxford.phrase.online.0439` — **in the street**
- `oxford.phrase.online.0447` — **in town**
- `oxford.phrase.online.0530` — **on the floor**
- `oxford.phrase.online.0557` — **out of sth**
- `oxford.phrase.online.0561` — **over there**

## C11 — Handle basic numbers and quantities
Count: **11**

- `oxford.phrase.online.0006` — **a few**
- `oxford.phrase.online.0010` — **a little**
- `oxford.phrase.online.0015` — **a lot**
- `oxford.phrase.online.0017` — **a lot of sth**
- `oxford.phrase.online.0348` — **How many…?**
- `oxford.phrase.online.0349` — **How much…?**
- `oxford.phrase.online.0481` — **lots of…**
- `oxford.phrase.online.0492` — **millions of…**
- `oxford.phrase.online.0496` — **more than…**
- `oxford.phrase.online.0696` — **thousands of…**
- `oxford.phrase.online.0703` — **too much**

## C12 — Handle basic time and dates
Count: **36**

- `oxford.phrase.online.0020` — **a period of time**
- `oxford.phrase.online.0038` — **all day**
- `oxford.phrase.online.0088` — **at the beginning of sth**
- `oxford.phrase.online.0089` — **at the end**
- `oxford.phrase.online.0090` — **at the end of sth**
- `oxford.phrase.online.0094` — **at the moment**
- `oxford.phrase.online.0095` — **at the same time**
- `oxford.phrase.online.0253` — **for a long time**
- `oxford.phrase.online.0254` — **for a moment**
- `oxford.phrase.online.0262` — **for many years**
- `oxford.phrase.online.0266` — **for the first time**
- `oxford.phrase.online.0321` — **half an hour**
- `oxford.phrase.online.0334` — **have time**
- `oxford.phrase.online.0347` — **How long…?**
- `oxford.phrase.online.0375` — **in April**
- `oxford.phrase.online.0414` — **in summer**
- `oxford.phrase.online.0433` — **in the morning**
- `oxford.phrase.online.0436` — **in the past**
- `oxford.phrase.online.0440` — **in the summer**
- `oxford.phrase.online.0454` — **It takes …**
- `oxford.phrase.online.0457` — **last time**
- `oxford.phrase.online.0458` — **last year**
- `oxford.phrase.online.0499` — **next time**
- `oxford.phrase.online.0500` — **next year**
- `oxford.phrase.online.0525` — **on Monday**
- `oxford.phrase.online.0548` — **one day**
- `oxford.phrase.online.0612` — **right now**
- `oxford.phrase.online.0670` — **that day**
- `oxford.phrase.online.0673` — **the 20th century**
- `oxford.phrase.online.0681` — **the next day**
- `oxford.phrase.online.0692` — **this morning**
- `oxford.phrase.online.0693` — **this time**
- `oxford.phrase.online.0694` — **this year**
- `oxford.phrase.online.0702` — **too long**
- `oxford.phrase.online.0746` — **X years ago**
- `oxford.phrase.online.0747` — **X years later**

Manual note: this confirms that separating time/dates from general numbers was the right Stage-01 critic decision. Some past/future references will need grammar review before we decide how productively they are used.

## C13 — Understand simple arrangements and event details
Count: **3**

- `oxford.phrase.online.0055` — **arrive at…**
- `oxford.phrase.online.0056` — **arrive in…**
- `oxford.phrase.online.0717` — **wait for sb/sth**

Important: phrase evidence below suggests C13 may eventually need to expand from only *understanding* arrangements to include simple plans/intentions.

## C14 — Understand basic signs and notices
Count: **0**

No primary Oxford A1 Phrase List item maps naturally here. This does **not** weaken C14; the capability comes from the ability evidence, and signs/notices may rely mainly on lexical/form language rather than listed phrases.

## C15 — Follow simple instructions and procedures
Count: **5**

- `oxford.phrase.online.0137` — **begin with sth**
- `oxford.phrase.online.0216` — **end in sth**
- `oxford.phrase.online.0474` — **look at sb/sth**
- `oxford.phrase.online.0628` — **sit down**
- `oxford.phrase.online.0642` — **stand up**

## C16 — Ask for and follow simple directions
Count: **11**

- `oxford.phrase.online.0158` — **car park**
- `oxford.phrase.online.0170` — **city centre**
- `oxford.phrase.online.0277` — **get off**
- `oxford.phrase.online.0278` — **get on**
- `oxford.phrase.online.0284` — **get there**
- `oxford.phrase.online.0286` — **get to…**
- `oxford.phrase.online.0296` — **go back**
- `oxford.phrase.online.0476` — **look for sb/sth**
- `oxford.phrase.online.0533` — **on the left**
- `oxford.phrase.online.0576` — **post office**
- `oxford.phrase.online.0704` — **town centre**

## C17 — Repair a basic communication problem
Count: **0**

No primary Oxford A1 Phrase List phrase directly supplies the required repair language such as asking for spelling/written form. This is a **content-supply flag**, not a reason to remove the capability: the ability source requires the performance, so later phrase authoring/other source evidence must supply the actual repair expressions.

## C18 — Express immediate needs; make and respond to basic requests/offers
Count: **7**

- `oxford.phrase.online.0049` — **anything else**
- `oxford.phrase.online.0076` — **ask for sth**
- `oxford.phrase.online.0229` — **excuse me**
- `oxford.phrase.online.0505` — **No problem**
- `oxford.phrase.online.0514` — **of course**
- `oxford.phrase.online.0738` — **would like**
- `oxford.phrase.online.0741` — **Would you like…?**

Several of these will also be mandatory in service transactions.

## C19 — Handle basic service transactions
Count: **1 primary**

- `oxford.phrase.online.0565` — **pay for sth**

Strong cross-links from C18: `anything else`, `excuse me`, `would like`, `Would you like…?`, `Thank you`, `You're welcome`, `No problem`, and `of course` are likely to recycle heavily here. Low primary count does not mean weak language support; much of the transaction language is shared interaction language.

## C20 — Complete basic forms
Count: **0**

No primary Oxford A1 Phrase List item is naturally owned here. Form completion is primarily a task using personal details, numbers, dates, spelling and writing mechanics already sourced elsewhere.

## C21 — Write a simple personal message
Count: **0**

No primary Oxford phrase is uniquely owned by this writing task. Many social/time/personal phrases will be reused here. This capability remains task-defined rather than phrase-defined.

# Existing cross-cutting / reference language

## X01 — Possession and ownership
Count: **2**

- `oxford.phrase.online.0328` — **have got**
- `oxford.phrase.online.0344` — **his or her**

These reinforce the Stage-01 decision that possession/ownership is cross-cutting across personal information, family, home and objects rather than a separate capability.

## General reference language
Count: **1**

- `oxford.phrase.online.0336` — **he or she**

This is reference/grammar language used across capabilities, not a real-world performance by itself. Grammar review should own the structural treatment.

# Architecture flags raised by phrase review

## P-GAP-01 — Simple opinion, evaluation, agreement and suggestion
Count: **14**

### Opinion / agreement / suggestion signals
- `oxford.phrase.online.0007` — **a good idea**
- `oxford.phrase.online.0032` — **agree with sb**
- `oxford.phrase.online.0113` — **bad thing**
- `oxford.phrase.online.0345` — **How about…?**
- `oxford.phrase.online.0395` — **in my opinion**
- `oxford.phrase.online.0688` — **think about sb/sth**
- `oxford.phrase.online.0689` — **think of sb/sth**
- `oxford.phrase.online.0722` — **What about…?**

### Evaluation / importance / difficulty signals
- `oxford.phrase.online.0111` — **bad for sb/sth**
- `oxford.phrase.online.0208` — **difficult for sb**
- `oxford.phrase.online.0312` — **good for sb/sth**
- `oxford.phrase.online.0316` — **good thing**
- `oxford.phrase.online.0366` — **important for sb/sth**
- `oxford.phrase.online.0453` — **It is important to do sth**

Manual conclusion: this is too coherent and too large to dismiss as random leftovers. The locked ability map currently has preferences, but **preference is not the same as opinion/evaluation/agreement/suggestion**. Stage-02 critic should decide between:
- adding a new capability such as **Express a simple opinion/evaluation and respond to a simple suggestion**; or
- proving that these phrases can be naturally distributed without losing the communicative function.

Current reviewer preference: **likely add/expand a capability**, but do not change Stage 01 before critic.

## P-GAP-02 — Plans and future intention
Count: **3 direct phrases**, with additional future-time support in C12.

- `oxford.phrase.online.0124` — **be going to do sth**
- `oxford.phrase.online.0427` — **in the future**
- `oxford.phrase.online.0570` — **plan for sth**

Supporting C12 phrases include `next year` and `one day`.

Manual conclusion: these do not fit comfortably inside the current C13 because C13 is receptive: *understand arrangements/event details*. Phrase evidence suggests a productive function: **talk about a simple plan/future intention**. The cleaner possible revision may be to expand C13 into a two-way **plans and arrangements** capability rather than add an unrelated new capability. Grammar review of `be going to` should strongly inform the final decision.

## P-X08 — Discourse, reason and expansion language
Count: **5**

- `oxford.phrase.online.0136` — **because of**
- `oxford.phrase.online.0256` — **for example**
- `oxford.phrase.online.0386` — **in fact**
- `oxford.phrase.online.0649` — **such as**
- `oxford.phrase.online.0665` — **talk about sb/sth**

Manual conclusion: these look more like **cross-cutting discourse/expansion resources** than a standalone A1 capability. They should help learners extend a short answer, give an example/reason, or frame a topic across several capabilities. Grammar review should decide exact control expectations.

## P-GAP-03 — Comparison
Count: **1**

- `oxford.phrase.online.0207` — **differences between A and B**

Manual conclusion: one phrase is not enough evidence to create a comparison capability. Hold this as an explicit flag for the grammar stage; if comparative grammar/features also appear strongly, comparison may need a real communicative home.

# Cross-links that must not be lost later

These primary assignments are intentionally not exclusive:

- `How much…?` — C11 numbers/quantities **and** C19 service transactions.
- `phone number` — C02 personal/contact information **and** C11 number handling.
- `there is` — C04 home/residence **and** C10 location/position.
- `excuse me` — C18 requests/attention **and** C16 directions/C19 service encounters.
- `would like` / `Would you like…?` — C18 requests/offers **and** C19 service transactions; `would like` may also touch C05 preference.
- `get on` / `get off` — C16 route/transport language and the transport-ticket branch of C19.
- `Thank you`, `You're welcome`, `No problem`, `of course` — C01 social politeness and C18/C19 interaction.
- `How often…?`, `once a…`, `X times a…`, `X hours a day` — C06 routines with C12 time/frequency support.
- `next year`, `one day` — C12 time references and P-GAP-02 future plans.
- `get married`, `grow up`, `X years ago/later` — family/life-event content plus time-reference support; productive past narration should not be assumed until grammar review.

# Stage-02 critic questions

1. Should P-GAP-01 become a new final capability for simple opinion/evaluation/agreement/suggestion, or can it be integrated cleanly without losing the function?
2. Should C13 be expanded from receptive arrangements to **make/understand simple plans and arrangements**, using P-GAP-02, or should future intention be separate?
3. Does C08 still deserve top-level status after phrase mapping, or is it really a receptive cross-cutting requirement across people/place/object domains?
4. C06 has 39 primary phrases and C12 has 36. Is this simply natural density, or is either capability hiding two materially different learner performances?
5. What exact functional phrases must be added for C17 repair, since Oxford A1 Phrase List provides no direct repair expression despite the ability requirement?
6. Should discourse phrases in P-X08 become a named cross-cutting requirement in the final architecture?
7. Does comparison remain a minor language point, or does grammar evidence make it a real A1 performance requirement?

# Stage status

- Oxford A1 phrases manually read: **199/199**.
- Every phrase has a recorded primary home or explicit architecture/cross-cutting flag.
- No phrase was forced into a capability merely to make coverage look complete.
- No phrase was silently dropped.
- No unit or lesson design has begun.

Next action: **Critic this phrase-stage result, resolve the architecture flags, update the single authoritative capability map only if evidence requires it, then proceed to manual grammar review.**
