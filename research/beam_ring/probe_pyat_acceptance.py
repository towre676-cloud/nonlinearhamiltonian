"""Exercise the installed production recursive API; its metric differs from the pilot."""
from pathlib import Path
import argparse
import hashlib
import inspect
import json
import time
from oracle import base_ring,load_runtime,LATTICE_SHA256


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',type=Path)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();at,np=load_runtime(args.runtime)
    start=time.perf_counter();ring=base_ring()
    construction=time.perf_counter()-start
    source=inspect.getsourcefile(at.get_acceptance)
    start=time.perf_counter()
    boundary,survived,tracked=ring.get_acceptance(('x','y'),(9,5),(.012,.006),
        nturns=64,offset=np.zeros(6),grid_mode=at.GridMode.RECURSIVE,
        use_mp=False,shift_zero=0.,omp_num_threads=1)
    elapsed=time.perf_counter()-start
    value={'status':'passed','accelerator_toolbox':at.__version__,
           'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),
           'lattice_sha256':LATTICE_SHA256,'construction_seconds':construction,
           'api_seconds':elapsed,'full_ring_elements':len(ring),'turns':64,
           'planes':['x','y'],'npoints':[9,5],'amplitudes_m':[.012,.006],
           'mode':'GridMode.RECURSIVE','use_mp':False,'shift_zero':0,
           'boundary':np.asarray(boundary).tolist(),'survived':np.asarray(survived).tolist(),
           'reported_tracked_coordinates':np.asarray(tracked).tolist(),
           'scope':'Production API feasibility only. Radial recursive boundary is a different metric from connected Cartesian grid; no matched-score speedup ratio.'}
    args.output.write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ['boundary','survived','reported_tracked_coordinates']},indent=2))


if __name__=='__main__':main()
