# CODE-AUDIT v43 — ภาคผนวก (สร้างอัตโนมัติด้วย /root/tgat/audit.py, ไม่ได้แก้โค้ด)

## A1. แผนที่ชั้น patch ใน web/app.js (comment หัว section)

- L19: 01 · 29-stability-kernel-v37.js
- L101: 02 · 00-data-normalizers.js
- L262: 03 · 00-legacy-quest-core.js
- L636: 04 · 01-studio-app.js
- L1362: 05 · 02-v12-quality.js
- L1611: 06 · 17-backup-import-guard.js
- L1639: 07 · 03-stability-backup.js
- L1938: 08 · 04-pwa-register.js
- L1942: 09 · 05-question-quality.js
- L1968: 10 · 06-srs-engine.js
- L2008: 11 · 07-smart-dashboard.js
- L2079: 12 · 19-exam-draft-guard.js
- L2139: 13 · 08-exam-engine.js
- L2185: 14 · 09-accessibility.js
- L2216: 15 · 10-quality-audit.js
- L2347: 16 · 11-question-audit.js
- L2413: 17 · 12-vocabulary-upgrade.js
- L2485: 18 · 20-learning-state-guard.js
- L2576: 19 · 13-learning-modules.js
- L2673: 20 · 14-unified-vocab-progress.js
- L2748: 21 · 15-learning-intelligence.js
- L2892: 22 · 16-learning-explanations.js
- L2949: 23 · 18-page-visual-system.js
- L3086: 24 · 21-question-explanations.js
- L3201: 25 · 22-language-practice-upgrade.js
- L3813: 26 · 23-functional-quality-fixes.js
- L3972: 27 · 24-final-functional-content-fixes.js
- L4139: 28 · 25-learning-system-v36.js
- L4306: 29 · 26-deep-quality-v36-1.js
- L4390: 30 · 27-production-hardening-v36-2.js
- L4502: 31 · 28-complete-learning-hardening-v36-3.js
- L4670: 32 · 30-v37-8-deep-audit.js
- L4743: 33 · 33-tgat1-content-expansion-v38-2.js
- L4872: 34 · 41-content-expansion-v39-5.js
- L4877: 35 · 42-tgat1-v40-content-integrity.js
- L4930: 36 · 37-mipad6-runtime-hardening.js
- L4956: 37 · 41-unified-audio-v40.js
- L5049: 38 · 43-semantic-content-quality-v40-2.js
- L5073: 39 · 45-offline-picture-bank-v40-4.js
- L5299: 40 · 46-exam-diversity-v40-4.js
- L5384: v40.6.7 consolidated quality + runtime hardening
- L5547: 41 · external-link offline notice (v40.7.27)
- L5770: v40.9.0 content audit (detection only; it never edits content)
- L5829: v42.0.0 TGAT1 Vocabulary Lab: bank-linked lexical practice + SRS
- L5873: v42.0.2 matching-game semantic guard

## A2. ฟังก์ชันที่ถูกนิยามซ้ำ (ตัวล่างสุดคือตัวที่ทำงานจริง ถ้าเป็น global)

รวม 66 ชื่อ

