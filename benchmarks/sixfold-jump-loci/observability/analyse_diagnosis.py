import json, sys, os, numpy as np
from collections import defaultdict, Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
import experiment as E, identify as I
from pathlib import Path
D = Path(HERE)/'out'/'diagnosis'
rows = [json.loads(l) for l in open(D/'features.jsonl')]
exact = {r['id']: r for r in map(json.loads, open(Path(ROOT)/'data'/'exact.jsonl'))}
FAM = list(I.FAMILIES); DI = FAM.index('delta')
val = [r for r in rows if r['key'][0] == 'val']
vy = np.array([exact[r['key'][1]]['least_depth'] for r in val])
vdelta = np.array([exact[r['key'][1]]['stratum'] == 'delta' for r in val])

def full_rule(feat):
    Xv = np.array([r[feat] for r in val]); tol = E.tolerance(Xv, vy)
    pv, cv = E.locus_prediction(Xv, tol); sel = E.selection_threshold(cv, pv == vy)
    def decide(r):
        p, c = E.locus_prediction(np.array([r[feat]]), tol)
        return int(p[0]), (int(p[0]) if sel is not None and c[0] >= sel else None)
    return decide, dict(tol=float(tol), selection=sel)

def delta_rule(feat, frozen_tol=None):
    """Branch supplied: depth 2 iff the delta distance is below a tolerance (validation delta cases, macro recall)."""
    d = np.array([r[feat][DI] for r in val])[vdelta]; y = vy[vdelta]
    cands = np.r_[1e-8, np.geomspace(1e-6, 1e6, 97)]
    tol = frozen_tol if frozen_tol is not None else max(cands, key=lambda t: np.mean(
        [np.mean(np.where(d < t, 2, 1)[y == k] == k) for k in (1, 2)]))
    return (lambda r: (2 if r[feat][DI] < tol else 1,)*2), dict(tol=float(tol))

rules = {}
rules['S0 unchanged'] = full_rule('weak_guarded')
rules['S1 nonlinear coefficients'] = full_rule('nl_guarded')
rules['S2 branch supplied (weak), recalibrated'] = delta_rule('weak_all')
rules['S2 branch supplied (weak), frozen S0 tol'] = delta_rule('weak_all', rules['S0 unchanged'][1]['tol'])
rules['S1+S2 nonlinear, branch supplied'] = delta_rule('nl_all')

# pairs
def pairs(src):
    out = defaultdict(list)
    sub = [r for r in rows if r['key'][0] == src]
    if src == 'orig':
        byg = defaultdict(dict)
        for r in sub:
            e = exact[r['key'][1]]; m = 'on' if e['perturbation'] is None else f"eps{abs(float(__import__('fractions').Fraction(e['perturbation']['delta']))):g}"
            byg[e['group']][m] = r
        for g, d in byg.items():
            for m in ('eps0.1', 'eps0.001', 'eps1e-05'): out[m].append((d['on'], d[m], g))
    else:
        idx = {r['key'][1]: r for r in sub}
        for k, r in idx.items():
            g, m, rep = k.split('|')
            if m != 'on': out[m].append((idx[f'{g}|on|{rep}'], r, g))
    return out

report = {'rules': {k: v[1] for k, v in rules.items()}, 'pairs': {}, 'ordering': {}, 'guard': {}, 'published_check': None}
for src in ('orig', 'fresh'):
    P = pairs(src)
    for name, (dec, _) in rules.items():
        for m, lst in P.items():
            f = sum(dec(a)[0] == 2 and dec(b)[0] == 1 for a, b, _ in lst)
            s = sum(dec(a)[1] == 2 and dec(b)[1] == 1 for a, b, _ in lst)
            ans = sum(dec(a)[1] is not None and dec(b)[1] is not None for a, b, _ in lst)
            fp = np.mean([dec(a)[0] == 1 for a, b, _ in lst])
            report['pairs'][f'{src}|{name}|{m}'] = dict(n=len(lst), forced=f, selective=s, answered=ans, on_locus_called_1=float(fp))
    for feat in ('weak_all', 'nl_all', 'weak_guarded', 'nl_guarded'):
        for m, lst in P.items():
            report['ordering'][f'{src}|{feat}|{m}'] = float(np.mean([a[feat][DI] < b[feat][DI] for a, b, _ in lst]))
    sub = [r for r in rows if r['key'][0] == src]
    for coef in ('weak', 'nl'):
        report['guard'][f'{src}|{coef}'] = dict(Counter('+'.join(r[f'{coef}_eligible']) for r in sub))
    # median delta distances and ratio to tolerance
    for coef in ('weak', 'nl'):
        for m, lst in P.items():
            report['ordering'][f'{src}|median_delta_{coef}|{m}'] = [float(np.median([a[f'{coef}_all'][DI] for a, _, _ in lst])),
                                                                  float(np.median([b[f'{coef}_all'][DI] for _, b, _ in lst]))]
# check S0 reproduces the published guarded predictions on the original delta test cases
pub = json.load(open(D/'published_guarded_49.json'))
lk = {(r['id'], r['noise_index']): r['depth'] for r in pub['selective']}; lf = {(r['id'], r['noise_index']): r['depth'] for r in pub['forced']}
dec = rules['S0 unchanged'][0]
chk = [(lf[r['key'][1], 1], lk[r['key'][1], 1]) == dec(r) for r in rows if r['key'][0] == 'orig']
report['published_check'] = dict(cases=len(chk), identical=int(sum(chk)))
report['nl_fit_failures'] = int(sum(not r.get('nl_ok', True) for r in rows))
json.dump(report, open(D/'report.json', 'w'), indent=1)
print(json.dumps(report['rules'], indent=0)); print(report['published_check'], 'nl failures', report['nl_fit_failures'])
for k, v in report['pairs'].items(): print(k, v)
for k, v in report['ordering'].items(): print(k, v)
for k, v in report['guard'].items(): print(k, v)
