# V43 — ใบสั่งงานละเอียด (ส่งต่อให้ Claude ทำต่อ)

> เขียนโดย Arena AI · 2026-11-19 16:10 (เวลาไทย) · ตัวเลขทุกตัวในไฟล์นี้ **วัดจริง** จากการ `rebuild_all.sh` + รันเทสต์เต็มชุดบนโปรเจกต์ใน commit `61a896c` ไม่ใช่การคาดเดา
> อ่านคู่กับ `HANDOFF.md` (กติกา + BACKLOG C/V/S/T/Q ที่ merge กลับมาแล้ว) และ `qa/R3-QA-LOG.md`

---

## 0. สถานะปัจจุบัน

| หัวข้อ | ค่า |
|---|---|
| เวอร์ชันแอปที่ build แล้ว | **42.0.2** (ยังไม่ bump เป็น 43.0.0 — ดูงาน T7) |
| git | `c8499e4` import → `fbe2f20` 8a headword → `b8b16b0` C1 LC → `e80af6e` C2 TC → `6d9368e` C3 RC → `61a896c` sync/pack |
| เทสต์ล่าสุด (เขียวครบ) | smoke 49/49 · regression_v42 60/60 · regression_r3_content 27/27 · regression_r3_ui 7/7 · smoke_r3_extra 94/94 · a11y `errors: []` |
| rebuild | deterministic (md5 `data/vault.json`, `qa/changes_r3.jsonl`, `web/data-vault.js` ตรงกัน 2 รอบ) |
| ชุดไฟล์ใน Drive (`tgat project/TGAT1 v43/`) | `WORKING-v43-part1.zip` (2,366,061 B, sha `43974531ca193707…`), `WORKING-v43-part2.zip` (2,238,009 B, sha `f17e0250c1346edf…`), `WORKING-v43-part3.zip` (396,366 B, sha `ee4ab3a9ae588dec…`), `MANIFEST-v43.json` · ชุดเก่าของ Claude 12:54 ยังอยู่ (`WORKING-part1/2.zip`, `MANIFEST.json`, `HANDOFF.md`) · `HANDOFF-claude-1256-BACKLOG.md` = สำเนา BACKLOG ที่ merge เข้า HANDOFF แล้ว |
| ข้อจำกัดที่เจอ | อัป `HANDOFF.md` ตัวเดี่ยวขึ้น Drive **ไม่ผ่าน** (security filter ของ connector provider บล็อกที่เนื้อหา) → HANDOFF รุ่น v43 อยู่ใน `WORKING-v43-part1.zip` กับใน git เท่านั้น · **ห้าม**ลองอัปซ้ำหรือดัดแปลงเนื้อหาเพื่อเลี่ยงฟิลเตอร์ |

### ตัวเลขสัญญาณเดาคำตอบ (วัดจาก `data/vault.json` ปัจจุบัน)

`python3 tools/bias_metrics.py data/vault.json`

| kind | n | answer_longest | unique_longest | answer_shortest | context-overlap |
|---|---|---|---|---|---|
| rc | 300 | **0.200** | 0.200 | 0.153 | **0.413** |
| long | 200 | 0.270 | 0.245 | 0.120 | 0.180 |
| short | 200 | 0.000 | 0.000 | 0.000 | **0.670** |
| tc | 300 | **0.420** | 0.137 | 0.387 | 0.027 |
| qr | 200 | 0.285 | 0.235 | 0.180 | 0.000 |

`python3 tools/rc_heuristics.py data/vault.json` (chance = 0.25)

| กลยุทธ์เดา RC | ความแม่น |
|---|---|
| longest | **0.200** ✅ |
| no-topic-name + longest | **0.200** ✅ |
| no-extreme-word + longest | **0.283** ✅ |
| max-context-overlap | **0.517** ❌ (เป้า ≤0.35) |
| combined (no name + no extreme + overlap) | **0.537** ❌ |
| extreme-word rate | answer 0.067 vs distractor **0.194** ❌ (ต่างกัน 2.9 เท่า) |

---

## 1. งานที่เสร็จแล้ว — **ห้ามทำซ้ำ**

| ID | งาน | ไฟล์ที่สร้าง/แก้ | commit | ผล |
|---|---|---|---|---|
| C1 | LC ชุด 11–20 เปลี่ยนจากถามความเข้าใจ → เติมบทสนทนา 20 บท/100 ข้อ | `content/lc_blank_v43_[e-h].json`, `tools/apply_lc_blank.py` (ขยาย glob), `tools/rebuild_vault.sh` (ตัด `apply_lc_comp.py`), ย้ายของเก่าไป `superseded/` | `b8b16b0` | ตำแหน่งคำตอบ 50/50/50/50 · quote ผ่าน · key-longest 26/100 |
| C2 | TC เขียนใหม่ 40 passage/300 ช่อง | `content/tc_v43_[a-j].json`, `tools/apply_tc_v43.py` (แทน `apply_tc.py`), `tools/update_registers.py` (tag `TC-rewrite`→G25) | `e80af6e` | vocab/collocation **125/300 (41.7%)** · verb 46, tense 46, clause 34, conn 27, inversion 10, tag 12 · ตำแหน่ง 75/75/75/75 |
| C3 | RC เขียนใหม่ 60 passage/300 ข้อ (คง context เดิม เปลี่ยน prompt/ตัวเลือก/เฉลย/tip) | `content/rc_v43_[a-k].json`, `content/rc_v43_tips.json`, `tools/apply_rc_v43.py`, `tools/check_rc_v43.py` (validator ใหม่), `tools/apply_rc_v43_len.py` + `qa/rc_v43_lenpatches/`, ย้าย RC pipeline เก่าไป `superseded/` | `6d9368e` | details **120/300 (40%)** · TRUE 25, paraphrase 25, attitude 25, reference 24, inference 21, purpose 21, wic 21, main 18 · ตำแหน่ง 75/75/75/75 · key-longest 20% · second-longest 44% |
| V1 (8a) | headword ปลอม 56 คำ → collocation จริง | `content/headword_rename_r3.json`, `tools/apply_headword_rename.py`, alias migration ใน `web/app.js`, `D['headwordAliases']` (56) ใน `web/data.js` | `fbe2f20` | REVIEW-QUEUE 1217 → 1161 |

---

