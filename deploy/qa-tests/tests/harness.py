"""Shared Playwright harness for TGAT1 English Studio QA (written in round 3, v42.0.2 work)."""
import os, sys, json, subprocess, time, socket, contextlib
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXE=os.path.join(ROOT,'tools','node_modules','axe-core','axe.min.js')
CHROME=os.environ.get('CHROME') or '/usr/bin/google-chrome'
PAGES=['home','hub','profile','vocab','exam','reading','game','analytics','settings']
DESKTOP={'width':1366,'height':900}
MOBILE={'width':390,'height':844}
SMALL={'width':320,'height':640}

def free_port():
    with contextlib.closing(socket.socket()) as s:
        s.bind(('127.0.0.1',0));return s.getsockname()[1]

@contextlib.contextmanager
def server(webdir):
    port=free_port()
    p=subprocess.Popen([sys.executable,'-m','http.server',str(port),'--bind','127.0.0.1'],cwd=webdir,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            socket.create_connection(('127.0.0.1',port),timeout=0.2).close();break
        except OSError: time.sleep(0.1)
    try: yield f'http://127.0.0.1:{port}'
    finally: p.terminate();p.wait()

@contextlib.contextmanager
def browser():
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=CHROME,args=['--no-sandbox'])
        try: yield b
        finally: b.close()

def new_page(b,base,viewport=DESKTOP,theme='light',color_scheme=None,storage=None):
    ctx=b.new_context(viewport=viewport,color_scheme=color_scheme or theme,service_workers='block',reduced_motion='reduce')
    pg=ctx.new_page();pg.errs=[]
    pg.on('pageerror',lambda e:pg.errs.append('pageerror: '+str(e)))
    pg.on('console',lambda m:m.type=='error' and pg.errs.append('console: '+m.text))
    pg.goto(base+'/index.html');pg.wait_for_function("typeof studioNav==='function' && !document.querySelector('.boot-splash') && !!window.__TGAT1_DATA_EXTRA && !!window.__TGAT1_V382_READY__",timeout=20000)
    if theme=='dark': pg.evaluate("studioTheme('dark')")
    return pg

def nav(pg,page):
    pg.evaluate(f"studioNav('{page}')");pg.wait_for_timeout(350)

def run_axe(pg,include='body'):
    if not pg.evaluate("!!window.axe"):
        axe_src=open(AXE).read()
        pg.route('**/axe.min.js',lambda route:route.fulfill(status=200,content_type='application/javascript',body=axe_src))
        pg.add_script_tag(url='/axe.min.js')
    return pg.evaluate("""async (inc)=>{const r=await axe.run(document.querySelector(inc)||document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']},resultTypes:['violations','incomplete']});
      const m=v=>({id:v.id,impact:v.impact,help:v.help,nodes:v.nodes.slice(0,8).map(n=>({t:n.target.join(' '),s:(n.failureSummary||'').slice(0,240),h:n.html.slice(0,160)})),n:v.nodes.length});
      return {violations:r.violations.map(m),incomplete:r.incomplete.filter(v=>v.id==='color-contrast').map(m)}}""",include)
