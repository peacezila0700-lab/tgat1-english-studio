"""v43 task 2: replace all 40 TC passages with rebalanced specs (content/tc_v43_[a-j].json).

Target mix per the official-blueprint gap analysis: ~40-50% vocabulary/collocation blanks
plus the grammar types missing in v42 (verb forms, tense/voice, relative/noun clause,
inversion, question tags, connectors). Answer positions use (j*3+j//8)%4 -> exactly 75/75/75/75.
"""
import json,glob,sys,os,re,collections
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
qs=[q for q in V if q['kind']=='tc']
assert len(qs)==300,len(qs)
# Load all specs; later files (k,l = C4 new-genre) override earlier ones by (set,passage)
seen={}
_loaded=0
for f in sorted(glob.glob('content/tc_v43_[a-l].json')):
    for g in json.load(open(f)):
        seen[(g['set'],g['passage'])]=g  # later files win
        _loaded+=1
groups=[seen[k] for k in seen]
assert _loaded==60,_loaded
assert len(groups)==40,len(groups)
REASON='TC v43 rebalance: v42.0.2 had 241/300 function-word blanks and no inversion/question-tag/verb-form spread; passages rewritten with ~40-50% vocabulary/collocation and the grammar types listed in qa/R3-BLUEPRINT-ALIGNMENT.md'
# split vault tc items into per-set passages: 7 items (A) then 8 items (B) per set
byp=collections.defaultdict(list)
for q in qs: byp[q['set']].append(q)
passages=[]
for s in range(1,21):
    g=byp[s]
    assert len(g)==15,(s,len(g))
    passages.append(g[:7]); passages.append(g[7:])
gi=0
for g,(spec) in zip(passages,groups):
    assert spec['set']==g[0]['set'] and {'A':7,'B':8}[spec['passage']]==len(g),(spec['set'],spec['passage'],g[0]['id'])
    c=spec['context']
    assert len(re.findall(r'\(\d+\) _+',c))==len(g)==len(spec['items']),spec['set']
    for k,(q,it) in enumerate(zip(g,spec['items'])):
        assert f'({k+1}) ____' in c,(spec['set'],k)
        assert q['prompt']==f'Which choice best completes blank ({k+1}) in context?',(q['id'],q['prompt'])
        pos=(gi*3+gi//8)%4
        opts=list(it['d']);opts.insert(pos,it['key'])
        assert len(opts)==4 and len(set(opts))==4,(q['id'],opts)
        new={'context':c,'options':opts,'answer':pos,'explanation':it['exp'],'tip':spec['tip'],'topic':spec['topic']}
        for fld,val in new.items():
            if q[fld]!=val:
                log(q['id'],fld,q[fld],val,REASON,'TC-rewrite');q[fld]=val
        gi+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('updated',gi)
print(collections.Counter(q['answer'] for q in qs))
print(collections.Counter(it['type'] for sp in groups for it in sp['items']))
