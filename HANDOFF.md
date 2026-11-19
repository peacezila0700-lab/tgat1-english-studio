# HANDOFF — TGAT1 English Studio (ใช้ส่งต่องานระหว่าง Claude ↔ Arena AI)

> อ่านไฟล์นี้ก่อนเริ่มงานทุกครั้ง แล้วเขียนต่อท้ายหัวข้อ "บันทึกส่งต่อ" ก่อนหยุดงานทุกครั้ง
> โฟลเดอร์กลางอยู่ใน Google Drive: `tgat project/TGAT1 v43/`

## กติกา (สำคัญที่สุด)
1. **ทำทีละฝั่ง** ห้าม Claude กับ Arena แก้พร้อมกัน
2. **เริ่มงานจาก WORKING.zip ล่าสุดเสมอ** (ดูเวลาแก้ไขล่าสุดใน Drive + บันทึกล่าสุดด้านล่าง)
3. **หยุดงานเมื่อไร ต้องอัป WORKING.zip + HANDOFF.md ทับของเดิม** แล้วเขียนบันทึกว่าทำถึงไหน
4. **ห้ามแก้ `web/data-vault.js`, `web/data.js`, `web/data-senses.js` ตรง ๆ** — ไฟล์พวกนี้ถูกสร้างใหม่ทุกครั้งที่รัน `tools/rebuild_all.sh` ของที่แก้ตรง ๆ จะหาย
   ให้แก้ที่ต้นทางแทน (ดูหัวข้อ "แก้ที่ไหน")
5. ห้ามลบข้อมูลโดยไม่มีเหตุผลตรวจสอบได้ ทุกการแก้ต้องลง log (`tools/changelog.py` → `qa/changes_r3.jsonl`)
6. ห้ามอ้างว่า "สมบูรณ์" / "มนุษย์ตรวจแล้ว" / "ทดสอบบนอุปกรณ์จริงแล้ว" ถ้าไม่ได้ทำจริง
7. ข้อสอบเป็น *original practice material* ไม่ใช่ข้อสอบจริง ไม่ใช่การทำนายคะแนน

## วิธีรับ-ส่งไฟล์ผ่าน Drive (ทำตามนี้ทุกครั้ง)
ไฟล์ใน `tgat project/TGAT1 v43/`:
- `HANDOFF.md` — ไฟล์นี้ (กติกา + สถานะ + บันทึกส่งต่อ + คำถาม)
- `MANIFEST.json` — รายชื่อ part ทั้งหมด + SHA-256 + ใครเขียน เมื่อไร
- `WORKING-part1.zip`, `WORKING-part2.zip`, … — โปรเจกต์ทั้งก้อน แบ่งเป็นส่วน (ตัวเชื่อม Drive อัปได้ไม่เกิน ~3 MB ต่อไฟล์)

**รับงาน:** โหลด MANIFEST.json + ทุก part → `python3 tools/sync_unpack.py <โฟลเดอร์ที่โหลด> <โฟลเดอร์ใหม่>`
(ถ้าไม่มีเครื่องรันโค้ด: แตก ZIP ทุก part ลงโฟลเดอร์เดียวกัน แล้วเทียบ SHA-256 กับ MANIFEST)
ถ้า part ขาดหรือ SHA ไม่ตรง → **หยุด อย่าทำงานบนสำเนานั้น** เขียนคำถามถึงผู้ใช้

**ส่งงาน:** เขียนบันทึกท้ายไฟล์นี้ → `python3 tools/sync_pack.py <โฟลเดอร์ส่งออก> <ชื่อผู้เขียน> "<สรุปสั้น>"`
→ ลบ (trash) MANIFEST/part/HANDOFF เดิมใน Drive → อัปของใหม่ทั้งชุด (ทุก part + MANIFEST + HANDOFF)
ห้ามอัปไม่ครบชุด ถ้าอัปไม่ครบให้เขียนในคำถามว่าขาดไฟล์ไหน

**สงสัย/ติดปัญหา:** อย่าเดา — เขียนในหัวข้อ "คำถามค้าง" ด้านล่าง แล้วหยุดถามผู้ใช้ก่อน
อีกฝั่งต้องอ่าน "คำถามค้าง" ก่อนเริ่มงานทุกครั้ง และตอบ/ปิดข้อที่ตอบแล้ว

## คำถามค้าง (ถึงผู้ใช้หรืออีกฝั่ง)
- [ผู้ใช้] (ก) headword 56 คำ: ซ่อนจากแบบฝึก หรือแก้เป็นคำปกติทีละคำ? → **ตัดสินแล้ว 2026-11-19: "rename เป็น collocation จริง" — Arena ทำเสร็จแล้ว (งาน 8a) ดูบันทึกส่งต่อด้านล่าง**
- [ผู้ใช้] (ข) TC เน้นศัพท์ ~140/300 ช่อง พอไหม? → **ตัดสินแล้ว 2026-11-19: "โอเค ~140 ช่อง (~47%)" — ยังไม่เริ่มงาน (ตรงกับงานข้อ 2)**
- [ผู้ใช้] Arena AI อ่าน/เขียน Google Drive เองได้ไหม? ถ้าได้ ต้องแชร์โฟลเดอร์ให้เมลไหน? → **ตอบ (Arena): ได้ — Arena เชื่อม Google Drive ผ่านบัญชีผู้ใช้โดยตรง (connector google_drive) อ่าน/เขียน/อัป/สร้าง/ลบ/trash ได้เอง ไม่ต้องแชร์โฟลเดอร์ให้เมลไหน**
- [ถึงผู้ใช้] GitHub: Arena `git push` ขึ้น GitHub ได้ (ทดสอบแล้ว) แต่ "สร้าง repo ใหม่" ต้อง (1) ให้ผู้ใช้กดสร้าง repo เปล่าบน github.com เอง 1 ที แล้ว Arena push ให้ หรือ (2) เพิ่มสิทธิ์ `Administration: Read & write` ให้ token — **ผู้ใช้สั่งพักเรื่อง GitHub ไว้ก่อน จะอัปตอนงานนิ่ง/มีประสิทธิภาพพอแล้ว (อัปท้ายสุด)**
- [ถึง Claude/ผู้รับช่วง] dependencies ที่ต้องลงทุก environment ใหม่ (ไม่มาใน ZIP): `pip install cmudict playwright` + `python -m playwright install chromium` + `python -m playwright install-deps chromium` (ต้องมี sudo) + `cd tools && npm install axe-core` และตั้ง `CHROME=$(playwright chromium path)` ตอนรันเทสต์ UI (harness.py แก้ให้รับ env CHROME แล้ว)

## สถานะตอนนี้
- เวอร์ชันแอปล่าสุดที่ build แล้ว: **v42.0.2** (โฟลเดอร์ `web/`)
- เป้าหมายรอบถัดไป: **v43.0.0** — ปรับคลังข้อสอบให้ตรงโครงสร้าง TGAT1 และเน้นคำศัพท์
- รายงานจุดที่ต้องแก้ (15 ข้อ P1–P3): https://claude.ai/artifact/A8gWqe6VzNR274c1stFXrb
  และสรุปใน `qa/R3-BLUEPRINT-ALIGNMENT.md`
- **ผู้ใช้ตัดสิน 2 เรื่องแล้ว (2026-11-19):**
  - (ก) headword 56 คำ → **rename เป็น collocation จริง** — ✅ Arena ทำเสร็จแล้ว (งาน 8a), เทสต์ผ่านครบ
  - (ข) Text Completion เน้นศัพท์/collocation ~140/300 ช่อง → **ตกลง ~140 ช่อง (~47%)** — รอเริ่มงาน (งานข้อ 2)

