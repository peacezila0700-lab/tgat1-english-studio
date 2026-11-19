"""Check and unpack parts downloaded from Drive.
Usage:  python3 tools/sync_unpack.py DOWNLOAD_DIR TARGET_DIR
Stops (exit 1) if any part listed in MANIFEST.json is missing or its SHA-256 differs.
"""
import hashlib, json, os, sys, zipfile
src, dst = sys.argv[1], sys.argv[2]
m = json.load(open(os.path.join(src, 'MANIFEST.json')))
bad = []
for p in m['parts']:
    f = os.path.join(src, p['name'])
    if not os.path.exists(f): bad.append(p['name'] + ': missing'); continue
    if hashlib.sha256(open(f, 'rb').read()).hexdigest() != p['sha256']: bad.append(p['name'] + ': sha256 mismatch')
if bad:
    print('STOP — do not work on this copy; ask the user:\n  ' + '\n  '.join(bad)); sys.exit(1)
os.makedirs(dst, exist_ok=True)
for p in m['parts']:
    zipfile.ZipFile(os.path.join(src, p['name'])).extractall(dst)
print(f"OK: {len(m['parts'])} parts by {m['written_by']} at {m['written_at']} -> {dst}")
