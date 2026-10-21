#!/usr/bin/env python3
"""Producer of all-degree polynomial-kernel claims (weyl-kernel-v1) from Weyl receipts.

Given a replayable weyl-invariant-kernel-v1 receipt, look for monomial-acting
generators, find an elimination identity sum lambda_i psi_i = U(a) V(b), recompute
the exact common zero set and emit either a 'monomial_span' or a 'finite_support'
claim. Every claim is replayed by check_weyl_kernel.py before it is returned. When
no support certificate is found the status is 'unclassified' and nothing about the
polynomial solutions is asserted.

Usage: weyl_kernel.py RECEIPT.json [--output KERNEL.json] [--max-degree N]
"""
from __future__ import annotations
import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import weyl_receipts as W            # noqa: E402
import check_weyl_kernel as K        # noqa: E402
import qlinalg as L                  # noqa: E402
from weyl_groebner import show_poly  # noqa: E402


# ---- univariate helpers (dict exponent -> Fraction) ---------------------------

def udeg(u):
    return max(u) if u else -1


def udivmod(x, y):
    x, q = dict(x), {}
    dy, ly = udeg(y), y[udeg(y)]
    while x and udeg(x) >= dy:
        e, c = udeg(x) - dy, x[udeg(x)] / ly
        q[e] = c
        for k, v in y.items():
            x[k + e] = x.get(k + e, F(0)) - c * v
            if not x[k + e]:
                del x[k + e]
    return q, x


def umul(x, y):
    out = {}
    for i, u in x.items():
        for j, v in y.items():
            out[i + j] = out.get(i + j, F(0)) + u * v
    return {k: v for k, v in out.items() if v}


def ugcd(x, y):
    while y:
        x, y = y, udivmod(x, y)[1]
    if not x:
        return {}
    lc = x[udeg(x)]
    return {k: v / lc for k, v in x.items()}


def as_rows(psi, var):
    """psi = sum_j c_j(var) * other^j ; return {j: univariate c_j}."""
    out = {}
    for (i, j), v in psi.items():
        e, o = (i, j) if var == 0 else (j, i)
        out.setdefault(o, {})[e] = v
    return out


def content(psi, var):
    g = {}
    for c in as_rows(psi, var).values():
        g = ugcd(g, c) if g else ugcd(c, {})
    return g


def divide_by(psi, u, var):
    out = {}
    for o, c in as_rows(psi, var).items():
        q, r = udivmod(c, u)
        if r:
            raise AssertionError('content does not divide')
        for e, v in q.items():
            out[(e, o) if var == 0 else (o, e)] = v
    return out


def rank_one_split(psi):
    rows = as_rows(psi, 1)               # coefficient of a^i as polynomial in b
    if not rows:
        return None
    i0 = next(iter(rows))
    v = rows[i0]
    j0 = next(iter(v))
    u = {i: r.get(j0, F(0)) / v[j0] for i, r in rows.items()}
    if any(r != {j: u[i] * c for j, c in v.items()} for i, r in rows.items()):
        return None
    return {k: c for k, c in u.items() if c}, v


def eliminate(psis, var, max_degree):
    """lambda with sum lambda_i psis_i a nonzero polynomial in the *other* variable only."""
    n = len(psis)
    for d in range(max_degree + 1):
        monos = [(x, y) for t in range(d + 1) for x in range(t + 1) for y in [t - x]]
        cols, keys = [], {}
        for i, psi in enumerate(psis):
            for m in monos:
                img = K.pmul({m: F(1)}, psi)
                cols.append(img)
                for k in img:
                    keys.setdefault(k, len(keys))
        bad = [k for k in keys if (k[0] if var == 0 else k[1]) > 0]
        M = [[c.get(k, F(0)) for c in cols] for k in bad]
        for v in (L.null_basis(M, len(cols)) if M else L.eye(len(cols))):
            total = {}
            for coef, c in zip(v, cols):
                if coef:
                    total = K.padd(total, c, coef)
            if total:
                lam = [{monos[j]: v[i * len(monos) + j] for j in range(len(monos)) if v[i * len(monos) + j]}
                       for i in range(n)]
                return lam, total
    return None


