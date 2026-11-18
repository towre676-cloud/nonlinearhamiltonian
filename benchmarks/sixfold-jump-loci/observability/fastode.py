"""Vectorised fixed-step RK4 for a polynomial Hamiltonian, its parameter sensitivities and its
initial-state sensitivities, over all initial states at once (model integrator for fitting;
the data are generated independently with DOP853)."""
import numpy as np

class Model:
    def __init__(self, lib, t, sub=2):
        self.lib = list(lib); self.t = np.asarray(t); self.sub = sub
        self.terms = self.lib + [(6, 0)]
        I = np.array([m[0] for m in self.terms]); Jx = np.array([m[1] for m in self.terms])
        self.I, self.J = I, Jx
        self.maxi, self.maxj = int(I.max()), int(Jx.max())

    def _pows(self, q, p):
        Q = np.stack([np.ones_like(q)] + [q**k for k in range(1, self.maxi+1)], -1)
        P = np.stack([np.ones_like(p)] + [p**k for k in range(1, self.maxj+1)], -1)
        return Q, P

    def _deriv(self, Q, P, a, b):
        """Per-term values of d^a_q d^b_p (q^i p^j) (without the coefficient), shape [n, terms]."""
        I, J = self.I, self.J
        fa = np.ones(len(I)); fb = np.ones(len(I))
        for k in range(a): fa = fa*(I-k)
        for k in range(b): fb = fb*(J-k)
        ok = (I >= a) & (J >= b)
        ii = np.where(ok, I-a, 0); jj = np.where(ok, J-b, 0)
        return Q[:, ii]*P[:, jj]*(fa*fb*ok)

    def rhs(self, c, y, Z, Phi, want):
        q, p = y[:, 0], y[:, 1]; Q, P = self._pows(q, p)
        Hp = self._deriv(Q, P, 0, 1); Hq = self._deriv(Q, P, 1, 0)
        dy = np.stack([Hp@c, -(Hq@c)], -1)
        if not want: return dy, None, None
        Hpq = self._deriv(Q, P, 1, 1)@c; Hpp = self._deriv(Q, P, 0, 2)@c; Hqq = self._deriv(Q, P, 2, 0)@c
        A = np.empty((len(q), 2, 2)); A[:, 0, 0] = Hpq; A[:, 0, 1] = Hpp; A[:, 1, 0] = -Hqq; A[:, 1, 1] = -Hpq
        G = np.stack([Hp[:, :-1], -Hq[:, :-1]], 1)            # monomial fields of the library, [n, 2, K]
        return dy, A@Z + G, A@Phi

    def solve(self, coef, ics, want=True):
        """coef over lib (q^6 coefficient fixed to 1). Returns X [n, T, 2], dX/dcoef [n,T,2,K], dX/dic [n,T,2,2]."""
        c = np.append(np.asarray(coef, float), 1.0); n = len(ics); K = len(self.lib)
        y = np.array(ics, float); Z = np.zeros((n, 2, K)); Phi = np.repeat(np.eye(2)[None], n, 0)
        X = [y.copy()]; ZS = [Z.copy()]; PS = [Phi.copy()]
        for k in range(len(self.t)-1):
            h = (self.t[k+1]-self.t[k])/self.sub
            for _ in range(self.sub):
                if want:
                    k1 = self.rhs(c, y, Z, Phi, True)
                    k2 = self.rhs(c, y+h/2*k1[0], Z+h/2*k1[1], Phi+h/2*k1[2], True)
                    k3 = self.rhs(c, y+h/2*k2[0], Z+h/2*k2[1], Phi+h/2*k2[2], True)
                    k4 = self.rhs(c, y+h*k3[0], Z+h*k3[1], Phi+h*k3[2], True)
                    Z = Z + h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]); Phi = Phi + h/6*(k1[2]+2*k2[2]+2*k3[2]+k4[2])
                else:
                    k1 = self.rhs(c, y, None, None, False); k2 = self.rhs(c, y+h/2*k1[0], None, None, False)
                    k3 = self.rhs(c, y+h/2*k2[0], None, None, False); k4 = self.rhs(c, y+h*k3[0], None, None, False)
                y = y + h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
                if not np.all(np.isfinite(y)) or np.abs(y).max() > 1e3: raise FloatingPointError('blow-up')
            X.append(y.copy())
            if want: ZS.append(Z.copy()); PS.append(Phi.copy())
        X = np.stack(X, 1)
        if not want: return X
        return X, np.stack(ZS, 1), np.stack(PS, 1)
