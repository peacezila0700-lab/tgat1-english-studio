#!/usr/bin/env python3
"""Verify: home count after lazy load + real mock answer click + exam flows."""
import asyncio, os, re
from playwright.async_api import async_playwright

BASE = "http://localhost:8765/"
CHROME = os.environ["CHROME"]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox","--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width":390,"height":844}, user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36")

        # 1. Home count: before and after waiting for lazy extra load
        print("=== HOME COUNT TIMELINE ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        t1 = await page.evaluate("document.querySelector('#app').innerText")
        m1 = re.findall(r'/[\d,]+ คำ', t1)
        w1 = await page.evaluate("window.STUDIO_DATA.words.length")
        print(f"  t+0.8s: display={m1} actual={w1}")

        await page.wait_for_timeout(3000)
        t2 = await page.evaluate("document.querySelector('#app').innerText")
        m2 = re.findall(r'/[\d,]+ คำ', t2)
        w2 = await page.evaluate("window.STUDIO_DATA.words.length")
        print(f"  t+3.8s: display={m2} actual={w2}")

        # 2. Real mock answer click
        print("\n=== MOCK ANSWER FLOW ===")
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
        # click first VLT_answer option
        clicked = await page.evaluate("""() => {
            const opt = document.querySelector('button[data-action="VLT_answer"]');
            if (opt) { opt.click(); return opt.textContent.trim().slice(0,30); }
            return null;
        }""")
        print(f"  clicked option: {clicked}")
        await page.wait_for_timeout(1500)
        answered = await page.evaluate("document.querySelector('#app').innerText.match(/ตอบแล้ว [\\d/]+/)?.[0] || 'N/A'")
        print(f"  answered count: {answered}")

        # 3. Go to next question
        await page.evaluate("document.querySelector('button[data-action=\"VLT_next\"]')?.click()")
        await page.wait_for_timeout(1200)
        q2 = await page.evaluate("document.querySelector('#app').innerText.slice(0,200)")
        print(f"  Q2 text: {q2[:120]}")

        # 4. Flag + favorite buttons
        await page.evaluate("document.querySelector('button[data-action=\"VLT_toggleFlagV12\"]')?.click()")
        await page.wait_for_timeout(500)
        await page.evaluate("document.querySelector('button[data-action=\"VLT_toggleFavorite\"]')?.click()")
        await page.wait_for_timeout(500)
        flags = await page.evaluate("document.querySelector('#app').innerText.match(/ติดธง [\\d]+/)?.[0] || 'N/A'")
        print(f"  flags: {flags}")

        # 5. Check finish flow — submit all
        print("\n=== FINISH FLOW ===")
        # answer remaining quickly via JS
        await page.evaluate("""async () => {
            for (let i = 0; i < 20; i++) {
                const opt = document.querySelector('button[data-action="VLT_answer"]');
                if (!opt) break;
                opt.click();
                await new Promise(r => setTimeout(r, 100));
                const next = document.querySelector('button[data-action="VLT_next"]');
                if (next && !next.disabled) next.click();
                await new Promise(r => setTimeout(r, 150));
            }
        }""")
        await page.wait_for_timeout(2000)
        tail = await page.evaluate("document.querySelector('#app').innerText.slice(0,300)")
        print(f"  after answering: {tail[:150]}")

        await browser.close()

asyncio.run(main())
