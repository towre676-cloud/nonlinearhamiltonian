"""Exact hypotheses for the delta-locus family H_eps = H_0 + eps q^3 p (Theorem J, row J7/weight 1)."""
from fractions import Fraction as F
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'sources'))
import sixfold_global_depth as G
import sixfold_jump_loci as J

def read(rows): return {(i, j): F(c) for i, j, c in rows}

def check(h0):
    c = lambda i, j: h0.get((i, j), F(0))
    a, b, x, r12, r31 = c(4,1), c(2,2), c(0,3), c(1,2), c(3,1)
    out = {'alpha': str(a), 'beta': str(b), 'x': str(x)}
    out['Delta_w'] = str(b*b - 3*a*x)
    out['g2=3x r31-2b r12'] = str(3*x*r31 - 2*b*r12)
    out['Gamma2'] = str(12*a*a*x*x + 4*a*b*b*x - b**4 - 45*b*x*x)
    out['off_cube_locus'] = not (3*b == a*a and 27*x == a**3)
    out['depth_H0'] = G.classify(h0)['depth']
    out['partners_H0'] = [sorted((list(k), str(v)) for k, v in p.items()) for p in J.cubic_form_partners(h0)]
    # T3(H_eps, D_{H_eps} q) for several eps; theorem: 48(3ax-b^2) q + 12(3x r31 - 2 b r12)
    probe = {(1, 0): F(1)}
    rows = []
    for e in [F(0), F(1,10), F(-1,10), F(1,1000), F(1,100000), F(7,3), F(-5)]:
        h = dict(h0); h[3,1] = c(3,1) + e
        h = {k: v for k, v in h.items() if v}
        t3 = G.transvectant(h, G.transvectant(h, probe, 1), 3)
        t5 = G.transvectant(h, G.transvectant(h, probe, 1), 5)
        predicted = {(1,0): 48*(3*a*x - b*b), (0,0): 12*(3*x*(r31+e) - 2*b*r12)}
        predicted = {k: v for k, v in predicted.items() if v}
        t3 = {k: v for k, v in t3.items() if v}
        rows.append({'eps': str(e), 'depth': G.classify(h)['depth'],
                     'T3_matches_formula': t3 == predicted, 'T3_const': str(t3.get((0,0), 0)),
                     'T5_zero': not any(t5.values()), 'partners': len(J.cubic_form_partners(h))})
    out['eps_sweep'] = rows
    return out

if __name__ == '__main__':
    rows = [json.loads(l) for l in open(HERE.parent / 'reference' / 'exact.jsonl')]
    on = [r for r in rows if r['stratum'] == 'delta' and r['least_depth'] == 2]
    report = {r['group']: dict(split=r['split'], **check(read(r['coefficients']))) for r in on}
    ok = all(v['depth_H0'] == 2 and v['Delta_w'] == '0' and v['g2=3x r31-2b r12'] == '0'
             and v['Gamma2'] != '0' and v['off_cube_locus']
             and all(s['T3_matches_formula'] and s['T5_zero'] and
                     (s['depth'] == 2) == (s['eps'] == '0') and
                     (s['depth'] == 1 or s['eps'] == '0') for s in v['eps_sweep'])
             for v in report.values())
    (HERE / 'out').mkdir(exist_ok=True)
    (HERE / 'out' / 'exact_check.json').write_text(json.dumps(report, indent=1))
    print('groups', len(report), 'all hypotheses verified:', ok)
    assert ok
