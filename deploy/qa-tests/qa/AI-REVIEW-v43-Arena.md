# AI-REVIEW v43 — Arena (รอบตรวจงาน Claude 17:28)

> ผู้ตรวจ: Arena AI · 2026-11-19 18:3x (เวลาไทย) · ตรวจแบบ **report-only ไม่แก้ไฟล์ข้อสอบ** (ตามกติกา C9)
> ต้นทาง: pack `WORKING-v43-part1..3.zip` written_at 2026-11-19T17:28+07:00 (sha ตรง MANIFEST ทั้ง 3 part)
> วิธีตรวจ: diff ทั้งต้นไม้เทียบกับ pack ของ Arena 16:13 + รันเทสต์จริง + รันสคริปต์วัดสัญญาณเดา + สคริปต์หาความซ้ำของเนื้อหา (`/tmp/spot.py` ในบันทึกส่งต่อ)

---

## 1. ผลการทวนคำอ้างของ Claude (run 17:21) — **จริงตามที่รายงาน**

| คำอ้าง | Arena ทวนแล้วได้ | สรุป |
|---|---|---|
| sha256 ตรง MANIFEST 3 part | part1 `cb499e4a…`, part2 `78e2ffbf…`, part3 `ec7ae7e7…` ตรงทั้ง 3 | ✅ |
| deploy zip sha ตรง `.sha256` | `404bbb2a…` และ `e76c6f9a…` ตรง | ✅ |
| `check_rc_v43.py` ALL CLEAN, type mix wic 60 | `11 files, 300 items` · detail 120, **wic 60**, main/reference/paraphrase/purpose/inference 18, true/attitude 15 · ALL CLEAN | ✅ |
| `check_quotes.py data/vault.json long rc` 565/0 | `quotes checked 565 not found 0` | ✅ |
| regression_r3_content **38/38** | **38/38 passed** (รันจริงบนเครื่อง Arena) | ✅ |
| smoke **49/49** | **49/49 checks passed** | ✅ |
| regression_v42 **60/60** รวม version 43.0.0 + axe | **60/60 checks passed** · `PASS a11y (axe-core): no critical/serious violations` | ✅ |
| bias_metrics: rc longest .147 / overlap .183 · tc longest .293 · short overlap .285 | ตรงทุกตัว | ✅ |
| rc_heuristics: max-context-overlap .270 · combined .270 | ตรงทุกตัว | ✅ |
| deploy zip ไม่มี qa/tools/tests/content/backups | 20 entries = ไฟล์ใน `web/` ครบทั้ง 20 (รวม learning-hub 3 ไฟล์) ไม่มีอะไรต้องห้ามปน | ✅ |
| version bump 43.0.0 | `sw.js` cache `tgat1-studio-v43.0.0` · `manifest.webmanifest` v43.0.0 · `data.js` header 43.0.0 · `tests/regression_v42.py:18 EXPECT_VERSION='43.0.0'` · `rebuild_all.sh` → `datafiles.js build data web 43.0.0` · `42.x` ที่เหลือเป็น comment ประวัติเท่านั้น | ✅ |
| เนื้อหาใหม่ที่เขียนไม่มีอักษรแปลกปน | char-scan `content/*.json` + `data/vault.json` → เจอแค่ `é` 19 จุด (café/résumé) ไม่มี CJK/เกาหลี/เวียดนาม | ✅ |

**ผลเทสต์ที่เหลือ (Arena รันต่อ):** regression_r3_ui / smoke_r3_extra / a11y_audit — ดูผลในบันทึกส่งต่อท้าย `HANDOFF.md`

