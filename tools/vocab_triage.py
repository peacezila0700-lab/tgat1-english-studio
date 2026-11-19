"""Triage the 1,217 noun-slot filler examples into: definite (grammar) fix / human review / uncertain.
Only definite grammar errors are edited; the sentence stays generic and remains in the human queue."""
import json,re,csv,sys,os,collections
sys.path.insert(0,os.path.dirname(__file__));from changelog import log
D=json.load(open('data/data.json'));S=json.load(open('data/senses.json'));W=D['studio']['words']
lazy={wi:k for k,wi in enumerate(D['lazySenses'])};EX=D['studio']['examples']
NOUN=[r"^The researchers discussed (.+) before deciding how to proceed\.$", r"^The (.+) affected the team.s final decision\.$", r"^The policy addresses concerns about (.+)\.$",
 r"^The school provided guidance about (.+) to students\.$", r"^The community discussed (.+) after the announcement\.$", r"^The report highlighted (.+) as an important factor",
 r"^The team collected information about (.+) before making a decision\.$", r"^The company reviewed the risks associated with (.+)\.$", r"^The survey measured changes related to (.+)\.$",
 r"^The study compared the effects of (.+) across two groups\.$", r"^The study examined (.+) and its effects on the community\.$", r"^The report discussed (.+) as an important part of the analysis\.$"]
BADPL={'forgivenesses':'forgiveness','cost of livings':'the cost of living','standard of livings':'standards of living','limitation of the studies':'the limitations of the study',
'global warmings':'global warming','hypothesises':'hypotheses','obesities':'obesity','overconsumptions':'overconsumption','cynicisms':'cynicism','revenges':'revenge',
'sleep deprivations':'sleep deprivation','preys':'prey','deflations':'deflation','discretions':'discretion','persuasions':'persuasion','facilitations':'facilitation',
'waste disposals':'waste disposal','deteriorations':'deterioration','workforces':'the workforce'}
UNSURE_PL={'intensities','attainments','atmospheres','majorities','validations','verifications','contentions','implementations','eliminations','curriculums','aptitudes',
'stresses','anxieties','sympathies','courtesies','appetites','reassessments','formulations','derivations','inhibitions','magnitudes','finances','economies','capacities',
'deliberations','clarifications','confirmations','refinements','reproductions','restorations','retirements','reductions','recoveries','transformations','frustrations','perceptions',
'personalities','vulnerabilities','tendencies','discrepancies','deficiencies','inequities','inequalities','motivations','prejudices','speculations','postponements','genders',
'cuisines','flavors','revenues','consumer behaviors','digital divides','balanced diets','greenhouse gases','immense pressures','intense pressures','physical activities'}
UNC=set('''access accuracy advertising advice awareness banking behavior care communication comprehension concentration confidence conservation content cooperation damage data
development diversity education employment energy equality evidence feedback funding grammar growth health housing inclusion information infrastructure justice leadership learning
management media nutrition participation planning pollution prevention privacy productivity progress protection quality reading recovery research safety satisfaction screening
security shopping sleep speaking stress success support teamwork technology traffic training transport trust visualization vocabulary waste welfare wellbeing work workload writing
climate public conflict debt'''.split())
AMBIG=set('change experience culture income memory performance policy practice service interaction balance assessment evaluation language design measurement treatment environment saving future average opportunity motivation pressure'.split())
def plural(p):
    w=p.split();h=w[-1]
    irr={'analysis':'analyses','hypothesis':'hypotheses','criterion':'criteria','study':'studies'}
    if h in irr: h=irr[h]
    elif re.search(r'[^aeiou]y$',h): h=h[:-1]+'ies'
    elif re.search(r'(s|sh|ch|x|z)$',h): h=h+'es'
    else: h=h+'s'
    return ' '.join(w[:-1]+[h])
HOLD=set(r['headword'] for r in csv.DictReader(open('qa/REVIEW-QUEUE.csv',encoding='utf-8-sig')) if r['category']=='headword-validity')
rows=[];stat=collections.Counter()
for i,w in enumerate(W):
    sl=S[lazy[i]] if i in lazy else (w.get('senses') or [])
    for j,s in enumerate(sl):
        ex=s.get('example','')
        for p in NOUN:
            m=re.search(p,ex)
            if not m: continue
            slot=m.group(1);head=slot.split()[-1].lower();new=None
            if w['w'] in HOLD: cls='uncertain';why='headword itself is in the headword-validity queue (likely non-collocation); fix or retire the headword first'
            elif slot.lower() in BADPL: cls='definite';new=ex.replace(slot,BADPL[slot.lower()]);why=f'uncountable/fixed noun wrongly pluralised (“{slot}”)'
            elif s.get('pos')=='phrase' and head not in UNC and head not in AMBIG and not head.endswith('s') and slot.lower()==w['w'].lower():
                cls='definite';new=ex.replace(slot,plural(slot),1);why=f'countable singular noun phrase without a determiner (“{slot}”)'
            elif slot.lower() in UNSURE_PL or head in AMBIG: cls='uncertain';why='plural/countability is acceptable only in some senses; needs a human judgement'
            else: cls='human';why='grammatical but generic template sentence; does not show typical collocation'
            if new and new.startswith('The the'): new='The'+new[7:]
            stat[cls]+=1;rows.append(dict(i=i,j=j,w=w['w'],pos=s.get('pos'),old=ex,new=new,cls=cls,why=why))
            if new:
                log(f"senses[{lazy[i]}].{j}" if i in lazy else f"studio.words[{i}].senses.{j}",'example',ex,new,'Round-3 noun-slot triage: definite grammar fix only ('+why+'); sentence remains generic and stays in the human-review queue','VOCAB-grammar')
                s['example']=new
                ee=EX.get(w['w'],[])
                for k,x in enumerate(ee):
                    if x==ex: ee[k]=new
            break
json.dump(S,open('data/senses.json','w'),ensure_ascii=False,indent=1);json.dump(D,open('data/data.json','w'),ensure_ascii=False,indent=1)
json.dump(rows,open('qa/r3-noun-slot-triage.json','w'),ensure_ascii=False,indent=1)
print(len(rows),stat)
