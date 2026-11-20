#!/usr/bin/env python3
"""Verify phrase practice actually starts + vocab word list structure."""
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

        # === Phrase practice deep check ===
        log("\n=== PHRASE PRACTICE DEEP ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        # click phrase practice tab first
        await page.evaluate("""() => {
            const tabs = [...document.querySelectorAll('button[data-action="studioVTab"]')];
            const pt = tabs.find(b => /phrase|สำนวน|Phrase/i.test(b.textContent));
            if (pt) pt.click();
        }""")
        await page.wait_for_timeout(1000)
        # now click start phrase practice
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const pp = btns.find(b => /studioStartPhrasePractice|เริ่มฝึก 10 ข้อ/i.test(b.getAttribute('data-action')||'')||/เริ่มฝึก 10 ข้อ/.test(b.textContent));
            if (pp) { pp.click(); return pp.getAttribute('data-action')+' :: '+pp.textContent.trim().slice(0,30); }
            return 'NOT FOUND';
        }""")
        log(f"phrase start: {clicked}")
        await page.wait_for_timeout(2500)
        # check modal or view change
        modal = await page.evaluate("document.querySelector('#studioModal, .pk-modal, [role=dialog]')?.innerText?.slice(0,400) || 'NO MODAL'")
        app_view = await page.evaluate("document.querySelector('#app').innerText.slice(0,300)")
        log(f"modal: {modal[:150].replace(chr(10),' | ')}")
        log(f"app view: {app_view[:150].replace(chr(10),' | ')}")
        # check if a quiz/practice started
        has_quiz = await page.evaluate("!!document.querySelector('[class*=quiz], [class*=practice], [data-action*=answer], [class*=sentence]')")
        log(f"practice elements found: {has_quiz}")

        # === Vocab word list structure ===
        log("\n=== VOCAB WORD LIST STRUCTURE ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.evaluate("document.querySelector('[data-page=\"vocab\"]')?.click()")
        await page.wait_for_timeout(1500)
        # scroll to find word cards
        await page.evaluate("window.scrollBy(0, 600)")
        await page.wait_for_timeout(500)
        # check for word items with English words
        word_items = await page.evaluate("""() => {
            // look for elements that look like word entries
            const all = [...document.querySelectorAll('div, button, li, span')];
            const wordEls = all.filter(e => {
                const t = e.textContent.trim();
                return t.length > 0 && t.length < 80 && /^[a-zA-Z]/.test(t) && e.children.length < 5;
            }).slice(0, 15);
            return wordEls.map(e => ({tag: e.tagName, cls: (e.className||'').toString().slice(0,40), text: e.textContent.trim().slice(0,50)}));
        }""")
        for w in word_items:
            log(f"  {w['tag']}.{w['cls']}: '{w['text']}'")
        # total word items
        total = await page.evaluate("""() => {
            // count elements that could be word rows
            return document.querySelectorAll('[class*=word], [class*=vocab], [class*=item], [class*=card]').length;
        }""")
        log(f"  total vocab-ish elements: {total}")

        await browser.close()

asyncio.run(main())