| ชื่อ | จำนวน | บรรทัด |
|---|---|---|
| `fn` | 7 | 4078, 4081, 4084, 4089, 4100, 5508, 5525 |
| `start` | 6 | 344, 888, 2045, 2856, 5765, 5856 |
| `audit` | 6 | 1947, 2232, 2398, 4640, 4874, 5055 |
| `add` | 6 | 321, 506, 1712, 1858, 3260, 3502 |
| `VLT_finish` | 5 | 611, 1324, 1582, 2177, 2872 |
| `studioRender` | 5 | 690, 1064, 1308, 2667, 4852 |
| `wrapped` | 5 | 4044, 4051, 4058, 5694, 5715 |
| `play` | 4 | 422, 886, 2476, 3678 |
| `VLT_startCategory` | 4 | 515, 3880, 4534, 5463 |
| `VLT_begin` | 4 | 523, 1322, 1564, 2166 |
| `VLT_renderQuiz` | 4 | 590, 1320, 1566, 2164 |
| `studioUpdateChrome` | 4 | 688, 1066, 1310, 4848 |
| `studioNav` | 4 | 689, 1110, 1154, 4850 |
| `bank` | 4 | 2228, 4516, 4681, 5390 |
| `decorate` | 4 | 2847, 2965, 4287, 4378 |
| `safe` | 4 | 2896, 4315, 4400, 4514 |
| `ans` | 3 | 347, 2471, 3904 |
| `explain` | 3 | 351, 2481, 3178 |
| `finish` | 3 | 369, 1062, 5865 |
| `hint` | 3 | 398, 2905, 3150 |
| `xbody` | 3 | 399, 2469, 3769 |
| `mt` | 3 | 403, 2470, 2719 |
| `VLT_startQuick` | 3 | 516, 4540, 5471 |
| `VLT_startDaily` | 3 | 517, 4544, 5476 |
| `VLT_startReview` | 3 | 520, 3890, 5511 |
| `VLT_prev` | 3 | 605, 1576, 2171 |
| `VLT_goto` | 3 | 606, 1578, 2172 |
| `VLT_exit` | 3 | 610, 1326, 2170 |
| `VLT_renderResult` | 3 | 616, 1588, 2175 |
| `VLT_home` | 3 | 692, 1557, 2173 |
| `studioWordDetail` | 3 | 847, 1501, 3699 |
| `esc` | 3 | 1953, 1975, 2838 |
| `save` | 3 | 274, 1973, 2631 |
| `render` | 3 | 2279, 4725, 5862 |
| `sweep` | 3 | 4130, 4300, 5030 |
| `run` | 3 | 4881, 5032, 5819 |
| `recordWord` | 2 | 315, 2679 |
| `mkMatch` | 2 | 393, 2468 |
| `mkSpell` | 2 | 394, 2473 |
| `spk` | 2 | 405, 2472 |
| `VLT_dailyPool` | 2 | 518, 3871 |
| `VLT_mixPool` | 2 | 519, 3867 |
| `VLT_startFavorites` | 2 | 521, 5481 |
| `VLT_startSprint` | 2 | 522, 5487 |
| `VLT_answer` | 2 | 604, 2168 |
| `VLT_next` | 2 | 607, 1580 |
| `VLT_retry` | 2 | 622, 1591 |
| `VLT_retryWrong` | 2 | 623, 5517 |
| `home` | 2 | 628, 691 |
| `studioHome` | 2 | 694, 1302 |
| `studioVTab` | 2 | 828, 4846 |
| `studioPhraseDetail` | 2 | 849, 3707 |
| `studioStartFlashcards` | 2 | 852, 2003 |
| `studioRenderFlash` | 2 | 853, 3727 |
| `studioFlashFlip` | 2 | 854, 2002 |
| `studioExam` | 2 | 879, 1555 |
| `hashText` | 2 | 1681, 2299 |
| `verifyEnvelope` | 2 | 1689, 2300 |
| `addError` | 2 | 3841, 4033 |
| `panel` | 2 | 4370, 4645 |
| `schedule` | 2 | 4493, 5764 |
| `V15_render` | 2 | 1992, 3749 |
| `int` | 2 | 107, 2491 |
| `safeLoad` | 2 | 3822, 4149 |
| `safeSave` | 2 | 3823, 4150 |
| `write` | 2 | 4401, 4515 |

## A3. จุดที่เก็บฟังก์ชันเดิมแล้วเขียนทับ (monkey-patch)

