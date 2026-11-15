"""Score predictions and run a nearest-trajectory baseline."""
import argparse
from fractions import Fraction
import json
from pathlib import Path

import numpy as np

CLASSES = (1, 2, 6)


def labels(data, split):
    return {r['id']:r for r in map(json.loads,(data/'exact.jsonl').read_text().splitlines())
            if r['split']==split}


def score(data, split, predictions):
    truth = labels(data, split)
    observations = {}
    for row in predictions:
        i,k,pred = row['id'],row['noise_index'],row['depth']
        if (i not in truth or type(k) is not int or k not in range(4)
                or (pred is not None and (type(pred) is not int or pred not in CLASSES))):
            raise ValueError(f'invalid prediction: {row}')
        if (i,k) in observations:
            raise ValueError(f'duplicate prediction: {(i,k)}')
        observations[i,k] = pred
    if len(observations) != 4*len(truth):
        raise ValueError('supply every model and noise index, using null to abstain')
    report={}
    for k in range(4):
        def summarize(items):
            selected=[(i,r) for i,r in items if observations[i,k] is not None]
            correct=sum(observations[i,k]==r['least_depth'] for i,r in selected)
            return dict(n=len(items),coverage=len(selected)/len(items),
                        selective_accuracy=correct/len(selected) if selected else None,
                        correct_fraction=correct/len(items))
        report[str(k)]={'overall':summarize(list(truth.items()))}
        strata=sorted({r['stratum'] for r in truth.values()})
        for stratum in strata:
            items=[(i,r) for i,r in truth.items() if r['stratum']==stratum]
            entry=summarize(items)
            entry['by_depth']={str(d):summarize([(i,r) for i,r in items if r['least_depth']==d])
                               for d in sorted({r['least_depth'] for _,r in items})}
            if stratum != 'depth-six':
                on={r['group']:i for i,r in items if r['perturbation'] is None}
                pair_metrics={}
                for eps in ('1/10','1/1000','1/100000'):
                    off=[(i,r) for i,r in items if r['perturbation']
                         and abs(Fraction(r['perturbation']['delta']))==Fraction(eps)]
                    pair=[(observations[on[r['group']],k],observations[i,k]) for i,r in off]
                    both=sum(a is not None and b is not None for a,b in pair)
                    right=sum((a,b)==(2,1) for a,b in pair)
                    pair_metrics[eps]={'pairs':len(pair),'coverage':both/len(pair),
                                       'both_correct_fraction':right/len(pair),
                                       'selective_pair_accuracy':right/both if both else None}
                entry['pairs_by_abs_perturbation']=pair_metrics
            report[str(k)][stratum]=entry
    return report


def baseline(data):
    def features(split,k):
        with np.load(data/f'trajectories_{split}.npz',allow_pickle=False) as a:
            ids=a['ids'].tolist()
            # Retain the trajectory shape, but average adjacent frames to reduce noise.
            qp=a['qp'][:,k]
            f=qp.reshape(len(ids),6,7,7,2).mean(axis=3).reshape(len(ids),-1)
        return ids,f
    validation=labels(data,'validation')
    train=labels(data,'train')
    predictions=[]
    thresholds=[]
    for k in range(4):
        train_ids,X=features('train',k)
        y=np.array([train[i]['least_depth'] for i in train_ids])
        def raw(split):
            ids,Y=features(split,k)
            errors=((Y[:,None,:]-X[None,:,:])**2).mean(axis=-1)
            scores=np.stack([errors[:,y==d].min(axis=1) for d in CLASSES],axis=1)
            choice=scores.argmin(axis=1)
            best,next_best=np.sort(scores,axis=1)[:,:2].T
            confidence=(next_best-best)/np.maximum(next_best,1e-30)
            return ids,np.array(CLASSES)[choice],confidence
        ids,guess,conf=raw('validation')
        good=guess==np.array([validation[i]['least_depth'] for i in ids])
        # Fixed requested validation precision. Calibration may decline to answer.
        threshold=2.
        for candidate in np.unique(np.r_[0.,conf]):
            keep=conf>=candidate
            if keep.sum()>=5 and good[keep].mean()>=.8:
                threshold=float(candidate)
                break
        thresholds.append(threshold)
        ids,guess,conf=raw('test')
        predictions.extend(dict(id=i,noise_index=k,depth=int(g) if c>=threshold else None)
                           for i,g,c in zip(ids,guess,conf))
    return {'validation_thresholds':thresholds,'test':score(data,'test',predictions)},predictions


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('data',type=Path)
    p.add_argument('--split',choices=('train','validation','test'),default='test')
    p.add_argument('--predictions',type=Path,help='JSON lines, omit to run baseline')
    p.add_argument('--save-baseline-predictions',type=Path)
    a=p.parse_args()
    if a.predictions:
        result=score(a.data,a.split,list(map(json.loads,a.predictions.read_text().splitlines())))
    else:
        result,predictions=baseline(a.data)
        if a.save_baseline_predictions:
            a.save_baseline_predictions.write_text(''.join(json.dumps(p)+'\n' for p in predictions))
    print(json.dumps(result,indent=2,allow_nan=False))
