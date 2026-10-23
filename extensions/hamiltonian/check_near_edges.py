#!/usr/bin/env python3
"""Checker for near-top rigidity (near-edge-v1).

Theorem NE. Let H be a polynomial whose top homogeneous part is c l^(d-1) m (d >= 3) and
which is not affine in m. Then D_inf(H) = span{1, H}.

Proof (checked identities [E1]..[E4]).
 1. Coordinates (m, l). Every monomial of H other than the top m l^(d-1) with m-exponent
    <= 1 lies strictly inside, so for the weights w_t = (1, t) on (m, l) the top vertex is
    first joined, as t decreases from 1, by monomials of m-exponent >= 2: the first edge
    E = m l^(d-1) + sum_{s>=1} e_s m^(1+sa) l^(d-1-sb), with b > a >= 1 coprime (total degree
    drops along the edge). By the top-weight lemma for w_t on the edge, gr D_inf(H) embeds
    in D_inf(E); it suffices to show D_inf(E) is finite-dimensional, and Lemma F
    (DYNAMIC_CORE_RESULTS.md section 6.6) then gives span{1, H}.
 2. D_inf(E) is graded by the edge weight; a homogeneous element G has total-degree top in
    V = K[l] + m K[l] (monomial theorem), i.e. starts with g l^N (type alpha) or
    g m l^(N-1) (type beta), and its monomials lie on a line of step (a, -b). Let t be the
    first step with e_t != 0. For large N the T_3 recurrence forces the coefficients of G
    strictly between steps 0 and t to vanish, and the step-t components of T_3(E, G) and
    T_3(E, {E, G}) are linear in (y, e_t g), y the step-t coefficient of G:
    [E1] type alpha: determinant
         N a^2 t^2 (d-2)(d-1)(at-1)^2 (at+1) C_alpha,  C_alpha cubic in N with leading
         coefficient 3(at(d-1) + bt + 2d - 4) > 0;
    [E2] type beta: determinant a^2 t^2 (d-N)(d-2)(d-1)(at+1)^2 C_beta with leading
         coefficient -3(at-1)(at(d-1) + bt + 2d - 4) of N^3, and for at = 1
         36 (d-N)(b-1)(d-2)(d-1) C'_beta with leading coefficient -(b+d-1) of N^2;
    [E3] type alpha with a = t = 1 (the only degenerate case): at step 2 the components of
         T_3(E, D^r G), r = 0..3, are linear in (y_2, e_1 y_1, e_2 g, e_1^2 g) with a 4x4
         determinant 10368 N^2 (b-1)^3 (d-2)^2 (d-1)(N+d-2)(b+d-1)(b+d-1-N) Q, Q quartic in N
         with leading coefficient
         -[2b^3 + b^2(7d-8) + 2b(4d-5)(d-1) + (d-1)^2(3d-4)] < 0;
         so e_1^2 g = 0 with e_1 != 0, i.e. g = 0.
    In every case g = 0, contradicting the choice of the top: homogeneous elements of
    D_inf(E) have bounded degree, so D_inf(E) is finite-dimensional.
 4. [E4] The gate and bracket conventions agree with weyl_receipts on sample points.

Usage: check_near_edges.py [CERT.json]
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)]

FORMAT = 'near-edge-v1'
VARS = ('N', 'd', 'a', 'b', 't', 'X0', 'X1', 'X2', 'X3')   # X* mark the unknowns
NV = len(VARS)


def pz(p):
    return {k: v for k, v in p.items() if v}


def padd(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return pz(out)


def pmul(*ps):
    out = {(0,) * NV: F(1)}
    for p in ps:
        nxt = {}
        for k1, v1 in out.items():
            for k2, v2 in p.items():
                k = tuple(x + y for x, y in zip(k1, k2))
                nxt[k] = nxt.get(k, F(0)) + v1 * v2
        out = pz(nxt)
    return out


def cst(c):
    return pz({(0,) * NV: F(c)})


def V(s):
    e = [0] * NV
    e[VARS.index(s)] = 1
    return {tuple(e): F(1)}


def lin(**kw):
    out = cst(kw.pop('c', 0))
    for s, c in kw.items():
        out = padd(out, pmul(cst(c), V(s)))
    return out


def ff(p, k):
    out = cst(1)
    for i in range(k):
        out = pmul(out, padd(p, cst(-i)))
    return out


def gate3(A, B, x, z):
    out = {}
    for l in range(4):
        out = padd(out, pmul(cst((-1) ** l * comb(3, l)), ff(A, 3 - l), ff(B, l), ff(x, l), ff(z, 3 - l)))
    return out


def br(A, B, x, z):
    return padd(pmul(A, z), pmul(cst(-1), B, x))


# monomials: (m-exponent, l-exponent, coefficient, step)
def T3(Fm, Gm, maxstep):
    out = {}
    for (A, B, c, s) in Fm:
        for (x, z, e, u) in Gm:
            if s + u <= maxstep:
                out[s + u] = padd(out.get(s + u, {}), pmul(c, e, gate3(A, B, x, z)))
    return out


def Dop(Fm, Gm, maxstep):
    acc = {}
    for (A, B, c, s) in Fm:
        for (x, z, e, u) in Gm:
            if s + u <= maxstep:
                key = s + u
                mexp, lexp = padd(A, x, cst(-1)), padd(B, z, cst(-1))
                acc.setdefault(key, [mexp, lexp, {}])
                acc[key][2] = padd(acc[key][2], pmul(c, e, br(A, B, x, z)))
    return [(m, l, c, s) for s, (m, l, c) in acc.items()]


def coeff(p, s):
    i = VARS.index(s)
    return pz({tuple(0 if j == i else v for j, v in enumerate(k)): c for k, c in p.items() if k[i] == 1})


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    out = {}
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        out = padd(out, pmul(cst((-1) ** j), M[0][j], det(minor)))
    return out


def first_order(kind, at_one=False):
    """2x2 determinant for type alpha / beta; edge step (a, -b), first perturbation at step t."""
    N, d, a, b, t = (V(s) for s in ('N', 'd', 'a', 'b', 't'))
    if at_one:
        a = t = cst(1)
    ta, tb = pmul(t, a), pmul(t, b)
    Hm = [(cst(1), padd(d, cst(-1)), cst(1), 0),
          (padd(cst(1), ta), padd(d, cst(-1), pmul(cst(-1), tb)), V('X3'), 1)]   # X3 = e_t
    if kind == 'alpha':
        Gm = [(cst(0), N, V('X0'), 0), (ta, padd(N, pmul(cst(-1), tb)), V('X1'), 1)]
    else:
        Gm = [(cst(1), padd(N, cst(-1)), V('X0'), 0),
              (padd(cst(1), ta), padd(N, cst(-1), pmul(cst(-1), tb)), V('X1'), 1)]
    e1 = T3(Hm, Gm, 1).get(1, {})
    e2 = T3(Hm, Dop(Hm, Gm, 1), 1).get(1, {})
    rows = [[coeff(E, 'X1'), coeff(coeff(E, 'X3'), 'X0')] for E in (e1, e2)]
    return det(rows)


def second_order():
    N, d, b = V('N'), V('d'), V('b')
    neg = lambda p: pmul(cst(-1), p)
    e1, e2 = V('X2'), V('X3')
    g0, y1, y2 = V('X0'), V('X1'), V('t')        # reuse slot 't' for y2 (t = 1 here)
    Hm = [(cst(1), padd(d, cst(-1)), cst(1), 0), (cst(2), padd(d, cst(-1), neg(b)), e1, 1),
          (cst(3), padd(d, cst(-1), pmul(cst(-2), b)), e2, 2)]
    Gm = [(cst(0), N, g0, 0), (cst(1), padd(N, neg(b)), y1, 1), (cst(2), padd(N, pmul(cst(-2), b)), y2, 2)]
    rows, Gr = [], Gm
    for r in range(4):
        ex = T3(Hm, Gr, 2).get(2, {})
        row = [coeff(ex, 't'), coeff(coeff(ex, 'X2'), 'X1'), coeff(coeff(ex, 'X3'), 'X0'),
               pz({k[:VARS.index('X2')] + (0,) + k[VARS.index('X2') + 1:]: v for k, v in coeff(ex, 'X0').items()
                   if k[VARS.index('X2')] == 2})]
        # verify that ex is exactly the claimed linear combination
        recon = padd(pmul(row[0], y2), pmul(row[1], e1, y1), pmul(row[2], e2, g0), pmul(row[3], e1, e1, g0))
        if recon != ex:
            raise ValueError('second-order equations are not linear in (y2, e1 y1, e2 g, e1^2 g)')
        rows.append(row)
        Gr = Dop(Hm, Gr, 2)
    return det(rows)


def lead_in_N(p):
    i = VARS.index('N')
    top = max(k[i] for k in p)
    return top, pz({k[:i] + (0,) + k[i + 1:]: v for k, v in p.items() if k[i] == top})


def divide_check(P, factors, name):
    prod = cst(1)
    for f in factors:
        prod = pmul(prod, f)
    # P = prod * C for the declared C: recover C by matching leading behaviour via exact division
    q, r = pdivide(P, prod)
    if r:
        raise ValueError(f'{name}: declared factors do not divide the determinant')
    return q


def pdivide(P, D):
    """Exact multivariate division by repeated leading-term elimination (lex on VARS)."""
    P = dict(P)
    q = {}
    lead = lambda p: max(p)
    dl = lead(D)
    while P:
        pl = lead(P)
        if any(x < y for x, y in zip(pl, dl)):
            return q, P
        mono = tuple(x - y for x, y in zip(pl, dl))
        c = P[pl] / D[dl]
        q[mono] = q.get(mono, F(0)) + c
        P = padd(P, pmul({mono: -c}, D))
    return pz(q), {}


def grid():
    import weyl_receipts as W
    n = 0
    for (A, B) in ((1, 5), (2, 3), (4, 1)):
        Hm = {(A, B): F(1)}
        C3, Dm = W.gate(Hm, 3), W.derivation(Hm)
        for x in range(0, 5):
            for z in range(0, 5):
                img = W.act(C3, {(x, z): F(1)})
                want = sum((-1) ** l * comb(3, l) * _ff(A, 3 - l) * _ff(B, l) * _ff(x, l) * _ff(z, 3 - l)
                           for l in range(4))
                if img.get((A + x - 3, B + z - 3), F(0)) != want:
                    return False, n
                imgd = W.act(Dm, {(x, z): F(1)})
                if imgd.get((A + x - 1, B + z - 1), F(0)) != A * z - B * x:
                    return False, n
                n += 2
    return True, n


def _ff(z, k):
    out = 1
    for i in range(k):
        out *= z - i
    return out


def check(cert=None):
    if cert is not None and cert.get('format') != FORMAT:
        raise ValueError('not a near-edge-v1 certificate')
    N, d, a, b, t = (V(s) for s in ('N', 'd', 'a', 'b', 't'))
    at, bt = pmul(a, t), pmul(b, t)
    res = {}
    # [E1]
    Da = first_order('alpha')
    Ca = divide_check(Da, [N, a, a, t, t, padd(d, cst(-2)), padd(d, cst(-1)), padd(at, cst(-1)), padd(at, cst(-1)),
                           padd(at, cst(1))], 'E1')
    deg, lc = lead_in_N(Ca)
    res['E1'] = deg == 3 and lc == pmul(cst(3), padd(pmul(at, padd(d, cst(-1))), bt, pmul(cst(2), d), cst(-4)))
    # [E2]
    Db = first_order('beta')
    Cb = divide_check(Db, [a, a, t, t, padd(d, pmul(cst(-1), N)), padd(d, cst(-2)), padd(d, cst(-1)), padd(at, cst(1)),
                           padd(at, cst(1))], 'E2')
    deg, lc = lead_in_N(Cb)
    res['E2'] = deg == 3 and lc == pmul(cst(-3), padd(at, cst(-1)),
                                        padd(pmul(at, padd(d, cst(-1))), bt, pmul(cst(2), d), cst(-4)))
    Db1 = first_order('beta', at_one=True)
    Cb1 = divide_check(Db1, [cst(36), padd(d, pmul(cst(-1), N)), padd(b, cst(-1)), padd(d, cst(-2)), padd(d, cst(-1))],
                       'E2b')
    deg, lc = lead_in_N(Cb1)
    res['E2_at1'] = deg == 2 and lc == pmul(cst(-1), padd(b, d, cst(-1)))
    # [E3]
    D2 = second_order()
    Q = divide_check(D2, [cst(10368), N, N, padd(b, cst(-1)), padd(b, cst(-1)), padd(b, cst(-1)), padd(d, cst(-2)),
                          padd(d, cst(-2)), padd(d, cst(-1)), padd(N, d, cst(-2)), padd(b, d, cst(-1)),
                          padd(b, d, cst(-1), pmul(cst(-1), N))], 'E3')
    deg, lc = lead_in_N(Q)
    want = pmul(cst(-1), padd(pmul(cst(2), b, b, b), pmul(b, b, padd(pmul(cst(7), d), cst(-8))),
                              pmul(cst(2), b, padd(pmul(cst(4), d), cst(-5)), padd(d, cst(-1))),
                              pmul(padd(d, cst(-1)), padd(d, cst(-1)), padd(pmul(cst(3), d), cst(-4)))))
    res['E3'] = deg == 4 and lc == want
    ok, n = grid()
    res['E4'] = ok
    bad = [k for k, v in res.items() if not v]
    if bad:
        raise ValueError(f'identities fail: {bad}')
    if cert is not None and cert.get('identities') != sorted(res):
        raise ValueError('certificate lists other identities')
    return {'status': 'passed', 'identities': sorted(res), 'grid_points': n,
            'theorem': 'every polynomial with top c l^(d-1) m that is not affine in m has D_inf = span{1, H}'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
