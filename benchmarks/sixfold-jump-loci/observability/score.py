"""Score confirmation fits with the frozen rules; compare with the local efficient-information prediction."""
import json, sys, os, collections, numpy as np
from fractions import Fraction as F
from scipy.stats import norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sens import *
D = HERE/'out'/'estimator'
fz = json.load(open(D/'frozen.json')); Z = fz['interval_z']
rows = [json.loads(l) for l in open(D/sys.argv[1] if len(sys.argv) > 1 else D/'confirm.jsonl')]
DESIGNS = {'A': IC_BENCH, 'B': np.array(json.load(open(HERE/'out'/'design.json'))['designed_ics'])}

def cell(r): return fz['cells'][f"{r['design']}|{r['sigma']:g}"]
def forced(r): return 1 if r['lam'] > cell(r)['lam_crit'] else 2
def selective(r):
    if r['lam'] > cell(r)['lam_crit']: return 1
    return 2 if abs(r['c_hat']) + Z*r['se_c'] < cell(r)['eta'] else None
def plugin(r):
    z = r['plug_z']; return None if not np.isfinite(z) else (1 if abs(z) > cell(r)['z_crit'] else 2)

def wilson(k, n):
    if n == 0: return (float('nan'),)*2
    p = k/n; z = 1.96; d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return (round(c-h, 3), round(c+h, 3))

# local prediction: J7 locus with fitted initial states
h0s = {}
for g, d in load_delta().items(): h0s[g] = d['h0']
for row in json.load(open(D/'fresh_groups.json')): h0s[row['group']] = {(i, j): F(c) for i, j, c in row['h0']}
sperp = {}
for g in {r['group'] for r in rows}:
    for ds, ics in DESIGNS.items(): sperp[g, ds] = signals(h0s[g], ics)[0]['J7_locus_unknown_ic']
def p_rej(r, eps):
    lc = np.sqrt(cell(r)['lam_crit']); dl = abs(eps)*sperp[r['group'], r['design']]/r['sigma']
    return norm.cdf(-lc + dl) + norm.cdf(-lc - dl)

idx = {(r['phase'], r['group'], r['design'], r['sigma'], r['rep'], r['member']): r for r in rows}
report = {'pairs': [], 'cases': [], 'failures': {}, 'coverage': {}}
keys = sorted({(r['phase'], r['design'], r['sigma']) for r in rows})
for ph, ds, sg in keys:
    sub = [r for r in rows if (r['phase'], r['design'], r['sigma']) == (ph, ds, sg)]
    report['failures'][f'{ph}|{ds}|{sg:g}'] = dict(n=len(sub), any_start_failed=sum(r['fails'] > 0 for r in sub),
        inconsistent=sum(r['inconsistent'] for r in sub), chi2_red_over_1p5=sum(r['chi2_red'] > 1.5 for r in sub),
        plugin_failed=sum(not r.get('plug_ok', False) for r in sub))
    cov = [abs(r['c_hat'] - r['c_true']) <= Z*r['se_c'] for r in sub]
    report['coverage'][f'{ph}|{ds}|{sg:g}'] = dict(n=len(cov), coverage=float(np.mean(cov)), ci=wilson(sum(cov), len(cov)))
    on = [r for r in sub if r['member'] == 'on']
    report['cases'].append(dict(phase=ph, design=ds, sigma=sg, member='on', n=len(on),
        false_pos_forced=float(np.mean([forced(r) == 1 for r in on])),
        false_pos_plugin=float(np.mean([plugin(r) == 1 for r in on])),
        selective_answered=float(np.mean([selective(r) is not None for r in on])),
        predicted_false_pos=float(np.mean([p_rej(r, 0.) for r in on]))))
    for mag in ('eps0.1', 'eps0.001', 'eps1e-05'):
        res = collections.Counter(); pred = []; nm_rej = []
        for r1 in [r for r in sub if r['member'] == mag]:
            r0 = idx.get((ph, r1['group'], ds, sg, r1['rep'], 'on'))
            if r0 is None: continue
            res['n'] += 1
            res['forced'] += forced(r0) == 2 and forced(r1) == 1
            res['plugin'] += plugin(r0) == 2 and plugin(r1) == 1
            s0, s1 = selective(r0), selective(r1)
            res['sel_answered'] += s0 is not None and s1 is not None
            res['sel_correct'] += s0 == 2 and s1 == 1
            res['sel_rule_error'] += (s1 == 2 and abs(r1['c_true']) >= cell(r1)['eta']) + (s0 == 1)
            nm_rej.append(forced(r1) == 1)
            pred.append((1 - p_rej(r0, 0.))*p_rej(r1, r1['eps']))
        n = res['n']
        report['pairs'].append(dict(phase=ph, design=ds, sigma=sg, magnitude=mag, n_pairs=n,
            forced_pairs=res['forced'], forced_ci=wilson(res['forced'], n),
            predicted_forced=round(float(np.mean(pred)), 3) if pred else None,
            near_miss_detect=round(float(np.mean(nm_rej)), 3) if nm_rej else None,
            plugin_pairs=res['plugin'], plugin_ci=wilson(res['plugin'], n),
            selective_answered=res['sel_answered'], selective_correct=res['sel_correct'],
            selective_rule_errors=res['sel_rule_error']))
json.dump(report, open(D/'score.json', 'w'), indent=1)
for p in report['pairs']: print(p)
for c in report['cases']: print(c)
print(json.dumps(report['failures'])); print(json.dumps(report['coverage']))
