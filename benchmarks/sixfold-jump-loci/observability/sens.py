"""Trajectory sensitivities and efficient-information calculations for the delta-locus family."""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
IC_BENCH = np.array([[-.38,-.31],[-.28,.19],[-.08,-.37],[.12,.33],[.31,-.15],[.39,.26]])
T_BENCH = np.linspace(0., .18, 49)
NOISE = [1e-5, 1e-3, 1e-2]
EPS = [1e-1, 1e-3, 1e-5]

# Weighted J7 library (wt q = 1, wt p = 2): nonconstant weight < 6, plus the weight-6 form; q^6 fixed.
LIB_W = [(1,0),(2,0),(3,0),(4,0),(5,0),(0,1),(1,1),(2,1),(3,1),(0,2),(1,2),(4,1),(2,2),(0,3)]
LIB_D5 = [(i, d-i) for d in range(1, 6) for i in range(d, -1, -1)]   # estimator library of the study
E31 = (3, 1)

def load_delta():
    rows = [json.loads(l) for l in open(ROOT/'reference'/'exact.jsonl')]
    rows = [r for r in rows if r['stratum'] == 'delta']
    groups = {}
    for r in rows:
        groups.setdefault(r['group'], {'split': r['split'], 'near': {}})
        h = {(i, j): F(c) for i, j, c in r['coefficients']}
        if r['least_depth'] == 2: groups[r['group']]['h0'] = h; groups[r['group']]['id0'] = r['id']
        else: groups[r['group']]['near'][abs(F(r['perturbation']['delta']))] = (h, r['id'], F(r['perturbation']['delta']))
    return groups

def fl(h): return {m: float(c) for m, c in h.items() if c}

def _field(h, q, p):
    Hp = sum(c*j*q**i*p**(j-1) for (i,j),c in h.items() if j)
    Hq = sum(c*i*q**(i-1)*p**j for (i,j),c in h.items() if i)
    return Hp, Hq

def _hess(h, q, p):
    Hpq = sum(c*i*j*q**(i-1)*p**(j-1) for (i,j),c in h.items() if i and j)
    Hpp = sum(c*j*(j-1)*q**i*p**(j-2) for (i,j),c in h.items() if j > 1)
    Hqq = sum(c*i*(i-1)*q**(i-2)*p**j for (i,j),c in h.items() if i > 1)
    return Hpq, Hpp, Hqq

def mono_field(m, q, p):
    i, j = m
    return (j*q**i*p**(j-1) if j else 0.*q, -(i*q**(i-1)*p**j) if i else 0.*q)

def trajectories(h, ics=IC_BENCH, t=T_BENCH):
    h = fl(h)
    def rhs(_, y):
        Hp, Hq = _field(h, y[0], y[1]); return [Hp, -Hq]
    out = []
    for y0 in ics:
        s = solve_ivp(rhs, (0, t[-1]), y0, t_eval=t, method='DOP853', atol=1e-13, rtol=1e-12)
        assert s.success and s.y.shape[1] == len(t)
        out.append(s.y.T)
    return np.stack(out)              # [ic, time, 2]

def jacobian(h, lib, ics=IC_BENCH, t=T_BENCH, with_ic=False):
    """Stacked d(observations)/d(coefficients) [and d/d(initial states)] at h, shape [N, K(+2*nic)]."""
    hf = fl(h); K = len(lib); nic = len(ics)
    blocks, ic_blocks = [], []
    for k, y0 in enumerate(ics):
        def rhs(_, y):
            q, p = y[0], y[1]
            Hp, Hq = _field(hf, q, p); Hpq, Hpp, Hqq = _hess(hf, q, p)
            A = np.array([[Hpq, Hpp], [-Hqq, -Hpq]])
            Z = y[2:2+2*K].reshape(2, K); P = y[2+2*K:].reshape(2, 2)
            Gm = np.array([mono_field(m, q, p) for m in lib]).T
            return np.concatenate([[Hp, -Hq], (A@Z + Gm).ravel(), (A@P).ravel()])
        y0a = np.concatenate([y0, np.zeros(2*K), np.eye(2).ravel()])
        s = solve_ivp(rhs, (0, t[-1]), y0a, t_eval=t, method='DOP853', atol=1e-13, rtol=1e-12)
        assert s.success
        Z = s.y[2:2+2*K].T.reshape(len(t), 2, K)          # [time, coord, K]
        P = s.y[2+2*K:].T.reshape(len(t), 2, 2)
        blocks.append(Z.reshape(-1, K))
        icb = np.zeros((len(t)*2, 2*nic)); icb[:, 2*k:2*k+2] = P.reshape(-1, 2); ic_blocks.append(icb)
    Jm = np.vstack(blocks)
    return np.hstack([Jm, np.vstack(ic_blocks)]) if with_ic else Jm

