#!/usr/bin/env python3
"""Independent checker for per-degree parametric rigidity certificates (quartic-rigidity-v1).

Family H_l = q^4 + l q^2 p^2 + p^4, l in Qbar. Every binary quartic over Qbar with four
distinct roots is GL2(Qbar)-equivalent to a nonzero multiple of some H_l with l^2 != 4 (any
four distinct points of P^1 can be moved to a set {+-r, +-1/r}), and both the static
condition and the dynamic core are GL2-covariant (T_k(F o g, G o g) = det(g)^k T_k(F,G) o g).

For a degree n and depth R the truncated space is
    S_n^R(l) = { G in V_n : T_3(H_l, D^r G) = 0 for r = 0..R },  D = {H_l, .},
and D_inf(H_l)_n is contained in S_n^R(l) (the dynamic core is graded for homogeneous H).
S_n(l) is the kernel of an explicit matrix M_n(l) whose entries are polynomials in l.

Certificate per degree n: several row subsets of M_n with their maximal-minor polynomials,
and a factorization of their gcd g_n with, for each factor f, the exact rank of M_n over
Q[x]/(f). The checker recomputes every minor polynomial from scratch (its own determinant
and Lagrange interpolation), the gcd, the factorization identity and each rank (its own
number-field elimination; a zero divisor met during elimination is a rejection). Then for
EVERY l in Qbar: if g_n(l) != 0, rank M_n(l) is the generic rank; otherwise l is a root of
one declared factor f and rank M_n(l) is the declared rank for f.

Usage: check_quartic_rigidity.py CERT.json
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import weyl_receipts as W  # noqa: E402  (operator arithmetic and gate definitions)

FORMAT = 'quartic-rigidity-v1'


def _lam_act(op_parts, G):
    """Apply sum_k l^k op_k to G = sum_k l^k G_k (lists indexed by the power of l)."""
    out = [dict() for _ in range(len(G) + len(op_parts) - 1)]
    for i, op in enumerate(op_parts):
        for k, g in enumerate(G):
            for e, c in W.act(op, g).items():
                out[i + k][e] = out[i + k].get(e, F(0)) + c
    return [W.tidy(x) for x in out]


def family_matrix_parts(n, depth=1):
    """M_n(l) = sum_k l^k M_k with rows the outputs of C3 D^r, r = 0..depth, on V_n."""
    H0 = {(4, 0): F(1), (0, 4): F(1)}
    H1 = {(2, 2): F(1)}
    Cp, Dp = [W.gate(H0, 3), W.gate(H1, 3)], [W.derivation(H0), W.derivation(H1)]
    keys = [(r, (a, n + 2 * r - 2 - a)) for r in range(depth + 1) for a in range(max(n + 2 * r - 1, 0))]
    index = {k: i for i, k in enumerate(keys)}
    mats = [[[F(0)] * (n + 1) for _ in keys] for _ in range(depth + 2)]
    for a in range(n + 1):
        G = [{(a, n - a): F(1)}]
        for r in range(depth + 1):
            img = _lam_act(Cp, G)
            for k, part in enumerate(img):
                for e, c in part.items():
                    mats[k][index[(r, e)]][a] += c
            G = _lam_act(Dp, G)
    return keys, mats


def row_degree(key):
    return key[0] + 1


def evaluate(mats, x):
    rows, cols = len(mats[0]), len(mats[0][0])
    return [[sum((mats[k][i][j] * x ** k for k in range(len(mats))), F(0)) for j in range(cols)] for i in range(rows)]


def det(M):
    M = [r[:] for r in M]
    n, d = len(M), F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c]), None)
        if p is None:
            return F(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            if f:
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return d


def lagrange(xs, ys):
    """Coefficients (low to high) of the interpolating polynomial."""
    out = [F(0)] * len(xs)
    for i, xi in enumerate(xs):
        basis, denom = [F(1)], F(1)
        for j, xj in enumerate(xs):
            if j != i:
                basis = [F(0)] + basis
                for k in range(len(basis) - 1):
                    basis[k] -= xj * basis[k + 1]
                denom *= xi - xj
        for k, c in enumerate(basis):
            out[k] += ys[i] * c / denom
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def pnorm(p):
    p = [F(c) for c in p]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return pnorm(out)


def pdivmod(a, b):
    a, q = a[:], [F(0)] * max(len(a) - len(b) + 1, 1)
    while len(a) >= len(b) and any(a):
        c, s = a[-1] / b[-1], len(a) - len(b)
        q[s] = c
        for i, x in enumerate(b):
            a[s + i] -= c * x
        a = pnorm(a) if len(a) > 1 else a
        if len(a) == 1 and a[0] == 0:
            break
    return pnorm(q), pnorm(a)


def pgcd(a, b):
    a, b = pnorm(a), pnorm(b)
    while any(b):
        a, b = b, pdivmod(a, b)[1]
    return [c / a[-1] for c in a]


def psub(a, b):
    n = max(len(a), len(b))
    return pnorm([(a[i] if i < len(a) else F(0)) - (b[i] if i < len(b) else F(0)) for i in range(n)])


class NF:
    """Arithmetic in Q[x]/(f); raises on a zero divisor."""
    def __init__(self, f):
        self.f = pnorm(f)
        if len(self.f) < 2:
            raise ValueError('factor must have positive degree')

    def red(self, a):
        a = pnorm(a)
        return pdivmod(a, self.f)[1] if len(a) >= len(self.f) else a

    def mul(self, a, b):
        return self.red(pmul(a, b))

    def inv(self, a):
        r0, r1, s0, s1 = self.f, self.red(a), [F(0)], [F(1)]
        while any(r1):
            q, r = pdivmod(r0, r1)
            r0, r1, s0, s1 = r1, r, s1, psub(s0, pmul(q, s1))
        if len(r0) != 1:
            raise ValueError('zero divisor in Q[x]/(f): the declared factor is reducible')
        return self.red([c / r0[0] for c in s0])


def nf_rank(mats, f):
    K = NF(f)
    M = [[K.red([m[i][j] for m in mats]) for j in range(len(mats[0][0]))] for i in range(len(mats[0]))]
    rank, rows, cols = 0, len(M), len(M[0]) if M else 0
    for c in range(cols):
        p = next((i for i in range(rank, rows) if any(M[i][c])), None)
        if p is None:
            continue
        M[rank], M[p] = M[p], M[rank]
        iv = K.inv(M[rank][c])
        for i in range(rank + 1, rows):
            if any(M[i][c]):
                fac = K.mul(M[i][c], iv)
                M[i] = [K.red(psub(u, K.mul(fac, v))) for u, v in zip(M[i], M[rank])]
        rank += 1
    return rank


def peval(p, x):
    return sum((c * x ** k for k, c in enumerate(p)), F(0))


def check(cert):
    if cert.get('format') != FORMAT or cert.get('family') != 'q^4 + l*q^2*p^2 + p^4':
        raise ValueError('not a quartic-rigidity-v1 certificate for the declared family')
    out = []
    for entry in cert['degrees']:
        n = entry['n']
        depth = entry['depth']
        if type(depth) is not int or depth < 0:
            raise ValueError('depth must be a nonnegative integer')
        keys, mats = family_matrix_parts(n, depth)
        generic = entry['generic_rank']
        g = None
        for rows, minor in zip(entry['row_subsets'], entry['minors']):
            if len(rows) != generic or len(set(rows)) != generic:
                raise ValueError('row subsets must have the generic rank size')
            cols = entry['column_subset']
            deg = sum(row_degree(keys[i]) for i in rows)
            xs = [F(x) for x in range(-(deg // 2) - 1, deg + 2)][:deg + 1]
            ys = [det([[evaluate(mats, x)[i][j] for j in cols] for i in rows]) for x in xs]
            poly = lagrange(xs, ys)
            if poly != pnorm(minor) or not any(poly):
                raise ValueError(f'degree {n}: a declared minor polynomial is wrong or zero')
            g = poly if g is None else pgcd(g, poly)
        g = [c / g[-1] for c in g]
        if pnorm(entry['gcd']) != g:
            raise ValueError(f'degree {n}: gcd of minors is wrong')
        prod = [F(1)]
        for fac in entry['factors']:
            for _ in range(fac['multiplicity']):
                prod = pmul(prod, pnorm(fac['poly']))
        if [c / prod[-1] for c in prod] != g:
            raise ValueError(f'degree {n}: factorization does not reproduce the gcd')
        exceptions = []
        for fac in entry['factors']:
            r = nf_rank(mats, fac['poly'])
            if r != fac['rank']:
                raise ValueError(f'degree {n}: declared rank over a factor is wrong')
            if r < generic:
                exceptions.append({'factor': fac['poly'], 'kernel_dimension': n + 1 - r})
        if generic > n + 1 or len(entry['column_subset']) != generic:
            raise ValueError('bad generic rank')
        # A generic rank below n+1 must come with polynomial kernel vectors v(l), M_n(l) v(l) = 0
        # identically, linearly independent at a sample point; then rank <= generic for every l.
        vecs = [[pnorm(c) for c in v] for v in entry.get('kernel_vectors', [])]
        if len(vecs) != n + 1 - generic:
            raise ValueError('kernel vectors must account for the generic corank')
        for v in vecs:
            dv = max(len(c) for c in v) - 1
            for x in range(dv + 3):
                Mx, vx = evaluate(mats, F(x)), [peval(c, F(x)) for c in v]
                if any(sum((a * b for a, b in zip(row, vx)), F(0)) for row in Mx):
                    raise ValueError('declared kernel vector is not annihilated identically')
        if vecs:
            sample = [[peval(c, F(7, 3)) for c in v] for v in vecs]
            if nf_rank([sample], [F(0), F(1)]) != len(vecs):
                raise ValueError('kernel vectors are dependent')
        out.append({'n': n, 'depth': depth, 'generic_kernel_dimension': n + 1 - generic, 'exceptions': exceptions})
    return {'status': 'passed', 'degrees': out,
            'scope': 'exact for every l in Qbar and each listed degree n; covers every quartic over Qbar with '
                     'distinct roots via GL2 covariance; D_inf(H)_n is contained in S_n'}


if __name__ == '__main__':
    try:
        print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())), indent=1))
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)
