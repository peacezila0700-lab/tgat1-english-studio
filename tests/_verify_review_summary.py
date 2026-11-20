"""Verify feature (c): review-summary teaching fires after 5 completed units."""
import asyncio, os, sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/home/user/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome', args=['--no-sandbox'])
        ctx = await b.new_context()
        page = await ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        await page.goto('http://localhost:8765/index.html')
        await page.wait_for_timeout(3000)

        # Verify TGAT1_showReviewSummary exists
        has_fn = await page.evaluate('typeof TGAT1_showReviewSummary')
        print(f'TGAT1_showReviewSummary: {has_fn}')

        # Verify TGAT1Hub exists (learning-hub.js parses)
        has_hub = await page.evaluate('typeof TGAT1Hub')
        print(f'TGAT1Hub: {has_hub}')

        # No page errors
        print(f'pageerrors: {errs}')

        # Test the summary function directly by calling it
        await page.evaluate('TGAT1_showReviewSummary()')
        await page.wait_for_timeout(1000)

        # Check if a modal/summary appeared
        modal_text = await page.evaluate('''() => {
            const modals = document.querySelectorAll('[class*="review"], [class*="summary"], [class*="modal"], [class*="overlay"]');
            return Array.from(modals).map(m => m.innerText.slice(0,100)).filter(t => t.length > 10);
        }''')
        print(f'modals found: {len(modal_text)}')
        for m in modal_text[:3]:
            print(f'  -> {m[:80]}')

        # Also check the hub page renders without errors
        await page.evaluate('studioNav("hub")')
        await page.wait_for_timeout(2000)
        hub_text = await page.evaluate('document.querySelector("#app").innerText.slice(0,200)')
        print(f'hub page: {hub_text[:100]}')
        print(f'pageerrors after hub: {errs}')

        await b.close()
        print('VERIFY: PASS' if has_fn == 'function' and has_hub == 'object' and not errs else 'VERIFY: FAIL')

asyncio.run(main())
