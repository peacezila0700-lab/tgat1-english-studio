#!/usr/bin/env python3
"""TGAT1 English Studio v42.0.0 regression + content-integrity suite.

Complements smoke_test.py (49 checks). Covers the defects fixed in v42.0.0 and the end-to-end flows
listed in the audit brief: vocabulary search/detail, Vocabulary Lab + SRS, Hub unit vocabulary,
a complete mock, save/resume, export/import, offline/PWA, 390px/1280px overflow, keyboard focus and
an axe-core accessibility scan (optional: set AXE_PATH=/path/to/axe.min.js).

Run:  python regression_v41.py ../TGAT1-English-Studio   (exit 0 = all PASS)
Content checks print the remaining HUMAN-REVIEW counts; those are reported, not failed.
"""
import asyncio, functools, http.server, json, os, re, socketserver, sys, threading, datetime
from pathlib import Path
from playwright.async_api import async_playwright

APP = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
AXE = os.environ.get('AXE_PATH')
EXPECT_VERSION = '42.0.1'
PAGES = ['home', 'hub', 'profile', 'vocab', 'exam', 'reading', 'game', 'analytics', 'settings']
results, notes = [], []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))


def note(msg):
    notes.append(msg); print('INFO ' + msg)


def load_val(path, prefix):
    s = path.read_text(encoding='utf-8')
    val, _ = json.JSONDecoder().raw_decode(s[s.index(prefix) + len(prefix):])
    return val


# ---------------------------------------------------------------- content (static)
META = re.compile(r"^(The lesson shows how to use|The (adjective|verb|noun|adverb|phrase|word) ['‘’“”][^'’”]+['’”] (gives|appears)|The writer uses ['‘’“”]|The report uses ['‘’“”]|"
                  r"The article examines the role of ['‘’“”]|The report introduces ['‘’“”]|Understanding ['‘’“”]|The passage introduces ['‘’“”])")
BROKEN_FILLERS = [r"^The committee considered the proposal \w+\.$", r"^The team responded \w+ to the ", r"^The team decided to [\w ]+ the (plan|proposal) after reviewing the evidence\.$",
                  r"^The researchers \w+ as conditions changed\.$", r"^The study examined why organizations need to [\w ]+ the issue\.$", r"^The situation became \w+ after the change\.$",
                  r"^The situation changed \w+ after the announcement\.$", r"^The report said the new approach was \w+ for most users\.$", r"^The team considered the response \w+ under the circumstances\.$"]
NOUN_FILLERS = [r"^The researchers discussed .+ before deciding how to proceed\.$", r"^The .+ affected the team.s final decision\.$", r"^The policy addresses concerns about .+\.$",
                r"^The school provided guidance about .+ to students\.$", r"^The community discussed .+ after the announcement\.$", r"^The report highlighted .+ as an important factor",
                r"^The team collected information about .+ before making a decision\.$", r"^The company reviewed the risks associated with .+\.$", r"^The survey measured changes related to .+\.$",
                r"^The study compared the effects of .+ across two groups\.$", r"^The study examined .+ and its effects on the community\.$", r"^The report discussed .+ as an important part of the analysis\.$"]


