import json, sys, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from sens import *
G = load_delta(); D = json.load(open(HERE/'out'/'design.json'))
designs = {'A': IC_BENCH, 'B': np.array(D['designed_ics'])}
out = {'accuracy': [], 'confounder': {}}
for g, d in G.items():
    if d['split'] != 'test': continue
    for dn, ics in designs.items():
        sig, s = signals(d['h0'], ics)
        for reg in ('known', 'J7_locus', 'J7_locus_unknown_ic', 'plugin_D5_g2'):
            for sg in NOISE:
                for e in EPS:
                    a = float(norm.cdf(e*sig[reg]/(2*sg)))
                    out['accuracy'].append(dict(group=g[:6], design=dn, regime=reg, sigma=sg, eps=e, case_acc=a, pair_acc=a*a))
        # abstention margin: smallest |eps| resolvable at alpha=0.05 two-sided, power 0.95
        out.setdefault('margin', []).append(dict(group=g[:6], design=dn, **{f'eta_sigma={sg}': (1.96+1.645)*sg/sig['J7_locus'] for sg in NOISE}))
        if dn == 'A':
            JW = jacobian(d['h0'], LIB_W, ics); T = nullspace(constraint_grads(d['h0'], LIB_W))
            N = JW@T; v, *_ = np.linalg.lstsq(N, s, rcond=None); w = T@v
            top = sorted(zip(LIB_W, w), key=lambda t: -abs(t[1]))[:5]
            out['confounder'][g[:6]] = dict(cos_angle=float(np.linalg.norm(N@v)/np.linalg.norm(s)),
                                            mimic=[(list(m), float(c)) for m, c in top])
json.dump(out, open(HERE/'out'/'tables.json', 'w'), indent=1)
import collections
agg = collections.defaultdict(list)
for r in out['accuracy']: agg[(r['design'], r['regime'], r['sigma'], r['eps'])].append(r['case_acc'])
for k, v in sorted(agg.items()):
    if k[2] == 1e-5 or k[2] == 1e-3: print(k, round(float(np.mean(v)), 4))
print(json.dumps(out['margin'], indent=0)); print(json.dumps(out['confounder'], indent=0))
