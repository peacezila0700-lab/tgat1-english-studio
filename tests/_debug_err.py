import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import *
with server('web') as base, browser() as b:
    pg = new_page(b, base)
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(base, wait_until='networkidle')
    pg.wait_for_timeout(2000)
    for e in errors:
        print("PAGEERROR:", e[:500])
    # Check if app.js loaded
    loaded = pg.evaluate("()=>typeof VLT_BANK")
    print("VLT_BANK type:", loaded)
    loaded2 = pg.evaluate("()=>typeof TGAT1_showReviewSummary")
    print("TGAT1_showReviewSummary type:", loaded2)
    loaded3 = pg.evaluate("()=>typeof TGAT1Hub")
    print("TGAT1Hub type:", loaded3)
    pg.context.close()
