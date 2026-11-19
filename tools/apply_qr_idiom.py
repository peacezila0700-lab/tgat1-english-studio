"""v43 (Claude): Question-Response idiom items from content/qr_idiom_v43_[a-z].json (BACKLOG C5).

Q-R had ~5/200 idiom items and 140/200 items built from 27 recycled distractor strings
("It was closed last week.", "Since last Tuesday." ...). 60 of the most-recycled items
(3 per set) are replaced by idiom/fixed-expression items whose distractors use the idiom's
words literally (the classic trap) or answer a different question. The answer index of the
replaced item is kept so positions stay 50/50/50/50; old_prompt is asserted.
"""
import json,glob,sys,os
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
REASON=('Q-R v43 idioms (C5): recycled-template item replaced by an idiom/fixed-expression item; '
        'distractors use the idiom words literally or answer another question')
n=0
for f in sorted(glob.glob('content/qr_idiom_v43_[a-z].json')):
    for e in json.load(open(f,encoding='utf-8')):
        q=by[e['id']];assert q['kind']=='qr' and q['prompt']==e['old_prompt'],e['id']
        assert q['answer']==e['answer'] and len(set(e['options']))==4,e['id']
        for fld in ('prompt','options','answer','explanation','tip','topic'):
            if q[fld]!=e[fld]: log(q['id'],fld,q[fld],e[fld],REASON,'QR-idiom');q[fld]=e[fld]
        n+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('qr idiom items',n)