## 2. งานค้าง — เรียงลำดับที่ควรทำ

> ทุกงานที่แตะเนื้อหา: แก้ที่ `content/` เท่านั้น → `sh tools/rebuild_all.sh` → รันเทสต์ → `python3 tools/update_registers.py` → เขียนบันทึกท้าย `HANDOFF.md` → commit
> ทุกงานต้อง **เพิ่ม gate ใหม่ในเทสต์** กันปัญหาเดิมกลับมา (งาน T6) — โค้ด gate สำเร็จรูปอยู่ในหัวข้อ 3

---

### งานที่ 1 (C3 ค้าง) — RC: เพิ่ม words-in-context จาก 21 → ~60 ข้อ · **ทำก่อน เพราะถูกและตรงเป้า blueprint ที่สุด**

**ปัญหา:** เป้าหมายจาก tutor count คือ *words in context 3 ข้อต่อ 15 ข้อ* (= 60 ต่อ 300) แต่ตอนนี้มี **21 ข้อ (1.05 ต่อ 15)** เพราะ Arena เน้นเติมประเภทที่คลังเดิมไม่มีเลย (TRUE/paraphrase/attitude/reference) ก่อน

**ตารางเป้าที่ให้ (รวม 300 พอดี และทุกประเภทอยู่ในช่วง tutor count):**

| type | ปัจจุบัน | เป้า | Δ | ต่อ 15 ข้อ (เป้า tutor) |
|---|---|---|---|---|
| detail | 120 | **120** | 0 | 6 (ช่วง 6–7) ✅ |
| wic | 21 | **60** | **+39** | 3 ✅ |
| true | 25 | 15 | −10 | 0.75 (official sample มี) |
| attitude | 25 | 15 | −10 | 0.75 |
| paraphrase | 25 | 18 | −7 | 0.9 (ช่วง 0–2) ✅ |
| reference | 24 | 18 | −6 | 0.9 (ช่วง 0–2) ✅ |
| inference | 21 | 18 | −3 | 0.9 (ช่วง 0–2) ✅ |
| purpose | 21 | 18 | −3 | รวม main+purpose = 1.8 (ช่วง 1–4) ✅ |
| main | 18 | 18 | 0 | |

**วิธีทำ:**
1. เลือก 39 ข้อที่จะแปลงเป็น wic — แนะนำแปลงจาก `true`/`attitude`/`paraphrase`/`reference`/`inference`/`purpose` ตาม Δ ในตาราง **ห้ามแปลงจาก detail** (detail ต้องคง 120 = 6/15)
2. กระจายให้ทุก passage ยังมี 5 ประเภทไม่ซ้ำกัน (เช็คด้วย `tools/check_rc_v43.py` — มัน assert ว่า slot 2–4 ไม่ซ้ำ type) และคง pattern "detail 2 ข้อต่อ passage"
3. ข้อ wic ต้องเลือกคำ/วลีที่ **มีจริงใน context ของ passage นั้น** และอยู่ในบริบทที่ตีความได้ทางเดียว · stem ใช้รูป: `In the passage, the word “X” is closest in meaning to` หรือ `In the passage, the phrase “X” is closest in meaning to`
4. ตัวเลือกของ wic เขียนเป็นวลีตัวพิมพ์เล็กทั้งหมด (ตามแบบ 21 ข้อที่มีอยู่) และต้องยาวพอ ๆ กัน — ดูกับดักเรื่อง length gate ด้านล่าง
5. อัปเดต `content/rc_v43_tips.json` ไม่ต้องแก้ (มี tip ของ wic อยู่แล้ว)

**ไฟล์:** `content/rc_v43_[a-k].json` (แก้ `type`, `prompt`, `key`, `d`, `exp` ของข้อที่แปลง)

**คำสั่งตรวจ:**
```sh
python3 tools/check_rc_v43.py           # type ตรงแผน + quote มีจริงในบท + ไม่มีอักษรแปลกปลอม
sh tools/rebuild_all.sh
python3 tests/regression_r3_content.py web
python3 tools/rc_heuristics.py data/vault.json
```

**เกณฑ์เสร็จ:** นับ type แล้วได้ wic ≥ 55, detail ≥ 118 · gate ใหม่ (หัวข้อ 3 ข้อ G-A) ผ่าน · เทสต์เดิมเขียวครบ · `update_registers.py` แล้ว commit

**กับดัก:** `tools/check_rc_v43.py` อ่านแผน type จาก `/tmp/rc_typeplan.json` ซึ่ง **หายไปแล้วหลัง sandbox reset** — ถ้ามันฟ้องว่า type ไม่ตรงแผน ให้ลบการเช็คนั้นออก หรือสร้างแผนใหม่จากตารางเป้าด้านบน (โค้ดสร้างแผนเดิมอยู่ใน git history ของ session Arena แต่ไม่ได้ commit ไฟล์แผน)

---

### งานที่ 2 (C7) — RC: ลด `max-context-overlap` จาก 51.7% → ≤35% · **หนักสุดของ RC ตอนนี้**

**ปัญหา:** กลยุทธ์ "เลือกตัวเลือกที่มีคำซ้ำกับบทอ่านมากที่สุด" ตอบถูก **51.7%** (chance 25%) เพราะ Arena เขียนคำตอบถูกโดยยกสำนวนจากบทอ่านตรง ๆ (จำเป็นสำหรับข้อ detail/reference) แต่ตัวลวงใช้คำที่ **ไม่โผล่ในบทอ่านเลย** ทำให้แยกได้ง่าย

**หลักฐาน:** `python3 tools/rc_heuristics.py data/vault.json` → `"max-context-overlap": 0.517`, `bias_metrics` → `answer_unique_top_context_overlap: 0.413`

**วิธีทำ (ทำทีละ passage, เริ่มจาก 20 passage แรกแล้ววัดใหม่):**
1. เปิด `tools/rc_heuristics.py` ดูวิธีนับ overlap (นับคำร่วมระหว่างตัวเลือกกับ context)
2. เขียนรายการคำที่ overlap สูงสุดต่อข้อ:
   ```sh
   python3 - << 'PY'
   import json,re,collections
   V=json.load(open('data/vault.json'))
   stop=set('the a an of to in for and or is are was were be been with that this it they he she as at on by from'.split())
   rows=[]
   for q in V:
       if q['kind']!='rc': continue
       cw={w for w in re.findall(r"[a-z']+",q['context'].lower()) if w not in stop}
       sc=[(len({w for w in re.findall(r"[a-z']+",o.lower()) if w not in stop}&cw),i) for i,o in enumerate(q['options'])]
       sc.sort(reverse=True)
       rows.append((sc[0][0]-sc[1][0], q['id'], sc[0][1]==q['answer'], q['options'][sc[0][1]][:60]))
   rows.sort(reverse=True)
   for r in rows[:40]: print(r)
   PY
   ```