def content_checks():
    data = load_val(APP / 'data.js', 'window.__TGAT1_DATA=')
    senses = load_val(APP / 'data-senses.js', 'window.__TGAT1_SENSES=')
    W = data['studio']['words']
    lazy = {wi: k for k, wi in enumerate(data['lazySenses'])}
    rows = []
    for i, w in enumerate(W):
        ss = senses[lazy[i]] if i in lazy else (w.get('senses') or [])
        for s in ss:
            rows.append((w, s))
    check('content: 3,508 unique headwords and 3,400 lazy sense sets preserved', len(W) == 3508 and len({w['w'] for w in W}) == 3508 and len(senses) == 3400, f'{len(W)}/{len(senses)}')
    check('content: 535 phrases preserved', len(data['studio']['phrases']) == 535, str(len(data['studio']['phrases'])))
    lat = [w['w'] for w in W if re.search(r'[A-Za-z]', w['th'])]
    check('content: main Thai glosses contain no English (comparisons live in note)', not lat, ', '.join(lat[:6]))
    dash = [w['w'] for w in W if re.search(r'\s-\s', w['th'])]
    check('content: no antonym pair (A - B) inside a main gloss', not dash, ', '.join(dash[:6]))
    tag = [w['w'] for w in W if re.search(r'\(ใช้(ในบริบทของ|กับการจัดการ)', w['th'])]
    check('content: no spurious "(ใช้ในบริบทของ…)" tags in glosses', not tag, ', '.join(tag[:6]))
    leak = [w['w'] for w in W if re.search(r'การเปลี่ยนแปลงเกิดขึ้น|ตามรายงาน$', w['th'])] + [w['w'] for w, s in rows if re.search(r'การเปลี่ยนแปลงเกิดขึ้น', s.get('meaning') or '')]
    check('content: no template sentence used as a gloss/meaning', not leak, ', '.join(leak[:6]))
    bad_paren = [w['w'] for w in W if w['th'].count('(') != w['th'].count(')') or re.match(r'^\s*[+;)]', w['th'])]
    check('content: no truncated/unbalanced gloss', not bad_paren, ', '.join(bad_paren[:6]))
    meta = [w['w'] for w, s in rows if META.search(s.get('example') or '')]
    check('content: no meta-language examples ("The adjective X gives…")', not meta, f'{len(meta)}: ' + ', '.join(meta[:6]))
    broken = [w['w'] for w, s in rows if any(re.match(p, s.get('example') or '') for p in BROKEN_FILLERS)]
    check('content: no adjective/adverb/verb filler templates', not broken, f'{len(broken)}: ' + ', '.join(broken[:6]))
    tmpl_tr = [w['w'] for w, s in rows if re.search(r'^บทอ่านเปรียบเทียบคำว่า|^สถานการณ์.+ - .+หลังจากมีการเปลี่ยนแปลง', s.get('translation') or '')]
    check('content: no template Thai translations', not tmpl_tr, ', '.join(tmpl_tr[:6]))
    empty = [w['w'] for w, s in rows if not (s.get('example') and s.get('translation') and s.get('meaning') and s.get('pos'))]
    check('content: every sense has pos, meaning, example and translation', not empty, ', '.join(empty[:6]))
    vpos = [w['w'] for w, s in rows if w['cat'] == 'คำที่มักสับสน' and s.get('pos') == 'v' and not re.search(r'\bv\b|phr v', w['pos'])]
    check('content: confusable-category senses no longer mislabelled as verbs', not vpos, ', '.join(vpos[:6]))
    poly = {w['w']: len(senses[lazy[i]] if i in lazy else w.get('senses') or []) for i, w in enumerate(W) if w['w'] in ('account', 'address', 'claim', 'issue', 'attempt', 'relative')}
    check('content: polysemy split (account/address/claim/issue ≥3 senses; attempt/relative ≥2)', all(poly[k] >= 3 for k in ('account', 'address', 'claim', 'issue')) and poly['attempt'] >= 2 and poly['relative'] >= 2, str(poly))
    off = [w['w'] for w in W if 'GAT รุ่นเก่า' in w['cat'] or w['cat'].startswith('TGAT1 Exam Vocabulary')]
    check('content: no category label implying official/past-paper TGAT1 content', not off, ', '.join(off[:4]))
    researchers = [(w['w'],s) for w,s in rows if re.match(r'The researchers discussed .+ before deciding how to proceed\.',s.get('example') or '',re.I)]
    bad_research = [w for w,s in researchers if (s.get('translation') or '').startswith('ทีมได้หารือเกี่ยวกับ')]
    check('Round 2: all 492 researchers translations name researcher(s), not team', len(researchers)==492 and not bad_research, f'{len(researchers)} rows; {len(bad_research)} still wrong')
    glued = [w['w'] for w,s in rows if re.search(r'[ก-๙](?:the plan|the first option|the customer|the request)',s.get('translation') or '')]
    check('Round 2: no four confirmed glued Thai-English translations remain', not glued, ', '.join(glued[:5]))
    meta_round2 = [w['w'] for w,s in rows if re.search(r'“(?:additionally|inspect|unfortunately|online|data|likely|crowded)” (?:adds information|describes a feature)',s.get('example') or '')]
    check('Round 2: seven confirmed meta-language examples are removed', not meta_round2, ', '.join(meta_round2[:7]))
    untranslated = [w['w'] for w,s in rows if (s.get('translation') or '') in ('เกี่ยวกับงบประมาณ','เกี่ยวกับบริษัท','เกี่ยวกับการศึกษา','เกี่ยวกับสติปัญญา','เชิงวิชาการ') and re.search(r'\b(?:budgetary|corporate|educational|intellectual|scholarly)\b',s.get('example') or '',re.I)]
    check('Round 2: five adjective example translations are not gloss-only', not untranslated, ', '.join(untranslated))
    for item in data.get('pack',{}).get('textCompletion',[]):
        item['actualWordCount']=len(re.findall(r"\b[\w’'-]+\b",re.sub(r'\(\d+\)',' ',item.get('content',''))))
    wrong_tc_counts=[x['id'] for x in data.get('pack',{}).get('textCompletion',[]) if x.get('wordCount')!=x.get('actualWordCount')]
    check('Round 2: Reading Lab TC counts exclude numbered blanks', not wrong_tc_counts, ', '.join(wrong_tc_counts))
    off_levels=[x['id'] for x in data.get('pack',{}).get('readingComprehension',[])+data.get('pack',{}).get('textCompletion',[]) if x.get('level')!='ระดับความยากโดยประมาณ · ไม่ใช่ CEFR']
    check('Round 2: Reading Lab levels are explicitly approximate, not CEFR', not off_levels, ', '.join(off_levels))
    phrase_types={x.get('type') for x in data['studio']['phrases']}
    check('Round 2: phrase taxonomy normalized to at most 10 labels', len(phrase_types)<=10, str(len(phrase_types)))
    nf = sum(1 for w, s in rows if any(re.match(p, s.get('example') or '') for p in NOUN_FILLERS))
    note(f'HUMAN-REVIEW queue: {nf} noun-slot filler examples remain (grammatical-but-generic or missing article) — see REVIEW-QUEUE.csv')
    return data


