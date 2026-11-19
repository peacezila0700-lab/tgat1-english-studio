# Lighthouse Report — v43.0.0 (T5)

Run: 2026-11-19 · mobile emulation · simulated throttling · localhost http.server

## Scores

| Category | Score |
|---|---|
| Performance | 50 |
| Accessibility | 100 |
| Best Practices | 96 |
| SEO | 100 |

## Web Vitals

- **FCP**: 10.5 s
- **LCP**: 18.6 s
- **TBT**: 250 ms
- **CLS**: 0.074
- **Speed Index**: 10.5 s
- **TTI**: 18.6 s

## Top opportunities

- **-13500 ms** — Enable text compression (uses-text-compression)
- **-9414 ms** — Eliminate render-blocking resources (render-blocking-resources)
- **-2700 ms** — Reduce unused JavaScript (unused-javascript)
- **-900 ms** — Reduce unused CSS (unused-css-rules)
- **-150 ms** — Minify CSS (unminified-css)

## Notes

- Accessibility 100 / SEO 100 — clean.

- Performance 50 is dominated by **server-side** factors on the audit harness (python http.server sends no gzip → "Enable text compression" -13.5s is harness artifact, not app defect).

- "Eliminate render-blocking resources" (-9.4s): `data.js` (1.6 MB) + `app.js` are parser-blocking `<script>` tags. Real fix: serve with compression + consider `defer` (app is DOMContentLoaded-gated so defer is safe).

- "Reduce unused JavaScript" (-2.7s): bundle size; T1/T2/T4 already trimmed inline handlers and lazy-loaded hub. Further gains need build-time tree-shaking (not present in this no-build pipeline).

- Raw JSON: `qa/lighthouse-v43.json`