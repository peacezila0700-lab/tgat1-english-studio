import json,collections,sys
sys.path.insert(0,'tools');from rc_types import rc_type
V=json.load(open(sys.argv[3] if len(sys.argv)>3 else 'data/vault.json'))
qs=[q for q in V if q['kind']=='rc'];ctx=collections.OrderedDict()
for q in qs: ctx.setdefault(q['context'],[]).append(q)
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,(c,ql) in enumerate(list(ctx.items())[a-1:b],a):
    print(f'== RC{i:02d} {ql[0]["id"]} [{ql[0]["topic"]}]\n{c}')
    for q in ql:
        print(f' - {q["id"]} <{rc_type(q["prompt"])}> {q["prompt"]}')
        for j,o in enumerate(q['options']): print('    ','*' if j==q['answer'] else ' ',o)
