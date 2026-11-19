"""Round 3: correct primary-stress mark placement in CMUdict-derived IPA.
Only entries whose current IPA equals the old naive conversion (mark placed straight after the previous vowel)
are regenerated; anything hand-edited is left alone and counted."""
import json,sys,os,re
sys.path.insert(0,os.path.dirname(__file__));import cmu_ipa;from changelog import log
def naive(text):
    out=[]
    for w in re.findall(r"[A-Za-z'’-]+",text.lower().replace('’',"'")):
        for piece in w.split('-'):
            piece=piece.strip("'")
            if not piece: continue
            if piece not in cmu_ipa.CMU: return None
            seg=[];
            for p in cmu_ipa.CMU[piece][0]:
                m=re.match(r'([A-Z]+)(\d)?',p);b,st=m.group(1),m.group(2)
                if b in cmu_ipa.V:
                    v=cmu_ipa.V[b]
                    if st=='0': v={'AH':'ə','ER':'ɚ'}.get(b,v)
                    seg.append(['V',v,st])
                else: seg.append(['C',cmu_ipa.C[b],None])
            k=next((i for i,x in enumerate(seg) if x[0]=='V' and x[2]=='1'),None);o=[x[1] for x in seg]
            if k is not None:
                prev=max([i for i in range(k) if seg[i][0]=='V'],default=-1);o.insert(prev+1,'ˈ')
            out.append(''.join(o))
    return '/'+' '.join(out)+'/'
D=json.load(open('data/data.json'));fixed=same=hand=0
for lst,name in [(D['studio']['words'],'studio.words'),(D['studio']['phrases'],'studio.phrases'),(D['pack']['phrases'],'pack.phrases'),(D['pack']['words'],'pack.words')]:
    for e in lst:
        if 'CMUdict' not in str(e.get('ipaSource','')) or not e.get('ipa'): continue
        nv=naive(e['w']);new=cmu_ipa.ipa_words(e['w'])
        if not nv or not new: hand+=1;continue
        if e['ipa']==nv and new!=nv:
            log(f"{name}:{e['w']}",'ipa',e['ipa'],new,'Stress mark moved to the syllable onset (maximal legal onset); v42.0.1 placed it directly after the preceding vowel, e.g. /kəˈmpɛɹ/ → /kəmˈpɛɹ/','IPA-stress');e['ipa']=new;fixed+=1
        elif e['ipa']==new: same+=1
        else: hand+=1
json.dump(D,open('data/data.json','w'),ensure_ascii=False,indent=1)
print('ipa stress fixed',fixed,'already correct',same,'not regenerated (differs from CMUdict conversion)',hand)