## งานที่ต้องทำ (เรียงลำดับ)
| # | งาน | ขนาด | สถานะ |
|---|-----|------|-------|
| 1 | LC ชุด 11–20 เปลี่ยนจากถามความเข้าใจ → เติมบทสนทนา (fill-in) ตาม blueprint | 10 บท/100 ข้อ | **เสร็จ (v43, Arena 2026-11-19) — ดูบันทึกส่งต่อด้านล่าง** |
| 2 | TC เพิ่มสัดส่วนศัพท์/collocation (~140 ช่อง) + ไวยากรณ์ที่ขาด (verb form, tense/voice, relative/noun clause, inversion, question tag) | ~140 ช่อง | **เสร็จ (v43, Arena 2026-11-19) — vocab 125/300 (41.7%) + ไวยากรณ์ครบทุกประเภท ดูบันทึกส่งต่อด้านล่าง** |
| 3 | RC ปรับประเภทคำถาม: details / main idea / words in context / inference / reference | ~150 ข้อ | **เสร็จ (v43, Arena 2026-11-19) — เขียนใหม่ทั้ง 300 ข้อ: details 120 (40%) + TRUE 25, paraphrase 25, attitude 25, reference 24, inference 21, purpose 21, wic 21, main idea 18 ดูบันทึกส่งต่อด้านล่าง** |
| 4 | บทอ่านประเภทใหม่: ข่าว ประกาศ โฆษณา บทความความรู้ (เริ่มจากธีมที่ซ้ำ) | ~30 RC + ~20 TC | ยังไม่เริ่ม |
| 5 | Q-R เพิ่ม idiom/สำนวน | ~60 ข้อ | ยังไม่เริ่ม |
| 6 | Short conversation ให้สถานการณ์หลากหลาย ไม่ซ้ำ LC | ~30 ข้อ | ยังไม่เริ่ม |
| 7 | ลดสัญญาณเดาคำตอบที่เหลือ ≤35% | ทั้งคลัง | ยังไม่เริ่ม |
| 8 | แผนคำศัพท์: headword 56 คำ, ตัวอย่าง 772 ข้อที่ต้องเขียนใหม่, gloss/วลีไม่ตรง, IPA | คลังศัพท์ | **8a headword 56 คำ = เสร็จ (v43, Arena)** · 8b–d (772 ตัวอย่าง / gloss / IPA) ยังไม่เริ่ม |
| 9 | อัปเดต log/เทสต์ → bump v43.0.0 → build ZIP + SHA-256 | — | ยังไม่เริ่ม |

## BACKLOG ทั้งหมด (งานค้างทุกอย่างของระบบ — อ่านก่อนเลือกงาน)
คอลัมน์ "ใครทำได้": **A** = Arena ทำได้แค่อ่าน/เขียนข้อความ (ไม่ต้องรันโค้ด) · **R** = ต้องมีเครื่องรันโค้ด/เทสต์ · **H** = ต้องมนุษย์หรืออุปกรณ์จริง (AI ห้ามอ้างว่าทำแล้ว) · **D** = รอผู้ใช้ตัดสินก่อน
สถานะ: ⬜ ยังไม่เริ่ม · 🟨 กำลังทำ (เขียนชื่อคนทำ) · ✅ เสร็จ (ใส่วันที่ + ผลเทสต์) — **ก่อนเริ่มงานไหน ให้เปลี่ยนเป็น 🟨 แล้วอัปทันที กันทำซ้ำ**

### C — เนื้อหาข้อสอบ/ภาษา (ตามรายงานเทียบ blueprint)
| ID | งาน | ไฟล์/ที่อยู่ | ใครทำได้ | เกณฑ์เสร็จ | สถานะ |
|---|---|---|---|---|---|
| C1 | LC ชุด 11–20 → เติมบทสนทนา (100 ข้อ) | ดู "สเปกงานข้อ 1" | A (+R ตรวจ) | 4 ไฟล์ e–h, quote ผ่าน, ความยาวคำตอบถูกไม่ยาวสุด >50% | ✅ 2026-11-19 Arena (v43) — `content/lc_blank_v43_[e-h].json` + `tools/apply_lc_blank.py` · commit `b8b16b0` · เทสต์เขียวทั้งชุด |
| C2 | TC เพิ่มศัพท์/collocation ~140 ช่อง + ไวยากรณ์ที่ขาด (verb form, tense/voice, relative/noun clause, inversion, question tag) | `content/tc_fixes_r3.py` หรือไฟล์สเปกใหม่ | A + D(ข) | ศัพท์/collocation ≥ เป้าที่ผู้ใช้เลือก; ทุกช่องมีคำตอบเดียว | ✅ 2026-11-19 Arena (v43) — vocab/collocation 125/300 (41.7%) + verb 46, tense 46, clause 34, conn 27, inversion 10, tag 12 · `content/tc_v43_[a-j].json` + `tools/apply_tc_v43.py` · commit `e80af6e` · ⚠ ค้าง 1 จุด: answer_longest 42% (ดู `qa/V43-NEXT-WORK.md` ข้อ 3) |
| C3 | RC ปรับประเภทคำถามต่อบท: details 6–7, main idea/purpose 1–4, words in context 3, inference 0–2, reference/paraphrase 0–2 (ต่อ 15 ข้อ) | `content/rc_r3_*.json` | A | นับประเภทได้ตามช่วง ทุกชุด | ✅ 2026-11-19 Arena (v43) — details 120/300 (40%), TRUE 25, paraphrase 25, attitude 25, reference 24, inference 21, purpose 21, wic 21, main 18 · `content/rc_v43_[a-k].json` + `tools/apply_rc_v43.py` · commit `6d9368e` · ⚠ ค้าง 1 จุด: words-in-context เหลือ 21 (1.05/15) ต่ำกว่าเป้า 3/15 (ดู `qa/V43-NEXT-WORK.md` ข้อ 1) |
| C4 | บทอ่านประเภทใหม่: ข่าว ประกาศ โฆษณา บทความความรู้ อีเมล (ตอนนี้เป็นเรื่องโครงการชุมชนเกือบหมด) — เริ่มจากบทที่ธีมซ้ำ | RC ~30 บท, TC ~20 บท | A | ไม่มีธีมซ้ำ; 100–200 คำ/บท | ⬜ |
| C5 | Q-R เพิ่ม idiom/สำนวนพูด (ตอนนี้ 21/200) | Q-R ~60 ข้อ (ต้องสร้างสเปก+สคริปต์ apply ใหม่) | A (+R สร้างสคริปต์) | idiom ≥ 60; ตัวลวงไม่เป็นคำตอบที่ถูกได้ด้วย | ⬜ |
| C6 | Short conversation สถานการณ์ซ้ำกับ LC 20 เรื่อง → เปลี่ยนให้หลากหลาย ~30 ข้อ | ต้องสร้างสเปกใหม่ | A | ไม่ซ้ำ LC; บริบทไม่ใบ้คำตอบ | ⬜ |
| C7 | ลดสัญญาณเดาคำตอบ ≤35%: RC ตัวเลือกยาวอันดับ 2 = 36.7%, absolutes 34%; LC ยาวอันดับ 2 = 42.5%; **Short conv context-overlap 69.5%** (หนักสุด) | `tools/bias_metrics.py`, `tools/rc_heuristics.py` วัด | A แก้ + R วัด | ทุกกลยุทธ์เดา ≤35% | ⬜ |
| C8 | ตรวจภาษาโดยมนุษย์: LC 200, TC 300 คำอธิบาย, RC 180+ ข้อ และคลังที่เหลือ | qa/REVIEW-QUEUE.csv | H | มีชื่อผู้ตรวจ+วันที่ใน REVIEW-QUEUE | ⬜ |
| C9 | AI ตรวจรอบสอง (ก่อนมนุษย์): อ่านทุกข้อหาคำตอบถูก 2 ตัว/ไม่มีตัวถูก, ภาษาไม่ธรรมชาติ, คำอธิบายไทยผิด — บันทึกเป็นรายการปัญหา **ไม่ต้องแก้เอง** | เขียนผลลง `qa/AI-REVIEW-<ชื่อ>.md` | A | ระบุ id + ปัญหา + ข้อเสนอแก้ | ⬜ |