3. แก้ 2 ทาง (ใช้ทั้งคู่): **(ก)** เติมคำที่โผล่ในบทอ่านเข้าไปในตัวลวง 1–2 คำต่อตัวเลือก (ต้องยังเป็นข้อผิดด้วยเหตุผลอื่น) **(ข)** เขียนคำตอบถูกใหม่ด้วยคำ synonym ที่ไม่ซ้ำบทอ่านตรง ๆ (แต่ต้องไม่กำกวม — ห้ามทำให้คำตอบถูกกลายเป็น "ตีความได้หลายทาง")
4. ห้ามใช้วิธีตัดคำออกจากบทอ่าน (context ถูก freeze แล้ว และมี gate `RC passages 100–200 words`)

**เกณฑ์เสร็จ:** `rc_heuristics.py` → `max-context-overlap ≤ 0.35` และ `combined ≤ 0.40` · gate เดิม (key-longest ≤30%, second-longest ≤50%, drop-topic-longest ≤35%) ต้องยังผ่าน · เทสต์เขียวครบ

---

### งานที่ 3 (C7 · เกิดจากงาน C2 ของ Arena) — TC: `answer_longest` 42% → ≤35%

**ปัญหา:** ใน 300 ช่อง TC คำตอบที่ถูกเป็นตัวเลือก **ยาวที่สุด** ถึง **42%** (126 ข้อ) — เกินเป้า 35% และ **ยังไม่มี gate ตัวไหนจับ** (`regression_r3_content.py` มี gate ยาวสุดเฉพาะ LC ≤30% กับ RC ≤30%/35%)

**สาเหตุ:** งาน C2 ใส่ collocation ยาว (เช่น `take pride in`, `a wide range of`, `according to`) เป็นคำตอบบ่อย ขณะที่ตัวลวงเป็นคำเดี่ยวสั้น ๆ

**วิธีทำ:**
1. แสดงรายการข้อที่ key ยาวสุด (วัดเป็น **ตัวอักษร** ไม่ใช่คำ):
   ```sh
   python3 - << 'PY'
   import json
   V=json.load(open('data/vault.json'))
   bad=[(len(q['options'][q['answer']]),q['id'],q['options']) for q in V
        if q['kind']=='tc' and len(q['options'][q['answer']])==max(map(len,q['options']))]
   bad.sort(reverse=True)
   print(len(bad),'/300 =',round(len(bad)/300,3))
   for b in bad[:25]: print(b)
   PY
   ```
2. แก้ที่ `content/tc_v43_[a-j].json`: **ยืดตัวลวง** ให้ยาวใกล้เคียง (เช่น ตัวลวง `so` → `so that`, `which` → `which is`) หรือ **หด key** (เช่น `a wide range of` → `various`) — ต้องไม่ทำให้คู่กำกวมกลับคืนมา (ดูรายการคู่ห้ามใน gate `TC: known ambiguous option pairs`)
3. ระวัง `bankAudit` ใน `tests/smoke_test.py`: `structuralCue` (ตัวลวงทุกตัวจบเหมือนกันแต่ key จบต่าง) และ `keyLengthOutlier` (คำใน key ≥ max(6, 1.8× ตัวลวงที่ยาวสุด))

**เกณฑ์เสร็จ:** `bias_metrics.py` → `tc.answer_longest ≤ 0.35` · gate ใหม่ (หัวข้อ 3 ข้อ G-C) ผ่าน · เทสต์เขียวครบ

---

### งานที่ 4 (C6 + C7) — Short Conversation: context-overlap 67% → ≤35% + สถานการณ์ซ้ำ LC

**ปัญหา 2 ชั้นใน 200 ข้อเดียวกัน:**
1. `answer_unique_top_context_overlap = 0.670` — เลือกตัวเลือกที่คำซ้ำกับบทสนทนามากสุด ตอบถูก 67% (หนักสุดทั้งคลัง)
2. สถานการณ์ซ้ำกับ LC 20 เรื่อง (บันทึกใน `qa/R3-QA-LOG.md`)

**วิธีทำ:**
1. ยังไม่มีสเปกไฟล์สำหรับ short — ต้องสร้างใหม่: ดูโครงสร้าง item ก่อน
   ```sh
   python3 -c "
   import json;V=json.load(open('data/vault.json'))
   s=[q for q in V if q['kind']=='short'];print(len(s));print(json.dumps(s[0],ensure_ascii=False)[:900])"
   ```
2. สร้าง `content/short_v43_[a-?].json` + `tools/apply_short_v43.py` (เลียนแบบ `tools/apply_tc_v43.py`: glob สเปก → map กับ item ใน vault → log ด้วย `changelog.log` → ตั้ง tag ใหม่ เช่น `SHORT-rewrite`)
3. เพิ่ม tag ใน `tools/update_registers.py` ทั้ง dict `G` (→ G30 หรือเลขถัดไป) และ dict `ST`
4. เขียนสถานการณ์ใหม่ 30 เรื่องที่ไม่ซ้ำ LC (LC ปัจจุบัน 40 เรื่อง: museum night, campus shuttle, market layout, library booking, clinic reminders, coastal trip, theatre subtitles, food bank, bike docks, heatwave room, timetable pilot, repair café, audio walk, food-waste survey, park watering, language exchange, bus-stop board, swimming lesson, museum workshop, flood notice + ชุด 1–10)
5. ลด overlap โดยทำให้ตัวลวงใช้คำจากบทสนทนาด้วย (เหมือนกันงานที่ 2)

**เกณฑ์เสร็จ:** `bias_metrics.py` → `short.answer_unique_top_context_overlap ≤ 0.35` · ไม่มีธีมซ้ำ LC (เขียนสคริปต์เทียบคำหลักของ context) · gate ใหม่ (หัวข้อ 3 ข้อ G-D) ผ่าน

