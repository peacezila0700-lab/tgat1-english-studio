import json,collections,sys
V=json.load(open('data/vault.json'))
qs=[q for q in V if q['kind']=='rc'];ctx=collections.OrderedDict()
for q in qs: ctx.setdefault(q['context'],[]).append(q)
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,(c,ql) in enumerate(list(ctx.items())[a-1:b],a):
    assert len(ql)==5
    print(f'== RC{i:02d} {ql[0]["id"]} [{ql[0]["topic"]}]\n{c}')
    print('   P3:',ql[2]['prompt'],'->',ql[2]['options'][ql[2]['answer']],' | V4:',ql[3]['prompt'])