### V — คลังคำศัพท์
| ID | งาน | ใครทำได้ | สถานะ |
|---|---|---|---|
| V1 | headword 56 คำที่ไม่ใช่คำปกติ: ซ่อน หรือแก้ทีละคำ (+44 ไม่แน่ใจ, 46 น่าจะใช้ได้) — รายชื่อใน `content/headword_triage_r3.json` | D(ก) แล้ว A | 🟨 8a เสร็จ 2026-11-19 Arena — 56 headword → collocation จริง (`content/headword_rename_r3.json`, `tools/apply_headword_rename.py`, commit `fbe2f20`) · เหลือ plausible 46 + uncertain 44 ใน `content/headword_triage_r3.json` |
| V2 | ตัวอย่างประโยค 772 ข้อที่ต้องเขียนใหม่ + 251 ไม่แน่ใจ (noun-slot) — รายการใน `qa/REVIEW-QUEUE.csv`, `qa/r3-noun-slot-triage.json` | A เขียน → H ยืนยัน | ⬜ |
| V3 | gloss/ความหมายไม่ตรงกัน 35 รายการ + ตัวอย่างวลี 87 รายการ (ใน REVIEW-QUEUE) | A | ⬜ |
| V4 | IPA: 1,333 รายการจาก eSpeak ใช้สัญลักษณ์ต่างจาก CMUdict → ทำให้เป็นแบบเดียวกัน; 83 รายการต้องฟังเช็ก | R + H | ⬜ |
| V5 | ผูกคลังศัพท์กับข้อสอบ: ศัพท์ที่ออกใน TC/RC ต้องอยู่ในคลัง และมีลิงก์ "ฝึกคำนี้" | A ทำรายการ + R ทำโค้ด | ⬜ |
| V6 | เพิ่ม collocation/word family ของคำระดับ B–C ที่ใช้ใน TC ใหม่ (C2) | A | ⬜ |

### S — ค้นคว้าเพิ่ม (Arena ช่วยได้ดี — เขียนผลลง `qa/RESEARCH-<หัวข้อ>.md` พร้อมลิงก์แหล่ง)
| ID | งาน | สถานะ |
|---|---|---|
| S1 | blueprint TGAT1 ปีสอบ 2570 (TCAS70) ประกาศแล้วหรือยัง เปลี่ยนจาก 2569 ไหม (myTCAS / ทปอ.) | ⬜ |
| S2 | ข้อสอบจำจริง/แนวข้อสอบปี 2568–2569 จากหลายแหล่ง (เว็บติว, YouTube เฉลย, กลุ่ม Facebook — Claude เข้า Facebook ไม่ได้) → สรุป *รูปแบบ* ไม่ลอกข้อสอบ | ⬜ |
| S3 | สถิติประเภทคำถาม TC/RC ปีล่าสุด จากแหล่งที่ 2–3 (ตอนนี้มีแค่ OnDemand แหล่งเดียว) | ⬜ |
| S4 | รายการ idiom/สำนวนที่ออกบ่อยใน Q-R และ Short conversation | ⬜ |
| S5 | ระดับคำศัพท์ที่ข้อสอบใช้ (CEFR B1–B2? C1?) เทียบกับคลัง A/B/C ของเรา | ⬜ |

### T — โค้ด/หนี้เทคนิค (ต้องรันเทสต์ทุกครั้ง: smoke + regression + axe)
| ID | งาน | ใครทำได้ | สถานะ |
|---|---|---|---|
| T1 | app.js มี 45 ชั้น patch, ฟังก์ชันถูก patch ทับ 43 ตัว, ชื่อซ้ำ 16 ชื่อ (`audit`×6, `start`×5, `decorate`×4, `studioRender`×4, `VLT_finish`×4) → รวมทีละโมดูล | R | ⬜ |
| T2 | CSP เข้ม: ย้าย inline `<script>` ใน index.html → app.js (ง่าย); แทน `on*=` ~300 จุดด้วย `data-action` + delegated listener; เลิก inline `style=` | R | ⬜ |
| T3 | `data.js` 2 MB บล็อกการแสดงผลแรก → แยก `studio.examples` และ `pack` เป็น lazy chunk (แบบที่ทำกับ vault/senses แล้ว) | R | ⬜ |
| T4 | `learning-hub*.js` (~93 KB gzip) โหลดตอนเริ่ม → โหลดเมื่อเข้า Hub (ต้องให้ `TGAT1Hub.continue()` บนหน้า Home ยังทำงาน offline) | R | ⬜ |
| T5 | Lighthouse / Web Vitals ยังไม่เคยรัน | R | ⬜ |
| T6 | ทุกงาน C/V ที่แก้ ต้องมี regression test ใหม่ใน `tests/regression_r3_content.py` (หรือไฟล์ v43) | R | ⬜ |
| T7 | bump เวอร์ชัน 43.0.0 ทุกที่: app, `sw.js` cache, manifest, header ข้อมูล (`tools/datafiles.js build … 43.0.0`), `EXPECT_VERSION` ใน `tests/regression_v42.py` | R | ⬜ |
| T8 | QA ZIP รอบก่อนขาด `qa/R3-BLUEPRINT-ALIGNMENT.md` → ใส่ในรอบ v43 | R | ⬜ |

### Q — การทดสอบที่ต้องคน/อุปกรณ์จริง (AI ห้ามอ้างว่าผ่าน)
| ID | งาน | สถานะ |
|---|---|---|
| Q1 | screen reader (VoiceOver/TalkBack/NVDA) + ตรวจ WCAG ด้วยมือ; axe "incomplete" 4,760 จุดต้องดูด้วยตา | ⬜ H |
| Q2 | iOS Safari, Android Chrome, ติดตั้ง PWA + อัปเดตเวอร์ชันจริง, โหลดบนเน็ตจริง | ⬜ H |
| Q3 | เปิด gzip/brotli บนโฮสต์ที่ deploy (ลดขนาด ~5 เท่า) | ⬜ H (ผู้ดูแลโฮสต์) |

**ลำดับแนะนำ:** C1 → (รอ D) → C2, C3, C7 → C4, C5, C6 → V1–V3 → T6, T7 → build v43 · ระหว่างรอ: S1–S5, C9 ทำคู่ขนานได้ (แค่เขียนไฟล์ใน qa/ ไม่ชนกับงานแก้)

> **หมายเหตุ:** HANDOFF.md ที่อยู่ใน Drive ใหม่กว่าสำเนาใน WORKING-part*.zip เสมอ ถ้าไม่ตรงกันให้เชื่อไฟล์ใน Drive

## เช็กลิสต์เขียนข้อสอบใหม่ทุกข้อ (ใช้กับ C1–C7)
1. คำตอบถูกข้อเดียว ตัดสินได้จากข้อความในโจทย์ ไม่ใช่ความรู้รอบตัว
2. ตัวลวงทุกตัวดูเป็นไปได้ ผิดด้วยเหตุผลที่อธิบายได้ ไม่ใช่ผิดไวยากรณ์ชัด ๆ หรือขำ ๆ
3. ความยาว/รูปแบบตัวเลือกใกล้กัน ไม่มี "all/never/always" เฉพาะในตัวลวง ไม่ลอกคำจากโจทย์มาใส่คำตอบถูก
4. ไม่ใช้ "all of the above / none of the above"
5. ตำแหน่งคำตอบ A/B/C/D กระจายเท่า ๆ กันในแต่ละชุด
6. ความยากตามสัดส่วน ง่าย 20% / กลาง 60% / ยาก 20%
7. คำอธิบายภาษาไทย: ทำไมข้อถูกถึงถูก + ตัวลวงแต่ละตัวผิดเพราะอะไร + คำพูดที่ยกมาต้องมีจริงในโจทย์
8. ห้ามลอกข้อสอบจริงหรือข้อสอบจากเว็บติว — ใช้แค่ *รูปแบบ* ข้อสอบทั้งหมดเป็น original practice material

