#!/usr/bin/env python3
"""Gates for the authored vocabulary examples (vocab V2, content/vocab_examples_v43_*.json).

Usage: python3 tools/check_vocab_examples.py            (reads data/data.json + data/senses.json)

G-K  each spec entry is present in the bank (applier ran) and the generic template is gone
G-L  example contains the headword verbatim, exactly once, and no Thai/foreign script
G-M  Thai translation has zero Latin letters (regression_v42.py:62 rule)
G-N  sentence hygiene: 7-24 words, <=150 chars, capital + full stop, no double space
G-O  no example repeats the 12 noun-slot templates; no sentence frame or opening trigram reused
G-P  examples are unique bank-wide (sense examples and studio.examples mirrors)
G-Q  the studio.examples mirror never duplicates the sense example; example2 is in the mirror
"""
import json, re, glob, sys, collections

D = json.load(open('data/data.json', encoding='utf-8'))
S = json.load(open('data/senses.json', encoding='utf-8'))
W = D['studio']['words']
lazy = {wi: k for k, wi in enumerate(D['lazySenses'])}
EX = D['studio'].get('examples') or {}
byw = {}
for i, w in enumerate(W):
    byw.setdefault(w['w'], i)

NOUN = [r"^The researchers discussed (.+) before deciding how to proceed\.$", r"^The (.+) affected the team.s final decision\.$",
        r"^The policy addresses concerns about (.+)\.$", r"^The school provided guidance about (.+) to students\.$",
        r"^The community discussed (.+) after the announcement\.$", r"^The report highlighted (.+) as an important factor",
        r"^The team collected information about (.+) before making a decision\.$", r"^The company reviewed the risks associated with (.+)\.$",
        r"^The survey measured changes related to (.+)\.$", r"^The study compared the effects of (.+) across two groups\.$",
        r"^The study examined (.+) and its effects on the community\.$", r"^The report discussed (.+) as an important part of the analysis\.$"]

specs = []
for f in sorted(glob.glob('content/vocab_examples_v43_[a-z].json')):
    for e in json.load(open(f, encoding='utf-8')):
        e['_spec'] = f
        specs.append(e)

fails = []
def bad(g, msg): fails.append(f'{g}: {msg}')

# every sense example + every mirror example in the bank, for the uniqueness gate
all_ex = collections.Counter()
for i, w in enumerate(W):
    sl = S[lazy[i]] if i in lazy else (w.get('senses') or [])
    for s in sl:
        if s.get('example'): all_ex[s['example']] += 1
for w, ee in EX.items():
    for x in ee:
        if x: all_ex[x] += 1

frames = collections.Counter()
opens = collections.Counter()
for e in specs:
    head = e['w']
    where = f"{head} sense {e.get('sense', 0)} ({e['_spec']})"
    if head not in byw:
        bad('G-K', f'unknown headword {head}'); continue
    i = byw[head]
    sl = S[lazy[i]] if i in lazy else (W[i].get('senses') or [])
    j = int(e.get('sense', 0))
    s = sl[j] if j < len(sl) else {}
    ex, th = e['example'], e['translation']
    if s.get('example') != ex or s.get('translation') != th:
        bad('G-K', f'{where}: spec not applied to the bank (bank has {str(s.get("example"))[:60]!r})')
    # G-M
    if re.search(r'[A-Za-z]', th): bad('G-M', f'{where}: Latin letters in the Thai translation')
    if not re.search(r'[\u0E00-\u0E7F]', th): bad('G-M', f'{where}: no Thai characters in the translation')
    # G-Q: mirror must not repeat the sense example, and must hold example2 when one is given
    mirror = EX.get(head, [])
    if ex in mirror:
        bad('G-Q', f'{where}: studio.examples duplicates the sense example (add an "example2")')
    if e.get('example2') and e['example2'] not in mirror:
        bad('G-Q', f'{where}: example2 not in studio.examples (mirror is {mirror[:1]})')
    for label, sent in (('example', ex), ('example2', e.get('example2'))):
        if not sent: continue
        w2 = f'{where} [{label}]'
        # G-L
        if sent.lower().count(head.lower()) != 1:
            bad('G-L', f'{w2}: headword occurs {sent.lower().count(head.lower())}× — must appear exactly once verbatim')
        if re.search(r'[\u0E00-\u0E7F]', sent): bad('G-L', f'{w2}: Thai characters in the English example')
        foreign = sorted({c for c in sent if ord(c) > 127 and c not in '‘’“”—–…'})
        if foreign: bad('G-L', f'{w2}: foreign script {foreign!r}')
        # G-N
        words = sent.split()
        if not 7 <= len(words) <= 24: bad('G-N', f'{w2}: {len(words)} words (want 7–24)')
        if len(sent) > 150: bad('G-N', f'{w2}: {len(sent)} chars (want ≤150)')
        if not sent[0].isupper() or not sent.endswith('.'): bad('G-N', f'{w2}: must start capital + end with a full stop')
        if '  ' in sent or ' .' in sent: bad('G-N', f'{w2}: spacing problem')
        # G-O
        for p in NOUN:
            if re.search(p, sent): bad('G-O', f'{w2}: noun-slot template')
        frames[re.sub(re.escape(head), 'X', sent, flags=re.I)] += 1
        opens[' '.join(words[:3]).lower()] += 1
        # G-P
        if all_ex[sent] > 1: bad('G-P', f'{w2}: sentence appears {all_ex[sent]}× bank-wide')
    if e.get('example2') and e['example2'] == ex:
        bad('G-P', f'{where}: example2 equals the sense example')

for f, n in frames.items():
    if n > 1: bad('G-O', f'sentence frame reused {n}×: {f[:70]!r}')
for k, v in {k: v for k, v in opens.items() if v > 3}.items():
    bad('G-O', f'{v} examples open with {k!r} (max 3)')

if fails:
    print(f'FAIL {len(fails)}')
    for x in fails[:60]: print('  ', x)
    sys.exit(1)
n2 = sum(1 for e in specs if e.get('example2'))
print(f'check_vocab_examples: {len(specs)} authored examples (+{n2} second examples) · gates G-K..G-Q clean')
print(f'  frames {len(frames)} distinct · opening trigrams {len(opens)} distinct · longest {max(len(e["example"]) for e in specs)} chars')
