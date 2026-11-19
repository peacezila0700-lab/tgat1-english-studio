"""Round-3 content regressions (static). Usage: python3 regression_r3_content.py WEBDIR
Each check guards a defect fixed in v42.0.2 so it cannot silently return."""
import json,re,sys,subprocess,os,collections
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(HERE)
web=sys.argv[1];tmp='/tmp/r3extract'
subprocess.run(['node',os.path.join(ROOT,'tools','datafiles.js'),'extract',web,tmp],check=True,capture_output=True)
V=json.load(open(f'{tmp}/vault.json'));D=json.load(open(f'{tmp}/data.json'))
R=[]
def check(n,c,d=''): R.append((n,bool(c),d));print(('PASS ' if c else 'FAIL ')+n+('' if c else f'  [{d}]'))
by=collections.defaultdict(list)
for q in V: by[q['kind']].append(q)
check('bank: 1,200 items, 4 unique options, valid key',len(V)==1200 and all(len(set(q['options']))==4 and 0<=q['answer']<4 for q in V))
bp=collections.Counter((q['set'],q['kind']) for q in V)
check('bank: per-set blueprint 10/10/10/15/15 unchanged',all(bp[(s,k)]==n for s in range(1,21) for k,n in [('qr',10),('short',10),('long',10),('tc',15),('rc',15)]))
lc=by['long'];ctx=collections.Counter(q['context'] for q in lc)
check('LC: 40 unique contexts × 5 items',len(ctx)==40 and set(ctx.values())=={5})
tmpl=[q['id'] for q in lc if re.search(r"Don’t worry about overspending|glance over my draft|Keeping it under \d+ baht",q['context'])]
check('LC: v42.0.1 fixed dialogue template removed (regression for round-3 LC rewrite)',not tmpl,tmpl[:3])
reuse=collections.Counter(o for q in lc for i,o in enumerate(q['options']) if i!=q['answer'])
check('LC: no distractor reused verbatim in more than 2 items',max(reuse.values())<=2,reuse.most_common(2))
check('LC: dialogues use contractions (no “Let us” / “I will”)',not [q for q in lc if re.search(r'\bLet us\b|\bI will\b',q['context'])])
check('LC: no stem refers to undefined “that step”',not [q for q in lc if 'that step' in q['prompt']])
for q in lc:
    if '(1) ____' in q['context']:
        n=re.search(r'blank \((\d)\)',q['prompt']).group(1)
        if f'({n}) ____' not in q['context']: check('LC blank number exists '+q['id'],False);break
L=[len(o) for q in lc for o in [q['options'][q['answer']]]]
lg=sum(len(q['options'][q['answer']])==max(map(len,q['options'])) for q in lc)/len(lc)
check('LC: key is longest option in ≤30% of items (v42.0.1: 50.5%)',lg<=0.30,f'{lg:.3f}')
tc=by['tc'];tg=collections.OrderedDict()
for q in tc: tg.setdefault(q['context'],[]).append(q)
check('TC: 40 passages, blank count equals item count',len(tg)==40 and all(len(re.findall(r'\(\d+\) _+',c))==len(g) for c,g in tg.items()))
check('TC: answer positions balanced 75/75/75/75',collections.Counter(q['answer'] for q in tc)==collections.Counter({0:75,1:75,2:75,3:75}))
off=[('Sidewalk','editor will review the guide'),('Emergency contact','send a new report'),('energy club','return the kit'),('makerspace','test the phone list'),('Wildlife','return costumes'),('produce storage','The club will present'),('mural','Riders can register'),('study circles','library will publish a calendar'),('crossing','share its schedule')]
bad=[t for t,p in off for c,g in tg.items() if p in c and t.lower() in g[0]['topic'].lower()]
check('TC: off-topic sentences copied from other passages removed',not bad,bad)
def blank_sent(q):
    n=re.search(r'blank \((\d+)\)',q['prompt']).group(1);m=re.search(r'[^.!?]*\('+n+r'\)\s*_+[^.!?]*',q['context']);return m.group(0) if m else ''
amb=[q['id'] for q in tc if set(q['options'])>={'safe','safer'} or set(q['options'])>={'so','so that'} or (set(q['options'])>={'which','that'} and q['options'][q['answer']]=='that' and not re.search(r'note \(\d+\)',blank_sent(q))) or (set(q['options'])>={'with','to'} and 'compare' in blank_sent(q))]
check('TC: known ambiguous option pairs removed (safe/safer, so/so that, which/that, compare with/to)',not amb,amb[:5])
check('TC: seed-exchange key is not “little” before a shade contrast',not [q for q in tc if 'Some herbs need (4)' in q['context'] and q['options'][q['answer']]=='little'])
check('TC: explanations are Thai (no English boilerplate)',not [q for q in tc if 'fits the sentence grammar and meaning' in q['explanation'] or not re.search('[฀-๿]',q['explanation'])])
rc=by['rc']
TPL=r'neighboring towns|before reviewing any participant|already solved every participant|suspended all regular activities|outside consulting firm|strict government penalty|commercial business'
check('RC: recycled template distractors removed',not [q['id'] for q in rc if re.search(TPL,' '.join(q['options']))])
def topic(q): return re.sub(r'[-‐–]',' ',re.sub(r'^(a|an|the)\s+','',q['topic'],flags=re.I).lower())
s1=0
for q in rc:
    keep=[i for i in range(4) if topic(q) not in re.sub(r'[-‐–]',' ',q['options'][i].lower())] or list(range(4))
    s1+=max(keep,key=lambda i:len(q['options'][i]))==q['answer']
