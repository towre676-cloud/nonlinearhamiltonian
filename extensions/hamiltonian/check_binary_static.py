#!/usr/bin/env python3
"""Independent checker for static finiteness at a simple root (binary-static-v1).

Claim. Let d be 5 or 6 and let n >= N0 (declared, re-derived here). Let H be a binary form
of degree d over an algebraically closed field of characteristic zero with a simple root P,
and let E_n(H) = {G in V_n : T_3(H, G) = T_5(H, G) = 0}. If E_n(H) != 0, then H has a root
of multiplicity >= d - 1 or a root of multiplicity exactly d - 2 together with two simple
roots, i.e. H has type (d-1, 1) or (d-2, 1, 1).

Proof structure checked here.
 1. Local normal form. Move P to (1:0) and use the stabiliser q -> a q + b p, p -> c p:
    H = q^(d-1) p + sum_{j=3..d} h_j q^(d-j) p^j (the q^(d-2) p^2 term is removed by the
    shear, the leading coefficient by scaling). The residual torus a^(d-1) c = 1 acts by
    h_j -> lam^(j-1) h_j with lam = a^(-d) arbitrary.
 2. Top lemma at P (weight (2,1), static version). The top part of H is q^(d-1) p, whose
    static space in degree n >= 3 is spanned by q^n and q^(n-1) p: the gate coefficients on
    q^(n-b) p^b are (b)_2 [d b - 2d + 6 - 3n] (T_3) and (b)_4 [(d-5)(b-4) - 5(n-b)] (T_5)
    up to nonzero constants; the checker re-derives both factorisations and shows that they
    have no common zero with 2 <= b <= n for n >= 3. Hence every nonzero G in E_n(H),
    G = sum_t g_t q^(n-t) p^t, has (g_0, g_1) != (0, 0).
 3. Top equations. The T_3 equation at output index t' determines g_(t'+2) from g_0, g_1
    with denominators that are polynomials in n; the T_5 equations at output indices
    0..R-1 give an R x 2 matrix M(n, h) with (A_t, B_t) (g_0, g_1)^T = 0. The checker
    re-derives M with its own arithmetic and compares with the declared rows up to row
    scalars s_t(n). For n >= N0 every denominator and scalar is nonzero and every index
    used exists.
 4. Rank. If E_n != 0 the matrix M(n, h) has a kernel vector (g_0, g_1) != 0. Three cases:
    g_1 = 0 (all A_t = 0), g_0 = 0 (all B_t = 0), or g_0 g_1 != 0; in the last case the
    torus of step 1 (A_t, B_t are weighted homogeneous of degrees W_t + 1, W_t) normalises
    g_0 = g_1, i.e. A_t + B_t = 0. In the first two cases h != 0 is normalised by the first
    nonzero h_j = 1. Every case is a polynomial system over Q[n] in the h_j; for each the
    certificate gives an elimination tree whose steps are explicit polynomial identities
    (derived polynomial = sum of multipliers times known polynomials), factorisations
    p = c(n) prod q_i^(m_i) with c(n) != 0 for n >= N0 (branch on q_i = 0), and leaves that
    are either a polynomial in n alone without integer roots >= N0 (no solution) or
    identities c_j(n) J_j = sum of multiples, so that all generators J_j vanish.
 5. The common zeros of J (fixed below, weighted homogeneous) are h = 0 (type (d-1,1)) and
    the points where x^(d-1) + h_3 x^(d-3) + ... + h_d has a root of multiplicity d - 2;
    checked in Q[a]/(a^2 - alpha).

Usage: check_binary_static.py CERT.json
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction as F
from math import comb

FORMAT = 'binary-static-v1'
ROWS = {5: 4, 6: 6}
# J generators in the variables (h3, ..., hd), as {exponents of (h3..hd): coefficient}
J_EXPECTED = {
    5: [{(0, 2, 0): F(1), (3, 0, 0): F(8, 27)}, {(0, 0, 1): F(1), (2, 0, 0): F(1, 12)}],
    6: [{(0, 2, 0, 0): F(1), (3, 0, 0, 0): F(2, 5)}, {(0, 0, 1, 0): F(1), (2, 0, 0, 0): F(3, 20)},
        {(0, 0, 0, 1): F(1), (1, 1, 0, 0): F(1, 50)}],
}

# ---- polynomials in (n, h3, ..., hd): dict {exponent tuple: Fraction} ----------------------


def pz(x):
    return {k: v for k, v in x.items() if v}


def padd(*xs):
    out = {}
    for x in xs:
        for k, v in x.items():
            out[k] = out.get(k, F(0)) + v
    return pz(out)


def pmul(a, b):
    out = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(x + y for x, y in zip(k1, k2))
            out[k] = out.get(k, F(0)) + v1 * v2
    return pz(out)


def psc(a, c):
    return pz({k: v * c for k, v in a.items()})


def ppow(a, e, nv):
    out = {(0,) * nv: F(1)}
    for _ in range(e):
        out = pmul(out, a)
    return out


def const(c, nv):
    return pz({(0,) * nv: F(c)})


def var(i, nv):
    e = [0] * nv
    e[i] = 1
    return {tuple(e): F(1)}


def n_only(p):
    return all(not any(k[1:]) for k in p)


def subs_var(p, i, value):
    """Substitute variable i by a constant."""
    out = {}
    for k, v in p.items():
        kk = list(k)
        e = kk[i]
        kk[i] = 0
        out[tuple(kk)] = out.get(tuple(kk), F(0)) + v * F(value) ** e
    return pz(out)


def parse(p, nv):
    out = {}
    for e, c in p:
        if len(e) != nv:
            raise ValueError('polynomial with the wrong number of variables')
        out[tuple(e)] = out.get(tuple(e), F(0)) + F(c)
    return pz(out)


# ---- univariate polynomials in n -----------------------------------------------------------


def uni(p):
    if not n_only(p):
        raise ValueError('expected a polynomial in n alone')
    out = {}
    for k, v in p.items():
        out[k[0]] = out.get(k[0], F(0)) + v
    return {e: c for e, c in out.items() if c}


def uval(u, x):
    return sum((c * F(x) ** e for e, c in u.items()), F(0))


def iroot_ceil(x, k):
    """Smallest integer r >= 0 with r^k >= x, for a rational x >= 0."""
    if x <= 0:
        return 0
    r = max(1, int(float(x) ** (1.0 / k)) - 2) if x < 10 ** 300 else 1
    while F(r) ** k < x:
        r = r * 2 if F(r * 2) ** k < x else r + 1
    while r > 0 and F(r - 1) ** k >= x:
        r -= 1
    return r


def nonzero_from(p, N0):
    """p is a polynomial in n alone; verify p(m) != 0 for every integer m >= N0."""
    u = uni(p)
    if not u:
        raise ValueError('a polynomial asserted nonzero is identically zero')
    deg = max(u)
    lead = u[deg]
    # Fujiwara bound: every complex root satisfies |z| <= 2 max_i |a_(deg-i)/a_deg|^(1/i)
    bound = 0
    for i in range(1, deg + 1):
        c = u.get(deg - i, F(0))
        if c:
            bound = max(bound, 2 * iroot_ceil(abs(c / lead), i) + 1)
    for m in range(N0, bound + 1):
        if uval(u, m) == 0:
            raise ValueError(f'polynomial in n vanishes at n = {m} >= N0')
    return True


def max_int_root(p):
    u = uni(p)
    deg = max(u)
    lead = u[deg]
    bound = 0
    for i in range(1, deg + 1):
        c = u.get(deg - i, F(0))
        if c:
            bound = max(bound, 2 * iroot_ceil(abs(c / lead), i) + 1)
    roots = [m for m in range(-bound, bound + 1) if uval(u, m) == 0]
    return max(roots, default=None)


# ---- step 2: top lemma for q^(d-1) p -------------------------------------------------------


def falling(x, r):
    out = 1
    for t in range(r):
        out *= (x - t)
    return out


def gate_coef(k, A, B, a, b):
    """T_k(q^A p^B, q^a p^b) = coef * q^(A+a-k) p^(B+b-k)  (exact integers)."""
    return sum((-1) ** i * comb(k, i) * falling(A, k - i) * falling(B, i) * falling(a, i) * falling(b, k - i)
               for i in range(k + 1))


def top_lemma(d, N0):
    # closed forms, then a check of the closed forms on a grid (both sides are polynomials of
    # degree <= 5 in (n, b), so agreement on a 7 x 7 grid proves the identity)
    c3 = lambda n, b: (d - 1) * (d - 2) * falling(b, 2) * (d * b - 2 * d + 6 - 3 * n)
    c5 = lambda n, b: (d - 1) * (d - 2) * (d - 3) * (d - 4) * falling(b, 4) * ((d - 5) * (b - 4) - 5 * (n - b))
    for n in range(20, 27):
        for b in range(0, 7):
            if gate_coef(3, d - 1, 1, n - b, b) != c3(n, b) or gate_coef(5, d - 1, 1, n - b, b) != c5(n, b):
                raise ValueError('closed forms of the top gate coefficients are wrong')
    # common zeros with 2 <= b <= n: b in {2, 3} needs d b - 2d + 6 = 3n; b >= 4 needs both
    # linear factors to vanish. Solve exactly.
    bad = []
    for b in (2, 3):
        if (d * b - 2 * d + 6) % 3 == 0:
            bad.append((d * b - 2 * d + 6) // 3)
    # b >= 4: d b - 2d + 6 = 3n and (d - 5)(b - 4) = 5(n - b)  -> linear system in (n, b)
    # 3n - d b = 6 - 2d ; 5n - (5 + d - 5) b = -4(d - 5)  i.e. 5n - d b = -4(d - 5)
    # subtract: 2n = -4(d - 5) - 6 + 2d  ->  n = -d + 7
    bad.append(7 - d)
    if max(bad) >= N0:
        raise ValueError('the static top space of q^(d-1) p is larger than span{q^n, q^(n-1) p}')
    return {'top_static_space': 'span{q^n, q^(n-1) p} for n >= 3', 'exceptional_degrees': sorted(set(bad))}


# ---- step 3: re-derive the top equations ---------------------------------------------------


class RLin:
    """Linear form in (g_0, g_1): {param: poly in (n, h)} / den, den a polynomial in n."""
    def __init__(self, coef, den):
        self.coef, self.den = coef, den


def mono_poly(k, A, B, t, nv):
    """Gate coefficient T_k(q^A p^B, q^(n-t) p^t) as a polynomial in n (exact)."""
    out = {}
    n = var(0, nv)
    for i in range(k + 1):
        c = (-1) ** i * comb(k, i) * falling(A, k - i) * falling(B, i) * falling(t, k - i)
        if c == 0:
            continue
        ff = const(1, nv)
        for s in range(i):
            ff = pmul(ff, padd(n, const(-t - s, nv)))
        out = padd(out, psc(ff, c))
    return out


def derive_rows(d, R):
    nv = d - 1
    H = {1: const(1, nv)}
    for j in range(3, d + 1):
        H[j] = var(j - 2, nv)
    one = const(1, nv)
    g = {0: RLin({0: one}, one), 1: RLin({1: one}, one)}
    used_den = []
    tmax = R + 3          # T_5 rows at output index <= R - 1 use g_t with t <= R + 3
    for tp in range(0, tmax - 1):
        tgt = tp + 2
        terms = []
        for j, hj in H.items():
            if j == 1:
                continue
            t = tp + 3 - j
            if t >= 0:
                terms.append((pmul(hj, mono_poly(3, d - j, j, t, nv)), g[t]))
        lead = mono_poly(3, d - 1, 1, tgt, nv)
        used_den.append(lead)
        den = one
        for _, L in terms:
            den = pmul(den, L.den)
        coef = {}
        for c, L in terms:
            other = one
            for _, L2 in terms:
                if L2 is not L:
                    other = pmul(other, L2.den)
            for p, v in L.coef.items():
                coef[p] = padd(coef.get(p, {}), pmul(pmul(c, v), other))
        g[tgt] = RLin({p: psc(v, -1) for p, v in coef.items()}, pmul(den, lead))
    rows = []
    for tpp in range(R):
        terms = []
        for j, hj in H.items():
            t = tpp + 5 - j
            if t >= 0:
                terms.append((pmul(hj, mono_poly(5, d - j, j, t, nv)), g[t]))
        den = one
        for _, L in terms:
            den = pmul(den, L.den)
        coef = {}
        for c, L in terms:
            other = one
            for _, L2 in terms:
                if L2 is not L:
                    other = pmul(other, L2.den)
            for p, v in L.coef.items():
                coef[p] = padd(coef.get(p, {}), pmul(pmul(c, v), other))
        rows.append((coef.get(0, {}), coef.get(1, {}), den))
    return rows, used_den, tmax


def wdeg(p):
    """Weighted degree (h_j has weight j - 1, n weight 0); None if not homogeneous."""
    ws = {sum(e * (j + 2) for j, e in enumerate(k[1:])) for k in p}
    return ws.pop() if len(ws) == 1 else (None if ws else -1)


# ---- step 4: elimination trees -------------------------------------------------------------


def run_steps(steps, L, nv, N0, J, stats, depth=0):
    if depth > 60:
        raise ValueError('elimination tree too deep')
    L = list(L)
    for st in steps:
        op = st['op']
        stats['steps'] += 1
        if op == 'derive':
            P = parse(st['poly'], nv)
            acc = {}
            for idx, mult in st['combo']:
                acc = padd(acc, pmul(parse(mult, nv), L[idx]))
            if acc != P:
                raise ValueError('a derived polynomial is not the declared combination')
            L.append(P)
        elif op == 'split':
            target = L[st['idx']]
            c = parse(st['const'], nv)
            nonzero_from(c, N0)
            prod = c
            facs = []
            for q, m in st['factors']:
                qq = parse(q, nv)
                if not qq or n_only(qq):
                    raise ValueError('split factors must involve the h variables')
                facs.append(qq)
                prod = pmul(prod, ppow(qq, m, nv))
            if prod != target:
                raise ValueError('declared factorisation is wrong')
            if len(st['branches']) != len(facs):
                raise ValueError('one branch per factor is required')
            for qq, br in zip(facs, st['branches']):
                run_steps(br, L + [qq], nv, N0, J, stats, depth + 1)
            return
        elif op == 'contradiction':
            nonzero_from(L[st['idx']], N0)
            stats['contradictions'] += 1
            return
        elif op == 'target':
            if len(st['idx']) != len(J):
                raise ValueError('every generator of J must be reached')
            for idx, c, Jj in zip(st['idx'], st['const'], J):
                cc = parse(c, nv)
                nonzero_from(cc, N0)
                if L[idx] != pmul(cc, Jj):
                    raise ValueError('target identity does not give c(n) J_j')
            stats['targets'] += 1
            return
        else:
            raise ValueError(f'unknown step {op!r}')
    raise ValueError('a branch ends without a leaf')


def check_J_locus(d):
    """Common zeros of J: h = 0, or (after the torus) h_3 = 1 and
    x^(d-1) + x^(d-3) + h_4 x^(d-4) + ... = (x - a)^(d-2) (x + (d-2) a)."""
    J = J_EXPECTED[d]
    # J_1 forces h_4^2 = -c h_3^3 so h_3 = 0 implies h_4 = 0, then the others vanish too
    # (each further generator is h_j plus a multiple of a monomial containing h_3).
    for Jj in J[1:]:
        lin = [k for k in Jj if sum(k) == 1]
        if len(lin) != 1 or not all(k[0] > 0 for k in Jj if k not in lin):
            raise ValueError('J does not have the expected triangular shape')
    # at h_3 = 1: a = -h_4 / (d - 2 choose ...): compare coefficients in Q[a]/(a^2 - alpha)
    m = d - 2
    # (x - a)^m (x + m a): coefficient of x^(d-3) is (C(m,2) - m^2) a^2 = 1 -> alpha
    c2 = comb(m, 2) - m * m
    alpha = F(1, c2)
    # coefficients of (x - a)^m (x + m a) as elements u + v a of Q(a)
    poly = [(F(1), F(0))]                       # highest degree first
    def mul_lin(p, r0, r1):                      # multiply by (x + (r0 + r1 a))
        out = [(F(0), F(0))] * (len(p) + 1)
        for i, (u, v) in enumerate(p):
            ou, ov = out[i]
            out[i] = (ou + u, ov + v)
            # times (r0 + r1 a): (u + v a)(r0 + r1 a) = u r0 + v r1 alpha + (u r1 + v r0) a
            ou, ov = out[i + 1]
            out[i + 1] = (ou + u * r0 + v * r1 * alpha, ov + u * r1 + v * r0)
        return out
    for _ in range(m):
        poly = mul_lin(poly, F(0), F(-1))
    poly = mul_lin(poly, F(0), F(m))
    if poly[1] != (F(0), F(0)) or poly[2] != (F(1), F(0)):
        raise ValueError('normalisation of the multiple-root locus failed')
    h = [x for x in poly[3:]]                    # h_4 .. h_d as elements of Q(a)
    if h[0][1] == 0:
        raise ValueError('the two conjugate multiple-root points must be distinct')
    def ev(Jj):
        tot = (F(0), F(0))
        for k, c in Jj.items():
            val = (F(1), F(0))
            for j, e in enumerate(k[1:]):
                for _ in range(e):
                    u, v = val
                    x, y = h[j]
                    val = (u * x + v * y * alpha, u * y + v * x)
            tot = (tot[0] + c * val[0], tot[1] + c * val[1])
        return tot
    for Jj in J:
        if ev(Jj) != (F(0), F(0)):
            raise ValueError('J does not vanish on the multiple-root locus')
    # conversely J determines h_4^2, h_5, ..., h_d from h_3 = 1, and h_4 = -2 a or its conjugate
    return {'J_zero_locus': f'h = 0 (type ({d - 1},1)) or type ({d - 2},1,1) with P one of its simple roots',
            'alpha': str(alpha)}


def check(cert):
    if cert.get('format') != FORMAT:
        raise ValueError('not a binary-static-v1 certificate')
    d = cert['degree']
    if d not in ROWS:
        raise ValueError('degree must be 5 or 6')
    nv = d - 1
    R = ROWS[d]
    N0 = cert['N0']
    if type(N0) is not int:
        raise ValueError('N0 must be an integer')
    top = top_lemma(d, N0)
    rows, used_den, tmax = derive_rows(d, R)
    if N0 < tmax + 1:
        raise ValueError('N0 below the index validity bound')
    for den in used_den:
        nonzero_from(den, N0)
    declared = cert['rows']
    if len(declared) != R:
        raise ValueError('wrong number of rows')
    M = []
    for (A, B, den), dec in zip(rows, declared):
        a, b, s = parse(dec['A'], nv), parse(dec['B'], nv), parse(dec['scale'], nv)
        nonzero_from(s, N0)
        nonzero_from(den, N0)
        if pmul(s, a) != A or pmul(s, b) != B:
            raise ValueError('declared row is not a scalar multiple of the derived row')
        wa, wb = wdeg(a), wdeg(b)
        if None in (wa, wb) or (wa != -1 and wb != -1 and wa != wb + 1):
            raise ValueError('rows are not weighted homogeneous of degrees W + 1, W')
        M.append((a, b))
    J = [{(0,) + k: v for k, v in Jj.items()} for Jj in J_EXPECTED[d]]
    locus = check_J_locus(d)
    # the systems to cover
    required = {('one', None)} | {(c, k) for c in ('A', 'B') for k in range(d - 2)}
    seen = set()
    stats = {'steps': 0, 'contradictions': 0, 'targets': 0}
    for sysc in cert['systems']:
        case, chart = sysc['case'], sysc.get('chart')
        key = (case, chart)
        if key not in required or key in seen:
            raise ValueError(f'unexpected or repeated system {key}')
        seen.add(key)
        base = []
        for a, b in M:
            p = {'one': padd(a, b), 'A': a, 'B': b}[case]
            if chart is not None:
                for i in range(1, chart + 1):
                    p = subs_var(p, i, 0)
                p = subs_var(p, chart + 1, 1)
            base.append(p)
        Jc = []
        for Jj in J:
            q = Jj
            if chart is not None:
                for i in range(1, chart + 1):
                    q = subs_var(q, i, 0)
                q = subs_var(q, chart + 1, 1)
            Jc.append(q)
        run_steps(sysc['steps'], base, nv, N0, Jc, stats)
    if seen != required:
        raise ValueError('not every case of the kernel vector is covered')
    return {'status': 'passed', 'degree': d, 'N0': N0, 'rows': R, **top, **locus, **stats,
            'theorem': f'for every binary form H of degree {d} with a simple root and every n >= {N0}: '
                       f'E_n(H) != 0 only if H has type ({d - 1},1) or ({d - 2},1,1)'}


def main():
    try:
        print(json.dumps(check(json.loads(open(sys.argv[1]).read())), indent=1))
    except (ValueError, KeyError, IndexError, TypeError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
