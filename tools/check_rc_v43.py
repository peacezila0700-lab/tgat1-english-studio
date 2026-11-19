#!/usr/bin/env python3
"""Validate rc_v43_*.json spec files before applying them.

Checks per item: 4 options total (key + 3 distractors, all distinct, none empty),
Thai explanation present and Latin-free of stray foreign scripts, quoted spans in
the prompt actually occur in the passage context, and the per-passage type order
matches /tmp/rc_typeplan.json (passages 20-59) where a plan exists.
"""
import json, re, sys, glob, collections

ALLOWED = re.compile(r'[\u0E00-\u0E7F\x00-\x7F\u2018\u2019\u201C\u201D\u2013\u2014\u2026\u00E9\u2192]')
QUOTE = re.compile(r'\u201C([^\u201D]{6,})\u201D')
STRIPCH = '"\'.;,'

def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u2019', "'").replace('\u201C', '"').replace('\u201D', '"')).strip()

def load_passages():
    """Passage contexts the specs were written against.

    /tmp/rc_passages.json was a scratch file of the authoring session and does not
    survive a sandbox reset, so fall back to data/vault.json (RC items are stored
    five per passage and task 3 never changed a context)."""
    import os
    if os.path.exists('/tmp/rc_passages.json'):
        return {p['first']: p for p in json.load(open('/tmp/rc_passages.json'))}
    V = json.load(open('data/vault.json', encoding='utf-8'))
    rc = [q for q in V if q.get('kind') == 'rc']
    out = {}
    for i in range(0, len(rc), 5):
        g = rc[i:i + 5]
        out[g[0]['id']] = {'first': g[0]['id'], 'set': g[0].get('set'),
                           'context': g[0]['context'], 'ids': [x['id'] for x in g]}
    print(f'INFO /tmp/rc_passages.json missing - rebuilt {len(out)} passage contexts from data/vault.json')
    return out

passages = load_passages()
plan = {}
try:
    rows = json.load(open('/tmp/rc_typeplan.json'))
    keys = [k for k in passages]
    for i, r in enumerate(rows):
        plan[keys[20 + i]] = r
except Exception as e:
    print('WARN no typeplan:', e)

errs, types = [], collections.Counter()
files = sorted(glob.glob('content/rc_v43_[a-k].json'))
n = 0
for f in files:
    data = json.load(open(f, encoding='utf-8'))
    for p in data:
        first = p['first']
        if first not in passages:
            errs.append(f'{f}: unknown first id {first}'); continue
        ctx = norm(p.get('context') or passages[first]['context'])  # v43 C4: new-genre passages carry their own context
        ids = passages[first]['ids']
        if len(p['items']) != len(ids):
            errs.append(f'{f}/{first}: {len(p["items"])} items but {len(ids)} ids')
        got = [it['type'] for it in p['items']]
        for it in got:
            types[it] += 1; n += 1
        if first in plan and got != plan[first]:
            errs.append(f'{f}/{first}: type order {got} != plan {plan[first]}')
        for slot, it in enumerate(p['items']):
            tag = f'{f}/{first}#{slot}({it["type"]})'
            raw = json.dumps(it, ensure_ascii=False)
            for ch in set(raw):
                if not ALLOWED.match(ch):
                    errs.append(f'{tag}: stray char {ch!r} U+{ord(ch):04X}')
            key, d = it.get('key', ''), it.get('d', [])
            if len(d) != 3:
                errs.append(f'{tag}: {len(d)} distractors (need 3)')
            opts = [key] + d
            if any(not o.strip() for o in opts):
                errs.append(f'{tag}: empty option')
            if len({norm(o).lower() for o in opts}) != len(opts):
                errs.append(f'{tag}: duplicate option text')
            if not it.get('exp', '').strip():
                errs.append(f'{tag}: missing explanation')
            for fld in ('prompt', 'exp'):
                for q in QUOTE.findall(it.get(fld, '')):
                    for part in [x for x in q.split('\u2026') if len(x.strip()) >= 6]:
                        if norm(part).strip(STRIPCH) not in ctx:
                            errs.append(f'{tag}: {fld} quote not in passage -> {part[:60]}')
print(f'{len(files)} files, {n} items, {sum(len(p["items"]) for f in files for p in json.load(open(f)))} total')
print('type mix:', dict(types.most_common()))
if errs:
    print(f'\n{len(errs)} PROBLEMS:')
    for e in errs: print(' -', e)
    sys.exit(1)
print('\nALL CLEAN')
