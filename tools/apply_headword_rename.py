"""v43 (R3): rename the 56 grid 'domain x noun' pseudo-collocations (headword-validity
queue, user decision (ก) = rename) into established English collocations.

Reads content/headword_rename_r3.json and, for each rename:
  * studio.words[i].w  -> new headword,  .th -> new Thai gloss
  * clears .ipa/.ipaSource so tools/ipa_fill.py regenerates CMUdict IPA for the NEW text
  * studio.examples    -> re-key old->new and replace the generic template sentence with a
                          natural example that actually shows the collocation
  * senses.json[lazy[i]][0] -> example/meaning/translation updated to the natural sentence
  * records every field change via changelog.log (category 'headword-rename')
  * accumulates data['headwordAliases'][old] = new so the app can migrate stored learner
    progress (normalizeVocabState reads __TGAT1_DATA.headwordAliases); nothing is deleted.

Must run AFTER the backups are copied into data/ and BEFORE vocab_triage.py / ipa_fill.py
(see tools/rebuild_all.sh). Idempotent within a rebuild because data/ is reset from backups.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from changelog import log

SPEC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'headword_rename_r3.json')
spec = json.load(open(SPEC, encoding='utf-8'))
D = json.load(open('data/data.json', encoding='utf-8'))
S = json.load(open('data/senses.json', encoding='utf-8'))
st = D['studio']; W = st['words']; EX = st['examples']
lazy = {wi: k for k, wi in enumerate(D['lazySenses'])}
idx = {w['w']: i for i, w in enumerate(W)}

# sanity: new headwords must be unique and must not collide with a headword we are not renaming
old_set = {r['old'] for r in spec['renames']}
new_list = [r['new'] for r in spec['renames']]
assert len(set(new_list)) == len(new_list), 'duplicate new headword in spec'
for w in W:
    if w['w'] in set(new_list) and w['w'] not in old_set:
        raise SystemExit(f"collision: '{w['w']}' already exists and is not being renamed")

aliases = D.get('headwordAliases', {})
n = 0
for r in spec['renames']:
    old, new, th, ex, tr, reason = r['old'], r['new'], r['th'], r['example'], r['translation'], r['reason']
    if old not in idx:
        print('WARN: headword not found (already renamed?):', old); continue
    i = idx[old]; w = W[i]

    log('studio.words:' + old, 'w', old, new, reason, 'headword-rename')
    if w.get('th') != th:
        log('studio.words:' + old, 'th', w.get('th'), th, 'Thai gloss updated to match the renamed collocation', 'headword-rename')
    w['w'] = new; w['th'] = th

    # clear IPA so ipa_fill regenerates it from CMUdict for the NEW headword text
    if w.get('ipa'):
        log('studio.words:' + old, 'ipa', w.get('ipa'), '', 'cleared; regenerated from CMUdict by ipa_fill for the new headword', 'headword-rename')
    w['ipa'] = ''; w.pop('ipaSource', None)

    # examples dict: re-key old->new, replace generic template with the natural sentence
    oldex = EX.pop(old, None)
    if oldex is not None:
        log('studio.examples:' + old, 'examples', oldex, [ex], 'generic template example replaced with a natural sentence showing the collocation', 'headword-rename')
    EX[new] = [ex]

    # senses: update the first (only) sense for these phrase entries
    if i in lazy:
        sl = S[lazy[i]]
        if isinstance(sl, list) and sl and isinstance(sl[0], dict):
            s0 = sl[0]
            if s0.get('example') != ex:
                log(f'senses[{lazy[i]}].0', 'example', s0.get('example'), ex, 'generic template example replaced with a natural sentence showing the collocation', 'headword-rename')
                s0['example'] = ex
            if s0.get('meaning') != th:
                log(f'senses[{lazy[i]}].0', 'meaning', s0.get('meaning'), th, 'sense meaning updated to match the renamed collocation', 'headword-rename')
                s0['meaning'] = th
            if s0.get('translation') != tr:
                log(f'senses[{lazy[i]}].0', 'translation', s0.get('translation'), tr, 'Thai translation updated to match the new natural example', 'headword-rename')
                s0['translation'] = tr

    aliases[old] = new
    del idx[old]; idx[new] = i
    n += 1

D['headwordAliases'] = aliases
json.dump(D, open('data/data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S, open('data/senses.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'apply_headword_rename: renamed {n} headwords, {len(aliases)} aliases emitted')
