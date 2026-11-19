# Changelog — v42.0.2 (Round 3 remediation)

Date: 2026-11-19. Follows v42.0.1.

## Content
- **Long Conversation:**
  - Rewrote the 20 templated blank-fill dialogues (100 items).
  - Revised the 20 comprehension dialogues and their 100 items: contractions, specific stems, plausible distractors, Thai explanations.
- **Text Completion:**
  - 84 item fixes: wrong key, second correct options, 15 off-topic copied sentences, illogical sequences.
  - 300 Thai explanations showing the completed sentence.
- **Reading Comprehension:**
  - 180 items rewritten.
  - 58 templated distractors replaced and 40 stems aligned with their keys.
  - Option lengths balanced.
  - Answer positions 75/75/75/75.

## Vocabulary and pronunciation
- Noun-slot triage: 194 grammar-only fixes; REVIEW-QUEUE statuses updated row by row.
- 146 headwords triaged (no deletions).
- IPA:
  - 8 headwords and 742 phrases filled from CMUdict (labelled word-by-word).
  - 336 CMUdict entries had the primary-stress mark moved to the syllable onset.
- 1 repeated gloss fixed; 2 reverse-duplicate pairs removed.

## App
- **Matching game:** de-duplication now lives in the active `mkMatch` override, with a semantic overlap guard across all glosses and synonym/antonym/family lists.
- Vocabulary MCQ and antonym-game distractor filters added.
- Phrase detail shows IPA and its source.
- Dark-mode contrast fixes; flashcard accessible name now uses the visible text plus `aria-pressed`.
- Transitional Content-Security-Policy meta.
- Version bump to 42.0.2: app, content, cache `tgat1-studio-v42.0.2`, manifest, data headers.

## Tests
- Original suites now expect 42.0.2: smoke 49/49, regression 60/60 (axe).
- New suites: `regression_r3_content.py` (27), `regression_r3_ui.py` (7), `smoke_r3_extra.py` (94), `a11y_audit.py` (144 scans, 0 violations).
