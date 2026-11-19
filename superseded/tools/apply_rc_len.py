import json,sys,os,re
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
F=json.load(open('content/rc_lenfix_r3.json'))
REASON='RC option-length balancing (key was uniquely longest) / removal of templated “To prove the <topic> had already solved every participant’s problem” distractor that named the topic'
for qid,ch in F.items():
    q=by[qid];o=list(q['options']);a=q['answer'];e=q['explanation']
    if 'key' in ch:
        old=o[a];o[a]=ch['key']
        for variant in (old,old.rstrip('.'),old[0].lower()+old[1:].rstrip('.')):
            if variant in e: e=e.replace(variant,ch['key'].rstrip('.'));break
    for old,new in ch.get('d',[]):
        assert old in o and o.index(old)!=a,(qid,old,o);o[o.index(old)]=new
    if 'dprove' in ch:
        j=[i for i,x in enumerate(o) if i!=a and x.startswith('To prove the ')];assert len(j)==1,(qid,o);o[j[0]]=ch['dprove']
    assert len(set(o))==4
    if o!=q['options']: log(qid,'options',q['options'],o,REASON,'RC-distractors');q['options']=o
    if e!=q['explanation']: log(qid,'explanation',q['explanation'],e,'explanation updated to the revised key wording','RC-distractors');q['explanation']=e
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1);print('ok',len(F))
