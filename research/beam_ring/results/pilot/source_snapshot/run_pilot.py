"""Run a small live physical pilot. No paper-speedup reproduction is claimed."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from oracle import RingOracle, connected_fraction, digest, load_runtime

HERE=Path(__file__).resolve().parent


def all_requests(protocol,stage='learning',designs=None):
    if designs is None:designs=range(len(protocol['designs']))
    return [(o,int(d),l)for d in designs
            for o,g in enumerate(protocol['stages'][stage]['launch_sets'])
            for l in range(len(g['coordinates']))]


def scores(oracle,designs):
    grids=oracle.stage_spec['launch_sets']
    result=[]
    for d in designs:
        row=[]
        for o,g in enumerate(grids):
            labels=[oracle.cache.get((o,d,l),{}).get('survived',False)
                    for l in range(len(g['coordinates']))]
            row.append(connected_fraction(labels,g))
        result.append(row)
    return result


def choose_final(values,count):
    # Frozen equal-weight scalarization, deterministic index tie-break.
    return sorted(range(len(values)),key=lambda i:(-sum(values[i]),i))[:count]


def frontier_search(oracle):
    """Exact origin-component traversal; never infer loss behind a boundary."""
    for o,g in enumerate(oracle.stage_spec['launch_sets']):
        for d in range(len(oracle.protocol['designs'])):
            pending={g['origin']};visited=set()
            while pending:
                nodes=sorted(pending-visited)
                if not nodes:break
                visited.update(nodes);pending=set()
                rows=oracle.query([(o,d,l)for l in nodes],purpose='connected_frontier')
                for l,row in zip(nodes,rows):
                    if row['survived']:pending.update(set(g['adjacency'][l])-visited)


def write_certificates(oracle,out):
    from certificates.grid_bounds import make_manifest,certify,check_certificate
    receipts=[]
    for o,g in enumerate(oracle.stage_spec['launch_sets']):
        cells=[f'cell_{l:04d}'for l in range(len(g['coordinates']))]
        designs=[x['id']for x in oracle.protocol['designs']]
        manifest=make_manifest(cells,{cells[i]:[cells[j]for j in ns]
                                      for i,ns in enumerate(g['adjacency'])},
                               dict(zip(cells,g['weights'])),cells[g['origin']],
                               designs,[oracle.turns],
                               physics={'protocol_sha256':oracle.protocol_sha256,
                                        'stage':oracle.stage,'objective':g['name'],
                                        'label_scope':'Observed finite-horizon PyAT labels; not continuum proof.'})
        events=[{'design':designs[e['design']],'cell':cells[e['launch']],
                 'horizon':oracle.turns,'label':int(e['survived']),
                 'source':digest(e)}for e in oracle.events if e['objective']==o]
        cert=certify(manifest,events)
        check_certificate(manifest,events,cert)
        record={'manifest':manifest,'events':events,'certificate':cert}
        name=f'objective_{o:02d}_certificate.json'
        (out/name).write_text(json.dumps(record,indent=2)+'\n')
        receipts.append({'objective':o,'certificate':name,'checker':'passed',
                         'observed_labels':len(events)})
    return receipts


def surrogate_run(protocol,oracle,method,seed,np):
    from acquisition.finite_meanbax import FiniteMeanBAX,SurvivalMLP,feature_table
    grids=oracle.stage_spec['launch_sets'];D=len(protocol['designs'])
    features=[];models=[];masks=[]
    for o,g in enumerate(grids):
        coords=np.array(g['coordinates'],float)
        columns=coords[:,[0,2]]/[.012,.006] if o==0 else coords[:,[4]]/.04
        features.append(feature_table([d['controls']for d in protocol['designs']],columns))
        models.append(SurvivalMLP(seed=seed+o,max_iter=150))
        masks.append(np.zeros((D,len(coords)),dtype=bool))
    callbacks=[lambda labels,g=g:connected_fraction(labels.tolist(),g)for g in grids]
    selector=FiniteMeanBAX(weights=[g['weights']for g in grids],
                          batch_size=protocol['pilot']['batch_points'],seed=seed,
                          objective_callbacks=callbacks)
    rng=np.random.default_rng(seed)
    universe=all_requests(protocol)
    selected=[universe[i]for i in rng.choice(len(universe),protocol['pilot']['initial_points'],replace=False)]
    oracle.query(selected,purpose='initial_data')
    logs=[]
    for iteration in range(protocol['pilot']['rounds']+1):
        predictions=[];fit=[]
        for o,g in enumerate(grids):
            entries=[e for e in oracle.events if e['objective']==o]
            X=np.array([features[o][e['design'],e['launch']]for e in entries])
            y=np.array([e['survival_fraction']for e in entries])
            models[o].fit(X,y)
            predictions.append(models[o].predict(features[o].reshape(-1,features[o].shape[-1])).reshape(D,-1))
            for e in entries:
                masks[o][e['design'],e['launch']]=True
                # Exact observed pass/fail overrides surrogate classification.
                predictions[o][e['design'],e['launch']]=float(e['survived'])
            fit.append(models[o].fit_receipt)
        estimates=selector.estimates(predictions)
        log={'iteration':iteration,'fit':fit,'estimated_objectives':estimates.tolist()}
        if iteration<protocol['pilot']['rounds']:
            if method=='finite_meanbax':
                selected=selector.select(predictions,masks)
                log['selection']=selector.last_selection
            else:
                available=[q for q in universe if q not in oracle.cache]
                selected=[available[i]for i in rng.choice(len(available),min(len(available),
                           protocol['pilot']['batch_points']),replace=False)]
                log['selection']={'reason':'uniform_unobserved_points','queries':[list(q)for q in selected]}
            oracle.query(selected,purpose=f'round_{iteration+1}')
        logs.append(log)
    return estimates.tolist(),logs


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',type=Path)
    p.add_argument('--protocol',type=Path,default=HERE/'protocol.json')
    p.add_argument('--output',type=Path,default=HERE/'results/pilot')
    p.add_argument('--methods',nargs='+',default=['full_grid','connected_frontier','uniform_surrogate','finite_meanbax'],
                   choices=['full_grid','connected_frontier','uniform_surrogate','finite_meanbax'])
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('never overwrite a completed/partial campaign')
    args.output.mkdir(parents=True)
    at,np=load_runtime(args.runtime)
    protocol=json.loads(args.protocol.read_text())
    source_files=[HERE/'oracle.py',Path(__file__),HERE/'acquisition/finite_meanbax.py',
                  HERE/'certificates/grid_bounds.py']
    frozen={'schema':'public-ring-live-pilot-execution-v1','frozen_utc':datetime.now(timezone.utc).isoformat(),
            'protocol_sha256':digest(protocol),'methods':args.methods,
            'selection':'Two highest equal-weight sums of normalized grid objectives; index tie-break.',
            'seed':protocol['pilot']['seed'],'shared_data':'No cross-method query cache or simulator-label reuse.',
            'validation_access':'Each optimizer receives only learning launches/horizon; validation after selection.',
            'scope':'Small finite design-set pilot, no error realizations, no industrial speedup contract.',
            'sources':{str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest()for f in source_files}}
    (args.output/'execution_frozen.json').write_text(json.dumps(frozen,indent=2)+'\n')
    summary={'status':'running','protocol_sha256':digest(protocol),'results':[],
             'tenfold_established':False,'scope':frozen['scope']}
    for method in args.methods:
        print('START '+method,flush=True)
        destination=args.output/method;destination.mkdir()
        start=time.perf_counter()
        oracle=RingOracle(protocol,stage='learning')
        if method=='full_grid':
            oracle.query(all_requests(protocol),purpose='exhaustive_learning_grid')
            estimated=scores(oracle,range(len(protocol['designs'])));details=[]
        elif method=='connected_frontier':
            frontier_search(oracle)
            estimated=scores(oracle,range(len(protocol['designs'])));details=[]
        else:
            estimated,details=surrogate_run(protocol,oracle,method,protocol['pilot']['seed'],np)
        chosen=choose_final(estimated,protocol['pilot']['final_designs'])
        selected_utc=datetime.now(timezone.utc).isoformat()
        selection={'method':method,'designs':chosen,'estimated_objectives':estimated,
                   'selected_utc':selected_utc,'details':details}
        (destination/'selection_locked.json').write_text(json.dumps(selection,indent=2)+'\n')
        learning_seconds=time.perf_counter()-start
        validation=RingOracle(protocol,stage='validation')
        validation.query(all_requests(protocol,'validation',chosen),purpose='independent_final_grid')
        validated=scores(validation,chosen)
        validation_ledger=validation.ledger()
        certificate_start=time.perf_counter()
        certs=write_certificates(oracle,destination)
        certificate_seconds=time.perf_counter()-certificate_start
        total=time.perf_counter()-start
        for label,obj in [('learning',oracle),('validation',validation)]:
            (destination/(label+'_events.json')).write_text(json.dumps(obj.events,indent=2)+'\n')
        record={'method':method,'selected_designs':chosen,'estimated_learning_objectives':estimated,
                'validated_objectives':validated,'learning_ledger':oracle.ledger(),
                'validation_ledger':validation_ledger,'learning_elapsed_seconds':learning_seconds,
                'certificate_seconds':certificate_seconds,'workflow_elapsed_seconds':total,
                'charged_protocol_preparation_seconds':protocol['preparation_seconds'],
                'charged_total_seconds':total+protocol['preparation_seconds'],
                'learning_certificates':certs,'selected_utc':selected_utc,
                'scope':'Live finite-set pilot; elapsed includes training/acquisition/final tracking/checkers, excludes installation and source-code development.'}
        (destination/'result.json').write_text(json.dumps(record,indent=2)+'\n')
        summary['results'].append(record)
        (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps({'method':method,'selected':chosen,'validation':validated,
                          'learning_queries':len(oracle.events),'final_queries':len(validation.events),
                          'charged_total_seconds':record['charged_total_seconds']}),flush=True)
    summary['status']='passed'
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('COMPLETE',flush=True)


if __name__=='__main__':main()