- L70: `original = window.VLT_begin`
- L75: `original = window.VLT_answer`
- L338: `TGAT_ITEMS = window.__TGAT1_DATA.items`
- L628: `VLT_legacyHome = home`
- L637: `STUDIO_DATA = window.__TGAT1_DATA.studio`
- L886: `studioOriginalPlay = play`
- L888: `studioOriginalStart = start`
- L1062: `studioOriginalFinishV6 = finish`
- L1064: `studioOriginalRenderV6 = studioRender`
- L1066: `studioOriginalChromeV6 = studioUpdateChrome`
- L1109: `original = window.studioNav`
- L1153: `prev = window.studioNav`
- L1301: `originalHome = studioHome`
- L1307: `originalRender = studioRender`
- L1309: `originalUpdate = studioUpdateChrome`
- L1319: `oldRenderQuiz = VLT_renderQuiz`
- L1321: `oldBegin = VLT_begin`
- L1323: `oldFinish = VLT_finish`
- L1325: `oldExit = VLT_exit`
- L1497: `VLT_explainPanelOriginal = VLT_explainPanel`
- L1501: `studioWordDetailOriginal = studioWordDetail`
- L1555: `studioExamOriginalV12 = studioExam`
- L1557: `VLT_homeOriginalV12 = VLT_home`
- L1564: `VLT_beginOriginalV12 = VLT_begin`
- L1566: `VLT_renderOriginalV12 = VLT_renderQuiz`
- L1576: `VLT_prevOriginalV12 = VLT_prev`
- L1578: `VLT_gotoOriginalV12 = VLT_goto`
- L1580: `VLT_nextOriginalV12 = VLT_next`
- L1582: `VLT_finishOriginalV12 = VLT_finish`
- L1588: `VLT_renderResultOriginalV12 = VLT_renderResult`
- L1591: `VLT_retryOriginalV12 = VLT_retry`
- L1600: `studioAnalyticsOriginalV12 = studioAnalytics`
- L2002: `oldFlip = studioFlashFlip`
- L2163: `oldRender = VLT_renderQuiz`
- L2165: `oldBegin = VLT_begin`
- L2167: `oldAnswer = VLT_answer`
- L2169: `oldExit = VLT_exit`
- L2171: `oldPrev = VLT_prev`
- L2172: `oldGoto = VLT_goto`
- L2173: `oldHome = VLT_home`
- L2174: `oldResult = VLT_renderResult`
- L2176: `oldFinish = VLT_finish`
- L2327: `oldRenderQuiz = window.VLT_renderQuiz`
- L2332: `oldFinish = window.VLT_finish`
- L2334: `oldRenderResult = window.VLT_renderResult`
- L2337: `oldExit = window.VLT_exit`
- L2339: `oldBegin = window.VLT_begin`
- L2397: `originalAudit = prior.audit`
- L2469: `originalXbody = xbody`
- L2471: `originalAns = ans`
- L2472: `originalSpk = spk`
- L2476: `originalPlay = play`
- L2481: `originalExplain = explain`
- L2667: `oldRender = studioRender`
- L2677: `originalRecordWord = window.recordWord`
- L2871: `original = window.VLT_finish`
- L3013: `oldVocab = window.studioVocabulary`
- L3015: `oldExam = window.studioExam`
- L3020: `oldChrome = window.studioUpdateChrome`
- L3022: `oldQuestion = window.STR_renderQ`
- L3024: `oldReview = window.STR_review`
- L3070: `oldProfilePage = window.studioProfile`
- L3677: `previousPlay = play`
- L3698: `previousWordDetail = studioWordDetail`
- L3706: `previousPhraseDetail = studioPhraseDetail`
- L3726: `oldRenderFlash = studioRenderFlash`
- L3748: `oldV15Render = window.V15_render`
- L3768: `oldXbody = xbody`
- L3820: `MAX_RECENT = 80`
- L3821: `MAX_ERRORS = 1200`
- L3870: `oldDaily = window.VLT_dailyPool`
- L3879: `oldCategory = window.VLT_startCategory`
- L3889: `oldReview = window.VLT_startReview`
- L4043: `old = window.STG_answer`
- L4050: `old = window.STR_answer`
- L4057: `old = window.VLT_answer`
- L4078: `old = VLT_mixPool`
- L4081: `old = VLT_dailyPool`
- L4084: `old = VLT_startCategory`
- L4087: `oldMkPic = window.mkPic`
- L4098: `oldPlay = window.play`
- L4846: `originalVTab = studioVTab`
- L4848: `previousChrome = studioUpdateChrome`
- L4850: `previousNav = studioNav`
- L4852: `previousRender = studioRender`
- L4854: `originalReadingBack = window.renderReadingBack`
- L5523: `oldRetry = window.VLT_retry`
- L5566: `previouslyFocused = document.activeElement`
- L5865: `old = run`

