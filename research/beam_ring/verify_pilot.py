"""Offline audit of finite-grid decisions, label binding and campaign accounting.

This checks implications of the observed numerical labels, not their physical
truth. It never substitutes a surrogate prediction for a tracked observation.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import math
from oracle import LATTICE_SHA256, connected_fraction, digest
from certificates.grid_bounds import check_certificate

HERE=Path(__file__).resolve().parent


def require(condition,message):
    if not condition:raise ValueError(message)


def certificate_binding(record,protocol,objective):
    g=protocol['stages']['learning']['launch_sets'][objective]
    cells=[f'cell_{i:04d}'for i in range(len(g['coordinates']))]
    m=record['manifest']
    require(m['cells']==cells,'certificate grid cells')
    require(m['adjacency']=={cells[i]:[cells[j]for j in ns]
                            for i,ns in enumerate(g['adjacency'])},'certificate grid adjacency')
    require(m['weights']==dict(zip(cells,[str(Fraction(v))for v in g['weights']])),
            'certificate objective weights')
    require(m['origin']==cells[g['origin']],'certificate grid origin')
    require(m['designs']==[d['id']for d in protocol['designs']],'certificate designs')
    require(m['horizons']==[protocol['stages']['learning']['turns']],'certificate horizon')
    require(m['physics']=={'protocol_sha256':digest(protocol),'stage':'learning',
                          'objective':g['name'],
                          'label_scope':'Observed finite-horizon PyAT labels; not continuum proof.'},
            'certificate physics binding')


def normalized_bounds(records):
    by_design={}
    for record in records:
        check_certificate(record['manifest'],record['events'],record['certificate'])
        total=sum(Fraction(v)for v in record['manifest']['weights'].values())
        require(total>0,'zero objective weight')
        for row in record['certificate']['rows']:
            bounds=row['origin_connected_weight']
            by_design.setdefault(row['design'],[]).append({
                'lower':str(Fraction(bounds['lower'])/total),
                'upper':str(Fraction(bounds['upper'])/total)})
    require(all(len(v)==2 for v in by_design.values()),'two connected objectives required')
    exclusions=[]
    for loser,lb in by_design.items():
        for winner,wb in by_design.items():
            if loser==winner:continue
            lower=[Fraction(v['lower'])for v in wb]
            upper=[Fraction(v['upper'])for v in lb]
            if all(a>=b for a,b in zip(lower,upper))and any(a>b for a,b in zip(lower,upper)):
                exclusions.append({'excluded':loser,'witness':winner})
    return {'schema':'two-grid-connected-objective-bounds-v1',
            'objective_order':[r['manifest']['physics']['objective']for r in records],
            'source_certificate_hashes':[digest(r)for r in records],
            'rows':by_design,'strict_pareto_exclusions':exclusions,
            'scope':'Conditional on observed finite-grid labels; per-grid raw/connected exclusions are not used.'}


def check_events(protocol,events,stage):
    spec=protocol['stages'][stage];keys=set()
    for e in events:
        require(e['stage']==stage and e['turns']==spec['turns'],'stage/horizon binding')
        require(e['protocol_sha256']==digest(protocol),'event protocol binding')
        key=(e['objective'],e['design'],e['launch'])
        require(key not in keys,'duplicate charged point');keys.add(key)
        o,d,l=key
        require(type(o)is int and 0<=o<len(spec['launch_sets']),'objective index')
        require(type(d)is int and 0<=d<len(protocol['designs']),'design index')
        require(type(l)is int and 0<=l<len(spec['launch_sets'][o]['coordinates']),'launch index')
        require(type(e['survived'])is bool,'boolean survival')
        if e['survived']:
            require(e['completed_turns']==spec['turns']and e['survival_fraction']==1,'survival horizon')
        else:
            require(0<=e['completed_turns']<spec['turns'],'zero-based loss turn')
            require(0<=e['loss_element_zero_based']<protocol['full_ring_elements'],'loss element')
            require(e['survival_fraction']==e['completed_turns']/spec['turns'],'fraction convention')
    return keys


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--campaign',type=Path,default=HERE/'results/pilot')
    p.add_argument('--protocol',type=Path,default=HERE/'protocol.json')
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    protocol=json.loads(args.protocol.read_text())
    require(protocol['lattice_sha256']==LATTICE_SHA256,'lattice binding')
    frozen=json.loads((args.campaign/'execution_frozen.json').read_text())
    require(frozen['protocol_sha256']==digest(protocol),'frozen protocol hash')
    for rel,sha in frozen['sources'].items():
        require(hashlib.sha256((args.campaign/'source_snapshot'/rel).read_bytes()).hexdigest()==sha,
                'historical executed source hash')
    summary=json.loads((args.campaign/'summary.json').read_text())
    require(summary['status']=='passed','campaign incomplete')
    require(summary['protocol_sha256']==digest(protocol),'summary binding')
    results={};combined={};events_by_method={};totals=0
    for row in summary['results']:
        method=row['method'];folder=args.campaign/method
        require(method not in results,'duplicate method')
        results[method]=row
        learning=json.loads((folder/'learning_events.json').read_text())
        validation=json.loads((folder/'validation_events.json').read_text())
        check_events(protocol,learning,'learning');check_events(protocol,validation,'validation')
        events_by_method[method]=learning
        for label,events in [('learning',learning),('validation',validation)]:
            ledger=row[label+'_ledger']
            require(ledger['stage']==label and ledger['turns']==protocol['stages'][label]['turns'],
                    'ledger stage/horizon')
            for call in ledger['calls']:
                require(type(call['points'])is int and call['points']>0,'positive batch size')
                require(type(call['seconds'])in(int,float)and math.isfinite(call['seconds'])
                        and call['seconds']>=0,'finite nonnegative timer')
                require(call['stage']==label,'call stage')
                require(type(call['design'])is int and 0<=call['design']<len(protocol['designs']),
                        'call design')
            require(ledger['physical_points']==len(events),'physical point count')
            require(sum(c['points']for c in ledger['calls'])==len(events),'batch accounting')
            require(math.isclose(sum(c['seconds']for c in ledger['calls']),ledger['tracking_seconds'],
                                 rel_tol=1e-12,abs_tol=1e-12),'timer sum')
            require(ledger['completed_particle_turns']==sum(e['completed_turns']for e in events),'turn work')
            totals+=len(events)
        selection=json.loads((folder/'selection_locked.json').read_text())
        chosen=selection['designs']
        require(chosen==row['selected_designs'],'selected design identity')
        require(all(e['design']in chosen for e in validation),'validation scope')
        wanted=sum(len(g['coordinates'])for g in protocol['stages']['validation']['launch_sets'])*len(chosen)
        require(len(validation)==wanted,'complete selected-design validation grid')
        for j,d in enumerate(chosen):
            for o,g in enumerate(protocol['stages']['validation']['launch_sets']):
                labels={e['launch']:e['survived']for e in validation if e['design']==d and e['objective']==o}
                score=connected_fraction([labels[l]for l in range(len(g['coordinates']))],g)
                require(score==row['validated_objectives'][j][o],'validated objective replay')
        records=[json.loads((folder/f'objective_{o:02d}_certificate.json').read_text())for o in range(2)]
        for o,r in enumerate(records):
            certificate_binding(r,protocol,o)
            expected=[{'design':protocol['designs'][e['design']]['id'],'cell':f"cell_{e['launch']:04d}",
                       'horizon':e['turns'],'label':int(e['survived']),'source':digest(e)}
                      for e in learning if e['objective']==o]
            require(r['events']==expected,'certificate/physical event binding')
        combined[method]=normalized_bounds(records)
    require(set(results)==set(frozen['methods']),'completed method set')
    exact_match=None
    if 'full_grid'in combined and 'connected_frontier'in combined:
        a=combined['full_grid']['rows'];b=combined['connected_frontier']['rows']
        for d in a:
            for i in range(2):
                require(a[d][i]['lower']==a[d][i]['upper'],'full-grid exact score')
                require(b[d][i]['lower']==b[d][i]['upper'],'frontier unresolved objective')
                require(a[d][i]==b[d][i],'frontier/exhaustive objective mismatch')
        exact_match=True
    report={'status':'passed','physical_point_evaluations':totals,
            'frozen_source_files_verified':len(frozen['sources']),
            'combined_objective_bounds':combined,
            'frontier_exhaustive_learning_objectives_equal':exact_match,
            'validation_scope':'Only selected designs. No global validation optimum/regret is established.',
            'timing_scope':'Measured workflow excludes install/development and final event/result log serialization; host not dedicated.',
            'physical_scope':'Checks numerical-label bookkeeping and finite-table implications, not simulator accuracy or continuous stability.',
            'tenfold_established':False}
    target=args.output or args.campaign/'verification.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='combined_objective_bounds'},indent=2))


if __name__=='__main__':main()