check('RC: test-wise heuristic (drop topic name, pick longest) ≤35% (v42.0.1: 81.3%)',s1/300<=0.35,f'{s1/300:.3f}')
lgr=sum(len(q['options'][q['answer']])==max(map(len,q['options'])) for q in rc)/300
check('RC: key is longest option in ≤30% of items (v42.0.1: 53.3%)',lgr<=0.30,f'{lgr:.3f}')
check('RC: no truncated mid-word evidence in explanations',not [q['id'] for q in rc if 'ว่า rain was' in q['explanation']])
st=[q for q in rc if re.search(r'What problem was the group trying to address\?|Which concern prompted',q['prompt']) and q['options'][q['answer']].lower().startswith('to ')]
check('RC: no “problem/concern” stem answered by a purpose infinitive',not st,[q['id'] for q in st][:3])
check('practice disclaimer present in index.html',('ไม่ใช่ข้อสอบทางการ' in open(os.path.join(web,'index.html'),encoding='utf-8').read()))

# ---- added in the merge pass (round 3) ----
norm=lambda x:re.sub(r'\s+',' ',x.replace('’',"'").replace('‘',"'")).strip().lower()
badq=[]
for q in by['long']+by['rc']:
    hay=norm(q['context']+' '+' '.join(q['options'])+' '+q['prompt'])
    for m in re.findall(r'“([^”]+)”',q['explanation']):
        if re.search('[A-Za-z]{3}',m) and not all(norm(pp).strip(' .') in hay for pp in re.split(r'\.\.\.|…',m) if pp.strip()): badq.append(q['id'])
check('LC/RC: every English quotation in an explanation exists in the item text',not badq,badq[:5])
check('RC: answer positions balanced 75/75/75/75',collections.Counter(q['answer'] for q in by['rc'])=={0:75,1:75,2:75,3:75})
nm=sum(1 for q in by['rc'] for i,o in enumerate(q['options']) if i!=q['answer'] and re.sub(r'^(a|an|the) ','',q['topic'].lower()) in o.lower())
check('RC: distractors no longer repeat the passage topic name (v42.0.1: 67% of distractors)',nm<=3,nm)
sec=sum(sorted(range(4),key=lambda i:-len(q['options'][i])).index(q['answer'])==1 for q in by['rc'])/300
check('RC: second-longest-option strategy ≤50% (documented residual cue)',sec<=0.50,f'{sec:.3f}')
TCC=['editor will review the guide','Families can return the kit','Players can return costumes','Riders can register','coordinator will test the phone list','The club will present its findings','library will publish a calendar','group will share its schedule']
check('TC: sentences copied from other passages are gone',not [q['id'] for q in by['tc'] if any(t in q['context'] for t in TCC)])
W={w['w']:w for w in D['studio']['words']}
check('IPA: stress mark at syllable onset for CMUdict entries (compare, explain)',W['compare']['ipa']=='/kəmˈpɛɹ/' and W['explain']['ipa']=='/ɪkˈspleɪn/',(W['compare']['ipa'],W['explain']['ipa']))
check('vocab: no headword deleted in round 3 (3,508 studio words)',len(D['studio']['words'])==3508,len(D['studio']['words']))
# ---- v43 gates (added by Claude, v43 round after Arena 16:13) ----
# G-A: RC question-type mix (types live in content/ specs; vault has no type field)
import glob as _glob
_rc_types=collections.Counter()
for _f in _glob.glob(os.path.join(ROOT,'content','rc_v43_[a-k].json')):
    for _p in json.load(open(_f,encoding='utf-8')):
        for _it in _p['items']: _rc_types[_it['type']]+=1
check('RC v43: detail is the most frequent type (>=110)',_rc_types['detail']>=110 and _rc_types['detail']==max(_rc_types.values()),dict(_rc_types))
check('RC v43: words-in-context >= 55 (target 3 per 15 items)',_rc_types['wic']>=55,_rc_types['wic'])
check('RC v43: TRUE/paraphrase/attitude/reference each >= 12',all(_rc_types[t]>=12 for t in ('true','paraphrase','attitude','reference')),{t:_rc_types[t] for t in ('true','paraphrase','attitude','reference')})
# G-B: RC context-overlap heuristic <= 0.35 (v43 Arena: 51.7%)
_stop=set('the a an of to in for and or is are was were be been with that this it they as at on by from'.split())
def _ov(q,o):
    cw={w for w in re.findall(r"[a-z']+",q['context'].lower()) if w not in _stop}
    return len({w for w in re.findall(r"[a-z']+",o.lower()) if w not in _stop}&cw)
