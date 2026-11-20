#!/usr/bin/env python3
"""Phrase practice test with bank preloaded."""
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

        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        # wait for bank to load
        for i in range(20):
            bank_len = await page.evaluate("window.VLT_BANK ? window.VLT_BANK.length : 0")
            if bank_len > 0:
                log(f"VLT_BANK loaded: {bank_len} items (waited {i*0.5}s)")
                break
            await page.wait_for_timeout(500)
        else:
            log("VLT_BANK NOT loaded after 10s — forcing load")
            await page.evaluate("window.VLT_ensureBank && window.VLT_ensureBank()")
            await page.wait_for_timeout(2000)
            bank_len = await page.evaluate("window.VLT_BANK ? window.VLT_BANK.length : 0")
            log(f"VLT_BANK after force: {bank_len}")

        # now go to vocab and try phrase practice
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const pp = btns.find(b => /studioStartPhrasePractice/.test(b.getAttribute('data-action')||''));
            if (pp) { pp.click(); return pp.textContent.trim().slice(0,30); }
            return 'NOT FOUND';
        }""")
        log(f"phrase start clicked: {clicked}")
        await page.wait_for_timeout(2000)
        modal = await page.evaluate("document.querySelector('#studioModal, .pk-modal, [role=dialog]')?.innerText?.slice(0,500) || 'NO MODAL'")
        app_view = await page.evaluate("document.querySelector('#app').innerText.slice(0,300)")
        log(f"modal: {modal[:200].replace(chr(10),' | ')}")
        log(f"app view: {app_view[:200].replace(chr(10),' | ')}")

        await browser.close()

asyncio.run(main())
