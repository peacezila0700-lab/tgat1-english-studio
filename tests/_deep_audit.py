#!/usr/bin/env python3
"""Deep real-user audit: walk every page, click everything, capture issues."""
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright

BASE = "http://localhost:8765/"
OUT = "/home/user/google_drive/project_claude/qa/deep_audit"
os.makedirs(OUT, exist_ok=True)

ISSUES = []
def log(msg):
    print(msg, flush=True)
    ISSUES.append(msg)

async def goto_page(page, nav_name, label):
    await page.goto(BASE, wait_until="networkidle")
    await page.wait_for_timeout(800)
    # try direct click with force
    sel = f'[data-page="{nav_name}"]'
    el = await page.query_selector(sel)
    if el:
        try:
            # use JS click — works regardless of CSS visibility
            await page.evaluate(f"document.querySelector('{sel}').click()")
        except Exception as e:
            log(f"  WARN: nav {label} click failed: {e}")
        await page.wait_for_timeout(1500)
        log(f"  navigated to {label}")
    return True

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=os.environ["CHROME"], args=["--no-sandbox","--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width":390,"height":844}, user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36")

        console_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type=="error" else None)
        page.on("pageerror", lambda e: console_errors.append(f"PAGEERROR: {e}"))

        # === 1. HOME ===
        log("\n=== [1] HOME ===")
        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f"{OUT}/home.png", full_page=True)
        log(f"  home: {len(await page.query_selector_all('button'))} buttons, {len(await page.query_selector_all('[data-page]'))} nav items")

        # === 2. VOCAB ===
        log("\n=== [2] VOCAB ===")
        await goto_page(page, "vocab", "vocab")
        await page.screenshot(path=f"{OUT}/vocab.png", full_page=True)
        sr = await page.query_selector("input[type=search], input[type=text]")
        if sr:
            await sr.fill("hello")
            await page.wait_for_timeout(500)
            await page.screenshot(path=f"{OUT}/vocab_search.png")
            await sr.fill("")
            await page.wait_for_timeout(300)
        else:
            log("  WARN: no search input on vocab page")

        # === 3. EXAM ===
        log("\n=== [3] EXAM ===")
        await goto_page(page, "exam", "exam")
        await page.screenshot(path=f"{OUT}/exam.png", full_page=True)
        # find a practice/quick button
        for btn in await page.query_selector_all("[data-action], button"):
            try:
                t = (await btn.inner_text())[:60]
                at = await btn.get_attribute("data-action","")
                if any(k in t for k in ["ฝึก","quick","ด่วน","เริ่ม","mock","test","ชุด"]):
                    log(f"  exam button: '{t}' action={at}")
                    await btn.click(force=True)
                    await page.wait_for_timeout(1500)
                    await page.screenshot(path=f"{OUT}/exam_quick.png", full_page=True)
                    # answer
                    for o in await page.query_selector_all("button, [data-action]"):
                        ot = await o.inner_text()
                        if ot.strip() and len(ot) < 300 and ot[0] in "ABCD" and len(ot) > 1:
                            await o.click(force=True)
                            await page.wait_for_timeout(1000)
                            break
                    await page.screenshot(path=f"{OUT}/exam_answered.png", full_page=True)
                    break
            except: pass

        # === 4. GAME ===
        log("\n=== [4] GAME ===")
        await goto_page(page, "game", "game")
        await page.screenshot(path=f"{OUT}/game.png", full_page=True)
        for btn in await page.query_selector_all("[data-action], button"):
            try:
                t = (await btn.inner_text())[:60]
                if any(k in t for k in ["เกม","ฝึก","quiz","start","เริ่ม"]):
                    await btn.click(force=True)
                    await page.wait_for_timeout(1500)
                    await page.screenshot(path=f"{OUT}/game_play.png", full_page=True)
                    break
            except: pass

        # === 5. ANALYTICS ===
        log("\n=== [5] ANALYTICS ===")
        await goto_page(page, "analytics", "analytics")
        await page.screenshot(path=f"{OUT}/analytics.png", full_page=True)

        # === 6. SETTINGS ===
        log("\n=== [6] SETTINGS ===")
        await goto_page(page, "settings", "settings")
        await page.screenshot(path=f"{OUT}/settings.png", full_page=True)
        # find theme toggle
        for el in await page.query_selector_all("[data-action], button, input[type=checkbox], select"):
            try:
                t = (await el.inner_text().catch(lambda: ""))[:60]
                at = (await el.get_attribute("data-action","").catch(lambda: ""))[:60]
                if "theme" in (t+at).lower() or "โหมด" in t or "มืด" in t or "dark" in (t+at).lower():
                    await el.click(force=True)
                    await page.wait_for_timeout(500)
                    await page.screenshot(path=f"{OUT}/settings_dark.png", full_page=True)
                    await el.click(force=True)
                    await page.wait_for_timeout(300)
                    break
            except: pass

        # === 7. PROFILE ===
        log("\n=== [7] PROFILE ===")
        await goto_page(page, "profile", "profile")
        await page.screenshot(path=f"{OUT}/profile.png", full_page=True)

        # === 8. HUB ===
        log("\n=== [8] HUB ===")
        await goto_page(page, "hub", "hub")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{OUT}/hub.png", full_page=True)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{OUT}/hub_scroll.png", full_page=True)

        # === Console errors ===
        log("\n=== CONSOLE ERRORS ===")
        for e in console_errors[:20]:
            log(f"  ERROR: {e[:120]}")
        if not console_errors:
            log("  (none)")

        # === Storage ===
        log("\n=== STORAGE KEYS ===")
        keys = await page.evaluate("JSON.stringify(Object.keys(localStorage))")
        log(f"  {keys[:400]}")

        await browser.close()
        with open(f"{OUT}/REPORT.txt","w") as f:
            f.write("\n".join(ISSUES))
        log(f"\n=== AUDIT DONE: {len(ISSUES)} entries ===")

asyncio.run(main())
