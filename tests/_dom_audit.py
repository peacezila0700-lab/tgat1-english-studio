#!/usr/bin/env python3
"""Deep DOM audit: inspect actual rendered content of each page for real-user issues."""
import asyncio, os, json
from playwright.async_api import async_playwright

BASE = "http://localhost:8765/"
OUT = "/home/user/google_drive/project_claude/qa/deep_audit"
os.makedirs(OUT, exist_ok=True)

ISSUES = []
def log(msg):
    print(msg, flush=True)
    ISSUES.append(msg)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=os.environ["CHROME"], args=["--no-sandbox","--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width":390,"height":844}, user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36")

        async def goto(nav):
            await page.goto(BASE, wait_until="networkidle")
            await page.wait_for_timeout(800)
            await page.evaluate(f"document.querySelector('[data-page=\"{nav}\"]')?.click()")
            await page.wait_for_timeout(1500)

        # ===== HOME =====
        log("\n=== HOME ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,2000) || ''")
        log("TEXT: " + text[:600].replace("\n"," | "))
        # check headings
        heads = await page.evaluate("[...document.querySelectorAll('h1,h2,h3')].map(e=>e.textContent).slice(0,10)")
        log(f"HEADINGS: {heads}")
        # check for empty sections
        empty = await page.evaluate("[...document.querySelectorAll('.pk-card, .pk-section')].filter(e=>e.innerText.trim().length<10).length")
        log(f"EMPTY CARDS: {empty}")

        # ===== VOCAB =====
        log("\n=== VOCAB ===")
        await goto("vocab")
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,1500) || ''")
        log("TEXT: " + text[:500].replace("\n"," | "))
        # check search
        inputs = await page.evaluate("[...document.querySelectorAll('input')].map(e=>({id:e.id,type:e.type,placeholder:e.placeholder}))")
        log(f"INPUTS: {inputs}")
        # check word list renders
        wordcount = await page.evaluate("document.querySelectorAll('.pk-card, .vword, .word-card, [class*=vocab], [class*=word]').length")
        log(f"VOCAB ELEMENTS: {wordcount}")

        # ===== EXAM =====
        log("\n=== EXAM ===")
        await goto("exam")
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,1500) || ''")
        log("TEXT: " + text[:500].replace("\n"," | "))
        buttons = await page.evaluate("[...document.querySelectorAll('button')].map(e=>e.textContent.trim().slice(0,30)).filter(Boolean).slice(0,20)")
        log(f"BUTTONS: {buttons}")

        # ===== GAME =====
        log("\n=== GAME ===")
        await goto("game")
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,1500) || ''")
        log("TEXT: " + text[:500].replace("\n"," | "))
        buttons = await page.evaluate("[...document.querySelectorAll('button')].map(e=>e.textContent.trim().slice(0,30)).filter(Boolean).slice(0,20)")
        log(f"BUTTONS: {buttons}")

        # ===== ANALYTICS =====
        log("\n=== ANALYTICS ===")
        await goto("analytics")
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,2000) || ''")
        log("TEXT: " + text[:600].replace("\n"," | "))

        # ===== SETTINGS =====
        log("\n=== SETTINGS ===")
        await goto("settings")
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,2000) || ''")
        log("TEXT: " + text[:600].replace("\n"," | "))
        # check toggles
        toggles = await page.evaluate("[...document.querySelectorAll('input[type=checkbox], input[type=radio], select')].map(e=>({type:e.type,name:e.name,checked:e.checked})).slice(0,20)")
        log(f"TOGGLES: {toggles}")

        # ===== PROFILE =====
        log("\n=== PROFILE ===")
        await goto("profile")
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,2000) || ''")
        log("TEXT: " + text[:600].replace("\n"," | "))
        inputs = await page.evaluate("[...document.querySelectorAll('input')].map(e=>({id:e.id,type:e.type,placeholder:e.placeholder,value:e.value})).slice(0,10)")
        log(f"INPUTS: {inputs}")

        # ===== HUB =====
        log("\n=== HUB ===")
        await goto("hub")
        await page.wait_for_timeout(2000)
        text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,2500) || ''")
        log("TEXT: " + text[:800].replace("\n"," | "))
        # check progress display
        prog = await page.evaluate("document.querySelector('[class*=progress], [class*=Progress]')?.textContent?.slice(0,100) || 'N/A'")
        log(f"PROGRESS: {prog}")

        # ===== Test full mock flow =====
        log("\n=== MOCK FLOW TEST ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        # find and click exam → start mock
        await page.evaluate("document.querySelector('[data-page=\"exam\"]')?.click()")
        await page.wait_for_timeout(1500)
        # click first mock set
        clicked = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button[data-action]')];
            const mock = btns.find(b => /เริ่มชุด|mock|จำลอง/i.test(b.textContent));
            if (mock) { mock.click(); return mock.textContent.slice(0,30); }
            return null;
        }""")
        log(f"Mock start: {clicked}")
        await page.wait_for_timeout(2000)
        quiz_text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,1000) || ''")
        log(f"QUIZ TEXT: {quiz_text[:400].replace(chr(10),' | ')}")
        # answer a question
        answered = await page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button')];
            const opt = btns.find(b => /^[ABCD]\./.test(b.textContent.trim()));
            if (opt) { opt.click(); return opt.textContent.trim().slice(0,20); }
            return null;
        }""")
        log(f"Answered: {answered}")
        await page.wait_for_timeout(1500)
        after_text = await page.evaluate("document.querySelector('#app')?.innerText?.slice(0,1500) || ''")
        log(f"AFTER ANSWER: {after_text[:500].replace(chr(10),' | ')}")

        await browser.close()
        with open(f"{OUT}/DOM_REPORT.txt","w") as f:
            f.write("\n".join(ISSUES))
        log(f"\n=== DOM AUDIT DONE: {len(ISSUES)} entries ===")

asyncio.run(main())
