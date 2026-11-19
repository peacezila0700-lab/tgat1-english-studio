"""Round-3 browser regressions for bugs fixed in v42.0.2. Usage: python3 regression_r3_ui.py WEBDIR"""
import sys,json
from harness import *
R=[]
def check(n,c,d=''): R.append((n,bool(c)));print(('PASS ' if c else 'FAIL ')+n+('' if c else f'  [{str(d)[:300]}]'))
MATCH="""()=>{const G=window.TGAT1MatchGuard;const lv=['S','A','B','C'];let bad=[],short=0;
 for(let r=0;r<400;r++){const l=lv[r%4];const pool=V.map((_,i)=>i).filter(i=>V[i][3]===l);const ws=[];for(let k=0;k<5;k++)ws.push(pool[Math.floor(Math.random()*pool.length)]);
  const q=mkMatch(ws);if(q.L.length!==5||q.l.length!==5||q.r.length!==5){short++;continue}
  const words=q.L.map(i=>String(V[i][0]).toLowerCase()),shown=q.L.map(i=>q.meaningMap[i]);
  if(new Set(words).size<5||new Set(shown).size<5)bad.push(['dup',words,shown]);
  for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)if(G.conflict(q.L[a],q.L[b])||G.thaiOverlap(shown[a],[shown[b]]))bad.push(['overlap',words[a],words[b]]);}
 return {bad:bad.slice(0,5),n:bad.length,short}}"""
MCQ="""()=>{const G=window.TGAT1MatchGuard;let n=0,bad=[];const lv=['S','A','B','C'];
 for(const g of ['translate','syn','ant']){for(let r=0;r<30;r++){S.cur=lv[r%4];try{play(g)}catch(e){continue}
  for(const q of (Q&&Q.qs)||[]){if(!q.o)continue;n++;const c=q.o[q.a];const o=q.o.filter((_,i)=>i!==q.a);
   const hit=g==='translate'?o.find(x=>G.thaiOverlap(x,[c])):o.find(x=>G.related(q.w,x,g));if(hit)bad.push([g,q.w,c,hit])}
  Q=null}}return {n,bad:bad.slice(0,5),count:bad.length}}"""
with server(sys.argv[1]) as base, browser() as b:
    pg=new_page(b,base);pg.evaluate("studioNav('game')")
    m=pg.evaluate(MATCH)
    check('match game (active override): 400 rounds have 5 unique words and 5 unique displayed meanings',m['short']==0 and not [x for x in m['bad'] if x[0]=='dup'],m)
    check('match game: no semantically overlapping pair in 400 rounds (semantic guard)',m['n']==0,m)
    q=pg.evaluate(MCQ)
    check('vocab MCQ (translate/syn/ant): no distractor overlaps the key or is a listed synonym/antonym',q['count']==0 and q['n']>500,q)
    pg.evaluate("TGAT1PhrasePlus.openBank()");pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('.v382-phrase-item').click()");pg.wait_for_timeout(400)
    check('phrase detail shows IPA with source label',pg.evaluate("!!document.querySelector('.v382-detail-ipa') && /CMUdict/.test(document.querySelector('.v382-detail-ipa').innerText)"))
    idx=pg.evaluate("STUDIO_DATA.words.findIndex(w=>w.w==='a lack of')");pg.evaluate("studioNav('vocab')");pg.evaluate(f"studioWordDetail({idx})");pg.wait_for_timeout(400)
    check('previously unsourced headword “a lack of” now shows IPA and source',pg.evaluate("/ə ˈlæk ˈʌv/.test(document.body.innerText)&&/CMUdict/.test(document.body.innerText)"))
    pg.context.close()
    for theme in ['light','dark']:
        pg=new_page(b,base,MOBILE if theme=='dark' else DESKTOP,theme)
        viol={}
        for name,js in [('flashcards',"studioNav('vocab');studioStartFlashcards()"),('mock',"VLT_startMock(1)"),('mock-answered',"VLT_startMock(1);VLT_answer(0)"),
                        ('tc-answered',"VLT_startCategory('tc');VLT_answer(0)"),('word-detail',"studioNav('vocab');studioWordDetail(5)"),('confirm',"studioNav('settings');studioResetProgress()"),
                        ('vocab-translation',"studioNav('vocab');studioStartVocabTranslation('en-th')"),('hub-unit',"studioNav('hub');TGAT1Hub.openUnit(1)")]:
            pg.goto(base+'/index.html');pg.wait_for_function("typeof studioNav==='function'");pg.evaluate(f"studioTheme('{theme}')");pg.evaluate(js);pg.wait_for_timeout(900)
            r=run_axe(pg);v=[x['id'] for x in r['violations'] if x['impact'] in('serious','critical') or x['id']=='label-content-name-mismatch']
            if v: viol[name]=v
        check(f'axe-core: no serious/critical violations (incl. contrast) in 8 deep states [{theme}]',not viol,viol)
        pg.context.close()
f=[r for r in R if not r[1]];print(f'\nregression_r3_ui: {len(R)-len(f)}/{len(R)} passed');sys.exit(1 if f else 0)
