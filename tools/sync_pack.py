"""Pack the whole project into parts small enough for a Google Drive connector upload.
Usage:  python3 tools/sync_pack.py OUTDIR AUTHOR "note"
Writes OUTDIR/WORKING-partN.zip (each <= LIMIT bytes) + OUTDIR/MANIFEST.json.
Every part is an ordinary ZIP: unzip all parts into ONE folder to get the full project.
"""
import hashlib, json, os, sys, zipfile, datetime
LIMIT = 2_800_000            # connector limit is ~3.1 MB per call; keep a margin
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'node_modules', '__pycache__', '.git'}
SKIP_FILES = {'backups/v42.0.1-original.zip'}

def files():
    for d, ds, fs in os.walk(ROOT):
        ds[:] = sorted(x for x in ds if x not in SKIP_DIRS)
        for f in sorted(fs):
            rel = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
            if rel not in SKIP_FILES:
                yield rel

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def main(out, author, note):
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.startswith('WORKING-part') or f == 'MANIFEST.json': os.remove(os.path.join(out, f))
    all_files = list(files())

    def pack(turn):
        """Zip every file, starting a new part once the current one passes `turn` bytes."""
        parts, n, z, cur = [], 0, None, None
        for rel in all_files:
            if z is None or os.path.getsize(cur['path']) > turn:
                if z: z.close(); parts.append(cur)
                n += 1
                cur = {'path': os.path.join(out, f'WORKING-part{n}.zip'), 'files': 0}
                z = zipfile.ZipFile(cur['path'], 'w', zipfile.ZIP_DEFLATED, compresslevel=9)
            z.write(os.path.join(ROOT, rel), rel); cur['files'] += 1
            z.fp.flush()
        if z: z.close(); parts.append(cur)
        return parts

    # A part can overshoot `turn` by at most the largest single compressed file
    # (qa/DATA-CHANGES.csv ≈ 0.5 MB), so keep that much headroom and retry tighter
    # if a part still lands over the connector limit.
    turn = LIMIT - 700_000
    for _ in range(6):
        for f in os.listdir(out):
            if f.startswith('WORKING-part'): os.remove(os.path.join(out, f))
        parts = pack(turn)
        if all(os.path.getsize(p['path']) <= LIMIT for p in parts): break
        turn = int(turn * 0.8)
    else:
        sys.exit(f'no packing under {LIMIT} bytes after 6 attempts; a single file is too big — split it by hand')
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    m = {'project': 'TGAT1 English Studio', 'written_by': author, 'written_at': now.isoformat(timespec='minutes'),
         'note': note, 'how_to_open': 'download ALL parts, unzip every part into the SAME empty folder',
         'parts': [{'name': os.path.basename(p['path']), 'bytes': os.path.getsize(p['path']),
                    'files': p['files'], 'sha256': sha(p['path'])} for p in parts]}
    json.dump(m, open(os.path.join(out, 'MANIFEST.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(m, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '?', sys.argv[3] if len(sys.argv) > 3 else '')
