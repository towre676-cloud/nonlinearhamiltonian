"""Compile the optional local PyAT extension; never replace an upstream kernel."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sysconfig
import numpy as np


def build(source_root, runtime):
    here=Path(__file__).resolve().parent
    source_root=Path(source_root)
    target=Path(runtime)/'at/integrators'/('FixedDeltaBlockPass'+sysconfig.get_config_var('EXT_SUFFIX'))
    command=['gcc','-shared','-fPIC','-O3','-DPYAT',
             '-I'+sysconfig.get_path('include'),'-I'+np.get_include(),
             '-I'+str(source_root/'atintegrators'),
             str(here/'FixedDeltaBlockPass.c'),'-o',str(target)]
    result=subprocess.run(command,capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stderr)
    return {'status':'built','command':command,'compiler_stderr':result.stderr,
            'kernel_source_sha256':hashlib.sha256((here/'FixedDeltaBlockPass.c').read_bytes()).hexdigest(),
            'binary_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
            'binary_path':str(target),'fast_math':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--runtime',type=Path,required=True)
    p.add_argument('--receipt',type=Path,required=True)
    a=p.parse_args();r=build(a.source_root,a.runtime);a.receipt.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
