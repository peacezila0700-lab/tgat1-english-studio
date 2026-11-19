# TGAT1 English Studio v42.0.2 — Round 3 engineering assessment (CSP, initial load, patch structure)

Measured on 2026-11-19 against the v42.0.2 build in this package. Nothing here has been tested on a physical device.

## 1. Content Security Policy

**Status: transitional CSP added (not strict).**

`index.html` now carries a `<meta http-equiv="Content-Security-Policy">` with `default-src 'self'`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `connect-src 'self'`, `worker-src 'self'`, and `img/media-src 'self' data: blob:`. This blocks third-party scripts, plugins, `<base>` hijacking and off-site form posts. It was added by the parallel session and verified here: smoke 49/49, regression 60/60, extra smoke 94/94, and no CSP console errors in any tested flow.

**Why it is not strict yet.** `script-src` still needs `'unsafe-inline'` for two reasons:

| Blocker | Count / location |
|---|---|
| Inline event-handler attributes (`onclick=`, `onchange=`, `onkeydown=` …) in templates and markup | ≈305 occurrences across `app.js`, `learning-hub.js` and `index.html` |
| Inline `<script>` block in `index.html` (theme colour sync, mobile “more” menu) | 1 |
| Inline `style=` attributes, which need `style-src 'unsafe-inline'` | many, generated in templates |

**Path to a strict CSP (not done; estimated as a separate engineering round):**
1. Move the inline `<script>` in `index.html` into `app.js`. This is low risk.
2. Replace `on*=` attributes with `data-action` attributes and one delegated `click`/`change`/`keydown` listener per root. This touches about 300 template strings, so it needs the full smoke/regression and axe suites after each module.
3. Serve the CSP as an HTTP header, including `frame-ancestors 'none'`, which a meta tag cannot set.
4. Replace inline `style=` attributes with classes, then drop `style-src 'unsafe-inline'`.

## 2. Initial-load performance

Asset sizes (bytes; gzip -9 shows what a server with compression would send):

| File | Raw | gzip | Loaded |
|---|---:|---:|---|
| index.html | 8,727 | 3,050 | initial |
| app.css | 274,015 | 56,570 | initial |
| learning-hub.css | 11,294 | 2,908 | initial |
| **data.js** | **2,039,132** | **330,626** | **initial (blocking)** |
| app.js | 763,338 | 214,582 | initial (blocking) |
| learning-hub-curriculum.js | 283,534 | 69,121 | initial |
| learning-hub.js | 77,696 | 23,928 | initial |
| data-vault.js | 1,056,723 | 238,080 | lazy (exam bank) |
| data-senses.js | 1,081,356 | 188,727 | lazy (word senses) |

Measured in Playwright Chrome with a local server and **no compression** (3.49 MB transferred before the app is interactive):
- Desktop 1366 px, no throttling: ready in ≈0.36–0.52 s.
- Mobile 390 px, simulated slow 3G (1.6 Mbit/s, 150 ms) plus 4× CPU slowdown: ready in ≈19.4 s.

With gzip or brotli on the host, the initial set falls to about 0.70 MB, roughly 3.5 s of transfer on that same simulated network. The simulation is a model, not a real-device measurement.

**Findings and recommendations (not implemented in v42.0.2; the risk of regressions is too high for this round):**
1. **Enable compression on the host.** This is the single largest win (about 5× fewer bytes) and needs no code change. `README-DEPLOYMENT.md` now says so.
2. **`data.js` (2.0 MB) blocks the first render.** It carries `studio.examples` (an example map for every word), `legacy.V/SYN/ANT/CL` and the `pack` content. Splitting rarely used parts (examples, `pack`) into a lazy chunk, as was already done for vault and senses, would roughly halve the blocking bytes.
3. `learning-hub-curriculum.js` and `learning-hub.js` (≈93 KB gzip) load at startup but are needed only on the Hub route. They could load on demand, provided `TGAT1Hub.continue()` on Home still works offline (the service worker already pre-caches them).
4. Lighthouse and Web Vitals were not run. Real-device timing on iOS Safari and Android Chrome is still untested.

## 3. Large nested-patch structure

`app.js` is a concatenation of 45 historical layers (`/* ===== NN · file.js ===== */`) that override one another at runtime:

- 526 function declarations (497 distinct names). **16 names are declared more than once** (for example `audit` ×6, `start` ×5, `decorate` ×4).
- **43 functions are declared and later reassigned** (monkey-patched), for example `studioRender` ×4, `VLT_finish` ×4, `studioNav` ×3, `VLT_renderQuiz` ×3 and `mkMatch`.

**A concrete bug this structure caused (found in round 3).** The v42.0.1 matching-game de-duplication was written into an earlier `mkMatch`. A later layer replaced `mkMatch`, so the fix never ran: 80 of 2,000 simulated rounds (4.0%) still had a duplicate word or overlapping meaning. The v42.0.2 fix goes into the active override, and a 400-round regression in `tests/regression_r3_ui.py` now exercises the function the game actually calls.

**Recommendation (not done).** Before any further feature work, generate a "final binding" map (for each global function, which layer wins) and add a test that fails when a layer redefines a function without an explicit `/* overrides: … */` marker. Then refactor the most-patched paths (render, exam engine, navigation) into single modules. No refactor was attempted in v42.0.2, to protect the passing flows.