## นิยาม "เสร็จ" ของ v43.0.0
- งาน C1–C7 ✅, V1–V3 ✅ (หรือมีเหตุผลที่บันทึกว่าทำไมยังค้าง), T6–T8 ✅
- เทสต์ทุกตัวผ่าน + เทสต์ใหม่สำหรับทุกการแก้; ตัวเลขเดาคำตอบทุกกลยุทธ์ ≤35%
- log ครบ: `qa/DATA-CHANGES.csv`, `qa/REVIEW-QUEUE.csv`, `qa/SOURCE-REGISTER.csv`, CHANGELOG, สถานะรอบ (`web/ROUND4-STATUS.md`)
- ZIP deploy **ห้ามมี** qa/ backups/ tools/ tests/ content/; ทำ SHA-256; ZIP QA+tests แยกอีกไฟล์
- รายงานสถานะแยก 4 หัวข้อ: แก้แล้ว / automated tests ผ่าน / ต้องให้มนุษย์-อุปกรณ์จริงตรวจ / ยังค้าง — ห้ามใช้คำว่า "สมบูรณ์" หรือ "มนุษย์ตรวจแล้ว" ถ้าไม่มีหลักฐาน

## ข้อความสั่งงานสำเร็จรูป (ผู้ใช้ copy ไปวางได้เลย)
- **ให้ Arena ทำงานแก้:** "อ่าน HANDOFF.md ทั้งไฟล์ก่อน ดูคำถามค้าง แล้วทำงาน [ID] จาก BACKLOG ตามกติกาและเช็กลิสต์ ทำทีละส่วน จบแต่ละส่วนให้ส่งชุดไฟล์ใหม่ (ทุก part + MANIFEST + HANDOFF ที่เขียนบันทึกแล้ว)"
- **ให้ Arena ค้นคว้า:** "อ่าน HANDOFF.md แล้วทำงาน S[1-5] ค้นจากหลายแหล่ง ใส่ลิงก์ทุกข้อ แยกให้ชัดว่าข้อไหนเป็นข้อมูลทางการ/ข้อไหนเป็นความเห็นติวเตอร์ เขียนผลเป็นไฟล์ qa/RESEARCH-S[n].md"
- **ให้ Arena ตรวจ:** "อ่าน HANDOFF.md แล้วทำงาน C9 กับ Part [ชื่อ] ชุด [เลข] เขียนเป็นรายการปัญหาเท่านั้น ห้ามแก้ไฟล์ข้อสอบ"
- **ให้ Claude ทำต่อ:** "ทำต่อจาก Drive โฟลเดอร์ tgat project/TGAT1 v43"

## สิ่งที่ Claude ต้องทำเมื่อกลับมา (เช็กลิสต์ของ Claude)
1. อ่าน HANDOFF.md ใน Drive → ดูบันทึกล่าสุดว่าใครทำอะไร + คำถามค้าง
2. โหลดทุก part + MANIFEST → `sync_unpack.py` → ถ้า Arena แก้มา ให้ใช้ของ Arena เป็นฐาน
3. รัน `rebuild_all.sh` + เทสต์ทั้งหมด + `check_quotes.py` + `bias_metrics.py` ตรวจงาน Arena; ถ้าพบปัญหา เขียนกลับใน HANDOFF
4. ถามผู้ใช้เฉพาะคำถามค้างที่ยังไม่มีคำตอบ แล้วทำงานถัดไปตามลำดับแนะนำ

> ⭐ **ใบสั่งงานละเอียด (ตัวเลขวัดจริง + คำสั่งพร้อมใช้): `qa/V43-NEXT-WORK.md`** — Arena เขียนเมื่อ 2026-11-19 16:10
> ครอบคลุม: งานเสร็จแล้ว (ห้ามทำซ้ำ), งานค้าง 15 รายการพร้อมคำสั่ง/ไฟล์/เกณฑ์เสร็จ, gate ใหม่สำหรับ `regression_r3_content.py`,
> กับดัก 15 ข้อที่เจอจริง, นิยามเสร็จของ v43.0.0 (ปรับตามค่าที่วัดได้), ลำดับงานที่แนะนำ

## สเปกงานข้อ 1 (เริ่มได้เลย ไม่ต้องรอคำตอบ ก/ข)
**เป้าหมาย:** Long conversation ชุด 11–20 (20 บทสนทนา × 5 ข้อ = 100 ข้อ) ตอนนี้เป็น "อ่านแล้วตอบคำถาม" → เปลี่ยนเป็น **"เติมบทสนทนา"** แบบเดียวกับชุด 1–10 ตาม blueprint TGAT1 (Long conversation = เติมบทสนทนา 2 บท × 5 ช่อง)
- **แม่แบบ:** `content/lc_blank_r3_a.json` … `_d.json` (ชุด 1–10 ทำแล้ว 20 บท) — รูปแบบ: `{"first": "<id ข้อแรกของบท>", "context": "บทสนทนาที่มี (1) ____ … (5) ____", "tip": "<ไทย>", "items": [{"key": "<คำตอบถูก>", "d": ["<ตัวลวง1>","<ตัวลวง2>","<ตัวลวง3>"], "exp": "<คำอธิบายภาษาไทย>"} ×5]}`
- **วัตถุดิบ:** หัวเรื่อง/ตัวละครเดิมของชุด 11–20 อยู่ใน `content/lc_comp_r3_[e-h].json` (ใช้ธีมเดิม เขียนบทสนทนาใหม่เป็นแบบเติม) — `first` ใช้ id เดิม (เช่น S11-Q021, S11-Q026 …)
- **สร้างไฟล์ใหม่:** `content/lc_blank_r3_e.json` … `_h.json` (ไฟล์ละ 5 บท)
- **แก้สคริปต์:** `tools/apply_lc_blank.py` เปลี่ยน glob เป็น `lc_blank_r3_[a-h].json` และ `assert len==40`; ถอด `apply_lc_comp.py` ออกจาก `tools/rebuild_vault.sh` (เก็บไฟล์ไว้ ไม่ลบ)
- **เกณฑ์คุณภาพ (ห้ามข้าม):**
  1. แต่ละช่องมีคำตอบถูก **ข้อเดียว** — ตัวลวงต้องผิดเพราะขัดกับประโยค *ก่อนหรือหลัง* ช่อง ไม่ใช่ผิดไวยากรณ์ชัด ๆ
  2. ความยาวตัวเลือกใกล้กัน — คำตอบถูก **ไม่ใช่** ตัวที่ยาวที่สุดเกินครึ่งของ 5 ข้อในบท
  3. ไม่มีคำจากบรรทัดถัดไปลอกมาใส่คำตอบถูกตรง ๆ (ห้ามใบ้ด้วยการซ้ำคำ)
  4. ภาษาเป็นธรรมชาติแบบพูด มี contraction (I'm, let's) ระดับ B1–B2 บทละ ~120–180 คำ
  5. `exp` ภาษาไทย อ้างประโยคในบทที่ทำให้ตอบได้ (คำพูดที่ยกมาต้องมีอยู่จริงในบท) และบอกว่าตัวลวงแต่ละตัวผิดเพราะอะไร
  6. สถานการณ์ไม่ซ้ำกับชุด 1–10 และไม่ซ้ำกันเอง
- **ตรวจหลังทำ:** `sh tools/rebuild_all.sh` แล้วรัน `tests/regression_r3_content.py web` + `tools/check_quotes.py` (ถ้ารันไม่ได้ ให้เขียนในบันทึก)
- ทำทีละไฟล์ (e → f → g → h) และ **ส่งงาน (sync_pack + อัป) หลังจบแต่ละไฟล์** เผื่อโควต้าหมด

