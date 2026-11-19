#!/usr/bin/env python3
"""Validate content/qr_v43_[a-z].json before/after applying it.

Checks per entry: the item exists and is a Q-R item, the slot is not the key, the current
option text is either `old` (pending) or `new` (already applied), the replacement is unique
inside the item, is not reused elsewhere in the bank, has no absolute words, is not the
unique longest/shortest option, and - the part that matters most - is still a WRONG answer
category for the question asked.

Run from the project root:  python3 tools/check_qr_v43.py
Exit code 1 if any problem is found.
"""
import json, re, sys, glob, collections

ALLOWED = re.compile(r'[\u0E00-\u0E7F\x00-\x7F\u2018\u2019\u201C\u201D\u2013\u2014\u2026]')
EXTREME = re.compile(r'\b(all|every|everyone|always|never|no one|nobody|nothing|only|must|completely|totally|impossible|guaranteed)\b', re.I)

FREQ = re.compile(r'\b(once|twice|thrice|\d+\s*times?\s*a|every\s+(day|week|month|year|morning|evening|monday|tuesday|wednesday|thursday|friday|saturday|sunday)|weekends?|daily|weekly|monthly|yearly|often|sometimes|rarely|seldom|usually|frequently)\b', re.I)
CLOCK = re.compile(r'(\d{1,2}:\d{2}|\b\d{1,2}\s*(a\.m\.|p\.m\.|am|pm)\b|o\u2019clock|o\'clock|\bnoon\b|\bmidnight\b|\bat\s+\d)', re.I)
DURATION = re.compile(r'(\bfor\s+(about\s+|nearly\s+|almost\s+)?(\w+\s+)?(minute|hour|day|week|month)s?\b|\b\d+\s*(minutes|hours|days|weeks)\b|\ball day\b|\bhalf an hour\b|\bquarter of an hour\b)', re.I)
ACCEPT = re.compile(r'^(sure|certainly|of course|no problem|no worries|i\u2019?ll|i will|yes|yeah|no,|sorry|absolutely|definitely|let me)\b', re.I)
OPINION = re.compile(r'(\bi think\b|\bi\u2019?d say\b|\bsounds\b|\bwould help\b|\bgood idea\b|\bgreat idea\b|\bin my opinion\b|\bthat could be fun\b|\bI agree\b|\bI doubt\b|\bseems (fine|good|great)\b)', re.I)
ADVICE = re.compile(r'^(ask|check|call|try|contact|look|take|bring|write|use|restart|report|tell|show|open|read|wait|pay|book|email|visit)\b', re.I)

def wc(s):
    return len(s.split())

def category_problem(prompt, new):
    p = prompt.lower()
    n = new.strip()
    if 'how often' in p and FREQ.search(n):
        return 'gives a frequency but the question asks how often (would be correct)'
    if ('what time' in p or 'when does' in p) and CLOCK.search(n):
        return 'gives a clock time but the question asks what time'
    if 'how long' in p and DURATION.search(n):
        return 'gives a duration but the question asks how long'
    if re.search(r'\b(could you|would you mind|can you|will you)\b', p) and ACCEPT.match(n):
        return 'accepts/refuses the request, which is what the key does'
    if 'what do you think' in p and OPINION.search(n):
        return 'states an opinion, which is what the key does'
    if re.search(r'what should (you|i|we|he|she|they) do', p) and ADVICE.match(n):
        return 'gives advice, which is what the key does'
    return None

V = json.load(open('data/vault.json', encoding='utf-8'))
by = {q['id']: q for q in V}
errs, pending, applied, superseded = [], 0, 0, 0
new_by_id = collections.defaultdict(dict)
entries = []
files = sorted(glob.glob('content/qr_v43_[a-z].json'))
for f in files:
    for e in json.load(open(f, encoding='utf-8')):
        entries.append((f, e))

# simulated bank after applying every entry
sim = {qid: list(q['options']) for qid, q in by.items() if q['kind'] == 'qr'}
# a later spec file may patch the same (id, slot) again; the earlier entry is then superseded
last = {}
for i, (f, e) in enumerate(entries):
    last[(e['id'], e['slot'])] = i
