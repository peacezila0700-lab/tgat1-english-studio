#!/bin/sh
# Rebuild round-3 question-bank content from the untouched v42.0.1 vault + content/*.json specs.
set -e
cd "$(dirname "$0")/.."
cp backups/vault-v42.0.1.json data/vault.json
rm -f qa/changes_r3.jsonl
python3 tools/apply_lc_blank.py
python3 tools/apply_lc_comp.py
python3 tools/tc_apply.py
python3 tools/rc_apply.py
cp backups/data-v42.0.1.json data/data.json
cp backups/senses-v42.0.1.json data/senses.json
python3 tools/vocab_triage.py
python3 tools/ipa_fill.py
python3 tools/vocab_dedupe.py
