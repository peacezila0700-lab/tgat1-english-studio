# Arena รอบ 2 — รายงานผล (v43.0.0, ทำตามลำดับ §5 ของ Claude)

เขียนโดย Arena · 2026-11-19 (Asia/Bangkok) · tree `project_claude/` · git `d0225e5` → `2c63f71`

สรุปสั้น: ทำครบ 4 ข้อแรกของลำดับที่ Claude แนะนำ (ข้อ 1 เป็นงานของมนุษย์ จึงข้ามมาเริ่มข้อ 2)
ทุกชุดทดสอบเขียวทั้งหมด · ยังไม่ได้แตะคลังศัพท์ (ข้อ 5) เพราะต้องมีการตัดสินเชิงภาษาโดยมนุษย์จำนวนมาก

| commit | งาน | ผล |
|---|---|---|
| `3b77a7b` | ข้อ 3 (§5) Q-R: ตัวลวงเฉพาะข้อ | 233 สลอตใน 101 ข้อ · ประโยคสำเร็จรูป 17 ประโยค (คลุม 230 สลอต) → 0 |
| `c2e331b` | ข้อ 2 (§5) Short conversation: บทสนทนาใหม่ 40 บท | 134 ข้อ · บทซ้ำ 60 คู่ → 0 คู่ |
| `2d1e65b` | ข้อ 3 ส่วนที่เหลือ Q-R: ตัวลวงที่ซ้ำ 2 ครั้ง | 24 สลอต · distinct 600/600 |
| `2c63f71` | ข้อ 4 (§5) RC: main/purpose/inference | แปลง TRUE 15 + attitude 15 → main 13 / purpose 11 / inference 6 |

---

## 1) Q-R — ตัวลวงเฉพาะข้อ (233 + 24 สลอต)

**ปัญหาเดิม:** ตัวลวง 17 ประโยคถูกใช้ซ้ำ 10–17 ครั้ง ครอบคลุม 230 จาก 600 สลอตใน 101 ข้อ
(จำประโยคได้ = ตัดตัวเลือกออกโดยไม่ต้องอ่านคำถาม) · หลังรอบแรกของ Arena ยังเหลือ 24 ประโยคที่ซ้ำ 2 ครั้ง

**สิ่งที่ทำ:**
- `content/qr_v43_[a-e].json` (233 entries) — ตัวลวงใหม่เขียนเป็น “คำตอบผิดหมวด” ของคำถามข้อนั้น
  (ถามความถี่ → ตอบสถานที่/เวลา, ถามเวลา → ตอบระยะเวลา ฯลฯ) พร้อมคำอธิบายไทยใหม่
- `content/qr_v43_f.json` (24 entries) — เก็บเศษสุดท้าย: วลีบอกสถานที่ 16 คู่ที่ข้อ “How often…”
  กับ “What time…” ในชุดเดียวกันใช้ร่วมกัน + อีก 8 ประโยคในข้อ request / how-long / what-should-you-do
- `tools/apply_qr_v43.py` (ต่อท้าย `rebuild_vault.sh` หลัง `apply_qr_idiom.py`) + `tools/check_qr_v43.py`

**ผลวัด:**

| ค่า | v43 Claude | หลัง Arena รอบ 2 |
|---|---|---|
| ประโยคตัวลวงที่ใช้ซ้ำ ≥3 ข้อ | 0 (แต่ซ้ำ ≥2 = 24) | **0 (ซ้ำ ≥2 = 0)** |
| distinct ตัวลวง / 600 สลอต | 576 | **600** |
| qr answer_longest | 0.275 | **0.205** |
| qr answer_shortest | 0.270 | 0.270 |
| extreme-word answer vs distractor | – | 0.080 vs 0.060 |

**gate ใหม่:** `regression_r3_content.py` G-H (ห้ามตัวลวงซ้ำ ≥2 ข้อ — เข้มขึ้นจาก ≥3) · G-I (key longest ≤25% / shortest ≤30%)
register: `QR-distractor` → G32

---

## 2) Short conversation — บทสนทนาใหม่ 40 บท (134 ข้อ)

**ปัญหาเดิม (ใหญ่กว่าที่บันทึกไว้รอบแรก):** 200 ข้อสร้างจาก 20 สถานการณ์ × 3 บทที่เหมือนกันทุกคำ
ยกเว้นชื่อคน (Jaccard สูงสุด 0.939) → อ่านบทเดียวตอบได้อีกสองบท

