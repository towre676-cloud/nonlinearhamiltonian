"""Independently replay the recorded numerical qualification; no new tracking."""
from pathlib import Path
from io import BytesIO
import argparse
import hashlib
import json
import math
import statistics
import zipfile
import numpy as np

HERE=Path(__file__).resolve().parent
MODEL_SHA='cbe4cbdc19ddec39e2e999c5337bf7cde93113570fd0639ac1e03007aa8355cb'


def require(condition,message):
    if not condition:raise ValueError(message)


def audit(archive,manifest,build_seconds):
    require(hashlib.sha256((HERE/'nsls2cb65pm.lte').read_bytes()).hexdigest()==MODEL_SHA,'model identity')
    with zipfile.ZipFile(archive)as z:
        names=z.namelist()
        require(len(names)==len(set(names)),'duplicate archive members')
        require(set(names)==set(manifest['files']),'archive member set')
        for name in names:
            require(not name.startswith('/')and '..'not in Path(name).parts,'archive path')
            require(hashlib.sha256(z.read(name)).hexdigest()==manifest['files'][name]['sha256'],
                    'recorded file checksum: '+name)
        def read(name):return json.loads(z.read(name))
        def arrays(name):
            with np.load(BytesIO(z.read(name)),allow_pickle=False)as data:
                require(set(data.files)=={'rout','islost','turn','elem'},'raw array fields')
                return {k:np.array(data[k])for k in data.files}
        p=read('confirmation/protocol.json')
        require(p['schema']=='bnl-independent-confirmation-v1','protocol schema')
        require(p['source_sha256']==MODEL_SHA,'protocol/model identity')
        require(p['turns']==256 and p['seed']==20261024,'frozen confirmation identity')
        require(p['gate']=={'label_errors_allowed_where_native40_and80_agree':0,
                           'core_position_max_abs_m':1e-6,'core_momentum_max_abs_normalized':1e-6},
                'frozen quality gate')
        require(np.asarray(p['launches']).shape==(6,64),'launch shape')
        for original,sha in p['source_hashes'].items():
            name='confirmation/source_snapshot/'+Path(original).name
            require(hashlib.sha256(z.read(name)).hexdigest()==sha,'executed source snapshot')
        methods=p['methods']
        require(len(methods)==15 and len({r['id']for r in methods})==15,'predeclared methods')
        reference40=arrays('confirmation/native40/run_0.npz')
        reference80=arrays('confirmation/native80/run_0.npz')
        agreement=reference40['islost']==reference80['islost']
        core=np.asarray(p['core_indices'])
        require(p['core_indices']==list(range(16)),'frozen core indices')
        build_snapshot=read('confirmation/source_snapshot/plugin_build_timing.json')
        require(build_seconds==build_snapshot['build_seconds'],'kernel build cost binding')
        rows=[];reference_cost=0.;total_points=0;campaign_cost=build_seconds
        for method in methods:
            name=method['id'];folder='confirmation/'+name+'/'
            recorded=read(folder+'result.json');all_arrays=[]
            require(recorded['method']==name,'method identity')
            require(recorded['native_steps']==method['native_steps']and recorded['sext_steps']==method['sext_steps'],
                    'integration policy binding')
            times=recorded['tracking_seconds']
            require(len(times)==method['repeats']and all(math.isfinite(v)and v>0 for v in times),'timing repeats')
            for rep in range(method['repeats']):
                d=arrays(folder+f'run_{rep}.npz');all_arrays.append(d)
                require(d['rout'].shape==(6,64)and d['islost'].shape==(64,), 'output dimensions')
                require(d['islost'].dtype.kind=='b','loss label type')
                require(np.all(np.isfinite(d['rout'][:,~d['islost']])),'finite surviving outputs')
                require(np.all((d['turn'][d['islost']]>=0)&(d['turn'][d['islost']]<256)),'loss turn')
                cost=read(folder+f'cost_{rep}.json')
                require(math.isclose(cost['seconds'],times[rep],rel_tol=1e-12,abs_tol=1e-12),'call timer')
                require(type(cost['fallback_particles'])is int and 0<=cost['fallback_particles']<=64,'fallback count')
                require(cost['fallback_particles']==recorded['fallback_counts'][rep],'fallback ledger binding')
                total_points+=64+cost['fallback_particles']
            d=all_arrays[0]
            for other in all_arrays[1:]:
                require(np.array_equal(d['islost'],other['islost']),'repeat label determinism')
                require(np.array_equal(d['rout'],other['rout'],equal_nan=True),'repeat state determinism')
            errors=np.flatnonzero(agreement&(d['islost']!=reference80['islost']))
            valid=not np.any(d['islost'][core])and not np.any(reference80['islost'][core])
            position=float(np.max(abs(d['rout'][[0,2]][:,core]-reference80['rout'][[0,2]][:,core])))if valid else None
            momentum=float(np.max(abs(d['rout'][[1,3]][:,core]-reference80['rout'][[1,3]][:,core])))if valid else None
            qualified=valid and not len(errors)and position<=1e-6 and momentum<=1e-6
            setup=recorded['native_construction_seconds']+recorded['compile_seconds']+recorded['warmup_seconds']
            require(math.isfinite(setup)and setup>=0,'construction cost')
            kernel_build=build_seconds if name.startswith('fused')else 0.
            median=statistics.median(times)
            campaign_cost+=sum(times)+setup
            require(median==recorded['median_tracking_seconds'],'median timer binding')
            row={'method':name,'qualified':bool(qualified),'label_error_indices':errors.tolist(),
                 'core_position_max_abs_m':position,'core_momentum_max_abs_normalized':momentum,
                 'median_tracking_with_fallback_seconds':median,'construction_and_warmup_seconds':setup,
                 'plugin_build_seconds':kernel_build,'first_workload_seconds':median+setup+kernel_build,
                 'fallback_counts':recorded['fallback_counts'],'elements':recorded['elements']}
            if name in ['native40','native80']:reference_cost+=sum(times)+setup
            rows.append(row)
        qualified_baselines=[r for r in rows if r['qualified']and r['method'].startswith(('native','analytic'))]
        require(qualified_baselines,'no qualified native baseline')
        best=min(qualified_baselines,key=lambda r:r['first_workload_seconds'])
        for row in rows:
            row['gain_vs_best_qualified_existing_first_workload']=best['first_workload_seconds']/row['first_workload_seconds']if row['qualified']else None
            saving=best['median_tracking_with_fallback_seconds']-row['median_tracking_with_fallback_seconds']
            row['conditional_reference_only_break_even_new_equal_cost_batches']=None if not row['qualified']or saving<=0 else max(1,math.ceil((reference_cost+row['construction_and_warmup_seconds']+row['plugin_build_seconds']-best['construction_and_warmup_seconds'])/saving))
            row['conditional_confirmation_campaign_break_even_additional_equal_cost_batches']=None if not row['qualified']or saving<=0 else max(1,math.ceil((campaign_cost-best['construction_and_warmup_seconds'])/saving))
        return {'status':'passed','confirmation_protocol_sha256':hashlib.sha256(z.read('confirmation/protocol.json')).hexdigest(),
                'checked_archive_files':len(names),'reference_agreement_points':int(agreement.sum()),
                'reference_unresolved_indices':np.flatnonzero(~agreement).tolist(),
                'confirmation_point_evaluations_including_guard_reruns':total_points,
                'best_qualified_existing_method':best['method'],'reference_generation_seconds':reference_cost,
                'measured_confirmation_campaign_seconds':campaign_cost,
                'amortization_scope':'Reference-only threshold excludes candidate search. Campaign threshold charges all 15 methods and repeats, each setup/warmup and one build; excludes earlier exploration, package/interpreter startup and reporting. Additional distinct equal-cost queries, reusing the qualified configuration; no future qualification or generalization guarantee.',
                'rows':rows,'industrial_tuning_tenfold_established':False,
                'scope':'One public historical ideal BNL model, fixed delta0, transverse outputs. Finite empirical gate, not universal or full6D equivalence. Qualification and plugin build are explicit costs.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',type=Path,default=HERE/'results/recorded_campaigns.zip')
    p.add_argument('--manifest',type=Path,default=HERE/'results/RECORDED_MANIFEST.json')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    build=json.loads((HERE/'engine/plugin_build_timing.json').read_text())
    # The receipt's measured elapsed field is checked explicitly at packaging.
    build_seconds=build['build_seconds']
    result=audit(args.archive,json.loads(args.manifest.read_text()),build_seconds)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='rows'},indent=2))


if __name__=='__main__':main()