for i, (f, e) in enumerate(entries):
    q = by.get(e['id'])
    if q is None:
        errs.append(f'{f}: unknown id {e["id"]}'); continue
    if q['kind'] != 'qr':
        errs.append(f'{f}: {e["id"]} is {q["kind"]}, not qr'); continue
    s = e['slot']
    if s == q['answer']:
        errs.append(f'{f}: {e["id"]} slot {s} is the key'); continue
    cur = q['options'][s]
    if cur == e['new']:
        applied += 1
    elif cur == e['old']:
        pending += 1
        sim[e['id']][s] = e['new']
    elif last[(e['id'], s)] != i:
        superseded += 1; continue          # a later spec entry replaced this slot again
    else:
        errs.append(f'{f}: {e["id"]} slot {s} is neither old nor new -> {cur[:60]}'); continue
    new_by_id[e['id']][s] = e['new']
    tag = f'{e["id"]}#{s}'
    for ch in set(e['new']):
        if not ALLOWED.match(ch):
            errs.append(f'{tag}: stray char {ch!r} U+{ord(ch):04X}')
    w = wc(e['new'])
    if not 3 <= w <= 14:
        errs.append(f'{tag}: {w} words (keep 3-14) -> {e["new"][:60]}')
    cat = category_problem(q['prompt'], e['new'])
    if cat:
        errs.append(f'{tag}: {cat} -> {e["new"][:70]}')

# per-item uniqueness + length cues, on the simulated options
for qid, slots in new_by_id.items():
    q = by[qid]
    opts = sim[qid]
    if len({o.strip().lower() for o in opts}) != 4:
        errs.append(f'{qid}: duplicate option text after patch -> {opts}')
    lens = [len(o) for o in opts]
    if lens[q['answer']] == max(lens) and lens.count(max(lens)) == 1:
        errs.append(f'{qid}: key became the unique longest option -> {opts}')

# bank-level length cues must not get worse
def cue(opts_map, idx):
    tot = hit = 0
    for qid, opts in opts_map.items():
        q = by[qid]; lens = [len(o) for o in opts]; tot += 1
        if lens[q['answer']] == idx(lens): hit += 1
    return hit / tot
before = {q['id']: list(q['options']) for q in V if q['kind'] == 'qr'}
for name, idx in (('answer_longest', max), ('answer_shortest', min)):
    b, a = cue(before, idx), cue(sim, idx)
    print(f'qr {name}: before {b:.3f} -> after {a:.3f}')
    if a > b + 0.005:
        errs.append(f'bank-level qr {name} got worse: {b:.3f} -> {a:.3f}')

# extreme-word balance: keys often contain frequency words ("Every Friday."), so the
# distractor side needs some too, otherwise "drop the option with an absolute word" works
er_ans = sum(bool(EXTREME.search(by[qid]['options'][by[qid]['answer']])) for qid in sim) / len(sim)
er_dis = sum(bool(EXTREME.search(o)) for qid, opts in sim.items() for i, o in enumerate(opts)
             if i != by[qid]['answer']) / (3 * len(sim))
print(f'qr extreme-word rate: answer {er_ans:.3f} vs distractor {er_dis:.3f} (gate: within 1.5x)')
if max(er_ans, er_dis) > 1.5 * min(er_ans, er_dis) + 1e-9:
    errs.append(f'qr extreme-word rate out of balance: answer {er_ans:.3f} vs distractor {er_dis:.3f}')

# reuse across the whole Q-R bank after applying
cnt = collections.Counter(o for qid, opts in sim.items() for i, o in enumerate(opts) if i != by[qid]['answer'])
reuse = [(n, s) for s, n in cnt.items() if n >= 2]
print(f'{len(files)} spec files, {len(entries)} entries ({pending} pending, {applied} already applied, {superseded} superseded by a later file)')
print(f'distractor sentences reused >=2 times after patch: {len(reuse)}')
for n, s in sorted(reuse, reverse=True)[:10]:
    print(f'  x{n}: {s[:70]}')
if errs:
    print(f'\n{len(errs)} PROBLEMS:')
    for x in errs:
        print(' -', x)
    sys.exit(1)
print('\nALL CLEAN')
