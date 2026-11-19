# Changelog — v42.0.1 (Round 2 remediation follow-up)

Date: 2026-11-18. Follow-up build after v42.0.0 Round 2 remediation.

## Changes
- Rebuilt Long Conversation and Text Completion content to use 40 unique contexts/passages each (200 LC questions and 300 TC questions). Set blueprint and group sizes are retained; TC correct-answer positions are distributed 75 per option position.
- Improved the five-pair vocabulary matching game to avoid duplicate words and duplicate first-gloss meanings in a round, while filling from the same difficulty group when possible.
- Expanded Vocabulary Lab eligibility to valid entries with stored example fallbacks, retaining source-matched exam contexts as the preferred pool. The interface distinguishes fallback examples from question-bank contexts.
- Display IPA source attribution on word detail and distinguish eSpeak output from CMUdict in the pronunciation caveat.
- Bumped app, content, manifest and service-worker cache version to 42.0.1 to ensure existing v42.0.0 installations receive the updated assets.
- Added two automated matching-game regression checks; updated the test suite and status documentation.

## Verification
- `node --check app.js learning-hub.js learning-hub-curriculum.js sw.js`: passed.
- `smoke_test.py`: 49/49 passed.
- `regression_v42.py`: 59/59 passed, including TC answer-position balance.
- axe-core and physical-device/editorial reviews were not performed. See `ROUND2-STATUS.md` for remaining risks.
