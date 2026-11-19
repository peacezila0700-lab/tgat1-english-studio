"""Test-wiseness heuristics for RC (and other kinds). Accuracy of answer-without-reading strategies.
usage: rc_heuristics.py vault.json [kind]"""
import json,sys,re,statistics as st,collections
V=json.load(open(sys.argv[1]));kind=sys.argv[2] if len(sys.argv)>2 else 'rc'
qs=[q for q in V if q['kind']==kind]
EXT=re.compile(r"\b(all|every|entire|entirely|never|always|permanently|completely|immediately|only|any|no one|nobody|everyone|nothing|must|whole|totally|forever|ban|banned|cancel\w*|refus\w*|stop\w*)\b",re.I)
STOP=set('the a an of to and in on for with by at from is are was were be been that this it its as or but not their they them'.split())
def topic(q): return re.sub(r'^(a|an|the)\s+','',q['topic'].strip().lower())
def norm(s): return re.sub(r'[-‐]',' ',s.lower())
def toks(s): return [w for w in re.findall(r"[a-z][a-z'-]+",s.lower()) if w not in STOP]
def H_longest(q): L=[len(o) for o in q['options']];return L.index(max(L))
def H_name(q):
    t=norm(topic(q));cand=[i for i,o in enumerate(q['options']) if t not in norm(o)] or [0,1,2,3]
    return max(cand,key=lambda i:len(q['options'][i]))
def H_extreme(q):
    cand=[i for i,o in enumerate(q['options']) if not EXT.search(o)] or [0,1,2,3]
    return max(cand,key=lambda i:len(q['options'][i]))
def H_overlap(q):
    c=set(toks(q['context']));sc=[len(set(toks(o))&c)/max(1,len(set(toks(o)))) for o in q['options']];return sc.index(max(sc))
def H_combo(q):
    t=norm(topic(q))
    cand=[i for i,o in enumerate(q['options']) if t not in norm(o) and not EXT.search(o)] or [i for i,o in enumerate(q['options']) if not EXT.search(o)] or [0,1,2,3]
    c=set(toks(q['context']))
    return max(cand,key=lambda i:(len(set(toks(q['options'][i]))&c)/max(1,len(set(toks(q['options'][i])))),len(q['options'][i])))
H={'longest':H_longest,'no-topic-name+longest':H_name,'no-extreme-word+longest':H_extreme,'max-context-overlap':H_overlap,'combined(no name,no extreme,overlap)':H_combo}
res={k:round(sum(f(q)==q['answer'] for q in qs)/len(qs),3) for k,f in H.items()}
ext_ans=sum(bool(EXT.search(q['options'][q['answer']])) for q in qs)/len(qs)
ext_dis=sum(sum(bool(EXT.search(o)) for i,o in enumerate(q['options']) if i!=q['answer']) for q in qs)/len(qs)/3
name_dis=sum(sum(norm(topic(q)) in norm(o) for i,o in enumerate(q['options']) if i!=q['answer']) for q in qs)/len(qs)/3
name_ans=sum(norm(topic(q)) in norm(q['options'][q['answer']]) for q in qs)/len(qs)
print(json.dumps({'kind':kind,'n':len(qs),'heuristic_accuracy (chance=0.25)':res,'extreme_word_rate_answer':round(ext_ans,3),'extreme_word_rate_distractor':round(ext_dis,3),'topic_name_rate_answer':round(name_ans,3),'topic_name_rate_distractor':round(name_dis,3)},indent=1,ensure_ascii=False))
