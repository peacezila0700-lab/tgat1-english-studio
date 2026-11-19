# TGAT1 English Studio — รายงานตรวจและแก้ไข v41.0.0

**วันที่:** 18 พ.ย. 2026 · **ต้นฉบับ:** `TGAT1-English-Studio-vocab-upgrade-2026-11-18.zip` (v40.9.0) · **ผลลัพธ์:** `TGAT1-English-Studio-v41.0.0.zip`
**ผู้ตรวจ:** Claude (AI) ในบทบาท front-end engineer / QA / บรรณาธิการภาษา — งานเขียนประโยคตัวอย่างใหม่เป็นข้อความที่ AI ร่าง ควรให้คนสุ่มตรวจตามคิวที่แนบ

## 0. สรุปสำหรับผู้บริหาร

| | ต้นฉบับ v40.9.0 | หลังแก้ v41.0.0 |
|---|---|---|
| Vocabulary Lab: ตัวลวงที่มีภาษาอังกฤษปน | 87–90 จาก 90 ช่อง (มีแค่ 6 แบบ) — คำตอบที่ถูกคือข้อเดียวที่เป็นไทยล้วนใน 29–30/30 ข้อ | 0/90 · ตัวลวง 85–86 แบบ · 0/30 ข้อที่เดาได้จากรูปแบบ |
| Vocabulary Lab: ผล SRS หลัง reload | **หายหมด** (บันทึก 0/10) | คงอยู่ 10/10 |
| ความคืบหน้าของคำจาก PACK หลัง reload | หาย 7/107 คำทุกครั้ง | คงอยู่ 107/107 |
| คำแปลหลักที่เป็นคู่ตรงข้าม ("ดีขึ้น - แย่ลง") | 79 | 0 |
| คำแปลหลักที่เป็นประโยคแม่แบบ ("การเปลี่ยนแปลงเกิดขึ้น…ตามรายงาน") | 23 | 0 |
| คำแปลหลักที่มีภาษาอังกฤษปน | 11 (audit เดิมนับ 10 ขาด `may be`) | 0 (ย้ายไปช่อง `note`) |
| แท็กบริบทที่ผิด "(ใช้ในบริบทของ…)" | 26 | 0 |
| ตัวอย่าง meta-language ("The adjective X gives…") | 425 | 0 |
| ตัวอย่างแม่แบบที่ช่องเป็น adj/adv/verb (มักผิดไวยากรณ์) | 538 | 0 |
| ตัวอย่างแม่แบบช่องคำนาม (ส่วนใหญ่ถูกไวยากรณ์แต่กว้าง) | 1,228 | **1,217 — needs human review** |
| คำสะกดผิดในคลังเกมเก่า (สระอำหาย) | 31 ช่อง | 0 |
| ข้อผิดพลาด a11y ระดับ serious (axe-core, 9 route ที่ 390px) | 12 node (สว่าง) + 10 node (มืด) · Lab โหมดมืด: กล่องบริบท 1.04:1 | 0 |
| smoke_test.py เดิม | 49/49 | 49/49 |
| regression_v41.py ใหม่ | ต้นฉบับไม่ผ่าน 12 ข้อ (เนื้อหา 11 + version 1) แล้วหยุดที่ Lab | 49/49 |

**ข้อสำคัญ:** audit เดิมประเมินปัญหาตัวอย่างไว้ที่ 343 แถว การตรวจซ้ำพบว่าตัวอย่างแบบแม่แบบมีราว **2,236 จาก 3,720 sense (≈60%)** แก้ส่วนที่ยืนยันได้ว่าผิดไปแล้ว 963 แถว (meta 425 + ช่องไม่ใช่คำนาม 538) และ 66 แถวในกลุ่มอื่น ยังเหลือ 1,217 แถวช่องคำนามที่ส่งเข้าคิวตรวจโดยคน **ยังไม่ควรประกาศว่าคลังศัพท์ผ่านการตรวจครบ**

## 1. วิธีทำงานและหลักฐาน

