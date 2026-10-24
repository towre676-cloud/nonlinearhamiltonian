#!/usr/bin/env python3
"""Reproducible public-lattice feasibility probe, not an optimization benchmark.

Uses Accelerator Toolbox 0.9.0. No space charge, radiation, RF or random errors.
One turn means the expanded 32-cell HMBA ring. Compares identical individual
particle labels in batched and cached single-particle execution.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import statistics
import sys
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',type=Path,help='optional isolated dependency directory')
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('public_ring_smoke.json'))
    parser.add_argument('--turns',type=int,default=128)
    parser.add_argument('--repeats',type=int,default=3)
    args=parser.parse_args()
    if args.turns<1 or args.repeats<1:
        raise ValueError('positive turns and repeats required')
    if args.runtime:
        sys.path.insert(0,str(args.runtime))
    os.environ['OMP_NUM_THREADS']='1'
    os.environ['OPENBLAS_NUM_THREADS']='1'
    import numpy as np
    import at
    if at.__version__!='0.9.0':
        raise ValueError('this probe was specified for accelerator-toolbox==0.9.0')
    source=Path(__file__).parent/'dataset_inspection/at_hmba.mat'
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    if digest!='8547502b0a4612a0e145fa6033e5ba98bb13567035fed43cadef760dae385c7b':
        raise ValueError('public lattice source mismatch')
    cell=at.Lattice.load(source)
    periodicity=int(cell.periodicity)
    ring=(cell*periodicity).disable_6d(copy=True)
    if ring.periodicity!=1 or len(ring)!=len(cell)*periodicity:
        raise ValueError('full-ring turn convention mismatch')
    # Fixed 64-point feasibility grid. This is not an accurate aperture quadrature.
    x=np.repeat(np.linspace(-.012,.012,8),8)
    y=np.tile(np.linspace(0,.006,8),8)
    inputs=np.zeros((6,len(x)),order='F')
    inputs[0]=x;inputs[2]=y
    def track(data):
        _,params,diagnostics=ring.track(np.asfortranarray(data),nturns=args.turns,
            refpts=[],losses=True,omp_num_threads=1,keep_lattice=True)
        loss=diagnostics['loss_map']
        return np.array(params['rout']),np.array(loss['islost']),np.array(loss['turn'])
    track(inputs[:,:1]) # warm kernel/cache initialization, recorded separately
    batch_times=[];single_times=[];max_error=0.
    for _ in range(args.repeats):
        start=time.perf_counter();batch=track(inputs);batch_times.append(time.perf_counter()-start)
        start=time.perf_counter();parts=[track(inputs[:,i:i+1])for i in range(len(x))]
        single_times.append(time.perf_counter()-start)
        singles=tuple(np.concatenate([p[k]for p in parts],axis=1 if k==0 else 0)for k in range(3))
        if not np.array_equal(batch[1],singles[1]) or not np.array_equal(batch[2],singles[2]):
            raise ValueError('batch/single survival labels disagree')
        finite=np.isfinite(batch[0])&np.isfinite(singles[0])
        max_error=max(max_error,float(np.max(np.abs(batch[0][finite]-singles[0][finite]),initial=0)))
        if not np.allclose(batch[0],singles[0],rtol=1e-12,atol=1e-14,equal_nan=True):
            raise ValueError('batch/single final states disagree')
    result={
        'status':'passed','scope':'public-lattice feasibility and batching probe only; no tuning gain',
        'lattice_sha256':digest,'source_cell_elements':len(cell),'source_periodicity':periodicity,
        'tracked_ring_elements':len(ring),'tracked_ring_periodicity':int(ring.periodicity),
        'ring_energy_eV':float(ring.energy),'ring_circumference_m':float(ring.get_s_pos(at.End)[0]),
        'turns':args.turns,'particles':len(x),'repeats':args.repeats,
        'survivors':int(np.sum(~batch[1])),'losses':int(np.sum(batch[1])),
        'final_state_max_batch_single_difference':max_error,
        'batch_seconds':batch_times,'cached_single_seconds':single_times,
        'batching_gain_median':statistics.median(single_times)/statistics.median(batch_times),
        'warm_initialization_excluded':True,
        'cold_import_install_and_input_generation_excluded':True,
        'physics':{'radiation':False,'rf':False,'space_charge':False,'errors':False},
        'baseline_obligation':'Compare active point selection with optimized batched/adaptive aperture search, not uncached scalar loops.',
        'versions':{n:importlib.metadata.version(n)for n in ['accelerator-toolbox','numpy','scipy','h5py']},
        'python':platform.python_version(),
    }
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
