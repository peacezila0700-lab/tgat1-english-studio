#!/usr/bin/env python3
"""TTS verification + UX round: all pages, light/dark, screenshots."""
import os, sys, time, json

os.environ['LD_LIBRARY_PATH'] = '/tmp/libx/usr/lib/x86_64-linux-gnu'
CHROME = '/home/user/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome'

from playwright.sync_api import sync_playwright

BASE = 'http://localhost:8765'
SHOT_DIR = '/home/user/google_drive/project_claude/qa/screenshots'
os.makedirs(SHOT_DIR, exist_ok=True)

def test_tts(page):
    """Test TTS on vocab page."""
    results = {}
    page.goto(BASE + '/index.html', wait_until='networkidle')
    time.sleep(1)

    # Navigate to vocab
    page.evaluate("window.studioNav('vocab')")
    time.sleep(1)

    # Check voices
    voices = page.evaluate("(() => { try { return window.speechSynthesis.getVoices(); } catch(e) { return 'error: '+e.message; } })()")
    results['voices_count'] = len(voices) if isinstance(voices, list) else 0
    results['voices_sample'] = voices[:3] if isinstance(voices, list) and len(voices) > 0 else voices

    # Try clicking first word to open detail modal
    first_word = page.evaluate("(() => { const btn = document.querySelector('.pk-word-grid .st-word'); return btn ? btn.textContent.substring(0,30) : null; })()")
    results['first_word'] = first_word

    if first_word:
        page.click('.pk-word-grid .st-word', timeout=5000)
        time.sleep(1)

        # Check if modal opened
        modal = page.query_selector('#studioModal')
        results['modal_opened'] = bool(modal)

        if modal:
            # Try clicking TTS button
            tts_btn = page.query_selector('#studioModal button[data-action="studioSayWord"]')
            results['tts_button_found'] = bool(tts_btn)

            if tts_btn:
                # Check speechSynthesis state
                synth_state = page.evaluate("(() => { return { hasSynth: !!window.speechSynthesis, hasUtterance: !!window.SpeechSynthesisUtterance, speaking: window.speechSynthesis.speaking, pending: window.speechSynthesis.pending }; })()")
                results['synth_state'] = synth_state

                # Click TTS button
                tts_btn.click()
                time.sleep(2)

                # Check if speaking started
                after_state = page.evaluate("(() => { return { speaking: window.speechSynthesis.speaking, pending: window.speechSynthesis.pending }; })()")
                results['after_click_state'] = after_state

                # Check if help modal appeared (fallback)
                help_modal = page.query_selector('.modal')
                results['help_modal_shown'] = bool(help_modal)

    return results

def screenshot_page(page, name, dark=False):
    """Take screenshot of current page."""
    if dark:
        page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
        time.sleep(0.5)
    page.screenshot(path=f'{SHOT_DIR}/{name}.png', full_page=True)
    if dark:
        page.evaluate("document.documentElement.setAttribute('data-theme','light')")
        time.sleep(0.3)

def test_all_pages(page):
    """Open all pages and screenshot."""
    pages = ['home', 'vocab', 'exam', 'game', 'analytics', 'settings', 'profile']
    for p in pages:
        try:
            page.evaluate(f"window.studioNav('{p}')")
            time.sleep(1.5)
            screenshot_page(page, f'light_{p}')
            screenshot_page(page, f'dark_{p}', dark=True)
            print(f'  ✓ {p}: screenshot done')
        except Exception as e:
            print(f'  ✗ {p}: {e}')

    # Also test hub
    try:
        page.evaluate("window.studioNav('hub')")
        time.sleep(3)  # hub loads lazily
        screenshot_page(page, 'light_hub')
        screenshot_page(page, 'dark_hub', dark=True)
        print('  ✓ hub: screenshot done')
    except Exception as e:
        print(f'  ✗ hub: {e}')

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox', '--disable-dev-shm-usage', '--autoplay-policy=no-user-gesture-required'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})

    print('=== TTS Test ===')
    tts_results = test_tts(page)
    print(json.dumps(tts_results, indent=2, ensure_ascii=False, default=str))

    print('\n=== UX Screenshots ===')
    test_all_pages(page)

    # Save TTS results
    with open(f'{SHOT_DIR}/tts_results.json', 'w') as f:
        json.dump(tts_results, f, indent=2, ensure_ascii=False, default=str)

    browser.close()
    print('\nDone!')