def poly2_rows(p):
    return [[i, j, str(c)] for (i, j), c in sorted(p.items())]


# ---- bivariate gcd and linear factors (producer side only) ---------------------

def b_rows(p):
    """p as {b-exponent: univariate in a}."""
    return as_rows(p, 0)


def from_b_rows(r):
    return {(i, j): c for j, u in r.items() for i, c in u.items() if c}


def b_deg(r):
    return max(r) if r else -1


def prem(f, g):
    """Pseudo-remainder of f by g in Q[a][b]."""
    f = {k: dict(v) for k, v in f.items()}
    dg, lg = b_deg(g), g[b_deg(g)]
    while f and b_deg(f) >= dg:
        df, lf = b_deg(f), f[b_deg(f)]
        f = {k: umul(v, lg) for k, v in f.items()}
        for k, v in g.items():
            t = umul(v, lf)
            e = k + df - dg
            f[e] = {i: c for i, c in udiff(f.get(e, {}), t).items()}
        f = {k: v for k, v in f.items() if v}
    return f


def udiff(x, y):
    out = dict(x)
    for k, v in y.items():
        out[k] = out.get(k, F(0)) - v
    return {k: v for k, v in out.items() if v}


def prim(r):
    c = {}
    for u in r.values():
        c = ugcd(c, u) if c else ugcd(u, {})
    return {k: udivmod(u, c)[0] for k, u in r.items()}, c


def bgcd(f, g):
    f, cf = prim(b_rows(f))
    g, cg = prim(b_rows(g))
    c = ugcd(cf, cg)
    while g and b_deg(g) > 0:
        r = prem(f, g)
        f, g = g, (prim(r)[0] if r else {})
    if g:                                   # nonzero constant in b: primitive gcd is 1
        f = {0: {0: F(1)}}
    out = K.pmul(from_b_rows(f), {(i, 0): v for i, v in c.items()})
    lead_c = out[max(out)]
    return {k: v / lead_c for k, v in out.items()}


def bdiv(p, g):
    """Exact division p / g in Q[a,b] (lex in b then a); None if not exact."""
    p, q = dict(p), {}
    gl = max(g, key=lambda t: (t[1], t[0]))
    while p:
        pl = max(p, key=lambda t: (t[1], t[0]))
        if pl[0] < gl[0] or pl[1] < gl[1]:
            return None
        m, c = (pl[0] - gl[0], pl[1] - gl[1]), p[pl] / g[gl]
        q[m] = c
        p = K.padd(p, K.pmul({m: c}, g), F(-1))
    return q


def linear_factors(g):
    """Split g = constant * prod(linear forms) * rest; return (constant, [(c1,c2,c0)], rest)."""
    found = []
    changed = True
    while changed and any(sum(k) > 0 for k in g):
        changed = False
        d = max(sum(k) for k in g)
        top = {k: v for k, v in g.items() if sum(k) == d}
        slopes = []
        # top(a, b) = b^m * f(a/b): candidate directions c1 a + c2 b with f(-c2/c1) = 0.
        if all(k[0] == 0 for k in top):
            slopes.append((F(0), F(1)))
        if all(k[1] == 0 for k in top):
            slopes.append((F(1), F(0)))
        fa = {k[0]: v for k, v in top.items()}
        for r in rational_roots(fa):
            slopes.append((F(1), -r))         # a - r b divides the top form
        if 0 not in fa:                        # every top term contains a
            slopes.append((F(1), F(0)))
        if 0 not in {k[1] for k in top}:       # every top term contains b
            slopes.append((F(0), F(1)))
        for c1, c2 in slopes:
            # find c0 with c1 a + c2 b + c0 | g: substitute along the line, all coefficients vanish
            for c0 in candidate_offsets(g, c1, c2):
                lf = {k: v for k, v in {(1, 0): c1, (0, 1): c2, (0, 0): c0}.items() if v}
                qt = bdiv(g, lf)
                if qt is not None:
                    found.append((c1, c2, c0))
                    g, changed = qt, True
                    break
            if changed:
                break
    const = g[(0, 0)] if set(g) == {(0, 0)} else None
    return const, found, g