## A4. catch ว่าง (กลืน error เงียบ)

L2, L39, L47, L51, L263, L263, L272, L286, L289, L301, L301, L681, L683, L691, L840, L933, L1063, L1684, L1846, L1850, L1867, L1906, L1907, L1918, L1933, L1989, L2017, L2153, L2177, L2181, L2211, L2211, L2299, L2307, L2402, L2466, L2618, L2619, L2631, L2632, L2701, L2831, L2990, L3239, L3361, L3921, L4029, L4031, L4045, L4052, L4059, L4109, L4298, L4299, L4350, L4351, L4804, L4806, L4809, L4822, L4826, L4826, L4971, L5286, L5699, L5720, L5724, L5787, L5816, L5820, L5822, L5845, L5895, L5909

## A5. setTimeout / setInterval / MutationObserver

- **setInterval**: L96, L339, L525, L952
- **MutationObserver**: L1076, L1085, L3019, L3019, L3784, L3789, L3958, L4132, L4301, L5041, L5683, L5765
- **setTimeout**: L42, L43, L95, L263, L302, L378, L505, L625, L675, L837, L911, L1104, L1118, L1744, L1801, L1827, L1842, L1846, L1924, L1925, L1958, L2260, L2406, L4135, L4135, L4497, L4666, L4666, L4946, L5033, L5043, L5043

## A6. innerHTML (ตรวจว่ามีข้อมูลจากผู้ใช้/ข้อมูลภายนอกไหลเข้าไหม)

L361, L375, L417, L439, L440, L441, L512, L596, L619, L700, L709, L756, L824, L853, L877, L879, L881, L891, L892, L1035, L1044, L1051, L1211, L1288, L1306, L1879, L1892, L1931, L1997, L1999, L2155, L2162, L2164, L2175, L2276, L2283, L2296, L2312, L2331, L2409, L2638, L2652, L2654, L2656, L2658, L2662, L2664, L2665, L2961, L3540, L3551, L3692, L3715, L3737, L3758, L4126, L4247, L4255, L4262, L4814, L4823, L4826, L4828, L4837, L4839, L4841, L5758, L5860, L5862

## A7. inline event handler ในเทมเพลต (บล็อก CSP เข้ม)

app.js: onclick×244, oninput×4, onchange×4, onkeydown×3, onsubmit×1

ฟังก์ชันที่ถูกเรียกจาก inline handler มากสุด: `studioNav`×22, `VLT_startCategory`×5, `studioStartFlashcards`×5, `studioCloseModal`×5, `TGAT1ReadingPlus.open`×5, `mt`×4, `VLT_startMock`×4, `VLT_startReview`×4, `studioWordDetail`×4, `studioFlashFlip`×4, `studioReviewResult`×4, `V15_grade`×4, `V17_jump`×4, `VLT_home`×3, `TGAT1VocabularyLab.start`×3, `if`×3, `studioGameLevel`×3, `studioOpenErrors`×3, `renderGrammarBack`×3, `renderReadingBack`×3, `TGAT1PhrasePlus.openBank`×3, `ans`×2, `bdu`×2, `bd`×2, `bdc`×2, `bdh`×2, `home`×2, `startStage`×2, `dq`×2, `VLT_toggleFavorite`×2, `studioStartPhrasePractice`×2, `studioVSearch`×2, `studioVTab`×2, `studioVPage`×2, `studioMarkWord`×2, `studioFlashMark`×2, `VLT_startDaily`×2, `start`×2, `V15_startRecall`×2, `studioRunVocabGame`×2

index.html: onclick×20

inline <script> ใน index.html: 984 ตัวอักษร (ต้องย้ายเข้า app.js ก่อนทำ CSP เข้ม)

## A8. global บน window (ชื่อ)

