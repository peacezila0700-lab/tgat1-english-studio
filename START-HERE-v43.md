# START HERE — v43 (อ่านไฟล์นี้ก่อนเป็นไฟล์แรก)

> เขียนโดย Arena AI · 2026-11-19 16:13 (เวลาไทย) · สำหรับ AI/คน ที่จะมารับงานต่อจาก Arena
> ไฟล์นี้คือ **แผนที่ + วิธีเช็ค + รายการที่ Arena ทำไม่ได้** ส่วนรายละเอียดงานแต่ละข้ออยู่ที่ `qa/V43-NEXT-WORK.md`

---

## 1. สรุปใน 30 วินาที

- โปรเจกต์ = แอปฝึก TGAT1 ภาษาอังกฤษ (web app + คลังข้อมูลข้อสอบ) ปัจจุบัน build เป็นเวอร์ชัน **42.0.2** ยังไม่ bump เป็น 43.0.0
- Arena ทำเสร็จ 4 งาน: **C1** (LC เติมบทสนทนา 100 ข้อ), **C2** (TC เขียนใหม่ 300 ช่อง), **C3** (RC เขียนใหม่ 300 ข้อ), **V1/8a** (headword ปลอม 56 คำ)
- เทสต์เขียวครบทั้งชุด และ rebuild deterministic
- **เหลืองานค้าง 15 รายการ** เรียงลำดับพร้อมคำสั่งใน `qa/V43-NEXT-WORK.md`
- งานที่ควรทำก่อน 3 อัน: (1) RC words-in-context 21→60 ข้อ · (3) TC คำตอบยาวสุด 42%→≤35% · (8) AI review RC/TC (เขียนรายงานอย่างเดียว)

---

## 2. รับไฟล์จาก Drive ยังไง

โฟลเดอร์ `tgat project / TGAT1 v43` (id `1sbaXysMpa4HeFy8KMHhJTCHDM9qIrKZS`)

**ให้ยึด `MANIFEST-v43.json` เป็นความจริงเสมอ** (ข้างในมี `written_at` + ชื่อ/ขนาด/sha256 ของ part ชุดปัจจุบัน) — เพราะทุกครั้งที่แพ็กใหม่ file id กับขนาดจะเปลี่ยน และในโฟลเดอร์มีทั้งชุดเก่าของ Claude (ชื่อไม่มี `v43`) กับชุดที่ trash แล้วปนอยู่

ชุดที่ Arena แพ็กล่าสุด (`written_at` 2026-11-19T16:13+07:00) ประกอบด้วย:
- `WORKING-v43-part1.zip` — โค้ด + `HANDOFF.md` + `START-HERE-v43.md` (ไฟล์นี้)
- `WORKING-v43-part2.zip` — `qa/` ทั้งหมด (รวม `V43-NEXT-WORK.md`), `content/`, ส่วนที่เหลือของ `tools/`
- `WORKING-v43-part3.zip` — `backups/` + `superseded/`
- `MANIFEST-v43.json`, `V43-NEXT-WORK.md` (อัปตัวเดี่ยวไว้ให้อ่านโดยไม่ต้องแตก zip), `START-HERE-v43.md` (ตัวเดี่ยว), `HANDOFF-claude-1256-BACKLOG.md` (BACKLOG ต้นฉบับของ Claude), `ARENA-PROMPT.md`

> `HANDOFF.md` ตัวเดี่ยว **อัปขึ้น Drive ไม่ได้** (security filter ของ connector บล็อกที่เนื้อหา) → อ่านได้จากใน part1 เท่านั้น

