#!/usr/bin/env python3
"""Checker for the monomial dynamic-core theorem in arbitrary exponents (monomial-theorem-v1).

Theorem. Let H = q^a p^b with a >= b >= 0 and d = a + b >= 3 (the case a < b follows by
the swap q <-> p). Over any field of characteristic zero:
  b = 0:          D_inf(H) = Q[q] + p Q[q] + p^2 Q[q]
  b = 1:          D_inf(H) = Q[q] + p Q[q]
  a = b >= 2:     D_inf(H) = Q[qp]
  a > b >= 2:     D_inf(H) = span{1, qp, H}

Proof (checked identities are marked [I1]..[I5]).
 M0 Support. D(q^c p^e) = (a e - b c) q^(c+a-1) p^(e+b-1) and C_k(q^c p^e) =
    psi_k(c, e) q^(c+a-k) p^(e+b-k) with psi_k(x, y) = sum_i (-1)^i C(k,i) (a)_(k-i) (b)_i
    (x)_i (y)_(k-i). Every C_k D^r shifts all exponents by the same vector, so distinct
    monomials have distinct images and D_inf(H) is spanned by the monomials it contains.
    A monomial m = q^c p^e lies in D_inf(H) iff psi_k vanishes at every point
    (c_r, e_r) = (c + r(a-1), e + r(b-1)) of its D-ray for r = 0..r_0, where r_0 is the first
    r with delta_r = (a e - b c) + r (b - a) = 0 (r_0 = infinity if there is none).
 M1 b = 0: psi_k = (a)_k (y)_k [I4 for k = 3]; e decreases along the ray, so e <= 2 survives
    every gate, and e >= 3 fails psi_3 at r = 0 because (a)_3 != 0.
 M2 b = 1: d^2 H / dp^2 = 0, so every term of C_k G contains d^(k-1) G / dp^(k-1) with
    k - 1 >= 2, and e <= 1 survives (e is constant along the ray). For e >= 2,
    psi_3 = a(a-1) y(y-1) [(a-2)(y-2) - 3x] [I3] is linear in r with slope -3a(a-1)^2 e(e-1)
    != 0, so the ray has one point, delta_0 = 0, c = a e, and (a-2)(e-2) - 3ae < 0.
 M3 a = b >= 2: psi_k(x, y) = -psi_k(y, x) for odd k (swap symmetry of T_k; [I5] for
    k = 3, 5, 7), so (qp)^c is killed by every gate and by D. For c != e the ray is
    infinite and psi_3 along it is a polynomial in r whose r^2 coefficient is
    -6 a (a-1)^3 (e - c) != 0 [I1 at b = a]; it has finitely many zeros.
 M4 a > b >= 2: psi_3 along any ray is a cubic in r with leading coefficient
    (a-1)(b-1)(a-b)(a+b-2) != 0 [I1], so at most three points of a ray pass the gate:
    the ray terminates with r_0 <= 2. Its endpoint lies on a e = b c, i.e. it is
    lambda (a, b) with lambda >= 0, and psi_3(lambda a, lambda b) =
    -2ab lambda (a-b)(lambda-1)(lambda(a+b) + a + b - 3) [I2] vanishes only for
    lambda in {0, 1} (the third root is negative for d >= 4). Endpoint 1 forces m = 1;
    endpoint H gives m = H (r_0 = 0), m = qp (r_0 = 1) or negative exponents (r_0 = 2).
    Finally 1, qp and H pass every gate: qp has degree 2 < k, D(qp) = (a - b) H, and
    T_k(H, H) = 0 for odd k.

Usage: check_monomial_theorem.py [CERT.json]
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from math import comb

FORMAT = 'monomial-theorem-v1'
VARS = ('a', 'b', 'c', 'e', 'r', 'l', 'x', 'y')
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
                k = tuple(i + j for i, j in zip(k1, k2))
                nxt[k] = nxt.get(k, F(0)) + v1 * v2
        out = pz(nxt)
    return out


def cst(c):
    return pz({(0,) * NV: F(c)})


def V(name):
    e = [0] * NV
    e[VARS.index(name)] = 1
    return {tuple(e): F(1)}


def lin(*terms):
    """lin(('a', 1), ('b', -1), 2) = a - b + 2."""
    out = {}
    for t in terms:
        out = padd(out, cst(t) if not isinstance(t, tuple) else {k: v * t[1] for k, v in V(t[0]).items()})
    return out


def ff(p, k):
    out = cst(1)
    for i in range(k):
        out = pmul(out, padd(p, cst(-i)))
    return out


def subst(p, name, q):
    """Substitute variable name by polynomial q."""
    i = VARS.index(name)
    out = {}
    cache = {0: cst(1)}
    for k, v in p.items():
        e = k[i]
        while e not in cache:
            top = max(cache)
            cache[top + 1] = pmul(cache[top], q)
        kk = list(k)
        kk[i] = 0
        out = padd(out, pmul({tuple(kk): v}, cache[e]))
    return out


def psi(k, X, Y, A=None, B=None):
    A = A if A is not None else V('a')
    B = B if B is not None else V('b')
    out = {}
    for i in range(k + 1):
        term = pmul(cst((-1) ** i * comb(k, i)), ff(A, k - i), ff(B, i), ff(X, i), ff(Y, k - i))
        out = padd(out, term)
    return out


def coeff_in(p, name):
    i = VARS.index(name)
    out = {}
    for k, v in p.items():
        kk = list(k)
        e = kk[i]
        kk[i] = 0
        out.setdefault(e, {})
        out[e] = padd(out[e], {tuple(kk): v})
    return out


def identities():
    a, b, c, e, r, l, x, y = (V(s) for s in VARS)
    res = {}
    # I1: psi_3 along the D-ray
    ray = psi(3, padd(c, pmul(r, lin(('a', 1), -1))), padd(e, pmul(r, lin(('b', 1), -1))))
    co = coeff_in(ray, 'r')
    lead = pmul(lin(('a', 1), -1), lin(('b', 1), -1), lin(('a', 1), ('b', -1)), lin(('a', 1), ('b', 1), -2))
    sub = pmul(cst(-3), lin(('a', 1), -1), lin(('b', 1), -1), lin(('a', 1), ('b', 1), -2),
               padd(pmul(a, e), pmul(cst(-1), b, c), lin(('a', -1), ('b', 1))))
    res['I1'] = co.get(3, {}) == lead and co.get(2, {}) == sub and max(co) == 3
    # I1 at b = a: r^2 coefficient -6 a (a-1)^3 (e - c), r^3 coefficient 0
    co_bb = {k: subst(v, 'b', a) for k, v in co.items()}
    res['I1_balanced'] = (co_bb.get(3, {}) == {} and
                          co_bb.get(2, {}) == pmul(cst(-6), a, ff(lin(('a', 1), -1), 1), lin(('a', 1), -1),
                                                   lin(('a', 1), -1), lin(('e', 1), ('c', -1))))
    # I2: psi_3 on the power line
    pw = psi(3, pmul(l, a), pmul(l, b))
    res['I2'] = pw == pmul(cst(-2), a, b, l, lin(('a', 1), ('b', -1)), lin(('l', 1), -1),
                           padd(pmul(l, lin(('a', 1), ('b', 1))), lin(('a', 1), ('b', 1), -3)))
    # I3: b = 1
    res['I3'] = psi(3, x, y, B=cst(1)) == pmul(a, lin(('a', 1), -1), y, lin(('y', 1), -1),
                                              padd(pmul(lin(('a', 1), -2), lin(('y', 1), -2)), pmul(cst(-3), x)))
    # I4: b = 0
    res['I4'] = psi(3, x, y, B=cst(0)) == pmul(ff(a, 3), ff(y, 3))
    # I5: antisymmetry for a = b, odd k = 3, 5, 7
    res['I5'] = all(padd(psi(k, x, y, B=a), psi(k, y, x, B=a)) == {} for k in (3, 5, 7))
    return res


def check(cert=None):
    if cert is not None and cert.get('format') != FORMAT:
        raise ValueError('not a monomial-theorem-v1 certificate')
    res = identities()
    bad = [k for k, ok in res.items() if not ok]
    if bad:
        raise ValueError(f'identities fail: {bad}')
    if cert is not None and cert.get('identities') != sorted(res):
        raise ValueError('certificate lists other identities')
    return {'status': 'passed', 'identities': sorted(res),
            'theorem': 'for H = q^a p^b, a >= b, a + b >= 3: D_inf = (+)_{j<=2} p^j Q[q] (b = 0), Q[q] + pQ[q] '
                       '(b = 1), Q[qp] (a = b), span{1, qp, H} (a > b >= 2)',
            'active_part': 'p Q[q] + p^2 Q[q] (b = 0); D_inf / span{1, H} (b = 1); 0 (a = b); Q qp (a > b >= 2)'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