---

### งานที่ 5 (C4) — บทอ่าน genre ใหม่: ข่าว / ประกาศ / โฆษณา / บทความความรู้ / อีเมล · ~30 RC + ~20 TC

**ปัญหา:** RC ทั้ง 60 passage (และ TC ส่วนใหญ่) เป็นเรื่อง "โครงการชุมชน/โรงเรียน → ทดลอง → ประเมิน" เหมือนกันหมด ทำให้:
- ไม่ตรง blueprint (ข้อสอบจริงมีข่าว ประกาศ โฆษณา บทความวิชาการ อีเมล)
- **มี passage เกือบซ้ำกัน 2 คู่** (ยืนยันแล้วด้วยการอ่านเทียบ):
  - `S14-Q056` (A community energy plan) ↔ `S20-Q051` (A home energy checklist) — ทั้งคู่: อาสาสมัคร + checklist + plug meter + standby power + ผลประหยัดต่างกันแต่ละบ้าน + สรุปว่าควรอิงผลวัด
  - `S07-Q046` (A lost-and-found data review) ↔ `S16-Q046` (A campus lost-property desk) — ทั้งคู่: ของหายค้างนาน → ทำระบบบันทึก/รหัส/ประกาศ → ของถูกรับคืนเร็วขึ้น → ยังเหลือปัญหา → วางแผนทบทวน
  - บันทึกไว้ใน `qa/R3-QA-LOG.md` บรรทัด 63

**วิธีทำ:**
1. เลือก RC 30 passage ที่ธีมซ้ำที่สุด (เริ่มจาก 2 คู่ด้านบน = 4 passage) → เขียน `context` ใหม่คนละ genre
2. **การเปลี่ยน context = ต้องเขียนข้อสอบ 5 ข้อของ passage นั้นใหม่ทั้งหมด** (เพราะข้อผูกกับข้อความในบท) + ต้องรัน `tools/check_rc_v43.py` ใหม่ — ไฟล์ `/tmp/rc_passages.json` ที่ Arena ใช้เก็บ context เก่า **หายไปแล้ว** สร้างใหม่ได้ด้วย:
   ```sh
   python3 - << 'PY'
   import json,collections
   V=json.load(open('data/vault.json'))
   rc=[q for q in V if q['kind']=='rc']
   out=[]
   for i in range(0,300,5):
       g=rc[i:i+5]
       out.append({'first':g[0]['id'],'set':g[0]['set'],'topic':g[0]['topic'],
                   'context':g[0]['context'],'ids':[x['id'] for x in g]})
   json.dump(out,open('/tmp/rc_passages.json','w'),ensure_ascii=False,indent=1)
   print(len(out))
   PY
   ```
3. สเปก RC ปัจจุบัน (`content/rc_v43_*.json`) **ไม่มี field `context`** (ใช้ context เดิมใน vault) → ถ้าจะเปลี่ยนบทอ่าน ต้องเพิ่ม `context` ในสเปก และแก้ `tools/apply_rc_v43.py` ให้เขียน `q['context']` ด้วย (ตอนนี้มันเขียนแค่ prompt/options/answer/explanation/tip) + ต้อง keep ความยาว 100–200 คำ (gate `bank: RC passages 100–200 words`)
4. TC: สร้าง passage ใหม่ 20 บท (ข่าว/ประกาศ/โฆษณา/อีเมล) ลง `content/tc_v43_[k-?].json` แล้วขยาย glob ใน `tools/apply_tc_v43.py` จาก `[a-j]` — ระวัง assert `len(groups)==40` ในนั้น ต้องแก้เป็น 60 และ map passage ให้ครบ (ตอนนี้มัน map แบบ 7+8 ต่อชุด = 40 passage พอดี)
5. genre ที่ควรมี (จาก official/tutor sample): ข่าวปิดพิพิธภัณฑ์, ประกาศย้ายสถานที่, โฆษณาขาย/รับสมัคร, บทความ AI/โซเชียล/ภาษี/ไลฟ์สดขายของ, อีเมลธุรกิจ, ประกาศรับสมัครงาน, ตารางกิจกรรม, บทวิจารณ์

**เกณฑ์เสร็จ:** ไม่มี passage คู่ไหนคล้ายกัน (วัดด้วย word-overlap ระหว่าง context ≤ 0.25) · genre ครอบคลุม ≥ 5 ประเภท · ความยาว 100–200 คำ · ทุกข้อมีคำอธิบายไทย + quote มีจริง · เทสต์เขียวครบ

---

### งานที่ 6 (C5) — Q-R: เพิ่ม idiom/สำนวนพูด จาก ~3–21 → ≥60 ข้อ

**ปัญหา:** Question-Response 200 ข้อเป็น wh-question/answer-type matching กับ polite request เกือบหมด · นับด้วย regex สำนวนสามัญเจอ **3 ข้อ** (Claude เคยรายงาน 21/200 — ต่างกันที่วิธีนับ ให้ใช้ 60 เป็นเป้าแบบ absolute)

**วิธีทำ:**
1. ดูโครง item: `python3 -c "import json;V=json.load(open('data/vault.json'));q=[x for x in V if x['kind']=='qr'][0];print(json.dumps(q,ensure_ascii=False)[:700])"`
2. สร้าง `content/qr_idiom_v43_[a-?].json` + `tools/apply_qr_idiom.py` (tag `QR-idiom` → เพิ่มใน `update_registers.py`)
3. สำนวนที่ควรมี (ระดับ TGAT1): `Small world, isn't it?` / `It slipped my mind` / `I'm all ears` / `It's up to you` / `No wonder` / `That rings a bell` / `I can't make it` / `Take your time` / `It's not my cup of tea` / `Let's call it a day` / `Break the ice` / `Once in a blue moon` / `Piece of cake` / `Under the weather` / `Cost an arm and a leg` / `Hit the books` / `Spill the beans` / `Bite the bullet` / `On the fence` / `Play it by ear`
4. **ตัวลวงต้องเป็นคำตอบที่ใช้ไม่ได้ในสถานการณ์นั้นจริง ๆ** ไม่ใช่ผิดไวยากรณ์ (ตามเช็กลิสต์เขียนข้อสอบใน HANDOFF) และต้องไม่มี 2 ตัวเลือกที่ถูกทั้งคู่