### หมายเหตุเรื่องเครื่อง (สำคัญสำหรับผู้รับงานต่อ)
- sandbox ของ Arena **ไม่มี** `/opt/pw-browsers/chromium-1243` ที่ Claude ระบุ → ต้อง `python3 -m playwright install chromium` (ได้ `chromium-1255`) **และต้องรัน `python3 -m playwright install-deps chromium` ด้วย** เพราะรอบนี้ chrome พังด้วย `libnspr4.so: cannot open shared object file` ทำให้ suite ที่เป็น browser ตายยกชุด (เนื้อหา/content suite ยังรันได้เพราะไม่ใช้ browser)
- `tools/check_rc_v43.py` ไม่ต้องพึ่ง `/tmp` แล้ว (Arena แก้ไว้รอบ 16:13) — มันจะแจ้ง `INFO /tmp/rc_passages.json missing - rebuilt 60 passage contexts from data/vault.json` และ `WARN no typeplan` ซึ่ง **ไม่ใช่ error**

---

## 2. ปัญหาที่ Arena เจอเพิ่ม (ยังไม่มีใครบันทึก) — เรียงตามความรุนแรง

### 🔴 A1. ตัวลวง Q-R ถูกรีไซเคิลหนักมาก: 230 ช่องใน 101 ข้อ
Claude บันทึกไว้ว่า "Q-R 86 ข้อที่เหลือยังใช้ตัวลวงสำเร็จรูปซ้ำ (27 ประโยค ซ้ำ 12–19 ครั้ง)" — **ตัวเลขจริงแย่กว่านั้น**

วัดจาก `data/vault.json` (นับประโยคตัวลวงที่ใช้ซ้ำ ≥ 4 ครั้ง):
- ประโยคตัวลวงที่ซ้ำ: **17 ประโยค**
- ช่องที่ต้องเขียนใหม่: **230 ช่อง** ครอบคลุม **101 ข้อ** (ไม่ใช่ 86)

| ประโยคตัวลวง | ใช้ซ้ำ |
|---|---|
| `For about two hours.` | 17 |
| `Three times a week.` | 17 |
| `Every Monday.` | 17 |
| `Near the main entrance.` | 17 |
| `At the far end of the hall.` | 17 |
| `I did it three days ago.` | 17 |
| `Since last Tuesday.` | 16 |
| `No, it was at noon.` | 15 |
| `It is on the third floor.` | 14 |
| `I heard about that problem yesterday.` | 14 |
| `I asked someone about it yesterday.` | 13 |
| `I thought about it at eight o’clock.` | 12 |

**ความเสี่ยง:** ผู้สอบที่เห็นข้อ 3–4 ข้อติดกันจะรู้ว่าประโยคพวกนี้คือตัวลวงเสมอ → ตัดทิ้งได้โดยไม่ต้องอ่านคำถาม (เป็น pattern ที่เรียนรู้ได้เร็วกว่าสัญญาณความยาว/overlap ที่แก้ไปแล้ว)

### 🔴 A2. Short Conversation: บทสนทนา 60 บท = ~20 สถานการณ์ × 3 (เปลี่ยนแค่ชื่อคน)
Claude บันทึกไว้แล้ว แต่ Arena วัดยืนยันเป็นตัวเลข:
- context ไม่ซ้ำ: **60 บท** สำหรับ 200 ข้อ
- คู่บทที่มี word-overlap (Jaccard) > 0.5: **60 คู่** · คู่ที่คล้ายสุด **0.94**
- ตัวอย่าง: `Tom: Hi, Mint. We need to set clear deadlines for…` ↔ `Ken: Hi, Tara. We need to set clear deadlines for…` ↔ `Maya: Hi, June. We need to set clear deadlines for…` (เหมือนกันทุกคำ ยกเว้นชื่อ)
- แม่แบบประโยคเปิดบท (4 คำแรก) ซ้ำ: 8 กลุ่ม กลุ่มละ 6 บท

**ความเสี่ยง:** ผู้สอบอ่านบทแรกจบจะเดาบทที่เหลือได้อีก 2 บท · และคำอธิบาย/ตัวลวงที่อิงเนื้อเรื่องจะใช้ได้กับทั้ง 3 บท

