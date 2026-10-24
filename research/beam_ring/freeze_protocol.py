"""Freeze a small public-ring pilot before any survival labels are generated."""
from pathlib import Path
import argparse
import importlib.metadata
import json
import platform
import time
from datetime import datetime, timezone
from oracle import FAMILIES, LATTICE_SHA256, base_ring, digest, load_runtime, set_strengths


def grids(np, nx, ny, ndp):
    x = np.linspace(-0.012, 0.012, nx)
    y = np.linspace(0, 0.006, ny)
    coordinates = [[float(a), 0., float(b), 0., 0., 0.] for a in x for b in y]
    adjacency = [[] for _ in coordinates]
    for i in range(nx):
        for j in range(ny):
            k = i * ny + j
            adjacency[k] = [a * ny + b for a, b in
                            [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
                            if 0 <= a < nx and 0 <= b < ny]
    da = {'name': 'entrance_xy_connected_grid', 'coordinates': coordinates,
          'origin': (nx//2)*ny, 'adjacency': adjacency,
          'weights': [1] * len(coordinates), 'shape': [nx, ny],
          'units': ['x:m', 'px:normalized', 'y:m', 'py:normalized', 'delta:relative', 'ct:m']}
    dp = np.linspace(-.04, .04, ndp)
    ma = {'name': 'entrance_delta_connected_grid',
          'coordinates': [[1e-6,0.,1e-6,0.,float(p),0.] for p in dp],
          'origin': ndp//2, 'weights': [1]*ndp, 'shape': [ndp],
          'adjacency': [[j for j in [i-1,i+1] if 0<=j<ndp] for i in range(ndp)],
          'units': da['units']}
    return [da, ma]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',type=Path)
    p.add_argument('--output',type=Path,default=Path(__file__).with_name('protocol.json'))
    args=p.parse_args()
    if args.output.exists():
        raise FileExistsError('protocol is frozen; choose a new path for a new experiment')
    started=time.perf_counter()
    at,np=load_runtime(args.runtime)
    ring=base_ring()
    strengths=[float(next(e for e in ring if e.FamName==f).PolynomB[2]) for f in FAMILIES]
    baseline=np.array(ring.get_chrom())
    response=np.empty((2,6)); step=.1
    for k in range(6):
        a=strengths.copy();b=strengths.copy();a[k]+=step;b[k]-=step
        set_strengths(ring,a);ca=np.array(ring.get_chrom())
        set_strengths(ring,b);cb=np.array(ring.get_chrom())
        response[:,k]=(ca-cb)/(2*step)
    _,singular,vh=np.linalg.svd(response,full_matrices=True)
    if singular[-1]<1e-5:
        raise ValueError('chromaticity response is not rank two')
    basis=vh[2:].T
    for j in range(4):
        if basis[np.argmax(abs(basis[:,j])),j]<0:basis[:,j]*=-1
    scale=8.0
    controls=[np.zeros(4)]
    for j in range(4):
        for sign in [-1,1]:
            u=np.zeros(4);u[j]=sign;controls.append(u)
    designs=[]
    for k,u in enumerate(controls):
        values=np.array(strengths)+scale*basis@u
        set_strengths(ring,values)
        chrom=np.array(ring.get_chrom())
        designs.append({'id':f'design_{k:02d}','controls':u.tolist(),
                        'strengths':values.tolist(),'chromaticity':chrom.tolist(),
                        'chromaticity_deviation':float(np.max(abs(chrom-baseline)))})
    # Validate corners as well as selected designs; this is sampled, not uniform proof.
    corner_max=0.
    import itertools
    for u in itertools.product([-1,1],repeat=4):
        set_strengths(ring,np.array(strengths)+scale*basis@np.array(u))
        corner_max=max(corner_max,float(np.max(abs(np.array(ring.get_chrom())-baseline))))
    value={'schema':'public-ring-pilot-v1','frozen_utc':datetime.now(timezone.utc).isoformat(),
           'lattice_sha256':LATTICE_SHA256,'full_ring_elements':3872,'full_ring_periodicity':1,
           'physics':{'energy_eV':6e9,'rf':False,'radiation':False,'space_charge':False,
                      'magnet_errors':False,'mechanical_apertures_added':False,
                      'loss_rule':'PyAT native element/aperture/numerical loss checks'},
           'control_definition':{'families':FAMILIES,'coefficient':'PolynomB[2], normalized m^-3',
                 'baseline':strengths,'response_step':step,'chromaticity_response':response.tolist(),
                 'singular_values':singular.tolist(),'nullspace_basis':basis.tolist(),
                 'scale':scale,'mirror_symmetry':'Six independently named families; mirror symmetry may be broken.',
                 'corner_chromaticity_max_deviation':corner_max,
                 'preservation_scope':'Selected designs and 16 corners numerically checked; no uniform interval theorem.'},
           'designs':designs,
           'stages':{'learning':{'turns':64,'launch_sets':grids(np,9,5,17)},
                     'validation':{'turns':256,'launch_sets':grids(np,13,7,25)}},
           'objective':'Origin-connected, equally weighted finite-grid survival fraction; maximize both components.',
           'objective_limits':'Not continuous dynamic aperture, true longitudinally resolved momentum acceptance, or infinite-time stability.',
           'pilot':{'seed':20261024,'initial_points':96,'rounds':2,'batch_points':24,'final_designs':2},
           'quality':'Pilot reports validation objectives and regret; no success threshold or tenfold claim.',
           'preparation_seconds':time.perf_counter()-started,
           'versions':{n:importlib.metadata.version(n)for n in ['accelerator-toolbox','numpy','scipy']},
           'python':platform.python_version()}
    if max(corner_max,max(d['chromaticity_deviation']for d in designs))>1e-4:
        raise ValueError('sampled chromaticity preservation failed')
    args.output.write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({'protocol_sha256':digest(value),'designs':len(designs),
                      'learning_points_per_design':62,'validation_points_per_design':116,
                      'corner_chromaticity_max_deviation':corner_max,
                      'preparation_seconds':value['preparation_seconds']}))


if __name__=='__main__':main()
