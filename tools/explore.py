import sys,json
from playwright.sync_api import sync_playwright
base=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1366,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(base+'/index.html');pg.wait_for_timeout(1500)
    for page in ['home','hub','profile','vocab','exam','reading','game','analytics','settings']:
        pg.evaluate(f"studioNav('{page}')");pg.wait_for_timeout(600)
        btns=pg.evaluate("""[...document.querySelectorAll('#app [onclick]')].map(b=>(b.getAttribute('onclick')||'').slice(0,90)+' | '+(b.innerText||'').replace(/\\s+/g,' ').slice(0,40))""")
        print('=====',page,len(btns))
        seen=set()
        for x in btns:
            k=x.split('(')[0]
            if k in seen: continue
            seen.add(k);print('  ',x)
    print('ERRORS',errs)
    b.close()