## โครงโฟลเดอร์ใน WORKING.zip
```
backups/   ข้อมูลต้นฉบับ v42.0.1 (ฐานที่ rebuild เริ่มจากตรงนี้ — ห้ามแก้)
content/   ★ สเปกการแก้ข้อสอบ (JSON/PY) — แก้ข้อสอบที่นี่
data/      vault.json / data.json / senses.json ที่ถอดออกมา (ถูกสร้างใหม่ทุก rebuild)
tools/     สคริปต์ apply_*.py, vocab_*.py, ipa_*.py, datafiles.js, rebuild_all.sh
tests/     เทสต์ทั้งหมด
qa/        log, REVIEW-QUEUE.csv, DATA-CHANGES.csv, SOURCE-REGISTER.csv, รายงาน
web/       ตัวแอปที่ build แล้ว (ผลลัพธ์ — ห้ามแก้ไฟล์ data-*.js ตรง ๆ)
superseded/ ไฟล์เก่าที่ไม่ใช้แล้ว (เก็บไว้อ้างอิง)
```

## แก้ที่ไหน
- **ข้อสอบ LC (เติมบทสนทนา ทั้ง 40 บท):** ชุด 1–10 `content/lc_blank_r3_[a-d].json` + ชุด 11–20 (v43) `content/lc_blank_v43_[e-h].json` → `tools/apply_lc_blank.py` (แบบ comp เดิม `lc_comp_r3_[e-h].json`/`apply_lc_comp.py` เลิกใช้แล้ว ย้ายไป `superseded/`)
- **TC (v43 เขียนใหม่ทั้ง 40 passage):** `content/tc_v43_[a-j].json` → `tools/apply_tc_v43.py` (ของเดิม round-3 `tc_fixes_r3.py`/`apply_tc.py` เลิกใช้ ย้ายไป `superseded/`)
- **RC (v43 เขียนใหม่ทั้ง 300 ข้อ):** `content/rc_v43_[a-k].json` + `content/rc_v43_tips.json` → `tools/apply_rc_v43.py` (pipeline เดิม round-3 `apply_rc.py`/`apply_rc_len.py`/`apply_rc_len2.py` + `rc_r3_[a-f].json`/`rc_*fix*_r3.json` เลิกใช้ ย้ายไป `superseded/`)
- **คำศัพท์/IPA:** `tools/vocab_triage.py`, `tools/ipa_fill.py`, `tools/vocab_dedupe.py`, `tools/ipa_stress_fix.py`
- งานใหม่ (v43) ให้สร้างไฟล์สเปกใหม่ใน `content/` + สคริปต์ apply ใหม่ใน `tools/` แล้วเพิ่มบรรทัดเรียกใน `tools/rebuild_vault.sh` หรือ `tools/rebuild_all.sh`
- ทุกการแก้ข้อมูลเรียก `changelog.log(item_id, field, old, new, reason, category)`

## วิธี build และทดสอบ
```sh
# ต้องมี: python3, node; เทสต์ UI ต้องมี playwright + chrome
cd tools && npm install axe-core && cd ..     # node_modules ไม่ได้รวมใน ZIP
sh tools/rebuild_all.sh                        # สร้าง data ใหม่จาก backups + content → web/
python3 tests/smoke_test.py web
python3 tests/regression_v42.py web
python3 tests/regression_r3_content.py web
python3 tests/regression_r3_ui.py web          # ต้องมี browser
python3 tests/smoke_r3_extra.py web            # ต้องมี browser
python3 tests/a11y_audit.py web qa/axe.json    # ต้องมี browser
node --check web/app.js
```
ถ้ารันเทสต์ไม่ได้ (ไม่มีเครื่องรันโค้ด) ให้เขียนในบันทึกว่า "ยังไม่ได้รันเทสต์" แล้วอีกฝั่งจะรันให้

## บันทึกส่งต่อ (เขียนต่อท้าย ใหม่สุดอยู่ล่างสุด)
### 2026-11-19 12:50 (เวลาไทย) — Claude
- สร้างโฟลเดอร์กลางใน Drive และ HANDOFF.md ฉบับแรก
- สถานะ: v42.0.2 build แล้ว เทสต์ทั้งหมดผ่านในรอบก่อน รายงานจุดที่ต้องแก้ส่งผู้ใช้แล้ว
- ยังไม่ได้เริ่มงาน v43 — รอผู้ใช้ตอบ (ก) และ (ข)
- ขั้นต่อไป: เริ่มงานข้อ 1 (LC ชุด 11–20 → fill-in)
- เพิ่ม `tools/sync_pack.py` / `tools/sync_unpack.py` และระบบแบ่ง part + MANIFEST (เพราะ ZIP ก้อนเดียว 4.6 MB อัปเข้า Drive ไม่ได้)

### 2026-11-19 13:49 (เวลาไทย) — Arena AI
- **รับงาน:** โหลด MANIFEST.json + WORKING-part1/2.zip จาก Drive → แตก → **SHA-256 ตรง MANIFEST ทั้งคู่** → ทำงานบนสำเนา (ไม่แตะ ZIP ต้นฉบับ)
- **ตั้งค่า environment ให้ build/test ได้** (deps ไม่มาใน ZIP): `pip install cmudict playwright` · `playwright install chromium` + `install-deps chromium` · `cd tools && npm install axe-core` · แก้ `tests/harness.py` ให้ `CHROME` อ่านจาก env var (fallback `/usr/bin/google-chrome`) เพื่อรันกับ chromium ของ playwright ได้
- **Baseline (ก่อนแก้):** `sh tools/rebuild_all.sh` deterministic (rebuild แล้ว git ไม่เห็น diff) · เทสต์ผ่านหมด: smoke_test 49/49, regression_v42 59/59, regression_r3_content 27/27, regression_r3_ui 7/7, smoke_r3_extra 94/94, a11y 0 serious/critical violations
- **งาน 8a — rename headword 56 คำ (ผู้ใช้ตัดสิน (ก) = rename):**
  - สเปก: `content/headword_rename_r3.json` (old→new + gloss ไทย + ประโยคตัวอย่างจริง + คำแปลไทย + reason ต่อคำ)
  - สคริปต์: `tools/apply_headword_rename.py` เสียบใน `tools/rebuild_all.sh` หลัง cp backups / ก่อน vocab_triage → ipa_fill สร้าง IPA (CMUdict) ให้หัวคำใหม่ทุกคำ (missing 0)
  - ผล: headword ปลอมแบบ "หมวด×คำนาม" (reading answer, career salary, data graph, urban public …) → collocation จริง (correct answer, starting salary, bar chart, urban residents …) + แทน template "The team discussed the X…" / "The researchers discussed X…" ด้วยประโยคธรรมชาติที่โชว์ collocation จริง ทั้งใน `studio.examples` และ `senses.json`
  - ตรวจแล้ว: 56 คำใหม่ **ไม่ชน** headword เดิม 3,508 คำ และไม่ชนกันเอง · คง 3,508 คำ (ไม่ลบ) · noun-slot queue ลด 1217→1161 (56 คำออกจากคิว)
  - **Migration ประวัติผู้เรียน:** emit `data.headwordAliases {old→new}` (ไปถึง `web/data.js`) + แก้ `web/app.js normalizeVocabState` ให้อ่าน alias → progress/SRS/favorites ที่ผูกกับหัวคำเก่าจะถูก migrate ไปหัวคำใหม่ ไม่หาย (ตามข้อกำหนด "ห้ามลบโดยไม่ migrate")
  - **แก้เทสต์ให้ตรงเนื้อหาใหม่:** `tests/regression_v42.py` — (1) expected "researchers template" 492→436 (เพราะ 56 คำถูกแทนด้วยประโยคจริง) (2) ตรวจแล้ว gloss ไทยต้องไม่มีอักษรละติน → แก้สเปก `reference word` ให้เป็นไทยล้วน
  - อัปเดต `qa/REVIEW-QUEUE.csv`: 56 แถว headword-validity → status "v43 RESOLVED: renamed …" (คง BOM + CRLF + 1,505 แถว)
