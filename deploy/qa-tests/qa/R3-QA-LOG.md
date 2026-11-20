# TGAT1 English Studio — Round 3 QA log (v42.0.1 → v42.0.2)

Date: 2026-11-19. Work was done by AI. **No human editorial, screen-reader or real-device review has been performed.** Practice questions are original practice material: not official TGAT1 questions, not past papers, not a score predictor.

## 0. Process notes
- Baseline: the v42.0.1 deploy ZIP plus the QA/tests ZIP (`qa/v42.0.1-inherited/`). The original suites were re-run on the untouched v42.0.1 build before any change: `smoke_test.py` 49/49 and `regression_v42.py` 60/60 (with axe-core).
- **Parallel session.** A second session (the same task, run in another chat) wrote to this folder at about 09:43–10:50. Its vocabulary, IPA, matching-game, accessibility, CSP, version and test work is kept. Its TC/RC rewrites were superseded by the round-3 specs used here; they are kept unapplied in `superseded/` (see `superseded/README.md`).
- **Reproducibility.** `tools/rebuild_all.sh` rebuilds every round-3 data change from the v42.0.1 originals (`backups/`) and logs each field change to `qa/changes_r3.jsonl`. `tools/update_registers.py` turns that log into `qa/DATA-CHANGES.csv` (inherited rows + 3,280 round-3 rows + code-change rows).

## 1. Long Conversation (40 contexts / 200 items) — all 200 reviewed
| Finding (v42.0.1) | Action |
|---|---|
| All 20 blank-fill dialogues (100 items) used **one fixed 10-line template**: identical lines (“Don’t worry about overspending”, “Keeping it under N baht…”, “Could you glance over my draft…”), verbatim recycled distractors, and the key always echoed the next line’s place/time/baht | **Rewritten:** 20 new dialogues, 100 items, varied discourse functions, distractors plausible in isolation but wrong in discourse, item-specific Thai explanations |
| Explanations named distractors that did not exist (e.g. photographer/bus/certificates) | Replaced; automated check confirms every English quotation in an explanation exists in the item |
| 20 comprehension dialogues (100 items): uncontracted speech (“Let us”, “I will”), generic stems (“What did the speakers do first?”, “Why do they want to take that step?”), absurd distractors, generic English explanations | **Revised:** contractions, specific stems, plausible distractors from the dialogue, Thai explanations. **Superseded in v43 (2026-11-19):** LC sets 11–20 are no longer comprehension dialogues — they were rewritten as blank fill-in dialogues (`content/lc_blank_v43_[e-h].json`, applied by `tools/apply_lc_blank.py`); the comp specs/applier moved to `superseded/`. |

Option-cue metrics (accuracy without reading; chance = 25%):

| Strategy | v42.0.1 | v42.0.2 |
|---|---:|---:|
| pick longest | 49.5% | 24.0% |
| drop options with absolutes, pick longest | 68.5% | 27.5% |
| max overlap with context | 42.5% | 36.5% |
| pick second-longest | 48.0% | **42.5% (residual cue, open)** |

## 2. Text Completion (40 passages / 300 items) — all 40 passages and 300 items read
- **84 item fixes** in `content/tc_fixes_r3.py`, each with a one-line reason:
  - **Wrong key:** “Some herbs need *little* sunlight, while others grow well in shade” → “plenty of”.
  - **Second correct option:** safe/safer, so/so that, which/that, compare with/to, before/after/during alternatives, “expressing” as a reduced relative, and similar.
  - **15 sentences copied from other passages** into eight-blank passages (e.g. “The editor will review the guide…” inside the sidewalk-map passage; “Players can return costumes…” inside the wildlife-shelter passage). Replaced with on-topic sentences.
  - Illogical sequences, e.g. “check names before using school records” → “check names against school records”.
- **300 explanations regenerated in Thai** (they were English boilerplate such as “In this context, X fits the sentence grammar…”). Each now shows the completed sentence plus a rule tied to the options; 11 have hand-written overrides. Distractor reasons are category-level, so the queue marks them “template-assisted · needs human review”.
- Answer positions remain 75/75/75/75. Blank integrity is checked: each blank appears exactly once and matches its item.
- **Theme repetition:** the 40 topics are distinct (maximum lexical Jaccard 0.19), but about 11/40 passages share a “try → measure → adjust” narrative, and the TC seed exchange overlaps the RC seed library. Logged in REVIEW-QUEUE; not rewritten.

## 3. Reading Comprehension distractors (60 passages / 300 items)
All 60 passages were read.

**Rewritten: 180 items** (main idea, sequence/detail and inference, for every passage). The v42.0.1 versions had these problems:
- Distractors repeated the passage’s topic noun phrase in 67% of cases (answers 8%).
- Distractors were absurd (“hired an outside consulting firm”, “strict government penalty”).
- The main-idea key followed the formula “How X was developed and improved”.
- Inference explanations quoted truncated evidence (“…ว่า rain was delayed…”).

**Also changed:**
- 40 purpose stems aligned with their infinitive keys, e.g. “What did … learn?” → “Why did …?”.
- 58 templated purpose distractors (“expand X to neighboring towns”, “replace X before reviewing any participant feedback”, “prove X had already solved every participant’s problem”) replaced with passage-based ones.
- Option lengths balanced in 175 items, by lengthening a distractor or shortening the key.

