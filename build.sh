#!/usr/bin/env bash
# Rebuild the JoSAA IIT cutoff database + website from IIT_ALL.txt.
# Runs each stage in order and STOPS immediately if any stage fails.
set -euo pipefail

cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

echo "==> [1/4] Building CSV database from IIT_ALL.txt"
"$PY" make_db.py

echo
echo "==> [2/4] Verifying CSV is consistent with IIT_ALL.txt"
"$PY" verify_db.py

echo
echo "==> [3/4] Checking course-group coverage (every program in a group)"
"$PY" check_groups.py | tail -n 8

echo
echo "==> [4/4] Generating index.html from the verified CSV"
"$PY" build_site.py

echo
echo "==> Done. Open index.html in your browser."
