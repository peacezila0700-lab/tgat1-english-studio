#!/usr/bin/env python3
"""Targeted checks: flashcards flow, export button, game modes."""
import asyncio, os
from playwright.async_api import async_playwright

BASE = "http://localhost:8765/"
CHROME = os.environ["CHROME"]

def log(msg):
    print(msg, flush=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox","--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width":390,"height":844}, user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36")

        # === Flashcards: click the actual flashcard start button ===
        log("\n=== FLASHCARDS ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        # list all buttons with actions
        btns = await page.evaluate("""() => [...document.querySelectorAll('button[data-action]')].map(b => b.getAttribute('data-action')+' :: '+b.textContent.trim().slice(0,35))""")
        for b in btns[:25]:
            log(f"  {b}")
        # find flashcard start (V15_startNew / flashcards action)
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const fc = btns.find(b => /startFlash|flash|V15_startNew|V15_startDue/i.test(b.getAttribute('data-action')||''));
            if (fc) { fc.click(); return fc.getAttribute('data-action')+' :: '+fc.textContent.trim().slice(0,30); }
            return 'NOT FOUND';
        }""")
        log(f"flashcard action: {clicked}")
        await page.wait_for_timeout(2000)
        fc_view = await page.evaluate("document.querySelector('#app').innerText.slice(0,300)")
        log(f"flashcard view: {fc_view[:150].replace(chr(10),' | ')}")

        # === Settings export: find actual export button ===
        log("\n=== SETTINGS EXPORT ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"settings\"]')?.click()")
        await page.wait_for_timeout(1500)
        btns2 = await page.evaluate("""() => [...document.querySelectorAll('button[data-action]')].map(b => b.getAttribute('data-action')+' :: '+b.textContent.trim().slice(0,35))""")
        for b in btns2[:25]:
            log(f"  {b}")
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const ex = btns.find(b => /exportAll|export|backup|TGAT1Safety/i.test(b.getAttribute('data-action')||''));
            if (ex) { ex.click(); return ex.getAttribute('data-action')+' :: '+ex.textContent.trim().slice(0,30); }
            return 'NOT FOUND';
        }""")
        log(f"export action: {clicked}")
        await page.wait_for_timeout(2000)
        export_view = await page.evaluate("document.querySelector('#app').innerText.slice(0,400)")
        log(f"after export: {export_view[:200].replace(chr(10),' | ')}")

        # === Game modes ===
        log("\n=== GAME MODES ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"game\"]')?.click()")
        await page.wait_for_timeout(1500)
        # Quick Play
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const qp = btns.find(b => /quickPlay|startQuick|สุ่ม|Quick Play/i.test(b.getAttribute('data-action')||'')||/สุ่ม/.test(b.textContent));
            if (qp) { qp.click(); return qp.getAttribute('data-action')+' :: '+qp.textContent.trim().slice(0,30); }
            return 'NOT FOUND';
        }""")
        log(f"quick play: {clicked}")
        await page.wait_for_timeout(2000)
        gp_view = await page.evaluate("document.querySelector('#app').innerText.slice(0,300)")
        log(f"game view: {gp_view[:150].replace(chr(10),' | ')}")

        await browser.close()

asyncio.run(main())