ED_STORAGE_FALLBACK, STG_answer, STG_getCurrentQuestion, STG_next, STG_review, STG_start, STG_toggleWrongQueue, STR_answer, STR_getCurrentQuestion, STR_next, STR_renderQ, STR_review, STR_start, STR_toggleWrongQueue, STUDIO_CONTENT_GATE_4064, STUDIO_DATA, STUDIO_ERROR_NOTEBOOK, STUDIO_EXAM_CATEGORY_KEY, STUDIO_FUNCTIONAL_QA, STUDIO_GAME_RETURN, STUDIO_GAME_SOUND, STUDIO_HISTORICAL_QUESTION, STUDIO_IS_RECENT_QUESTION, STUDIO_ORDER_DIVERSE_QUESTIONS, STUDIO_PICTURE_BANK, STUDIO_POLYSEMY, STUDIO_QUALITY_4064, STUDIO_RECORD_ERROR, STUDIO_REMEMBER_QUESTION, STUDIO_SELECT_DIVERSE_QUESTIONS, STUDIO_SNAPSHOT_MISSED, TGAT1Accessibility, TGAT1Adaptive, TGAT1AdaptiveCore, TGAT1BackupImportGuard, TGAT1CompleteLearning, TGAT1ContentQuality, TGAT1DataGuards, TGAT1DecorateSecondary, TGAT1DeepQuality, TGAT1ExamDraftGuard, TGAT1LazySenses, TGAT1LazyVault, TGAT1LearningCoach, TGAT1LearningExplain, TGAT1LearningStateGuard, TGAT1MatchGuard, TGAT1PhrasePlus, TGAT1ProductionHardening, TGAT1QuestionExplanations, TGAT1QuestionGuidance, TGAT1ReadingPlus, TGAT1RuntimeHealth, TGAT1Safety, TGAT1Stable, TGAT1V12Evidence, TGAT1V19, TGAT1V20, TGAT1_CONTENT_AUDIT_V408, TGAT1_DEEP_AUDIT, TGAT1_FUNCTIONAL_AUDIT, TGAT1_LANGUAGE_PRACTICE, TGAT1_MIPAD6_RUNTIME, TGAT1_SEMANTIC_CONTENT_AUDIT, TGAT1_V382_CONTENT_AUDIT, TGAT1_V40_CONTENT_AUDIT, TGAT1_VERSION, TGAT1_addAnalyticsHook, TGAT1_addGameHook, TGAT1_addHomeHook, TGAT1_addSettingsHook, TGAT1_addVocabularyHook, TGAT1_addVocabularyPreHook, V14_exportAudit, V14_filterMissed, V14_flagQuestion, V14_startCategoryReview, V14_unflagQuestion, V15_checkRecall, V15_exit, V15_grade, V15_render, V15_startDue, V15_startDueRecall, V15_startNew, V15_startRecall, V16_startTask, V16_toggleTask, V17_closeChecklist, V17_discardDraft, V17_jump, V17_openChecklist, V17_resumeDraft, V17_toggleFlag, VLT_ORIGINAL_HOME, VLT_RUN, VLT_STATE, VLT_answer, VLT_begin, VLT_dailyPool, VLT_ensureBank, VLT_escape, VLT_exit, VLT_explainPanel, VLT_finish, VLT_hintText, VLT_learningExplanation, VLT_mixPool, VLT_record, VLT_renderQuiz, VLT_renderResult, VLT_retry, VLT_retryWrong, VLT_shuffle, VLT_startCategory, VLT_startDaily, VLT_startFavorites, VLT_startQuick, VLT_startRandomMock, VLT_startReview, VLT_startSprint, VLT_toast, VLT_toggleFlagV12, __TGAT1ApplyPendingSenseRepairs, __TGAT1_ANALYTICS_BASE__, __TGAT1_ANALYTICS_HOOKS__, __TGAT1_GAME_BASE__, __TGAT1_GAME_HOOKS__, __TGAT1_HOME_BASE__, __TGAT1_HOME_HOOKS__, __TGAT1_LIGHT_STRONG_V8__, __TGAT1_PAGE_VISUAL_V330__, __TGAT1_PERSONAL_MOTION_V7__, __TGAT1_PERSONAL_V9__, __TGAT1_SETTINGS_BASE__, __TGAT1_SETTINGS_HOOKS__, __TGAT1_STABILITY_V13__, __TGAT1_STORAGE_ESTIMATE, __TGAT1_V16_DASHBOARD__, __TGAT1_V17_EXAM__, __TGAT1_V19_LAST_TIMING__, __TGAT1_V19__, __TGAT1_V20_AUDIT__, __TGAT1_V35_NAV_ANNOUNCER__, __TGAT1_V382_INIT__, __TGAT1_VOCAB_BASE__, __TGAT1_VOCAB_HOOKS__, __TGAT1_VOCAB_PRE_HOOKS__, __TGAT_UNIFIED_AUDIO_V40, __readingPassages, __tg362Resize, __v8NavWrapped, ans, mkPic, mt, play, recordWord, renderGrammarBack, renderReadingBack, studioAnalytics, studioEsc, studioExam, studioExportAll, studioHome, studioImportAll, studioNav, studioPersistSession, studioProfile, studioStartFlashcards, studioStartSentenceGame, studioStartVocabTranslation, studioToast, studioUpdateChrome, studioV9Grammar, studioV9SetTarget, studioVocabTranslationLevel, studioVocabulary, toast

