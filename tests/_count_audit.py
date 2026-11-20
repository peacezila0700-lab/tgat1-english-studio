#!/usr/bin/env python3
"""Investigate word count discrepancy and mock answer flow."""
import asyncio, os
from playwright.async_api import async_playwright

BASE = "http://localhost:8765/"
CHROME = os.environ["CHROME"]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox","--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width":390,"height":844}, user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36")

        # 1. Check actual counts in browser
        print("=== COUNT CHECK ===")
        counts = await page.evaluate("""() => {
            const d = window.STUDIO_DATA || {};
            return {
                words_length: (d.words||[]).length,
                phrases_length: (d.phrases||[]).length,
                items_length: (d.items||[]).length,
                examples_length: (d.examples||[]).length,
                bank_length: (window.VLT_BANK||[]).length,
                vocab_total_dom: document.querySelector('[class*=v15-kpi] b')?.textContent
            };
        }""")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        counts = await page.evaluate("""() => {
            const d = window.STUDIO_DATA || {};
            return {
                words_length: (d.words||[]).length,
                phrases_length: (d.phrases||[]).length,
                items_length: (d.items||[]).length,
                bank_length: (window.VLT_BANK||[]).length
            };
        }""")
        print(f"STUDIO_DATA.words.length = {counts.get('words_length')}")
        print(f"STUDIO_DATA.phrases.length = {counts.get('phrases_length')}")
        print(f"STUDIO_DATA.items.length = {counts.get('items_length')}")
        print(f"VLT_BANK.length = {counts.get('bank_length')}")

        # 2. Home displayed number
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        home_text = await page.evaluate("document.querySelector('#app').innerText")
        import re
        m = re.findall(r'/[\d,]+ คำ', home_text)
        print(f"Home 'คำ' count display: {m}")

        # 3. Vocab page numbers
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        vocab_text = await page.evaluate("document.querySelector('#app').innerText")
        vm = re.findall(r'([\d,]+)\s*(?:ถึงกำหนดทบทวน|ทำเครื่องหมายว่าจำได้|ยังไม่เคยประเมิน)', vocab_text)
        print(f"Vocab KPIs: {vm}")

        # 4. Mock answer flow - inspect button structure
        print("\n=== MOCK ANSWER BUTTON INSPECTION ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"exam\"]')?.click()")
        await page.wait_for_timeout(1200)
        await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const mock = btns.find(b => /เริ่มชุด|จำลอง/i.test(b.textContent));
            if (mock) mock.click();
        }""")
        await page.wait_for_timeout(2000)
        btns = await page.evaluate("""() => [...document.querySelectorAll('button')].slice(0,25).map(b => ({
            text: b.textContent.trim().slice(0,40),
            action: b.getAttribute('data-action')||'',
            cls: b.className.slice(0,40)
        }))""")
        for b in btns:
            print(f"  btn: '{b['text']}' action={b['action']} class={b['cls']}")

        await browser.close()

asyncio.run(main())