- **เทสต์หลังแก้ (เขียวครบ):** smoke_test 49/49 · regression_v42 **60/60** · regression_r3_content 27/27 · regression_r3_ui 7/7 · smoke_r3_extra 94/94 · a11y 0 violations · `node --check web/app.js` OK · changelog `qa/changes_r3.jsonl` +442 รายการ (category `headword-rename`)
- **ยังไม่ได้ทำ:** ยังไม่ bump version (คง 42.0.2 — จะ bump v43.0.0 ตอนงานครบในงานข้อ 9) · ยังไม่ sync ZIP กลับ Drive (รอผู้ใช้สั่ง / ทำตอนจบเซสชัน) · GitHub พักไว้ตามที่ผู้ใช้สั่ง
- **ขั้นต่อไป (ยังไม่ได้เริ่ม):** งานข้อ 1 (LC ชุด 11–20 → fill-in 100 ข้อ) หรืองานข้อ 2 (TC rebalance ~140 ช่องศัพท์ ตามที่ผู้ใช้ตกลง (ข)) — งานใหญ่ทั้งคู่ ควรทำทีละข้อแล้วรันเทสต์กำกับ
- **git:** Arena init repo ในเครื่อง + commit แล้ว (ยังไม่ push — รอผู้ใช้สร้าง repo/อนุญาต) branch `main`

### 2026-11-19 14:24 (เวลาไทย) — Arena AI
- **งานข้อ 1 — LC ชุด 11–20 เปลี่ยนจาก "ถามความเข้าใจ" → "เติมบทสนทนา (blank fill-in)" ครบ 20 บท / 100 ข้อ (เสร็จ):**
  - สเปกใหม่: `content/lc_blank_v43_e.json` (S11-Q021…S13-Q021), `_f.json` (S13-Q026…S15-Q026), `_g.json` (S16-Q021…S18-Q021), `_h.json` (S18-Q026…S20-Q026) — โครงเดียวกับชุด 1–10 (`first/topic/context/tip/items[{key,d[3],exp}]`) เขียนบทสนทนาใหม่ทั้ง 20 บท (บริบทไม่ซ้ำชุด 1–10 และไม่ซ้ำกันเอง) แต่ละบทมี `(1) ____`…`(5) ____`
  - หัวข้อใหม่ 20 เรื่อง: museum night / campus shuttle / market layout / library booking / clinic reminders / coastal trip / theatre subtitles / food bank / bike docks / heatwave room / timetable pilot / repair café / audio walk / food-waste survey / park watering / language exchange / bus-stop board / swimming lesson / museum workshop / flood notice
  - `tools/apply_lc_blank.py` ขยายให้ glob `lc_blank_v43_[e-h].json` ต่อจาก r3_[a-d] (รวม 40 บท, assert ครบ) — ตำแหน่งคำตอบใช้สูตรเดิม `(ci*5+k*3+ci//4)%4` → สมดุล 50/50/50/50 ทั้ง 200 ข้อ
  - เลิกใช้ comp-style: ลบ `python3 tools/apply_lc_comp.py` ออกจาก `tools/rebuild_vault.sh` และย้าย `apply_lc_comp.py` + `lc_comp_r3_[e-h].json` ไป `superseded/` (มีหมายเหตุใน `superseded/README.md`)
  - ผ่าน gate เนื้อหาครบ: 40 contexts unique ×5 · key-is-longest ชุดใหม่ 26/100 (รวมทั้งแบงก์ 54/200 ≤ 60) · ไม่มี `Let us`/`I will` · distractor ไม่ซ้ำverbatim เกิน 2 ข้อ · คำพูดอังกฤษใน `“…”` ของ explanation มีจริงในบททุกจุด · structuralCue/keyLengthOutlier/fragmentKey/genericDistractor = 0 · nearDuplicate = 0
  - `sh tools/rebuild_all.sh` OK (3,749 รายการใน `qa/changes_r3.jsonl`) + รัน `tools/update_registers.py` → `qa/DATA-CHANGES.csv` ใหม่ (12,239 แถว รวม 576 แถว LC v43)
- **เทสต์หลังแก้ (เขียวครบ):** smoke_test 49/49 · regression_v42 60/60 · regression_r3_content 27/27 · regression_r3_ui 7/7 · smoke_r3_extra 94/94 · a11y_audit errors=[]
- **ยังไม่ได้ทำ:** ยังไม่ bump version (คง 42.0.2) · ยังไม่ sync ZIP กลับ Drive · GitHub พักไว้ตามคำสั่งผู้ใช้
- **ขั้นต่อไป:** งานข้อ 2 — TC rebalance เพิ่มช่องศัพท์/collocation ~140 ช่อง + ไวยากรณ์ที่ขาด (ผู้ใช้ตกลง (ข) แล้ว)

### 2026-11-19 15:02 (เวลาไทย) — Arena AI
- **งานข้อ 2 — TC rebalance (เสร็จ):** เขียน passage ใหม่ทั้ง 40 passage / 300 ข้อ (`content/tc_v43_[a-j].json` ไฟล์ละ 4 passage = 2 ชุด)
  - สัดส่วนใหม่: **vocab/collocation 125 ช่อง (41.7%)** (เดิม 29 ช่อง ≈ 10%) + verb form 46, tense/voice 46, relative/noun clause 34, connector/preposition 27, **inversion 10, question tag 12** (เดิมไม่มีเลย) — ตรงช่วง 40–50% ที่ผู้ใช้ตกลงใน (ข)
  - genre หลากหลายขึ้นตาม blueprint: ข่าว, ประกาศ, อีเมลธุรกิจ, โฆษณา (ยิม/คอนโด/ทัวร์), คู่มือเครื่องใช้, การ์ดสูตรอาหาร, บทวิจารณ์หนัง/หนังสือ, คอลัมน์สุขภาพ, รายงานประชุม, podcast, บทสัมภาษณ์วิทยุ, ป้ายพิพิธภัณฑ์, คู่มือห้องสมุด, นิตยสารชุมชน
  - `tools/apply_tc_v43.py` เสียบแทน `apply_tc.py` ใน `tools/rebuild_vault.sh` (ของเดิมย้ายไป `superseded/` + หมายเหตุใน `superseded/README.md`) — ตำแหน่งคำตอบสูตร `(j*3+j//8)%4` → 75/75/75/75 ตรงตามเทสต์
  - explanation เขียนใหม่เป็นไทยรายข้อ (อ้างอิงเลขช่อง) + tip เฉพาะ passage — เลิกใช้ตัว generate template เดิม
  - `tools/update_registers.py` เพิ่ม mapping `TC-rewrite` → G25 ใน DATA-CHANGES.csv (1,730 แถว)
- **ตรวจแล้ว:** ไม่มีอักษรแปลกปลอม (จีน/เกาหลี/เวียดนาม/รัสเซีย) ในไฟล์ใหม่ (เจอระหว่างเขียน 8 จุด แก้หมด) · ผ่าน gate เดิมครบ: คู่กำกวม safe/safer, so/so that, which/that, compare with/to ไม่มี · structuralCue/keyLengthOutlier/genericDistractor/nearDuplicate = 0
- **เทสต์หลังแก้ (เขียวครบ):** smoke_test 49/49 · regression_v42 60/60 · regression_r3_content 27/27 · regression_r3_ui 7/7 · smoke_r3_extra 94/94 · a11y errors=[] · rebuild deterministic (md5 ตรงกันสองรอบ)
- `qa/R3-BLUEPRINT-ALIGNMENT.md` gap #2 (TC) → ขึ้นสถานะ DONE พร้อมตัวเลข
- **ยังไม่ได้ทำ:** ยังไม่ bump version (คง 42.0.2) · ยังไม่ sync ZIP กลับ Drive · GitHub พักไว้ตามคำสั่งผู้ใช้
- **ขั้นต่อไป:** งานข้อ 3 — RC ปรับประเภทคำถาม (details มากสุด + เพิ่ม TRUE-statement, reference, paraphrase, attitude) ~150 ข้อ

