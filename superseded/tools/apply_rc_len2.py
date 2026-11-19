import json,sys,os
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
F=json.load(open('content/rc_lenfix2_r3.json'))
for qid,pairs in F.items():
    q=by[qid];o=list(q['options'])
    for old,new in pairs: assert old in o and o.index(old)!=q['answer'],(qid,old);o[o.index(old)]=new
    assert len(set(o))==4;log(qid,'options',q['options'],o,'RC option-length balancing round 3 (key was uniquely longest)','RC-distractors');q['options']=o
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1);print('ok',len(F))
K=json.load(open('content/rc_keyshort_r3.json'))
for qid,new in K.items():
    q=by[qid];o=list(q['options']);old=o[q['answer']];o[q['answer']]=new;assert len(set(o))==4
    log(qid,'options',q['options'],o,'RC key shortened so that answer length does not form a second-longest-option cue','RC-distractors');q['options']=o
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1);print('keys',len(K))
import re as _re
TF=json.load(open('content/rc_tplfix_r3.json'));TPL=r'neighboring towns|before reviewing any participant feedback'
for qid,new in TF.items():
    if qid=='_stems': continue
    q=by[qid];o=list(q['options']);idx=[i for i,x in enumerate(o) if _re.search(TPL,x)];assert len(idx)==len(new)==2 and q['answer'] not in idx,(qid,o)
    for i,t in zip(idx,new): o[i]=t
    assert len(set(o))==4;log(qid,'options',q['options'],o,'RC purpose item: two remaining templated distractors that named the topic (“expand … to neighboring towns”, “replace … before reviewing any participant feedback”) replaced with passage-based distractors','RC-distractors');q['options']=o
for qid,p in TF['_stems'].items():
    q=by[qid];log(qid,'prompt',q['prompt'],p,'RC purpose stem aligned with infinitive-of-purpose key','RC-stem');q['prompt']=p
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1);print('tplfix',len(TF)-1)
K2=json.load(open('content/rc_keyshort2_r3.json'))
for qid,new in K2.items():
    q=by[qid];o=list(q['options']);old=o[q['answer']];o[q['answer']]=new;assert len(set(o))==4,(qid,o);e=q['explanation']
    for v in (old,old.rstrip('.'),old[0].lower()+old[1:].rstrip('.'),old[0].upper()+old[1:].rstrip('.')):
        if v in e: e=e.replace(v,new.rstrip('.'));break
    log(qid,'options',q['options'],o,'RC key shortened: second-longest option was the key in 52% of RC items','RC-distractors');q['options']=o
    if e!=q['explanation']: log(qid,'explanation',q['explanation'],e,'explanation updated to the revised key wording','RC-distractors');q['explanation']=e
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1);print('keyshort2',len(K2))
