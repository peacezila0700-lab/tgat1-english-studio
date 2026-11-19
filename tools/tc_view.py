import json,collections,re,sys
V=json.load(open('data/vault.json'))
qs=[q for q in V if q['kind']=='tc'];ctx=collections.OrderedDict()
for q in qs: ctx.setdefault(q['context'],[]).append(q)
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,(c,ql) in enumerate(list(ctx.items())[a-1:b],a):
    t=c
    for k,q in enumerate(ql,1):
        o=q['options'];key=o[q['answer']];ds=[x for j,x in enumerate(o) if j!=q['answer']]
        t=t.replace(f'({k}) ____',f'[{k}:{key.upper()} | {"/".join(ds)}]')
    print(f'TC{i:02d} {ql[0]["id"]}: {t}\n')
