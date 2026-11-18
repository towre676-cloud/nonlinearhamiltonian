"""Phases: prior -> calibrate (train+validation, on-locus only) -> freeze -> confirm (transfer + fresh).
Usage: python run_estimator.py {calibrate|fresh_groups|confirm} [workers]"""
import json, sys, os, hashlib, random
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np
from fractions import Fraction as F
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sens import *
from estimator import analyse, weak_fit, LIB_W
OUT = HERE/'out'/'estimator'; OUT.mkdir(parents=True, exist_ok=True)
DESIGNS = {'A': IC_BENCH, 'B': np.array(json.load(open(HERE/'out'/'design.json'))['designed_ics'])}
SIG = {'s5': 1e-5, 's3': 1e-3}

def prior():
    p = OUT/'prior.json'
    if p.exists(): return np.array(json.load(open(p))['prior'])
    rows = [json.loads(l) for l in open(ROOT/'data'/'exact.jsonl')]
    ids = {r['id'] for r in rows if r['split'] == 'train' and r['stratum'] == 'delta' and r['least_depth'] == 2}
    z = np.load(ROOT/'data'/'trajectories_train.npz')
    fits = [weak_fit(z['t'], z['qp'][k, 1], 1e-5, LIB_W) for k, i in enumerate(z['ids']) if i in ids]
    pr = np.mean(fits, 0)
    json.dump({'source': 'benchmark training trajectories, delta depth-2 training labels, noise index 1',
               'n': len(fits), 'prior': pr.tolist()}, open(p, 'w'), indent=1)
    return pr

def job(spec):
    phase, gkey, member, h, eps, design, sk, rep, seed = spec
    ics = DESIGNS[design]; X = trajectories(h, ics)
    Y = X + SIG[sk]*np.random.default_rng(seed).standard_normal(X.shape)
    o = analyse(T_BENCH, Y, SIG[sk], PRIOR)
    o.update(phase=phase, group=gkey, member=member, eps=eps, design=design, sigma=SIG[sk], rep=rep,
             c_true=36*float(h[(0,3)])*eps)
    return o

def seed_of(*a): return int(hashlib.sha256(repr(a).encode()).hexdigest()[:15], 16)

def run(specs, path, workers):
    done = set()
    if path.exists(): done = {(r['group'], r['member'], r['design'], r['sigma'], r['rep']) for r in map(json.loads, open(path))}
    todo = [s for s in specs if (s[1], s[2], s[5], SIG[s[6]], s[7]) not in done]
    with Pool(workers) as pool, open(path, 'a') as f:
        for k, o in enumerate(pool.imap_unordered(job, todo)):
            f.write(json.dumps(o)+'\n'); f.flush()
            if k % 20 == 0: print(path.name, k+1, '/', len(todo), flush=True)

def members(h0, near):
    out = [('on', h0, 0.)]
    for mag, (h, _, de) in sorted(near.items(), reverse=True): out.append((f'eps{float(mag):g}', h, float(de)))
    return out

PRIOR = prior()

if __name__ == '__main__':
    phase = sys.argv[1]; workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    G = load_delta()
    if phase == 'calibrate':
        specs = [('cal', g, 'on', d['h0'], 0., ds, sk, r, seed_of('cal', g, ds, sk, r))
                 for g, d in G.items() if d['split'] != 'test' for ds in DESIGNS for sk in SIG for r in range(4)]
        run(specs, OUT/'calibration.jsonl', workers)
    elif phase == 'fresh_groups':
        sys.path.insert(0, str(ROOT/'sources')); sys.path.insert(0, str(ROOT))
        import generate as Gen, sixfold_global_depth as GD
        rng = random.Random(20261118); rows = []
        for index in range(12):
            h, axis, partners = Gen.instance('delta', rng, index); assert axis == (3, 1) and partners
            h = {m: c for m, c in h.items() if c}; assert GD.classify(h)['depth'] == 2
            sign = rng.choice([-1, 1]); near = {}
            for e in Gen.EPS:
                hp = dict(h); hp[axis] = h.get(axis, F(0)) + sign*e; hp = {m: c for m, c in hp.items() if c}
                assert GD.classify(hp)['depth'] == 1; near[str(e)] = [[i, j, str(c)] for (i, j), c in sorted(hp.items())]
            rows.append({'group': f'fresh{index:02d}', 'h0': [[i, j, str(c)] for (i, j), c in sorted(h.items())],
                         'sign': sign, 'near': near})
        json.dump(rows, open(OUT/'fresh_groups.json', 'w'), indent=1); print('fresh groups', len(rows), 'exact depths verified')
    elif phase == 'confirm':
        rd = lambda rows: {(i, j): F(c) for i, j, c in rows}
        specs = []
        for g, d in G.items():
            if d['split'] != 'test': continue
            for mem, h, e in members(d['h0'], d['near']):
                for ds in DESIGNS:
                    for r in range(6): specs.append(('transfer', g, mem, h, e, ds, 's5', r, seed_of('tr', g, mem, ds, r)))
        for row in json.load(open(OUT/'fresh_groups.json')):
            near = {F(k): (rd(v), None, row['sign']*F(k)) for k, v in row['near'].items()}
            for mem, h, e in members(rd(row['h0']), near):
                for ds in DESIGNS:
                    for r in range(6): specs.append(('fresh', row['group'], mem, h, e, ds, 's5', r, seed_of('fr', row['group'], mem, ds, r)))
                    for r in range(2): specs.append(('fresh', row['group'], mem, h, e, ds, 's3', r, seed_of('fr3', row['group'], mem, ds, r)))
        run(specs, OUT/'confirm.jsonl', workers)
