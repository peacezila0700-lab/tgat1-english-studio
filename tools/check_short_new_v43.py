#!/usr/bin/env python3
"""Validate content/short_new_v43_[a-d].json (new Short Conversation dialogues).

Simulates the whole Short Conversation bank after the specs are applied and checks both the
per-item rules (blank numbering, four distinct options, quotes in the Thai explanation really
occur in the dialogue, no stray scripts, key not the longest option) and the bank-level rules
that the replacement is supposed to fix: no two dialogues may be near-copies of each other,
the "pick the option with most words from the dialogue" shortcut must stay at or below 35%,
the extreme-word balance must stay within 1.5x, and answer positions must not move.

Run from the project root:  python3 tools/check_short_new_v43.py
"""
import json, re, sys, glob, collections, itertools

ALLOWED = re.compile(r'[\u0E00-\u0E7F\x00-\x7F\u2018\u2019\u201C\u201D\u2013\u2014\u2026]')
EXTREME = re.compile(r'\b(all|every|everyone|always|never|no one|nobody|nothing|only|must|completely|totally|impossible|guaranteed)\b', re.I)
QUOTE = re.compile(r'\u201C([^\u201D]{6,})\u201D')
STOP = set('the a an of to in for and or is are was were be been with that this it they he she as at on by from our we you i ll'.split())
STRIPCH = '"\'.;,'

def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u2019', "'").replace('\u201C', '"').replace('\u201D', '"')).strip()

def cw(s):
    return {w for w in re.findall(r"[a-z']+", s.lower()) if w not in STOP and len(w) > 2}

V = json.load(open('data/vault.json', encoding='utf-8'))
short = [q for q in V if q['kind'] == 'short']
byid = {q['id']: q for q in V}
groups = collections.defaultdict(list)
for q in short:
    groups[q['context']].append(q)

errs = []
specs = []
files = sorted(glob.glob('content/short_new_v43_[a-d].json'))
for f in files:
    for e in json.load(open(f, encoding='utf-8')):
        specs.append((f, e))

# simulated bank: context per item id + options per item id
sim_ctx, sim_opts, sim_ans, sim_text = {}, {}, {}, {}
for q in short:
    sim_ctx[q['id']] = q['context']; sim_opts[q['id']] = list(q['options'])
    sim_ans[q['id']] = q['answer']; sim_text[q['id']] = (q['explanation'], q.get('tip') or '')

for f, e in specs:
    a = byid.get(e['first'])
    if a is None or a['kind'] != 'short':
        errs.append(f'{f}: unknown short id {e["first"]}'); continue
    grp = groups[a['context']]
    if grp[0]['context'] == e['context']:
        continue                                    # already applied
    if len(grp) != len(e['items']):
        errs.append(f'{f}/{e["first"]}: {len(e["items"])} items but the group has {len(grp)}'); continue
    blanks = sorted(int(q['prompt'].split('blank (')[1].split(')')[0]) for q in grp)
    if blanks != sorted(it['blank'] for it in e['items']):
        errs.append(f'{f}/{e["first"]}: blanks {sorted(it["blank"] for it in e["items"])} != bank {blanks}')
    ctx = e['context']
    # dialogue shape
    lines = [l for l in ctx.split('\n') if l.strip()]
    if len(lines) < 5:
        errs.append(f'{f}/{e["first"]}: dialogue has only {len(lines)} lines')
    for n in blanks:
        if ctx.count(f'({n}) ____') != 1:
            errs.append(f'{f}/{e["first"]}: blank ({n}) must appear exactly once as "({n}) ____"')
    for extra in re.findall(r'\((\d)\) ____', ctx):
        if int(extra) not in blanks:
            errs.append(f'{f}/{e["first"]}: context has blank ({extra}) with no item')
    speakers = []
    for l in lines:
        m = re.match(r'^([A-Z][\w\u0E00-\u0E7F]*):\s', l)
        if not m:
            errs.append(f'{f}/{e["first"]}: line is not "Name: text" -> {l[:50]}')
        else:
            speakers.append(m.group(1))
    if len(set(speakers)) != 2:
        errs.append(f'{f}/{e["first"]}: need exactly 2 speakers, got {sorted(set(speakers))}')
    if any(speakers[i] == speakers[i + 1] for i in range(len(speakers) - 1)):
        errs.append(f'{f}/{e["first"]}: speakers must alternate')
    wc = len(ctx.split())
    if not 60 <= wc <= 160:
        errs.append(f'{f}/{e["first"]}: dialogue is {wc} words (keep 60-160)')
    ctx_n = norm(ctx)
    for it in e['items']:
        opts = list(it['d'])
        if len(opts) != 3:
            errs.append(f'{f}/{e["first"]}#{it["blank"]}: {len(opts)} distractors (need 3)')
        pos = next(q['answer'] for q in grp if int(q['prompt'].split('blank (')[1].split(')')[0]) == it['blank'])
        full = list(opts); full.insert(pos, it['key'])
        blob = json.dumps({'c': ctx, 'i': it}, ensure_ascii=False)
        for ch in set(blob):
            if not ALLOWED.match(ch):
                errs.append(f'{f}/{e["first"]}#{it["blank"]}: stray char {ch!r} U+{ord(ch):04X}')
        if len({norm(o).lower() for o in full}) != 4:
            errs.append(f'{f}/{e["first"]}#{it["blank"]}: duplicate option text')
        if any(not o.strip() for o in full):
            errs.append(f'{f}/{e["first"]}#{it["blank"]}: empty option')
        if len(it['key']) > max(len(o) for o in opts):
            errs.append(f'{f}/{e["first"]}#{it["blank"]}: key is the longest option ({len(it["key"])} > {max(len(o) for o in opts)})')
        if not re.search(r'[\u0E00-\u0E7F]', it['exp']):
            errs.append(f'{f}/{e["first"]}#{it["blank"]}: explanation has no Thai')
        for fld in ('exp', 'tip'):
            for qt in QUOTE.findall(it.get(fld, '')):
                for part in [x for x in qt.split('\u2026') if len(x.strip()) >= 6]:
                    hay = ctx_n + ' ' + norm(' '.join(full))
                    if norm(part).strip(STRIPCH) not in hay:
                        errs.append(f'{f}/{e["first"]}#{it["blank"]}: {fld} quote not in dialogue/options -> {part[:60]}')
        qid = next(q['id'] for q in grp if int(q['prompt'].split('blank (')[1].split(')')[0]) == it['blank'])
        sim_ctx[qid] = ctx; sim_opts[qid] = full; sim_ans[qid] = pos; sim_text[qid] = (it['exp'], it['tip'])

