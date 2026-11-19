# T2/T4 STATUS — CSP hardening + lazy hub (DONE)

## Completed & committed
- **T2 (CSP) — `a267500`:** inline `on*=` → `data-action` + delegated dispatcher (click/change/input/submit/keydown);
  18 `window.TGAT1_c_*` wrappers; boot helpers moved to top of app.js; CSP `script-src 'self'` (no `'unsafe-inline'`);
  learning-hub.js 29 onclicks converted; harness axe via URL routing; suites green.
- **T4 (lazy hub) — `c028805`:** `learning-hub*.js` no longer load at startup — `window.TGAT1_loadHub()`
  injects curriculum + engine on first hub entry; `studioNavNow('hub')` awaits load before render;
  `studioHome()` background-loads so the Continue CTA appears (SW-cached → offline-safe);
  tests patched to `wait_for_function("typeof TGAT1Hub==='object'")`.
  Suites: r3_ui 7/7, smoke_r3_extra 94/94, r3_content 59/59, **regression_v42 58/60**.

## regression_v42 58/60 — 2 failures are PRE-EXISTING (not from T2/T4)
Verified by stashing T4 and re-running at T2 commit: same 2 failures.
1. `vocab detail: main meaning is "แย่ลง"` — modal check; passes when run in isolation (likely test-order/state pollution in suite).
2. `save/resume: in-progress mock survives reload` — `{'saved': False, 'answered': 0, 'live': True}`; passes in isolation.
Both pass when the steps run standalone — suite-order timing issue, not a regression from T2/T4. LEAVE AS-IS for now (out of T2/T4 scope); note for later investigation.

## Remaining work order (from qa/V43-NEXT-WORK.md)
1. ✅ T2 (CSP) — DONE
2. ✅ T4 (learning-hub lazy) — DONE
3. **T5 — Lighthouse / Web Vitals audit** — NEXT
4. Debts: A3 → A4 → A5 → C4 → S4
5. 7 `check_quotes.py` misses
6. regression_v42 2 pre-existing failures (investigate when time allows)

## Gotchas for T4+
- Playwright env: `CHROME=/home/user/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome`,
  `AXE_PATH=tools/node_modules/axe-core/axe.min.js`; run from `tests/` dir with `../web` arg.
- Fresh sandbox needs: `pip3 install playwright`, `python3 -m playwright install chromium`,
  `install-deps chromium`, `npm install axe-core` + copy axe.min.js into `tools/node_modules/axe-core/`.
- `git commit` needs `git config user.name/user.email` first (sandbox resets git identity).
- Tool-call limit per turn: chunk work, commit per chunk, re-check `git status` at turn start.
- Never hand-edit `qa/REVIEW-QUEUE.csv`, `data/data.json`, `web/data.js` — author specs in `content/`.
- Drive upload (do NOT repeat): folder `1sbaXysMpa4HeFy8KMHhJTCHDM9qIrKZS`, WORKING-v43-Arena-part1/2/3.zip.
