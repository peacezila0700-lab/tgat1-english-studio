# TGAT1 English Studio v43.0.0

Static progressive web app. Serve this directory over HTTPS, or on localhost for development. Opening `index.html` as a file may disable PWA features.

**Enable gzip or brotli compression on the host.** The initial download is about 3.5 MB uncompressed and about 0.7 MB compressed; `data.js` alone is 2 MB.

`index.html` contains a transitional Content-Security-Policy meta tag. If the host can send headers, also send the same policy as an HTTP header and add `frame-ancestors 'none'`.

The deployment package contains only web-root files. It excludes backups, QA data, scripts and tests.

**Release status:** remediation build, not final production approval. See `ROUND3-STATUS.md`.

Practice content is original practice material: not official TGAT1 questions, not past papers, and not a score prediction.
