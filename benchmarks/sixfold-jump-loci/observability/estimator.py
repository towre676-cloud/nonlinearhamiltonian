"""Constrained profile-likelihood estimator for the delta locus (J7, weight 1) and the plug-in comparator.
Uses only: the observed tracks, the sample times, the stated noise level, the stratum hypothesis, and
training trajectories (for one prior start). Never sees generating coefficients."""
import sys, numpy as np
from pathlib import Path
from scipy.optimize import least_squares
from numpy.polynomial.legendre import leggauss, legfit, legint, legval, legvander
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
from sens import LIB_W, LIB_D5
from fastode import Model
import identify

FREE = [(1,0),(2,0),(3,0),(4,0),(5,0),(0,1),(1,1),(2,1),(0,2),(1,2)]
IW = {m: n for n, m in enumerate(LIB_W)}; ID5 = {m: n for n, m in enumerate(LIB_D5)}
SETTINGS = dict(method='trf', x_scale='jac', ftol=1e-12, xtol=1e-12, gtol=1e-12, max_nfev=60)
X_BOUNDS = (0.05, 20.0)

# ---------- locus parametrisation: u = (FREE..., beta, x[, eps]) ----------
def theta(u, eps=True):
    b, x = u[10], u[11]; e = u[12] if eps else 0.
    th = np.zeros(len(LIB_W))
    for n, m in enumerate(FREE): th[IW[m]] = u[n]
    th[IW[2,2]] = b; th[IW[0,3]] = x; th[IW[4,1]] = b*b/(3*x); th[IW[3,1]] = 2*b*u[9]/(3*x) + e
    return th

def dtheta(u, eps=True):
    b, x, r12 = u[10], u[11], u[9]; D = np.zeros((len(LIB_W), 13 if eps else 12))
    for n, m in enumerate(FREE): D[IW[m], n] = 1
    D[IW[2,2], 10] = 1; D[IW[0,3], 11] = 1
    D[IW[4,1], 10] = 2*b/(3*x); D[IW[4,1], 11] = -b*b/(3*x*x)
    D[IW[3,1], 9] = 2*b/(3*x); D[IW[3,1], 10] = 2*r12/(3*x); D[IW[3,1], 11] = -2*b*r12/(3*x*x)
    if eps: D[IW[3,1], 12] = 1
    return D

def project(th):
    """Unconstrained weighted-library coefficients -> locus coordinates (with transverse eps)."""
    c = lambda m: th[IW[m]]
    x = float(np.clip(c((0,3)), *X_BOUNDS)); b = c((2,2)); r12 = c((1,2))
    return np.array([c(m) for m in FREE] + [b, x, c((3,1)) - 2*b*r12/(3*x)])

# ---------- observation-based starts ----------
def weak_fit(t, Y, sigma, lib, ridge=0., prior=None):
    """Weak-form least squares (Legendre primitives, as in identify.fit_field) over an arbitrary library."""
    half = (t[-1]-t[0])/2; grid = (t-t[0])/half - 1
    nodes, w = leggauss(5); l, r = grid[:-1], grid[1:]; wd = (r-l)/2
    sample = ((r+l)[:, None]/2 + wd[:, None]*nodes).ravel(); w = (wd[:, None]*w/2).ravel()
    series = legfit(grid, Y.transpose(1, 0, 2).reshape(len(t), -1), 6)
    sm = legval(sample, series).T.reshape(len(sample), len(Y), 2).transpose(1, 0, 2)
    basis = legvander(sample, 6)[:, 1:]; prim = legval(sample, legint(np.eye(7), lbnd=-1)).T[:, 1:]
    nz = np.sqrt(2*np.arange(1, 7)+1)
    mom = -np.einsum('t,tk,stc->skc', w, basis*nz, sm)
    lib6 = list(lib) + [(6, 0)]
    L = np.einsum('t,tk,stcm->skcm', w, half*prim*nz, identify.field_features(sm, lib6))
    A = L[..., :-1].reshape(-1, len(lib)); b = (mom - L[..., -1]).ravel()
    s = np.maximum(np.linalg.norm(A, axis=0), 1e-30); As = A/s
    if ridge:
        p = prior*s; As = np.vstack([As, np.sqrt(ridge)*np.eye(len(lib))]); b = np.concatenate([b, np.sqrt(ridge)*p])
    return np.linalg.lstsq(As, b, rcond=None)[0]/s

def ic_start(t, Y):
    half = (t[-1]-t[0])/2; grid = (t-t[0])/half - 1
    series = legfit(grid, Y.transpose(1, 0, 2).reshape(len(t), -1), 6)
    return legval(-1., series).reshape(len(Y), 2)

def d5_to_w(th5): return np.array([th5[ID5[m]] for m in LIB_W])

