#!/usr/bin/env python3
"""Deep audit: remaining features - flashcards, phrases, grammar, reading, hub, export."""
import asyncio, os, re
from playwright.async_api import async_playwright

BASE = "http://localhost:8765/"
CHROME = os.environ["CHROME"]

ISSUES = []
def log(msg):
    print(msg, flush=True)
    ISSUES.append(msg)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox","--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width":390,"height":844}, user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36")

        # === VOCAB: flashcards ===
        log("\n=== VOCAB FLASHCARDS ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        # find flashcard button
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const fc = btns.find(b => /flash|flashcard|การ์ด|ทวน/i.test(b.textContent));
            if (fc) { fc.click(); return fc.textContent.trim().slice(0,40); }
            return null;
        }""")
        log(f"flashcard clicked: {clicked}")
        await page.wait_for_timeout(1500)
        fc_text = await page.evaluate("document.querySelector('#app').innerText.slice(0,400)")
        log(f"flashcard view: {fc_text[:200].replace(chr(10),' | ')}")

        # === VOCAB: word detail ===
        log("\n=== VOCAB WORD DETAIL ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        # search a word and open detail
        await page.evaluate("""() => {
            const inp = document.getElementById('studioVSearch');
            if (inp) { inp.value = 'hello'; inp.dispatchEvent(new Event('input', {bubbles:true})); }
        }""")
        await page.wait_for_timeout(1000)
        detail = await page.evaluate("""() => {
            const btn = document.querySelector('[data-action="TGAT1VocabularyLab.openTerm"], [class*=word-card], [data-action*=Word], [class*=vocab-item]');
            if (btn) { btn.click(); return btn.textContent.slice(0,30); }
            // try first word card
            const cards = [...document.querySelectorAll('button, .pk-card')].filter(e => e.textContent.trim().length>0 && e.textContent.trim().length<60);
            if (cards[2]) { cards[2].click(); return cards[2].textContent.slice(0,30); }
            return null;
        }""")
        log(f"word detail clicked: {detail}")
        await page.wait_for_timeout(1500)
        # check modal
        modal = await page.evaluate("document.querySelector('#studioModal, .pk-modal, [role=dialog]')?.innerText?.slice(0,300) || 'NO MODAL'")
        log(f"modal: {modal[:150].replace(chr(10),' | ')}")

        # === READING TRAINER ===
        log("\n=== READING TRAINER ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"more\"], [data-action=\"studioMobileMore\"]')?.click()")
        await page.wait_for_timeout(500)
        await page.evaluate("document.querySelector('[data-page=\"reading\"]')?.click()")
        await page.wait_for_timeout(1500)
        rt_text = await page.evaluate("document.querySelector('#app').innerText.slice(0,400)")
        log(f"reading trainer: {rt_text[:200].replace(chr(10),' | ')}")

        # === HUB unit learning ===
        log("\n=== HUB UNIT LEARN ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"hub\"]')?.click()")
        await page.wait_for_timeout(2000)
        # click continue learning
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const cont = btns.find(b => /เรียนต่อ|continue|ถัดไป|next/i.test(b.textContent));
            if (cont) { cont.click(); return cont.textContent.trim().slice(0,30); }
            return null;
        }""")
        log(f"hub continue: {clicked}")
        await page.wait_for_timeout(2000)
        hub_learn = await page.evaluate("document.querySelector('#app').innerText.slice(0,500)")
        log(f"hub learn view: {hub_learn[:250].replace(chr(10),' | ')}")

        # === SETTINGS: export ===
        log("\n=== SETTINGS EXPORT ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"settings\"]')?.click()")
        await page.wait_for_timeout(1500)
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const ex = btns.find(b => /ส่งออก|export|สำรอง/i.test(b.textContent));
            if (ex) { ex.click(); return ex.textContent.trim().slice(0,30); }
            return null;
        }""")
        log(f"export clicked: {clicked}")
        await page.wait_for_timeout(1500)
        export_text = await page.evaluate("document.querySelector('#app').innerText.slice(0,500)")
        log(f"after export: {export_text[:200].replace(chr(10),' | ')}")

        # === PROFILE: save ===
        log("\n=== PROFILE SAVE ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"profile\"]')?.click()")
        await page.wait_for_timeout(1500)
        # fill name
        await page.evaluate("document.getElementById('pname') && (document.getElementById('pname').value='TestUser', document.getElementById('pname').dispatchEvent(new Event('input',{bubbles:true})))")
        # click save
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const save = btns.find(b => /บันทึก|save/i.test(b.textContent));
            if (save) { save.click(); return save.textContent.trim().slice(0,30); }
            return null;
        }""")
        log(f"profile save clicked: {clicked}")
        await page.wait_for_timeout(1000)

        # === Check toast appears ===
        toast = await page.evaluate("document.querySelector('.toast, [class*=toast]')?.textContent?.slice(0,80) || 'NO TOAST'")
        log(f"toast: {toast}")

        await browser.close()
        with open("/home/user/google_drive/project_claude/qa/deep_audit/FEATURE_REPORT.txt","w") as f:
            f.write("\n".join(ISSUES))
        log(f"\n=== FEATURE AUDIT DONE ===")

asyncio.run(main())
