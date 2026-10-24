#!/usr/bin/env python3
"""Replay small literature-data ingestion; no network, training or new tracking."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import statistics
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def require(condition,message):
    if not condition:
        raise ValueError(message)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'INGESTION_REPLAY.json')
    args=parser.parse_args()
    catalog=json.loads((HERE/'SOURCE_CATALOG.json').read_text())
    require(len(catalog['sources'])==catalog['method_source_records']==73,'source count')
    require(all(row['primary_urls']for row in catalog['sources']),'source URLs')
    url_count=len({u for r in catalog['sources']for u in r['primary_urls']})
    require(url_count==catalog['distinct_primary_url_strings'],'URL count')
    require(len(json.loads((HERE/'datasets_catalog.json').read_text())['assets'])==12,'asset count')
    env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
    runs=[]
    for script in ['check_dataset_samples.py','inspect_multifidelity_data.py',
                   'differentiable_data/replay_memory.py', 'check_core_vs_tractability.py']:
        start=time.perf_counter()
        command=[sys.executable,'-B',str(HERE/script)]
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True)
        require(result.returncode==0,script+' failed: '+result.stderr[-2000:])
        runs.append({'script':script,'exit_code':result.returncode,
                     'checker_seconds':time.perf_counter()-start,
                     'result':json.loads(result.stdout)})
    ring=json.loads((HERE/'public_ring_smoke.json').read_text())
    source=HERE/'dataset_inspection/at_hmba.mat'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==ring['lattice_sha256'],'ring source')
    require(ring['tracked_ring_periodicity']==1 and ring['tracked_ring_elements']==3872,'ring turn')
    require(ring['survivors']+ring['losses']==ring['particles']==64,'particle accounting')
    require(ring['turns']==128 and ring['repeats']==3,'stored probe protocol')
    require(ring['final_state_max_batch_single_difference']==0,'stored state agreement')
    for label in ['batch_seconds','cached_single_seconds']:
        require(len(ring[label])==3 and all(math.isfinite(t)and t>0 for t in ring[label]),'stored timers')
    ratio=statistics.median(ring['cached_single_seconds'])/statistics.median(ring['batch_seconds'])
    require(abs(ratio-ring['batching_gain_median'])<1e-12,'stored timer arithmetic')
    quantum_dir=HERE/'bosonic_gsim_replay'
    quantum_sources=json.loads((quantum_dir/'source_manifest.json').read_text())
    require(quantum_sources['commit']=='4eddbc9c838f7164520ae2ed06d1778beacd906a','quantum pin')
    require(len(quantum_sources['files'])==21,'quantum source count')
    for entry in quantum_sources['files']:
        data=(quantum_dir/'source'/entry['path']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==entry['git_blob_sha'],'quantum Git blob identity')
        require(hashlib.sha256(data).hexdigest()==entry['sha256'],'quantum source checksum')
    quantum=json.loads((quantum_dir/'replay_receipt.json').read_text())
    require(quantum['pinned_commit']==quantum_sources['commit'],'quantum receipt pin')
    require(len(quantum['replays'])==2,'quantum example count')
    for row in quantum['replays']:
        result_path=quantum_dir/(row['experiment']+'.results.json')
        require(hashlib.sha256(result_path.read_bytes()).hexdigest()==row['result_sha256'],'quantum result checksum')
        require(json.loads(result_path.read_text())==row['result'],'quantum result agreement')
        require(row['returncode']==0,'stored quantum replay completion')
        result=row['result']
        if row['experiment']=='fig10_nilpotent_phase':
            metrics=[result[part][key] for part in ['single_mode','two_mode']
                     for key in ['max_module_grid_error','max_grid_refinement_gap']]
        else:
            require(row['experiment']=='fig8_beyond_gaussian','quantum example identity')
            metrics=[result[key] for key in ['hom_max_analytic_error','hom_max_fock_error',
                                           'random_interferometer_max_fock_error']]
        require(all(math.isfinite(v)and 0<=v<1e-12 for v in metrics),'stored quantum residuals')
    report={'status':'passed','data_and_exact_replays':runs,'method_source_records':len(catalog['sources']),
            'distinct_primary_url_strings':url_count,'dataset_asset_groups':12,
            'stored_ring_probe_consistency':'passed','new_ring_tracking_run':False,
            'quantum_source_files_hash_checked':21,'stored_quantum_examples_consistency':'passed',
            'new_quantum_simulation_run':False,
            'published_speedups_reproduced':False,
            'scope':'Source/data consistency, a formal polynomial recurrence and stored probe arithmetic; no new tenfold or physics validation.'}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'passed','data_and_exact_replays':len(runs),
                     'stored_ring_probe_consistency':'passed'},indent=2))


if __name__=='__main__':
    main()
