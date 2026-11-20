#!/usr/bin/env python3
"""Verify multiple examples in word detail — isolated test."""
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

        # Fresh context — no running session
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        # search a word that likely has multiple senses
        await page.evaluate("""() => {
            const inp = document.getElementById('studioVSearch');
            inp.value = 'run';
            inp.dispatchEvent(new Event('input', {bubbles:true}));
        }""")
        await page.wait_for_timeout(1000)
        # click first word card via studioWordDetail
        clicked = await page.evaluate("""() => {
            const cards = [...document.querySelectorAll('button[data-action="studioWordDetail"]')];
            if (cards[0]) { cards[0].click(); return cards[0].textContent.slice(0,30); }
            return 'NO CARD';
        }""")
        log(f"  word clicked: {clicked}")
        await page.wait_for_timeout(2000)
        modal = await page.evaluate("document.querySelector('#studioModal, .pk-modal, [role=dialog]')?.innerText?.slice(0,1200) || 'NO MODAL'")
        # count numbered examples
        import re
        nums = re.findall(r'^\s*[1-4]\.', modal, re.M)
        log(f"  numbered examples found: {len(nums)}")
        log(f"  modal snippet: {modal[:400].replace(chr(10),' | ')}")
        await page.screenshot(path="/home/user/google_drive/project_claude/qa/deep_audit/word_examples.png")

        await browser.close()

asyncio.run(main())
