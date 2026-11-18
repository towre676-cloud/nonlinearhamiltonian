"""Diagnostic ablations of the repository's guarded weak-locus pipeline (n = 49, sigma = 1e-5) on identical
observations: the original benchmark test delta cases and the frozen fresh design-A confirmation observations.
Stages replaced one at a time: coefficients (weak -> nonlinear trajectory fit), branch guard (-> delta supplied),
calibration (-> threshold-free pair ordering). Diagnostic only; no estimator claim."""
import json, sys, os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
from collections import Counter, defaultdict
from multiprocessing import Pool
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
import identify as I
import experiment as E
from fractions import Fraction as F
from sens import load_delta, trajectories, T_BENCH, IC_BENCH
from estimator import Problem, SETTINGS, ID5
from sens import LIB_D5
from pathlib import Path
OUT = Path(HERE)/'out'/'diagnosis'; OUT.mkdir(parents=True, exist_ok=True)
K, N, SIGMA = 1, 49, 1e-5
FAM = list(I.FAMILIES); DI = FAM.index('delta')

def nonlinear_fit(Y, sigma):
    """Unconstrained degree-5 trajectory fit from the study's own weak start; returns an identify.Fit."""
    pb = Problem(T_BENCH, Y, sigma)
    w = I.fit_field(T_BENCH, Y, sigma, 'weak')
    th5 = np.zeros(len(LIB_D5))
    for n, m in enumerate(I.TERMS): th5[ID5[m]] = w.coefficients[n]
    from estimator import ic_start
    v0 = np.concatenate([th5, ic_start(T_BENCH, Y).ravel()])
    r = least_squares(pb.res_d5, v0, jac=pb.jac_d5, **SETTINGS)
    cov = np.linalg.pinv(pb.jac_d5(r.x).T @ pb.jac_d5(r.x))[:len(LIB_D5), :len(LIB_D5)]
    perm = [ID5[m] for m in I.TERMS]                     # identify.TERMS order
    c = r.x[perm]; C = cov[np.ix_(perm, perm)]
    L = np.linalg.cholesky(C + 1e-30*np.eye(len(c)))
    return I.Fit(c, L, 1.0, float(np.linalg.cond(C))), bool(r.status > 0)

def eligible(fit):
    se = fit.residual_scale*np.linalg.norm(fit.inverse_information, axis=1)
    det = dict(zip(I.TERMS, abs(fit.coefficients) > 4*se))
    if det[0, 4]: return ['quartic']
    if det[3, 2]: return ['c32']
    if det[0, 3]: return ['delta', 'origin'] + (['gamma'] if det[2, 2] else [])
    return ['depth-six']

def features(Y, sigma, with_nl=True):
    w = I.fit_field(T_BENCH, Y, sigma, 'weak')
    out = dict(weak_guarded=I.distances(w, True).tolist(), weak_all=I.distances(w, False).tolist(),
               weak_eligible=eligible(w))
    if with_nl:
        nf, ok = nonlinear_fit(Y, sigma)
        out.update(nl_guarded=I.distances(nf, True).tolist(), nl_all=I.distances(nf, False).tolist(),
                   nl_eligible=eligible(nf), nl_ok=ok)
    return out

def job(spec):
    key, Y, sigma = spec
    return key, features(Y, sigma)

def seed_of(*a):
    import hashlib; return int(hashlib.sha256(repr(a).encode()).hexdigest()[:15], 16)

if __name__ == '__main__':
    data = Path(ROOT)/'data'; arrays = E.load_arrays(data); labels = E.read_labels(data/'exact.jsonl')
    exact = {r['id']: r for r in map(json.loads, open(data/'exact.jsonl'))}
    specs = []
    # validation (all strata) for recalibrating each stage with the repository's own procedures
    va = arrays['validation']
    for i, cid in enumerate(va['ids']): specs.append((('val', str(cid)), va['qp'][i, K], SIGMA))
    te = arrays['test']
    for i, cid in enumerate(te['ids']):
        if exact[str(cid)]['stratum'] == 'delta': specs.append((('orig', str(cid)), te['qp'][i, K], SIGMA))
    rd = lambda rows: {(i, j): F(c) for i, j, c in rows}
    for row in json.load(open(Path(HERE)/'out'/'estimator'/'fresh_groups.json')):
        mem = [('on', rd(row['h0']))] + [(f'eps{float(F(k)):g}', rd(v)) for k, v in sorted(row['near'].items(), key=lambda kv: -F(kv[0]))]
        for m, h in mem:
            X = trajectories(h, IC_BENCH)
            for r in range(6):
                Y = X + SIGMA*np.random.default_rng(seed_of('fr', row['group'], m, 'A', r)).standard_normal(X.shape)
                specs.append((('fresh', f"{row['group']}|{m}|{r}"), Y, SIGMA))
    path = OUT/'features.jsonl'; done = set()
    if path.exists(): done = {tuple(json.loads(l)['key']) for l in open(path)}
    todo = [s for s in specs if s[0] not in done]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 2) as pool, open(path, 'a') as f:
        for k, (key, o) in enumerate(pool.imap_unordered(job, todo)):
            f.write(json.dumps(dict(key=list(key), **o))+'\n'); f.flush()
            if k % 25 == 0: print(k+1, '/', len(todo), flush=True)
