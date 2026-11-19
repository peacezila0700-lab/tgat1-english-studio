"""Fill missing IPA (8 headwords + phrases) from CMUdict word-by-word, using the same ARPAbet→IPA
convention as the existing CMUdict entries (verified to reproduce 94%+ of them)."""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__));from cmu_ipa import ipa_words;from changelog import log
D=json.load(open('data/data.json'))
SRC_W='CMUdict · US English (word-by-word; phrase stress and weak forms not modelled)'
n=0;miss=[]
for w in D['studio']['words']:
    if not w.get('ipa'):
        g=ipa_words(w['w'])
        if g: log('studio.words:'+w['w'],'ipa+ipaSource','',g+' | '+SRC_W,'Missing IPA and source; generated from CMUdict word-by-word with the app’s existing ARPAbet→IPA convention','IPA-fill');w['ipa']=g;w['ipaSource']=SRC_W;n+=1
        else: miss.append(w['w'])
pn=0
for lst,name in [(D['studio']['phrases'],'studio.phrases'),(D['pack']['phrases'],'pack.phrases')]:
    for p in lst:
        if p.get('ipa'): continue
        g=ipa_words(p['w'])
        if g: p['ipa']=g;p['ipaSource']=SRC_W;pn+=1
        else: miss.append(p['w'])
log('studio.phrases+pack.phrases','ipa+ipaSource','(none)',f'{pn} phrases filled','Phrase IPA added from CMUdict word-by-word; phrases with words missing from CMUdict left without IPA','IPA-fill')
json.dump(D,open('data/data.json','w'),ensure_ascii=False,indent=1)
print('headwords',n,'phrases',pn,'missing',len(miss),miss[:30])
