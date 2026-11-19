#!/bin/sh
# Rebuild data/vault.json from the untouched v42.0.1 bank by replaying every round-3 content change in order.
set -e
cd "$(dirname "$0")/.."
cp backups/vault-v42.0.1.json data/vault.json
rm -f qa/changes_r3.jsonl
python3 tools/apply_lc_blank.py >/dev/null
python3 tools/apply_tc_v43.py >/dev/null
python3 tools/apply_rc_v43.py >/dev/null
python3 tools/apply_short_v43.py >/dev/null
python3 tools/apply_qr_idiom.py >/dev/null
python3 tools/apply_short_new_v43.py >/dev/null
python3 tools/apply_qr_v43.py >/dev/null
python3 tools/apply_a3.py >/dev/null
echo rebuilt
