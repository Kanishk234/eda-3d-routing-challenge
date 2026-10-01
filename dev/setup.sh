#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
revision=499ad7e2a415a97e9ce9b3396b0477e75ebd13e6
python3 -m venv .venv
.venv/bin/python -m pip install --no-index -r dev/requirements.txt
mkdir -p dev/upstream
if [[ ! -d "dev/upstream/$revision" ]]; then
    temporary=$(mktemp -d "dev/upstream/.snapshot.XXXXXX")
    git archive "$revision" | tar -x -C "$temporary"
    mv "$temporary" "dev/upstream/$revision"
fi
.venv/bin/python --version
printf 'Pinned evaluator: %s\n' "$revision"
