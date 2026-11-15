"""Validate package integrity, exact obstruction certificates and split isolation."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np

from generate import G, EPS, NOISE, obstruction, read_terms

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('data',type=Path)
data=parser.parse_args().data
manifest=json.loads((data/'manifest.json').read_text())
for name,digest in manifest['sha256'].items():
    assert hashlib.sha256((data/name).read_bytes()).hexdigest()==digest
rows=list(map(json.loads,(data/'exact.jsonl').read_text().splitlines()))
assert len(rows)==manifest['models']
groups={}
for r in rows:
    h=read_terms(r['coefficients'])
    assert G.classify(h)['depth']==r['least_depth']
    for probe in r['probe_certificates']:
        assert obstruction(h,read_terms(probe['polynomial']),r['least_depth'])==probe['first_failure']
    groups.setdefault(r['group'],[]).append(r)
for members in groups.values():
    assert len({m['split'] for m in members})==1
    original,=[m for m in members if m['perturbation'] is None]
    if original['least_depth']==6:
        assert len(members)==1
        continue
    assert len(members)==1+len(EPS)
    seen=set()
    for m in members:
        ch=m['perturbation']
        if ch:
            perturbed=read_terms(original['coefficients'])
            axis=tuple(ch['monomial'])
            delta=Fraction(ch['delta'])
            perturbed[axis]=perturbed.get(axis,0)+delta
            assert {a:c for a,c in perturbed.items() if c}==read_terms(m['coefficients'])
            seen.add(abs(delta))
            assert (original['least_depth'],m['least_depth'])==(2,1)
    assert seen==set(EPS)
for split in ('train','validation','test'):
    ids=[r['id'] for r in rows if r['split']==split]
    with np.load(data/f'trajectories_{split}.npz',allow_pickle=False) as a:
        assert a['ids'].tolist()==ids
        assert a['qp'].shape==(len(ids),4,6,49,2) and np.isfinite(a['qp']).all()
        assert np.array_equal(a['noise_sigma'],NOISE)
        assert np.array_equal(a['qp'][:,0,:,0,:],
                              np.broadcast_to(manifest['initial_states'],(len(ids),6,2)))
        assert np.all(np.diff(a['t'])>0)
print('PASS: hashes, pair isolation, exact labels, obstruction certificates and trajectory arrays')
print(Counter((r['stratum'],r['least_depth']) for r in rows))
