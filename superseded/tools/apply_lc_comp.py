import json,glob,sys,os,re,collections
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V};order=[q['id'] for q in V]
ctxs=[]
for f in sorted(glob.glob('content/lc_comp_r3_[e-h].json')): ctxs+=json.load(open(f))
assert len(ctxs)==20
CONTR=[(r'\bLet us\b',"Let’s"),(r'\blet us\b',"let’s"),(r'\bI will\b',"I’ll"),(r'\bWe will\b',"We’ll"),(r'\bwe will\b',"we’ll"),(r'\bdo not\b',"don’t"),(r'\bdoes not\b',"doesn’t"),(r'\bcannot\b',"can’t"),(r'\bis not\b',"isn’t"),(r'\bare not\b',"aren’t"),(r'\bIf it is\b',"If it’s"),(r'\bit is\b',"it’s")]
TIP='ฟังหาสามเรื่อง: ปัญหาที่ทำให้เริ่มคุย ข้อเสนอพร้อมเหตุผล และใครจะทำอะไรต่อ ระวังตัวเลือกที่ใช้คำจากบทสนทนาแต่ระบุผู้ทำ เวลา หรือลำดับผิด'
REASON='LC comprehension items revised: v42.0.1 used fixed generic stems ("What did the speakers do first?", "Why do they want to take that step?"), implausible distractors, keys usually longest, generic English explanations; dialogue used unnatural uncontracted speech'
for ci,c in enumerate(ctxs):
    i0=order.index(c['first']);ids=order[i0:i0+5]
    assert all(by[x]['kind']=='long' for x in ids) and len(set(by[x]['context'] for x in ids))==1
    ctx=by[ids[0]]['context']
    for a,b in CONTR: ctx=re.sub(a,b,ctx)
    for k,(qid,it) in enumerate(zip(ids,c['items'])):
        q=by[qid];pos=(ci*5+k*3+ci//4+1)%4
        opts=list(it['d']);opts.insert(pos,it['key']);assert len(set(opts))==4
        new={'context':ctx,'prompt':it['prompt'],'options':opts,'answer':pos,'explanation':it['exp'],'tip':TIP}
        for fld,val in new.items():
            if q[fld]!=val: log(qid,fld,q[fld],val,REASON,'LC-revise');q[fld]=val
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print(collections.Counter(by[x]['answer'] for x in by if by[x]['kind']=='long'))
