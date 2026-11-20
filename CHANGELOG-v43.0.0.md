# TGAT1 English Studio v43.0.0

Release date: 2026-11-19 (Thai time). Content round v43, work by Arena AI (C1, C2, C3, V1) and Claude (everything below marked "Claude").

## Content

| Area | Change | Who |
|---|---|---|
| Long conversation (LC) | Sets 11–20 converted from comprehension questions to blank fill-in dialogues (100 items) | Arena (C1) |
| Text completion (TC) | All 40 passages / 300 blanks rewritten; vocabulary/collocation 41.7 %, plus verb form, tense/voice, clauses, connectors, inversion, question tags | Arena (C2) |
| TC | Answer is the longest option in 29.3 % of blanks (was 42 %); 38 distractors lengthened and their Thai explanations rewritten | Claude |
| Reading comprehension (RC) | All 300 items rewritten with a blueprint question-type mix | Arena (C3) |
| RC | Words-in-context 21 → 60 items (3 per 15); detail stays 120 | Claude |
| RC | 64 answer keys paraphrased so they no longer copy the passage word-for-word; picking the option with most passage words now works 27 % of the time (was 51.7 %) | Claude |
| RC | 4 passages replaced by new genres (news report, job advertisement, email, feature article); this removes the near-duplicate pair S14-Q056/S20-Q051 and the station-sign / lost-property repeats | Claude |
| Short conversation | 120 recycled, off-topic distractors replaced by topical lures; word-matching now works 28.5 % (was 67 %) | Claude |
| Question–Response | 60 idiom / fixed-expression items replace 60 items built from recycled distractors (idioms were ~5/200) | Claude |
| All kinds | Distractors with absolute words (all/every/never/only…) reduced so they no longer give the answer away (RC 0.047 vs 0.12 answer/distractor rate in the extended list; within 1.5× on the task-7 list) | Claude |
| Vocabulary | 56 invented headwords renamed to real collocations | Arena (V1) |

## App / build

- Version, cache namespace and manifest bumped to 43.0.0 (`tgat1-studio-v43.0.0`) so installed PWAs pick up the new content.
- New build steps: `tools/apply_short_v43.py`, `tools/apply_qr_idiom.py`; `tools/apply_rc_v43.py` can now replace a passage when a spec carries `context`.
- New regression gates in `tests/regression_r3_content.py` (G-A … G-G): RC type mix, RC and short-conversation context-overlap, TC key-length, Q-R idiom count, extreme-word balance, RC passage near-duplicates and genre count.

## Not done in this release (see qa/V43-NEXT-WORK.md and HANDOFF.md)

Vocabulary queue V2–V6, code refactors T1–T4, Lighthouse (T5), real-device and screen-reader checks (Q1–Q3). All new and changed items still need human proofreading.
