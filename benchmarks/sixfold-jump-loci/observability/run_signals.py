import json, sys, numpy as np
from scipy.stats import norm
sys.path.insert(0, __import__('os').path.dirname(__file__))
from sens import *
groups = load_delta(); res = {}
for g, d in groups.items():
    sig, s = signals(d['h0'])
    mu0 = trajectories(d['h0'])
    lin = {}
    for e in EPS:
        h1, cid, de = d['near'][F(e).limit_denominator(10**6)]
        diff = (trajectories(h1) - mu0).reshape(-1)
        lin[str(e)] = {'d_exact': float(np.linalg.norm(diff)), 'd_linear': abs(float(de))*sig['known'],
                       'rel_err': float(np.linalg.norm(diff - float(de)*s)/np.linalg.norm(diff))}
    res[g] = {'split': d['split'], 'signals': sig, 'linearisation': lin}
    print(g[:6], d['split'], {k: round(v, 5) for k, v in sig.items()},
          {k: (round(v['d_exact']/v['d_linear'], 6), f"{v['rel_err']:.2e}") for k, v in lin.items()}, flush=True)
json.dump(res, open(HERE/'out'/'signals.json', 'w'), indent=1)