## A9. localStorage keys

tgat1-content-expanded, tgat1-english-studio-backup-v3.json, tgat1-english-studio-backup.json, tgat1-studio-v43.0.0, tgat1-v20-evidence, tgat19-actions, tgat19-btn, tgat19-card, tgat19-dialog, tgat19-dialog-head, tgat19-filter, tgat19-formgrid, tgat19-grid, tgat19-head, tgat19-input, tgat19-kpi, tgat19-muted, tgat19-note, tgat19-overlay, tgat19-qrow, tgat19-quality-center, tgat19-queue-count, tgat19-queue-list, tgat19-review-overlay, tgat19-review-title, tgat19-row, tgat19-search, tgat19-select, tgat19-status, tgat19-timing-card, tgat19-timing-grid, tgat19-wrap, tgat19StorageControls, tgat19backupResults, tgat19persist-status, tgat1_, tgat1_english_studio_v1, tgat1_learning_hub_v1, tgat1_personal_study_days_v1, tgat1_personal_target_score_v1, tgat1_production_health_v1, tgat1_studio_active_session_v1, tgat1_studio_content_quality_v1, tgat1_studio_content_review_v1, tgat1_studio_error_notebook_v1, tgat1_studio_error_notebook_v2, tgat1_studio_everyday_phrase_v382, tgat1_studio_grammar_clinic_v1, tgat1_studio_health_v1, tgat1_studio_learning_activity_v1, tgat1_studio_learning_coach_v1, tgat1_studio_reading_plus_v382, tgat1_studio_reading_trainer_v1, tgat1_studio_recent_practice_v1, tgat1_studio_recent_sentence_practice_v1, tgat1_studio_recovery_v1, tgat1_studio_runtime_errors_v1, tgat1_studio_smart_review_v1, tgat1_studio_vocab_progress_v1, tgat1_v14_question_flags, tgat1_v16_study_plan_v1, tgat1_v17_exam_draft_v1, tgat1_v19_exam_timing_history_v1, tgat1_v19_exam_timing_live_v1, tgat1_v19_manual_question_review_v1, tgat1_vlt_active_run_v1

## A10. CSS

