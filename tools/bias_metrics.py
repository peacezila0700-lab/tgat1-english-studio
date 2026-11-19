"""Option-cue metrics for the question bank. Usage: bias_metrics.py vault.json [kind...]"""
import json,sys,re,collections,statistics as st
V=json.load(open(sys.argv[1]));kinds=sys.argv[2:] or ['rc','long','short','tc','qr']
STOP=set('the a an of to and in on for with by at from is are was were be been that this it its as or but not their they them he she his her we our you your will can may should would could has have had do does did which who what when where why how than then so if into about over after before during more most less only also all any some each other such one two three'.split())
def toks(s): return [w for w in re.findall(r"[a-z][a-z'-]+",s.lower()) if w not in STOP]
def caps(s): return set(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*",s))
def metrics(qs):
    n=len(qs);longest=uniq_longest=shortest=0;ratios=[];overlap_top=0;ctxname_ans=ctxname_dis=0;topic_ans=0;topic_dis=0;zl=[]
    for q in qs:
        L=[len(o) for o in q['options']];a=q['answer'];mx=max(L)
        if L[a]==mx: longest+=1
        if L[a]==mx and L.count(mx)==1: uniq_longest+=1
        if L[a]==min(L): shortest+=1
        others=[L[i] for i in range(4) if i!=a];ratios.append(L[a]/(sum(others)/3))
        sd=st.pstdev(L) or 1;zl.append((L[a]-st.mean(L))/sd)
        c=set(toks(q['context']));ov=[len(set(toks(o))&c)/max(1,len(set(toks(o)))) for o in q['options']]
        if ov[a]==max(ov) and ov.count(max(ov))==1: overlap_top+=1
        tw=set(toks(q.get('topic','')))
        has=[bool(tw and tw<=set(toks(o))) for o in q['options']]
        topic_ans+=has[a];topic_dis+=sum(has)-has[a]
    return dict(n=n,answer_longest=round(longest/n,3),answer_unique_longest=round(uniq_longest/n,3),answer_shortest=round(shortest/n,3),
        mean_len_ratio=round(st.mean(ratios),3),mean_len_z=round(st.mean(zl),3),answer_unique_top_context_overlap=round(overlap_top/n,3),
        topic_phrase_in_answer=round(topic_ans/n,3),topic_phrase_in_distractors_per_q=round(topic_dis/n,3))
out={}
for k in kinds:
    qs=[q for q in V if q['kind']==k]
    if qs: out[k]=metrics(qs)
    # by prompt type for rc
print(json.dumps(out,indent=1))