### 🟠 A3. คำอธิบาย 150 ข้อ (ใน 600 ข้อ TC+RC) ไม่ได้เอ่ยถึงตัวลวงเลย
วัดโดย: ใน `explanation` ไม่มีคำศัพท์ (≥4 ตัวอักษร) จากตัวลวงทั้ง 3 ตัวปรากฏอยู่
- Claude เคย flag เรื่องนี้เฉพาะ TC (ใน `qa/AI-REVIEW-v43-Claude.md` หัวข้อ "explanation does not mention distractor (TC)") — **ตัวเลขจริงรวม RC ด้วยคือ 150 ข้อ**
- ความเสี่ยง: ผู้เรียนไม่รู้ว่าทำไมอีก 3 ตัวเลือกผิด → คุณค่าทางการเรียนลดลง (ไม่ใช่ความเสี่ยงเรื่องการเดา)

### 🟠 A4. ตัวลวง RC 81 ตัวทำจากคำในบทอ่าน ≥80%
Claude flag ไว้ 25 ตัว (เกณฑ์ ≥60% content words + เงื่อนไขอื่น) · Arena วัดด้วยเกณฑ์ "คำเนื้อหา ≥80% ของตัวลวงปรากฏในบท และตัวยาว ≥5 คำ" → เจอ **81 ตัว**
- ตัวอย่างที่ overlap = 1.00: `S20-Q059: Every family returned the form on time.` · `S13-Q054: Students had to contribute before the lesson.` · `S12-Q054: To record who borrowed each item.`
- ความเสี่ยง: **บางตัวอาจเป็นคำตอบที่ถูกข้อที่สอง** ต้องให้คนอ่านเทียบบท (AI ตรวจให้ไม่ได้) — Arena ยังไม่ได้ตัดสินว่าผิด ถูก flag ไว้เพื่อให้มนุษย์ตรวจ

### 🟡 A5. สัญญาณรูปแบบตัวลวง TC (ยืนยันตัวเลขของ Claude)
| รูปแบบ | เจอ | เป็นคำตอบ |
|---|---|---|
| wh-ever (`whatever/whenever/…`) | 13 | **0 (0%)** |
| passive `being/been V3` | 4 | **0 (0%)** |
| gerund `V-ing` ขึ้นต้น | 98 | 15 (15%) |
| infinitive `to V` ขึ้นต้น | 44 | 7 (16%) |

จำนวนน้อย (13 + 4) แต่เป็น 0% ทั้งคู่ → ควรสลับให้เป็นคำตอบบ้างในบางข้อ

### 🟡 A6. สัญญาณใหม่: `answer_shortest` ของ RC กับ Q-R ขยับขึ้น
| kind | Arena 16:13 | Claude 17:28 |
|---|---|---|
| rc.answer_shortest | 0.153 | **0.260** |
| qr.answer_shortest | 0.180 | **0.270** |

เป็นผลข้างเคียงของการยืดตัวลวงให้ยาวขึ้น (เพื่อแก้ answer_longest) → ตอนนี้ "เลือกข้อสั้นสุด" ได้ผล 26–27% (chance 25%) ยังไม่รุนแรง แต่ควรจับตา และมี gate ไว้ (ยังไม่มี gate ตัวไหนวัด `answer_shortest`)

### 🟡 A7. นิยาม "ฟังก์ชันซ้ำ" ไม่ตรงกันระหว่างสองรอบ
- Arena (รอบ 15:xx) บันทึก: ชื่อซ้ำ **16** ชื่อ → นับเฉพาะ `function x()` ที่ประกาศซ้ำ
- Claude (CODE-AUDIT): **66** ชื่อ → `code_audit.py` นับรวม `x = function…` และ `x = (…) =>` ด้วย
- Arena รัน `code_audit.py` ซ้ำบนต้นไม้ของ Claude ได้ **66 dups** ตามเดิม และนับแบบแคบได้ **16** → **ทั้งคู่ถูก** แต่เอกสารต้องระบุนิยาม ไม่งั้นตอน refactor จะวัด "เหลือเท่าไหร่" ไม่ได้
- ตัวเลขอื่นของ CODE-AUDIT ทวนแล้วตรงหมด: `catch{}` ว่าง 74 (app.js) + 20 (learning-hub) = 94 · `innerHTML` 69+11 = 80 · inline `on*=` 256 (app.js) + 20 (index.html) + 29 (learning-hub.js) = **305** · `setInterval` 4 + `setTimeout` 32 = 36 · `MutationObserver` 12 · `window.X=` 178