**เกณฑ์เสร็จ:** idiom ≥ 60 ใน 200 · `bias_metrics` qr ไม่แย่ลง (answer_longest ตอนนี้ 0.285) · gate ใหม่ · เทสต์เขียวครบ

---

### งานที่ 7 (C7) — ลด extreme-word cue ทั่วคลัง

**ปัญหา:** ตัวลวงมีคำประเภท absolute (`all, every, never, always, only, must, no one, completely`) **19.4%** ขณะที่คำตอบถูกมีแค่ **6.7%** → ตัดตัวเลือกที่มีคำ absolute ทิ้งแล้วเดาที่เหลือ ดีขึ้นชัด (รวมในกลยุทธ์ `no-extreme-word+longest` = 28.3% สำหรับ RC)

**วิธีทำ:**
```sh
python3 - << 'PY'
import json,re
V=json.load(open('data/vault.json'))
EX=r'\b(all|every|everyone|always|never|no one|nobody|nothing|only|must|completely|totally|impossible|guaranteed)\b'
for kind in ['rc','tc','long','short','qr']:
    ks=[q for q in V if q['kind']==kind]
    a=sum(1 for q in ks if re.search(EX,q['options'][q['answer']],re.I))
    d=sum(1 for q in ks for i,o in enumerate(q['options']) if i!=q['answer'] and re.search(EX,o,re.I))
    print(kind,'answer',a,f'{a/len(ks):.3f}','distractor',d,f'{d/(3*len(ks)):.3f}')
PY
```
แก้โดย **ลดคำ absolute ในตัวลวง** (เขียนให้เป็นข้อผิดแบบเจาะจงมากขึ้น เช่น `never` → `rarely` หรือระบุเงื่อนไขผิดแทน) ในไฟล์สเปก `content/rc_v43_*.json`, `content/tc_v43_*.json`, `content/lc_blank_*.json`

**เกณฑ์เสร็จ:** อัตรา extreme-word ของ answer กับ distractor ต่างกันไม่เกิน 1.5 เท่าในทุก kind

---

### งานที่ 8 (C9) — AI ตรวจรอบสอง (ก่อนมนุษย์) · **เขียนรายงานเท่านั้น ห้ามแก้ไฟล์ข้อสอบ**

**งาน:** อ่านข้อสอบทีละส่วน หา (ก) มีคำตอบถูก 2 ข้อ (ข) ไม่มีคำตอบถูก (ค) ภาษาไม่ธรรมชาติ (ง) คำอธิบายไทยผิด/ไม่ตรงกับข้อ (จ) ตัวลวงผิดไวยากรณ์ชัดจนไม่ต้องอ่านบท

**ผลลัพธ์:** `qa/AI-REVIEW-<kind>-<sets>.md` รูปแบบ: `| id | ปัญหา | หลักฐาน | ข้อเสนอแก้ |`

**ลำดับที่ควรตรวจก่อน:** RC 300 (เขียนใหม่ทั้งหมด ยังไม่มีใครตรวจ) → TC 300 → LC 100 → ที่เหลือ

**หมายเหตุ:** `tools/check_quotes.py` ตรวจ quote อัตโนมัติอยู่แล้ว (ผ่าน) — งานนี้คือส่วนที่ automate ไม่ได้

---

### งานที่ 9 (V2) — ตัวอย่างประโยค noun-slot 772 + 105 + 120 รายการ

**หลักฐาน (`qa/REVIEW-QUEUE.csv`, 1,505 แถว):**
| status | จำนวน |
|---|---|
| needs human rewrite (grammatical but generic template) | **772** |
| UNCERTAIN — headword อยู่ใน headword-validity queue (แก้/ถอด headword ก่อน) | 146 |
| corrected — spot-check recommended | 120 |
| UNCERTAIN — plural/countability | 105 |
| PLAUSIBLE collocation — keep after human confirmation | 46 |
| UNCERTAIN — needs editor decision | 44 |

หมวด: `example-quality` 1,217 · `headword-validity` 146 · `spot-check AI-drafted text` 120 · อื่น ๆ 22 · priority P1 647 / P2 856 / P3 2

**วิธีทำ:**
1. `python3 tools/vocab_triage.py` (สร้าง queue ใหม่ทุก rebuild) — อย่าแก้ CSV ด้วยมือ
2. ตัวอย่างใหม่เขียนในไฟล์สเปก (หา pattern เดิม: `content/vocab_*` / ดู `tools/vocab_triage.py` ว่าอ่าน field ไหน) แล้วให้ pipeline เขียนทับ — **ห้ามแก้ `data/data.json` หรือ `web/data.js` ตรง ๆ**
3. ลำดับ: P1 ก่อน → ทำครั้งละ 50 คำ → rebuild + เทสต์ → commit
4. `headword-validity` 146 รายการ: ตัดสินก่อนว่า headword นั้นควรอยู่ต่อไหม (plausible 46 เก็บ / uncertain 44 ตัดสิน) มิฉะนั้นตัวอย่างที่เขียนจะเสียเปล่า

**เกณฑ์เสร็จ:** queue เหลือ 0 ในหมวด example-quality (หรือมีเหตุผลบันทึกต่อรายการ) · REVIEW-QUEUE.csv มีชื่อผู้ตรวจ+วันที่สำหรับส่วนที่มนุษย์ยืนยันแล้ว

---

### งานที่ 10 (V3) — gloss ไม่ตรง 35 รายการ + วลีขาดตัวอย่าง 87 รายการ

ดูรายการใน `qa/REVIEW-QUEUE.csv` (กรอง `category` = `legacy-gloss` / `example-quality` ที่ headword เป็นวลี) และ `qa/r3-gloss-scan.json`
**กติกาเดิมที่ต้องรักษา:** gloss ไทยต้องมี **ศูนย์ตัวอักษรละติน** (gate `regression_v42.py:62`), ห้ามมี antonym pair (A - B) ใน gloss หลัก, comparison ให้ไว้ใน note เท่านั้น

---

### งานที่ 11 (V4) — IPA: 1,333 รายการnotation eSpeak + 83 รายการต้องฟังเช็ก