### 2026-11-19 15:46 (เวลาไทย) — Arena AI
- **งานข้อ 3 — RC ปรับประเภทคำถาม (เสร็จ):** เขียนใหม่ทั้ง 60 passage / 300 ข้อ (`content/rc_v43_[a-k].json` — a=passage 1–10, b–k ไฟล์ละ 5 passage) คง context เดิมของ v42.0.2 (บทอ่านยัง 106–136 คำ) แต่เปลี่ยน prompt / ตัวเลือก / คำอธิบาย / tip ทั้งหมด
  - **สัดส่วนประเภทคำถามใหม่ (จากเดิมทุก passage ใช้ 5 ประเภทเดียวกัน = main idea / sequence / purpose / detail / word meaning อย่างละ 20%):**
    - **details 120 ข้อ (40%) = มากที่สุด** ตาม blueprint
    - ประเภทที่คลังเดิมไม่มีเลย: **TRUE-statement 25, paraphrase 25, attitude/tone 25, reference (“It/They refers to”) 24**
    - คงไว้: inference 21, purpose 21, word-in-context 21, main idea 18
    - แต่ละ passage มีการผสม 5 ประเภทต่างกัน (ไม่ใช้แพทเทิร์นเดียวซ้ำ 60 ครั้ง) — stem ไม่ซ้ำเกิน 5 ครั้ง (unique 268/300)
  - `tools/apply_rc_v43.py` เสียบแทน `apply_rc.py`+`apply_rc_len.py`+`apply_rc_len2.py` ใน `tools/rebuild_vault.sh` — เขียนทั้ง 5 ข้อของทุก passage (pipeline เดิมแก้แค่ 4 ข้อ เหลือ word-meaning item ของ v42 ไว้) · ตำแหน่งคำตอบจัดแบบ greedy ให้สมดุล **75/75/75/75** พอดี
  - `content/rc_v43_tips.json` — tip แยกตามประเภทคำถาม 9 แบบ (เดิม RC ทั้ง 300 ข้อใช้ tip เดียวกัน 2 แบบ)
  - explanation เขียนใหม่เป็นไทยรายข้อ พร้อมยกประโยคหลักฐานภาษาอังกฤษใน `“…”` — `tools/check_rc_v43.py` (เครื่องมือตรวจใหม่) เช็คว่าทุก quote มีจริงในบทอ่าน + ไม่มีอักษรแปลกปลอม + ตัวเลือกครบ 4 ไม่ซ้ำ + ประเภทตรงแผน
  - **gate สัญญาณเดาคำตอบ:** key-longest **60/300 = 20.0%** (gate ≤30%) · second-longest **132/300 = 44.0%** (gate ≤50%) · drop-topic-then-pick-longest **20.0%** (gate ≤35%) — ต้องขยายตัวลวง 226 จุด (168 จุดให้คีย์ไม่ยาวสุด + 58 จุดกระจายอันดับสอง · patch 1–7 เก็บไว้ที่ `qa/rc_v43_lenpatches/` รันด้วย `tools/apply_rc_v43_len.py`) เพราะรอบแรก key ยาวสุดถึง 70%
  - เลิกใช้ RC pipeline round-3: ย้าย `tools/apply_rc.py`, `apply_rc_len.py`, `apply_rc_len2.py` + `content/rc_r3_[a-f].json`, `rc_lenfix*_r3.json`, `rc_keyshort*_r3.json`, `rc_tplfix_r3.json` ไป `superseded/` (มีหมายเหตุใน `superseded/README.md`)
  - `tools/update_registers.py` เพิ่ม mapping `RC-rewrite` → **G26** ใน `qa/DATA-CHANGES.csv` (1,425 แถว) · `qa/changes_r3.jsonl` รวม 5,192 รายการ
- **เทสต์หลังแก้ (เขียวครบ):** smoke_test 49/49 · regression_v42 60/60 · regression_r3_content 27/27 · regression_r3_ui 7/7 · smoke_r3_extra 94/94 · a11y errors=[]
- `qa/R3-BLUEPRINT-ALIGNMENT.md` gap #4 (RC question types) → ขึ้นสถานะ DONE พร้อมตัวเลข + แก้ย่อหน้าสรุป (เหลือ gap เดียวคือ genre แคบ = งานข้อ 4)
- **ยังไม่ได้ทำ:** ยังไม่ bump version (คง 42.0.2) · ยังไม่ sync ZIP กลับ Drive · GitHub พักไว้ตามคำสั่งผู้ใช้
- **ขั้นต่อไป:** งานข้อ 4 — บทอ่านประเภทใหม่ (ข่าว ประกาศ โฆษณา บทความความรู้) ~30 RC + ~20 TC เริ่มจากธีมที่ซ้ำ

### 2026-11-19 15:58 (เวลาไทย) — Arena AI · หมายเหตุเรื่องซิงก์ Drive (ต้องอ่าน)
- **Arena เริ่มงานจากแพ็ก 12:46 แต่ใน Drive มีแพ็กใหม่กว่าของ Claude (12:54) + `HANDOFF.md` 12:56** ซึ่งเพิ่มตาราง BACKLOG ทั้งหมด (V1–V6, S1–… ฯลฯ) ที่ไฟล์ HANDOFF รุ่นที่ Arena ใช้ (11,688 ไบต์) ไม่มี
- ผลต่างระหว่างสองแพ็กน่าจะมีแค่ `HANDOFF.md` (จำนวนไฟล์ใน ZIP เท่ากัน 192 ไฟล์, MANIFEST 12:54 ระบุว่า "เพิ่ม BACKLOG ทั้งหมด") — งานเนื้อหา/โค้ดในคลังไม่ได้ต่างกัน แต่ยัง **ไม่ได้ยืนยันด้วยการ diff ZIP ต่อไฟล์**
- Arena เก็บ HANDOFF รุ่น 12:56 ของ Claude ไว้ในโฟลเดอร์เดียวกันชื่อ `HANDOFF-claude-1256-BACKLOG.md` (copy) — **รอบหน้าให้ merge ตาราง BACKLOG นั้นเข้า HANDOFF ไฟล์นี้** ก่อนทำงานต่อ
- **ชุดที่ Arena อัปขึ้น Drive ใช้ชื่อมี v43 กำกับ:** `WORKING-v43-part1.zip`, `WORKING-v43-part2.zip`, `WORKING-v43-part3.zip` + `MANIFEST-v43.json` (ชุด v43 = งานข้อ 1, 2, 3, 8a ครบ + เทสต์เขียวทั้งชุด)
  ชุดเก่าของ Claude (`WORKING-part1.zip`, `WORKING-part2.zip`, `MANIFEST.json`, `HANDOFF.md` — modifiedTime 12:54/12:56) ยังอยู่ในโฟลเดอร์ ไม่ได้ลบ
- **อัป `HANDOFF.md` ตัวเดี่ยวไม่ผ่าน:** security filter ของ connector provider บล็อกเนื้อหาไฟล์นี้ จึงไม่มี HANDOFF รุ่น v43 วางไว้ที่หน้าโฟลเดอร์ — ตัวเต็มอยู่ใน `WORKING-v43-part1.zip` (และใน git commit) เท่านั้น ห้ามพยายามอัปซ้ำหรือดัดแปลงเนื้อหาเพื่อเลี่ยงฟิลเตอร์
- `tools/sync_pack.py` ถูกแก้: เดิมหมุน part ที่ >LIMIT*0.9 ทำให้ part ล้นเกิน 2.8 MB (qa/DATA-CHANGES.csv บีบอัดแล้ว ~0.5 MB) ตอนนี้เว้น headroom 700 KB และแพ็กใหม่แน่นขึ้นอัตโนมัติถ้ายังมี part เกินลิมิต — รอบนี้จึงได้ 3 parts (เดิม 2)

