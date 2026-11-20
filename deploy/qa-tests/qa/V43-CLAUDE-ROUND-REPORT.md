# V43 — รายงานรอบของ Claude (ต่อจาก Arena 16:13) · ส่งต่อให้ Arena / ผู้รับงานถัดไป

> เขียนโดย Claude · 2026-11-19 17:26 (เวลาไทย) · ตัวเลขทุกตัว **วัดจริง** จาก `sh tools/rebuild_all.sh` + เทสต์เต็มชุด (run สุดท้าย 17:21)
> อ่านคู่กับ `qa/V43-NEXT-WORK.md` (ใบสั่งงานของ Arena — เลขงาน 1–15 ในไฟล์นี้อ้างตามไฟล์นั้น) และ log ท้าย `HANDOFF.md`
> baseline ก่อนเริ่ม: rebuild + เทสต์ได้ตัวเลขตรงกับของ Arena ทุกตัว (49/49 · 60/60 · 27/27 · 7/7 · 94/94 · a11y `errors: []` · overlap 0.517 · tc 0.420 · short 0.670)

## 0. วิธีอ่านไฟล์ชุดนี้

- ชุดใหม่ใน Drive ชื่อ `WORKING-v43-part*.zip` + `MANIFEST-v43.json` (written_at 2026-11-19T17:2x+07:00, written_by Claude) — **แทนชุด Arena 16:13** (ชุด Arena ถูกย้ายไปถังขยะหลังอัปของใหม่และตรวจแล้ว ยังกู้คืนได้จาก Trash ของ Drive)
- `.git` อยู่ใน zip ไม่ได้ (sync_pack ข้าม) → ประวัติ commit ของรอบนี้: `7ae0098` import Arena 16:13 → `9cb5088` งานเนื้อหาทั้งหมด + gate + bump 43.0.0 → commit สุดท้าย = แก้ S17-Q049 + เอกสาร + ZIP deploy
- ไฟล์ deploy แยกใน Drive: `TGAT1-English-Studio-v43.0.0.zip` (เฉพาะ `web/`) + `TGAT1-English-Studio-v43.0.0-QA-and-tests.zip` + `.sha256` ของทั้งคู่

## 1. แก้แล้ว (ก่อน → หลัง)

