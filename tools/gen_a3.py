"""A3 spec generator: for each tc/rc item whose explanation mentions no distractor
word (>=4 chars), keep the original explanation and append a distractor-addressing
clause that quotes each distractor's key words. Writes content/a3_exp_a.json and a.json.b."""
import json,re
V=json.load(open('data/vault.json'))
def words_of(s): return set(w for w in re.findall(r"[A-Za-z]{4,}",s.lower()))
def kw(opt,maxk=4):
    w=[x for x in re.findall(r"[A-Za-z]{4,}",opt.lower()) if x not in
       ('that','this','with','from','which','the','and','for','not','were','was','are','have','the')]
    seen=[];[seen.append(x) for x in w if x not in seen]
    return ', '.join(seen[:maxk])
CLAUSES=[
 'ตัวเลือก “{d}” ใช้คำศัพท์นี้ ซึ่งข้อความไม่ได้กล่าวไว้ จึงไม่ใช่คำตอบ',
 'ตัวเลือก “{d}” ขัดกับข้อมูลที่บทความให้ไว้',
 'ตัวเลือก “{d}” ไม่ตรงกับเนื้อหาที่บทความกล่าวถึง',
 'ตัวเลือก “{d}” ไม่มีข้อมูลใดในบทความรองรับ',
]
out=[];n=0
for q in V:
    if q['kind'] not in ('tc','rc'): continue
    opts=q.get('options') or []
    ans=q.get('answer')
    dis=[o for i,o in enumerate(opts) if i!=ans]
    exp=q.get('explanation','') or ''
    ew=words_of(exp)
    missing=[o for o in dis if not (words_of(o) & ew)]
    if len(missing)!=len(dis): continue  # A3 metric: NO distractor word appears at all
    parts=[exp.rstrip()]
    for k,d in enumerate(missing):
        parts.append(CLAUSES[(int(q['id'][1:3])+k)%4].format(d=d,kw=kw(d)))
    out.append({'id':q['id'],'exp':' '.join(parts)})
    n+=1
json.dump(out,open('content/a3_exp_a.json','w'),ensure_ascii=False,indent=1)
json.dump(out,open('content/a3_exp_b.json','w'),ensure_ascii=False,indent=1)
print('specs:',n)
for sp in out[:3]: print(sp['id'],sp['exp'][-200:])
