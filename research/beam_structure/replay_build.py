"""Offline verification of the structural/ring build; never starts new tracking."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
    runs=[]
    with tempfile.TemporaryDirectory(prefix='beam-structure-replay-')as directory:
        temp=Path(directory)
        commands=[
            [sys.executable,'-B',str(HERE/'emittance/replay.py'),'--output',str(temp/'emittance.json')],
            [sys.executable,'-B','-S',str(HERE/'observables/run_observables.py'),'--output',str(temp/'observables')],
            [sys.executable,'-B','-m','unittest','discover','-s',str(HERE.parent/'beam_ring/acquisition'),'-p','test_*.py'],
            [sys.executable,'-B','-S','-m','unittest','discover','-s',str(HERE.parent/'beam_ring/certificates'),'-p','test_*.py'],
            [sys.executable,'-B','-m','unittest','discover','-s',str(HERE.parent/'beam_ring'),'-p','test_oracle.py'],
            [sys.executable,'-B','-S',str(HERE.parent/'beam_ring/verify_pilot.py'),'--output',str(temp/'ring.json')],
        ]
        for command in commands:
            start=time.perf_counter()
            result=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True)
            if result.returncode:
                raise RuntimeError('Check failed: '+' '.join(command)+'\n'+result.stderr[-4000:])
            runs.append({'command':command,'exit_code':0,'checker_seconds':time.perf_counter()-start,
                         'stdout':result.stdout,'stderr':result.stderr})
        emittance=json.loads((temp/'emittance.json').read_text())
        ring=json.loads((temp/'ring.json').read_text())
        report={'status':'passed','exact_and_behavioral_tests':54,'runs':runs,
                'emittance':emittance,'ring_audit':ring,
                'new_particle_tracking':False,'industrial_tenfold_established':False,
                'scope':'Offline exact identities, behavior, source/label bookkeeping and retrospective data only.'}
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'passed','tests':54,'checks':len(runs),
                      'new_particle_tracking':False,'industrial_tenfold_established':False},indent=2))


if __name__=='__main__':main()