def rational_roots(u):
    u = {k: v for k, v in u.items() if v}
    if not u or len(u) == 1 and 0 in u:
        return []
    low = min(u)
    roots = [F(0)] if low > 0 else []
    u = {k - low: v for k, v in u.items()}
    if len(u) == 1:
        return roots
    from math import gcd, isqrt
    den = 1
    for c in u.values():
        den = den * c.denominator // gcd(den, c.denominator)
    a0, an = abs(int(u[0] * den)), abs(int(u[max(u)] * den))
    divs = lambda n: {d for i in range(1, isqrt(n) + 1) if n % i == 0 for d in (i, n // i)}
    for p in divs(a0):
        for q in divs(an):
            for r in (F(p, q), F(-p, q)):
                if r not in roots and sum(c * r ** e for e, c in u.items()) == 0:
                    roots.append(r)
    return roots


def candidate_offsets(g, c1, c2):
    """Rational c0 such that g vanishes on c1 a + c2 b + c0 = 0 (exact)."""
    # Parametrize the line: if c1 != 0, a = -(c2 t + c0)/c1, b = t; collect coefficients in t
    # as polynomials in c0 and take common rational roots of the first nonzero one.
    out = []
    for c0 in rational_roots_line(g, c1, c2):
        out.append(c0)
    return out


def rational_roots_line(g, c1, c2):
    # Evaluate g on the line at several sample t-values: each gives a univariate polynomial in c0.
    polys = []
    for t in range(0, 4):
        poly = {}
        for (i, j), v in g.items():
            if c1:
                # a = (-c2 t - c0)/c1 : expand (x + y c0)^i with x = -c2 t / c1, y = -1/c1
                x, y, bb = -c2 * t / c1, F(-1) / c1, F(t) ** j
                base = {0: F(1)}
                for _ in range(i):
                    base = umul(base, {0: x, 1: y})
                for e, c in base.items():
                    poly[e] = poly.get(e, F(0)) + v * c * bb
            else:
                # c2 b + c0 = 0 : b = -c0/c2, a = t
                xa = F(t) ** i
                base = {0: F(1)}
                for _ in range(j):
                    base = umul(base, {1: F(-1) / c2})
                for e, c in base.items():
                    poly[e] = poly.get(e, F(0)) + v * c * xa
        polys.append({k: c for k, c in poly.items() if c})
    nz = [p for p in polys if p]
    if not nz:
        return []
    return [r for r in rational_roots(nz[0]) if all(sum(c * r ** e for e, c in p.items()) == 0 for p in nz)]


def find_support(psis, max_degree):
    """Common linear factor g, cofactors phi_i = psi_i / g and (lambda, U, V) with
    sum lambda_i phi_i = U(a) V(b); prefers the description with the fewest families."""
    g = psis[0]
    for p in psis[1:]:
        g = bgcd(g, p)
    const, lins, rest = linear_factors(g)
    if const is None:
        return None                         # a nonlinear common curve: not handled
    phis = [bdiv(p, g) for p in psis]
    candidates = []
    for i, phi in enumerate(phis):
        split = rank_one_split(phi)
        if split:
            lam = [{} for _ in phis]
            lam[i] = {(0, 0): F(1)}
            candidates.append((lam, split[0], split[1]))
    ga = gb = {}
    for phi in phis:
        ca, cb = content(phi, 0), content(phi, 1)
        ga = ugcd(ga, ca) if ga else ca
        gb = ugcd(gb, cb) if gb else cb
    reduced = [divide_by(divide_by(p, ga, 0), gb, 1) for p in phis]
    for var in (0, 1):
        found = eliminate(reduced, var, max_degree)
        if found:
            lam, r = found
            r1 = {(j if var == 0 else i): c for (i, j), c in r.items()}
            U, V = (ga, umul(gb, r1)) if var == 0 else (umul(ga, r1), gb)
            # lambda_i phi_i = lambda_i ga gb reduced_i, so the same lambda gives U V.
            candidates.append((lam, U, V))
    best = None
    for lam, U, V in candidates:
        if not U or not V:
            continue
        la, lb, pts = K.zero_set(phis, U, V)
        score = (len(la) + len(lb), len(pts))
        if best is None or score < best[0]:
            best = (score, lam, U, V)
    if best is None:
        return None
    return const, lins, phis, best[1], best[2], best[3]


def _support_object(receipt, idx, found):
    const, lins, phis, lam, U, V = found
    return {'format': K.FORMAT, 'coefficient_domain': 'Q', 'receipt': receipt,
            'support': {'monomial_generators': idx,
                        'common_factor': {'constant': str(const),
                                          'linear_factors': [[str(c) for c in t] for t in lins]},
                        'cofactors': [poly2_rows(p) for p in phis],
                        'multipliers': [poly2_rows(l) for l in lam],
                        'U': [[e, str(c)] for e, c in sorted(U.items())],
                        'V': [[e, str(c)] for e, c in sorted(V.items())]}}


def classify(receipt, max_degree=6):
    W.verify_certificate(receipt)
    P = [W.read_terms(g, 4) for g in receipt['generators']]
    mono = [(i, K.shift_and_psi(op)) for i, op in enumerate(P)]
    mono = [(i, sp[1]) for i, sp in mono if sp]
    if not mono:
        return {'status': 'unclassified', 'reason': 'no monomial-acting generator'}, None
    idx, psis = [i for i, _ in mono], [p for _, p in mono]
    found = find_support(psis, max_degree)
    if not found:
        return {'status': 'unclassified', 'reason': 'no support certificate within degree budget'}, None
    obj = _support_object(receipt, idx, found)
    # Let the checker's own recomputation of the zero set fill in the claim fields.
    la, lb, pts = K.zero_set(found[2], found[4], found[5])
    fam = [K.linear_zero_set(*t) for t in found[1]]
    la = set(la) | {d[0] for k, *d in fam if k == 'vertical'}
    lb = set(lb) | {d[0] for k, *d in fam if k == 'horizontal'}
    prog = {(tuple(d[0]), tuple(d[1])) for k, *d in fam if k == 'progression'}
    pts = set(pts) | {x for k, *d in fam if k == 'points' for x in d[0]}
    on = lambda a, b: a in la or b in lb or any((a - a0) * db == (b - b0) * da and a >= a0 and (a - a0) % da == 0
                                                for (a0, b0), (da, db) in prog)
    pts = sorted(x for x in pts if not on(*x))
    claim = {'vertical_lines': sorted(la), 'horizontal_lines': sorted(lb),
             'progressions': [[list(b), list(st)] for b, st in sorted(prog)], 'points': [list(p) for p in pts]}
    if len(idx) == len(P):
        claim['kind'] = 'monomial_span'
    elif not la and not lb and not prog:
        images = []
        for a, b in pts:
            img = {}
            for gi, op in enumerate(P):
                for e, c in W.act(op, {(a, b): F(1)}).items():
                    img[(gi, e)] = c
            images.append(img)
        keys = sorted({k for img in images for k in img})
        M = [[img.get(k, F(0)) for img in images] for k in keys]
        null = L.null_basis(M, len(pts)) if M else L.eye(len(pts))
        basis = [W.tidy({tuple(pts[i]): v[i] for i in range(len(pts))}) for v in null]
        claim.update(kind='finite_support', basis=[W.dump_terms(g) for g in basis],
                     basis_display=[show_poly(g) for g in basis])
    else:
        return {'status': 'unclassified', 'reason': 'support has infinite families but some generator is not '
                'monomial-acting', 'support_families': claim}, None
    obj['claim'] = claim
    result = K.check(obj)
    return {**result, 'status': 'classified'}, obj


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('receipt', type=Path)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--max-degree', type=int, default=6)
    a = ap.parse_args()
    meta, obj = classify(json.loads(a.receipt.read_text()), a.max_degree)
    if obj and a.output:
        a.output.write_text(json.dumps(obj, indent=1) + '\n')
        meta['written'] = str(a.output)
    print(json.dumps(meta, indent=2))
    if meta['status'] != 'classified':
        sys.exit(3)


if __name__ == '__main__':
    main()