Metrics (chance = 25%):

| Strategy | v42.0.1 | v42.0.2 |
|---|---:|---:|
| drop options containing the topic name, pick longest | **81.3%** | 24.0% |
| pick longest | 53.0% | 24.0% |
| drop options with absolutes, pick longest | 50.3% | 34.0% |
| max overlap with passage | 54.7% | 26.0% |
| pick second-longest | 5.3% | **36.7% (residual cue, open)** |
| topic name in a distractor | 67.3% | 0.1% |

Not rewritten: the 60 vocabulary-in-context items (only 13 length fixes) and the purpose-item keys (only stems and lengths). Answer positions 75/75/75/75. Keys were kept correct per passage; the evidence is quoted in each Thai explanation, and an automated check confirms every quoted English span exists in the item. **A human must still confirm each key is uniquely correct.**

Still open: near-duplicate RC passages (two home-energy passages S14-Q056/S20-Q051; two lost-property passages S07-Q046/S16-Q046); Short Conversation’s context-overlap cue (69.5%, not in round-3 scope).

## 4. Vocabulary
- **Noun-slot queue (1,217):**
  - definite grammar fix applied: 194 (plural/article only; each sentence stays generic and stays in the human queue)
  - needs human rewrite: 772
  - uncertain: 251
  - Statuses are written per row in REVIEW-QUEUE; there was no bulk rewrite.
- **146 headwords:**
  - not an established collocation (category label + noun, e.g. “reading answer”, “data graph”): 56 — retire/rename recommended
  - plausible collocation: 46
  - uncertain: 44
  - None deleted. Deletion would shift stored progress indices, so this is the editor’s decision.
- **IPA:**
  - 8 headwords that had no IPA or source now have CMUdict IPA plus a source label.
  - 742 phrases gained word-by-word CMUdict IPA, labelled as such (no phrase stress or weak forms).
  - **A stress-mark placement bug** across CMUdict-derived entries was fixed in 336 entries: the mark sat straight after the previous vowel, e.g. /kəˈmpɛɹ/, /ɪˈkspleɪn/, /səˈɡnɪfɪkənt/ → /kəmˈpɛɹ/, /ɪkˈspleɪn/, /səɡˈnɪfɪkənt/.
  - 83 hand-differing entries were left alone and queued. The 1,333 eSpeak entries still use eSpeak notation (queued).
- **Gloss/source alignment:**
  - 35 headwords whose main gloss does not contain the first sense meaning: queued (`qa/r3-gloss-scan.json`)
  - 87 phrases whose example does not contain the phrase verbatim: queued
  - 1 repeated gloss fixed (publish)
  - 2 exact reverse-duplicate antonym/confusable pairs removed
- **Games:**
  - Matching game: the v42.0.1 dedupe was dead code because a later override replaced it. The fix is now in the active override: unique words, unique displayed meanings, and a semantic guard using all glosses plus synonym/antonym/family lists. 400-round regression; 0/2,000 simulated conflicts, down from 80/2,000.
  - Translate, synonym and antonym MCQs filter distractors that overlap the key.

## 5. Accessibility and viewports
- axe-core 4.x (`tests/a11y_audit.py`): **144 scans** = 36 routes/states (all 9 routes, word detail, flashcards, vocab drills, Vocabulary Lab, mock exam before/after answering, TC/RC practice with feedback, sprint, Reading Lab, Hub unit, matching and sentence games, grammar, phrase bank, errors, adaptive, confirm dialog) × light/dark × 1366/390 px.
  - **0 violations in v42.0.2** (v42.0.1: 36 contrast violations in dark mode plus 8 flashcard label-name mismatches).
  - axe reports 4,760 “incomplete” contrast nodes (gradients, overlapping elements) that need manual or visual checking.
  - The original `regression_v42.py` axe scan (9 routes + lab): no critical or serious violations.
- Viewports tested in headless Chrome: 320, 390, 768, 1366, 1920 px (`smoke_r3_extra.py`, 94 checks); no horizontal overflow on any route.
- **Not done:** screen readers (VoiceOver/TalkBack/NVDA), iOS Safari, Android Chrome, real PWA install/update cycle, manual WCAG review. WCAG conformance is **not** claimed.

## 6. CSP, performance, patch structure
See `R3-ENGINEERING-ASSESSMENT.md`. A transitional CSP was added. Performance was measured, with recommendations but no code change. The patch-layer risk was quantified; it caused the dead matching-game fix.

## 7. Automated results for the shipped build (v42.0.2)
| Suite | Result |
|---|---|
| `node --check` on all 7 JS files | pass |
| `tests/smoke_test.py` (original) | 49/49 |
| `tests/regression_v42.py` (original, EXPECT_VERSION 42.0.2, axe on) | 60/60 |
| `tests/regression_r3_content.py` (new, 27 data/content regressions) | 27/27 |
| `tests/regression_r3_ui.py` (new: matching/MCQ guard, phrase IPA, axe deep states) | 7/7 |
| `tests/smoke_r3_extra.py` (new: 5 viewports, flows, offline) | 94/94 |
| `tests/a11y_audit.py` (144 axe scans) | 0 violations |

Automated tests do not certify English/Thai quality, distractor validity, pronunciation, or behaviour on physical devices.
