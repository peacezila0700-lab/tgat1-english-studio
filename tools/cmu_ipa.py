import cmudict,re
CMU=cmudict.dict()
V={'AA':'ɑ','AE':'æ','AH':'ʌ','AO':'ɔ','AW':'aʊ','AY':'aɪ','EH':'ɛ','ER':'ɝ','EY':'eɪ','IH':'ɪ','IY':'i','OW':'oʊ','OY':'ɔɪ','UH':'ʊ','UW':'u'}
C={'B':'b','CH':'tʃ','D':'d','DH':'ð','F':'f','G':'ɡ','HH':'h','JH':'dʒ','K':'k','L':'l','M':'m','N':'n','NG':'ŋ','P':'p','R':'ɹ','S':'s','SH':'ʃ','T':'t','TH':'θ','V':'v','W':'w','Y':'j','Z':'z','ZH':'ʒ'}
_1=set('b d f ɡ h dʒ k l m n p ɹ s ʃ t tʃ θ ð v w j z ʒ'.split())
_2=set(tuple(x.split('+')) for x in 'p+l p+ɹ p+j b+l b+ɹ b+j t+ɹ t+w t+j d+ɹ d+w d+j k+l k+ɹ k+w k+j ɡ+l ɡ+ɹ ɡ+w ɡ+j f+l f+ɹ f+j θ+ɹ θ+w ʃ+ɹ s+p s+t s+k s+m s+n s+l s+w s+f s+j m+j n+j h+j v+j l+j'.split())
_3=set(tuple(x.split('+')) for x in 's+p+l s+p+ɹ s+p+j s+t+ɹ s+t+j s+k+ɹ s+k+w s+k+l s+k+j'.split())
ONSETS=set((c,) for c in _1)|_2|_3
def word(ph):
    seg=[]
    for p in ph:
        m=re.match(r'([A-Z]+)(\d)?',p);b,st=m.group(1),m.group(2)
        if b in V:
            v=V[b]
            if st=='0': v={'AH':'ə','ER':'ɚ'}.get(b,v)
            seg.append(['V',v,st])
        else: seg.append(['C',C[b],None])
    k=next((i for i,x in enumerate(seg) if x[0]=='V' and x[2]=='1'),None)
    out=[x[1] for x in seg]
    if k is not None:
        prev=max([i for i in range(k) if seg[i][0]=='V'],default=-1)
        cons=[x[1] for x in seg[prev+1:k]]
        # round 3: maximal legal English onset (the v42.0.1 data put the mark right after the previous
        # vowel, e.g. /kəˈmpɛɹ/, /ɪˈkspleɪn/; correct syllabification gives /kəmˈpɛɹ/, /ɪkˈspleɪn/)
        start=prev+1 if prev<0 else k
        for n in range(len(cons),-1,-1):
            if n==0 or tuple(cons[len(cons)-n:]) in ONSETS: start=k-n;break
        out.insert(start,'ˈ')
    return ''.join(out)
def ipa_words(text):
    ws=re.findall(r"[A-Za-z'’-]+",text.lower().replace('’',"'"))
    parts=[]
    for w in ws:
        for piece in w.split('-'):
            if not piece: continue
            piece=piece.strip("'")
            if piece not in CMU: return None
            parts.append(word(CMU[piece][0]))
    return '/'+' '.join(parts)+'/'
