# AI-REVIEW v43 (C9) — Claude, 2026-11-19

> **ขอบเขต:** รอบนี้เป็นการตรวจแบบ (1) สคริปต์หาจุดเสี่ยงทั้งคลัง + (2) ข้อสังเกตจากการแก้ไขจริงของ Claude ในรอบนี้ · **ยังไม่ใช่การอ่านครบทุกข้อทีละข้อ** และผู้ตรวจเป็นคนเดียวกับผู้แก้บางส่วน (ไม่อิสระ) → ต้องมีมนุษย์หรือ AI อีกตัว spot-check ตามรายการด้านล่าง · **ไม่ได้แก้ไฟล์ข้อสอบจากรายงานนี้** ยกเว้น 1 จุดที่ระบุไว้

## 1. ปัญหาเชิงระบบที่พบ (สำคัญที่สุด)

| id / กลุ่ม | ปัญหา | หลักฐาน | ข้อเสนอแก้ |
|---|---|---|---|
| Short Conversation ทั้ง 200 ข้อ | **บทสนทนา 60 บทมาจากสถานการณ์แค่ 20 แบบ** แต่ละแบบซ้ำ 3 ครั้งโดยเปลี่ยนแค่ชื่อคน | กลุ่มซ้ำ (id แรกของแต่ละบท): S01-Q011 / S07-Q017 / S14-Q014; S01-Q014 / S08-Q011 / S14-Q017; S01-Q017 / S08-Q014 / S15-Q011; S02-Q011 / S08-Q017 / S15-Q014; S02-Q014 / S09-Q011 / S15-Q017; S02-Q017 / S09-Q014 / S16-Q011 … รวม 20 กลุ่ม (รายการเต็มใน `qa/AI-REVIEW-v43-short-duplicates.txt`) | เขียนสถานการณ์ใหม่ 40 บท (งาน C6) ให้ไม่ซ้ำกันและไม่ซ้ำ LC · รอบนี้ทำแค่เปลี่ยนตัวลวงเพื่อแก้ overlap |
| Short Conversation blank (2)/(4) | ตัวลวงยังเป็นประโยคสำเร็จรูปที่ใช้ซ้ำทุกบท (เช่น “Let’s ignore it and hope nobody notices.”) | blank (1)/(3) แก้แล้ว 120 ข้อ, blank (2)/(4) ยังไม่แก้ | เขียนตัวลวงเฉพาะบทให้ blank (2)/(4) |
| Short Conversation 120 ข้อที่แก้ | คำอธิบายไทยเดิมอาจยังเอ่ยถึงตัวลวงทั่วไปที่ถูกเปลี่ยนออกไปแล้ว (เช่น “ค่าตั๋ว การเลื่อนงาน”) | `tools/apply_short_v43.py` ต่อท้ายคำอธิบายตัวหลอกใหม่ แต่ไม่ได้ลบข้อความเดิม | ตรวจทีละข้อแล้วเขียนคำอธิบายใหม่ |
| Q-R 86 ข้อที่เหลือ | ยังใช้ตัวลวงสำเร็จรูปซ้ำ ≥2 ตัว (มี 27 ประโยคที่ใช้ซ้ำ 12–19 ครั้ง เช่น “At the far end of the hall.”, “Since last Tuesday.”) | วัดจาก `data/vault.json` หลังแทนที่ 60 ข้อด้วย idiom | เขียนตัวลวงใหม่เฉพาะข้อ |
| TC relative-clause items | ตัวลวงใหม่ที่ Claude ใช้ยืดความยาว (`whereas`, `wherever`, `whatever`, `whichever`, `whoever`) ไม่เคยเป็นคำตอบเลย → อาจกลายเป็นสัญญาณให้ตัดทิ้งได้ | 15 จุดใน `content/tc_v43_*.json` | รอบหน้าให้ wh-ever เป็นคำตอบจริงในบาง passage |
| TC verb-form items | ตัวลวงแบบ passive infinitive/gerund (`to be V3`, `being V3`) ที่เพิ่มรอบนี้ไม่เคยเป็นคำตอบ | 13 จุด | เพิ่มข้อที่ passive เป็นคำตอบถูก |

## 2. RC — ตัวลวงที่ทำจากคำในบทเกือบทั้งหมด (เสี่ยงถูกด้วย) ต้องให้คนอ่านเทียบบท

สคริปต์: ตัวลวงที่ ≥90% ของคำหลักอยู่ในบทอ่าน (ไม่นับข้อ wic/reference) · ส่วนใหญ่เป็น “จริงในบทแต่ไม่ตอบคำถาม” ซึ่งเป็นตัวลวงที่ดี แต่ต้องยืนยัน

