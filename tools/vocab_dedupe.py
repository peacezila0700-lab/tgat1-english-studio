"""Remove two exact reverse-duplicate pairs (verifiable: same two words, already present in reverse order)."""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
D=json.load(open('data/data.json'))
ant=D['legacy']['ANT'];seen=set();keep=[]
for r in ant:
    k=frozenset((r[0].lower(),r[1].lower()))
    if k in seen: log('legacy.ANT',"pair",json.dumps(r,ensure_ascii=False),'(removed)','exact reverse duplicate of an earlier antonym pair; games picked it twice as often','VOCAB-dedupe');continue
    seen.add(k);keep.append(r)
D['legacy']['ANT']=keep
cf=D['studio']['confused'];seen=set();keep=[]
for r in cf:
    k=frozenset((r['a'].lower(),r['b'].lower()))
    if k in seen: log('studio.confused',"pair",json.dumps(r,ensure_ascii=False),'(removed; note kept on the first entry)','exact reverse duplicate of an earlier confusable pair shown twice in the list','VOCAB-dedupe');continue
    seen.add(k);keep.append(r)
D['studio']['confused']=keep
json.dump(D,open('data/data.json','w'),ensure_ascii=False,indent=1);print(len(D['legacy']['ANT']),len(D['studio']['confused']))
# definite gloss fix: repeated part
for w in D['studio']['words']:
    if w['w']=='publish' and w['th']=='ตีพิมพ์; เผยแพร่; ตีพิมพ์':
        log('studio.words:publish','th',w['th'],'ตีพิมพ์; เผยแพร่','gloss repeated the same Thai meaning twice','VOCAB-gloss');w['th']='ตีพิมพ์; เผยแพร่'
for v in D['legacy']['V']:
    if v[0]=='publish' and v[1]=='ตีพิมพ์; เผยแพร่; ตีพิมพ์': v[1]='ตีพิมพ์; เผยแพร่'
json.dump(D,open('data/data.json','w'),ensure_ascii=False,indent=1)
