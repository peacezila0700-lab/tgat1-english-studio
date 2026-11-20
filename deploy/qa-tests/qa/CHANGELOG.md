# CHANGELOG

## v41.0.0 — 2026-11-18

Release type: data-quality + bug-fix release on top of v40.9.0. Learner data, storage keys, the 1,200-question bank (`data-vault.js` byte-identical), the 70-unit Learning Hub, the /100 mock scale, import/export and offline behaviour are preserved.

### Fixed — application
- **Vocabulary Lab answers were guessable.** Thai meanings were compared with an ASCII-only normaliser, so every Thai gloss collapsed to an empty key and was filtered out; distractors came only from six English-tainted glosses and the correct answer was the only pure-Thai option. Meanings are now compared with a Unicode-aware key; English-tainted glosses are never offered; distractors that share a meaning segment with the answer (or each other) are rejected.
- **Vocabulary Lab SRS grades were never saved.** The module called an undeclared `save()` that resolved to the legacy game's global `save` (key `eng3`). It now saves `tgat1_studio_vocab_progress_v1`; session kind `examVocab` is accepted by the data guard.
- **Progress for 7 runtime-added (PACK) words was dropped on every reload** because the vocab state was normalised before the PACK merge. The guard now receives the full word list.
- Word detail / flashcards / Lab feedback show the new `note` field (comparisons and antonym pairs moved out of the main gloss).
- Vocabulary filter and word detail label A/B/C as an internal difficulty group (not CEFR); source tag reads "ที่มา: …" with an "unverified" tooltip.
- Accessibility: mobile-nav text contrast 3.24:1 → ~5.9:1 (light) with a dark-mode colour; dark breadcrumb 3.09:1 fixed; Vocabulary Lab context box in dark mode was 1.04:1 (unreadable) — fixed; Learning Hub unit buttons no longer use an aria-label that omits the visible text.
- Version unified to 41.0.0 (`TGAT1_VERSION`, index meta, manifest, service-worker cache `tgat1-studio-v41.0.0`, data headers).

### Fixed — content (field-level before/after in `qa/DATA-CHANGES.csv`, 3,940 changes, 1,287 headwords)
- 79 antonym-category glosses that showed both opposites ("ดีขึ้น - แย่ลง") → the word's own meaning; pair kept in `note`; template translations and "The situation became X…" examples rewritten.
- 118 commonly-confused entries: headword/sense POS corrected (e.g. `during` prep, `a few` det, `its` det), clean Thai glosses, comparisons moved to `note`.
- 11 glosses with embedded English (audit counted 10) → Thai-only.
- 23 adverbs whose gloss was a template sentence ("การเปลี่ยนแปลงเกิดขึ้น…ตามรายงาน") + 2 with a bogus usage tag → rewritten.
- 26 spurious "(ใช้ในบริบทของ…)" tags removed; truncated `maintenance` and unbalanced `few`/`during` glosses fixed.
- 425 meta-language examples ("The adjective 'X' gives a more precise description…") and 538 adjective/adverb/verb filler templates (often ungrammatical, e.g. "decided to worsen the plan") rewritten with natural sentences and matching Thai translations.
- Polysemy: `account`, `address`, `claim`, `issue` split into 3 aligned senses; `attempt`, `relative` split into 2; further POS fixes (`idea`, `offset`, `opt for`, `poor`, `slight`, `upside`, `rich`, `say`, `many`, `intensify`, `sponsor`).
- 98 category labels that implied official/past-paper TGAT1 provenance relabelled as reference/practice vocabulary.
- 31 Thai misspellings (dropped ำ, doubled prefixes) in the legacy matching-game bank.
- 9 conversational phrases whose example was the phrase itself now have a short dialogue.

### Added
- `regression_v41.py` (49 checks: content integrity, Lab option integrity, SRS persistence across reload, Hub isolation, full mock 100/100, save/resume, export/import, 390/1280 overflow, keyboard/focus, offline/PWA v41 cache, optional axe-core scan).
- `qa/` folder: AUDIT-REPORT.md, SOURCE-REGISTER.csv, REVIEW-QUEUE.csv (1,491 rows), DATA-CHANGES.csv, test logs, SHA-256 lists.

### Known limitations (not certified)
- 1,217 noun-slot filler examples remain and are queued for human review; 146 synthetic "domain × noun" headwords are queued (not deleted).
- Sources `Complete Guide`, `TGAT1 curated vocabulary`, `เพิ่มใหม่` are unidentified; do not distribute publicly until provenance/rights are confirmed.
- New example sentences were drafted by an AI editor; a 120-row random sample is queued for proof-reading.
- Not tested on physical iOS/Android devices, real screen readers or installed PWAs.

## v42.0.2 — Round 3 (2026-11-19)
See qa/R3-QA-LOG.md, qa/R3-ENGINEERING-ASSESSMENT.md and web/CHANGELOG-v42.0.2.md. LC rewritten/revised (200), TC 84 fixes + 300 Thai explanations, RC 180 rewritten + cue balancing, vocabulary triage (1,217 + 146), IPA fill + stress fix (336), matching-game guard, dark-mode contrast (axe 144 scans, 0 violations), transitional CSP. Not human-reviewed.
