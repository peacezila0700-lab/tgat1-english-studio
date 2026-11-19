import json,sys,os,glob,collections
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));rcs=[q for q in V if q['kind']=='rc'];G=collections.OrderedDict()
for q in rcs: G.setdefault(q['context'],[]).append(q)
G=list(G.values())
spec={}
for f in sorted(glob.glob('content/rc_r3_0[0-9].json')): spec.update(json.load(open(f)))
R='RC revised in round 3: passage-specific distractors replace recycled templates that repeated the topic name; key/length cues reduced; stems aligned with answers'
done=0
import re
STOP=set('the a an of to and in on for with by at from is was were be that this it its as or but not their they them how why what which who so more most'.split())
def tk(x): return set(w for w in re.findall(r"[a-z]+",x.lower()) if w not in STOP and len(w)>2)
def evidence_exp(q,qi,key):
    sents=re.split(r'(?<=[.!?])\s+',q['context'])
    if qi==3:
        m=re.search(r'[“"]([^”"]+)[”"]',q['prompt']);w=m.group(1) if m else ''
        hit=[x for x in sents if w.lower() in x.lower()]
        ev=hit[0] if hit else ''
        return f"ในบริบทนี้ “{w}” หมายถึง {key} ดูจากประโยค “{ev}” ตัวเลือกอื่นเป็นความหมายอื่นของคำ หรือเป็นรายละเอียดอื่นในบทอ่านที่ไม่ใช่ความหมายของคำนี้"
    best=max(sents,key=lambda x:len(tk(x)&tk(key)))
    return f"คำถามนี้ถามเหตุผลหรือจุดประสงค์ คำตอบคือ “{key}” หลักฐานใกล้เคียงที่สุดในบทอ่านคือ “{best}” ตัวเลือกอื่นเป็นเหตุการณ์อื่นในเรื่อง ขัดกับบทอ่าน หรือไม่มีหลักฐานรองรับ"
for tag,s in spec.items():
    g=G[int(tag[1:])-1]
    for qi in range(5):
        it=s.get(f'q{qi}')
        if not it: continue
        q=g[qi];a=q['answer'];opts=list(q['options']);oldkey=opts[a]
        if 'key' in it: opts[a]=it['key']
        if 'd' in it:
            others=[i for i in range(4) if i!=a]
            for i,t in zip(others,it['d']): opts[i]=t
        for old,new in it.get('dmap',{}).items():
            assert old in opts,(tag,qi,old,opts);opts[opts.index(old)]=new
        assert len(set(opts))==4,(tag,qi,opts)
        if opts!=q['options']: log(q['id'],'options',q['options'],opts,R,'RC-distractor');q['options']=opts
        if 'prompt' in it and it['prompt']!=q['prompt']: log(q['id'],'prompt',q['prompt'],it['prompt'],R,'RC-stem');q['prompt']=it['prompt']
        exp=it.get('exp')
        if not exp and qi in (2,3): exp=evidence_exp(q,qi,opts[a])
        if not exp and opts[a]!=oldkey:
            exp=q['explanation'].replace(oldkey,opts[a]) if oldkey in q['explanation'] else q['explanation']+f' (คำตอบที่ถูก: {opts[a]})'
        if exp and exp!=q['explanation']: log(q['id'],'explanation',q['explanation'],exp,R+('' if it.get('exp') else '; explanation rule-generated from passage evidence — needs human review'),'RC-explanation' if it.get('exp') else 'RC-explanation-rule');q['explanation']=exp
        done+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1);print('rc items touched',done,'passages',len(spec))
