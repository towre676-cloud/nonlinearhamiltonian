"""Replay the frozen 15-method confirmation in a new output directory.

Install pinned dependencies and build the local kernel first. No beam controls
or remote services are contacted. Existing output directories are rejected.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',type=Path,help='isolated pip --target dependency directory')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--build-receipt',type=Path,required=True,
                   help='Fresh receipt from build_kernel.py; charges this machine\'s build time.')
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh directory; recorded results are immutable.')
    if hashlib.sha256((HERE/'nsls2cb65pm.lte').read_bytes()).hexdigest()!='cbe4cbdc19ddec39e2e999c5337bf7cde93113570fd0639ac1e03007aa8355cb':
        raise ValueError('model identity mismatch')
    if args.runtime:sys.path.insert(0,str(args.runtime.resolve()))
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
        os.environ[key]='1'
    # Load the selected installation before preserved acquisition helpers can
    # prepend their historical runtime path.
    import at
    selected_root=args.runtime.resolve()if args.runtime else Path(sys.prefix).resolve()
    if not Path(at.__file__).resolve().is_relative_to(selected_root):
        raise ValueError('PyAT was not loaded from the requested runtime or active environment')
    build=json.loads(args.build_receipt.read_text())
    if build['kernel_source_sha256']!=hashlib.sha256((HERE/'engine/FixedDeltaBlockPass.c').read_bytes()).hexdigest():
        raise ValueError('kernel build/source identity mismatch')
    if build['binary_sha256']!=hashlib.sha256(Path(build['binary_path']).read_bytes()).hexdigest():
        raise ValueError('kernel binary identity mismatch')
    sys.path.insert(0,str(HERE/'benchmarks'))
    selected_search_path=list(sys.path)
    import qualification_bnl as q
    sys.path[:]=selected_search_path
    import confirmation_bnl as c
    if q.at.__version__!='0.9.0':raise ValueError('accelerator-toolbox==0.9.0 required')
    # Explicitly override historical acquisition paths without changing the
    # preserved benchmark sources or their numerical/gating logic.
    q.SOURCE=HERE/'nsls2cb65pm.lte'
    q.BASE=HERE/'benchmarks'
    c.BASE=HERE/'benchmarks'
    c.OUT=args.output.resolve()
    with tempfile.TemporaryDirectory(prefix='bnl-engine-replay-')as directory:
        started=time.perf_counter()
        engine=Path(directory)/'engine';shutil.copytree(HERE/'engine',engine)
        for name in ['plugin_build_timing.json','fused_build_receipt.json']:
            (engine/name).write_text(json.dumps(build,indent=2)+'\n')
        q.COMPILER=engine/'compiler.py';c.LAB=engine
        preparation_seconds=time.perf_counter()-started
        c.main()
        (c.OUT/'launcher_costs.json').write_text(json.dumps({
            'working_copy_preparation_seconds':preparation_seconds,
            'note':'Separate launcher preparation; source tests and dependency installation excluded.'},indent=2)+'\n')


if __name__=='__main__':main()
