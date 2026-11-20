# TGAT1 English Studio v42.0.2 — Round 3 status

**Status: remediation build, not final production approval.** Practice questions are original practice material: **not official TGAT1 questions, not past papers, and not a score prediction.** No human editor, screen-reader user or physical device has reviewed this build.

## Fixed in v42.0.2 (details: qa/R3-QA-LOG.md, qa/DATA-CHANGES.csv)
- **Long Conversation (200 items):**
  - The 20 blank-fill dialogues all used one fixed template; they were rewritten from scratch (100 items).
  - The 20 comprehension dialogues (100 items) were revised with natural contractions, specific stems, plausible distractors and Thai explanations.
  - Answering by longest option now scores 24% (was 49.5%); the absolutes rule scores 27.5% (was 68.5%).
- **Text Completion (300 items):**
  - 84 fixes: one wrong key, items with a second correct option, 15 sentences copied from other passages, illogical sequences.
  - All 300 explanations are now Thai and show the completed sentence (template-assisted).
- **Reading Comprehension:**
  - 180 items rewritten (main idea, sequence, inference); 58 templated distractors and 40 mismatched stems fixed; option lengths balanced.
  - The “drop the option with the topic name, pick the longest” strategy now scores 24% (was 81.3%).
- **Vocabulary:**
  - 1,217-item noun-slot queue triaged: 194 grammar fixes, 772 need a human rewrite, 251 uncertain.
  - 146 headwords triaged: 56 not established, 46 plausible, 44 uncertain. None deleted.
  - Missing IPA added for 8 headwords and 742 phrases (CMUdict, labelled).
  - A stress-mark placement bug was fixed in 336 CMUdict-derived entries.
  - Matching game: the de-duplication fix now runs in the active code, plus a semantic guard. MCQ distractors that overlapped the key were removed.
- **Accessibility:** dark-mode contrast and the flashcard accessible name fixed. axe-core 4.x: 0 violations across 144 scans (36 states × light/dark × desktop/mobile).
- **Security/engineering:** transitional CSP added. Performance and the patch-layer structure were assessed (qa/R3-ENGINEERING-ASSESSMENT.md).
- **Release:** app, content, cache, manifest and data headers are all 42.0.2, so installed PWAs pick up the new assets.

## Still open — do not claim complete or production-ready
1. **Human editorial review** of all round-3 content (200 LC, 300 TC explanations, 180+ RC items) and of the remaining bank. No item has been proofread by a person.
2. **Residual option cues:**
   - RC: the second-longest option is the key in 36.7% of items; the absolutes rule scores 34%.
   - LC: second-longest is 42.5%.
   - Short Conversation: the context-overlap rule scores 69.5% (not in round-3 scope).
   - Several RC/TC passages repeat themes.
3. **Vocabulary decisions:** 772 + 251 example sentences, 146 headword decisions, 35 gloss/sense mismatches, 87 phrase examples, 1,333 eSpeak IPA entries in a different notation, and 83 IPA entries to listen-check.
4. **Accessibility:** no screen-reader or manual WCAG audit; 4,760 axe “incomplete” contrast nodes need visual checks. WCAG conformance is not claimed.
5. **Devices:** iOS Safari, Android Chrome, a real PWA install/update cycle and real-network load times are untested.
6. **Engineering:**
   - Strict CSP needs about 300 inline handlers refactored.
   - The 2 MB `data.js` blocks the first render; enable gzip/brotli on the host.
   - 45 override layers, with 43 monkey-patched functions, remain.

## Verification for v42.0.2
- `node --check` (7 JS files): pass
- `smoke_test.py`: 49/49
- `regression_v42.py`: 60/60, including axe
- `regression_r3_content.py`: 27/27
- `regression_r3_ui.py`: 7/7
- `smoke_r3_extra.py`: 94/94
- `a11y_audit.py`: 0 violations in 144 scans