```sh
mkdir -p ~/tgat && cd ~/tgat
# ดาวน์โหลด 3 part ลงโฟลเดอร์นี้ แล้ว:
python3 - << 'PY'
import json,hashlib
m=json.load(open('MANIFEST-v43.json'))
for e in m['parts']:
    h=hashlib.sha256(open(e['name'],'rb').read()).hexdigest()
    print(e['name'], 'OK' if h==e['sha256'] else f'MISMATCH {h}')
PY
for z in WORKING-v43-part*.zip; do unzip -oq "$z"; done   # แตกทั้ง 3 part ลงโฟลเดอร์เดียวกัน
ls   # ต้องเห็น HANDOFF.md data/ web/ tools/ tests/ content/ qa/ backups/ superseded/
```
> **อย่าใช้** `WORKING-part1.zip` / `WORKING-part2.zip` / `MANIFEST.json` / `HANDOFF.md` (ไม่มี v43) — เป็นชุดเก่าของ Claude 12:54 เก็บไว้เทียบเท่านั้น
> ในโฟลเดอร์อาจเห็นชื่อไฟล์ซ้ำของตัวที่ trash แล้ว → ยึด **ขนาดไฟล์ตามตาราง** เป็นตัวจริง

---

## 3. แผนที่ไฟล์ — อันไหนคืออะไร เปิดอันไหนก่อน

### อ่านก่อน (เอกสาร)
| ไฟล์ | คืออะไร | อ่านส่วนไหน |
|---|---|---|
| `START-HERE-v43.md` | ไฟล์นี้ | ทั้งไฟล์ |
| `qa/V43-NEXT-WORK.md` | **ใบสั่งงานจริง** — 15 งานค้าง แต่ละข้อมี file path + คำสั่ง + เกณฑ์เสร็จ + กับดัก 15 ข้อ + gate ใหม่ 4 ตัวพร้อมวาง | หัวข้อ 2 (งานค้าง) → 3 (gate) → 4 (คำสั่ง) → 5 (กับดัก) |
| `HANDOFF.md` | กติกาการร่วมงาน + BACKLOG C/V/S/T/Q + บันทึกส่งต่อ (log) | `## กติกา`, `## BACKLOG ทั้งหมด`, `## บันทึกส่งต่อ` (5 รายการล่างสุด = ของ Arena) |
| `qa/R3-BLUEPRINT-ALIGNMENT.md` | เทียบคลังข้อสอบกับ blueprint จริง | ตาราง gaps (gap ที่เหลือ = genre แคบ → งาน C4) |
| `qa/R3-QA-LOG.md` | ปัญหา QA ที่เปิดค้าง | บรรทัด ~63 (near-dup passages, ShortConv overlap) |
| `qa/REVIEW-QUEUE.csv` | งานคลังคำศัพท์ 1,505 แถว (สร้างอัตโนมัติทุก rebuild — **อย่าแก้ด้วยมือ**) | กรองคอลัมน์ `category`/`status` |

### ข้อมูล (ห้ามแก้ตรง ๆ — ถูกสร้างใหม่ทุก build)
| ไฟล์ | คืออะไร |
|---|---|
| `data/vault.json` | **ข้อสอบที่ใช้จริงทั้งหมด** (LC/ShortConv/LongConv/TC/RC/Q-R) — เอาไว้อ่าน/วัดสถิติ |
| `data/data.json` | คลังคำศัพท์ (`studio.words` 3,508 + `studio.phrases` 535, `lazySenses`, `items`, `pack`, `headwordAliases` 56) |
| `web/data.js`, `web/data-vault.js`, `web/data-senses.js` | ข้อมูลที่ build ออกมาให้เว็บใช้ |
| `backups/` | ต้นฉบับ v42.0.1 — **ห้ามแก้ ห้ามลบ** (ใช้ rollback) |
| `superseded/` | สเปก/pipeline เก่าที่ปลดระวางแล้ว (LC comp, TC เก่า, RC pipeline รอบ 3) — เก็บไว้อ้างอิง |