ids = list(sim_ctx)
# 1) no two dialogues near-copies
ctxs = {c: [i for i in ids if sim_ctx[i] == c] for c in {sim_ctx[i] for i in ids}}
worst = (0, None, None)
pairs = 0
for a, b in itertools.combinations(ctxs, 2):
    A, B = cw(a), cw(b)
    j = len(A & B) / max(1, len(A | B))
    if j > 0.5:
        pairs += 1
    if j > worst[0]:
        worst = (j, a[:45], b[:45])
print(f'dialogues: {len(ctxs)} unique for {len(ids)} items')
print(f'near-duplicate pairs (Jaccard > 0.5): {pairs} | worst {worst[0]:.3f}  {worst[1]} <-> {worst[2]}')
if pairs:
    errs.append(f'{pairs} dialogue pairs still overlap > 0.5 (worst {worst[0]:.3f})')

# 2) context-overlap shortcut
hit = 0
for i in ids:
    c = cw(sim_ctx[i])
    ov = [len(cw(o) & c) for o in sim_opts[i]]
    if max(range(4), key=lambda k: ov[k]) == sim_ans[i]:
        hit += 1
print(f'context-overlap shortcut: {hit/len(ids):.3f} (gate <= 0.35)')
if hit / len(ids) > 0.35:
    errs.append(f'context-overlap shortcut {hit/len(ids):.3f} > 0.35')

# 3) extreme-word balance + longest cue
ea = sum(bool(EXTREME.search(sim_opts[i][sim_ans[i]])) for i in ids) / len(ids)
ed = sum(bool(EXTREME.search(o)) for i in ids for k, o in enumerate(sim_opts[i]) if k != sim_ans[i]) / (3 * len(ids))
lng = sum(len(sim_opts[i][sim_ans[i]]) == max(map(len, sim_opts[i])) for i in ids) / len(ids)
print(f'extreme-word: answer {ea:.3f} vs distractor {ed:.3f} (gate: within 1.5x) | key longest {lng:.3f}')
if max(ea, ed) > 1.5 * min(ea, ed) + 1e-9:
    errs.append(f'extreme-word balance out: answer {ea:.3f} vs distractor {ed:.3f}')
if lng > 0.10:
    errs.append(f'key is the longest option in {lng:.1%} of short items (was 0%)')

# 4) positions unchanged
before = collections.Counter(q['answer'] for q in short)
after = collections.Counter(sim_ans[i] for i in ids)
if before != after:
    errs.append(f'answer positions moved: {dict(before)} -> {dict(after)}')

n_spec = sum(len(e['items']) for _, e in specs)
print(f'{len(files)} spec files, {len(specs)} dialogues, {n_spec} items')
if errs:
    print(f'\n{len(errs)} PROBLEMS:')
    for x in errs:
        print(' -', x)
    sys.exit(1)
print('\nALL CLEAN')