- แตก ZIP ลงโฟลเดอร์ใหม่ บันทึก SHA-256 ของต้นฉบับทุกไฟล์ (`qa/SHA256-original-v40.9.0.txt`) และทำงานในสำเนาแยก ไม่แก้ ZIP ต้นฉบับ
- ยืนยันว่า `backups/data.js` และ `backups/data-senses.js` ตรงกับไฟล์หลัก (hash เดียวกัน) ส่วน `backups/app.js` เป็นรุ่นก่อน runtime fix ตามที่ UPGRADE-QA ระบุ — ไฟล์ใน ZIP เป็นชุดเดียวกัน
- **ตรวจข้อมูล "ที่ผู้เรียนเห็นจริง"** โดย dump `STUDIO_DATA` จาก browser หลัง runtime layer ทั้งหมดทำงาน (PACK merge +7 คำ/+119 วลี, sense repair) ไม่ใช่จากไฟล์ดิบอย่างเดียว
- การแก้ข้อมูลทำผ่าน **ตารางแก้รายแถว** (`corrections/*.json` ในโฟลเดอร์ทำงาน) ที่ผ่านการอ่านทีละแถว แล้ว apply ด้วยสคริปต์ที่ตรวจว่า headword ไม่ซ้ำ และบันทึก before/after ทุกฟิลด์ใน `qa/DATA-CHANGES.csv` (3,940 field changes · 1,287 headwords) การ serialize JSON ตรวจแล้วว่า round-trip ได้ไบต์ตรงต้นฉบับ จึงไม่มีการเปลี่ยนส่วนที่ไม่ได้แก้
- regex/POS ใช้เพื่อ**คัดกรอง**เท่านั้น ทุกแถวที่แก้ผ่านการอ่านและเขียนคู่ EN–TH ใหม่ ไม่มี bulk replacement ของเนื้อหาภาษา (ยกเว้นการเปลี่ยนชื่อหมวด 98 แถวซึ่งเป็น metadata และการแก้คำสะกดที่ระบุคำต่อคำ 31 จุด)
- ตรวจด้วยเครื่องมือ: `node --check`, Playwright + Chromium (headless), axe-core 4.14.1

## 2. รายการปัญหา (เรียงตาม priority)

สถานะ: **fixed** = แก้และมีเทสต์ยืนยัน · **verified-no-change** = ตรวจแล้วไม่ต้องแก้ · **needs human review** = ส่งคิวให้คน

### P0 — ทำให้ตอบผิด/เดาได้ หรือข้อมูลผู้เรียนหาย

**P0-1 Vocabulary Lab: คำตอบที่ถูกเดาได้จากรูปแบบ (ไม่อยู่ใน audit เดิม)** — fixed
- ไฟล์: `app.js` โมดูล `v41.0.0 TGAT1 Vocabulary Lab` → `optionsFor()`
- หลักฐาน: `norm()` ตัดทุกอักขระที่ไม่ใช่ `[a-z0-9]` คำแปลไทยทุกคำจึงกลายเป็นสตริงว่างและถูกกรองทิ้ง ตัวลวงที่เหลือจึงมาจากคำแปลที่มีภาษาอังกฤษปนเท่านั้น probe 3 รอบ × 10 ข้อ: ตัวลวงมีอังกฤษ 87/90 ช่อง มีแค่ 6 แบบ คำตอบที่ถูกเป็นตัวเลือกไทยล้วนข้อเดียวใน 29/30 ข้อ (`qa/probes-before-after.log`)
- แก้: ใช้ `meaningKey()` ที่รองรับ Unicode (`\p{L}\p{M}\p{N}`) · ไม่รับคำแปลที่มีอักษรละตินเป็นตัวเลือก · ไม่รับตัวลวงที่มีส่วนความหมาย (แยกด้วย ; , /) ซ้ำกับคำตอบหรือกันเอง เพื่อให้มีคำตอบที่ถูกได้ข้อเดียว · เพิ่ม QA hook แบบอ่านอย่างเดียว `snapshot()` / `_optionsFor()`
- หลังแก้: ตัวลวงอังกฤษ 0/90, 86 แบบ; regression ตรวจ 300 คำ: Thai-only, 4 ตัวเลือกไม่ซ้ำ, ตรงคำตอบ 1 ข้อ, ไม่มีส่วนความหมายซ้ำ, ตัวเลือกไม่ซ้ำกันรวม 587 แบบ
- ความเสี่ยง: ตัวลวงยังสุ่มจากคลังที่ POS เดียวกันก่อน ความหมายใกล้กันแบบไม่มีคำซ้ำ (เช่น ใจดี/มีเมตตา) ยังเป็นไปได้ในทางทฤษฎี

