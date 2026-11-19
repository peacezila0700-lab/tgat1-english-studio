import json,glob,sys,os,collections
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V};order=[q['id'] for q in V]
P=[]
for f in sorted(glob.glob('content/rc_r3_[a-f].json')): P+=json.load(open(f))
assert len(P)==60
R={'q1':'RC main-idea item rewritten: v42.0.1 distractors repeated the passage/topic name and were implausible (choose-the-option-without-the-name strategy scored 81% overall); key was a fixed “How X was developed and improved” formula',
   'q2':'RC sequence/detail item rewritten: distractors were invented actions naming the project; now uses other real steps from the passage in the wrong order or unsupported details',
   'q5':'RC inference item rewritten: distractors were extreme/absurd statements naming the project (100% guessable by the name rule); explanation previously quoted a truncated evidence fragment',
   'q3':'RC purpose item: stem did not match the infinitive-of-purpose key (e.g. “What did … learn?” → “To check …”); stem rewritten'}
POS={'q1':0,'q2':1,'q3':2,'q5':4}
import collections as _c
USED=_c.Counter(q['answer'] for q in V if q['kind']=='rc')
for pi,p in enumerate(P):
    i0=order.index(p['first']);ids=order[i0:i0+5]
    assert all(by[x]['kind']=='rc' for x in ids) and len(set(by[x]['context'] for x in ids))==1
    for k,pos in POS.items():
        q=by[ids[pos]]
        if k=='q3' and 'q3' not in p:
            if 'q3prompt' in p and q['prompt']!=p['q3prompt']: log(q['id'],'prompt',q['prompt'],p['q3prompt'],R['q3'],'RC-stem');q['prompt']=p['q3prompt']
            continue
        it=p[k];USED[q['answer']]-=1;ap=min(range(4),key=lambda x:(USED[x],(x-pi)%4));USED[ap]+=1
        opts=list(it['d']);opts.insert(ap,it['key'])
        new={'options':opts,'answer':ap,'explanation':it['exp']}
        if 'prompt' in it: new['prompt']=it['prompt']
        for fld,val in new.items():
            if q[fld]!=val: log(q['id'],fld,q[fld],val,R[k],'RC-distractors');q[fld]=val
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print(collections.Counter(q['answer'] for q in V if q['kind']=='rc'))