| งาน (เลขตาม V43-NEXT-WORK) | ไฟล์ | ก่อน → หลัง |
|---|---|---|
| **1** RC words-in-context | `content/rc_v43_[a-k].json` (39 ข้อแปลงประเภท, จับคู่ passage↔ประเภทด้วย bipartite matching ให้ทุก passage ยังมี type ไม่ซ้ำ) | wic **21 → 60** · detail 120 คงเดิม · true 25→15 · attitude 25→15 · paraphrase/reference/inference/purpose → 18 · main 18 (ตรงตารางเป้าของ Arena ทุกตัว) |
| **2** RC max-context-overlap | key 64 ข้อถอดความ (ไม่ลอกคำจากบท) + ตัดความยาว key ไม่ให้ยาวสุด | overlap **0.517 → 0.270** · combined **0.537 → 0.270** · G-B count metric **→ 0.263** · bias rc unique-top-overlap 0.413 → 0.183 · key-longest 0.200 → 0.147 · second-longest 0.44 → ≤0.40 |
| **3** TC answer_longest | `content/tc_v43_[a-j].json` 38 ตัวลวงยืด + เขียนคำอธิบายไทยใหม่ 22 ข้อ | **0.420 → 0.293** |
| **4** Short conv overlap | สร้าง pipeline ใหม่ `content/short_v43_[ab].json` + `tools/apply_short_v43.py` (tag `SHORT-rewrite` → G30) · blank (1)/(3) ทั้ง 120 ข้อ เปลี่ยนตัวลวงสำเร็จรูป 1 ตัวเป็นตัวหลอกที่ใช้คำจากบทสนทนา | unique-top-overlap **0.670 → 0.285** · G-D count **0.695 → ≤0.30** |
| **5** C4 genre + near-dup | `tools/apply_rc_v43.py` รองรับ `context`/`topic` ในสเปกแล้ว (assert 100–200 คำ) · `tools/check_rc_v43.py` ใช้ context จากสเปกถ้ามี · บทใหม่ 4 บท: ข่าว (`S20-Q051`), ประกาศรับสมัครงาน (`S16-Q046`), อีเมล (`S14-Q046`), บทความ live-stream (`S13-Q046`) | near-dup max **0.309 → <0.25** · genre RC 1 → 5 |
| **6** Q-R idiom | pipeline ใหม่ `content/qr_idiom_v43_[ab].json` + `tools/apply_qr_idiom.py` (tag `QR-idiom` → G31) · แทน 60 ข้อที่ใช้ตัวลวงสำเร็จรูปซ้ำมากที่สุด (3 ข้อ/ชุด) | idiom **~3–5 → 60** · qr answer_longest 0.285 → 0.275 · ตำแหน่งคำตอบ 50/50/50/50 คงเดิม |
| **7** extreme-word | RC 45 ตัวลวง + LC 93 ตัวลวง (ลด all/every/only/never แบบเปลี่ยนความหมายจริง ไม่ใช่แค่สลับเป็น each) | answer vs distractor (รายการคำของงาน 7): rc 0.047/0.058 · long 0.11/0.13 · short 0.13/0.09 · qr 0.08/0.055 → **ทุก kind อยู่ใน 1.5 เท่า** (TC ไม่นับ: 0 vs 3 ตัวลวงที่เป็นคำเดี่ยว) |
| **8** C9 AI review | `qa/AI-REVIEW-v43-Claude.md` + `qa/AI-REVIEW-v43-short-duplicates.txt` | รายงานเท่านั้น (แก้ 1 จุด `S17-Q049` เพราะตัวลวงเกือบจริง) |
| **13** T6/T7/T8 | gate ใหม่ 11 ตัว · bump **43.0.0** (`web/app.js`, `index.html`, `sw.js` cache `tgat1-studio-v43.0.0`, `manifest.webmanifest`, `tools/rebuild_all.sh`, `tests/regression_v42.py` EXPECT_VERSION) · `web/CHANGELOG-v43.0.0.md` · ZIP deploy + ZIP QA + SHA-256 | ZIP deploy ไม่มี qa/backups/tools/tests/content (ตรวจด้วย `unzip -l`) · ZIP QA มี `qa/R3-BLUEPRINT-ALIGNMENT.md` |
| **15** S1–S5 | `qa/RESEARCH-S1-S5.md` | blueprint ยังเดิม · TGAT สอบ 30 ม.ค.–1 ก.พ. 2570 · สถิติประเภทข้อ 2567/2568 จากแหล่งที่ 2 |

**gate ใหม่ใน `tests/regression_r3_content.py`** (27 → 38 checks): G-A type mix (3 checks) · G-B RC overlap · G-C TC longest · G-D short overlap · G-E Q-R idiom ≥60 + ตำแหน่ง 50/50/50/50 · G-F extreme-word 1.5× · G-G RC near-dup ≤0.25 + genre ≥5

## 2. automated ผ่าน (run 17:21)

- `rebuild_all.sh` rc=0 · `check_rc_v43.py` ALL CLEAN (type mix: detail 120, wic 60, main/reference/paraphrase/purpose/inference 18, true/attitude 15) · `check_quotes.py data/vault.json long rc` 565 quotes, not found 0
- regression_r3_content **38/38** · smoke **49/49** (bankAudit structuralCue = 0 หลังแก้ 7 ข้อ idiom ที่ key เป็น “!”/“?” ตัวเดียว) · regression_v42 **60/60** (รวม versions all 43.0.0 + axe) · regression_r3_ui **7/7** · smoke_r3_extra **94/94** · a11y `errors: []`
- `bias_metrics`: answer_longest rc 0.147 · long 0.275 · short 0.000 · tc 0.293 · qr 0.275 — context-overlap rc 0.183 · long 0.160 · short 0.285 · tc 0.027 · qr 0.000
- `rc_heuristics`: longest 0.147 · no-extreme+longest 0.193 · max-context-overlap 0.270 · combined 0.270
- ตั้งเครื่องรอบนี้: chromium อยู่ที่ `/opt/pw-browsers/chromium-1243/chrome-linux64/chrome` (ไม่ต้อง `playwright install`) · `check_quotes.py` ต้องส่ง args `data/vault.json long rc`

## 3. ต้องให้มนุษย์ตรวจ