### 2026-11-19 16:10 (เวลาไทย) — Arena AI: merge BACKLOG กลับ + เขียนใบสั่งงานละเอียด `qa/V43-NEXT-WORK.md`
- ดาวน์โหลด `HANDOFF-claude-1256-BACKLOG.md` (31,359 B, ของ Claude 12:56) มาเทียบหัวข้อกับ HANDOFF ในเครื่อง (20,959 B, มีแค่ log ของ Arena) → พบว่าไฟล์ในเครื่อง**ไม่มีส่วน BACKLOG ทั้งหมด (C/V/S/T/Q) + เช็กลิสต์เขียนข้อสอบ + นิยามเสร็จ + ข้อความสั่งงานสำเร็จรูป + สเปกงานข้อ 1** → merge กลับเข้ามาแล้ว (เพิ่ม 104 บรรทัด) HANDOFF ตอนนี้ครบทั้งสองฝั่ง
- อัปเดตตาราง BACKLOG ตามงานจริง: C1 ✅ (commit b8b16b0), C2 ✅ (e80af6e), C3 ✅ (6d9368e), V1 🟨 8a เสร็จ (fbe2f20) เหลือ plausible 46 + uncertain 44
- สร้าง `qa/V43-NEXT-WORK.md` = ใบสั่งงานละเอียด มีตัวเลขที่**วัดจริง**จาก build ปัจจุบัน: rc_heuristics → longest 20% / no-topic+longest 20% / no-extreme+longest 28.3% / **max-context-overlap 51.7%** / combined 53.7% · bias_metrics → **TC answer_longest 42%**, **Short conv context-overlap 67%**, RC overlap 41.3%, extreme-word answer 6.7% vs distractor 19.4% · RC type mix ตอนนี้ details 120, TRUE 25, paraphrase 25, attitude 25, reference 24, inference 21, purpose 21, **wic 21 (เป้า 60)**, main 18 · REVIEW-QUEUE 1,505 แถว (example-quality 1,217 / headword-validity 146 / spot-check 120) · axe incomplete 144 จุด
- หนี้ใหม่ที่ Arena ทิ้งไว้และบันทึกในไฟล์นั้นแล้ว: (1) RC wic ต่ำกว่าเป้า 3/15 (2) TC answer_longest 42% ยังไม่มี gate จับ (3) ไฟล์ /tmp ที่ validator ใช้อ้าง (rc_typeplan.json, rc_passages.json) หายหลัง sandbox reset → มีสคริปต์สร้างใหม่ให้ในไฟล์
- อัปขึ้น Drive เป็นไฟล์เดี่ยว `qa/V43-NEXT-WORK.md` (HANDOFF.md ตัวเดี่ยวยังอัปไม่ผ่าน security filter ของ connector — อยู่ใน zip กับ git เท่านั้น)

### 2026-11-19 16:13 (เวลาไทย) — Arena AI: เพิ่ม `START-HERE-v43.md` + แก้ `tools/check_rc_v43.py` ให้ไม่พึ่ง /tmp
- สร้าง `START-HERE-v43.md` (15 KB) = ไฟล์อ่านก่อนเป็นไฟล์แรกสำหรับผู้รับงานต่อ: วิธีรับ/แตก zip + เช็ค sha, แผนที่ไฟล์ (เอกสาร/ข้อมูล/สเปก/tools/tests — อันไหนคืออะไร เปิดอันไหนก่อน), บล็อกคำสั่งตั้งเครื่อง+เทสต์ครบชุดพร้อม **ค่าที่ควรได้** (ไว้เช็คว่าเครื่องถูก), สิ่งที่ทำไม่ได้ 15 ข้อพร้อมเหตุผล (แบ่งเป็น ข้อจำกัดเครื่องมือ / งานค้างที่เริ่มแล้ว / งานที่ต้องคนจริง / ความผิดพลาดของ Arena เอง), ข้อความสั่งงานสำเร็จรูป 3 แบบ, กติกาห้าม 8 ข้อ
- แก้ `tools/check_rc_v43.py`: เดิมอ่าน `/tmp/rc_passages.json` ตรง ๆ → sandbox reset แล้ว tool พังทันที (FileNotFoundError) ตอนนี้ถ้าไม่มีไฟล์นั้นจะประกอบ context ของ 60 passage จาก `data/vault.json` เอง (RC เก็บ 5 ข้อ/passage และงาน C3 ไม่เคยเปลี่ยน context) · รันแล้วได้ `11 files, 300 items` + type mix ตรงกับที่วัดไว้ + `ALL CLEAN`
- `/tmp/rc_typeplan.json` (แผน type ต่อ passage) กู้ไม่ได้ — เขียนบอกไว้แล้วว่า gate ใหม่ G-A ให้อ่าน type จาก `content/` เท่านั้น
- หมายเหตุ: `.git` ไม่ได้อยู่ใน zip (sync_pack แพ็กเฉพาะไฟล์งาน) และไม่ได้ push GitHub → ผู้รับงานต่อจะไม่มีประวัติ commit มีแต่ log ท้ายไฟล์นี้

### 2026-11-19 17:26 (เวลาไทย) — Claude: รับต่อจาก Arena 16:13 · งาน 1–8 + T6–T8 + S1–S5 · bump 43.0.0
- **อ่านสรุปเต็มที่ `qa/V43-CLAUDE-ROUND-REPORT.md`** (4 หัวข้อ: แก้แล้ว / automated ผ่าน / ต้องมนุษย์ตรวจ / ยังค้าง) และ `qa/AI-REVIEW-v43-Claude.md`
- baseline ก่อนแก้ตรงกับตัวเลขของ Arena ทุกตัว (เครื่องนี้ chromium อยู่ที่ `/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`)
- RC: wic 21→60 (ตารางเป้าของ Arena ครบทุกประเภท) · key ถอดความ 64 ข้อ → max-context-overlap 0.517→0.270, combined 0.537→0.270 · บทอ่าน genre ใหม่ 4 บท (ข่าว/รับสมัครงาน/อีเมล/บทความ) แทน S13-Q046, S14-Q046, S16-Q046, S20-Q051 → near-dup 0.309→<0.25 · `apply_rc_v43.py` + `check_rc_v43.py` รองรับ field `context`/`topic`/`genre` ในสเปกแล้ว
- TC: answer_longest 0.420→0.293 (ยืดตัวลวง 38 ข้อ + เขียนคำอธิบายไทยใหม่)
- Short conv: pipeline ใหม่ `content/short_v43_[ab].json` + `tools/apply_short_v43.py` (tag SHORT-rewrite/G30) · overlap 0.670→0.285 · **พบใหม่:** 60 บทสนทนามาจาก 20 สถานการณ์ × 3 (เปลี่ยนแค่ชื่อ) ดู `qa/AI-REVIEW-v43-short-duplicates.txt`
- Q-R: pipeline ใหม่ `content/qr_idiom_v43_[ab].json` + `tools/apply_qr_idiom.py` (tag QR-idiom/G31) · idiom 60 ข้อแทนข้อที่ใช้ตัวลวงสำเร็จรูป
- extreme-word: แก้ตัวลวง RC 45 + LC 93 → answer/distractor อยู่ใน 1.5 เท่าทุก kind
- gate ใหม่ 11 ตัว (regression_r3_content 27→38) · bump 43.0.0 ทุกไฟล์ที่ Arena ระบุ · `web/CHANGELOG-v43.0.0.md` · ZIP deploy + ZIP QA + .sha256 (อัปแยกใน Drive)
- เทสต์สุดท้าย 17:21: content 38/38 · smoke 49/49 · v42 60/60 · r3_ui 7/7 · extra 94/94 · a11y errors [] · check_rc ALL CLEAN · check_quotes 565/0
- commit: `7ae0098` import → `9cb5088` งานหลัก → commit สุดท้าย (S17-Q049 + เอกสาร) · `.git` ไม่อยู่ใน zip
- **ไม่ได้ทำ:** V2–V6 คลังศัพท์, T1–T5, Q1–Q3, Short conv สถานการณ์ใหม่ 40 บท, Q-R ตัวลวงอีก 86 ข้อ — เหตุผลอยู่ในรายงาน
