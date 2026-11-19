#!/bin/sh
# Single reproducible rebuild of all round-3 data changes (question bank + vocabulary) from the v42.0.1 originals.
set -e
cd "$(dirname "$0")/.."
sh tools/rebuild_vault.sh
cp backups/data-v42.0.1.json data/data.json
cp backups/senses-v42.0.1.json data/senses.json
python3 tools/apply_headword_rename.py
python3 tools/apply_vocab_examples.py
python3 tools/vocab_triage.py
python3 tools/ipa_fill.py
python3 tools/vocab_dedupe.py
python3 tools/ipa_stress_fix.py
node tools/datafiles.js build data web 43.0.0
echo "rebuild_all: done ($(wc -l < qa/changes_r3.jsonl) logged changes)"
