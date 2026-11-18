"""Explicit Gronwall remainder bound for mu_eps - mu_0 - eps*s along q^3 p (proved bound; constants in float64)."""
import json, sys, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from sens import *

def supabs(h, Q, P, di=0, dj=0):
    """Upper bound of sup |d^di_q d^dj_p H| on |q|<=Q, |p|<=P."""
    tot = 0.
    for (i, j), c in h.items():
        if i < di or j < dj: continue
        f = 1.
        for a in range(di): f *= (i - a)
        for a in range(dj): f *= (j - a)
        tot += abs(c)*f*Q**(i-di)*P**(j-dj)
    return tot

def constants(h, Q, P):
    S = lambda a, b: supabs(h, Q, P, a, b)
    L1 = np.sqrt(2*S(1,1)**2 + S(0,2)**2 + S(2,0)**2)                       # ||Df||_F
    B2 = np.sqrt((S(2,1)**2 + 2*S(1,2)**2 + S(0,3)**2) + (S(3,0)**2 + 2*S(2,1)**2 + S(1,2)**2))
    Mg = np.sqrt(Q**6 + 9*Q**4*P**2); Lg = np.sqrt(9*Q**4 + 36*Q**2*P**2 + 9*Q**4)
    return L1, B2, Mg, Lg

def bound(h, margin=0.05, eps_max=0.1, n=4000):
    hf = fl(h); X = trajectories(h)
    out = []
    for k in range(len(IC_BENCH)):
        Q = np.abs(X[k,:,0]).max() + margin; P = np.abs(X[k,:,1]).max() + margin
        L1, B2, Mg, Lg = [v*(1+1e-9) for v in constants(hf, Q, P)]
        D = lambda t: Mg*np.expm1(L1*t)/L1
        assert eps_max*D(T_BENCH[-1]) <= margin, 'bootstrap: perturbed orbit may leave the box'
        Cs = []
        for t in T_BENCH:
            tau = np.linspace(0, t, n+1)[1:]; dt = t/n if t else 0.
            integrand = np.exp(L1*(t - tau + dt))*(0.5*B2*D(tau)**2 + Lg*D(tau))  # monotone majorant, right sums
            Cs.append(float(integrand.sum()*dt))
        out.append(dict(Q=Q, P=P, L1=L1, B2=B2, Mg=Mg, Lg=Lg, C=Cs))
    Ctot = float(np.sqrt(sum(c**2 for o in out for c in o['C'])))
    return Ctot, out

if __name__ == '__main__':
    G = load_delta(); g = '1ae54b'; key = [k for k in G if k.startswith(g)][0]; d = G[key]
    Ctot, per = bound(d['h0'])
    sig, s = signals(d['h0']); mu0 = trajectories(d['h0'])
    rows = []
    for e in EPS:
        h1, _, de = d['near'][F(e).limit_denominator(10**6)]
        R = float(np.linalg.norm((trajectories(h1) - mu0).reshape(-1) - float(de)*s))
        rows.append(dict(eps=e, actual_remainder=R, bound=e**2*Ctot, linear_norm=e*sig['known']))
    res = dict(group=key, C_total=Ctot, s_norm=sig['known'], per_ic=[{k: v for k, v in o.items() if k != 'C'} for o in per],
               eps_rows=rows, eps_linear_10pct=0.1*sig['known']/Ctot)
    json.dump(res, open(HERE/'out'/'remainder.json','w'), indent=1); print(json.dumps(res, indent=1))
