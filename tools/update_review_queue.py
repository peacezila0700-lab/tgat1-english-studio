"""Round 3: update qa/REVIEW-QUEUE.csv in place (row ids kept) and append new findings."""
import csv,json,collections,io
SRC='qa/v42.0.1-inherited/REVIEW-QUEUE.csv'
R=list(csv.DictReader(open(SRC,encoding='utf-8-sig')));F=list(R[0].keys())
T=json.load(open('qa/r3-noun-slot-triage.json'))
tri={(t['w'],t['old']):t for t in T}
# Arena round 2 (vocab V2): examples replaced by authored sentences in content/vocab_examples_v43_*.json
import os
auth={}
if os.path.exists('qa/r3-vocab-example-spec.json'):
    for a in json.load(open('qa/r3-vocab-example-spec.json')):
        auth.setdefault((a['w'],a['old']['example']),a)
H=json.load(open('content/headword_triage_r3.json'));pl,un=set(H['plausible']),set(H['uncertain'])
cnt=collections.Counter()
for r in R:
    if r['category']=='example-quality':
        a=auth.get((r['headword'],r['current value']))
        if a:
            r['current value']=a['new']['example']
            r['suggested action']='proofread the authored example + Thai translation'
            r['status']='round 3 (Arena): example rewritten by hand — authored sentence showing a typical collocation · needs human proofreading'
            cnt['ex-authored']+=1;continue
        t=tri.get((r['headword'],r['current value']))
        if not t: cnt['ex-unmatched']+=1;continue
        if t['cls']=='definite':
            r['status']='round 3: grammar corrected ('+t['why']+') → “'+(t['new'] or '')+'” · sentence still generic · needs human rewrite';cnt['ex-definite']+=1
        elif t['cls']=='uncertain':
            r['status']='round 3 triage: UNCERTAIN — '+t['why']+' · needs human decision';cnt['ex-uncertain']+=1
        else:
            r['status']='round 3 triage: needs human rewrite ('+t['why']+') · not auto-edited';cnt['ex-human']+=1
    elif r['category']=='headword-validity':
        h=r['headword']
        if h in pl: r['status']='round 3 triage: PLAUSIBLE collocation · keep after human confirmation';cnt['hw-plausible']+=1
        elif h in un: r['status']='round 3 triage: UNCERTAIN · needs editor decision (keep / rename / retire)';cnt['hw-uncertain']+=1
        else: r['status']='round 3 triage: NOT an established collocation (category label + noun) · recommend retire or rename · not deleted (would shift stored progress indices)';cnt['hw-definite']+=1
    elif r['category']=='human review: regenerated practice contexts':
        r['status']='round 3: LC rewritten/revised (200), TC 84 ambiguity/off-topic fixes + 300 Thai explanations, RC 180 items rewritten + 74 length fixes · still needs human English/Thai proofreading'
    elif r['category']=='human review: matching-game uniqueness':
        r['status']='round 3: active mkMatch override fixed (unique words + displayed meanings + semantic guard); 400-round regression passes · human spot-check of guard word lists recommended'
n=len(R)
def add(pri,cat,loc,hw,field,val,reason,action,status):
    global n;n+=1;R.append(dict(zip(F,[f'RQ-{n:04d}',pri,cat,loc,hw,'',field,val,reason,action,status])))
add('P1','human review: round-3 question content','data-vault.js long (S01–S20 Q021–Q030)','','context+options+explanation','200 items (100 rewritten dialogues, 100 revised items)','authored in round 3; automated checks only','English naturalness + Thai explanation proofreading by a qualified teacher','pending human review')
add('P1','human review: round-3 question content','data-vault.js rc (positions 1,2,5 of each passage)','','options+explanation','180 rewritten items + 74 length-balanced items + 36 stems','authored in round 3; automated cue metrics only','check every key is uniquely correct from the passage; proofread Thai explanations','pending human review')
add('P2','human review: rule-generated explanations','data-vault.js tc','','explanation','300 TC explanations (template-assisted, 11 hand overrides)','distractor reasons are generic category statements','replace generic distractor sentences with item-specific reasons where useful','rule-generated · needs human review')
add('P2','residual test-wiseness cue','data-vault.js rc','','options','second-longest option is the key in ~44% of RC items; “avoid extreme words” rule scores 36% (chance 25%)','length/wording balance only partially corrected','vary key length further; rewrite distractors that rely on absolutes','open')
add('P2','residual test-wiseness cue','data-vault.js short','','options','Short Conversation: max context-overlap option is the key in 69.5% of 200 items; key is never longest/shortest','not in round-3 scope','rewrite distractors to reuse context words','open')
add('P2','theme repetition','data-vault.js','','context','RC energy-check passages (S14-Q056 vs S20-Q051), lost-property passages (S07-Q046 vs S16-Q046), TC seed exchange vs RC seed library (S01); ~10/40 LC, 11/40 TC, 9/60 RC passages share a try→measure→adjust narrative','passages are lexically distinct but thematically repetitive','replace one passage in each near-duplicate pair; vary text types (opinion, narrative, notice, email)','open')
add('P2','ipa-notation','data.js studio.words/phrases ipaSource=eSpeak','','ipa','1,333 eSpeak entries use eSpeak notation (stress before vowel, ɐ, ɾ, mixed ɜː/ɚ)','inconsistent with CMUdict-derived entries; UI shows the source caveat','normalize or re-source from a dictionary with human listening check','open')
add('P2','ipa-review','data.js CMUdict entries','','ipa','83 CMUdict-labelled entries differ from both the naive and corrected CMUdict conversions','probably hand-edited; not auto-regenerated','check by listening','open')
add('P3','ipa-phrase','data.js phrases ipaSource=CMUdict word-by-word','','ipa','phrase IPA generated word by word: every word carries citation stress; weak forms (to, of, for, a) not modelled','source label states this','add phrase stress/weak forms if pronunciation is taught from these','open')
add('P2','gloss-alignment','data.js studio.words','','th vs senses[0].meaning','35 headwords whose main gloss does not contain the first sense meaning (qa/r3-gloss-scan.json)','headword gloss and sense list come from different sources','align main gloss with senses or reorder senses','needs human review')
add('P2','phrase-example','data.js studio.phrases','','example','87 phrases whose example does not contain the phrase verbatim (often inflected, e.g. applied for)','many are acceptable inflections; some may not show the phrase','check each example shows the target phrase','needs human review')
with open('qa/REVIEW-QUEUE.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=F);w.writeheader();w.writerows(R)
print(dict(cnt),'rows',len(R))