- `!important` 2298 จุด · `@media` 123 บล็อก · ขนาด 265 KB
- section L8: app.css
- section L16: 09-visual-redesign.css
- section L18: 10-learning-modules.css
- section L20: 22-language-practice.css
- section L89: 25-learning-system-v36.css
- section L105: 26-deep-quality-v36-1.css
- section L119: 27-production-hardening-v36-2.css
- section L121: 28-complete-learning-hardening-v36-3.css
- section L123: 31-premium-design-v38.css
- section L409: 32-premium-tablet-v38-1.css
- section L588: 33-content-expansion-v38-2.css
- section L684: 34-quality-polish-v38-3.css
- section L734: 36-mipad6-optimized.css
- section L867: 44-mipad6-landscape-v40-4.css
- section L963: 41-unified-audio-v40.css
- section L970: v40.7.1 — ธีมพรีเมียมกลาง: เทาอ่อน · สีเดียว · การ์ดเรียบ · แอนิเมชันเบา
- section L1025: v40.7.2 — แก้กล่องซ้อนใน hero และจัดสีให้สะอาด
- section L1037: v40.7.3 — กล่อง hero/mission ของ Game และ Daily Mission
- section L1053: v40.7.2 — แก้หัวข้อสีม่วงและกล่องตกแต่งซ้อนใน hero
- section L1058: v40.7.4 — โหมดประหยัดเครื่อง (อัตโนมัติเมื่อ RAM ≤4GB หรือ CPU ≤4 แกน)
- section L1063: v40.7.6 — หน้าสอบใหม่ (โครงสร้างและสีใช้ token)
- section L1087: v40.7.7 — หน้าแรก: เรียบขึ้น ตัดภาพซ้อนและวงโคจร + ลูกเล่นทำครั้งเดียว
- section L1107: v40.7.8 — หน้าศัพท์: ค้นหา แท็บ การ์ดคำ และการแบ่งหน้า
- section L1127: v40.7.9 — ป้ายสรุปใน hero ของทุกโมดูล และปุ่มที่ไม่พร้อมใช้งาน
- section L1135: v40.7.10 — แก้ความคมชัดหัวข้อใน hero, ป้ายหัว, ช่องกรอก
- section L1146: v40.7.11 — ป๊อปอัปยืนยันในแอป: ปุ่มอ่านง่าย
- section L1151: v40.7.12 — หน้าสรุปผลกลาง (TG_summary) ใช้ร่วมกันทุกเกมและโหมดฝึก
- section L1164: v40.7.12 — หน้าอ่าน: โครงใหม่ (หัวหน้า · สถิติ · Blueprint · กริดบทอ่าน · เช็กลิสต์)
- section L1197: v40.7.12 — หน้าวิเคราะห์: การ์ดสถิติเป็นกริด 2 คอลัมน์บนมือถือ
- section L1205: v40.7.16 — หน้าโปรไฟล์และหน้าตั้งค่า: โครงใหม่เป็นส่วนๆ
- section L1251: v40.7.16 — Game Center: กริดโหมดเกมกระชับ และซ่อนปุ่มเสียงที่หลุดแถว
- section L1259: v40.7.17 — Mi Pad 6 แนวนอน (~1280×800): เมนูข้างจอ มีระยะขอบ และกริด 3–4 คอลัมน์
- section L1545: v42.0.2 dark-mode contrast fixes

selector ที่นิยามซ้ำมากสุด 40 อันดับ: `body`×18, `.studio-content`×18, `.studio-sidebar`×15, `.dash-hero`×15, `.studio-topbar`×14, `.dash-hero h1`×14, `.studio-mobile-nav`×13, `.dash-hero-visual`×13, `.studio-mobile-nav button`×12, `:root`×10, `.studio-mobile-nav button span`×10, `.dash-gauge`×10, `.top-metric`×9, `.studio-footer`×9, `.dash-hero-foot`×9, `.dash-gauge-inner strong`×9, `.st-section-head`×8, `to`×8, `.dash-kpi-grid`×8, `.dash-quick-grid`×8, `.st-title`×7, `100%`×7, `.avatar-button`×7, `.topbar-title`×7, `.dash-hero-copy>p`×7, `.dash-orbit-one`×7, `.dash-orbit-two`×7, `.dash-kpi`×7, `.dash-quick-card`×7, `:focus-visible`×6, `.st-card`×6, `.studio-main`×6, `.st-word-grid`×6, `.dash-float-card`×6, `.module-hero-art`×6, `html`×5, `#app`×5, `.brand-mark`×5, `.vault-view`×5, `.st-hero`×5

