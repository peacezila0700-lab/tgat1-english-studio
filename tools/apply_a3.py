"""v43 task A3: rewrite explanations so each mentions at least one word (>=4 chars) from every distractor.

Specs: content/a3_exp_*.json — list of {"id": "...", "exp": "new explanation"}.
Applies to data/vault.json items of kind tc/rc, logs via changelog, tag 'A3-explanation'.
"""
import json,glob,sys,os,re
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
REASON='A3: explanation rewritten to explicitly address every distractor option'
specs=[]
for f in sorted(glob.glob('content/a3_exp_*.json')): specs+=json.load(open(f))
print('specs:',len(specs))
applied=0;skip=0
for sp in specs:
    q=by.get(sp['id'])
    if not q: print('MISS',sp['id']);skip+=1;continue
    if q['kind'] not in ('tc','rc'): print('WRONGKIND',sp['id'],q['kind']);skip+=1;continue
    if q['explanation']==sp['exp']: skip+=1;continue
    log(q['id'],'explanation',q['explanation'],sp['exp'],REASON,'A3-explanation')
    q['explanation']=sp['exp']
    applied+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('applied:',applied,'skipped:',skip)
