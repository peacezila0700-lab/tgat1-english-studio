"""Test-wise heuristic solvers for RC (no passage reading). Usage: rc_solver.py vault.json"""
import json,sys,re,collections
V=json.load(open(sys.argv[1]));qs=[q for q in V if q['kind']==(sys.argv[2] if len(sys.argv)>2 else 'rc')]
STOP=set('the a an of to and in on for with by at from is was were be that this it its as or but not their they them how why what which who'.split())
def norm(s): return re.sub(r'[-‐–]',' ',s.lower())
def topic(q): return norm(re.sub(r'^(a|an|the)\s+','',q['topic'],flags=re.I))
def toks(s): return [w for w in re.findall(r"[a-z]+",s.lower()) if w not in STOP]
n=len(qs);acc=collections.Counter()
for q in qs:
    o=q['options'];a=q['answer'];L=[len(x) for x in o];t=topic(q)
    # S1: drop options containing the topic phrase, then longest
    keep=[i for i in range(4) if t not in norm(o[i])] or list(range(4))
    s1=max(keep,key=lambda i:L[i]);acc['S1 drop-topic-name then longest']+= s1==a
    acc['S2 longest']+= L.index(max(L))==a
    c=set(toks(q['context']));ov=[len(set(toks(x))&c)/max(1,len(set(toks(x)))) for x in o]
    acc['S3 max passage-word overlap']+= ov.index(max(ov))==a
    acc['S4 option lacks topic name (any)']+= (t not in norm(o[a])) and sum(t in norm(x) for x in o)>=2
print(json.dumps({k:round(v/n,3) for k,v in acc.items()},indent=1),'n=',n,' chance=0.25')
