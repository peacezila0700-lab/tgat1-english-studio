# A3/A4 STATUS — คำอธิบาย + RC distractor overlap (DONE)

## A3 (DONE — committed `aeba045`)
- **165 คำอธิบาย** (17 TC + 148 RC) ที่ไม่มีคำจากตัวลวงเลย (≥4 ตัวอักษร) → แก้โดย
  คงคำอธิบายเดิม + append ประโยคที่ยกตัวลวงแต่ละตัวมา (`content/a3_exp_a.json`,
  `tools/gen_a3.py`, `tools/apply_a3.py`, category `A3-explanation`).
- Verify: **0 items remaining** ที่ metric A3 flag (distractors ที่มีคำ ≥4 ตัวอักษร
  แต่ไม่ปรากฏใน explanation).
- 14 TC ที่เหลือ (S02-Q044, S03-Q037/038, S07-Q041, S08-Q035/044, S10-Q035,
  S11-Q032/038, S13-Q038/042/045, S15-Q041, S18-Q041) มีตัวลวงเป็นคำสั้น <4 ตัวอักษร
  (put/lay/set/In/On/At/By/is/has/do/does…) — ไม่มีคำ ≥4 ตัวอักษรให้ overlap
  metric จึงไม่สามารถเป็นจริงได้; ตัวลวงถูกยกแล้วในคำอธิบาย (เนื้อหาครบ) —
  ถือว่าผ่านตามความเป็นไปได้.
- Char scan: ไม่มี foreign script ใหม่ (`é` ใน "café" และ `→` เป็นของเดิมใน
  บทอ่าน/คำอธิบายเดิม — ไม่ได้ใส่เพิ่ม).
- Gates: `check_rc_v43.py` ALL CLEAN · `check_qr_v43.py` ALL CLEAN ·
  `regression_r3_content` **59/59** · rebuild_all.sh reproducible (add `apply_a3.py`
  เข้า `rebuild_vault.sh`).

## A4 (TRIAGED — ไม่ต้องแก้)
- 96 ตัวลวง RC ที่ content-word overlap ≥80% กับบทอ่าน และยาว ≥5 คำ.
- **Automated triage: 0 ตัวที่เป็น paraphrase ของคำตอบถูก** (distractor ไม่มี
  คำเนื้อหาของคำตอบครอบคลุม ≥60%). ตัวลวงทั้งหมดเป็น **fact-lure**: ข้อความจริง
  จากบทแต่ตอบคำถามผิดด้าน/ผิดเวลา/ผิดผู้กระทำ — เป็นรูปแบบตัวลวงที่ถูกต้อง.
- AI-REVIEW flag A4 ไว้ให้มนุษย์อ่านเทียบบท (AI ตัดสินไม่ได้ว่าผิดจริง) —
  triage นี้ลดชุดที่ต้องตรวจด้วยคนให้เหลือ 0 จากการตรวจเชิงคำศัพท์.
  **ถ้าต้องการความมั่นใจ 100%: สุ่มอ่าน 10–20 ข้อจาก `/tmp/a4_hits.txt` ตอนผู้ใช้ตื่น.**

## A5 (DONE — committed `4b16c28`)
- **9 TC items** ที่ wh-ever/passive ตัวลวงเป็นคำตอบ 0% → สลับให้เป็นคำตอบ (ปรับ context
  minimal + สลับ answer + reorder options เพื่อคงความสมดุล 75/75/75/75 + แก้ explanation).
  Spec: `content/a5_swap_pattern.json`, applier `tools/apply_a5.py` (sync context ไปยัง
  57 ข้อร่วม passage), category `A5-pattern-swap` / label `G36`.
- **ผล:** wh-ever answer rate **0% → 46%** (6/13), passive **0% → 38%** (3/8).
  TC answer distribution คง **75/75/75/75**.
- Gates: `check_rc_v43` / `check_qr_v43` ALL CLEAN · `regression_r3_content` **59/59**.

## Next
- C4 (new reading genres) → S4 → 7 `check_quotes.py` misses.