# ---------- fitting ----------
class Problem:
    def __init__(self, t, Y, sigma):
        self.t, self.Y, self.sigma = t, Y, sigma; self.n = len(Y)
        self.MW = Model(LIB_W, t); self.MD = Model(LIB_D5, t); self.y = Y.ravel()

    def _split(self, v, k): return v[:k], v[k:].reshape(self.n, 2)

    def res_locus(self, v, eps):
        k = 13 if eps else 12; u, ic = self._split(v, k)
        if not eps: u = np.append(u, 0.)
        try: X = self.MW.solve(theta(u), ic, want=False)
        except FloatingPointError: return np.full(self.y.size, 1e6)
        return (X.ravel() - self.y)/self.sigma

    def jac_locus(self, v, eps):
        k = 13 if eps else 12; u, ic = self._split(v, k)
        uu = u if eps else np.append(u, 0.)
        _, Z, P = self.MW.solve(theta(uu), ic)
        Jt = Z.reshape(self.n, -1, len(LIB_W)); Jc = Jt @ dtheta(uu, eps)
        Ji = np.zeros((self.n, Z.shape[1]*2, 2*self.n))
        for i in range(self.n): Ji[i, :, 2*i:2*i+2] = P[i].reshape(-1, 2)
        return np.concatenate([Jc, Ji], -1).reshape(-1, k + 2*self.n)/self.sigma

    def fit_locus(self, u0, ic0, eps):
        k = 13 if eps else 12; v0 = np.concatenate([u0[:k], ic0.ravel()])
        lo = np.full(v0.size, -np.inf); hi = np.full(v0.size, np.inf); lo[11], hi[11] = X_BOUNDS
        v0[11] = np.clip(v0[11], *X_BOUNDS)
        try:
            r = least_squares(lambda v: self.res_locus(v, eps), v0, jac=lambda v: self.jac_locus(v, eps),
                              bounds=(lo, hi), **SETTINGS)
            return dict(v=r.x, cost=float(r.cost), status=int(r.status), nfev=int(r.nfev), ok=r.status > 0)
        except Exception as e:
            return dict(v=v0, cost=np.inf, status=-99, nfev=0, ok=False, err=repr(e))

    def res_d5(self, v):
        th, ic = self._split(v, len(LIB_D5))
        try: X = self.MD.solve(th, ic, want=False)
        except FloatingPointError: return np.full(self.y.size, 1e6)
        return (X.ravel() - self.y)/self.sigma

    def jac_d5(self, v):
        th, ic = self._split(v, len(LIB_D5)); _, Z, P = self.MD.solve(th, ic); K = len(LIB_D5)
        Ji = np.zeros((self.n, Z.shape[1]*2, 2*self.n))
        for i in range(self.n): Ji[i, :, 2*i:2*i+2] = P[i].reshape(-1, 2)
        return np.concatenate([Z.reshape(self.n, -1, K), Ji], -1).reshape(-1, K + 2*self.n)/self.sigma

def analyse(t, Y, sigma, prior_w):
    """Full constrained profile-likelihood analysis plus plug-in comparator for one observed case."""
    pb = Problem(t, Y, sigma); ic0 = ic_start(t, Y)
    th5 = np.zeros(len(LIB_D5)); w5 = identify.fit_field(t, Y, sigma, 'weak').coefficients
    for n, m in enumerate(identify.TERMS): th5[ID5[m]] = w5[n]
    thw = weak_fit(t, Y, sigma, LIB_W)
    starts = {'weak_D5': project(d5_to_w(th5)), 'weak_W': project(thw),
              'weak_W_ridge': project(weak_fit(t, Y, sigma, LIB_W, ridge=1e-2, prior=prior_w)),
              'train_prior': project(prior_w)}
    fails = 0; m1 = []
    for name, u0 in starts.items():
        f = pb.fit_locus(u0, ic0, True); f['start'] = name; m1.append(f); fails += not f['ok']
    best1 = min(m1, key=lambda f: f['cost'])
    m0 = [pb.fit_locus(best1['v'][:12], best1['v'][13:].reshape(-1, 2), False),
          pb.fit_locus(starts['weak_W'][:12], ic0, False)]
    fails += sum(not f['ok'] for f in m0); best0 = min(m0, key=lambda f: f['cost'])
    re = pb.fit_locus(np.append(best0['v'][:12], 0.), best0['v'][12:].reshape(-1, 2), True)
    fails += not re['ok']
    if re['cost'] < best1['cost']: best1 = re
    v = best1['v']; Jm = pb.jac_locus(v, True); cov = np.linalg.pinv(Jm.T@Jm)
    x, eps = v[11], v[12]; gc = np.zeros(v.size); gc[11] = 36*eps; gc[12] = 36*x
    c_hat = 36*x*eps; se_c = float(np.sqrt(gc@cov@gc))
    lam = 2*(best0['cost'] - best1['cost']); dof = Y.size - v.size
    out = dict(lam=float(lam), c_hat=float(c_hat), se_c=se_c, eps_hat=float(eps), se_eps=float(np.sqrt(cov[12, 12])),
               x_hat=float(x), chi2_red=float(2*best1['cost']/dof), fails=int(fails),
               best_start=best1.get('start', 'refit_from_M0'), inconsistent=bool(lam < -1e-6))
    # plug-in: unconstrained degree-5 nonlinear fit from the study's weak start, Wald test of g2.
    v0 = np.concatenate([th5, ic0.ravel()])
    try:
        r = least_squares(pb.res_d5, v0, jac=pb.jac_d5, **SETTINGS)
        th, Jd = r.x, pb.jac_d5(r.x); cd = np.linalg.pinv(Jd.T@Jd)
        a = lambda m: th[ID5[m]]
        g = np.zeros(r.x.size); g[ID5[0,3]] = 3*a((3,1)); g[ID5[3,1]] = 3*a((0,3)); g[ID5[2,2]] = -2*a((1,2)); g[ID5[1,2]] = -2*a((2,2))
        g2 = 3*a((0,3))*a((3,1)) - 2*a((2,2))*a((1,2))
        out.update(plug_z=float(g2/np.sqrt(g@cd@g)), plug_ok=bool(r.status > 0), plug_chi2_red=float(2*r.cost/(Y.size-r.x.size)))
    except Exception as e:
        out.update(plug_z=float('nan'), plug_ok=False, plug_err=repr(e))
    return out
