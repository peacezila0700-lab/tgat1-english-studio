#!/usr/bin/env python3
"""TGAT1 English Studio smoke test.

Opens the app in a real (headless) Chrome exactly like a new student would and checks the
things that broke in v40.7.30: buttons that did nothing on first launch, the endless
"coach box" loop after answering, broken Thai meanings, offline mode and the update flow.
v40.8.0 adds Learning Hub checks (70 units, Continue Learning, hints, locking, resume, offline)
and content/version consistency checks.

Setup (once):
    pip install playwright
    python -m playwright install chromium
Run:
    python smoke_test.py ../TGAT1-English-Studio
Exit code 0 = everything passed.
"""
import asyncio, functools, http.server, json, os, re, socketserver, sys, threading
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    sys.exit('Playwright is missing: pip install playwright && python -m playwright install chromium')

APP = Path(sys.argv[1] if len(sys.argv) > 1 else '../TGAT1-English-Studio').resolve()
PAGES = ['home', 'hub', 'profile', 'vocab', 'exam', 'reading', 'game', 'analytics', 'settings']
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))


def serve(directory):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(directory))
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f'http://127.0.0.1:{httpd.server_address[1]}/index.html'


def load_js_json(path, prefix):
    s = path.read_text(encoding='utf-8')
    body = s[s.index(prefix) + len(prefix):].rstrip()
    return json.loads(body[:-1] if body.endswith(';') else body)


def content_checks():
    data = load_js_json(APP / 'data.js', 'window.__TGAT1_DATA=')
    senses = load_js_json(APP / 'data-senses.js', 'window.__TGAT1_SENSES=')
    words = data['studio']['words']
    thai = re.compile(r'[฀-๿]')
    no_thai = [w['w'] for w in words if not thai.search(w.get('th') or '')]
    half = [w['w'] for w in words if re.match(r'^[A-Za-z]+ \+ ', w.get('th') or '')]
    mixed = []
    glued = re.compile(r'[฀-๿][A-Za-z]{2,}|[A-Za-z]{2,}[฀-๿]')
    for k, wi in enumerate(data['lazySenses']):
        for se in senses[k] or []:
            if glued.search(se.get('translation') or ''):
                mixed.append(words[wi]['w'])
    check('content: every word has a Thai meaning', not no_thai, ', '.join(no_thai[:5]))
    check('content: no half-translated "word + word" meanings', not half, ', '.join(half[:5]))
    check('content: example translations are not Thai/English glued', not mixed, ', '.join(mixed[:5]))


async def new_page(browser, url, width=1280, sw=False):
    ctx = await browser.new_context(service_workers='allow' if sw else 'block',
                                    viewport={'width': width, 'height': 900 if width > 600 else 844})
    page = await ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)[:160]))
    page.on('console', lambda m: errors.append(m.text[:160]) if m.type == 'error' and 'Service Worker registration blocked' not in m.text else None)
    await page.goto(url)
    await page.wait_for_timeout(1500)
    return ctx, page, errors