**สถานะ:** `tools/ipa_stress_fix.py` แก้ stress mark แล้ว 336 คำ · ที่เหลือ 2,554 ถูกแล้ว · **83 คำไม่ regenerate เพราะต่างจาก CMUdict conversion** (ต้องคนฟัง)
**วิธีทำ:** ทำให้สัญกรณ์เป็น CMUdict แบบเดียวกันทั้งคลัง (ตอนนี้ผสม eSpeak) — ดู `tools/ipa_fill.py` + `tools/ipa_stress_fix.py` เป็นแบบ · 83 รายการที่ค้างต้องมนุษย์ฟัง (ห้าม AI อ้างว่าตรวจแล้ว)

---

### งานที่ 12 (V5 + V6) — ผูกคลังศัพท์กับข้อสอบ + เพิ่ม collocation ให้คำ B–C ที่ใช้ใหม่

- **V5:** ศัพท์ที่ออกใน TC/RC (โดยเฉพาะของใหม่ 300 + 300 ข้อ) ต้องอยู่ในคลัง และมีปุ่ม "ฝึกคำนี้" จากหน้าข้อสอบ → ต้องทำทั้งรายการคำ (A) และโค้ด (R) ใน `web/app.js`
  ```sh
  # สร้างรายการคำที่ออกสอบแต่ไม่มีในคลัง
  python3 - << 'PY'
  import json,re
  V=json.load(open('data/vault.json')); D=json.load(open('data/data.json'))
  bank={w['w'].lower() for w in D['studio']['words']}|{p['w'].lower() for p in D['studio']['phrases']}
  need=set()
  for q in V:
      if q['kind'] in ('tc','rc'):
          for w in re.findall(r"[a-z]+(?:[ -][a-z]+)*", (q['context']+' '+' '.join(q['options'])).lower()):
              if w not in bank and len(w)>3: need.add(w)
  print(len(need)); print(sorted(need)[:60])
  PY
  ```
- **V6:** เพิ่ม collocation/word family ให้คำระดับ B–C ที่ใช้ในงาน C2/C3 ใหม่ (ตอนนี้ TC มี inversion/question tag แล้ว คลังคำยังไม่มีตัวอย่างกลุ่มนั้น)

---

### งานที่ 13 (T1–T8) — โค้ด/หนี้เทคนิค + **bump 43.0.0**

| ID | งาน | รายละเอียดที่ทำต่อได้ทันที |
|---|---|---|
| T1 | app.js มี 45 ชั้น patch / ฟังก์ชันถูก patch ทับ 43 ตัว / ชื่อซ้ำ 16 ชื่อ (`audit`×6, `start`×5, `decorate`×4, `studioRender`×4, `VLT_finish`×4) | รวมทีละโมดูล + รัน `regression_r3_ui.py` ทุกครั้ง |
| T2 | CSP เข้ม | ย้าย inline `<script>` ใน `web/index.html` → `web/app.js`; แทน `on*=` ~300 จุดด้วย `data-action` + delegated listener |
| T3 | `web/data.js` 2 MB บล็อก first paint | แยก `studio.examples` + `pack` เป็น lazy chunk (แบบเดียวกับ `data-vault.js`/`data-senses.js` ที่ `tools/datafiles.js` ทำอยู่แล้ว) |
| T4 | `learning-hub*.js` ~93 KB gzip โหลดตอนเริ่ม | โหลดเมื่อเข้า Hub แต่ `TGAT1Hub.continue()` บนหน้า Home ต้องยังทำงาน offline |
| T5 | Lighthouse / Web Vitals | ยังไม่เคยรัน |
| T6 | **ทุกงาน C/V ต้องมี regression test ใหม่** | ใช้โค้ดในหัวข้อ 3 ของไฟล์นี้ |
| T7 | **bump 43.0.0** | ไฟล์ที่มี `42.0.2`: `web/app.js`, `web/index.html`, `web/manifest.webmanifest`, `web/sw.js`, `web/data.js` (header), `tools/rebuild_all.sh` (บรรทัด `node tools/datafiles.js build data web 42.0.2`), `tests/regression_v42.py:18` (`EXPECT_VERSION = '42.0.2'`), `tests/regression_r3_ui.py`, `tests/regression_r3_content.py`, `tests/harness.py`, `tools/update_registers.py`, `tools/apply_rc_v43.py`, `tools/apply_tc_v43.py` · cache namespace ใน `sw.js` ต้องขึ้น `tgat1-studio-v43.0.0` |
| T8 | ZIP deploy | **ห้ามมี** `qa/ backups/ tools/ tests/ content/` · ทำ SHA-256 · ZIP ของ QA+tests แยกอีกไฟล์ · รอบนี้ต้องใส่ `qa/R3-BLUEPRINT-ALIGNMENT.md` ด้วย (รอบก่อนขาด) |

---

### งานที่ 14 (Q1–Q3) — ต้องมนุษย์/อุปกรณ์จริง · **AI ห้ามอ้างว่าผ่าน**

- Q1 screen reader (VoiceOver/TalkBack/NVDA) + WCAG ด้วยมือ · axe `incomplete` มี **144 จุด/ไฟล์ผล** (`qa/_arena_axe_v43.json`, `qa/axe-r3-final.json`) ต้องดูด้วยตา
- Q2 iOS Safari, Android Chrome, ติดตั้ง PWA + อัปเดตเวอร์ชันจริง, โหลดบนเน็ตจริง
- Q3 เปิด gzip/brotli บนโฮสต์ที่ deploy

### งานที่ 15 (S1–S5) — ค้นคว้า (ทำขนานได้ เขียนลง `qa/RESEARCH-S<n>.md` พร้อมลิงก์)

S1 blueprint TGAT1 ปี 2570 (TCAS70) ประกาศหรือยัง · S2 แนวข้อสอบ 2568–2569 (สรุปรูปแบบ ห้ามลอก) · S3 สถิติประเภทคำถาม TC/RC จากแหล่งที่ 2–3 · S4 รายการ idiom ที่ออกบ่อย · S5 ระดับ CEFR ของคำศัพท์ข้อสอบจริงเทียบคลัง A/B/C

---

## 3. gate ใหม่ที่ต้องเพิ่มใน `tests/regression_r3_content.py` (งาน T6)

เพิ่มต่อจากบล็อก RC ที่มีอยู่ (ประมาณบรรทัด 43–56) — โค้ดพร้อมวาง:

