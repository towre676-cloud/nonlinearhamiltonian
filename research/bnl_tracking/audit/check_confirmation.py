"""Independent confirmation gate/cost audit, without new tracking."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import numpy as np


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root=args.campaign
    protocol=json.loads((root/'protocol.json').read_text())
    recorded=json.loads((root/'confirmation_audit.json').read_text())
    for original,expected in protocol['source_hashes'].items():
        data=(root/'source_snapshot'/Path(original).name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==expected
    r40=np.load(root/'native40/run_0.npz',allow_pickle=False)
    r80=np.load(root/'native80/run_0.npz',allow_pickle=False)
    agree=r40['islost']==r80['islost'];core=np.array(protocol['core_indices'])
    assert protocol['core_indices']==list(range(16))
    build=json.loads((root/'source_snapshot/plugin_build_timing.json').read_text())
    buildtime=float(build.get('seconds',build.get('elapsed_seconds',build.get('build_seconds'))))
    results=[];points=0
    for method in protocol['methods']:
        folder=root/method['id'];saved=json.loads((folder/'result.json').read_text())
        assert saved['native_steps']==method['native_steps']and saved['sext_steps']==method['sext_steps']
        times=[];fallback=[];first=None
        for rep in range(method['repeats']):
            cost=json.loads((folder/f'cost_{rep}.json').read_text())
            times.append(cost['seconds']);fallback.append(cost['fallback_particles'])
            points+=64+cost['fallback_particles']
            with np.load(folder/f'run_{rep}.npz',allow_pickle=False)as z:
                data={k:np.array(z[k])for k in z.files}
            if first is None:first=data
            else:
                assert np.array_equal(first['islost'],data['islost'])
                assert np.array_equal(first['rout'],data['rout'],equal_nan=True)
        assert times==saved['tracking_seconds']and fallback==saved['fallback_counts']
        median=statistics.median(times);assert median==saved['median_tracking_seconds']
        errors=np.flatnonzero(agree&(first['islost']!=r80['islost'])).tolist()
        valid=not np.any(first['islost'][core])and not np.any(r80['islost'][core])
        pos=float(np.max(abs(first['rout'][[0,2]][:,core]-r80['rout'][[0,2]][:,core])))if valid else None
        mom=float(np.max(abs(first['rout'][[1,3]][:,core]-r80['rout'][[1,3]][:,core])))if valid else None
        qualified=valid and not errors and pos<=1e-6 and mom<=1e-6
        setup=sum(saved[k]for k in ['native_construction_seconds','compile_seconds','warmup_seconds'])
        plugin=buildtime if method['id'].startswith('fused')else 0.
        elapsed=median+setup+plugin
        original=next(row for row in recorded['results']if row['method']==method['id'])
        assert original['qualified']==bool(qualified)and original['label_error_indices']==errors
        assert math.isclose(original['first_workload_seconds'],elapsed,rel_tol=1e-14)
        results.append({'method':method['id'],'qualified':bool(qualified),
            'label_error_indices':errors,'core_position_max_abs_m':pos,
            'core_momentum_max_abs_normalized':mom,'median_tracking_seconds':median,
            'setup_seconds':setup,'plugin_build_seconds':plugin,'first_workload_seconds':elapsed,
            'fallback_particles_by_repeat':fallback})
    existing=[row for row in results if row['qualified']and row['method'].startswith(('native','analytic'))]
    best=min(existing,key=lambda row:row['first_workload_seconds'])
    refcost=sum(sum(json.loads((root/name/'result.json').read_text())['tracking_seconds'])
                +next(row['setup_seconds']for row in results if row['method']==name)
                for name in ['native40','native80'])
    for row in results:
        row['gain_vs_strongest_qualified_existing_first_workload']=best['first_workload_seconds']/row['first_workload_seconds']if row['qualified']else None
        saving=best['median_tracking_seconds']-row['median_tracking_seconds']
        row['conditional_break_even_distinct_equivalent_cost_queries']=None if not row['qualified']or saving<=0 else max(1,math.ceil((refcost+row['setup_seconds']+row['plugin_build_seconds']-best['setup_seconds'])/saving))
    report={'status':'passed','source_hashes_verified':len(protocol['source_hashes']),
        'methods_checked':len(results),'reference_agreement_points':int(agree.sum()),
        'reference_unresolved_indices':np.flatnonzero(~agree).tolist(),
        'physical_point_evaluations_with_guard_reruns':points,
        'strongest_qualified_existing':best['method'],'reference_generation_seconds':refcost,
        'plugin_build_seconds':buildtime,'results':results,
        'limitations':['One historical ideal model at fixed momentum, not the present operating BNL machine.',
            '64 new launch points, one 256-turn horizon; 40/80 agreement is empirical resolution agreement, not a physical truth proof.',
            'Timing order fixed; some baselines have one timing sample and host is shared; no industrial runtime guarantee.',
            'No end-to-end optimizer comparison or current machine controls.',
            'Amortization requires distinct future queries that also qualify; repeats of identical inputs are cache-equivalent.'],
        'industrial_tenfold_established':False}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='results'},indent=2))
    print(json.dumps([r for r in results if r['qualified']],indent=2))


if __name__=='__main__':main()
