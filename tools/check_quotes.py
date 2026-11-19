"""Verify that English quotations inside explanations exist in the context or options (evidence integrity)."""
import json,re,sys
V=json.load(open(sys.argv[1]));kinds=sys.argv[2:]
bad=0;tot=0
norm=lambda s:re.sub(r'\s+',' ',s.replace('’',"'").replace('‘',"'")).strip().lower()
for q in V:
    if q['kind'] not in kinds: continue
    hay=norm(q['context']+' '+' '.join(q['options'])+' '+q['prompt'])
    for m in re.findall(r'“([^”]+)”',q['explanation']):
        if not re.search('[A-Za-z]{3}',m): continue
        tot+=1
        parts=[p for p in re.split(r'\.\.\.|…',m) if p.strip()]
        if not all(norm(p).strip(' .') in hay for p in parts):
            bad+=1;print(q['id'],'|',m[:90])
print('quotes checked',tot,'not found',bad)
