"""Build the local extension in an explicit target or active virtual environment."""
from pathlib import Path
import argparse
import json
import sys
import time

HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',type=Path)
    p.add_argument('--receipt',type=Path,required=True)
    args=p.parse_args()
    if args.runtime:sys.path.insert(0,str(args.runtime.resolve()))
    import at
    if at.__version__!='0.9.0':raise ValueError('accelerator-toolbox==0.9.0 required')
    if args.runtime is None and sys.prefix==sys.base_prefix:
        raise ValueError('Use an active virtual environment or an explicit --runtime target.')
    runtime=args.runtime or Path(at.__file__).resolve().parent.parent
    sys.path.insert(0,str(HERE/'engine'))
    from build_fused import build
    started=time.perf_counter();result=build(HERE/'engine/vendor/at0_9_0',runtime)
    result['build_seconds']=time.perf_counter()-started
    args.receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
