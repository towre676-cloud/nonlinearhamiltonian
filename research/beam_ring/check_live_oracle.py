"""Small live batching/prefix regression for the hardened oracle, not tuning."""
from pathlib import Path
import argparse
import hashlib
import json
from oracle import RingOracle,digest,load_runtime

HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',type=Path)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();load_runtime(args.runtime)
    protocol=json.loads((HERE/'protocol.json').read_text())
    selected={};stages={};count=0
    for stage in ['learning','validation']:
        batch=RingOracle(protocol,stage=stage);single=RingOracle(protocol,stage=stage)
        requests=[]
        for d in [0,1]:
            for o,g in enumerate(protocol['stages'][stage]['launch_sets']):
                requests.extend((o,d,l)for l in [0,g['origin'],len(g['coordinates'])-1])
        actual=batch.query(requests,purpose='oracle_regression_batch')
        individual=[single.query([r],purpose='oracle_regression_single')[0]for r in requests]
        for a,b in zip(actual,individual):
            assert {k:v for k,v in a.items()if k!='purpose'}=={k:v for k,v in b.items()if k!='purpose'}
        selected[stage]=actual
        stages[stage]={'batch_ledger':batch.ledger(),'single_ledger':single.ledger()}
        count+=len(batch.events)+len(single.events)
    for short,long in zip(selected['learning'],selected['validation']):
        if not short['survived']:
            assert not long['survived']
            assert short['completed_turns']==long['completed_turns']
            assert short['loss_element_zero_based']==long['loss_element_zero_based']
    result={'status':'passed','protocol_sha256':digest(protocol),'physical_point_evaluations':count,
            'batch_single_labels_and_losses':'identical','deterministic_prefix_check':'passed',
            'oracle_source_sha256':hashlib.sha256((HERE/'oracle.py').read_bytes()).hexdigest(),
            'stages':stages,'events':selected,
            'scope':'Selected physical points only; not a universal map equivalence or speedup.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ['stages','events']},indent=2))


if __name__=='__main__':main()
