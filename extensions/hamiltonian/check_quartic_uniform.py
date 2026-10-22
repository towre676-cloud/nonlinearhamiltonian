#!/usr/bin/env python3
"""Independent checker for the all-degree quartic theorem (quartic-uniform-v1).

Theorem. For every binary quartic H over an algebraically closed field of characteristic
zero with four distinct roots, D_inf(H) = span{1, H}. (Over Q the same holds by descent.)

Proof structure checked here.
 1. Normal form: H ~ c * H_l, H_l = q^4 + l q^2 p^2 + p^4, l^2 != 4 (four distinct points of
    P^1 can be moved to {+-r, +-1/r}); D_inf is GL2-covariant and graded for homogeneous H.
 2. D_inf(H)_n lies in S_n = {G in V_n : T3(H,G) = 0, T3(H,{H,G}) = 0}.
 3. In V_n write G = sum_t h_t q^(n-t) p^t. Both T3(H_l, .) and D = {H_l, .} move t by odd
    amounts, so S_n splits into the two parity classes of t. The static condition at output
    index t gives the exact recurrence
        24(t+3)(t+2)(t+1) h_(t+3) + 12 l (n-1-t)(t+1)(n-2-2t) h_(t+1)
                                       - 24 (n+1-t)(n-t)(n-1-t) h_(t-1) = 0,
    so every h_t is determined by the top coefficients h_0, h_2 (even class) and h_1 (odd).
 4. D G has coefficients d_s = 4(s+1) h_(s+1) + 2 l (2s - 2 - n) h_(s-1) - 4 (n-s+3) h_(s-3)
    in degree n+2, and the top equations of T3(H_l, D G) = 0 are linear forms in the free
    top coefficients with coefficients polynomial in (n, l). These are re-derived here from
    the three formulas above with this file's own polynomial arithmetic.
 5. Odd class: the formal resultant R1(n) = Res_l(c_1, c_3) is a nonzero polynomial whose
    integer roots are all <= 3, so for every integer n >= 4 the two coefficients of h_1 have
    no common root l: h_1 = 0. Even class: the minors m01, m02 of the 2x2 system in (h_0, h_2)
    are divisible by l^2 - 4, and R2(n) = Res_l(m01/(l^2-4), m02/(l^2-4)) has integer roots
    only <= 4: for l^2 != 4, h_0 = h_2 = 0. A nonzero formal Sylvester resultant excludes a
    common factor whether or not a leading coefficient vanishes.
 6. The formulas of step 4 use coefficient indices that exist once n >= threshold; for
    smaller n the embedded per-degree certificate (quartic-rigidity-v1) applies.
Usage: check_quartic_uniform.py CERT.json
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_quartic_rigidity as R  # noqa: E402  (per-degree checker for small n)

FORMAT = 'quartic-uniform-v1'
# The top equations use h_t for t <= 8 (from the static recurrence at output indices <= 5) and
# d_s for s <= 7; every one of these coefficients exists exactly when n >= 8.
VALIDITY = 8

# ---- polynomials in (n, l): dict {(en, el): F} ----------------------------------------


def pz(d):
    return {k: F(v) for k, v in d.items() if v}


def padd(*xs):
    out = {}
    for x in xs:
        for k, v in x.items():
            out[k] = out.get(k, F(0)) + v
    return pz(out)


def pmul(a, b):
    out = {}
    for (i, j), u in a.items():
        for (k, l), v in b.items():
            out[(i + k, j + l)] = out.get((i + k, j + l), F(0)) + u * v
    return pz(out)


def psc(a, c):
    return pz({k: v * c for k, v in a.items()})


N = {(1, 0): F(1)}
LAM = {(0, 1): F(1)}


def cst(c):
    return pz({(0, 0): F(c)})


def lin(c0, cn=0):              # c0 + cn * n
    return pz({(0, 0): F(c0), (1, 0): F(cn)})


class Lin:
    """A linear form in the free top coefficients with polynomial coefficients over a common
    rational denominator: {param: poly} / den (den a nonzero rational)."""
    def __init__(self, coef=None, den=F(1)):
        self.coef, self.den = coef or {}, F(den)

    def scale(self, poly):
        return Lin({p: pmul(v, poly) for p, v in self.coef.items()}, self.den)

    def plus(self, other):
        a, b = self.den, other.den
        coef = {}
        for p in set(self.coef) | set(other.coef):
            coef[p] = padd(psc(self.coef.get(p, {}), b), psc(other.coef.get(p, {}), a))
        return Lin(coef, a * b)

    def div(self, c):
        return Lin(self.coef, self.den * c)


def top_equations(free, n_h=16, n_d=13, eq_ts=(0, 1, 2, 3, 4)):
    h = {t: Lin({t: cst(1)}) for t in free}
    zero = Lin()
    for t in range(n_h):
        if t + 3 in h:
            continue
        B = psc(pmul(pmul(LAM, lin(-1 - t, 1)), lin(-2 - 2 * t, 1)), 12 * (t + 1))
        C = psc(pmul(pmul(lin(1 - t, 1), lin(-t, 1)), lin(-1 - t, 1)), -24)
        acc = h.get(t + 1, zero).scale(B).plus(h.get(t - 1, zero).scale(C))
        h[t + 3] = acc.scale(cst(-1)).div(24 * (t + 3) * (t + 2) * (t + 1))
    d = {}
    for s in range(n_d):
        t1 = h.get(s + 1, zero).scale(cst(4 * (s + 1)))
        t2 = h.get(s - 1, zero).scale(psc(pmul(LAM, lin(2 * s - 2, -1)), 2))
        t3 = h.get(s - 3, zero).scale(lin(-4 * (3 - s), -4))       # -4 (n - s + 3)
        d[s] = t1.plus(t2).plus(t3)
    eqs = {}
    for t in eq_ts:
        A = cst(24 * (t + 3) * (t + 2) * (t + 1))
        B = psc(pmul(pmul(LAM, lin(1 - t, 1)), lin(-2 * t, 1)), 12 * (t + 1))
        C = psc(pmul(pmul(lin(3 - t, 1), lin(2 - t, 1)), lin(1 - t, 1)), -24)
        e = d.get(t + 3, zero).scale(A).plus(d.get(t + 1, zero).scale(B)).plus(d.get(t - 1, zero).scale(C))
        eqs[t] = e
    return eqs


# ---- univariate helpers --------------------------------------------------------------------

def in_l(p, nv):
    out = {}
    for (a, b), v in p.items():
        out[b] = out.get(b, F(0)) + v * F(nv) ** a
    deg = max([b for b, v in out.items() if v], default=-1)
    return [out.get(i, F(0)) for i in range(deg + 1)]


def formal_in_l(p, nv, deg):
    v = in_l(p, nv)
    return v + [F(0)] * (deg + 1 - len(v))


def det(M):
    M = [r[:] for r in M]
    n, dd = len(M), F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c]), None)
        if p is None:
            return F(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            dd = -dd
        dd *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            if f:
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return dd


def sylvester(a, b):
    """Formal resultant of a, b given with formal degrees len-1."""
    da, db = len(a) - 1, len(b) - 1
    size = da + db
    rows = [[F(0)] * i + list(reversed(a)) + [F(0)] * (size - da - 1 - i) for i in range(db)]
    rows += [[F(0)] * i + list(reversed(b)) + [F(0)] * (size - db - 1 - i) for i in range(da)]
    return det(rows)


def degs(p):
    return max((b for (a, b) in p), default=-1), max((a for (a, b) in p), default=-1)


def lagrange(xs, ys):
    out = [F(0)] * len(xs)
    for i, xi in enumerate(xs):
        basis, den = [F(1)], F(1)
        for j, xj in enumerate(xs):
            if j != i:
                basis = [F(0)] + basis
                for k in range(len(basis) - 1):
                    basis[k] -= xj * basis[k + 1]
                den *= xi - xj
        for k, c in enumerate(basis):
            out[k] += ys[i] * c / den
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def divide_by_l2m4(p):
    """Exact division of p(n, l) by l^2 - 4; raises if not divisible."""
    by_n = {}
    for (a, b), v in p.items():
        by_n.setdefault(a, {})[b] = v
    out = {}
    for a, u in by_n.items():
        deg = max(u)
        r = dict(u)
        for e in range(deg, 1, -1):
            c = r.get(e, F(0))
            if c:
                out[(a, e - 2)] = out.get((a, e - 2), F(0)) + c
                r[e] = r.get(e, F(0)) - c
                r[e - 2] = r.get(e - 2, F(0)) + 4 * c
        if any(v for v in r.values()):
            raise ValueError('minor is not divisible by l^2 - 4')
    return pz(out)


def integer_roots(poly):
    """All integer roots of a nonzero rational univariate polynomial (exact)."""
    p = [F(c) for c in poly]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    roots = []
    ev = lambda q, x: sum((c * F(x) ** i for i, c in enumerate(q)), F(0))
    changed = True
    while changed and len(p) > 1:
        changed = False
        for r in range(-64, 65):
            if ev(p, r) == 0:
                out, carry = [F(0)] * (len(p) - 1), F(0)
                for i in range(len(p) - 1, 0, -1):
                    carry = p[i] + carry * r
                    out[i - 1] = carry
                p, changed = out, True
                roots.append(r)
                break
    if len(p) > 1:
        d = len(p) - 1
        bound = 2 * max(abs(p[d - i] / p[d]) ** (1.0 / i) for i in range(1, d + 1)) + 2
        den = 1
        for c in p:
            den = den * c.denominator // gcd(den, c.denominator)
        ip = [int(c * den) for c in p]
        for x in range(-int(bound) - 1, int(bound) + 2):
            acc = 0
            for c in reversed(ip):
                acc = acc * x + c
            if acc == 0:
                roots.append(x)
    return sorted(roots)


def resultant_poly(a, b, deg_bound):
    dla, _ = degs(a)
    dlb, _ = degs(b)
    xs = list(range(1000, 1000 + deg_bound + 3))
    ys = [sylvester(formal_in_l(a, x, dla), formal_in_l(b, x, dlb)) for x in xs]
    return lagrange([F(x) for x in xs], ys)


def check(cert):
    if cert.get('format') != FORMAT or cert.get('family') != 'q^4 + l*q^2*p^2 + p^4':
        raise ValueError('not a quartic-uniform-v1 certificate')
    thr = cert['threshold']
    if type(thr) is not int or thr < VALIDITY:
        raise ValueError(f'threshold must be at least {VALIDITY}, where the symbolic top equations are exact')
    odd = top_equations([1])
    even = top_equations([0, 2])
    c1, c3 = odd[1].coef.get(1, {}), odd[3].coef.get(1, {})
    rows = [(even[t].coef.get(0, {}), even[t].coef.get(2, {})) for t in (0, 2, 4)]
    if [c1, c3] != [pz({tuple(k): F(v) for k, v in x}) for x in cert['odd_coefficients']]:  # noqa: E501
        raise ValueError('declared odd-class coefficients differ from the re-derived ones')
    m01 = padd(pmul(rows[0][0], rows[1][1]), psc(pmul(rows[1][0], rows[0][1]), -1))
    m02 = padd(pmul(rows[0][0], rows[2][1]), psc(pmul(rows[2][0], rows[0][1]), -1))
    r01, r02 = divide_by_l2m4(m01), divide_by_l2m4(m02)
    # resultant degree bounds from the Sylvester structure
    (dl1, dn1), (dl3, dn3) = degs(c1), degs(c3)
    (da, dna), (db, dnb) = degs(r01), degs(r02)
    R1 = resultant_poly(c1, c3, dl3 * dn1 + dl1 * dn3)
    R2 = resultant_poly(r01, r02, db * dna + da * dnb)
    if [str(c) for c in R1] != cert['R1'] or [str(c) for c in R2] != cert['R2']:
        raise ValueError('declared resultants differ from the recomputed ones')
    if len(R1) < 2 and not any(R1) or len(R2) < 2 and not any(R2):
        raise ValueError('a resultant vanishes identically')
    roots1, roots2 = integer_roots(R1), integer_roots(R2)
    top_root = max(roots1 + roots2)
    if top_root >= thr:
        raise ValueError('a resultant has an integer root at or above the threshold')
    small = cert['small_degree_certificate']
    res = R.check(small)
    covered = {d['n'] for d in res['degrees']}
    if not set(range(1, thr)) <= covered:
        raise ValueError('the per-degree certificate does not cover all degrees below the threshold')
    for d in res['degrees']:
        if d['n'] < thr:
            want = 1 if d['n'] == 4 else 0
            if d['generic_kernel_dimension'] != want or any(e['factor'] != ['-4', '0', '1'] for e in d['exceptions']):
                raise ValueError(f"degree {d['n']}: unexpected kernel or exceptional factor")
    return {'status': 'passed', 'theorem': 'D_inf(H) = span{1, H} for every binary quartic with distinct roots',
            'threshold': thr, 'R1_integer_roots': roots1, 'R2_integer_roots': roots2,
            'small_degrees_certified': sorted(covered),
            'scope': 'all polynomial degrees, every quartic over an algebraically closed field of characteristic '
                     'zero with distinct roots; over Q by descent'}


if __name__ == '__main__':
    try:
        print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())), indent=1))
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)
