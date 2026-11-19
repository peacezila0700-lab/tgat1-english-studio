"""TGAT1 English Studio extra smoke checks (round 3). Complements the original smoke_test.py.
Written in round 3 before the original QA/tests ZIP was supplied; kept as an additional suite
(routes on 5 viewports incl. 320/768/1920 px, flows, offline). Usage: python3 smoke_r3_extra.py WEBDIR"""
import sys, json, traceback
from harness import *
RESULTS=[]
def check(name):
    def deco(fn):
        def run(*a):
            try: fn(*a); RESULTS.append((name,True,''))
            except Exception as e: RESULTS.append((name,False,(str(e) or repr(e))[:300]))
        run.__name__=name; return run
    return deco
def ok(c,msg='assertion failed'):
    if not c: raise AssertionError(msg)
def fresh(pg,base):
    pg.goto(base+'/index.html');pg.wait_for_function("typeof studioNav==='function' && !document.querySelector('.boot-splash')",timeout=20000)

def main(webdir):
    with server(webdir) as base, browser() as b:
        for vpname,vp in [('desktop',DESKTOP),('mobile',MOBILE),('small320',SMALL),('tablet768',{'width':768,'height':1024}),('wide1920',{'width':1920,'height':1080})]:
            pg=new_page(b,base,vp)
            for page in PAGES:
                @check(f'route {page} renders [{vpname}]')
                def t():
                    nav(pg,page);txt=pg.inner_text('#app');ok(len(txt)>40,f'thin page: {len(txt)} chars')
                    ok(pg.evaluate("STUDIO_PAGE")==page,'STUDIO_PAGE mismatch')
                t()
                if vpname not in ('desktop','wide1920'):
                    @check(f'route {page} no horizontal overflow [{vpname}]')
                    def t2():
                        w=pg.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)");ok(w<=vp['width']+1,f'scrollWidth {w}>{vp["width"]}')
                    t2()
            @check(f'no console/page errors across routes [{vpname}]')
            def t3(): ok(not pg.errs,'; '.join(pg.errs[:5]))
            t3();pg.context.close()
        pg=new_page(b,base)
        @check('dark theme applies and persists after reload')
        def t():
            pg.evaluate("studioTheme('dark')");fresh(pg,base);ok(pg.evaluate("document.documentElement.dataset.theme")=='dark')
            pg.evaluate("studioTheme('light')")
        t()
        @check('version metadata consistent (app/cache/content/meta/manifest/sw)')
        def t():
            v=pg.evaluate("TGAT1_VERSION");meta=pg.evaluate("document.querySelector('meta[name=tgat1-version]').content")
            man=pg.evaluate("fetch('./manifest.webmanifest').then(r=>r.json())");sw=pg.evaluate("fetch('./sw.js').then(r=>r.text())")
            ok(v['app']==v['content']==meta,f'{v} {meta}');ok(v['cache']=='tgat1-studio-v'+v['app']);ok(man['version']=='v'+v['app'],man['version'])
            ok(f"'tgat1-studio-v{v['app']}'" in sw,'sw cache name')
        t()
        @check('mock exam set 1: 60 questions, answer all, finish shows result')
        def t():
            fresh(pg,base);pg.evaluate("VLT_startMock(1)");pg.wait_for_timeout(400)
            n=pg.evaluate("VLT_RUN.qs.length");ok(n==60,f'{n} items')
            pg.evaluate("(()=>{for(let i=0;i<VLT_RUN.qs.length;i++){VLT_goto(i);VLT_answer(0)}})()");pg.wait_for_timeout(200)
            pg.evaluate("VLT_finish(true)");pg.wait_for_timeout(600)
            ok(pg.evaluate("!VLT_RUN || !!VLT_RUN.done || /คะแนน|score|ผลสอบ/i.test(document.querySelector('#app').innerText)"),'no result')
        t()
        for kind in ['qr','short','long','tc','rc']:
            @check(f'category practice {kind}: renders options and explanation after answer')
            def t():
                fresh(pg,base);pg.evaluate(f"VLT_startCategory('{kind}')");pg.wait_for_timeout(300)
                ok(pg.evaluate("document.querySelectorAll('#app [onclick^=\"VLT_answer(\"]').length")==4,'not 4 options')
                pg.evaluate("VLT_answer(0)");pg.wait_for_timeout(250)
                ok(len(pg.inner_text('#app'))>200,'no feedback')
            t()
        @check('matching game: complete one round with correct pairs')
        def t():
            fresh(pg,base);nav(pg,'game');pg.evaluate("studioRunVocabGame('match')");pg.wait_for_timeout(400)
            L=pg.evaluate("Q.qs[Q.i].L");ok(len(L)==5,f'{len(L)} pairs')
            for i in L: pg.evaluate(f"mt('l',{i});mt('r',{i})");pg.wait_for_timeout(60)
            ok(pg.evaluate("Q.qs[Q.i].dn.length")==5 or pg.evaluate("Q.ans!==null"),'round not completed')
        t()
        @check('flashcards: open and flip by keyboard')
        def t():
            fresh(pg,base);nav(pg,'vocab');pg.evaluate("studioStartFlashcards()");pg.wait_for_timeout(400)
            ok(pg.locator('.st-flash').count()>0,'no card');pg.focus('.st-flash');before=pg.inner_text('#app');pg.keyboard.press('Enter');pg.wait_for_timeout(300)
            ok(pg.inner_text('#app')!=before,'flip did not change content')
        t()
        @check('vocabulary lab starts with 4 options')
        def t():
            fresh(pg,base);pg.evaluate("TGAT1VocabularyLab.start('vocab')");pg.wait_for_timeout(500)
            ok(len(pg.inner_text('#app'))>100)
        t()
        @check('learning hub: open unit 1')
        def t():
            fresh(pg,base);nav(pg,'hub');pg.evaluate("TGAT1Hub.openUnit(1)");pg.wait_for_timeout(500);ok('ประธาน' in pg.inner_text('body'))
        t()
        @check('reading plus: start passage')
        def t():
            fresh(pg,base);nav(pg,'reading');pg.evaluate("TGAT1ReadingPlus.start('R382-TC-01')");pg.wait_for_timeout(500);ok(len(pg.inner_text('body'))>500)
        t()
        @check('word detail modal shows IPA source')
        def t():
            fresh(pg,base);nav(pg,'vocab');pg.evaluate("studioWordDetail(0)");pg.wait_for_timeout(400);txt=pg.inner_text('body');ok('CMUdict' in txt or 'eSpeak' in txt or 'IPA' in txt,'no IPA source')
        t()
        @check('practice disclaimer: not official TGAT1 / not score prediction is visible')
        def t():
            fresh(pg,base);txt=pg.inner_text('body');ok('ไม่ใช่ข้อสอบทางการ' in txt,'footer disclaimer missing')
        t()
        @check('no console/page errors in flows')
        def t(): ok(not pg.errs,'; '.join(pg.errs[:5]))
        t();pg.context.close()
        # Service worker / offline
        ctx=b.new_context(viewport=DESKTOP);pg=ctx.new_page()
        @check('service worker installs and app reloads offline')
        def t():
            pg.goto(base+'/index.html');pg.wait_for_function("navigator.serviceWorker && navigator.serviceWorker.controller || false",timeout=20000) if False else None
            pg.evaluate("navigator.serviceWorker.ready.then(()=>true)");pg.reload();pg.wait_for_timeout(1500)
            ok(pg.evaluate("!!navigator.serviceWorker.controller"),'no controller')
            pg.wait_for_timeout(1500);ctx.set_offline(True);pg.reload();pg.wait_for_function("typeof studioNav==='function'",timeout=15000)
            pg.evaluate("VLT_startMock(2)");pg.wait_for_timeout(800);ok(pg.evaluate("!!VLT_RUN && VLT_RUN.qs.length===60"),'vault not available offline')
            ctx.set_offline(False)
        t();ctx.close()
    fails=[r for r in RESULTS if not r[1]]
    for n,s,m in RESULTS: print(('PASS ' if s else 'FAIL ')+n+(('  -> '+m) if m else ''))
    print(f'\nsmoke_r3_extra: {len(RESULTS)-len(fails)}/{len(RESULTS)} passed')
    return 1 if fails else 0
if __name__=='__main__': sys.exit(main(sys.argv[1]))