```python
# ---- v43 gates (เพิ่มโดย Claude/Arena รอบ v43) ----
# G-A: RC question-type mix ตาม blueprint (ต้องอ่าน type จากสเปก เพราะ vault ไม่เก็บ field type)
import glob as _glob
_rc_types = collections.Counter()
for _f in _glob.glob(os.path.join(ROOT, 'content', 'rc_v43_[a-k].json')):
    for _p in json.load(open(_f, encoding='utf-8')):
        for _it in _p['items']: _rc_types[_it['type']] += 1
check('RC v43: detail เป็นประเภทที่พบบ่อยที่สุด (>=110)', _rc_types['detail'] >= 110, dict(_rc_types))
check('RC v43: words-in-context >= 55 (เป้า 3/15 ข้อ)', _rc_types['wic'] >= 55, _rc_types['wic'])
check('RC v43: มี TRUE/paraphrase/attitude/reference อย่างละ >= 12',
      all(_rc_types[t] >= 12 for t in ('true', 'paraphrase', 'attitude', 'reference')),
      {t: _rc_types[t] for t in ('true', 'paraphrase', 'attitude', 'reference')})

# G-B: RC context-overlap heuristic <= 0.35
_stop = set('the a an of to in for and or is are was were be been with that this it they as at on by from'.split())
def _ov(q, o):
    cw = {w for w in re.findall(r"[a-z']+", q['context'].lower()) if w not in _stop}
    return len({w for w in re.findall(r"[a-z']+", o.lower()) if w not in _stop} & cw)
_hit = sum(max(range(4), key=lambda i: _ov(q, q['options'][i])) == q['answer'] for q in rc)
check('RC: max-context-overlap heuristic <=35% (v43 วัดได้ 51.7%)', _hit / 300 <= 0.35, f'{_hit/300:.3f}')

# G-C: TC answer-longest <= 35% (v43 วัดได้ 42%)
_tcl = sum(len(q['options'][q['answer']]) == max(map(len, q['options'])) for q in tc)
check('TC: key เป็นตัวเลือกยาวสุด <=35% (v43 วัดได้ 42%)', _tcl / 300 <= 0.35, f'{_tcl/300:.3f}')

# G-D: Short conversation context-overlap <= 35% (v43 วัดได้ 67%)
_sh = by['short']
_shl = sum(max(range(4), key=lambda i: _ov(q, q['options'][i])) == q['answer'] for q in _sh)
check('Short conv: context-overlap heuristic <=35% (v43 วัดได้ 67%)', _shl / len(_sh) <= 0.35, f'{_shl/len(_sh):.3f}')
```
> ใส่ทีละ gate ตามงานที่ทำเสร็จ — **อย่าใส่ทั้งหมดทีเดียว** เพราะจะทำให้เทสต์แดงยกชุดและดูไม่ออกว่างานไหนค้าง
> gate G-A ต้องแก้ `/tmp` dependency: ให้ validator กับ gate อ่าน type จาก `content/` เท่านั้น (อย่าอ้าง `/tmp`)

---

## 4. คำสั่งพร้อมใช้ (copy ทั้งบล็อก)

**ติดตั้ง deps ใหม่ทุกครั้งที่ sandbox reset (ไม่ persist):**
```sh
cd /home/user/google_drive/project
pip install cmudict playwright 2>&1 | tail -2
python3 -m playwright install chromium
mkdir -p tools/node_modules && cd tools && npm i axe-core --silent && cd ..
export CHROME=/home/user/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome
export AXE_PATH=tools/node_modules/axe-core/axe.min.js
ls "$CHROME" "$AXE_PATH"
```
> `tests/harness.py` ถูก patch ให้ reads `CHROME` จาก env แล้ว (เก็บไว้ใน git) — อย่า revert
> path chromium อาจเปลี่ยนเลข version: `ls /home/user/.cache/ms-playwright/`

**build + เทสต์เต็มชุด (นาน > 3 นาที ต้องรันแบบ background):**
```sh
cd /home/user/google_drive/project
sh tools/rebuild_all.sh 2>&1 | tail -3
python3 tools/update_registers.py
python3 tests/regression_r3_content.py web
python3 tests/smoke_test.py web
python3 tests/regression_v42.py web
python3 tests/regression_r3_ui.py web
python3 tests/smoke_r3_extra.py web
python3 tests/a11y_audit.py web /tmp/axe.json
python3 tools/check_quotes.py
python3 tools/bias_metrics.py data/vault.json
python3 tools/rc_heuristics.py data/vault.json
```
> ชื่อไฟล์เทสต์ที่ถูกต้อง: `smoke_test.py`, `a11y_audit.py` (ไม่ใช่ smoke.py/a11y.py) · suite เนื้อหา/UI รับอาร์กิวเมนต์ `web` · a11y รับ `web OUT.json`
> `update_registers.py` idempotent (copy จาก `qa/v42.0.1-inherited/DATA-CHANGES.csv` ก่อน append ทุกครั้ง) รันซ้ำได้

**ตรวจสเปก RC ก่อน rebuild:** `python3 tools/check_rc_v43.py`

**แพ็กลง Drive:**
```sh
python3 tools/sync_pack.py /home/user/google_drive/sync_v43 "<ชื่อผู้เขียน>" "<สรุปสั้น>"
# ได้ WORKING-part1..N.zip + MANIFEST.json (part ละ <= 2.8 MB)
# ถ้าต้องการชื่อมี v43 กำกับ: เปลี่ยนชื่อไฟล์ + แก้ name/sha ใน MANIFEST ให้ตรงกัน (ดู commit 61a896c)
```

---

## 5. กับดักที่เจอจริงระหว่างงาน v43 (อ่านก่อนลงมือ — ทุกข้อเกิดขึ้นจริง)

1. **ภาษาไทยที่ AI เขียนเองปนอักษรแปลก** — เจอ 8 จุดในงาน C2: `語`, `인용` (เกาหลี), `自习`, `名词`, `อดี ต`, `up- ` เหลือ, `stok` และเวียดนาม `chứ` ระหว่างงาน C3 → **ต้องรัน char-scan ทุกครั้งหลังเขียน content**
   ```sh
   python3 - << 'PY'
   import re,glob,sys
   ALLOWED=re.compile(r'[\u0E00-\u0E7F\x00-\x7F\u2018\u2019\u201C\u201D\u2013\u2014\u2026\u00E9\u2192]')
   for f in sys.argv[1:]:
       s=open(f,encoding='utf-8').read()
       bad={c:f'U+{ord(c):04X}' for c in set(s) if not ALLOWED.match(c)}
       print(f, bad or 'CLEAN')
   PY
   ```