**สิ่งที่ทำ:**
- `content/short_new_v43_[a-f].json` — 40 บทใหม่ (2 ผู้พูด, 3–4 ช่องว่างต่อบท) พร้อมตัวเลือก
  คำอธิบายไทย และ tip ใหม่ทุกข้อ · คง id/set/difficulty และ **คงตำแหน่งคำตอบเดิม** (applier แทรก key
  ที่ index เดิม)
- `tools/apply_short_new_v43.py` (อยู่ใน `rebuild_vault.sh` หลัง `apply_short_v43.py`) +
  `tools/check_short_new_v43.py` (ตรวจ near-dup, context-overlap shortcut, extreme-word balance,
  key longest/shortest, structural cue จากเครื่องหมายวรรคตอน, ความตรงของคำพูดใน “…” และอักขระแปลก)
- register: `SHORT-new` → G33

**ผลวัด:**

| ค่า | ก่อน | หลัง |
|---|---|---|
| คู่บทที่ซ้ำกัน (Jaccard > 0.5) | 60 (สูงสุด 0.939) | **0 (สูงสุด 0.192)** |
| บทที่ไม่ซ้ำ / 200 ข้อ | 20 | **60** |
| short answer_unique_top_context_overlap | 0.285 | **0.195** |
| structural cue (ตัวเลือกเดียวที่ลงท้ายด้วย `?`) | – | **0** (เคย 56 ในร่างแรก) |
| short answer_shortest | 0.000 (v42.0.1) | **0.170** (ร่างแรก 0.888 → แก้แล้ว) |

**บทเรียนที่บันทึกไว้:** ร่างแรกพลาด 2 เรื่อง — (ก) key เป็นคำถามและตัวลวงเป็นข้อความบอกเล่าทั้งสามข้อ
ทำให้ `bankAudit.structuralCue` ขึ้น 56 ข้อ (แก้โดยทำตัวลวงหนึ่งข้อเป็นคำถามที่ไม่ได้คำตอบจากประโยคถัดไป)
และ (ข) key สั้นที่สุด 88.8% ของข้อ (แก้โดยย่อตัวลวงหนึ่งข้อต่อข้อสอบ 85 รายการ โดยคงความหมายเดิม)

**gate ใหม่:** G-J — 60 บทต้องไม่ซ้ำ, คู่บท overlap ≤0.30, key longest ≤10%, key shortest ≤30%

---

## 3) RC — เพิ่ม main / purpose / inference ตามข้อสอบปี 2568

**เหตุผล:** ตารางนับของติวเตอร์ (ดู `qa/RESEARCH-S1-S5.md` S3) ปี 2568 มี main idea + purpose 4/15
และ inference 2/15 ขณะที่คลังมี 1.8/15 และ 0.9/15 · ส่วน TRUE-statement กับ attitude **ไม่มีในตารางทั้งสองปี**

**สิ่งที่ทำ:** แปลงข้อ TRUE 15 ข้อ + attitude 15 ข้อ (ใน 25 บทอ่าน) เป็นข้อใหม่ที่อิงบทอ่านเดิม
— main 13 · purpose 11 · inference 6 (แก้ใน `content/rc_v43_[a-k].json` ตรง ๆ เพราะ spec คือ source of truth
และ `rebuild_vault.sh` replay จาก `backups/vault-v42.0.1.json`)

**type mix 300 ข้อ:** detail 120 · wic 60 · main 18→**31** · purpose 18→**29** · inference 18→**24** ·
reference 18 · paraphrase 18 · true 15→**0** · attitude 15→**0**
(main+purpose = 3.0/15 จาก 1.8/15 · ยังไม่ถึง 4/15 เพราะต้องรักษา reference/paraphrase ของปี 2567 ไว้)

**ผลวัด:** rc answer_longest 0.147 → **0.120** · answer_shortest 0.260 → 0.333 → **0.287**
(ย่อตัวลวง 14 ข้อ) · overlap 0.183 → 0.187

**gate ที่แก้:** G-A เขียนใหม่เป็น main+purpose ≥55 · inference ≥20 · reference/paraphrase ≥12 ·
true == attitude == 0 (รวมเป็น 48 checks)

---

## ตรวจซ้ำทั้งหมด (log: `/tmp/arena_round6.log`)

