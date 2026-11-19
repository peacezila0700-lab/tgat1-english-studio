#!/usr/bin/env python3
"""v43 (Arena round 2, task V2): replace generic noun-slot filler examples with authored ones.

Why: 1,217 phrase examples in the vocabulary bank were generated from 12 sentence templates
("The researchers discussed X before deciding how to proceed.", ...). They are grammatical but
show no typical collocation, so `qa/REVIEW-QUEUE.csv` keeps them in the human-review queue.

Spec files: content/vocab_examples_v43_[a-z].json
  [{"w": "<headword>", "sense": 0, "example": "<new sentence>", "translation": "<Thai>"}]

The example and its Thai translation are replaced as a pair (they are reviewed as a pair in the
queue). Runs BEFORE tools/vocab_triage.py so the triage queue shrinks on its own - never edit
data/data.json, data/senses.json or qa/REVIEW-QUEUE.csv by hand.
"""
import json, glob, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from changelog import log

REASON = ('Round-3 vocab V2: generic noun-slot template example replaced by an authored sentence '
          'that shows a typical collocation, with a matching Thai translation')
TAG = 'VOCAB-example'

D = json.load(open('data/data.json', encoding='utf-8'))
S = json.load(open('data/senses.json', encoding='utf-8'))
W = D['studio']['words']
lazy = {wi: k for k, wi in enumerate(D['lazySenses'])}
EX = D['studio'].get('examples') or {}
byw = {}
for i, w in enumerate(W):
    byw.setdefault(w['w'], i)

done = skipped = mirrored = untouched = 0
seen = collections.Counter()
applied = []
for f in sorted(glob.glob('content/vocab_examples_v43_[a-z].json')):
    for e in json.load(open(f, encoding='utf-8')):
        head = e['w']
        assert head in byw, f'{f}: unknown headword {head}'
        i = byw[head]
        sl = S[lazy[i]] if i in lazy else (W[i].get('senses') or [])
        j = int(e.get('sense', 0))
        assert j < len(sl), (head, j, len(sl))
        s = sl[j]
        seen[(head, j)] += 1
        assert seen[(head, j)] == 1, f'{head} sense {j} appears twice in the specs'
        old_ex, old_th = s.get('example'), s.get('translation')
        if old_ex == e['example'] and old_th == e['translation']:
            skipped += 1
            continue
        loc = f'senses[{lazy[i]}].{j}' if i in lazy else f'studio.words[{i}].senses.{j}'
        log(loc, 'example+translation', {'example': old_ex, 'translation': old_th},
            {'example': e['example'], 'translation': e['translation']}, REASON, TAG)
        s['example'] = e['example']
        s['translation'] = e['translation']
        # studio.examples is the "legacy examples" list the word detail shows UNDER the sense
        # example. Never let it duplicate the sense example: when the mirror held the very same
        # generic sentence, put the spec's second authored sentence (example2) there instead.
        for k, x in enumerate(EX.get(head, [])):
            if x == old_ex:
                if e.get('example2'):
                    EX[head][k] = e['example2']
                    mirrored += 1
                    log(f'studio.examples[{head}][{k}]', 'example', x, e['example2'],
                        'Round-3 vocab V2: the mirror example was the same generic template sentence as the '
                        'sense example; replaced by a second authored sentence so the detail view shows two '
                        'different collocation examples', TAG)
                else:
                    untouched += 1
        done += 1
        applied.append({'w': head, 'sense': j, 'old': {'example': old_ex, 'translation': old_th},
                        'new': {'example': e['example'], 'translation': e['translation']}, 'spec': f})

json.dump(applied, open('qa/r3-vocab-example-spec.json', 'w'), ensure_ascii=False, indent=1)
json.dump(S, open('data/senses.json', 'w'), ensure_ascii=False, indent=1)
json.dump(D, open('data/data.json', 'w'), ensure_ascii=False, indent=1)
print(f'vocab examples: {done} replaced, {skipped} already applied, {mirrored} mirror entries given a second authored sentence, {untouched} mirrors left as-is (no example2)')
