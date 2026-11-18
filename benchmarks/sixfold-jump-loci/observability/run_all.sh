#!/bin/sh
# Regenerates observability/out/*. Python 3.12 with requirements.txt; about one minute.
set -e
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
python3 exact_check.py
python3 run_signals.py > out/signals.log
python3 remainder.py > /dev/null
python3 design.py > out/design.log
python3 evaluate_design.py > out/design_test.log
python3 tables.py > out/tables.log
echo "observability outputs regenerated in $(pwd)/out"