_hit=sum(max(range(4),key=lambda i:_ov(q,q['options'][i]))==q['answer'] for q in rc)
check('RC: max-context-overlap heuristic <=35% (v43 Arena: 51.7%)',_hit/300<=0.35,f'{_hit/300:.3f}')
# G-C: TC answer-longest <= 35% (v43 Arena: 42%)
_tcl=sum(len(q['options'][q['answer']])==max(map(len,q['options'])) for q in by['tc'])
check('TC: key is the longest option <=35% (v43 Arena: 42%)',_tcl/300<=0.35,f'{_tcl/300:.3f}')
# G-D: Short conversation context-overlap <= 35% (v43 Arena: 67%)
_sh=by['short']
_shl=sum(max(range(4),key=lambda i:_ov(q,q['options'][i]))==q['answer'] for q in _sh)
check('Short conv: context-overlap heuristic <=35% (v43 Arena: 67%)',_shl/len(_sh)<=0.35,f'{_shl/len(_sh):.3f}')
# G-E: Q-R idiom items >= 60 (C5; v43 Arena counted 3)
_qi=[q for q in by['qr'] if q.get('topic')=='Idioms and expressions']
check('Q-R: idiom/fixed-expression items >= 60 (v43 Arena: 3)',len(_qi)>=60,len(_qi))
check('Q-R: answer positions balanced 50/50/50/50',collections.Counter(q['answer'] for q in by['qr'])=={0:50,1:50,2:50,3:50})
# G-F: extreme-word cue: answer vs distractor rate within 1.5x (TC excluded: options are single function words)
_EX=re.compile(r'\b(all|every|everyone|always|never|no one|nobody|nothing|only|must|completely|totally|impossible|guaranteed)\b',re.I)
_er={}
for _k in ('rc','long','short','qr'):
    _qs=by[_k];_a=sum(bool(_EX.search(q['options'][q['answer']])) for q in _qs)/len(_qs)
    _d=sum(bool(_EX.search(o)) for q in _qs for i,o in enumerate(q['options']) if i!=q['answer'])/(3*len(_qs))
    _er[_k]=(round(_a,3),round(_d,3))
check('extreme-word rate: answer vs distractor within 1.5x in rc/long/short/qr (v43 Arena RC 0.067 vs 0.194)',all(max(a,d)<=1.5*min(a,d)+1e-9 for a,d in _er.values()),_er)
# G-G: RC passages are not near-duplicates (C4; v43 Arena found S14-Q056/S20-Q051 at 0.309) + new genres present
import itertools as _it
_st=set('the a an of to in for and or is are was were be been with that this it they as at on by from their more some had but not when which than so who could would can also each one two its after before then them other only did over into about'.split())
_P={q['id']:{w for w in re.findall(r"[a-z]+",q['context'].lower()) if w not in _st and len(w)>2} for q in rc[::5]}
_mx=max((len(_P[a]&_P[b])/len(_P[a]|_P[b]),a,b) for a,b in _it.combinations(_P,2))
check('RC: no passage pair with word overlap >0.25 (v43 Arena: 0.309)',_mx[0]<=0.25,f'{_mx[0]:.3f} {_mx[1]}/{_mx[2]}')
_gen=collections.Counter(_p.get('genre','project report') for _f in _glob.glob(os.path.join(ROOT,'content','rc_v43_[a-k].json')) for _p in json.load(open(_f,encoding='utf-8')))
check('RC: at least 5 passage genres (C4)',len(_gen)>=5,dict(_gen))
# G-H: Q-R distractors must not be canned sentences reused across items
# (Arena round 2 found 17 sentences covering 230 of 600 slots in 101 items -
#  recognising a recycled sentence removed an option without reading the question)
_qd=collections.Counter(o for q in by['qr'] for i,o in enumerate(q['options']) if i!=q['answer'])
_re=sorted([(n,s) for s,n in _qd.items() if n>=3],reverse=True)
check('Q-R: no distractor sentence reused in >=3 items (v43 Claude: 17 sentences x10-17)',not _re,_re[:3])
# G-I: Q-R length cues (v43 Claude: longest 0.275 / shortest 0.270)
_ql=sum(len(q['options'][q['answer']])==max(map(len,q['options'])) for q in by['qr'])/len(by['qr'])
_qsh=sum(len(q['options'][q['answer']])==min(map(len,q['options'])) for q in by['qr'])/len(by['qr'])
check('Q-R: key is the longest option <=25% (v43 Claude 0.275, Arena round 2 0.205)',_ql<=0.25,f'{_ql:.3f}')
check('Q-R: key is the shortest option <=30% (v43 Claude 0.270)',_qsh<=0.30,f'{_qsh:.3f}')
f=[r for r in R if not r[1]];print(f'\nregression_r3_content: {len(R)-len(f)}/{len(R)} passed');sys.exit(1 if f else 0)
