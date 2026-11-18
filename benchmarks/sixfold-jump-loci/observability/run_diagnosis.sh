#!/bin/sh
# Guarded-pipeline ablations on identical observations (about 4 minutes on 2 cores).
set -e
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
mkdir -p out/diagnosis
[ -f ../data/manifest.json ] || (cd .. && python3 generate.py data > /dev/null)
[ -f out/diagnosis/published_guarded_49.json ] || (cd .. && python3 experiment.py data /tmp/identified && python3 -c "import json;json.dump(json.load(open('/tmp/identified/predictions.json'))['49']['guarded-weak-locus'],open('observability/out/diagnosis/published_guarded_49.json','w'))")
python3 diagnose.py 2 > out/diagnosis/run.log
python3 analyse_diagnosis.py > out/diagnosis/report.log
