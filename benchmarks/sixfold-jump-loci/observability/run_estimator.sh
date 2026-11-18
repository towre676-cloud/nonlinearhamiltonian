#!/bin/sh
# Constrained-estimator study: prior, calibration, freeze, confirmation, scoring. About 45 minutes on 2 cores.
set -e
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
[ -f ../data/manifest.json ] || (cd .. && python3 generate.py data > /dev/null)
python3 run_estimator.py fresh_groups
python3 run_estimator.py calibrate 2 > out/estimator/calibrate.log 2>&1
python3 freeze.py > out/estimator/freeze.log
python3 run_estimator.py confirm 2 > out/estimator/confirm.log 2>&1
python3 score.py > out/estimator/score.log 2>&1
echo "estimator outputs in $(pwd)/out/estimator"
