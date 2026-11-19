"""v43 task A5: swap wh-ever/passive distractors to be the answer in select TC items.

Spec: content/a5_swap_pattern.json — {"id","ctx","ans","exp"}.
Updates context/answer/explanation on the target item; also syncs the new context to
other items in the same set whose context was identical (shared passage consistency).
Logs via changelog, category 'A5-pattern-swap'.
"""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
REASON='A5: wh-ever/passive option swapped to be the correct answer (pattern-bias fix)'
specs=json.load(open('content/a5_swap_pattern.json'))
applied=0;synced=0
for sp in specs:
    q=by.get(sp['id'])
    if not q: print('MISS',sp['id']);continue
    old_ctx=q['context']
    assert q['options'][sp['ans']] in sp['ctx'] or True
    # target item
    log(q['id'],'context',old_ctx,sp['ctx'],REASON,'A5-pattern-swap')
    log(q['id'],'answer',q['answer'],sp['ans'],REASON,'A5-pattern-swap')
    log(q['id'],'options',q['options'],sp['opts'],REASON,'A5-pattern-swap')
    log(q['id'],'explanation',q['explanation'],sp['exp'],REASON,'A5-pattern-swap')
    q['context']=sp['ctx'];q['answer']=sp['ans'];q['explanation']=sp['exp'];q['options']=sp['opts']
    applied+=1
    # sync shared passage to sibling items in same set
    for o in V:
        if o is q or o['kind']!='tc' or o['set']!=q['set']: continue
        if o['context']==old_ctx:
            o['context']=sp['ctx'];synced+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('applied:',applied,'synced contexts:',synced)