# ---------------------------------------------------------------- browser helpers
def serve(directory):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(directory)))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f'http://127.0.0.1:{httpd.server_address[1]}/index.html'


async def page_for(browser, url, width=1280, sw=False, **kw):
    ctx = await browser.new_context(service_workers='allow' if sw else 'block', viewport={'width': width, 'height': 900 if width > 600 else 844}, **kw)
    page = await ctx.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:160]))
    page.on('console', lambda m: errs.append(m.text[:160]) if m.type == 'error' and 'Service Worker registration blocked' not in m.text else None)
    await page.goto(url); await page.wait_for_timeout(1500)
    return ctx, page, errs


async def main():
    content_checks()
    httpd, url = serve(APP)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None, args=['--no-sandbox'])

        # 1) version + bank structure (blueprint)
        ctx, page, errs = await page_for(browser, url)
        v = await page.evaluate("""(async()=>{const sw=await (await fetch('sw.js')).text();const mf=await (await fetch('manifest.webmanifest')).json();
            return {app:TGAT1_VERSION.app,meta:document.querySelector('meta[name=tgat1-version]').content,cache:TGAT1_VERSION.cache,sw:/tgat1-studio-v([\\d.]+)/.exec(sw)[1],mf:mf.version}})()""")
        check(f'versions: app/meta/cache/sw/manifest all {EXPECT_VERSION}', v['app'] == v['meta'] == EXPECT_VERSION and v['cache'] == 'tgat1-studio-v' + EXPECT_VERSION and v['sw'] == EXPECT_VERSION and v['mf'] == 'v' + EXPECT_VERSION, str(v))
        await page.evaluate('VLT_ensureBank()'); await page.wait_for_timeout(800)
        bank = await page.evaluate("""(()=>{const B=VLT_BANK,ids=new Set(B.map(q=>q.id));const sets={};const bad=[];
          for(const q of B){(sets[q.set]=sets[q.set]||{qr:0,short:0,long:0,tc:0,rc:0})[q.category]++;
            const o=q.options||[];if(o.length!==4||new Set(o.map(x=>String(x).trim())).size!==4||o.some(x=>!String(x).trim())||!(q.answer>=0&&q.answer<4))bad.push(q.id);}
          const rcLen={};for(const q of B.filter(q=>q.category==='rc')){const n=String(q.context||'').trim().split(/\\s+/).length;rcLen[q.set+'|'+n]=n}
          const lens=Object.values(rcLen), longContexts=new Set(B.filter(q=>q.category==='long').map(q=>q.context)), tcContexts=new Set(B.filter(q=>q.category==='tc').map(q=>q.context)),tcPos=[0,0,0,0];
          for(const q of B.filter(q=>q.category==='tc'))if(q.answer>=0&&q.answer<4)tcPos[q.answer]++;
          return {n:B.length,unique:ids.size,bad:bad.length,sets:Object.keys(sets).length,dist:Object.values(sets).every(s=>s.qr===10&&s.short===10&&s.long===10&&s.tc===15&&s.rc===15),
                  rcMin:Math.min(...lens),rcMax:Math.max(...lens),rcPassages:lens.length,longContexts:longContexts.size,tcContexts:tcContexts.size,tcPos}})()""")
        check('bank: 1,200 unique questions, 4 distinct non-empty options, valid answer', bank['n'] == 1200 and bank['unique'] == 1200 and bank['bad'] == 0, str(bank))
        check('bank: 20 sets × (QR10/Short10/Long10/TC15/RC15) blueprint split', bank['sets'] == 20 and bank['dist'], str(bank))
        check('Round 2: 40 unique Long Conversation contexts and 40 unique Text Completion passages', bank['longContexts']==40 and bank['tcContexts']==40, str(bank))
        check('Round 2: TC answer positions are balanced 75/75/75/75', bank['tcPos']==[75,75,75,75], str(bank['tcPos']))
        check('bank: RC passages 100–200 words', 100 <= bank['rcMin'] and bank['rcMax'] <= 200, str(bank))

        # 1b) Vocabulary matching game: each round must have five unique words and unambiguous glosses.
        match = await page.evaluate("""(()=>{const rounds=Array.from({length:12},()=>mkMatch(pick(byLv(S.cur),5)));return rounds.map(q=>({n:q.L.length,words:q.L.map(i=>V[i][0].toLowerCase()),meanings:q.L.map(i=>String(V[i][1]).split(';')[0].normalize('NFKC').toLowerCase().replace(/[\\s.,;:!?。；，]+/g,' ').trim()),left:q.l.length,right:q.r.length,permutation:q.L.every(i=>q.l.includes(i)&&q.r.includes(i))}))})()""")
        check('match game: 12 generated rounds each contain 5 unique words, unique first-gloss meanings and balanced columns', len(match)==12 and all(x['n']==x['left']==x['right']==5 and len(set(x['words']))==5 and len(set(x['meanings']))==5 and x['permutation'] for x in match), str(match[:2]))
        await page.evaluate("play('match')")
        solved = await page.evaluate("""(()=>{const q=Q.qs[0];for(const i of q.L){mt('l',i);mt('r',i)}return {matches:q.dn.length,expected:q.L.length,answered:Q.ans!==null}})()""")
        check('match game: correct word–meaning pairs complete the round without mismatch penalties', solved['matches']==solved['expected']==5 and solved['answered'], str(solved))
        await ctx.close()
        ctx, page, errs = await page_for(browser, url)

        # 2) Vocabulary Lab option integrity (the v41 P0 fix) — many generated items, read through the QA hook
        await page.evaluate("TGAT1LazySenses.ensure()"); await page.wait_for_timeout(600)
        lab = await page.evaluate("""(()=>{const L=TGAT1VocabularyLab.list();let items=0,latin=0,dup=0,shared=0,nullOpt=0,ansMiss=0;const seen={};
          const key=s=>String(s||'').normalize('NFC').toLowerCase().replace(/[^\\p{L}\\p{M}\\p{N}]+/gu,' ').trim();
          const parts=t=>String(t||'').replace(/\\([^)]*\\)/g,' ').split(/[;,/]|\\s-\\s/).map(key).filter(Boolean);
          for(const x of L.slice(0,300)){const o=TGAT1VocabularyLab._optionsFor(x.w);if(!o){nullOpt++;continue}items++;
            if(o.filter(t=>t===x.th).length!==1)ansMiss++;if(new Set(o.map(key)).size!==4)dup++;
            o.forEach(t=>{if(/[A-Za-z]/.test(t))latin++;seen[t]=(seen[t]||0)+1});
            const ps=o.map(parts);for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)if(ps[i].some(p=>ps[j].includes(p)))shared++;}
          return {pool:L.length,items,latin,dup,shared,ansMiss,nullOpt,distinctOptions:Object.keys(seen).length}})()""")
        check('vocab lab: options are Thai-only, 4 distinct, exactly one matches the target', lab['items'] >= 250 and lab['latin'] == 0 and lab['dup'] == 0 and lab['ansMiss'] == 0, str(lab))
        check('vocab lab: no two options share a meaning segment (single defensible answer)', lab['shared'] == 0, str(lab))
        check('vocab lab: distractors drawn from a wide pool (not a fixed handful)', lab['distinctOptions'] > 400, str(lab))

        # 3) vocab search + detail (note shown, gloss clean)
        await page.evaluate("studioNav('vocab')"); await page.wait_for_timeout(500)
        await page.evaluate("studioVSearch('deteriorate')"); await page.wait_for_timeout(700)
        found = await page.evaluate("[...document.querySelectorAll('#app .st-word b')].some(e=>e.textContent.trim()==='deteriorate')")
        check('vocab: search finds "deteriorate"', found)
        i_det = await page.evaluate("STUDIO_DATA.words.findIndex(w=>w.w==='deteriorate')")
        await page.evaluate(f"studioWordDetail({i_det})"); await page.wait_for_timeout(900)
        modal = await page.evaluate("(document.querySelector('#studioModal')||{}).innerText||''")
        check('vocab detail: main meaning is "แย่ลง" (not "ดีขึ้น - แย่ลง") and comparison is shown as a note', 'แย่ลง; เสื่อมลง' in modal and 'ดีขึ้น - แย่ลง' not in modal and 'หมายเหตุ: คู่ตรงข้าม' in modal, modal[:160].replace('\n', ' '))
        check('vocab detail: level shown as internal difficulty group, not CEFR', 'กลุ่มความยาก' in modal and 'ภายในแอป' in modal)
        await page.evaluate("studioCloseModal&&studioCloseModal()")

        # 4) Vocabulary Lab full round + SRS log, separate from mock scores
        before = await page.evaluate("({log:(STUDIO_VSTATE.reviewLog||[]).length,hist:(VLT_STATE.history||[]).length,sets:JSON.stringify(VLT_STATE.completedSets||{})})")
        await page.evaluate("TGAT1VocabularyLab.start('mixed')"); await page.wait_for_timeout(700)
        snap = await page.evaluate("TGAT1VocabularyLab.snapshot()")
        n = len(snap['items']) if snap else 0
        for k in range(n):
            await page.evaluate("TGAT1VocabularyLab.answer(0)"); await page.wait_for_timeout(40)
            await page.evaluate("TGAT1VocabularyLab.grade(true)"); await page.wait_for_timeout(40)
        after = await page.evaluate("({log:(STUDIO_VSTATE.reviewLog||[]).length,hist:(VLT_STATE.history||[]).length,sets:JSON.stringify(VLT_STATE.completedSets||{}),saved:!!localStorage.getItem('tgat1_studio_vocab_progress_v1')})")
        check('vocab lab: full round writes one SRS log entry per item and persists to storage', n >= 5 and after['log'] - before['log'] == n and after['saved'], f'n={n} {before}->{after}')
        await page.reload(); await page.wait_for_timeout(1500)
        kept = await page.evaluate("({log:(STUDIO_VSTATE.reviewLog||[]).length,items:Object.keys(STUDIO_VSTATE.items).length,kind:((STUDIO_VSTATE.sessions||[]).slice(-1)[0]||{}).kind})")
        check('vocab lab: SRS grades survive a reload (regression for the lost-progress bug)', kept['log'] == after['log'] and kept['items'] >= n and kept['kind'] == 'examVocab', str(kept))
        check('vocab lab: does not change mock history or completed sets', after['hist'] == before['hist'] and after['sets'] == before['sets'])
        await page.evaluate("TGAT1VocabularyLab.start('mixed')"); await page.wait_for_timeout(500)
        await page.evaluate("TGAT1VocabularyLab.exit()"); await page.wait_for_timeout(400)
        check('vocab lab: exit returns to the vocabulary page', await page.evaluate("STUDIO_PAGE==='vocab' && !TGAT1VocabularyLab.snapshot()"))
        check('no JavaScript errors in vocabulary flows', not errs, '; '.join(errs[:3]))
        await ctx.close()

        # 5) Hub shortcut + unit vocabulary does not complete the unit
        ctx, page, errs = await page_for(browser, url)
        await page.evaluate("studioNav('hub')"); await page.wait_for_timeout(600)
        hub0 = await page.evaluate("JSON.stringify((TGAT1Hub.state().units||TGAT1Hub.state().done||{}))")
        await page.evaluate("TGAT1VocabularyLab.start('unit',1)"); await page.wait_for_timeout(1500)
        snap = await page.evaluate("TGAT1VocabularyLab.snapshot()")
        n = len(snap['items']) if snap else 0
        for k in range(n):
            await page.evaluate("TGAT1VocabularyLab.answer(0)"); await page.wait_for_timeout(40)
            await page.evaluate("TGAT1VocabularyLab.grade(false)"); await page.wait_for_timeout(40)
        st = await page.evaluate("TGAT1Hub.state()")
        hub1 = json.dumps(st.get('units') or st.get('done') or {}, separators=(',', ':'))
        logged = any((e.get('k') == 'vocab' and e.get('u') == 1) for e in (st.get('history') or []))
        check('hub: unit-1 vocabulary activity runs (≥5 items) and is logged', n >= 5 and logged, f'n={n} logged={logged}')
        check('hub: vocabulary practice does not mark the unit complete', hub0.replace(' ', '') == hub1.replace(' ', ''), f'{hub0[:80]} -> {hub1[:80]}')
        check('no JavaScript errors in Hub vocabulary flow', not errs, '; '.join(errs[:3]))
        await ctx.close()

        # 6) full mock (all correct) -> 100/100 ; save/resume mid-mock
        ctx, page, errs = await page_for(browser, url)
        await page.evaluate("VLT_startMock(1)"); await page.wait_for_timeout(1500)
        await page.evaluate("(()=>{const r=VLT_RUN;for(let i=0;i<3;i++){VLT_goto(i);VLT_answer(r.qs[i].answer)}})()"); await page.wait_for_timeout(300)
        await page.evaluate("window.dispatchEvent(new Event('pagehide'))"); await page.wait_for_timeout(200)
        await page.reload(); await page.wait_for_timeout(2500)
        resumed = await page.evaluate("(()=>{const s=JSON.parse(localStorage.getItem('tgat1_vlt_active_run_v1')||'null');return {saved:!!(s&&s.run),answered:s&&s.run?Object.keys(s.run.answers||{}).length:0,live:!!VLT_RUN}})()")
        check('save/resume: an in-progress mock is saved and survives a reload', resumed['saved'] and resumed['answered'] >= 3, str(resumed))
        await page.evaluate("VLT_exit&&VLT_exit()"); await page.wait_for_timeout(300)
        await page.evaluate("VLT_startMock(2)"); await page.wait_for_timeout(1200)
        await page.evaluate("(()=>{const r=VLT_RUN;r.qs.forEach((q,i)=>{VLT_goto(i);VLT_answer(q.answer)});VLT_finish()})()"); await page.wait_for_timeout(1200)
        res = await page.evaluate("(()=>{const t=document.querySelector('#app').innerText;const h=(VLT_STATE.history||[]).slice(-1)[0]||{};return {t:t.slice(0,400),score:h.score,total:h.total,scale:VLT_STATE.scoreScale}})()")
        check('mock: a complete 60-question mock finishes and scores 100/100 on the /100 scale', res['score'] == 100 and res['total'] == 100 and res['scale'] == 100, str({k: res[k] for k in ('score', 'total', 'scale')}))
        check('no JavaScript errors in mock/resume flows', not errs, '; '.join(errs[:3]))
        await ctx.close()

        # 7) export / import round-trip
        ctx, page, errs = await page_for(browser, url, accept_downloads=True)
        await page.evaluate("localStorage.setItem('tgat1_studio_vocab_progress_v1',JSON.stringify({items:{ability:{status:'known',reps:2,interval:2,due:Date.now()+1e8,last:Date.now()}},favorites:['ability'],sessions:[]}))")
        await page.reload(); await page.wait_for_timeout(1200)
        async with page.expect_download() as dl:
            await page.evaluate("studioExportAll()")
        d = await dl.value
        path = await d.path()
        payload = json.loads(Path(path).read_text(encoding='utf-8'))
        blob = json.dumps(payload, ensure_ascii=False)
        check('export: backup JSON is produced with app id, version, timestamp and the vocabulary progress', payload.get('app') and payload.get('version') and payload.get('exportedAt') and 'tgat1_studio_vocab_progress_v1' in blob and 'ability' in blob and payload.get('integrity'), str(list(payload.keys())))
        await page.evaluate("localStorage.removeItem('tgat1_studio_vocab_progress_v1')")
        await page.evaluate("studioNav('settings')"); await page.wait_for_timeout(500)
        await page.evaluate("""(()=>{const i=document.createElement('input');i.type='file';i.id='qaImport';i.onchange=()=>studioImportAll(i);document.body.appendChild(i)})()""")
        await page.set_input_files('#qaImport', path); await page.wait_for_timeout(600)
        await page.click('#studioModal .st-btn:not(.secondary)'); await page.wait_for_timeout(1500)
        restored = await page.evaluate("(()=>{const v=JSON.parse(localStorage.getItem('tgat1_studio_vocab_progress_v1')||'null');return !!(v&&v.items&&v.items.ability&&v.favorites.includes('ability'))})()")
        check('import: backup restores vocabulary progress after confirmation', restored)
        check('no JavaScript errors in export/import', not [e for e in errs if 'download' not in e.lower()], '; '.join(errs[:3]))
        await ctx.close()

        # 8) routes @390/1280: errors + overflow, incl. Vocabulary Lab and word detail
        for width in (1280, 390):
            ctx, page, errs = await page_for(browser, url, width)
            over = {}
            for name in PAGES:
                await page.evaluate(f"studioNav('{name}')"); await page.wait_for_timeout(900)
                over[name] = await page.evaluate("document.documentElement.scrollWidth-window.innerWidth")
            await page.evaluate("TGAT1VocabularyLab.start('mixed')"); await page.wait_for_timeout(1800)
            over['vocabLab'] = await page.evaluate("document.documentElement.scrollWidth-window.innerWidth")
            await page.evaluate("TGAT1VocabularyLab.exit()"); await page.wait_for_timeout(300)
            await page.evaluate("studioWordDetail(STUDIO_DATA.words.findIndex(w=>w.w==='historic'))"); await page.wait_for_timeout(900)
            over['detail'] = await page.evaluate("document.documentElement.scrollWidth-window.innerWidth")
            check(f'layout @{width}px: no horizontal overflow on 9 routes + Vocabulary Lab + word detail', all(x <= 2 for x in over.values()), str({k: x for k, x in over.items() if x > 2}))
            check(f'no console/page errors @{width}px', not errs, '; '.join(errs[:3]))
            await ctx.close()

        # 9) keyboard + focus
        ctx, page, errs = await page_for(browser, url)
        await page.keyboard.press('Tab')
        first = await page.evaluate("(()=>{const a=document.activeElement;return {cls:a.className,text:a.textContent.trim().slice(0,30)}})()")
        check('keyboard: first Tab reaches the "skip to content" link', 'skip-to-content' in first['cls'], str(first))
        await page.keyboard.press('Enter'); await page.wait_for_timeout(200)
        check('keyboard: skip link moves focus to main content', await page.evaluate("document.activeElement&&document.activeElement.id==='app'"))
        vis = []
        for _ in range(12):
            await page.keyboard.press('Tab'); await page.wait_for_timeout(40)
            vis.append(await page.evaluate("(()=>{const a=document.activeElement;if(!a||a===document.body)return null;const cs=getComputedStyle(a);return (cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0)||cs.boxShadow!=='none'})()"))
        vis = [x for x in vis if x is not None]
        check('keyboard: focused controls show a visible focus indicator', vis and all(vis), f'{sum(1 for x in vis if x)}/{len(vis)}')
        await page.evaluate("TGAT1VocabularyLab.start('mixed')"); await page.wait_for_timeout(1500)
        await page.focus('#app [onclick^="TGAT1VocabularyLab.answer"]'); await page.keyboard.press('Enter'); await page.wait_for_timeout(200)
        check('keyboard: a Vocabulary Lab option can be answered with Enter', await page.evaluate("!!document.querySelector('#app .st-alert')"))
        await ctx.close()

        # 10) offline / PWA with the new cache
        ctx = await browser.new_context(service_workers='allow'); page = await ctx.new_page()
        await page.goto(url); await page.wait_for_timeout(6000)
        keys = await page.evaluate("caches.keys()")
        cached = await page.evaluate(f"(async()=>{{const c=await caches.open('tgat1-studio-v{EXPECT_VERSION}');const k=(await c.keys()).map(r=>new URL(r.url).pathname.split('/').pop());return k}})()")
        check('PWA: v42 cache installed with app shell + data-senses + data-vault', f'tgat1-studio-v{EXPECT_VERSION}' in keys and all(f in cached for f in ['app.js', 'data.js', 'data-senses.js', 'data-vault.js', 'learning-hub.js']), str(keys))
        await ctx.set_offline(True); await page.reload(); await page.wait_for_timeout(2500)
        await page.evaluate("studioNav('vocab')"); await page.wait_for_timeout(600)
        await page.evaluate("studioWordDetail(STUDIO_DATA.words.findIndex(w=>w.w==='annually'))"); await page.wait_for_timeout(1500)
        off = await page.evaluate("(document.querySelector('#studioModal')||{}).innerText||''")
        check('offline: word detail with lazy senses opens and shows corrected gloss', 'ทุกปี' in off and 'การเปลี่ยนแปลงเกิดขึ้น' not in off, off[:100].replace('\n', ' '))
        await ctx.close()

        # 11) axe-core scan (report; fail only on critical)
        if AXE and Path(AXE).exists():
            axe_src = Path(AXE).read_text(encoding='utf-8')
            summary = {}
            for width, theme in ((1280, 'light'), (390, 'light'), (390, 'dark')):
                ctx, page, errs = await page_for(browser, url, width)
                if theme == 'dark':
                    await page.evaluate("studioTheme('dark')"); await page.wait_for_timeout(400)
                for name in PAGES + ['vocabLab']:
                    if name == 'vocabLab':
                        await page.evaluate("TGAT1VocabularyLab.start('mixed')"); await page.wait_for_timeout(1500)
                    else:
                        await page.evaluate(f"studioNav('{name}')"); await page.wait_for_timeout(900)
                    await page.evaluate(axe_src)
                    r = await page.evaluate("axe.run(document,{resultTypes:['violations']}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length})))")
                    for v in r:
                        k = (v['id'], v['impact'])
                        summary[k] = summary.get(k, 0) + v['n']
                await ctx.close()
            crit = {k: n for k, n in summary.items() if k[1] in ('critical', 'serious')}
            for (rid, imp), n in sorted(summary.items(), key=lambda x: (x[0][1] != 'critical', x[0][1] != 'serious', -x[1])):
                note(f'axe {imp}: {rid} × {n} nodes (9 routes + lab; 1280 light, 390 light, 390 dark)')
            check('a11y (axe-core): no critical/serious violations on 9 routes + Vocabulary Lab (1280 light, 390 light, 390 dark)', not crit, str(crit))
        else:
            note('axe-core not provided (set AXE_PATH) — automated a11y scan skipped')
        await browser.close()
    httpd.shutdown()
    failed = [r for r in results if not r[1]]
    stamp = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    print(f'\n{len(results) - len(failed)}/{len(results)} checks passed · {stamp}')
    sys.exit(1 if failed else 0)

asyncio.run(main())