**P0-2 Vocabulary Lab: ผลทบทวน SRS ไม่ถูกบันทึก (ไม่อยู่ใน audit เดิม)** — fixed
- ไฟล์: `app.js` Vocabulary Lab `grade()` เรียก `save()` ที่ไม่ได้ประกาศในโมดูล จึงไปเรียก `const save` ระดับ global ของเกมเก่า (เขียนคีย์ `eng3`) ไม่ได้เขียน `tgat1_studio_vocab_progress_v1`
- หลักฐาน: ทำ Lab 10 ข้อ → reviewLog ในหน่วยความจำ 10, ใน storage `None`, หลัง reload 0 (UPGRADE-QA เดิมรายงาน "เขียน SRS log 10 รายการ" เพราะดูแค่ในหน่วยความจำ)
- แก้: `saveVocab()` ภายในโมดูลเรียก `studioSave('tgat1_studio_vocab_progress_v1', …)` และเพิ่ม `examVocab` ใน whitelist ชนิด session ของ `normalizeVocabState()` (เพิ่มค่าใหม่ ไม่กระทบข้อมูลเดิม)
- หลังแก้: storage 10/10, reload 10/10, session kind `examVocab` คงอยู่ (เทสต์ regression ข้อ "SRS grades survive a reload")

**P0-3 ความคืบหน้าของ 7 คำจาก PACK หายทุกครั้งที่ reload (ไม่อยู่ใน audit เดิม)** — fixed
- ไฟล์: `app.js` การสร้าง `STUDIO_VSTATE` เรียก `normalizeVocabState(..., STUDIO_DATA.words)` ก่อน PACK merge คำที่เพิ่มตอน runtime จึงถูกตัดออก
- หลักฐาน: ตั้งสถานะ 107 คำ PACK → reload เหลือ 100
- แก้: ส่งรายการคำ `STUDIO_DATA.words + pack.words` ให้ normalizer · หลังแก้ 107/107

**P0-4 คำแปลหลัก 23 คำเป็นประโยคแม่แบบ (ไม่อยู่ใน audit เดิม)** — fixed
- `data.js` + `data-senses.js`: เช่น `annually` = "การเปลี่ยนแปลงเกิดขึ้นทุกปีตามรายงาน", `hopefully` = "การเปลี่ยนแปลงเกิดขึ้นหวังว่าตามรายงาน" ซึ่งเป็นคำตอบที่ถูกใน quiz
- แก้: เขียนคำแปล/ความหมาย/ตัวอย่าง/คำแปลตัวอย่างใหม่ทั้ง 23 คำ (G4) + `unhappy`, `untruthful` ที่มีแท็ก "(ใช้กับการจัดการงานหรือเป้าหมาย)"

**P0-5 หมวดคำตรงข้าม: คำแปลหลักเป็นคู่ตรงข้าม 79 คำ (ไม่อยู่ใน audit เดิม)** — fixed
- เช่น `deteriorate` = "ดีขึ้น - แย่ลง", `acquit` = "ตัดสินว่าผิด - ยกฟ้อง" (ครึ่งแรกคือความหมายตรงข้าม), `separate` = "เชื่อม - แยก" คำแปลตัวอย่างเป็นแม่แบบ "บทอ่านเปรียบเทียบคำว่า … (A - B)" และ adj ใช้ "The situation became X after the change."
- แก้ (G1): คำแปลหลักเหลือความหมายของคำนั้น · คู่ตรงข้ามย้ายไป `note` (เช่น "คู่ตรงข้าม: improve (ดีขึ้น) ↔ deteriorate (แย่ลง)") · แก้ POS (`convict`, `construct`, `discard`, `neglect` เดิมเป็น n) · เขียนตัวอย่างใหม่ 47 แถว และคำแปลตัวอย่างใหม่ 79 แถว

### P1 — คุณภาพ/ความถูกต้องสำคัญ

