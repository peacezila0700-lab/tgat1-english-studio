# Question bank vs. TGAT1 blueprint (checked 2026-11-19)

## Sources

**Official**
- myTCAS blueprint “TGAT1 91 การสื่อสารภาษาอังกฤษ” (TCAS70 page): https://mytcas.com/blueprint/tgat1-91/
- myTCAS sample items: https://blueprint.mytcas.com/tgat1-91/
- The page itself says the blueprint and samples do not guarantee the format of the current year’s exam.

**Third party, not official**
- OnDemand tutor handout: question-type counts for 2567 and 2568, compiled from tutors’ analysis. https://www.ondemand.in.th/wp-content/uploads/2025/12/LRF-20250115-Liveคืนหมาหอมติว-TGAT1-เอกสารติว_ลายน้ำ-1.pdf
- TruePlookpanya course pages.

**Not available**
- Real past papers are not published.
- Facebook content could not be searched or read from this environment.

## Structure: matches the blueprint
| Part | Blueprint | Bank (per set × 20) | Result |
|---|---|---|---|
| Question-Response | 10 | 10 | ✓ |
| Short conversations | 3 conversations, 3–4 blanks, 10 items | 3 conversations (3/3/4), fill-in, 10 | ✓ |
| Long conversations | 2 conversations × 5, **fill-in (เติมบทสนทนา)** | sets 1–10 fill-in ✓; **sets 11–20 comprehension questions ✗** | partial |
| Text completion | 2 passages, 7–8 blanks, 15 | 2 passages (7+8), 15 | ✓ |
| Reading comprehension | 3 passages × 5, 100–200 words | 3 × 5, 106–136 words | ✓ |
| Format | 4 options, 60 items, 60 min | 4 options, 60 items | ✓ |

## Content mix: gaps found
1. **Long conversation format.**
   - Bank: 100 of 200 items (sets 11–20) ask comprehension questions (“What are the speakers mainly discussing?”).
   - Blueprint: the part is a dialogue-completion task.
   - Fix: convert these 20 dialogues to fill-in-the-blank items.
2. **Text completion targets.**
   - Bank: 241 of 300 blanks (80%) test function words (prepositions, conjunctions, relatives); 30 test word or verb forms; only 29 test vocabulary or collocation.
   - Official sample: both blanks are content words (“community”, “feel”).
   - Tutor counts:
     - 2567: 11 of 15 blanks were vocabulary/collocation.
     - 2568: a wider grammar spread, including finite/non-finite verbs, tense/voice/modals, relative and noun clauses, inversion, question tags, and sentence connectors (Instead/Similarly/Ultimately).
   - Fix: rebalance to roughly 40–50% vocabulary/collocation and add the missing grammar types.
   - **Status v43 (2026-11-19): DONE.** All 40 TC passages rewritten (`content/tc_v43_[a-j].json`, applied by `tools/apply_tc_v43.py`): 125/300 blanks (41.7%) vocabulary/collocation; grammar spread now includes verb forms (46), tense/voice (46), relative/noun clauses (34), connectors/prepositions (27), inversion (10, e.g. Not only.../Rarely.../Only when.../So careful was...) and question tags (12). Answer positions stay exactly 75/75/75/75.
3. **Text types and difficulty.**
   - Bank: every TC/RC passage, and most LC dialogues, is a “community/school project → trial → evaluation” story.
   - Official and tutor samples: news, notices or ads and expository texts, e.g. Centre Pompidou closure, a relocation advert, AI-generated images, “nepo babies”, tariffs, live-stream selling.
   - Fix: diversify genres and raise the lexical level of TC and RC.
4. **Reading question types.**
   - Bank: every passage uses the same 5 types (main idea, sequence, purpose, word-in-context, inference), 20% each.
   - Tutor counts per 15 items:
     - details: 6–7
     - main idea/purpose: 1–4
     - word in context: 3
     - inference: 0–2
     - reference, paraphrase, evidence: 0–2 each
   - The official sample includes author’s purpose, “true statement” and a person’s position.
   - Missing from the bank: “Which statement is TRUE”, reference (“it refers to”), paraphrase, attitude/stance.
   - Fix: vary the 5 questions per passage, with details as the largest share.
   - **Status v43 (2026-11-19): DONE.** All 300 RC items rewritten (`content/rc_v43_[a-k].json` + per-type tips in `content/rc_v43_tips.json`, applied by `tools/apply_rc_v43.py`): details 120/300 (40%, largest share), TRUE-statement 25, paraphrase 25, attitude/tone 25, reference 24, inference 21, purpose 21, word-in-context 21, main idea 18. Every passage now carries a different combination of 5 types instead of one fixed pattern. Answer positions stay exactly 75/75/75/75; key-longest 20% (gate ≤30%), second-longest 44.0% (gate ≤50%), drop-topic-pick-longest 20% (gate ≤35%). The retired round-3 RC pipeline is in `superseded/`.
5. **Question-Response.**
   - The format matches.
   - Bank: mostly wh-question/answer-type matching and polite requests.
   - Tutor samples also stress idiomatic or social responses (“Small world, isn’t it?”) and functional replies.
   - Fix: add more idiomatic/social-function items.

## Conclusion
The structure of the 1,200-item bank matches the official blueprint, apart from the LC format in sets 11–20.

The content mix differed from the official sample items and from third-party analyses of the 2567–2568 exams in four ways: TC is grammar-heavy (fixed in v43), passage genres are narrow (still open, task 4), RC question types are uniform (fixed in v43), and LC sets 11–20 are comprehension rather than completion (fixed in v43).

The questions are original practice material written for this app, not taken or adapted from real TGAT1 papers. They should not be presented as matching the real exam in difficulty or distribution.
