#!/usr/bin/env python3
"""Independent checker for all-degree polynomial-kernel claims (weyl-kernel-v1).

A weyl-kernel-v1 object wraps a weyl-invariant-kernel-v1 receipt (replayed by
weyl_receipts.verify_certificate, which proves that the polynomial common kernel
of the receipt generators P_i is the full dynamic core) and adds a *support
certificate* that determines that common kernel in all degrees.

Mathematics. Call P monomial-acting when all its normally ordered terms
q^a' p^b' dq^c dp^d share one shift (a'-c, b'-d). Then P q^a p^b = psi(a,b) q^(a+da) p^(b+db)
with psi(a,b) = sum coef * (a)_c (b)_d, and distinct monomials go to distinct
monomials, so P G = 0 iff supp G lies in Z(psi) = {(a,b) in N^2 : psi(a,b) = 0}.
Write psi_i = g * phi_i for a common factor g that is a product of linear forms
(its zeros are lines, arithmetic progressions or finitely many points). If
sum_i lambda_i phi_i = U(a) V(b) with U, V nonzero, every common zero of the phi_i lies on a
vertical line a = a0 with U(a0) = 0 or a horizontal line b = b0 with V(b0) = 0. On each
such line the checker restricts all psi_i and either finds the whole line or the
finitely many integer roots. That gives Z exactly, as lines plus points.

Claims accepted:
  'monomial_span'  every generator is monomial-acting; kernel = span of monomials in Z.
  'finite_support' Z (from the declared monomial subset) is finite; kernel is computed
                   by exact linear algebra on span(Z) against ALL generators.
Anything else is rejected; the checker never infers a classification from a window.
Usage: check_weyl_kernel.py KERNEL.json
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import weyl_receipts as W  # noqa: E402  (the receipt checker; no discovery code)

FORMAT = 'weyl-kernel-v1'


# --- bivariate / univariate exact polynomials, own implementation -------------

def padd(x, y, s=F(1)):
    out = dict(x)
    for k, v in y.items():
        out[k] = out.get(k, F(0)) + s * v
    return {k: v for k, v in out.items() if v}


def pmul(x, y):
    out = {}
    for (i, j), u in x.items():
        for (k, l), v in y.items():
            out[(i + k, j + l)] = out.get((i + k, j + l), F(0)) + u * v
    return {k: v for k, v in out.items() if v}


def falling(var, c):
    """(var)_c as a bivariate polynomial; var 0 = a, 1 = b."""
    out = {(0, 0): F(1)}
    for t in range(c):
        lin = {((1, 0) if var == 0 else (0, 1)): F(1)}
        if t:
            lin[(0, 0)] = F(-t)
        out = pmul(out, lin)
    return out


def shift_and_psi(op):
    shifts = {(a - c, b - d) for (a, b, c, d) in op}
    if len(shifts) != 1:
        return None
    psi = {}
    for (a, b, c, d), v in op.items():
        psi = padd(psi, pmul(falling(0, c), falling(1, d)), v)
    return shifts.pop(), psi


def read_poly2(rows):
    out = {}
    for r in rows:
        if len(r) != 3 or type(r[0]) is not int or type(r[1]) is not int or min(r[0], r[1]) < 0:
            raise ValueError('bad polynomial row')
        if type(r[2]) not in (int, str):
            raise ValueError('coefficients must be exact')
        out[(r[0], r[1])] = out.get((r[0], r[1]), F(0)) + F(r[2])
    return {k: v for k, v in out.items() if v}


def slice_poly(psi, var, value):
    """Restrict psi to var = value; return univariate coefficient dict in the other variable."""
    out = {}
    for (i, j), v in psi.items():
        e, other = (i, j) if var == 0 else (j, i)
        out[other] = out.get(other, F(0)) + v * F(value) ** e
    return {k: v for k, v in out.items() if v}


def ueval(u, x):
    return sum((c * F(x) ** e for e, c in u.items()), F(0))


def nat_roots(u):
    """All roots in N of a nonzero univariate rational polynomial (exact)."""
    if not u:
        raise ValueError('zero polynomial has no finite root set')
    low = min(u)
    roots = {0} if low > 0 else set()
    u = {e - low: c for e, c in u.items()}
    if len(u) == 1:
        return roots
    den = 1
    for c in u.values():
        den = den * c.denominator // gcd(den, c.denominator)
    const = abs(int(u[0] * den))
    # Integer roots divide the constant term (rational root theorem); enumerate divisors.
    divs = set()
    for d in range(1, isqrt(const) + 1):
        if const % d == 0:
            divs |= {d, const // d}
    roots |= {d for d in divs if ueval(u, d) == 0}
    return roots


def zero_set(psis, U, V):
    """Exact common zero set in N^2 of psis, given U(a)V(b) in their ideal (checked by caller)."""
    lines_a, lines_b, points = set(), set(), set()
    for a0 in nat_roots(U):
        slices = [slice_poly(p, 0, a0) for p in psis]
        nz = [s for s in slices if s]
        if not nz:
            lines_a.add(a0)
        else:
            points |= {(a0, b) for b in nat_roots(nz[0]) if all(ueval(s, b) == 0 for s in nz)}
    for b0 in nat_roots(V):
        slices = [slice_poly(p, 1, b0) for p in psis]
        nz = [s for s in slices if s]
        if not nz:
            lines_b.add(b0)
        else:
            points |= {(a, b0) for a in nat_roots(nz[0]) if all(ueval(s, a) == 0 for s in nz)}
    points = {(a, b) for a, b in points if a not in lines_a and b not in lines_b}
    return sorted(lines_a), sorted(lines_b), sorted(points)


def _rank(rows, cols):
    a = [r[:] for r in rows]
    rk = 0
    for c in range(cols):
        piv = next((i for i in range(rk, len(a)) if a[i][c]), None)
        if piv is None:
            continue
        a[rk], a[piv] = a[piv], a[rk]
        for i in range(rk + 1, len(a)):
            if a[i][c]:
                f = a[i][c] / a[rk][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[rk])]
        rk += 1
    return rk


def linear_zero_set(c1, c2, c0):
    """N^2 points of c1*a + c2*b + c0 = 0 as ('vertical', a0) | ('horizontal', b0) |
    ('progression', (a0, b0), (da, db)) | ('points', [...])."""
    den = 1
    for c in (c1, c2, c0):
        den = den * c.denominator // gcd(den, c.denominator)
    c1, c2, c0 = (int(c * den) for c in (c1, c2, c0))
    if c1 == 0 and c2 == 0:
        raise ValueError('constant linear factor')
    if c2 == 0 or c1 == 0:
        c, kind = (c1, 'vertical') if c2 == 0 else (c2, 'horizontal')
        return ('points', []) if (-c0) % c or -c0 // c < 0 else (kind, -c0 // c)
    if c1 < 0:
        c1, c2, c0 = -c1, -c2, -c0
    if c2 > 0:                                  # finitely many points: c1 a + c2 b = -c0
        return ('points', [(( -c0 - c2 * b) // c1, b) for b in range(0, max(-c0, -1) // c2 + 1)
                           if (-c0 - c2 * b) % c1 == 0 and -c0 - c2 * b >= 0])
    m = -c2                                      # a = (m b - c0) / c1, increasing in b
    g = gcd(c1, m)
    da, db = m // g, c1 // g
    start = max(0, -(-c0 // m)) if c0 > 0 else 0
    for b in range(start, start + db):
        if (m * b - c0) % c1 == 0 and m * b - c0 >= 0:
            return ('progression', ((m * b - c0) // c1, b), (da, db))
    return ('points', [])


def check(obj):
    if obj.get('format') != FORMAT or obj.get('coefficient_domain') != 'Q':
        raise ValueError('not a weyl-kernel-v1 object over Q')
    receipt = obj['receipt']
    W.verify_certificate(receipt)
    P = [W.read_terms(g, 4) for g in receipt['generators']]
    sup = obj['support']
    idx = sup['monomial_generators']
    if not idx or len(set(idx)) != len(idx) or any(type(i) is not int or not 0 <= i < len(P) for i in idx):
        raise ValueError('invalid monomial generator subset')
    psis = []
    for i in idx:
        sp = shift_and_psi(P[i])
        if sp is None:
            raise ValueError(f'generator {i} is not monomial-acting')
        psis.append(sp[1])
    # Common factor g = constant * prod(linear factors); psi_i = g * phi_i.
    cf = sup['common_factor']
    g = {(0, 0): F(cf['constant'])}
    if not g[(0, 0)]:
        raise ValueError('common factor constant must be nonzero')
    lines = []
    for c1, c2, c0 in cf['linear_factors']:
        c1, c2, c0 = F(c1), F(c2), F(c0)
        g = pmul(g, {k: v for k, v in {(1, 0): c1, (0, 1): c2, (0, 0): c0}.items() if v})
        lines.append(linear_zero_set(c1, c2, c0))
    phis = [read_poly2(x) for x in sup['cofactors']]
    if len(phis) != len(psis) or any(pmul(g, f) != p for f, p in zip(phis, psis)):
        raise ValueError('psi_i = g * phi_i fails')
    lam = sup['multipliers']
    if len(lam) != len(idx):
        raise ValueError('one multiplier per monomial generator required')
    total = {}
    for l, phi in zip(lam, phis):
        total = padd(total, pmul(read_poly2(l), phi))
    U = {e: F(c) for e, c in sup['U']}
    V = {e: F(c) for e, c in sup['V']}
    if not U or not V or any(not c for c in U.values()) or any(not c for c in V.values()):
        raise ValueError('U and V must be nonzero')
    if total != pmul({(e, 0): c for e, c in U.items()}, {(0, e): c for e, c in V.items()}):
        raise ValueError('elimination identity sum lambda_i phi_i = U(a) V(b) fails')
    # Z = Z(g) u (common zeros of the phi_i); the latter by slicing the U, V lines.
    la, lb, pts = zero_set(phis, U, V)
    la, lb, prog, pts = set(la), set(lb), set(), set(pts)
    for kind, *data in lines:
        if kind == 'vertical':
            la.add(data[0])
        elif kind == 'horizontal':
            lb.add(data[0])
        elif kind == 'progression':
            prog.add((tuple(data[0]), tuple(data[1])))
        else:
            pts |= set(data[0])

    def on_family(a, b):
        return a in la or b in lb or any(
            (a - a0) * db == (b - b0) * da and a >= a0 and (a - a0) % da == 0 for (a0, b0), (da, db) in prog)
    pts = sorted(x for x in pts if not on_family(*x))
    la, lb, prog = sorted(la), sorted(lb), sorted(prog)
    claim = obj['claim']
    declared = [claim['vertical_lines'], claim['horizontal_lines'],
                [[list(b), list(s)] for b, s in (map(tuple, x) for x in claim['progressions'])],
                [list(x) for x in claim['points']]]
    if declared != [la, lb, [[list(b), list(s)] for b, s in prog], [list(x) for x in pts]]:
        raise ValueError('declared zero set differs from the recomputed one')
    if claim['kind'] == 'monomial_span':
        if sorted(idx) != list(range(len(P))):
            raise ValueError('monomial_span needs every generator to be monomial-acting')
        desc = ([f'q^{a}*Q[p]' for a in la] + [f'p^{b}*Q[q]' for b in lb] +
                [f'q^{a0}*p^{b0}*Q[q^{da}*p^{db}]' for (a0, b0), (da, db) in prog] +
                [f'q^{a}*p^{b}' for a, b in pts])
        return {'status': 'passed', 'kind': 'monomial_span', 'kernel': desc,
                'dimension': 'infinite' if la or lb or prog else len(pts),
                'scope': 'all polynomial degrees; full dynamic core by the replayed operator receipt'}
    if claim['kind'] != 'finite_support' or la or lb or prog:
        raise ValueError('finite_support needs a finite zero set')
    # Kernel inside span(points): exact rank of the stacked action of every generator.
    images = []
    for a, b in pts:
        img = {}
        for gi, op in enumerate(P):
            for e, c in W.act(op, {(a, b): F(1)}).items():
                img[(gi, e)] = c
        images.append(img)
    keys = sorted({k for img in images for k in img})
    M = [[img.get(k, F(0)) for img in images] for k in keys]
    nullity = len(pts) - (_rank(M, len(pts)) if M else 0)
    basis = [W.read_terms(g, 2) for g in claim['basis']]
    if len(basis) != nullity:
        raise ValueError(f'declared kernel basis has {len(basis)} elements; the kernel has dimension {nullity}')
    allowed = set(pts)
    for g in basis:
        if not set(g) <= allowed or any(W.act(op, g) for op in P):
            raise ValueError('declared basis element is not in the kernel')
    if _rank([[g.get(m, F(0)) for m in pts] for g in basis], len(pts)) != len(basis):
        raise ValueError('declared kernel basis is dependent')
    return {'status': 'passed', 'kind': 'finite_support', 'dimension': nullity,
            'kernel': claim['basis_display'],
            'scope': 'all polynomial degrees; full dynamic core by the replayed operator receipt'}


if __name__ == '__main__':
    try:
        print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())), indent=2))
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)
