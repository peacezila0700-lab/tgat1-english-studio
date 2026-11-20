#!/usr/bin/env python3
"""Final checks: vocab search, dark mode, word list render, phrase practice."""
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

        # === Vocab search ===
        log("\n=== VOCAB SEARCH ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        # count word cards before search
        before = await page.evaluate("document.querySelectorAll('.pk-card, [class*=vocab-item], [class*=word-card]').length")
        log(f"  word cards before search: {before}")
        # type "hello"
        await page.evaluate("""() => {
            const inp = document.getElementById('studioVSearch');
            inp.value = 'hello';
            inp.dispatchEvent(new Event('input', {bubbles:true}));
        }""")
        await page.wait_for_timeout(1000)
        after = await page.evaluate("document.querySelectorAll('.pk-card, [class*=vocab-item], [class*=word-card]').length")
        text_after = await page.evaluate("document.querySelector('#app').innerText")
        has_hello = "hello" in text_after.lower()
        log(f"  word cards after 'hello' search: {after}, contains hello: {has_hello}")
        # search nonsense
        await page.evaluate("""() => {
            const inp = document.getElementById('studioVSearch');
            inp.value = 'zzzzqqqq';
            inp.dispatchEvent(new Event('input', {bubbles:true}));
        }""")
        await page.wait_for_timeout(1000)
        none_text = await page.evaluate("document.querySelector('#app').innerText")
        has_empty = "ไม่พบ\|ไม่มี\|ไม่เจอ\|no result\|0 คำ" in none_text.lower() or "ไม่พบ" in none_text
        log(f"  nonsense search shows empty state: {has_empty}")
        log(f"  nonsense search text snippet: {none_text[:200].replace(chr(10),' | ')}")

        # === Dark mode ===
        log("\n=== DARK MODE ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        theme_before = await page.evaluate("document.documentElement.getAttribute('data-theme') || 'light'")
        log(f"  theme before: {theme_before}")
        # go to settings, pick dark
        await page.evaluate("document.querySelector('[data-page=\"settings\"]')?.click()")
        await page.wait_for_timeout(1200)
        # find theme select
        sel = await page.evaluate("""() => {
            const el = document.querySelector('select');
            if (el) { el.value = 'dark'; el.dispatchEvent(new Event('change', {bubbles:true})); return 'select set dark'; }
            return 'NO SELECT';
        }""")
        log(f"  theme selector: {sel}")
        await page.wait_for_timeout(1000)
        theme_after = await page.evaluate("document.documentElement.getAttribute('data-theme') || 'light'")
        log(f"  theme after: {theme_after}")
        await page.screenshot(path="/home/user/google_drive/project_claude/qa/deep_audit/dark_home.png")
        # check bg color is dark
        bg = await page.evaluate("getComputedStyle(document.body).backgroundColor")
        log(f"  body bg: {bg}")

        # === Phrase practice ===
        log("\n=== PHRASE PRACTICE ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const pp = btns.find(b => /phrase|สำนวน|Phrase/i.test(b.getAttribute('data-action')||'') || /ฝึก 10 ข้อ/.test(b.textContent));
            if (pp) { pp.click(); return pp.getAttribute('data-action')+' :: '+pp.textContent.trim().slice(0,30); }
            return 'NOT FOUND';
        }""")
        log(f"  phrase practice: {clicked}")
        await page.wait_for_timeout(2000)
        pp_view = await page.evaluate("document.querySelector('#app').innerText.slice(0,400)")
        log(f"  phrase view: {pp_view[:200].replace(chr(10),' | ')}")

        await browser.close()

asyncio.run(main())