- ทุกข้อที่ Claude เขียน/แก้ (รายการละเอียดใน `qa/AI-REVIEW-v43-Claude.md` หัวข้อ 3): wic ใหม่ 43 · key ถอดความ 64 · บทอ่านใหม่ 4 บท/20 ข้อ · ตัวลวง RC/LC ที่ตัดคำ absolute 138 · TC 38 · Short 120 (สร้างจากแม่แบบ 8 แบบ) · Q-R idiom 60
- ตัวลวง RC 25 ตัวที่สคริปต์ชี้ว่า “ทำจากคำในบทเกือบหมด” (หัวข้อ 2 ของรายงาน review) — ส่วนใหญ่ตั้งใจให้ “จริงในบทแต่ไม่ตอบคำถาม” แต่ต้องยืนยัน
- เหมือนเดิมจาก Arena: Q1–Q3 (screen reader, iOS/Android/PWA, gzip/brotli), T5 Lighthouse, IPA 83 คำ — **AI ไม่ได้ทำและไม่อ้างว่าผ่าน**

## 4. ยังค้าง (เหตุผลตรง ๆ)

| งาน | สถานะ | เหตุผล |
|---|---|---|
| Short conv: สถานการณ์ซ้ำ | **ค้าง — ใหญ่กว่าที่ Arena บันทึก** | พบว่า 60 บทมาจาก 20 สถานการณ์ × 3 (เปลี่ยนแค่ชื่อคน) ต้องเขียนบทใหม่ 40 บท ไม่ใช่ 30 · รอบนี้แก้แค่ตัวลวงเพื่อลด overlap |
| Short conv blank (2)/(4) + คำอธิบายเดิม | ค้าง | ตัวลวงสำเร็จรูปยังอยู่ใน blank (2)/(4) · คำอธิบายไทยของ 120 ข้อที่แก้ อาจยังเอ่ยถึงตัวลวงเก่า |
| Q-R 86 ข้อที่เหลือ | ค้าง | ยังใช้ตัวลวงสำเร็จรูปซ้ำ (27 ประโยค ซ้ำ 12–19 ครั้ง) |
| C4 ส่วนที่เหลือ | ค้างบางส่วน | ทำ 4 บทจากเป้า ~30 บท · TC ไม่ต้องทำเพิ่มเพราะ TC ของ Arena มี genre 36 แบบอยู่แล้ว |
| สัญญาณใหม่ที่ Claude สร้าง | ต้องแก้รอบหน้า | ตัวลวง wh-ever 15 จุด และ passive `to be/being V3` 13 จุดใน TC ไม่เคยเป็นคำตอบ (ดูรายงาน review) |
| 9–12 คลังศัพท์ V2–V6 (REVIEW-QUEUE 1,505) | **ไม่ได้ทำ** | งานตัดสินเชิงภาษาจำนวนมาก (772 ตัวอย่างต้องเขียนใหม่ + headword 146 ต้องตัดสินก่อน) — เลือกใช้เวลากับข้อสอบที่วัดผลได้ก่อน |
| 13 T1–T4 (refactor app.js, CSP, lazy data.js, lazy hub) | ไม่ได้ทำ | เสี่ยงทำ UI พังโดยไม่มีอุปกรณ์จริงทดสอบ ควรทำเป็นรอบแยก |
| 14 Q1–Q3, T5 | ไม่ได้ทำ (ห้าม AI อ้าง) | ต้องคน/อุปกรณ์จริง |

## 5. ลำดับที่แนะนำสำหรับรอบถัดไป

1. มนุษย์ spot-check ตามหัวข้อ 3 (เริ่มจาก Q-R idiom 60 และบทอ่านใหม่ 4 บท)
2. Short conversation: เขียนสถานการณ์ใหม่ 40 บทแทนบทที่ซ้ำ (ใช้ pipeline `apply_short_v43.py` ขยายให้รับ context ใหม่ได้แบบเดียวกับ RC)
3. Q-R: เขียนตัวลวงเฉพาะข้อให้ 86 ข้อที่เหลือ (ขยาย `apply_qr_idiom.py` หรือทำ `apply_qr_v43.py`)
4. RC: เพิ่ม main/purpose ให้ใกล้ปี 2568 (4/15) โดยลด true/attitude (ดู `qa/RESEARCH-S1-S5.md` S3)
5. คลังศัพท์ V2–V6 → T1–T4 → Q1–Q3
