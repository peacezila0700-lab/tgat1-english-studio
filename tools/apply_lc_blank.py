import json,glob,sys,os
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V};order=[q['id'] for q in V]
ctxs=[]
for f in sorted(glob.glob('content/lc_blank_r3_[a-d].json')): ctxs+=json.load(open(f))
R3=len(ctxs);assert R3==20,R3
V43_RE='LC v43: sets 11-20 converted from comprehension questions to blank fill-in dialogues to match the official TGAT1 long-conversation blueprint'
for f in sorted(glob.glob('content/lc_blank_v43_[e-h].json')): ctxs+=json.load(open(f))
assert len(ctxs)==40,len(ctxs)
n=0
for ci,c in enumerate(ctxs):
    v43=ci>=R3
    reason=('LC blank dialogue rewritten: v42.0.1 used one fixed 10-line template for all 20 blank-type dialogues, reused distractors verbatim, and explanations named distractors not present' if not v43 else V43_RE)
    tag='LC-rewrite'
    i0=order.index(c['first']);ids=order[i0:i0+5]
    assert all(by[x]['kind']=='long' for x in ids) and len(set(by[x]['context'] for x in ids))==1,ids
    for k,(qid,it) in enumerate(zip(ids,c['items'])):
        q=by[qid];pos=(ci*5+k*3+ci//4)%4
        opts=list(it['d']);opts.insert(pos,it['key']);assert len(opts)==4 and len(set(opts))==4
        new={'context':c['context'],'options':opts,'answer':pos,'explanation':it['exp'],'tip':c['tip'],'prompt':f'Which response best completes blank ({k+1})?'}
        assert f'({k+1}) ____' in c['context']
        for fld,val in new.items():
            if q[fld]!=val:
                log(qid,fld,q[fld],val,reason,tag);q[fld]=val
        n+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1);print('updated',n)
import collections;print(collections.Counter(by[x]['answer'] for x in by if by[x]['kind']=='long'))
