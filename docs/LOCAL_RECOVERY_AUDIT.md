# Local Recovery Audit

Date: 2026-08-10

## Purpose

Determine whether the owner's pre-handoff local archive contained curriculum plans or
other project materials missing from the private team repository.

## Repository check

At audit time, GitHub contained only `main` at commit `72d7050`; there were no other
remote branches or pull requests. The local clone was clean and already up to date.

## Recovered files

Exactly three meaningful local-only files were found outside ignored caches, temporary
test data, and per-agent run logs:

1. `references/legacy/conversation between me and ai.txt`
2. `references/legacy/live ai agent.txt`
3. `references/legacy/AGENT_LESSON_FACTORY_EXAMPLE.md`

All three were read in full before this audit was written.

## Findings

- No hidden A2, B1, B2, C1, or C2 curriculum map was found.
- No cross-level grammar, vocabulary, pronunciation, discourse, or recycling map was
  found.
- The old seven-unit structure is an A1 proposal, not a cross-level spine. The later
  conversation explicitly recommends extracting and auditing objectives before locking
  units, abilities, or lesson counts.
- The live-agent file is a useful delivery hypothesis for one early A1 lesson, not a
  course outline.
- The lesson-factory example is an operational automation reference from another
  project, not curriculum evidence.

## What the archive confirms

The recovered planning supports the current repo's strongest decisions:

- serious learning over streak-driven play;
- strategic Arabic explanation for Arabic-speaking beginners;
- one measurable ability per lesson;
- understand, practice, use, explain, review;
- source-first curriculum construction;
- gold lesson and learner testing before mass production;
- mastery is not equivalent to watching or activity completion.

## Conclusion

The new team is not waiting on an undiscovered local cross-level plan. The missing
vertical curriculum architecture must be designed explicitly and committed as a new
source-of-truth artifact. Use `docs/VERTICAL_CURRICULUM_SPINE_BRIEF.md` as the starting
contract.
