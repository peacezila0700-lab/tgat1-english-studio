"""v43 (Claude): Short Conversation lure distractors from content/short_v43_[a-z].json.

v42/v43-Arena short items reused the same generic, off-topic distractors in every
dialogue ("Can we hand the whole task to another team instead?" ...), so picking the
option with most words from the dialogue was right 67% of the time
(bias_metrics short.answer_unique_top_context_overlap). Each spec entry swaps ONE
generic distractor (asserted by its old text) for a topical lure that reuses words from
the dialogue but does not fit the next line. Answer positions are unchanged.
"""
import json,glob,sys,os
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
V=json.load(open('data/vault.json'));by={q['id']:q for q in V}
REASON=('Short conversation v43: generic recycled distractor replaced by a topical lure '
        '(uses words from the dialogue but does not answer/lead to the next line) so '
        'word-matching no longer finds the key (bias_metrics short context-overlap 0.670)')
n=0
for f in sorted(glob.glob('content/short_v43_[a-z].json')):
    for e in json.load(open(f,encoding='utf-8')):
        q=by[e['id']];assert q['kind']=='short',e['id']
        s=e['slot'];assert s!=q['answer'] and q['options'][s]==e['old'],(e['id'],s,q['options'][s])
        opts=list(q['options']);opts[s]=e['new'];assert len(set(opts))==4,e['id']
        log(q['id'],'options',q['options'],opts,REASON,'SHORT-rewrite');q['options']=opts
        ex=q['explanation'].rstrip()+e['exp_add']
        log(q['id'],'explanation',q['explanation'],ex,REASON,'SHORT-rewrite');q['explanation']=ex
        n+=1
json.dump(V,open('data/vault.json','w'),ensure_ascii=False,indent=1)
print('short lures',n)