## RC: distractor almost entirely made of passage words (possible second correct answer)
| S01-Q051 | What did the students do during the first week of the experi | D: They placed large signs near the entrance. | K: They observed where people stopped to ask for directions. |
| S01-Q051 | What did the students do during the first week of the experi | D: They recommended adding a small digital board. | K: They observed where people stopped to ask for directions. |
| S01-Q058 | Why did the museum decide to keep both versions of the guide | D: The weekend trial showed both versions were too long. | K: Different visitors preferred different formats. |
| S02-Q054 | Which option best restates: “The information is not an offic | D: The board is the town’s official weather forecast. | K: The board shows real conditions, not predictions. |
| S03-Q054 | Which option best restates: “The club did not claim that its | D: The club proved every source of the river pollution. | K: The data was limited but still useful to officials. |
| S04-Q056 | What did the student expect most answers to be about? | D: Neighbors who left their doors open. | K: New buildings in the neighborhood. |
| S05-Q048 | What is the central point of the passage? | D: Circle seating is always better than rows. | K: The best seating depends on the task being done. |
| S05-Q055 | Which option matches what the passage says? | D: The old schedule used columns for locations. | K: Visitors found information faster with the new version. |
| S06-Q057 | Why did the school choose plants that survive without water? | D: Vegetables received many fewer votes than flowers did. | K: Fewer students volunteered for daily watering. |
| S07-Q051 | What did the survey responses show about the bell signal? | D: It was too loud in the main building. | K: It was clearer in the main building than near the gym. |
| S07-Q057 | Why did the association keep the original text beside the tr | D: Because volunteers preferred the first version. | K: So staff could check the details. |
| S08-Q049 | Which option best restates: “Their report emphasized the dif | D: A report should prove the cause of a pattern. | K: Seeing a pattern is not the same as explaining why it happens. |
| S08-Q052 | Why did several musicians ignore the chart at first? | D: Guest musicians had already changed the seats. | K: They already knew where they usually sat. |
| S09-Q047 | Besides tags, what else did students record? | D: The arguments used in past debates. | K: Which topics had been used more than once. |
| S09-Q056 | How were the two groups of plants watered? | D: Both received the same amount each day. | K: One a little daily, the other more every three days. |
| S12-Q049 | Which statement agrees with the information in the passage? | D: The organizers will redesign the whole art trail. | K: Visitors spent longer looking at the artworks. |
| S12-Q049 | Which statement agrees with the information in the passage? | D: Visitors were asked to comment before the signs were made. | K: Visitors spent longer looking at the artworks. |
| S13-Q060 | Which option matches what the passage says? | D: Volunteers repaired the items for the families. | K: Many people came back with clothes they had mended. |
| S14-Q054 | What is the main idea of the passage? | D: How coaches plan weekend sports sessions. | K: Coaches changing a program to keep new players. |
| S15-Q046 | Why did the organizers arrange the first-aid day? | D: Participants asked for a reference card. | K: Volunteers were unsure how to respond to accidents. |
| S15-Q047 | Which step were some participants still uncertain about? | D: Placing someone in the recovery position. | K: Dealing with severe bleeding. |
| S15-Q055 | According to the passage, which statement is TRUE? | D: The second review found more mistakes. | K: The same readers tested the app twice. |
| S17-Q049 | Which of these statements is TRUE? | D: Peer mentors explained the difficult steps. | K: More learners started to speak up. |
| S18-Q053 | Which option best restates: “After a month, rooms were being | D: Rooms were used less often after a month. | K: Sharing improved, but some groups stayed too long. |
| S20-Q059 | Which option best restates: “Not every family returned the f | D: Every family returned the form on time. | K: Because some forms were not returned, the survey will be shorter next time. |
## RC: key and a distractor share >=60% content words
| S05-Q056 | K: Compared products by the big number on the front. | D: Compared only products with sodium. |
| S06-Q054 | K: Volunteers should help with language, not make decisions. | D: Volunteers make better decisions than officials. |
| S15-Q055 | K: The same readers tested the app twice. | D: Staff tested the app before readers did. |
## TC: distractor is another form of the key (check both cannot fit)
| S01-Q041 | K: established | D: establishing | explanation does not mention this distractor |
| S01-Q041 | K: established | D: establishes | explanation does not mention this distractor |
| S03-Q041 | K: welcomed | D: welcoming | explanation does not mention this distractor |
| S09-Q040 | K: opened | D: opening | explanation does not mention this distractor |
## explanation does not mention distractor (TC)
tc distractors not named in exp: 14


**แก้แล้ว 1 จุดระหว่างตรวจ:** `S17-Q049` ตัวลวง “Peer mentors explained the difficult steps.” ใกล้เคียงข้อเท็จจริงเกินไปหลังตัดคำ every → เปลี่ยนเป็น “Peer mentors gave formal lectures to the class.”

## 3. รายการที่ Claude แก้ในรอบนี้และต้องมีคน spot-check

| กลุ่ม | จำนวน | ที่ต้องดู |
|---|---|---|
| RC words-in-context ใหม่ | 43 ข้อ (39 แปลงจากประเภทอื่น + 4 ในบทใหม่) | คำ/วลีที่เลือกตีความได้ทางเดียวไหม · ตัวลวงไม่ใช่ความหมายที่ใช้ได้ในบริบท |
| RC key ที่ถอดความ (paraphrase) | 64 ข้อ | ความหมายยังตรงกับบทครบไหม (บางข้อตัดรายละเอียด เช่น `S07-Q046` “Mobiles and purses were soon returned.” ตัด “often/within a week”) |
| RC บทอ่านใหม่ 4 บท | 20 ข้อ (`S13-Q046`, `S14-Q046`, `S16-Q046`, `S20-Q051`) | ภาษาธรรมชาติ ความยาว ระดับยาก |
| RC/LC ตัวลวงที่ลดคำ absolute | RC 45 · LC 93 | ตัวลวงยังผิดชัดหลังตัดคำ all/every/only ไหม |
| TC ตัวลวงที่ยืดความยาว + คำอธิบายไทยที่เขียนใหม่ | 38 ข้อ | ไวยากรณ์ในคำอธิบาย |
| Short Conversation ตัวหลอกใหม่ | 120 ข้อ | ภาษาธรรมชาติ (สร้างจากแม่แบบ 8 แบบ) |
| Q-R idiom | 60 ข้อ | ไม่มีสองคำตอบที่ใช้ได้ · ระดับสำนวนเหมาะกับ ม.6 |