def constraint_grads(h, lib):
    c = lambda i, j: float(h.get((i, j), 0))
    a, b, x, r12, r31 = c(4,1), c(2,2), c(0,3), c(1,2), c(3,1)
    g1 = {(2,2): 2*b, (4,1): -3*x, (0,3): -3*a}
    g2 = {(0,3): 3*r31, (3,1): 3*x, (2,2): -2*r12, (1,2): -2*b}
    rows = [[g.get(m, 0.) for m in lib] for g in (g1, g2)]
    rows += [[1. if m == mm else 0. for m in lib] for mm in lib if mm[0] + 2*mm[1] > 6]
    return np.array(rows)

def nullspace(A, tol=1e-12):
    u, s, vt = np.linalg.svd(A); r = int((s > tol*s[0]).sum()); return vt[r:].T

def generator_tangent(h, lib):
    """Tangent of the benchmark's own delta generator family (x = 1 fixed)."""
    c = lambda i, j: float(h.get((i, j), 0)); b, r12 = c(2,2), c(1,2)
    idx = {m: n for n, m in enumerate(lib)}; vecs = []
    for m in [(1,0),(2,0),(3,0),(0,1),(1,1)]:
        v = np.zeros(len(lib)); v[idx[m]] = 1; vecs.append(v)
    v = np.zeros(len(lib)); v[idx[2,2]] = 1; v[idx[4,1]] = 2*b/3; v[idx[3,1]] = 2*r12/3; vecs.append(v)
    v = np.zeros(len(lib)); v[idx[1,2]] = 1; v[idx[3,1]] = 2*b/3; vecs.append(v)
    return np.array(vecs).T

def efficient(s, N):
    """||(I - P_N) s|| via least squares (N may be rank deficient)."""
    if N.shape[1] == 0: return float(np.linalg.norm(s))
    Q, R = np.linalg.qr(N); d = np.abs(np.diag(R)); Q = Q[:, d > 1e-12*d.max()]
    return float(np.linalg.norm(s - Q@(Q.T@s)))

def signals(h, ics=IC_BENCH, t=T_BENCH):
    """Return dict of first-order signal norms per unit eps for the four information regimes."""
    JW = jacobian(h, LIB_W, ics, t, with_ic=True); K = len(LIB_W)
    Jp, Jic = JW[:, :K], JW[:, K:]
    s = Jp[:, LIB_W.index(E31)]
    T = nullspace(constraint_grads(h, LIB_W)); TG = generator_tangent(h, LIB_W)
    out = {'known': float(np.linalg.norm(s)),
           'generator_family': efficient(s, Jp@TG),
           'J7_locus': efficient(s, Jp@T),
           'J7_locus_unknown_ic': efficient(s, np.hstack([Jp@T, Jic]))}
    # plug-in route of the study: unconstrained degree-5 least squares, then test g2 = 3x r31 - 2 b r12.
    JD = jacobian(h, LIB_D5, ics, t); M = JD.T@JD
    gD = constraint_grads(h, LIB_D5)[1]
    x = float(h[(0,3)]); var = gD@np.linalg.solve(M, gD)   # sigma^2 units
    out['plugin_D5_g2'] = float(3*x/np.sqrt(var))          # signal per unit eps per unit sigma
    out['cond_D5'] = float(np.linalg.cond(JD / np.linalg.norm(JD, axis=0)))
    return out, s
