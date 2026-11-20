#!/usr/bin/env python3
"""Verify 3 fixes: cannot-answer button, progress ring, multiple examples."""
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

        # === Fix 1: Cannot-answer button ===
        log("\n=== FIX 1: Cannot-answer button ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        # wait bank
        for i in range(15):
            bl = await page.evaluate("window.VLT_BANK ? window.VLT_BANK.length : 0")
            if bl > 0: break
            await page.wait_for_timeout(500)
        await page.evaluate("document.querySelector('[data-page=\"exam\"]')?.click()")
        await page.wait_for_timeout(1200)
        await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const mock = btns.find(b => /เริ่มชุด|จำลอง/i.test(b.textContent));
            if (mock) mock.click();
        }""")
        await page.wait_for_timeout(2000)
        # check for skip button (not flag)
        has_skip = await page.evaluate("!!document.querySelector('button[data-action=\"VLT_skipAnswer\"]')")
        has_flag = await page.evaluate("!!document.querySelector('button[data-action=\"VLT_toggleFlagV12\"]')")
        log(f"  skip button present: {has_skip}")
        log(f"  flag button present: {has_flag}")
        # click skip
        skip_text = await page.evaluate("""() => {
            const b = document.querySelector('button[data-action=\"VLT_skipAnswer\"]');
            if (b) { b.click(); return b.textContent.trim(); }
            return null;
        }""")
        log(f"  skip button text: {skip_text}")
        await page.wait_for_timeout(1000)
        skip_after = await page.evaluate("document.querySelector('button[data-action=\"VLT_skipAnswer\"]')?.textContent?.trim() || 'GONE'")
        log(f"  skip button after click: {skip_after}")

        # === Fix 2: Progress ring on home ===
        log("\n=== FIX 2: Progress ring on home ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        has_ring = await page.evaluate("!!document.querySelector('#app svg[viewBox]') || document.querySelector('#app .ring-wrap')")
        log(f"  ring SVG present: {has_ring}")
        ring_text = await page.evaluate("document.querySelector('#app .pk-k-label')?.closest('.pk-kpi')?.textContent?.slice(0,60) || 'N/A'")
        log(f"  ring KPI text: {ring_text}")
        await page.screenshot(path="/home/user/google_drive/project_claude/qa/deep_audit/home_ring.png")

        # === Fix 3: Multiple examples in word detail ===
        log("\n=== FIX 3: Multiple examples ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        await page.evaluate("""() => {
            const inp = document.getElementById('studioVSearch') || document.querySelector('input[type=text], input[type=search]');
            if (inp) { inp.value = 'account'; inp.dispatchEvent(new Event('input', {bubbles:true})); }
        }""")
        await page.wait_for_timeout(1000)
        clicked = await page.evaluate("""() => {
            const cards = [...document.querySelectorAll('button, .pk-card')].filter(e => /account/i.test(e.textContent));
            if (cards[0]) { cards[0].click(); return cards[0].textContent.slice(0,30); }
            return null;
        }""")
        log(f"  word clicked: {clicked}")
        await page.wait_for_timeout(1500)
        modal = await page.evaluate("document.querySelector('#studioModal, .pk-modal')?.innerText?.slice(0,800) || 'NO MODAL'")
        # count example sentences (numbered)
        ex_count = modal.count("1.") + modal.count("2.") + modal.count("3.") + modal.count("4.")
        log(f"  modal has examples: {ex_count > 0}")
        log(f"  modal snippet: {modal[:300].replace(chr(10),' | ')}")

        await browser.close()

asyncio.run(main())