2. **`edit_file` พังกับ string ผสม script** → ใช้ python `str.replace` + `assert count==1` แทนเสมอ
3. **อ้างข้อความในบทอ่านผิด passage** — เจอ 1 จุด (เขียน reference question อ้างประโยคของอีก passage) → `tools/check_rc_v43.py` เช็คว่าทุก `“…”` ใน prompt/explanation มีจริงใน context · gate `LC/RC: every English quotation in an explanation exists in the item text` ก็จับด้วย
4. **length gate วัดเป็น "ตัวอักษร" ไม่ใช่คำ** · `==` max ถือว่า "ยาวสุด" (เสมอก็นับ) → ต้องให้ตัวลวงยาวกว่า key **อย่างน้อย 1 ตัวอักษร**
5. งาน C3 รอบแรก key ยาวสุด **70%** (gate ≤30%) → ต้องขยายตัวลวง **226 จุด** (168 ให้ key ไม่ยาวสุด + 58 กระจายอันดับสอง) patch เก็บใน `qa/rc_v43_lenpatches/` รันด้วย `python3 tools/apply_rc_v43_len.py <patch.json>` · **เขียนตัวเลือกให้ยาวพอ ๆ กันตั้งแต่แรกจะประหยัดงานมาก**
6. **คู่ตัวเลือกกำกวมต้องห้าม** (gate เดิมจับ): `safe/safer`, `so/so that`, `which/that` เมื่อ key = `that` (ยกเว้นประโยคมี `note (`), `compare with/to`
7. `bankAudit` ใน smoke_test: `structuralCue` (ตัวลวง punctuation เหมือนกันหมดแต่ key ต่าง), `keyLengthOutlier` (คำใน key ≥ max(6, 1.8× ตัวลวงที่ยาวสุด)), `genericDistractor`
8. ตัวเลือกจบด้วย `?` ได้ ถ้าไม่โดน structuralCue
9. **bulk content change ทำให้จำนวนในเทสต์ที่ hardcode เพี้ยน** → `grep -rn "<ตัวเลข>" tests/` หลังแก้ใหญ่ (เคยต้องแก้ 492→436)
10. `xxd` ไม่มีใน sandbox → ใช้ python อ่าน bytes
11. timestamp ใน HANDOFF ต้องเป็นเวลาไทย: `TZ=Asia/Bangkok date '+%Y-%m-%d %H:%M'`
12. **ห้ามแก้ `web/data-*.js`, `data/*.json` ตรง ๆ** — ถูกสร้างใหม่ทุก `rebuild_all.sh`
13. `backups/` = ข้อมูล v42.0.1 ต้นฉบับ ห้ามแก้
14. เทสต์ยาว > 180 วิ ต้องรันแบบ background (start_process) ไม่งั้น timeout
15. `tools/sync_pack.py` เคยแพ็กล้มเหลวเพราะ part ล้น 2.8 MB → แก้แล้วใน commit `61a896c` (headroom 700 KB + retry)

---

## 6. นิยาม "เสร็จ" ของ v43.0.0 (ของ Claude + ส่วนที่ Arena เพิ่ม)

ของ Claude (ใน HANDOFF):
- C1–C7 ✅, V1–V3 ✅ (หรือบันทึกเหตุผลที่ค้าง), T6–T8 ✅
- เทสต์ทุกตัวผ่าน + มีเทสต์ใหม่ทุกการแก้ · ตัวเลขเดาคำตอบทุกกลยุทธ์ ≤35%
- log ครบ: `qa/DATA-CHANGES.csv`, `qa/REVIEW-QUEUE.csv`, `qa/SOURCE-REGISTER.csv`, CHANGELOG, `web/ROUND4-STATUS.md`
- ZIP deploy ห้ามมี qa/ backups/ tools/ tests/ content/ + SHA-256 + ZIP QA แยก
- รายงาน 4 หัวข้อ: แก้แล้ว / automated ผ่าน / ต้องให้มนุษย์ตรวจ / ยังค้าง

Arena เพิ่ม (จากที่วัดได้จริง):
- `rc_heuristics.py`: `max-context-overlap ≤ 0.35`, `combined ≤ 0.40`
- `bias_metrics.py`: `tc.answer_longest ≤ 0.35`, `short.answer_unique_top_context_overlap ≤ 0.35`, extreme-word rate ของ answer กับ distractor ต่างกัน ≤ 1.5 เท่าทุก kind
- RC type mix: wic ≥ 55, detail ≥ 118
- ไม่มี RC passage คู่ไหน word-overlap > 0.25 (แก้ปัญหา near-dup 2 คู่)
- `sync_pack.py` ผ่านในครั้งเดียว (part ≤ 2.8 MB)

---

## 7. ลำดับที่แนะนำ (ถ้าทำคนเดียว เรียงตามความคุ้มค่า)

1. **งานที่ 1** (RC wic 21→60) — เล็ก ชัด ตรง blueprint
2. **งานที่ 3** (TC answer_longest 42%→35%) — เล็ก วัดง่าย เป็นหนี้ที่ Arena ทิ้งไว้
3. **งานที่ 8** (C9 AI review RC/TC) — ขนานได้ ไม่ต้องแก้ไฟล์
4. **งานที่ 2** (RC context-overlap 51.7%→35%) — ใหญ่ ต้องทำทีละ passage
5. **งานที่ 5** (C4 genre ใหม่ + near-dup) — ใหญ่ ต้องเขียน context ใหม่
6. **งานที่ 4** (Short conv) — ต้องสร้าง pipeline ใหม่ทั้งเส้น
7. **งานที่ 6, 7** (Q-R idiom, extremes)
8. **งานที่ 9–12** (V2–V6 คลังศัพท์)
9. **งานที่ 13** (T1–T8 + bump 43.0.0) — ทำท้ายสุด เพราะ bump version ต้องทำหลังจากเนื้อหาหยุดนิ่ง
10. **งานที่ 14–15** (มนุษย์/ค้นคว้า) — ขนานได้ทุกเมื่อ