```
sh tools/rebuild_all.sh          # 125/98 + 6,565 logged changes
python3 tools/update_registers.py # appended 6,572
tools/check_short_new_v43.py      # ALL CLEAN (6 files, 40 dialogues, 134 items)
tools/check_qr_v43.py             # ALL CLEAN (257 entries, 250 applied, 7 superseded)
tools/check_rc_v43.py             # ALL CLEAN (11 files, 300 items)
tools/check_quotes.py data/vault.json short qr rc tc long   # 1,031 quotes / 7 not found
tests/regression_r3_content.py web  # 48/48
tests/smoke_test.py web             # 49/49
tests/regression_v42.py web         # 60/60
tests/regression_r3_ui.py web       # 7/7
tests/smoke_r3_extra.py web         # 94/94
tests/a11y_audit.py web /tmp/axe_r3.json  # errors: []
```

env ที่ต้องมี: `CHROME=~/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome`,
`AXE_PATH=tools/node_modules/axe-core/axe.min.js`

**7 quote ที่ไม่พบเป็นของเดิม (ไม่ใช่ของรอบนี้):** `S02-Q005 grab a quick bite` · `S03-Q003 not my cup of tea` ·
`S05-Q003 cost an arm and a leg` · `S06-Q001 spill the beans` · `S06-Q008 give someone a hand` ·
`S06-Q008 Sure thing. Where do they go?` · `S09-Q009 How did you find + สิ่งของ/งาน?`
→ ทั้งหมดอยู่ในข้อ idiom ของ Claude ที่คำอธิบายอ้างตัวสำนวน (ไม่ได้อยู่ใน context) — เสนอให้แก้เป็น
การอ้างตัวเลือกแทน หรือขยาย `check_quotes.py` ให้รวมสำนวนใน `prompt`/`label`

---

## สิ่งที่ควรรู้เวลารัน pipeline (artifact ที่ไม่ใช่บั๊ก)

1. `check_qr_v43.py` รายงาน `7 superseded by a later file` — หมายถึง entry ใน `qr_v43_[b,d].json`
   ที่ `qr_v43_f.json` แก้ซ้ำอีกครั้ง (ตั้งใจ) · validator รอบนี้เข้าใจกรณีนี้แล้ว
2. `check_short_new_v43.py` จะรายงานตัวเลขจาก vault เมื่อ spec ถูก apply ไปแล้ว (context ตรงกัน = ข้าม)
   → ถ้าแก้ spec หลัง apply ต้อง `sh tools/rebuild_all.sh` ก่อน แล้วค่อยรัน validator
3. `check_rc_v43.py` WARN `no typeplan` เป็นเรื่องปกติ (`/tmp/rc_typeplan.json` เป็นไฟล์ชั่วคราวของรอบเขียนข้อ)

---

## ยังค้าง (เรียงตามที่แนะนำ)

| งาน | สถานะ | หมายเหตุ |
|---|---|---|
| ข้อ 5 (§5) คลังศัพท์ V2–V6 | **ยังไม่เริ่ม** | `qa/REVIEW-QUEUE.csv` 1,505 แถว: 772 needs-human-rewrite · 146 uncertain-headword · 105 plural-countability · 46 plausible · 44 uncertain — ส่วนใหญ่ต้องมนุษย์ตัดสิน |
| T1–T4 refactor (`app.js`, CSP, lazy `data.js`, lazy hub) | ยังไม่เริ่ม | ควรทำเป็นรอบแยก มี `regression_r3_ui.py` + `smoke_r3_extra.py` กันพัง |
| A3 คำอธิบาย 150/600 ข้อ (TC+RC) ไม่เอ่ยคำของตัวลวงที่ยาว ≥4 ตัวอักษรเลย | ค้าง | ตรวจด้วย `/tmp/spot.py` ของ Arena |
| A4 ตัวลวง RC 81 ข้อใช้คำจากบทอ่าน ≥80% | ค้าง | ทำให้ตัดตัวเลือกด้วย “คำที่ไม่อยู่ในบทอ่าน” ได้ |
| A5 pattern-key ใน TC: wh-ever 13/0 · passive 4/0 · gerund-init 98/15 · infinitive-init 44/7 | ค้าง | ต้องกระจายคำตอบให้เข้า pattern บ้าง |
| C4 บทอ่าน genre ใหม่ | ทำ 4 จากเป้า ~30 | `content/rc_v43_i.json` มี `context`/`topic`/`genre` |
| idiom ที่ยังขาด (S4) | ค้าง | `hit the nail on the head`, `better late than never`, `bite off more than you can chew` |
| 2-key risk `S03-Q003, S04-Q002, S04-Q006, S05-Q006` (Q-R idiom regex 22 vs gate 60) | ค้าง | ต้องคนตรวจ |
| Q1–Q3 / T5 | ห้าม AI อ้าง | ต้องคน + อุปกรณ์จริง |
