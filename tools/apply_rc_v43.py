"""v43 task 3: rewrite all 300 RC items from content/rc_v43_[a-k].json.

v42.0.2 gave every passage the same five question types (main idea / sequence /
purpose / detail / word-meaning). The official-blueprint gap analysis
(qa/R3-BLUEPRINT-ALIGNMENT.md gap 3) asks for detail items to be the most
frequent type and for the missing types -- TRUE-statement, reference,
paraphrase and attitude/tone -- to appear. Each spec item carries an explicit
`type`; tips come from content/rc_v43_tips.json (one per type).
Answer positions are assigned greedily so the bank stays 75/75/75/75.
"""
import json,glob,sys,os,collections
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V};order=[q['id'] for q in V]
rc=[q for q in V if q['kind']=='rc']
assert len(rc)==300,len(rc)
P=[]
for f in sorted(glob.glob('content/rc_v43_[a-k].json')): P+=json.load(open(f))
assert len(P)==60,len(P)
TIPS=json.load(open('content/rc_v43_tips.json'))
REASON=('RC v43 question-type mix: v42.0.2 repeated the same five question types on every '
        'passage (main idea / sequence / purpose / detail / word meaning) with no TRUE-statement, '
        'reference, paraphrase or attitude item; all 300 items rewritten so detail is the most '
        'frequent type (120/300) and every type in qa/R3-BLUEPRINT-ALIGNMENT.md gap 3 is present')
TAG='RC-rewrite'
USED=collections.Counter()
n=0
for p in P:
    i0=order.index(p['first']);ids=order[i0:i0+5]
    assert all(by[x]['kind']=='rc' for x in ids),(p['first'],ids)
    assert len({by[x]['context'] for x in ids})==1,p['first']
    if 'context' in p: assert 100<=len(p['context'].split())<=200,(p['first'],len(p['context'].split()))
    assert len(p['items'])==5,(p['first'],len(p['items']))
    for it,qid in zip(p['items'],ids):
        q=by[qid]
        pos=min(range(4),key=lambda x:(USED[x],(x-n)%4));USED[pos]+=1
        opts=list(it['d']);opts.insert(pos,it['key'])
        assert len(set(opts))==4,(qid,opts)
        new={'prompt':it['prompt'],'options':opts,'answer':pos,
             'explanation':it['exp'],'tip':TIPS[it['type']]}
        if 'context' in p:  # v43 C4 (Claude): new-genre passage replaces the frozen context
            new['context']=p['context'];new['topic']=p['topic']
        for fld,val in new.items():
            if q[fld]!=val:
                log(qid,fld,q[fld],val,REASON,TAG);q[fld]=val
        n+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('items',n)
print('positions',dict(sorted(collections.Counter(q['answer'] for q in rc).items())))
print('tips',len({q['tip'] for q in rc}))
