#!/usr/bin/env python3
"""Dynamic cores of polynomial Hamiltonians whose top part has at most two roots
(two-root-perturbation-v1). See DYNAMIC_CORE_RESULTS.md section 6.

Given a rational H of degree d >= 3 whose top homogeneous part H_d has at most two distinct
roots over Qbar, the checker recomputes the top type and applies the proved criteria:

  unequal  H_d = c l^a m^b, a > b >= 2   Theorem U: D_inf = span{1, H, G} with G = (lm)(x - x0)
           if the translation x -> x + x0 that kills H_(d-1) puts H into
           l^(a-b) K[lm] + K lm + K; otherwise span{1, H}.          (complete)
  pure     H_d = c l^d                      W = (+)_{j<=2} m^j K[l] if d_v H_(>=3) = 0 and d_v^2 H_2 = 0;
                                            V = K[l] + m K[l] if d_v^2 H = 0;
                                            span{1, H} if H = f(l) + m g(l) + gamma m^2, gamma != 0,
                                            deg g < d/2 (Theorem Q') or the transverse top is finite
                                            (Theorem T); otherwise conjectural.
  near     H_d = c l^(d-1) m                V if d_v^2 H = 0; span{1, H} otherwise (Theorem NE,
                                            check_near_edges.py).                   (complete)
  balanced H_d = c Q^mu, Q a quadratic form  K[G] with G = Q(x - x0) if the translation killing
                                            H_(d-1) puts H into K[Q]; otherwise span{1, H} (Theorem B,
                                            check_balanced.py).                     (complete)
Here v is the direction annihilated by l (d_v l = 0).

Usage: check_two_root.py CERT.json
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_root_rigidity as RR  # noqa: E402

FORMAT = 'two-root-perturbation-v1'

# ---- bivariate polynomials {(i, j): F} for q^i p^j -----------------------------------------


def tidy(p):
    return {k: F(v) for k, v in p.items() if v}


def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return tidy(out)


def mul(a, b):
    out = {}
    for (i, j), u in a.items():
        for (k, l), v in b.items():
            out[(i + k, j + l)] = out.get((i + k, j + l), F(0)) + u * v
    return tidy(out)


def sc(a, c):
    return tidy({k: v * c for k, v in a.items()})


def power(a, e):
    out = {(0, 0): F(1)}
    for _ in range(e):
        out = mul(out, a)
    return out


def comp(H, X, Y):
    """H(X, Y) for polynomials X, Y."""
    out = {}
    for (i, j), c in H.items():
        out = add(out, sc(mul(power(X, i), power(Y, j)), c))
    return out


def part(H, e):
    return {k: v for k, v in H.items() if sum(k) == e}


def dq(H):
    return tidy({(i - 1, j): i * c for (i, j), c in H.items() if i})


def dp(H):
    return tidy({(i, j - 1): j * c for (i, j), c in H.items() if j})


def dv(H, v):
    return add(sc(dq(H), v[0]), sc(dp(H), v[1]))


def degree(H):
    return max(i + j for i, j in H) if H else -1


def proportional(A, B):
    """Return c with A = c B (B != 0), or None."""
    if not B:
        return F(0) if not A else None
    k = next(iter(B))
    c = A.get(k, F(0)) / B[k]
    return c if add(A, sc(B, -c)) == {} else None


def in_span(A, basis):
    """Exact membership test of A in span(basis) (small dense linear algebra)."""
    keys = sorted(set(A) | {k for b in basis for k in b})
    cols = [[b.get(k, F(0)) for k in keys] for b in basis]
    rhs = [A.get(k, F(0)) for k in keys]
    # Gaussian elimination on the augmented system
    M = [[cols[c][r] for c in range(len(basis))] + [rhs[r]] for r in range(len(keys))]
    piv, row = [], 0
    for c in range(len(basis)):
        pr = next((r for r in range(row, len(M)) if M[r][c] != 0), None)
        if pr is None:
            continue
        M[row], M[pr] = M[pr], M[row]
        for r in range(len(M)):
            if r != row and M[r][c] != 0:
                f = M[r][c] / M[row][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[row])]
        row += 1
    return all(M[r][-1] == 0 for r in range(row, len(M)))


def lin(a, b):
    """The linear form a q + b p."""
    return tidy({(1, 0): F(a), (0, 1): F(b)})


def top_forms(Hd, d):
    """Root forms of H_d with multiplicities: list of (form or quadratic, multiplicity)."""
    f = RR.dehom(Hd, d)
    mu_inf = d - (len(f) - 1)
    c, S = RR.yun(f)
    out = []
    for i, s in enumerate(S, start=1):
        s = RR.norm(s)
        if len(s) == 2:                                      # x - r  ->  q - r p
            out.append((lin(1, s[0] / s[1]), i))          # root r = -s0/s1, form q - r p
        elif len(s) == 3:                                    # irreducible or split quadratic in x
            # homogenise: s0 p^2 + s1 q p + s2 q^2
            out.append(({(0, 2): s[0], (1, 1): s[1], (2, 0): s[2]}, i, 'quadratic'))
        elif len(s) > 3:
            raise ValueError('top part has more than two roots')
    if mu_inf:
        out.append((lin(0, 1), mu_inf))
    return out


def translation_killing(H, d):
    """(x0, y0) with H_(d-1) + x0 d_q H_d + y0 d_p H_d = 0, or None."""
    Hd, Hd1 = part(H, d), part(H, d - 1)
    A, B = dq(Hd), dp(Hd)
    keys = sorted(set(A) | set(B) | set(Hd1))
    rows = [(A.get(k, F(0)), B.get(k, F(0)), -Hd1.get(k, F(0))) for k in keys]
    # solve the 2-unknown system exactly
    sol = None
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a1, b1, c1 = rows[i]
            a2, b2, c2 = rows[j]
            det = a1 * b2 - a2 * b1
            if det:
                sol = ((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det)
                break
        if sol:
            break
    if sol is None:
        # rank <= 1: only possible if H_d is a power of a linear form; not used for U / balanced
        return None
    x0, y0 = sol
    if any(a * x0 + b * y0 != c for a, b, c in rows):
        return None
    return x0, y0


def shift(H, x0, y0):
    return comp(H, {(1, 0): F(1), (0, 0): F(x0)}, {(0, 1): F(1), (0, 0): F(y0)})


def classify(H):
    H = tidy(H)
    d = degree(H)
    if d < 3:
        raise ValueError('degree must be at least 3')
    Hd = part(H, d)
    forms = top_forms(Hd, d)
    roots = sum(2 if len(f) == 3 else 1 for f in forms)
    if roots > 2:
        raise ValueError('top part has at least three roots: use check_root_rigidity.py')
    out = {'degree': d}
    # balanced: one quadratic of multiplicity mu, or two linear forms of equal multiplicity
    quads = [f for f in forms if len(f) == 3]
    lins = [f for f in forms if len(f) == 2]
    if quads or (len(lins) == 2 and lins[0][1] == lins[1][1]):
        Q = quads[0][0] if quads else mul(lins[0][0], lins[1][0])
        mu = d // 2
        out['top'] = 'balanced'
        t = translation_killing(H, d)
        if t is not None:
            Hs = shift(H, *t)
            ok = True
            for e in range(d + 1):
                comp_e = part(Hs, e)
                if e % 2:
                    ok &= not comp_e
                else:
                    ok &= proportional(comp_e, power(Q, e // 2)) is not None
            if ok:
                G = shift(Q, -t[0], -t[1])
                out.update(route='P+ balanced', proved=True, core='K[G]', G=ser(G),
                           active_part='0 (all stationary)')
                return out
        out.update(route='B', proved=True, core='span{1, H}', active_part='0')
        return out
    if len(lins) == 2 and min(f[1] for f in lins) >= 2:     # unequal
        (l, a), (m, b) = sorted(lins, key=lambda f: -f[1])
        out['top'] = f'unequal ({a},{b})'
        t = translation_killing(H, d)
        if t is not None:
            Hs = shift(H, *t)
            lm = mul(l, m)
            ok = True
            for e in range(d + 1):
                comp_e = part(Hs, e)
                basis = []
                if e >= a - b and (e - a + b) % 2 == 0:
                    basis.append(mul(power(l, a - b), power(lm, (e - a + b) // 2)))
                if e == 2:
                    basis.append(lm)
                if e == 0:
                    basis.append({(0, 0): F(1)})
                ok &= in_span(comp_e, basis) if basis else not comp_e
            if ok:
                G = shift(mul(l, m), -t[0], -t[1])
                out.update(route='U', proved=True, core='span{1, H, G}', G=ser(G),
                           active_part='K G ({H, G} = (a-b) H mod span{1, G})')
                return out
        out.update(route='U', proved=True, core='span{1, H}', active_part='0')
        return out
    l, mult = max(lins, key=lambda f: f[1])
    v = (l.get((0, 1), F(0)), -l.get((1, 0), F(0)))          # d_v l = 0
    d2 = dv(dv(H, v), v)
    if mult == d - 1:                                        # near: H_d = c l^(d-1) m
        out['top'] = 'near'
        if not d2:
            out.update(route='P+ near', proved=True, core='K[l] + m K[l]', active_part='infinite')
        else:
            # Theorem NE (check_near_edges.py): every near top that is not affine in m
            out.update(route='NE', proved=True, core='span{1, H}', active_part='0')
        return out
    out['top'] = 'pure'                                       # H_d = c l^d
    high = {k: c for k, c in H.items() if sum(k) >= 3}
    if not dv(high, v) and not dv(dv(part(H, 2), v), v):
        out.update(route='P+ pure W', proved=True, core='(+)_{j<=2} m^j K[l]', active_part='infinite')
    elif not d2:
        out.update(route='P+ pure V', proved=True, core='K[l] + m K[l]', active_part='infinite')
    elif degree(d2) == 0 and qprime(H, l, d):
        out.update(route="Q'", proved=True, core='span{1, H}', active_part='0')
    elif transverse_finite(H, l)[0] and transverse_pure_ok(H, l):
        out.update(route='T', proved=True, core='span{1, H}', active_part='0')
    else:
        out.update(route='pure, conjectural', proved=False, core='span{1, H} (conjectured)',
                   active_part='0 (conjectured)')
    return out


def coords(H, l):
    """H in coordinates X = l, Y = m (m = p if l involves q, else q): dict (i, j) -> X^i Y^j."""
    a, b = l.get((1, 0), F(0)), l.get((0, 1), F(0))
    if a != 0:
        q_, p_ = {(1, 0): 1 / a, (0, 1): -b / a}, {(0, 1): F(1)}
    else:
        q_, p_ = {(0, 1): F(1)}, {(1, 0): 1 / b}
    return comp(H, q_, p_)


def transverse_finite(H, l):
    """Theorem T: the part of maximal m-degree s >= 2 is F = m^s phi(l) with deg phi >= 2 and F not of
    the form c (m (l + gamma))^s. Returns (applies, description)."""
    Ht = coords(H, l)
    s_ = max(j for i, j in Ht)
    if s_ < 2:
        return False, 'affine'
    phi = {i: c for (i, j), c in Ht.items() if j == s_}
    e = max(phi)
    if e < 2:
        return False, f'transverse top m^{s_} times a polynomial of degree {e}'
    if e == s_:
        gam = phi.get(e - 1, F(0)) / (e * phi[e])
        if all(phi.get(i, F(0)) == phi[e] * comb(e, i) * gam ** (e - i) for i in range(e + 1)):
            return False, 'transverse top in K[G]'
    return True, f'transverse top m^{s_} phi(l), deg phi = {e}'


def transverse_pure_ok(H, l):
    """Pure tops need in addition that phi is not a perfect power c (l + gamma)^e: otherwise D_inf(F)
    contains the m-homogeneous quadratic m (l + gamma) and the reduction to K[l] fails."""
    Ht = coords(H, l)
    s_ = max(j for i, j in Ht)
    phi = {i: c for (i, j), c in Ht.items() if j == s_}
    e = max(phi)
    gam = phi.get(e - 1, F(0)) / (e * phi[e])
    return not all(phi.get(i, F(0)) == phi[e] * comb(e, i) * gam ** (e - i) for i in range(e + 1))


def hull_vertices(Ht):
    """Monomials (m-exp, l-exp) of Ht (keys (i, j) for X^i Y^j, X = l, Y = m) that are the unique
    maximiser of m-exp + t * l-exp for some t in the open interval (0, 1): the Newton-polygon
    vertices strictly between the total-degree direction (t = 1) and the m-degree direction (t = 0).
    Exact: for each candidate the admissible t form an interval cut out by linear inequalities."""
    pts = sorted({(j, i) for (i, j) in Ht})
    out = set()
    for v in pts:
        lo, hi = F(0), F(1)                       # open interval (lo, hi)
        ok = True
        for p in pts:
            if p == v:
                continue
            a, b = F(v[0] - p[0]), F(v[1] - p[1])  # need a + t b > 0
            if b > 0:
                lo = max(lo, -a / b)
            elif b < 0:
                hi = min(hi, -a / b)
            elif a <= 0:
                ok = False
                break
        if ok and lo < hi:
            out.add(v)
    return out


def unequal_vertex(H, l):
    Ht = coords(H, l)
    for mm, ll in hull_vertices(Ht):
        if mm >= 2 and ll >= 2 and mm != ll:
            return True, (mm, ll)
    return False, None


def qprime(H, l, d):
    """Theorem Q' family: in coordinates X = l, Y = m (m = p or q complementary),
    H = f(X) + Y g(X) + gamma Y^2 with deg g < d/2."""
    a, b = l.get((1, 0), F(0)), l.get((0, 1), F(0))
    # choose m and invert (q, p) = linear in (X, Y)
    if a != 0:          # X = a q + b p, Y = p  ->  q = (X - b Y)/a, p = Y
        q_ = {(1, 0): 1 / a, (0, 1): -b / a}
        p_ = {(0, 1): F(1)}
    else:               # X = b p, Y = q
        q_ = {(0, 1): F(1)}
        p_ = {(1, 0): 1 / b}
    Ht = comp(H, q_, p_)                         # now (i, j) means X^i Y^j
    for (i, j), c in Ht.items():
        if j >= 3 or (j == 2 and i > 0) or (j == 1 and 2 * i >= d):
            return False
    return True


def ser(P):
    return {f'{i},{j}': str(c) for (i, j), c in sorted(P.items())}


def check(cert):
    if cert.get('format') != FORMAT:
        raise ValueError('not a two-root-perturbation-v1 certificate')
    H = {tuple(map(int, k.split(','))): F(v) for k, v in cert['hamiltonian'].items()}
    res = classify(H)
    if cert.get('claim') != {k: res[k] for k in ('route', 'core', 'proved')}:
        raise ValueError('declared classification differs from the recomputed one')
    return {'status': 'passed', **res}


def certify(H):
    res = classify(H)
    cert = {'format': FORMAT, 'hamiltonian': ser(tidy(H)), 'claim': {k: res[k] for k in ('route', 'core', 'proved')}}
    cert['result'] = check(cert)
    return cert


def main():
    try:
        print(json.dumps(check(json.loads(open(sys.argv[1]).read())), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