### ตรงที่เขียนงาน (แก้ตรงนี้เท่านั้น)
| ไฟล์ | คืออะไร |
|---|---|
| `content/rc_v43_[a-k].json` | สเปก RC 300 ข้อ (60 passage × 5) — **ไม่มี field `context`** ใช้ context เดิมใน vault; field: `first`, `items[{type,prompt,key,d[3],exp}]` |
| `content/rc_v43_tips.json` | tip ภาษาไทย 9 อัน (เป็น dict ของ string — glob `[a-k]` เท่านั้น ไม่งั้น tool พัง) |
| `content/tc_v43_[a-j].json` | สเปก TC 40 passage/300 ช่อง |
| `content/lc_blank_v43_[e-h].json` | สเปก LC เติมบทสนทนา 20 เรื่อง/100 ข้อ |
| `content/headword_rename_r3.json` | 56 headword ปลอม → collocation จริง |
| `content/headword_triage_r3.json` | dict `{plausible: 46, uncertain: 44}` — headword ที่ต้องคนตัดสิน |

### เครื่องมือ
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `tools/rebuild_all.sh` | build ทั้งเส้น: rebuild_vault.sh (apply_lc_blank → apply_tc_v43 → apply_rc_v43) → headword_rename → vocab_triage → ipa_fill → vocab_dedupe → ipa_stress_fix → `node tools/datafiles.js build data web 42.0.2` |
| `tools/update_registers.py` | เขียน log การเปลี่ยนแปลงลง `qa/DATA-CHANGES.csv`, `qa/changes_r3.jsonl`, `qa/SOURCE-REGISTER.csv` (idempotent รันซ้ำได้) |
| `tools/check_rc_v43.py` | ตรวจสเปก RC ก่อน rebuild (type/quote/อักษรแปลกปลอม) — **Arena แก้ให้ไม่ต้องพึ่ง /tmp แล้ว** (16:13) ถ้าไม่มี `/tmp/rc_passages.json` มันจะดึง context จาก `data/vault.json` เอง |
| `tools/bias_metrics.py data/vault.json` | วัดสัญญาณเดาคำตอบทุก kind (ต้องส่ง path เป็น argv[1] เสมอ ไม่งั้น IndexError) |
| `tools/rc_heuristics.py data/vault.json` | วัดกลยุทธ์เดา RC 5 แบบ + อัตรา extreme-word |
| `tools/check_quotes.py` | ตรวจ quote ในคำอธิบายว่ามีจริงในโจทย์ |
| `tools/apply_rc_v43_len.py <patch.json>` | ยืด/หดตัวเลือก RC (patch ที่ใช้แล้วอยู่ใน `qa/rc_v43_lenpatches/` — **ห้ามรันซ้ำ** มัน assert ว่าเจอข้อความเดิม 1 ครั้ง) |
| `tools/sync_pack.py OUTDIR AUTHOR "note"` | แพ็กลง Drive (part ≤ 2.8 MB + MANIFEST.json) |

### เทสต์ (5 ตัว + a11y)
| ไฟล์ | ตรวจอะไร | ผลล่าสุด |
|---|---|---|
| `tests/smoke_test.py web` | bankAudit + โครงสร้างข้อมูล | 49/49 |
| `tests/regression_v42.py web` | เวอร์ชัน/cache/PWA/gloss | 60/60 |
| `tests/regression_r3_content.py web` | **gate เนื้อหา** (length, ambiguity, type) | 27/27 |
| `tests/regression_r3_ui.py web` | UI | 7/7 |
| `tests/smoke_r3_extra.py web` | เสริม | 94/94 |
| `tests/a11y_audit.py web OUT.json` | axe | `errors: []` · `incomplete` 144 จุด (ต้องคนดู) |
| `tests/harness.py` | ตัวรัน Playwright (patch ให้รับ `CHROME` จาก env แล้ว — **อย่า revert**) | — |

---

## 4. ตั้งเครื่อง + เช็คให้ครบ (copy ทั้งบล็อก รัน ~5 นาที)

