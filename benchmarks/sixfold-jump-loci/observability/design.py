"""Initial-condition exchange design for the efficient (unknown-background, J7-locus) information.
Selection uses train + validation delta groups only."""
import json, sys, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from sens import *

_G = np.array([[a, b] for a in np.arange(-.4, .4001, .05) for b in np.arange(-.4, .4001, .05)])
RMAX = float(np.linalg.norm(IC_BENCH, axis=1).max())          # fairness: no larger amplitude than the benchmark
GRID = _G[np.linalg.norm(_G, axis=1) <= RMAX + 1e-12]

def ieff_from_M(M, B):
    MB = B.T@M@B
    return 1.0/np.linalg.inv(MB)[-1, -1]

def basis(h):
    T = nullspace(constraint_grads(h, LIB_W)); e = np.zeros(len(LIB_W)); e[LIB_W.index(E31)] = 1
    return np.hstack([T, e[:, None]])

def ic_info(h, ic):
    Jb = jacobian(h, LIB_W, ics=np.array([ic])); return Jb.T@Jb

def criterion(Ms, Bs, idx):
    vals = []
    for M, B in zip(Ms, Bs):
        tot = sum(M[i] for i in idx)
        try: v = ieff_from_M(tot, B)
        except np.linalg.LinAlgError: return -np.inf
        if not np.isfinite(v) or v <= 0: return -np.inf
        vals.append(np.log(v))
    return float(np.mean(vals))

if __name__ == '__main__':
    G = load_delta()
    fit = [d for d in G.values() if d['split'] in ('train', 'validation')]
    cands = np.vstack([IC_BENCH, GRID])
    Ms, Bs = [], []
    for d in fit:
        Ms.append([ic_info(d['h0'], c) for c in cands]); Bs.append(basis(d['h0']))
    cur = list(range(6)); best = criterion(Ms, Bs, cur); start = best
    improved = True
    while improved:
        improved = False
        for slot in range(6):
            for c in range(len(cands)):
                if c in cur: continue
                trial = cur.copy(); trial[slot] = c
                v = criterion(Ms, Bs, trial)
                if v > best + 1e-9: best, cur, improved = v, trial, True
        print('pass', best, flush=True)
    design = cands[cur]
    res = dict(rmax=RMAX, n_candidates=len(cands), benchmark_mean_log_ieff=start, designed_mean_log_ieff=best,
               designed_ics=design.tolist(), selection_groups=[k for k, d in G.items() if d['split'] != 'test'])
    json.dump(res, open(HERE/'out'/'design.json', 'w'), indent=1); print(json.dumps(res, indent=1))
