# TGAT1 English Studio v42.0.0 — Round 2 status

**Status: remediation build, not a final production approval.** This package contains verified code/data fixes and deployment hygiene improvements. Several high-impact content findings still require original editorial work; they are deliberately not disguised by weak automatic rewrites. Practice questions are original practice material, **not official TGAT1 questions and not a score prediction**.

## Corrected in this build
- Vocabulary Lab now chooses a source only from a question `context` that actually contains the searched headword; otherwise the existing sense-example fallback is used.
- Repaired all **492** confirmed English-subject/Thai-subject mismatches (`researchers` had been translated as “team”) and elevated these entries in `qa/REVIEW-QUEUE.csv` for human confirmation.
- Corrected four Thai/English-glued translations, five example translations that previously only repeated the headword meaning, and seven confirmed meta-language examples.
- Six Learning Hub explanations now refer to the answer text, not A/B/C/D labels that are shuffled in the UI.
- Re-labelled Reading Lab difficulty as approximate, explicitly not CEFR; Text Completion word counts now exclude numbered blank markers (133 and 138 words for the two displayed passages).
- Normalized phrase-type labels to nine categories; duplicate phrase comparison now ignores common punctuation variants; removed the confirmed bad synonym/word-family cases and exact reverse antonym duplicate.
- Leaving the vocabulary page clears flashcard session state. Flashcard interaction now has button semantics, keyboard activation, and an accessible name.
- Added theme-variable styling for reported result/review/feedback regions and made the light-theme mock review context readable. These CSS changes are **not a substitute for a full state-by-state dark-mode visual/contrast audit**.
- Updated version/cache metadata to 42.0.0. Production ZIP excludes backups, QA source data, old scripts, and intermediate files. Updated the old vocabulary QA note as historical/superseded and repaired the malformed SRC-10 CSV record.
- Random mock group selection avoids reusing the exact same non-empty passage context twice within a single random mock. This does not repair duplicated fixed-set content.

## Still open — blocks a “complete” or production-ready claim
1. **RC distractors (#1):** no full rewrite of 300 RC items. The documented answer-length/project-name heuristic bias (~70.8% expected under the reported strategy) remains. Existing RC results should not be interpreted as calibrated reading ability.
2. **Long Conversation (#2):** sets 11–20 still repeat the long-dialogue source texts used in sets 1–10. The random-mock exact-context guard only prevents selecting identical contexts twice in one random mock; it does not create the missing 20 dialogues or fix fixed sets.
3. **Text Completion (#3):** story-source repetition (40 passages derived from 10 story themes) remains.
4. **Contrast/a11y (#5, #21):** broad theme-aware overrides and flashcard keyboard semantics are in place, but the reported states have not been re-audited with axe-core or assistive technology. Regression explicitly reports that axe-core was not available. Do not claim the contrast findings fully resolved.
5. **Legacy examples (#11):** only the confirmed report/passage meta-language patterns are filtered from the historic-example panel. The larger generic-example inventory still needs review.
6. **Remaining P2:** phrase/headword translation-source alignment; IPA normalization/source labeling; missing phrase IPA; distractor-length imbalance; further synonym/antonym/family and legacy duplicate-meaning game review; broader accessibility/contrast; and complete content review remain open.
7. **P3:** strict CSP is not added because inline event handlers are pervasive; initial-load performance and large nested-patch refactor have not been addressed.
8. **Human/real-device validation:** 1,217 examples remain in the existing generic-example queue; 146 headwords remain in validity review; 70 Hub lessons and the full 1,200-item question bank were not read line-by-line. iOS Safari, Android Chrome, real screen readers, and an actual PWA installation were not tested.

## Verification performed
- `node --check`: app.js, learning-hub.js, learning-hub-curriculum.js, sw.js — passed.
- `smoke_test.py`: **49/49 passed** (desktop/mobile routes, main flows, Hub, offline checks).
- `regression_v42.py`: **48/48 passed** for the present regression assertions, including 1,200-question structure, complete mock, persistence, mobile/desktop layout and keyboard checks. Its optional axe-core scan was skipped because AXE_PATH/core was not supplied.
- Added targeted Round 2 data checks: no remaining flagged `researchers` translation, glued translation, five untranslated examples, or seven meta-language examples; TC word-count and approximate-level checks pass; phrase-type count ≤10.
- These automated checks do not certify English/Thai quality, distractor validity, or complete WCAG conformance.