```sh
cd <โฟลเดอร์ที่แตก zip>            # เช่น /home/user/google_drive/project
# --- deps (ไม่ persist ใน sandbox ต้องลงใหม่ทุกรอบ) ---
pip install cmudict playwright 2>&1 | tail -2
python3 -m playwright install chromium
mkdir -p tools/node_modules && (cd tools && npm i axe-core --silent)
ls /home/user/.cache/ms-playwright/          # ดูเลข version ของ chromium
export CHROME=/home/user/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome
export AXE_PATH=tools/node_modules/axe-core/axe.min.js
ls "$CHROME" "$AXE_PATH"                     # ต้องมีทั้งสองอัน ไม่งั้น a11y จะข้าม
# --- build + เทสต์ (นานกว่า 3 นาที → รันแบบ background) ---
sh tools/rebuild_all.sh 2>&1 | tail -3
python3 tools/update_registers.py
python3 tools/check_rc_v43.py
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

**ค่าที่ต้องได้ถ้าเครื่องถูก (ตัวเลขของ Arena เมื่อ 16:0x):**
- เทสต์: smoke 49/49 · v42 60/60 · r3_content 27/27 · r3_ui 7/7 · extra 94/94 · a11y errors `[]`
- `check_rc_v43.py`: `11 files, 300 items` + type mix `detail 120, paraphrase 25, true 25, attitude 25, reference 24, wic 21, inference 21, purpose 21, main 18` → `ALL CLEAN`
- `rc_heuristics.py`: longest 0.200 · no-topic+longest 0.200 · no-extreme+longest 0.283 · **max-context-overlap 0.517** · combined 0.537
- `bias_metrics.py`: rc.answer_longest 0.200 · **tc.answer_longest 0.420** · **short.context_overlap 0.670** · qr.answer_longest 0.285

> ตัวเลขที่ **ตัวหนา** = ปัญหาที่ยังไม่แก้ (เป้า ≤0.35) — ดูรายละเอียดวิธีแก้ใน `qa/V43-NEXT-WORK.md` งานที่ 2, 3, 4

---

## 5. สิ่งที่ Arena ทำไม่ได้ / ยังค้าง — พร้อมเหตุผล

### 5.1 ข้อจำกัดของเครื่องมือ/สภาพแวดล้อม (แก้ไม่ได้ด้วยโค้ด)
1. **อัป `HANDOFF.md` ตัวเดี่ยวขึ้น Drive ไม่ผ่าน** — connector provider บล็อกด้วย security filter ที่ *เนื้อหา* (ลอง 1 ครั้ง ไม่ผ่าน) ·Arena ไม่ลองซ้ำและไม่ดัดแปลงเนื้อหาเพื่อเลี่ยงฟิลเตอร์ → ผลคือ HANDOFF รุ่น v43 (56,972 B, merge BACKLOG ครบ) **อยู่ใน `WORKING-v43-part1.zip` เท่านั้น** ใครอยากอ่านแบบไม่ต้องแตก zip ก็อ่านไม่ได้ · ไฟล์อื่น (`V43-NEXT-WORK.md`, `START-HERE-v43.md`) อัปปกติ
2. **git ไม่ได้ push และ `.git` ไม่ได้อยู่ใน zip** — GitHub connector ไม่รองรับ และ PAT ที่ผู้ใช้ให้มาใช้ไม่ได้ (ผู้ใช้สั่งพักเรื่อง GitHub ไว้) → ประวัติ commit 6 ตัว (`c8499e4`→`72ce543`) **หายไปสำหรับผู้รับงานต่อ** เหลือแค่ข้อความ log ใน `HANDOFF.md` ท้ายไฟล์ (Arena เขียน log ละเอียดไว้แทนแล้ว) · `sync_pack.py` แพ็กเฉพาะไฟล์งาน ไม่รวม `.git`
3. **deps ไม่ persist** — `cmudict`, `playwright`+chromium, `tools/node_modules/axe-core` ต้องลงใหม่ทุก sandbox reset · ไม่มี `xxd` · ถ้าไม่ตั้ง `AXE_PATH` เทสต์ `regression_v42.py` จะรายงาน 59/59 แล้วข้าม axe (ดูเผิน ๆ เหมือนผ่าน)
4. **ไฟล์ scratch ใน `/tmp` หายไป** (`rc_typeplan.json`, `rc_passages.json`, log เทสต์) — Arena แก้ `tools/check_rc_v43.py` ให้สร้าง context จาก `data/vault.json` เองแล้ว (16:13) เหลือแค่ **แผน type ต่อ passage** ที่ไม่มี → gate ใหม่ G-A ใน `qa/V43-NEXT-WORK.md` หัวข้อ 3 เขียนให้อ่าน type จาก `content/` แทน `/tmp` แล้ว (อย่ากลับไปอ้าง `/tmp`)
5. **เทสต์ยาวเกิน 180 วินาที** ต้องรันแบบ background/process tool ไม่งั้นโดน timeout กลางคัน
6. **ไฟล์ 9 ไฟล์หายไปจากโฟลเดอร์ Drive ระหว่างที่ Arena อัป** (ไม่ทราบสาเหตุ ผู้ใช้ยืนยันว่าไม่มี agent อื่นทำงานพร้อมกัน) → กฎ: **`search_files`/`list` ใหม่ทุกครั้งก่อนแก้หรือลบ** อย่ายึด id ที่บันทึกไว้เก่า

### 5.2 งานที่ Arena เริ่มแล้วแต่ไม่จบ (มีเหตุผลเชิงเวลา/ขอบเขต)
7. **RC context-overlap 51.7% (งาน C7)** — ไม่ได้แก้ เพราะต้องรื้อตัวเลือกทีละ passage (60 passage) และเสี่ยงทำให้ข้อ detail/reference กำกวม ต้องทำแบบค่อย ๆ วัด · นี่คืองานใหญ่สุดของ RC
8. **TC คำตอบเป็นตัวเลือกลองสุด 42% (หนี้ที่ Arena สร้างเองในงาน C2)** — เกิดจากใส่ collocation ยาว (`take pride in`, `a wide range of`) เป็นคำตอบ ขณะที่ตัวลวงเป็นคำเดี่ยว · ยังไม่แก้ และ **ยังไม่มี gate ตัวไหนจับ** (gate ยาวสุดมีแค่ LC/RC) → ต้องเพิ่ม gate G-C
9. **RC words-in-context เหลือ 21 ข้อ (เป้า 60)** — Arena เลือกเติมประเภทที่คลังไม่มีเลยก่อน (TRUE/paraphrase/attitude/reference) จึงเบียดโควตา wic · ตารางเป้าที่ให้ใหม่อยู่ใน `qa/V43-NEXT-WORK.md` งานที่ 1 (รวม 300 พอดี)
10. **RC passage เกือบซ้ำ 2 คู่ ยังอยู่** (`S14-Q056`↔`S20-Q051` เรื่องประหยัดพลังงานบ้าน, `S07-Q046`↔`S16-Q046` เรื่องของหาย) — ไม่ได้แก้เพราะสเปก RC **ไม่มี field `context`** (ใช้บทเดิมใน vault) การเปลี่ยนบทอ่าน = ต้องเขียน 5 ข้อของ passage นั้นใหม่ทั้งชุด + แก้ `tools/apply_rc_v43.py` ให้เขียน context + รักษาความยาว 100–200 คำ → เป็นงาน C4
11. **Short Conversation ยังไม่มี pipeline สเปกเลย** — งาน C1/C2/C3 มี `content/*.json` + `tools/apply_*.py` แต่ ShortConv 200 ข้อแก้ได้ทางเดียวคือแก้ vault ตรง ๆ ซึ่งผิดกติกา → ต้องสร้างเส้นใหม่ (ดูแบบจาก `tools/apply_tc_v43.py`) รวมถึง tag ใหม่ใน `tools/update_registers.py`
12. **Q-R idiom: นับได้ 3 ข้อ ไม่ใช่ 21 ข้อ** — เอกสารของ Claude ระบุ 21/200 แต่ regex สำนวนสามัญของ Arena เจอ 3 → **ยังไม่ได้ตัดสินว่าวิธีนับไหนถูก** (ขึ้นกับว่านับอะไรเป็น idiom) Arena เลยตั้งเป้าแบบ absolute ≥60 และให้ทำรายการสำนวนไว้ให้แล้ว
13. **ยังไม่ bump เป็น 43.0.0 (งาน T7)** — ตั้งใจไม่ทำ เพราะ `42.0.2` กระจายอยู่ 12 ไฟล์ รวมทั้ง `tests/regression_v42.py:18 EXPECT_VERSION` กับ cache namespace `tgat1-studio-v42.0.2` ใน `web/sw.js` ต้องเปลี่ยนพร้อมกันไม่งั้นเทสต์แดงยกชุด · และควร bump **หลัง**เนื้อหาหยุดนิ่ง (ไม่งั้นต้อง bump หลายรอบ)

### 5.3 งานที่ AI ห้ามทำ/ห้ามอ้างว่าผ่าน (ต้องคนหรืออุปกรณ์จริง)
14. Q1 screen reader (VoiceOver/TalkBack/NVDA) + WCAG ด้วยมือ + axe `incomplete` 144 จุด · Q2 iOS Safari / Android Chrome / ติดตั้ง PWA / โหลดบนเน็ตจริง · Q3 gzip/brotli บนโฮสต์ · T5 Lighthouse/Web Vitals (ไม่เคยรัน)
15. **คลังคำ V2 (772 ตัวอย่างที่ต้องคนเขียนใหม่) + 83 คำ IPA ที่ต้องคนฟัง** — เป็นงานตัดสินเชิงภาษาที่ AI เคยพลาดซ้ำ (งานนี้ Arena เจออักษรจีน/เกาหลี/เวียดนามปนในข้อความที่ตัวเองเขียน 8+ จุด) → ถ้า AI เขียน ต้องมี AI อีกตัวตรวจ (งาน C9) และมนุษย์ spot-check

### 5.4 ความผิดพลาดที่ Arena ทำไว้ระหว่างทาง (บันทึกกันพลาดซ้ำ)
- เขียนข้อความไทยปนอักษรแปลก 8 จุดในงาน C2 (`語`, `인용`, `自习`, `名词`, `อดี ต`, `stok`) และปนเวียดนาม `chứ` + คำไทยผิด (`เครื่องดิ่ม`, `ไม่สัญญาลผลเดียวกัน`) ในงาน C3 → **ตอนนี้แก้หมดแล้ว** แต่ต้องมี char-scan ทุกครั้ง (สคริปต์อยู่ใน `qa/V43-NEXT-WORK.md` กับดักข้อ 1)
- เขียน reference question อ้างประโยคของ passage อื่น 1 จุด → แก้แล้ว และเพิ่มการเช็คใน `tools/check_rc_v43.py`
- งาน C3 รอบแรก key ยาวสุด 70% (gate ≤30%) → ต้องขยายตัวลวง 226 จุด เก็บ patch ไว้ใน `qa/rc_v43_lenpatches/` (รันซ้ำไม่ได้)
- `tools/sync_pack.py` แพ็กล้มเหลวเพราะ part ล้น 2.8 MB (`qa/DATA-CHANGES.csv` บีบแล้ว 511 kB) → แก้แล้วใน commit `61a896c` (headroom 700 kB + retry ×0.8) **อย่า revert**

---

## 6. ข้อความสั่งงานสำเร็จรูป (copy ไปวางให้ AI ที่รับงานต่อ)

**แบบ A — ทำงานที่ 1 (RC wic 21→60):**
```
อ่าน START-HERE-v43.md แล้วตามด้วย qa/V43-NEXT-WORK.md งานที่ 1
งาน: เพิ่ม RC ประเภท words-in-context จาก 21 → 60 ข้อ (3/15) โดยคง detail ไว้ 120
ตามตารางเป้าในไฟล์นั้น ห้ามแตะ data/ หรือ web/data*.js ตรง ๆ แก้ที่ content/rc_v43_[a-k].json
จากนั้น: python3 tools/check_rc_v43.py → sh tools/rebuild_all.sh → เทสต์ 5 ตัว + a11y
→ python3 tools/update_registers.py → เพิ่ม gate G-A ใน tests/regression_r3_content.py
→ เขียน log ท้าย HANDOFF.md (เวลาไทย) → commit
รายงาน 4 หัวข้อ: แก้แล้ว / automated ผ่าน / ต้องให้มนุษย์ตรวจ / ยังค้าง
```

**แบบ B — ทำงานที่ 3 (TC answer_longest 42%→≤35%):**
```
อ่าน START-HERE-v43.md + qa/V43-NEXT-WORK.md งานที่ 3
งาน: ลดสัดส่วนที่คำตอบ TC เป็นตัวเลือกยาวที่สุด (วัดเป็นจำนวนตัวอักษร) จาก 42% → ≤35%
แก้ที่ content/tc_v43_[a-j].json (ยืดตัวลวงหรือหด key) ระวังคู่กำกวมต้องห้ามกับ bankAudit
เพิ่ม gate G-C ใน tests/regression_r3_content.py แล้วรันเทสต์ครบชุด + update_registers + log + commit
```

**แบบ C — ทำงานที่ 8 (C9 AI review — รายงานเท่านั้น):**
```
อ่าน START-HERE-v43.md + qa/V43-NEXT-WORK.md งานที่ 8
งาน: ตรวจ RC 300 ข้อ (ก่อน แล้วค่อย TC 300) หา คำตอบถูก 2 ข้อ / ไม่มีคำตอบถูก /
ภาษาไม่ธรรมชาติ / คำอธิบายไทยผิด / ตัวลวงผิดไวยากรณ์ชัด
ห้ามแก้ไฟล์ข้อสอบ ให้เขียนรายงาน qa/AI-REVIEW-RC-<sets>.md รูปแบบตาราง
| id | ปัญหา | หลักฐาน | ข้อเสนอแก้ |
```

---

## 7. กติกาห้าม (สั้น ๆ — ฝ่าฝืนแล้วงานพัง)

1. ห้ามแก้ `data/*.json`, `web/data*.js` ตรง ๆ (build ใหม่ทับทุกครั้ง) — แก้ที่ `content/` แล้ว rebuild
2. ห้ามแตะ `backups/`
3. ห้ามรันซ้ำ `qa/rc_v43_lenpatches/rc_lenpatch1..7.json`
4. ทุกครั้งที่แก้สเปก RC → รัน `python3 tools/check_rc_v43.py` + char-scan
5. bulk content change → `grep -rn "<ตัวเลข>" tests/` เพราะจำนวนในเทสต์ hardcode (เคยต้องแก้ 492→436)
6. log ทุกการแก้: `update_registers.py` + บันทึกท้าย `HANDOFF.md` เป็นเวลาไทย (`TZ=Asia/Bangkok date '+%Y-%m-%d %H:%M'`) + git commit
7. แพ็กส่ง Drive ด้วย `tools/sync_pack.py` แล้ว **ตั้งชื่อไฟล์ให้มี `v43`** + ทำให้ name/sha ใน MANIFEST ตรงกับชื่อจริง
8. AI ห้ามอ้างว่าผ่านงานที่ต้องคน/อุปกรณ์จริง (Q1–Q3, IPA 83 คำ, Lighthouse)