async def main():
    content_checks()
    httpd, url = serve(APP)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None, args=['--no-sandbox'])

        # 1) every page renders without errors, desktop and phone
        for width in (1280, 390):
            ctx, page, errors = await new_page(browser, url, width)
            for name in PAGES:
                await page.evaluate(f"studioNav('{name}')")
                await page.wait_for_timeout(1300)
                n = await page.evaluate("document.querySelector('#app').innerText.length")
                over = await page.evaluate("document.documentElement.scrollWidth-window.innerWidth")
                check(f'page {name} @{width}px renders', n > 200 and over <= 2, f'text={n} overflow={over}')
            check(f'no JavaScript errors @{width}px', not errors, '; '.join(errors[:3]))
            await ctx.close()

        # 2) start buttons work on a fresh launch (question bank not loaded yet)
        starts = {
            'Daily mission': 'VLT_startDaily()', 'Quick 10': 'VLT_startQuick()', '90-second sprint': 'VLT_startSprint()',
            'Practice by part (rc)': "VLT_startCategory('rc')", 'Mock set 1': 'VLT_startMock(1)',
            'Random full mock': 'VLT_startRandomMock()', 'Adaptive diagnostic': 'TGAT1Adaptive.start()',
        }
        for label, call in starts.items():
            ctx, page, errors = await new_page(browser, url)
            await page.evaluate(call)
            await page.wait_for_timeout(2500)
            text = await page.evaluate("document.querySelector('#app').innerText.slice(0,80)")
            check(f'fresh launch: {label} opens a question', re.search(r'ข้อ(ที่)? ?1', text), text.replace('\n', ' ')[:60])
            await ctx.close()

        # 3) answering a question must not make the page grow forever; finish a whole run
        ctx, page, errors = await new_page(browser, url)
        await page.evaluate("studioNav('exam')")  # preload the bank so this test is independent of test 2
        await page.wait_for_timeout(2500)
        await page.evaluate('VLT_startQuick()')
        await page.wait_for_timeout(1500)
        first = page.locator('#app [onclick^="VLT_answer"]')
        if not await first.count():
            check('answering: a question is shown', False, 'no answer buttons')
            await ctx.close()
            first = None
        if first is not None:
            await first.first.click(force=True)
            await page.wait_for_timeout(500)
            h1 = await page.evaluate('document.documentElement.scrollHeight')
            await page.wait_for_timeout(2000)
            h2 = await page.evaluate('document.documentElement.scrollHeight')
            check('answering: page height stays stable', h2 - h1 < 50, f'{h1}px -> {h2}px')
            coach = await page.evaluate("document.querySelectorAll('.tg36-coach-wrap').length")
            check('answering: one coach box per question', coach <= 1, f'{coach} boxes')
            for _ in range(12):
                nxt = page.locator('#app [onclick^="VLT_next"]')
                if await nxt.count():
                    await nxt.first.click(force=True)
                    await page.wait_for_timeout(300)
                opts = page.locator('#app [onclick^="VLT_answer"]')
                if not await opts.count():
                    break
                await opts.first.click(force=True)
                await page.wait_for_timeout(300)
            await page.wait_for_timeout(800)
            text = await page.evaluate("document.querySelector('#app').innerText")
            check('a full 10-question run reaches the results page', 'ผลการฝึก' in text, text[:60].replace('\n', ' '))
            await ctx.close()

        # 4) a vocabulary game started from Home shows only the game
        ctx, page, errors = await new_page(browser, url)
        await page.evaluate("studioRunVocabGame('match')")
        await page.wait_for_timeout(1500)
        leak = await page.evaluate("!!document.querySelector('#app #tg36CoachPlan')")
        check('vocab game from Home has no Home blocks inside', not leak)
        await ctx.close()

        # 6) Learning Hub (v40.8.0)
        ctx, page, errors = await new_page(browser, url)
        cur = await page.evaluate("""(()=>{const c=TGAT1_HUB_CURRICULUM,ids=new Set(c.items.map(x=>x[0]));
          const bad=c.units.filter(u=>!u.concepts.length||!u.learn||!(u.guided||(u.act||[]).some(a=>a.type==='mock'))||!u.assess);
          const missing=c.units.flatMap(u=>(u.guided&&u.guided.ids)||[]).filter(i=>!ids.has(i));
          return {n:c.units.length,seq:c.units.every((u,i)=>u.n===i+1),bad:bad.length,missing:missing.length,withAppActivities:c.units.filter(u=>(u.act||[]).length).length}})()""")
        check('hub: exactly 70 sequential units, each with concepts, lesson, practice (guided or full mock) and an assessment',
              cur['n'] == 70 and cur['seq'] and not cur['bad'] and not cur['missing'], str(cur))
        await page.evaluate("studioNav('hub')"); await page.wait_for_timeout(600)
        await page.evaluate("TGAT1Hub.continue()"); await page.wait_for_timeout(600)
        text = await page.evaluate("document.querySelector('#app').innerText")
        check('hub: Continue Learning on a fresh launch opens Unit 1', 'หน่วยที่ 1' in text, text[:80].replace('\n', ' '))
        await page.evaluate("TGAT1Hub.learnDone(1)"); await page.wait_for_timeout(900)
        opts = await page.evaluate("document.querySelectorAll('#app .lh-opt').length")
        check('hub: guided practice shows a question with 4 options', opts == 4, f'options={opts}')
        right = await page.evaluate("""(()=>{const r=TGAT1Hub.state().active,ref=r.items[r.i];
          const it=TGAT1_HUB_CURRICULUM.items.find(x=>x[0]===ref.id);const ans=ref.src==='bank'?VLT_get(ref.id).answer:it[6];return ref.o.indexOf(ans)})()""")
        await page.evaluate(f"TGAT1Hub.pick({(right + 1) % 4})"); await page.wait_for_timeout(400)
        ph = await page.evaluate("TGAT1Hub.state().active.phase")
        shown = await page.evaluate("!!document.querySelector('#app .lh-opt.is-correct, #app .lh-opt.correct')")
        check('hub: a first wrong answer gives a hint and a second chance (answer not revealed)', ph == 'hint' and not shown, f'phase={ph}')
        await page.reload(); await page.wait_for_timeout(1500)
        na = await page.evaluate("TGAT1Hub.nextAction().k")
        check('hub: an unfinished activity is resumed after reload', na == 'resume', na)
        await page.evaluate("TGAT1Hub.pause()"); await page.wait_for_timeout(300)
        before = await page.evaluate("JSON.stringify(TGAT1Hub.state().active)")
        await page.evaluate("TGAT1Hub.step(5,'learn')"); await page.wait_for_timeout(400)
        after = await page.evaluate("JSON.stringify(TGAT1Hub.state().active)")
        check('hub: later units stay locked (no skipping)', before == after)
        v = await page.evaluate("""(async()=>{const m=document.querySelector('meta[name=tgat1-version]').content;
          const sw=await (await fetch('sw.js')).text();const mf=await (await fetch('manifest.webmanifest')).text();
          return {meta:m,app:TGAT1_VERSION.app,cache:TGAT1_VERSION.cache,swOk:sw.includes("'"+TGAT1_VERSION.cache+"'"),mfOk:mf.includes('v'+TGAT1_VERSION.app),
                  hubFiles:['learning-hub.js','learning-hub.css','learning-hub-curriculum.js'].every(f=>sw.includes('./'+f))}})()""")
        check('versions: index, app, manifest and service worker agree', v['meta'] == v['app'] and v['swOk'] and v['mfOk'], str(v))
        check('service worker caches the Learning Hub files', v['hubFiles'])
        audit = await page.evaluate("TGAT1_CONTENT_AUDIT_V408.run()")
        bk, vo, rl = audit['bank'], audit['vocabulary'], audit['readingLab']['answerPositions']
        check('content audit: no placeholder Thai meanings or mismatched placeholder translations',
              vo['placeholderMeanings'] == 0 and vo['mismatchedPlaceholderTranslations'] == 0, str({k: vo[k] for k in ('placeholderMeanings', 'mismatchedPlaceholderTranslations')}))
        check('content audit: no punctuation-cue, fragment-key or generic-distractor questions in the bank',
              bk['structuralCueCount'] == 0 and bk['fragmentKeyCount'] == 0 and bk['genericDistractorCount'] == 0,
              str({k: bk[k] for k in ('structuralCueCount', 'fragmentKeyCount', 'genericDistractorCount')}))
        check('content audit: Reading Lab answers use all four positions', min(rl) > 0, str(rl))
        check('no JavaScript errors in Learning Hub checks', not errors, '; '.join(errors[:3]))
        await ctx.close()

        # 5) service worker: no surprise reload on first visit; exam works offline
        ctx = await browser.new_context(service_workers='allow')
        page = await ctx.new_page()
        navs = []
        page.on('framenavigated', lambda f: navs.append(f.url) if f == page.main_frame else None)
        await page.goto(url)
        await page.wait_for_timeout(7000)
        check('first visit does not reload the page by itself', len(navs) == 1, f'{len(navs) - 1} reload(s)')
        await ctx.set_offline(True)
        await page.reload()
        await page.wait_for_timeout(2500)
        await page.evaluate("studioNav('exam')")
        await page.wait_for_timeout(3000)
        bank = await page.evaluate('VLT_BANK.length')
        check('offline: exam question bank loads from cache', bank == 1200, f'bank={bank}')
        await page.evaluate("studioNav('hub')")
        await page.wait_for_timeout(1500)
        hubtext = await page.evaluate("document.querySelector('#app').innerText")
        check('offline: Learning Hub opens from cache', 'หน่วย' in hubtext and 'Continue' in hubtext, hubtext[:60].replace('\n', ' '))
        await ctx.close()

        await browser.close()
    httpd.shutdown()
    failed = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(failed)}/{len(results)} checks passed')
    sys.exit(1 if failed else 0)


asyncio.run(main())
