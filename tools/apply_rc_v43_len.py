#!/usr/bin/env python3
"""Apply option-length patches to content/rc_v43_*.json.

Patch file format: list of [first_id, slot, old_distractor, new_distractor].
The RC key-longest gate needs a distractor strictly longer than the key in most
items; these patches expand one plausible distractor per item without changing
which option is correct.
"""
import json, glob, sys

patch = json.load(open(sys.argv[1], encoding='utf-8'))
specs = {}
for f in sorted(glob.glob('content/rc_v43_[a-k].json')):
    for p in json.load(open(f, encoding='utf-8')):
        specs[p['first']] = (f, p)
n = 0
for first, slot, old, new in patch:
    f, p = specs[first]
    d = p['items'][slot]['d']
    if old not in d:
        print('MISS', first, slot, old); sys.exit(1)
    if d.count(old) != 1:
        print('AMBIGUOUS', first, slot, old); sys.exit(1)
    d[d.index(old)] = new
    n += 1
for f in {specs[k][0] for k in specs}:
    data = [p for k, (ff, p) in specs.items() if ff == f]
    data.sort(key=lambda p: p['first'])
    json.dump(data, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('patched', n, 'distractors')