## A11. sw.js
```js
/* TGAT1 English Studio v43.0.0 offline service worker. */
'use strict';
const CACHE_NAME = 'tgat1-studio-v43.0.0';
const APP_SHELL = [
  './', './index.html', './app.css', './app.js', './data.js',
  './learning-hub.css', './learning-hub.js', './learning-hub-curriculum.js',
  './manifest.webmanifest', './icon-192.png', './icon-512.png',
  './icon-maskable-192.png', './icon-maskable-512.png', './apple-touch-icon.png'
];
const LAZY_CHUNKS = ['./data-vault.js', './data-senses.js'];
const cleanUrl = url => { const u=new URL(url,self.location.href);u.search='';u.hash='';return u.href; };
const isAppEntry = url => { const scope=new URL(self.registration.scope);return url.pathname===scope.pathname||url.pathname===scope.pathname+'index.html'; };
function fresh(url){return new Request(url,{cache:'reload'});}
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL.map(fresh)).then(()=>Promise.allSettled(LAZY_CHUNKS.map(url=>fetch(fresh(url)).then(r=>r&&r.ok?cache.put(url,r):undefined)))))));
self.addEventListener('message',event=>{if(event.data&&event.data.type==='SKIP_WAITING')self.skipWaiting();});
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('tgat1-studio-')&&k!==CACHE_NAME).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
  const req=event.request,url=new URL(req.url);
  if(req.method!=='GET'||url.origin!==self.location.origin)return;
  if(req.mode==='navigate'){
    event.respondWith(fetch(req).then(response=>{if(response&&response.ok&&isAppEntry(url)){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put('./index.html',copy));}return response;}).catch(()=>caches.match('./i
```

## A12. ตัวเลขที่ฝังในเทสต์ (เพี้ยนเมื่อแก้เนื้อหาเยอะ)

- tests/regression_r3_content.py:12: `check('bank: 1,200 items, 4 unique options, valid key',len(V)==1200 and all(len(set(q['options']))==4 and 0<=q['answer']<4 for q in V))`
- tests/regression_r3_content.py:51: `check('RC: test-wise heuristic (drop topic name, pick longest) ≤35% (v42.0.1: 81.3%)',s1/300<=0.35,f'{s1/300:.3f}')`
- tests/regression_r3_content.py:76: `check('vocab: no headword deleted in round 3 (3,508 studio words)',len(D['studio']['words'])==3508,len(D['studio']['words']))`
- tests/regression_r3_content.py:93: `check('RC: max-context-overlap heuristic <=35% (v43 Arena: 51.7%)',_hit/300<=0.35,f'{_hit/300:.3f}')`
- tests/regression_r3_content.py:96: `check('TC: key is the longest option <=35% (v43 Arena: 42%)',_tcl/300<=0.35,f'{_tcl/300:.3f}')`
- tests/regression_r3_ui.py:5: `def check(n,c,d=''): R.append((n,bool(c)));print(('PASS ' if c else 'FAIL ')+n+('' if c else f'  [{str(d)[:300]}]'))`
- tests/regression_v42.py:60: `check('content: 3,508 unique headwords and 3,400 lazy sense sets preserved', len(W) == 3508 and len({w['w'] for w in W}) == 3508 and len(sen`
- tests/regression_v42.py:61: `check('content: 535 phrases preserved', len(data['studio']['phrases']) == 535, str(len(data['studio']['phrases'])))`
- tests/regression_v42.py:91: `check('Round 2: all 436 researchers translations name researcher(s), not team', len(researchers)==436 and not bad_research, f'{len(researche`
- tests/regression_v42.py:151: `check('bank: 1,200 unique questions, 4 distinct non-empty options, valid answer', bank['n'] == 1200 and bank['unique'] == 1200 and bank['bad`
- tests/regression_v42.py:155: `check('bank: RC passages 100–200 words', 100 <= bank['rcMin'] and bank['rcMax'] <= 200, str(bank))`
- tests/regression_v42.py:242: `check('mock: a complete 60-question mock finishes and scores 100/100 on the /100 scale', res['score'] == 100 and res['total'] == 100 and res`
- tests/smoke_test.py:95: `check(f'page {name} @{width}px renders', n > 200 and over <= 2, f'text={n} overflow={over}')`
- tests/smoke_test.py:216: `check('offline: exam question bank loads from cache', bank == 1200, f'bank={bank}')`
