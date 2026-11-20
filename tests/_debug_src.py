import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
with server('web') as base, browser() as b:
    pg = new_page(b, base)
    pg.goto(base, wait_until='networkidle')
    pg.evaluate("async()=>{await VLT_ensureBank();return VLT_BANK.length}")
    pg.wait_for_timeout(1000)
    pg.evaluate("""()=>{
      const r = VLT_BANK.filter(q => q.source)[0];
      VLT_begin({mode:'tgat',label:'test',qs:[{...r,userAnswer:null}],index:0,answers:{},score:0,combo:0,reviewOn:true});
    }""")
    pg.wait_for_timeout(500)
    pg.evaluate("""()=>{
      const wrong = [0,1,2,3].filter(i => i !== VLT_RUN.qs[0].answer);
      window.ans(wrong[0]);
    }""")
    pg.wait_for_timeout(500)
    # Find the ดูผล button and click with real Playwright
    btns = pg.locator("button").all()
    clicked = False
    for btn in btns:
        txt = btn.inner_text()
        if "ดูผล" in txt:
            btn.click()
            clicked = True
            break
    print("clicked:", clicked)
    pg.wait_for_timeout(1000)
    txt = pg.evaluate("()=>document.body.innerText.slice(0,3000)")
    print("BODY:", txt)
    print("HAS SOURCE:", pg.evaluate("()=>document.body.innerText.includes('แหล่งที่มา')"))
    pg.context.close()
