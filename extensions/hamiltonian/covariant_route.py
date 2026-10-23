#!/usr/bin/env python3
"""Second, independent proof route for quartic degrees 4k via classical covariants (supplementary).

For a quartic f with Hessian D = f_qq f_pp - f_qp^2 and T = {f, D}, it verifies:
  * the syzygy T^2 = -(16/9) D^3 + I f^2 D + J f^3 and {f, T} = (1/2) dP/dD;
  * the closed form T3(f, f^a D^b) = T [ -(1/3) a(a-1)(4a+1+6b) f^(a-2) D^b
        + (3/16) b(b-1)(2b-1) I f^a D^(b-2) + (3/8) b(b-1)(b-2) J f^(a+1) D^(b-3) ];
  * the companion formula T3(f, T f^a D^b) = P * [same bracket] + sum_{r+s<=2} (a)_r (b)_s
        f^(a-r) D^(b-s) R_rs with 17 covariant constants, solved exactly and overdetermined;
  * for E_{4k} = {Phi(f, D) : T3(f, Phi) = 0}, the top two equations of T3(f, D Phi) = 0 are
        c00 psi0 = 0 with c00 = -I k^2 (4k+1)/2, and c10 psi0 + c11 psi1 = 0 with
        c11 = I (k-1)(72k^3 - 34k^2 - k + 3) / (3 (10 - 12k)),
    checked against direct computation on binary forms for several quartics and k.
The certified theorem itself is checked by check_quartic_uniform.py (monomial route).
Usage: covariant_route.py
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W   # noqa: E402
import qlinalg as L         # noqa: E402

pm, add, sc = W.pmul, W.add, W.scale


def der(g, c, d):
    return W.pder(g, c, d)


def hess(f):
    return add(pm(der(f, 2, 0), der(f, 0, 2)), sc(pm(der(f, 1, 1), der(f, 1, 1)), -1))


def pb(f, g):
    return add(pm(der(f, 1, 0), der(g, 0, 1)), sc(pm(der(f, 0, 1), der(g, 1, 0)), -1))


def T3(f, g):
    return W.act(W.gate(f, 3), g)


def power(a, n):
    r = {(0, 0): F(1)}
    for _ in range(n):
        r = pm(r, a)
    return r


def comb(target, basis):
    keys = sorted(set(target) | {k for b in basis for k in b})
    aug = [[b.get(k, F(0)) for b in basis] + [target.get(k, F(0))] for k in keys]
    red, piv = L.rref(aug, len(basis) + 1)
    if len(basis) in piv:
        return None
    c = [F(0)] * len(basis)
    for i, p in enumerate(piv):
        c[p] = red[i][-1]
    return c


def ff(x, r):
    out = 1
    for t in range(r):
        out *= x - t
    return out


def setup(lam):
    f = W.tidy({(4, 0): F(1), (2, 2): F(lam), (0, 4): F(1)})
    D = hess(f)
    T = pb(f, D)
    a, I, J = comb(pm(T, T), [power(D, 3), pm(power(f, 2), D), power(f, 3)])
    assert a == F(-16, 9)
    return f, D, T, I, J


def mono(f, D, a, b):
    return {} if a < 0 or b < 0 else pm(power(f, a), power(D, b))


def bracket(f, D, I, J, a, b):
    return add(sc(mono(f, D, a - 2, b), F(-a * (a - 1) * (4 * a + 1 + 6 * b), 3)),
               sc(mono(f, D, a, b - 2), F(3, 16) * b * (b - 1) * (2 * b - 1) * I),
               sc(mono(f, D, a + 1, b - 3), F(3, 8) * b * (b - 1) * (b - 2) * J))


RB = {(0, 0): [(0, 1, 1, 0), (1, 0, 0, 1)], (1, 0): [(1, 1, 1, 0), (2, 0, 0, 1)],
      (0, 1): [(0, 2, 1, 0), (2, 0, 2, 0), (1, 1, 0, 1)], (2, 0): [(3, 0, 0, 1), (2, 1, 1, 0), (0, 3, 0, 0)],
      (1, 1): [(1, 2, 1, 0), (2, 1, 0, 1), (3, 0, 2, 0)], (0, 2): [(0, 3, 1, 0), (1, 2, 0, 1), (2, 1, 2, 0), (3, 0, 1, 1)]}


def main():
    report = {}
    # syzygy, {f,T}, closed form of T3(f, f^a D^b)
    for lam in (F(2, 3), F(-7, 5), F(1)):
        f, D, T, I, J = setup(lam)
        assert pb(f, T) == add(sc(power(D, 2), F(-8, 3)), sc(power(f, 2), I / 2))
        for a in range(7):
            for b in range(7 - a):
                assert T3(f, mono(f, D, a, b)) == pm(T, bracket(f, D, I, J, a, b)), (lam, a, b)
    report['T3_closed_form'] = 'verified for a + b <= 6 on three quartics'
    # companion constants R_rs: exact overdetermined solve over four quartics
    unknowns = [(rs, i) for rs in RB for i in range(len(RB[rs]))]
    rows, rhs = [], []
    for lam in (F(1), F(3, 7), F(-5, 2), F(2, 9)):
        f, D, T, I, J = setup(lam)
        P = pm(T, T)
        for a in range(4):
            for b in range(4):
                resid = add(T3(f, pm(T, mono(f, D, a, b))), sc(pm(P, bracket(f, D, I, J, a, b)), -1))
                cols = []
                for (rs, i) in unknowns:
                    (r, s), ex = rs, RB[rs][i]
                    cols.append(sc(mono(f, D, a - r + ex[0], b - s + ex[1]), ff(a, r) * ff(b, s) * I ** ex[2] * J ** ex[3])
                                if a >= r and b >= s else {})
                for k in set(resid) | {k for c in cols for k in c}:
                    rows.append([c.get(k, F(0)) for c in cols])
                    rhs.append(resid.get(k, F(0)))
    red, piv = L.rref([r + [v] for r, v in zip(rows, rhs)], len(unknowns) + 1)
    assert len(unknowns) not in piv and len(piv) == len(unknowns), 'companion system inconsistent or underdetermined'
    report['companion_constants'] = {f'{rs}:{RB[rs][i]}': str(red[j][-1]) for j, (rs, i) in
                                     ((piv.index(u), unknowns[u]) for u in range(len(unknowns)))}
    # top equations in degree 4k versus the closed forms
    checked = 0
    for lam in (F(1), F(-3, 4)):
        f, D, T, I, J = setup(lam)
        for k in (7, 8, 9):
            basis = [mono(f, D, m, k - m) for m in range(k + 1)]
            imgs = [T3(f, x) for x in basis]
            keys = sorted({x for im in imgs for x in im})
            null = L.null_basis([[im.get(x, F(0)) for im in imgs] for x in keys], k + 1)
            assert len(null) == 2
            c00 = -I * k * k * (4 * k + 1) / 2
            c11 = I * (k - 1) * (72 * k ** 3 - 34 * k ** 2 - k + 3) / (3 * (10 - 12 * k))
            for v in null:
                Phi = W.tidy({kk: sum((basis[m].get(kk, F(0)) * c for m, c in enumerate(v)), F(0))
                              for kk in {x for bb in basis for x in bb}})
                out = T3(f, pb(f, Phi))
                cvec = comb(out, [mono(f, D, m, k - m) for m in range(k + 1)])
                assert cvec[0] == c00 * v[0], (lam, k)
                if v[0] == 0:
                    assert cvec[1] == c11 * v[1], (lam, k)
                checked += 1
    report['top_equations'] = f'c00 and c11 closed forms agree with direct computation ({checked} cases)'
    report['status'] = 'passed'
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