**P1-1 ตัวอย่าง sense แบบแม่แบบ (finding #1 ของ audit เดิม)** — fixed บางส่วน / needs human review บางส่วน
- ตรวจ 3,720 sense ที่ผู้เรียนเห็นจริง จัดกลุ่มด้วยการทำ skeleton ของประโยค แล้วอ่านทีละแถว:
  - Tier A meta-language 425 แถว (รวม `attempt the issue`, `concentrate the issue` ที่ audit ยกตัวอย่าง) → **fixed ทั้งหมด** (G5)
  - Tier B/C ช่อง adj/adv/verb/conj/prep 538 แถว ซึ่งผิดไวยากรณ์หรือผิดความหมายบ่อย (เช่น "The team decided to worsen the plan", "The researchers confer as conditions changed", "The situation changed respectively") → **fixed ทั้งหมด** (G7 + G4)
  - Tier B/C ช่องคำนาม 1,217 แถว ("The researchers discussed X before deciding how to proceed." ฯลฯ) → **needs human review** ส่วนใหญ่ถูกไวยากรณ์แต่ไม่ได้สอนการใช้คำ; 500 แถวเป็น headword วลีที่มักขาด article (เช่น "discussed learning challenge")
  - Tier D 12 แถวที่ไม่พบ headword ตรงตัว → **verified-no-change** ทั้งหมดเป็นรูปผันไม่ปกติที่ถูกต้อง (broke, forgave, lit, misled, underwent, spoke, saw, acquitted …)
- ตัวอย่างใหม่ 1,029 แถว: ตรวจอัตโนมัติว่ามี headword/รูปผันครบทุกแถว (2 แถวเป็นรูปพหูพจน์ของคำประสมที่ถูกต้อง) และใน regression ไม่มีแม่แบบ meta/adj/adv/verb เหลือ
- ความเสี่ยง: เป็นข้อความที่ AI ร่าง แม้อ่านทีละแถว ควรให้คนสุ่มตรวจ 120 แถวที่จัดไว้ในคิว

**P1-2 คำแปลหลักที่มีภาษาอังกฤษปน (finding #2)** — fixed
- พบ 11 ไม่ใช่ 10 (`may be` = "กริยาช่วย + be" ไม่ถูกนับ) · ย้ายข้อเปรียบเทียบไปช่อง `note` ใหม่ที่แสดงในหน้า detail, flashcard และ feedback ของ Lab · คำแปลหลักเป็นไทยล้วน · ตัวเลือก quiz ตรวจแล้ว (P0-1)

**P1-3 หมวด "คำที่มักสับสน" POS ผิดเป็นระบบ** — fixed
- 125 คำ: POS ของ sense เป็น `v` 81 แถว แม้เป็นคำนาม/ตัวกำหนด (`a few`, `much`, `its`, `dessert`) · POS headword ผิด (`during`/`beside` = adj, `put off`/`put out` = adj, `well`/`much`/`its`/`there` = n) · `during` คำแปลขาดเป็น "+ คำนาม) ต่างจาก"
- แก้ (G2) 118 คำ: POS headword + sense, คำแปลไทยสะอาด, ข้อเปรียบเทียบไปที่ `note` · ตัวอย่างเดิมดีอยู่แล้ว คงไว้

**P1-4 POS/polysemy watchlist (finding #3)** — fixed / verified
- `account`, `address`, `claim`, `issue`: เดิมรวมหลาย POS/ความหมายไว้ใน sense เดียว → แยกเป็น 3 sense แต่ละ sense มี POS–ความหมาย–ตัวอย่าง–คำแปลตรงกัน
- `attempt` (+ n), `relative` (n ญาติ / adj สัมพัทธ์ ซึ่งเดิมความหมาย "ญาติ" คู่กับ POS adj), `concentrate` (ตัวอย่างใหม่), `certain` sense 0 → det, `accountability` (ตัวอย่างเดิมใช้ accountable)
- verified-no-change: `destroy`, `employ` (2 sense ถูกแล้ว), `encourage`, `false`, `kind` (adj/n แยกถูกแล้ว), `obscure` (adj/v ถูกแล้ว), `rent` (v/n ถูกแล้ว), `oppose`/`conceal`/`demolish`/`exactly` (คำแปลตัวอย่างของ oppose แก้ใน G1)
- พบเพิ่มระหว่างทาง: `idea`(v→n), `offset`(n→v), `opt for`(n→phr v), `poor`(n→adj), `slight`(v→adj), `upside`(v→n), `rich`(v→adj), `say`(adj→v), `many`(adj→det), `intensify`(adj→v), `sponsor` → fixed

**P1-5 แท็กบริบทปลอมในคำแปล** — fixed (G3)
- 26 คำมี "(ใช้ในบริบทของ…)" ที่ไม่สัมพันธ์กับคำ เช่น `advise` → "สิ่งแวดล้อมหรือธรรมชาติ", `effect` → "กฎหรือหน่วยงาน" · ลบออกจาก `th` และลบฟิลด์ `usage` ที่ถือแท็กเดียวกัน · `maintenance` คำแปลขาด ("การบำรุงรักษ") · `few` วงเล็บไม่ปิด

**P1-6 หมวด "ศัพท์จากโจทย์ GAT รุ่นเก่าฯ" (finding #4)** — fixed
- 90 คำเปลี่ยนเป็น "ศัพท์อ่านขั้นสูง (อ้างอิงแนวข้อสอบเก่า · ไม่ใช่ข้อสอบ TGAT1 ทางการ)" · และ 8 คำที่หมวดขึ้นต้น "TGAT1 Exam Vocabulary · …" เปลี่ยนเป็น "ศัพท์ฝึกแนว TGAT1 (เขียนขึ้นใหม่) · …" · ไม่มีโค้ดอ้างชื่อหมวดเหล่านี้ (ตรวจแล้ว) ข้อมูลผู้เรียนไม่กระทบเพราะ key คือ headword

**P1-7 ที่มา/สิทธิ์ข้อมูล (finding #5)** — needs human review
- `Complete Guide` 1,774 · `TGAT1 curated vocabulary` 1,368 · `เพิ่มใหม่` 358 · editorial 8 (+ วลี 535 รายการจาก 4 ป้าย) ในแพ็กเกจไม่มีหลักฐานที่ระบุผู้จัดทำ/รุ่น/URL/license **ไม่ได้เดา** — ทำ `SOURCE-REGISTER.csv` ระบุ UNVERIFIED และสิ่งที่ต้องขอจากเจ้าของ · IPA: CMUdict (0.7a ขึ้นไปเป็น BSD-2-Clause, รุ่นที่ใช้ไม่ได้บันทึก) และ eSpeak NG (ตัวโปรแกรมเป็น GPL-3.0+; สถานะของ output ให้เจ้าของ/ที่ปรึกษากฎหมายยืนยัน) · UI แสดงป้ายเป็น "ที่มา: …" พร้อม tooltip ว่ายังไม่ยืนยัน
- **คำแนะนำ:** ห้ามเผยแพร่สาธารณะ/แจกจ่ายจนกว่าเจ้าของยืนยันที่มาของ SRC-01..03

**P1-8 headword แบบ grid "โดเมน × คำนาม" ที่ไม่ใช่ collocation จริง** — needs human review
- หมวด "TGAT-focused collocations and expressions" 602 คำ เป็น 18 โดเมน × ~30 คำนาม มีหลายคำที่ไม่ใช่ collocation ในภาษาอังกฤษ เช่น `reading author`, `health sleep`, `learning grammar`, `career salary`, `data increase` · คัดด้วยดุลยพินิจบรรณาธิการได้ 146 คำ (คำที่เป็นธรรมชาติอย่าง public policy, urban design ไม่ถูกนับ) · **ไม่ลบ** ตามข้อกำหนด และเพราะ key ความคืบหน้าผู้เรียนผูกกับ headword

**P1-9 คลังเกมเก่าสะกดผิด** — fixed
- `data.js legacy.V` (ใช้เป็นตัวเลือกในเกมจับคู่): สระอำหาย/คำซ้ำ 31 จุด เช่น `คานวณ`, `จาเลย`, `ทาร้ายร่างกาย`, `โน้มน้ำว`, `มีราคำที่จ่ายไหว`, `ความความเป็นของแท้` → แก้แบบระบุคำต่อคำ (ไม่ใช่ regex กว้าง; `หน้า` ที่ถูกต้องไม่ถูกแตะ)

### P2 — ความเสี่ยง / UX / a11y

**P2-1 Accessibility** — fixed (เท่าที่ตรวจได้อัตโนมัติ)
- เมนูมือถือ: สี `#8a8f99` บนพื้นขาว 3.24:1 (ต่ำกว่า 4.5:1) → `#5f6672` (~5.9:1) และสีเฉพาะโหมดมืด `#aeb6c4`
- โหมดมืด: breadcrumb `#646973` 3.09:1 → `#9aa3b2`
- **Vocabulary Lab โหมดมืด: กล่องบริบท 1.04:1 (แทบมองไม่เห็นตัวอักษร)** เพราะใช้สีพื้นสำรองเป็นสีอ่อน → ใช้พื้นโปร่งแสง
- Hub: ปุ่มหน่วยมี aria-label ที่ไม่ตรงกับข้อความที่มองเห็น (WCAG 2.5.3) → ใช้ข้อความที่มองเห็น + สถานะแบบ screen-reader-only
- หลังแก้: axe-core ไม่มี critical/serious ใน 9 route + Lab ที่ 1280 สว่าง / 390 สว่าง / 390 มืด · keyboard: Tab แรกถึง skip link, Enter ย้าย focus ไป main, focus indicator มองเห็นได้ 12/12, ตอบ Lab ด้วย Enter ได้
- **ข้อจำกัด:** ไม่ได้ทดสอบ screen reader จริง (NVDA/VoiceOver/TalkBack), Safari iOS, Android Chrome จริง หรือการติดตั้ง PWA บนอุปกรณ์ · axe ตรวจได้ราว 30–40% ของเกณฑ์ WCAG

**P2-2 ระดับ A/B/C (finding #6)** — fixed (การแสดงผล) / needs human review (หลักฐาน)
- โค้ดไม่ได้อ้าง CEFR (ตรวจแล้ว) แต่ UI แสดง "ระดับ A" ซึ่งอาจถูกเข้าใจเป็น CEFR · เปลี่ยนเป็น "กลุ่ม A · พื้นฐาน" / "กลุ่มความยาก A · ภายในแอป" พร้อม tooltip และ aria-label ว่าไม่ใช่ CEFR · ระดับต่อ sense ต้องมีแหล่งที่มีสิทธิ์ใช้ (เช่น EVP ต้องตรวจ license) — ไม่ได้ทำ เพราะไม่มีแหล่งข้อมูลรองรับ

**P2-3 ตัวอย่างวลีสนทนา 9 รายการ** — fixed: ตัวอย่างเดิมคือวลีเอง เพิ่มบทสนทนาสั้นให้เห็นบริบท

**P2-4 legacy.V `account`, `figure` มี "account for =" ในคำแปลเกม** — needs human review

**P2-5 Lab ให้ XP แต่ schema ไม่เก็บ `xp`** — needs human review (P3 ในคิว)

### Versioning (finding #7) — fixed
- เลือก **41.0.0** (โค้ด Lab ระบุ v41.0.0 อยู่แล้ว และ release นี้เปลี่ยนข้อมูล/พฤติกรรม) · ปรับ `TGAT1_VERSION` (app/cache/content), `index.html` meta 3 จุด, `manifest.webmanifest`, `sw.js` CACHE_NAME `tgat1-studio-v41.0.0`, header ของ `data.js`/`data-senses.js`/`learning-hub.js`
- ข้อมูลผู้เรียนไม่เสีย: ตรวจแล้วว่า `content` ใช้แค่ประทับลงบน snapshot ไม่มีโค้ดล้างข้อมูลตามเลข version · คีย์ localStorage เดิมทุกตัวคงชื่อ · SW ลบ cache เก่าตอน activate และ pre-cache data-senses/data-vault ใหม่ · `data-vault.js` (คลังข้อสอบ) ไม่เปลี่ยนแม้แต่ไบต์ (hash เดิม)

### ส่วนที่ตรวจแล้วไม่ต้องแก้ (verified-no-change)
- คลังข้อสอบ 1,200 ข้อ ID ไม่ซ้ำ · 20 ชุด × QR10/Short10/Long10/TC15/RC15 · ทุกข้อมี 4 ตัวเลือกไม่ซ้ำ ไม่ว่าง เฉลยถูกช่วง · passage RC อยู่ใน 100–200 คำ (ตาม blueprint MyTCAS ใน brief; ไม่ได้เปิดหน้าเว็บซ้ำ)
- Learning Hub 70 หน่วย เรียงลำดับ ล็อก/resume ถูก · การฝึกศัพท์ไม่นับเป็นคะแนน mock และไม่ทำให้ผ่านหน่วย (มีเทสต์)
- Mock ครบ 60 ข้อให้ 100/100 บน scale /100 · save/resume mock ระหว่างทำ · export (envelope v3 + integrity) / import ผ่าน
- ไม่มี external script/stylesheet · footer ระบุชัดว่าข้อสอบเป็นโจทย์ฝึก ไม่ใช่ข้อสอบทางการ

## 3. ผลทดสอบ (log จริงใน `qa/`)

| ชุดทดสอบ | ผล | log |
|---|---|---|
| `node --check` ทุกไฟล์ JS (7) + manifest JSON | PASS 8/8 | `node-check.log` |
| `smoke_test.py` เดิม (ต้นฉบับ baseline) | 49/49 | `smoke-baseline-v40.9.0.log` |
| `smoke_test.py` เดิม (v41.0.0) | **49/49** | `smoke-final.log` |
| `regression_v41.py` ใหม่ (v41.0.0) | **49/49** | `regression-final.log` |
| `regression_v41.py` กับต้นฉบับ | FAIL 12 ข้อ (เนื้อหา 11 + version 1) แล้วหยุดที่ Lab (ต้นฉบับไม่มี QA hook) | `regression-against-original.log` |
| probe ก่อน/หลังแก้ (ตัวลวง Lab, SRS persistence, PACK progress) | ดูตารางข้อ 0 | `probes-before-after.log` |

regression_v41.py ครอบคลุม: เนื้อหา 14 ข้อ · version · โครงคลังข้อสอบ/blueprint · ตัวเลือก Lab · ค้นหาและ detail · Lab ครบรอบ + SRS + reload · Hub unit vocab ไม่ทำให้ผ่านหน่วย · save/resume · mock เต็มชุด · export/import · 9 route + Lab + detail ที่ 390/1280 ไม่มี overflow/console error · keyboard/focus · offline + PWA cache v41 · axe-core 3 รูปแบบ

## 4. Needs human review — สรุปจำนวน (`qa/REVIEW-QUEUE.csv`, 1,491 แถว)

| priority | หมวด | จำนวน | เหตุผล |
|---|---|---|---|
| P1 | headword-validity | 146 | grid "โดเมน × คำนาม" ที่ไม่ใช่ collocation จริง |
| P1 | source-license | 5 | ป้ายที่มาไม่ระบุแหล่ง/สิทธิ์ (ครอบคลุม 3,508 คำ + 535 วลี) |
| P2 | example-quality | 1,217 | ตัวอย่างแม่แบบช่องคำนาม (500 แถวมักขาด article) |
| P2 | spot-check AI-drafted text | 120 | สุ่ม 120 จาก 1,029 ประโยคที่เขียนใหม่ ให้คนพิสูจน์อักษรคู่ EN–TH |
| P2 | level-evidence | 1 | A/B/C ไม่มีหลักฐาน/ไม่แยกต่อ sense |
| P2 | legacy-gloss | 1 | account/figure ในเกมเก่า |
| P3 | schema | 1 | XP ของ Lab ไม่ถูกเก็บ |

**จำนวนที่ตรวจแล้ว/คงเหลือ (ตัวอย่าง sense):** 3,720 แถวผ่านการคัดกรอง · แก้แล้ว 1,029 แถว · verified-no-change 12 แถว (D) · ส่วนที่ไม่ติดธงอีก 2,462 แถว**ไม่ได้อ่านทีละแถว**ในรอบนี้ (ไม่ติดธงไม่ได้แปลว่าถูกต้อง) · คงเหลือในคิว 1,217 แถว

## 5. ข้อเสนอ (P3)
1. เปลี่ยนตัวอย่าง 1,217 แถวในคิวตามลำดับ: คำที่อยู่ใน Lab/Hub ก่อน (คำที่โยงกับคลังข้อสอบ)
2. ตัดสินใจเรื่อง 146 headword grid: เปลี่ยนเป็น collocation จริงพร้อม migration ของคีย์ความคืบหน้า
3. เก็บ `source` และ `level` ต่อ sense เมื่อได้แหล่งที่มีสิทธิ์ใช้
4. เพิ่ม `regression_v41.py` ใน CI ก่อนทุก release และทดสอบบน iOS Safari / Android Chrome / screen reader จริง
5. พิจารณาให้ Lab เลือก sense ที่ตรงกับบริบทของโจทย์ แทนการใช้ `th` รวมของ headword (สำหรับคำหลายความหมาย)
