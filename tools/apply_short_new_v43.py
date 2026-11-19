#!/usr/bin/env python3
"""v43 (Arena round 2): brand-new Short Conversation dialogues from content/short_new_v43_[a-f].json.

Why: the 200 Short Conversation items were built on only 20 situations. Each situation had
three dialogues that were identical except for the speakers' names (word-overlap Jaccard up
to 0.94), so a candidate who read one dialogue could answer the other two without reading.

Each spec entry replaces ONE dialogue group (all items that share a context) with a new
conversation on the same topic label but a different setting, problem and information flow,
plus new options/explanations/tips for every blank. Item ids, sets, kinds and difficulty are
kept; answer positions are kept exactly as they were so the bank-level distribution does not
move.

Spec entry shape:
  {"first": "S07-Q017",                 # any item id of the group being replaced
   "context": "Ana: ...\\nBo: (1) ____\\n...",
   "items": [{"blank": 1, "key": "...", "d": ["...", "...", "..."],
              "exp": "...", "tip": "..."}]}
`d` holds the three distractors; the applier puts the key back at the position it already
occupies in the bank (answer positions are preserved, not re-randomised).
"""
import json, glob, sys, os, collections
sys.path.insert(0, os.path.dirname(__file__))
from changelog import log

REASON = ('Short conversation v43: dialogue replaced by a new conversation on the same topic '
          '(the bank had only 20 situations, each copied three times with different names - '
          'word overlap up to 0.94), options and Thai explanations rewritten to match')

V = json.load(open('data/vault.json', encoding='utf-8'))
groups = collections.defaultdict(list)
for q in V:
    if q['kind'] == 'short':
        groups[q['context']].append(q)
byid = {q['id']: q for q in V}

done = skipped = 0
for f in sorted(glob.glob('content/short_new_v43_[a-f].json')):
    for e in json.load(open(f, encoding='utf-8')):
        anchor = byid[e['first']]
        assert anchor['kind'] == 'short', e['first']
        grp = groups[anchor['context']]
        if grp[0]['context'] == e['context']:
            skipped += 1
            continue
        assert len(grp) == len(e['items']), (e['first'], len(grp), len(e['items']))
        blanks = sorted(int(q['prompt'].split('blank (')[1].split(')')[0]) for q in grp)
        assert blanks == sorted(it['blank'] for it in e['items']), (e['first'], blanks)
        for q in sorted(grp, key=lambda x: int(x['prompt'].split('blank (')[1].split(')')[0])):
            n = int(q['prompt'].split('blank (')[1].split(')')[0])
            spec = next(it for it in e['items'] if it['blank'] == n)
            pos = q['answer']
            opts = list(spec['d'])
            opts.insert(pos, spec['key'])
            assert len(set(opts)) == 4, (q['id'], 'duplicate option')
            for field, new in (('context', e['context']), ('options', opts),
                               ('explanation', spec['exp']), ('tip', spec['tip'])):
                if q[field] != new:
                    log(q['id'], field, q[field], new, REASON, 'SHORT-new')
                q[field] = new
            done += 1
json.dump(V, open('data/vault.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('short items rewritten', done, '| groups already applied', skipped)
