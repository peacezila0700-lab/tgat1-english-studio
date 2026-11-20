# TGAT1 English Studio v42.0.1 — Round 2 status

**Status: remediation build; not final production approval.** This patch follows the v42.0.0 Round 2 work with additional vocabulary-game/data fixes, regenerated practice content, updated PWA cache/versioning, and a fresh automated regression pass. It does not certify editorial quality or accessibility conformance. Practice questions are original practice material, **not official TGAT1 questions and not a score prediction**.

## Corrected / improved in v42.0.1
- Rewrote the Long Conversation and Text Completion source contexts: structural audit finds **40 unique LC contexts linked to 200 questions** and **40 unique TC passages linked to 300 questions**, across all 20 sets. Per-set blueprint/group sizes are preserved. TC answer positions are balanced A/B/C/D = 75 each. Text themes may still recur; uniqueness is not a claim of human editorial quality.
- Improved the vocabulary matching game to fill five-item rounds when the selected five include duplicate first-gloss meanings, and avoid repeated words/first-gloss meanings within a round where the usable pool allows it.
- Vocabulary Lab retains genuine exam-context matches first and now includes valid vocabulary entries with a stored example as a fallback pool; the UI identifies these as vocabulary examples rather than exam-source contexts. This prevents the source-matching filter from shrinking practice to a small set after the bank was revised.
- Word-detail UI now shows the recorded IPA source with each entry and cautions that eSpeak-generated IPA may differ in notation/stress from CMUdict and should be checked by listening. This improves provenance transparency; it is not a pronunciation audit.
- Bumped app/content/cache/manifest metadata to **42.0.1** so existing v42.0.0 PWA caches are replaced on update.
- Earlier v42.0.0 fixes remain: corrected 492 researcher-subject translations, four glued translations, five incomplete example translations, seven flagged meta-language examples, six Hub explanations, approximate (not CEFR) Reading Lab labels, TC word counts excluding blank markers, phrase taxonomy and selected lexical/flashcard/accessibility fixes.

## Still open — do not claim complete or production-ready
1. **RC distractors:** no full rewrite of 300 RC items. The documented answer-length/project-name heuristic bias remains; existing RC results are not calibrated reading-ability estimates.
2. **Content editorial review:** all newly rewritten LC/TC contexts require English/Thai human review for naturalness, factual coherence, level and question-answer fit. The 40 TC passages still reuse some broad themes. The full 1,200-question bank has not been read line by line.
3. **Vocabulary quality:** the noun-slot example queue still has **1,217** items requiring human review; **146** headwords remain in validity review. Matching-game uniqueness is based on the first gloss only, not full semantic equivalence. Phrase/headword translation alignment, missing phrase IPA, distractor-length balance and broader synonym/antonym/family/duplicate-meaning review remain open.
4. **Contrast/accessibility:** theme-aware CSS and flashcard keyboard semantics are in place, but no axe-core scan was run in this environment and no assistive-technology/device audit has been completed. Do not claim WCAG conformance.
5. **P3/engineering:** strict CSP is not added because inline event handlers are pervasive; initial-load performance and the large nested-patch refactor were not addressed.
6. **Human/real-device validation:** iOS Safari, Android Chrome, real screen readers, a real PWA installation/update cycle, and complete language proofreading remain untested. Automated checks do not certify English/Thai quality, distractor validity, or PWA behavior on physical devices.

## Verification performed for v42.0.1
- `node --check`: app.js, learning-hub.js, learning-hub-curriculum.js, sw.js — passed.
- `smoke_test.py`: **49/49 passed** (desktop/mobile routes, main flows, Hub, offline checks).
- `regression_v42.py`: **59/59 passed**, including bank/vault structure, balanced TC answer positions, 12 generated match-game rounds and a correct-pair completion flow, vocabulary pool/options, SRS, Hub, mock/resume, import/export, responsive layout, keyboard focus, and PWA/offline checks.
- axe-core scan: **not run** (AXE_PATH/core not provided).
- Automated structural checks confirm 1,200 questions in the 20-set blueprint, 40 unique LC contexts, 40 unique TC passages and balanced TC answer positions. This does not verify the generated passages by a human.