---

## 3. รายการที่มนุษย์ต้อง spot-check (รวมจาก Claude + ที่ Arena เพิ่ม)

จาก Claude (`qa/AI-REVIEW-v43-Claude.md` หัวข้อ 3): wic ใหม่ 43 · key ถอดความ 64 · บทอ่านใหม่ 4 บท/20 ข้อ · ตัวลวง RC/LC ที่ตัดคำ absolute 138 · TC 38 · Short 120 · Q-R idiom 60

Arena เพิ่ม:
- **A4** ตัวลวง RC 81 ตัวที่คำเกือบทั้งหมดมาจากบท (เสี่ยงคำตอบถูก 2 ข้อ) — รายการ id อยู่ใน `/tmp/spot_out.md` ของรอบตรวจนี้
- **A1** ตัวลวง Q-R 17 ประโยคซ้ำ (รายการอยู่ในตาราง A1)
- Q-R idiom: Arena นับด้วย regex สำนวนสามัญเจอ **22 ข้อ** ที่มีสำนวนในเฉลยหรือบท ขณะที่ gate ของ Claude นับจากสเปกได้ **60 ข้อ** → ต่างกันเพราะ gate นับ tag ในสเปก ส่วน regex นับเฉพาะสำนวนในรายการที่ Arena มี · **ไม่ใช่ข้อผิดพลาด แต่ควรมีคนยืนยันว่า 60 ข้อนั้นเป็นสำนวนจริงทั้งหมด** (Arena สุ่มดู `S01-Q002` แล้วใช้ได้: `It slipped my mind` + ตัวลวง `slipped off the table` ที่หลอกด้วยการใช้คำตรงตัว)
- Q-R 4 ข้อที่ตัวลวงก็เป็นสำนวน (เสี่ยงถูก 2 ข้อ): `S03-Q003`, `S04-Q002`, `S04-Q006`, `S05-Q006`

---

## 4. สิ่งที่ Arena เสนอให้ทำต่อ (เรียงลำดับ — เห็นด้วยกับ Claude §5 แต่สลับ 2 กับ 3)

1. **Q-R: เขียนตัวลวงเฉพาะข้อ 230 ช่อง / 101 ข้อ (A1)** — ทำก่อนเพราะเป็น pattern ที่ผู้สอบใช้เป็นทางลัดได้ชัดที่สุด และงานเป็นเชิงกลไก (ไม่ต้องเขียนบทใหม่) ตรวจด้วย gate "ไม่มีประโยคตัวลวงซ้ำเกิน 2 ครั้งทั้งคลัง" ได้ทันที
2. **Short conv: สถานการณ์ใหม่ 40 บท (A2)** — ใหญ่กว่า ต้องขยาย `tools/apply_short_v43.py` ให้รับ `context` ใหม่ได้ (ตอนนี้รับแค่ `slot/old/new/exp_add`)
3. **คำอธิบายที่ไมได้เอ่ยถึงตัวลวง 150 ข้อ (A3)** — ทำควบกับข้อ 1–2 ได้เลยตอนแตะข้อนั้น
4. RC main/purpose → 4/15 ตามปี 2568 (ลด true/attitude) — งานเล็ก
5. เพิ่ม gate: `answer_shortest ≤ 0.30` ต่อ kind (A6) + `ไม่มีประโยคตัวลวงซ้ำ ≥ 3 ครั้ง` (A1) + `ไม่มี context คู่ไหน Jaccard > 0.5` (A2)
6. คลังศัพท์ V2–V6 → โค้ด T1–T4 → Q1–Q3 (ต้องคน/อุปกรณ์จริง)
