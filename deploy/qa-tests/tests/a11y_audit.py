"""axe-core audit over routes and interactive states, light+dark, desktop+mobile.
Usage: python3 a11y_audit.py WEBDIR OUT.json"""
import sys, json
from harness import *
STATES=[(p,f"studioNav('{p}')") for p in PAGES]+[
 ('word-detail',"studioNav('vocab');studioWordDetail(5)"),
 ('flashcards',"studioNav('vocab');studioStartFlashcards()"),
 ('vocab-new',"studioNav('vocab');V15_startNew()"),
 ('vocab-recall',"studioNav('vocab');V15_startRecall()"),
 ('vocab-translation',"studioNav('vocab');studioStartVocabTranslation('en-th')"),
 ('phrase-practice',"studioNav('vocab');studioStartPhrasePractice()"),
 ('vocab-lab',"TGAT1VocabularyLab.start('vocab')"),
 ('mock-exam',"VLT_startMock(1)"),
 ('category-tc',"VLT_startCategory('tc')"),
 ('category-rc',"VLT_startCategory('rc')"),
 ('sets-list',"studioNav('exam');studioShowSets()"),
 ('reading-plus',"studioNav('reading');TGAT1ReadingPlus.start('R382-TC-01')"),
 ('reading-legacy',"studioNav('reading');TGAT1ReadingPlus.openLegacy()"),
 ('hub-unit',"studioNav('hub')"),
 ('match-game',"studioNav('game');studioRunVocabGame('match')"),
 ('sentence-game',"studioNav('game');studioStartSentenceGame('tr')"),
 ('sprint',"VLT_startSprint()"),
 ('grammar',"studioNav('grammar')"),
 ('phrase-bank',"TGAT1PhrasePlus.openBank()"),
 ('errors',"studioOpenErrors()"),
 ('adaptive',"TGAT1Adaptive.start()"),
 ('confirm-dialog',"studioNav('settings');studioResetProgress()"),
]
def answer_first(pg):
    # click first visible option to reach the feedback/explanation state
    pg.evaluate("""(()=>{if(typeof VLT_RUN!=='undefined'&&VLT_RUN){VLT_answer(0);return}const b=[...document.querySelectorAll('#app button')].find(b=>/opt|choice|option/.test(b.className));if(b)b.click()})()""")
    pg.wait_for_timeout(300)
def main(webdir,out):
    res=[]
    with server(webdir) as base, browser() as b:
        for vpname,vp in [('desktop',DESKTOP),('mobile',MOBILE)]:
            for theme in ['light','dark']:
                pg=new_page(b,base,vp,theme)
                for name,js in STATES:
                    pg.goto(base+'/index.html');pg.wait_for_function("typeof studioNav==='function' && !document.querySelector('.boot-splash')")
                    pg.evaluate(f"studioTheme('{theme}')")
                    try:
                        pg.evaluate(js)
                        if 'hub' in js:
                            pg.wait_for_function("typeof TGAT1Hub==='object'",timeout=8000)
                            if name=='hub-unit': pg.evaluate("TGAT1Hub.openUnit(1)")
                        pg.wait_for_timeout(1200)
                    except Exception as e: res.append({'state':name,'vp':vpname,'theme':theme,'error':str(e)[:200]});continue
                    r=run_axe(pg); res.append({'state':name,'vp':vpname,'theme':theme,**r})
                    if name in('mock-exam','category-tc','category-rc','vocab-lab','adaptive'):
                        answer_first(pg); r=run_axe(pg); res.append({'state':name+'+answered','vp':vpname,'theme':theme,**r})
                res.append({'state':'_errors','vp':vpname,'theme':theme,'errs':pg.errs[:30]})
                pg.context.close()
    json.dump(res,open(out,'w'),ensure_ascii=False,indent=1)
    agg={}
    for r in res:
        for v in r.get('violations',[]): agg.setdefault(v['id'],[]).append(f"{r['state']}/{r['vp']}/{r['theme']}:{v['n']}")
    for k,v in agg.items(): print(k,len(v),v[:6])
    print('errors:',[r for r in res if r.get('error') or r.get('errs')])
if __name__=='__main__': main(sys.argv[1],sys.argv[2])
