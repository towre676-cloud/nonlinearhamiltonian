"""Prospective test-split evaluation of the IC design (see PREREGISTRATION.md)."""
import json, sys, numpy as np
from scipy.optimize import least_squares
sys.path.insert(0, __import__('os').path.dirname(__file__))
from sens import *
from design import basis

FREE = [(1,0),(2,0),(3,0),(4,0),(5,0),(0,1),(1,1),(2,1),(0,2),(1,2)]   # + beta, x, eps
idx = {m: n for n, m in enumerate(LIB_W)}

def theta(u):
    b, x, e = u[10], u[11], u[12]
    th = np.zeros(len(LIB_W))
    for n, m in enumerate(FREE): th[idx[m]] = u[n]
    th[idx[2,2]] = b; th[idx[0,3]] = x; th[idx[4,1]] = b*b/(3*x); th[idx[3,1]] = 2*b*u[9]/(3*x) + e
    return th

def dtheta(u):
    b, x, r12 = u[10], u[11], u[9]; D = np.zeros((len(LIB_W), 13))
    for n, m in enumerate(FREE): D[idx[m], n] = 1
    D[idx[2,2], 10] = 1; D[idx[0,3], 11] = 1
    D[idx[4,1], 10] = 2*b/(3*x); D[idx[4,1], 11] = -b*b/(3*x*x)
    D[idx[3,1], 9] = 2*b/(3*x); D[idx[3,1], 10] = 2*r12/(3*x); D[idx[3,1], 11] = -2*b*r12/(3*x*x); D[idx[3,1], 12] = 1
    return D

def H(u):
    th = theta(u); out = {m: th[idx[m]] for m in LIB_W}; out[(6,0)] = 1.0; return out

def mu(u, ics): return trajectories(H(u), ics).reshape(-1)

def u_of(h0):
    c = lambda i, j: float(h0.get((i, j), 0))
    return np.array([c(*m) for m in FREE] + [c(2,2), c(0,3), 0.])

def mc(h0, ics, eps, sigma, reps):
    u0 = u_of(h0); ut = u0.copy(); ut[12] = eps
    clean = mu(ut, ics); est, z = [], []
    for seed in range(reps):
        y = clean + sigma*np.random.default_rng(seed).standard_normal(clean.shape)
        fun = lambda u: mu(u, ics) - y
        jac = lambda u: jacobian(H(u), LIB_W, ics) @ dtheta(u)
        r = least_squares(fun, u0, jac=jac, method='lm', xtol=1e-14, ftol=1e-14, gtol=1e-14)
        Jf = jac(r.x); cov = sigma**2*np.linalg.inv(Jf.T@Jf)
        est.append(r.x[12]); z.append(r.x[12]/np.sqrt(cov[12, 12]))
    return np.array(est), np.array(z)

if __name__ == '__main__':
    G = load_delta(); D = json.load(open(HERE/'out'/'design.json'))
    designs = {'A_benchmark': IC_BENCH, 'B_designed': np.array(D['designed_ics'])}
    res = {'groups': {}}
    for g, d in G.items():
        if d['split'] != 'test': continue
        row = {}
        for name, ics in designs.items():
            sig, _ = signals(d['h0'], ics)
            row[name] = sig
        row['ratio_Ieff_J7'] = (row['B_designed']['J7_locus']/row['A_benchmark']['J7_locus'])**2
        row['ratio_Ieff_J7_unknown_ic'] = (row['B_designed']['J7_locus_unknown_ic']/row['A_benchmark']['J7_locus_unknown_ic'])**2
        row['ratio_known'] = (row['B_designed']['known']/row['A_benchmark']['known'])**2
        res['groups'][g] = row
        print(g[:6], {k: round(v, 3) for k, v in row.items() if k.startswith('ratio')}, flush=True)
    r = np.array([v['ratio_Ieff_J7'] for v in res['groups'].values()])
    res['primary'] = dict(ratios=r.tolist(), geometric_mean=float(np.exp(np.log(r).mean())),
                          success=bool((r > 1).all() and np.exp(np.log(r).mean()) >= 2))
    print('primary', res['primary'], flush=True)
    key = [k for k in G if k.startswith('1ae54b')][0]; h0 = G[key]['h0']; sigma = 1e-5
    res['monte_carlo'] = {}
    for name, ics in designs.items():
        sperp = signals(h0, ics)[0]['J7_locus']
        for eps in (0., 1e-2):
            est, z = mc(h0, ics, eps, sigma, 40)
            res['monte_carlo'][f'{name} eps={eps}'] = dict(
                predicted_sd=sigma/sperp, empirical_sd=float(est.std(ddof=1)), mean_eps_hat=float(est.mean()),
                reject_rate=float((np.abs(z) > 1.96).mean()),
                predicted_reject=float(norm.cdf(-1.96 + eps*sperp/sigma) + norm.cdf(-1.96 - eps*sperp/sigma)))
            print(name, eps, res['monte_carlo'][f'{name} eps={eps}'], flush=True)
    json.dump(res, open(HERE/'out'/'design_test.json', 'w'), indent=1)
