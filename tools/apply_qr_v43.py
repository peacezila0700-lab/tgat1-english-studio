#!/usr/bin/env python3
"""v43 (Arena round 2): item-specific Q-R distractors from content/qr_v43_[a-z].json.

Why: 17 canned wrong responses were reused across the Question-Response bank
("For about two hours." x17, "Three times a week." x17, "Near the main entrance." x17 ...),
covering 230 of the 600 distractor slots in 101 items. A candidate who meets the same
sentence three times learns it is always wrong and can discard it without reading the
question - a shortcut that no length/overlap gate catches.

Each spec entry swaps ONE distractor (asserted by its old text) for a sentence written for
that item: wrong response *category* for the question asked, similar length to the other
options, no absolute words, and not reused anywhere else in the bank. Answer positions and
keys are untouched, and no explanation mentions the replaced text (verified before writing).
"""
import json, glob, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from changelog import log

REASON = ('Q-R v43: canned distractor reused across many items replaced by an item-specific '
          'wrong-category response, so recognising a recycled sentence no longer removes an option')

V = json.load(open('data/vault.json', encoding='utf-8'))
by = {q['id']: q for q in V}
n = skipped = 0
for f in sorted(glob.glob('content/qr_v43_[a-z].json')):
    for e in json.load(open(f, encoding='utf-8')):
        q = by[e['id']]
        assert q['kind'] == 'qr', e['id']
        s = e['slot']
        assert s != q['answer'], (e['id'], 'slot is the key')
        cur = q['options'][s]
        if cur == e['new']:
            skipped += 1
            continue
        assert cur == e['old'], (e['id'], s, cur, e['old'])
        opts = list(q['options'])
        opts[s] = e['new']
        assert len(set(opts)) == 4, e['id']
        log(q['id'], 'options', q['options'], opts, REASON, 'QR-distractor')
        q['options'] = opts
        n += 1
json.dump(V, open('data/vault.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('qr distractors replaced', n, '| already applied', skipped)
