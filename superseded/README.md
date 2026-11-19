Files from a parallel session that worked in this folder on 2026-11-19 (≈09:43–10:50).
That session rewrote TC/RC items with its own specs; the question bank shipped in v42.0.2 uses the
round-3 specs in content/ (lc_*, tc_fixes_r3.py, rc_r3_[a-f].json, rc_lenfix*.json, rc_keyshort_r3.json)
applied by tools/rebuild_all.sh. These superseded files are kept for traceability only and are not applied.
The same parallel session's vocabulary, IPA, matching-game, accessibility and CSP work IS kept and applied.

Added 2026-11-19 (v43 task 1): tools/apply_lc_comp.py and content/lc_comp_r3_[e-h].json (the round-3
comprehension-style dialogues for LC sets 11-20) were retired from tools/rebuild_vault.sh because sets 11-20
are now blank fill-in dialogues applied by tools/apply_lc_blank.py from content/lc_blank_v43_[e-h].json.

Added 2026-11-19 (v43 task 2): tools/apply_tc.py and content/tc_fixes_r3.py (round-3 TC ambiguity fixes +
template-generated Thai explanations on the v42 passages) were retired from tools/rebuild_vault.sh because all
40 TC passages are now rewritten by tools/apply_tc_v43.py from content/tc_v43_[a-j].json (vocab/collocation
rebalance + missing grammar types). The round-3 checks that guarded those old passages remain in
tests/regression_r3_content.py and still pass trivially against the new content.

Added 2026-11-19 (v43 task 3): the round-3 RC pipeline (tools/apply_rc.py, apply_rc_len.py,
apply_rc_len2.py with content/rc_r3_[a-f].json, rc_lenfix*_r3.json, rc_keyshort*_r3.json,
rc_tplfix_r3.json) was retired from tools/rebuild_vault.sh. Those specs patched four of the five
items on each passage and left the v42.0.1 question-type pattern intact (main idea / sequence /
purpose / detail / word meaning on every passage). All 300 RC items are now rewritten by
tools/apply_rc_v43.py from content/rc_v43_[a-k].json + content/rc_v43_tips.json so that detail is
the most frequent type (120/300) and the blueprint's missing types are present: TRUE-statement 25,
paraphrase 25, attitude/tone 25, reference 24 (plus inference 21, purpose 21, main 18,
word-in-context 21). The round-3 RC gates in tests/regression_r3_content.py (template distractors,
longest-option heuristics, evidence-quotation check, 75/75/75/75 positions) still run and pass
against the new content.
