#!/usr/bin/env python3
"""Triangular structures for pure tops (triangular-pure-v1). See DYNAMIC_CORE_RESULTS.md section 6.8.

Pure tops c l^d contain Hamiltonians that are simple in triangular coordinates
(Q, P) = (q, p + w(q)): the map is symplectic but not affine, so the flat gates are not
covariant under it. Below, the transvectants T_k are those of weyl_receipts:
T_k(f, g) = (d_q1 d_p2 - d_p1 d_q2)^k f(1) g(2) on the diagonal.

Theorem X (triangular transvectant formula). Write f~ = f o tau, tau(q, p) = (q, p + w(q)).
Then, as formal power series in t,
    sum_k t^k/k! T_k(h~, g~) o tau^-1
        = exp( t (dQ1 dP2 - dP1 dQ2) + sum_{j>=2} t^j w^(j)(Q)/j! (dP1 dP2^j + (-1)^j dP1^j dP2) ) h(1) g(2),
evaluated on the diagonal, with the coefficients w^(j)(Q) frozen (not differentiated).
Proof: for h = exp(dQ + aP), g = exp(cQ + bP) the p-derivatives act as a and b, and
(b d_q1 - a d_q2)^k on the diagonal is the k-th t-derivative along (q + tb, q - ta); the
exponent there is t(db - ca) + a[w(q+tb) - w(q)] + b[w(q-ta) - w(q)], whose t-linear terms
cancel. Both sides are bilinear differential operators that agree on exponentials. [X1]
checks the formula against weyl_receipts on a grid.

Theorem K (containments; P = p + w(q), Q = q, all exact):
 K1  deg w = 2, H = F(P) + lam Q:  K[P] + K Q  is contained in D_inf(H).
     Proof: for deg w = 2 the correction series is c t^2 dP1 dP2 (dP1 + dP2), even in t, and
     the flat part vanishes on K[P] x K[P]; so T_k(F(P), G(P)) = 0 for odd k. Q is linear.
     {H, P^n} = lam n P^(n-1) and {H, Q} = -F'(P).                        [K1: grid]
 K2  any w, H = h(Q, P) with h quadratic:  tau* K[Q, P]_{<=2}  is contained in D_inf(H).
     Proof: on the coefficient of t^k (k odd >= 3) every term of Theorem X has total
     derivative order 2a + sum (j + 1) >= k + 1 >= 4, split over two quadratics, so some
     factor is differentiated three times, except the order-4 term t^3 (dP1 dP2^3 - dP1^3 dP2),
     which also differentiates one factor three times. The brackets of quadratics are
     quadratic.                                                            [K2: grid]
 K3  s = 2 twisted squares. Let Q = l - gamma, G = Q m + v(l) (v any polynomial), k >= 1, and
       H = c Q^(k-2) G^2 + r  polynomial,  with  r in span{1, Q^(k-2)}  (k >= 2)  or
       Q r of degree <= 2 (k = 1, r = rational, H polynomial).
     Then span{1, G, H} (k >= 2), respectively span{1, Q, G, H} (k = 1), lies in D_inf(H).
     Proof: G is affine in m with linear m-coefficient, so T_j(G, f) = v^(j) d_m^j f for j >= 3,
     which vanishes on H (m-degree 2). {H, G} = (k-2) c (H - r) + Q r' and {H, Q} = -2 c Q^(k-1) G
     close the span under the conditions on r.                             [K3: grid]

K4 (deg w = 2, normal form H = A P^4 + (deg <= 2 in P) + mu Q (P - r)(P + 3r)): span{1, G, H} with
     G = A (P - r)^3 + c2 (P - r) + mu Q (P - r); proof and checks in check_cubic_phase.py.
K1' (deg w = 2, H = F(P) + lam Q + mu Q P, mu != 0): span{1, P, P^2, H}, together with Q if
     deg F = 3, and with P H if moreover lam = 0, lies in D_inf(H).
     Proof: Theorem X with deg w = 2; the factor Q P absorbs one d_Q and one d_P, so every odd
     term of T_k(Q P, g) differentiates g in P three times, and vanishes for g in span{1, P, P^2}.
     {H, P} = lam + mu P. For deg F = 3, {H, Q} = -F'(P) - mu Q is in the span. P H: exact
     polynomial identity verified on a tensor grid larger than its degrees.  [K1': grid]

Detection (detect) puts a pure-top H in coordinates (l, m), reads the m-degree s and the
transverse top phi, and recognises the families; certify() records explicit generators, and
check() re-verifies exactly that their span is D-invariant and killed by every gate (for K1 the
tower K[P] is truncated at P^NMAX; K1 itself proves the full tower). Equality of the cores with
these spans is verified by direct computation in the tests (conjecture P004 of the ledger).

Usage: check_triangular.py [CERT.json]
"""
from __future__ import annotations
import json
import random
import sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)]
import weyl_receipts as W            # noqa: E402
import check_two_root as TR          # noqa: E402
import qlinalg as L                  # noqa: E402

FORMAT = 'triangular-pure-v1'
NMAX = 6

# ---- univariate helpers (dict exponent -> F) ---------------------------------------------


def uderiv(u, j):
    out = {}
    for e, c in u.items():
        if e >= j:
            out[e - j] = c * comb(e, j) * factorial(j)
    return out


def U(u):
    """univariate {e: c} in Q as a bivariate polynomial."""
    return TR.tidy({(e, 0): c for e, c in u.items()})


def tri(h, w):
    """h(q, p + w(q))."""
    return TR.comp(h, {(1, 0): F(1)}, TR.add({(0, 1): F(1)}, U(w)))


def untri(f, w):
    """f(Q, P - w(Q))."""
    return TR.comp(f, {(1, 0): F(1)}, TR.add({(0, 1): F(1)}, TR.sc(U(w), F(-1))))


# ---- Theorem X: the triangular transvectants ------------------------------------------------


def _opmul(A, B):
    """bidifferential operators {(a, b, c, e): poly in Q}: d_Q1^a d_P1^b d_Q2^c d_P2^e."""
    out = {}
    for ka, pa in A.items():
        for kb, pb in B.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            out[k] = TR.add(out.get(k, {}), TR.mul(pa, pb))
    return {k: v for k, v in out.items() if v}


def _opadd(*As):
    out = {}
    for A in As:
        for k, v in A.items():
            out[k] = TR.add(out.get(k, {}), v)
    return {k: v for k, v in out.items() if v}


def _opsc(A, c):
    return {k: TR.sc(v, c) for k, v in A.items() if c}


def tau_series(w, kmax):
    """E_k with sum_k t^k E_k = exp(sum_j t^j X_j) (commuting operators): E_k = (1/k) sum j X_j E_(k-j)."""
    one = {(0, 0): F(1)}
    X = {1: {(1, 0, 0, 1): one, (0, 1, 1, 0): {(0, 0): F(-1)}}}
    for j in range(2, kmax + 1):
        c = U(uderiv(w, j))
        if c:
            X[j] = {(0, 1, 0, j): TR.sc(c, F(1, factorial(j))),
                    (0, j, 0, 1): TR.sc(c, F((-1) ** j, factorial(j)))}
    E = [{(0, 0, 0, 0): one}]
    for k in range(1, kmax + 1):
        acc = {}
        for j in range(1, k + 1):
            if j in X:
                acc = _opadd(acc, _opsc(_opmul(X[j], E[k - j]), F(j)))
        E.append(_opsc(acc, F(1, k)))
    return E


def apply_bi(A, h, g):
    out = {}
    for (a, b, c, e), coef in A.items():
        dh = W.pder(h, a, b)
        dg = W.pder(g, c, e)
        if dh and dg:
            out = TR.add(out, TR.mul(coef, TR.mul(dh, dg)))
    return out


def tau_T(h, g, w, k, E=None):
    E = E or tau_series(w, k)
    return TR.sc(apply_bi(E[k], h, g), F(factorial(k)))


def flat_T(Hq, Gq, k):
    return W.act(W.gate(Hq, k), Gq) if k >= 1 else TR.mul(Hq, Gq)


def rand_poly(rng, deg, dens=0.6):
    return TR.tidy({(i, s - i): F(rng.randint(-3, 3)) for s in range(deg + 1) for i in range(s + 1)
                    if rng.random() < dens})


def grid_X(n=40, seed=3):
    rng = random.Random(seed)
    for _ in range(n):
        w = {e: F(rng.randint(-2, 2)) for e in range(rng.randint(2, 5) + 1)}
        h, g = rand_poly(rng, rng.randint(1, 4)), rand_poly(rng, rng.randint(1, 4))
        E = tau_series(w, 7)
        for k in range(1, 8):
            lhs = untri(flat_T(tri(h, w), tri(g, w), k), w)
            if lhs != tau_T(h, g, w, k, E):
                return False
    return True


# ---- exact invariant-span certificates -------------------------------------------------------


def span_ok(H, gens):
    """span(gens) is D-invariant and killed by every gate C_k = T_k(H, .), k odd >= 3."""
    gens = [TR.tidy(g) for g in gens]
    D, gates = W.derivation(H), W.gates(H)
    mons = sorted({m for g in gens for m in g})
    for g in gens:
        for Ck in gates.values():
            if W.act(Ck, g):
                return False
        Dg = W.act(D, g)
        mons2 = sorted(set(mons) | set(Dg))
        if set(Dg) - set(mons):
            return False
        rows = [[gg.get(m, F(0)) for gg in gens] for m in mons2]
        if L.rank(rows, len(gens)) != L.rank([r + [Dg.get(m, F(0))] for r, m in zip(rows, mons2)], len(gens) + 1):
            return False
    return True


def grid_K(seed=5):
    rng = random.Random(seed)
    ok = {'K1': True, 'K2': True, 'K3': True}
    for _ in range(6):
        w = {2: F(rng.choice([1, -2])), 1: F(rng.randint(-2, 2)), 0: F(rng.randint(-1, 1))}
        Fp = {(0, j): F(rng.randint(-2, 2)) for j in range(rng.randint(2, 4))}
        Fp[(0, rng.randint(3, 4))] = F(1)
        lam = F(rng.randint(-2, 2))
        H = tri(TR.add(Fp, {(1, 0): lam}), w)
        gens = [{(0, 0): F(1)}, {(1, 0): F(1)}] + [tri({(0, n): F(1)}, w) for n in range(1, NMAX + 1)]
        ok['K1'] &= span_ok(H, gens)
    for _ in range(6):
        w = {e: F(rng.randint(-2, 2)) for e in range(rng.randint(2, 5))}
        w[rng.randint(3, 5)] = F(1)
        h = TR.add(rand_poly(rng, 2), {(0, 2): F(rng.choice([1, 2, -1]))})
        H = tri(h, w)
        gens = [tri({m: F(1)}, w) for m in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))]
        ok['K2'] &= span_ok(H, gens)
    ok["K1'"] = True
    for _ in range(4):                     # K1': span{1, P, P^2, H} (+ Q for deg F = 3)
        w = {2: F(rng.choice([1, 3])), 1: F(rng.randint(-2, 2))}
        f = rng.randint(3, 5)
        h = {(0, f): F(1), (1, 1): F(rng.choice([1, -2])), (1, 0): F(rng.randint(-2, 2))}
        for j in range(f - 1):
            h[(0, j)] = F(rng.randint(-2, 2))
        H = tri(TR.tidy(h), w)
        gens = [{(0, 0): F(1)}, tri({(0, 1): F(1)}, w), tri({(0, 2): F(1)}, w), H] + ([{(1, 0): F(1)}] if f == 3 else [])
        ok["K1'"] &= span_ok(H, gens)
    # deg F = 3, lam = 0: P H is in the core. T_k(H, P H) is bilinear in H and P H, so of degree <= 2
    # in each of mu, a, b (H = P^3 + a P + b + mu Q P), and depends on w only through c = w''/2 with
    # degree <= 2 (k <= 7 and each correction factor uses three derivatives): the 3^4 tensor grid
    # below proves the identity for all values.
    for c in (1, 2, -3):
        for mu in (1, -1, 2):
            for a in (0, 1, -2):
                for b in (0, 1, 3):
                    w = {2: F(c)}
                    H = tri({(0, 3): F(1), (0, 1): F(a), (0, 0): F(b), (1, 1): F(mu)}, w)
                    gens = [{(0, 0): F(1)}, {(1, 0): F(1)}, tri({(0, 1): F(1)}, w), tri({(0, 2): F(1)}, w), H,
                            TR.mul(tri({(0, 1): F(1)}, w), H)]
                    ok["K1'"] &= span_ok(H, gens)
    for k in range(1, 5):
        for _ in range(3):
            gam = F(rng.randint(-1, 1))
            Q = {(1, 0): F(1), (0, 0): -gam}
            v = TR.tidy({(i, 0): F(rng.randint(-2, 2)) for i in range(rng.randint(2, 4))})
            G = TR.add(TR.mul(Q, {(0, 1): F(1)}), v)
            c = F(rng.choice([1, -1, 2]))
            if k >= 2:
                r = TR.add({(0, 0): F(rng.randint(-2, 2))}, TR.sc(TR.power(Q, k - 2), F(rng.randint(-2, 2))))
                H = TR.add(TR.sc(TR.mul(TR.power(Q, k - 2), TR.mul(G, G)), c), r)
                gens = [{(0, 0): F(1)}, G, H]
            else:
                # c (G^2 - v(gamma)^2)/Q + a Q + b : polynomial, Q r of degree <= 2
                v0 = sum(cc * gam ** i for (i, _), cc in v.items())
                num = TR.add(TR.mul(G, G), {(0, 0): -v0 * v0})
                quo = _divide_by_linear(num, gam)
                H = TR.add(TR.sc(quo, c), TR.sc(Q, F(rng.randint(-2, 2))), {(0, 0): F(rng.randint(-2, 2))})
                gens = [{(0, 0): F(1)}, Q, G, H]
            ok['K3'] &= span_ok(H, gens)
    return ok


def _divide_by_linear(f, gam):
    """f / (q - gam) for f vanishing on q = gam (exact synthetic division in q)."""
    out = {}
    byj = {}
    for (i, j), c in f.items():
        byj.setdefault(j, {})[i] = c
    for j, col in byj.items():
        n = max(col)
        rem = F(0)
        quot = {}
        for i in range(n, -1, -1):
            rem = rem * gam + col.get(i, F(0))
            if i > 0:
                quot[i - 1] = rem
        if rem != 0:
            raise ValueError('not divisible')
        for i, c in quot.items():
            if c:
                out[(i, j)] = c
    return TR.tidy(out)


# ---- detection of the families for a pure top ------------------------------------------------


def _to_qp(g, l):
    """g(X, Y) -> polynomial in (q, p), with X = l, Y = m as in check_two_root.coords."""
    a, b = l.get((1, 0), F(0)), l.get((0, 1), F(0))
    if a != 0:
        X, Y = {(1, 0): a, (0, 1): b}, {(0, 1): F(1)}
    else:
        X, Y = {(0, 1): b}, {(1, 0): F(1)}
    return TR.comp(g, X, Y)


def _udiv(a, b):
    """exact univariate division a / b, or None."""
    a = dict(a)
    db, lb = max(b), b[max(b)]
    q = {}
    while a and max(a) >= db:
        da = max(a)
        c = a[da] / lb
        q[da - db] = c
        for e, v in b.items():
            a[e + da - db] = a.get(e + da - db, F(0)) - c * v
        a = {e: v for e, v in a.items() if v}
    return None if a else q


def _umul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, F(0)) + x * y
    return {e: v for e, v in out.items() if v}


def _uadd(*ps):
    out = {}
    for p in ps:
        for e, v in p.items():
            out[e] = out.get(e, F(0)) + v
    return {e: v for e, v in out.items() if v}


def _usc(a, c):
    return {e: v * c for e, v in a.items() if v * c}


def _upow(a, n):
    out = {0: F(1)}
    for _ in range(n):
        out = _umul(out, a)
    return out


def _k4(h):
    """For h = a(P) + Q b(P) in normal form (no P^3): if deg a = 4 and b = mu (P - r)(P + 3r), return
    G = A (P - r)^3 + c2 (P - r) + mu Q (P - r), c2 the (P - r)^2 coefficient of a; else None."""
    a = {j: c for (i, j), c in h.items() if i == 0}
    b = {j: c for (i, j), c in h.items() if i == 1}
    if not a or max(a) != 4 or a.get(3) or not b or max(b) != 2:
        return None
    mu, nu = b[2], b.get(1, F(0))
    r = nu / (2 * mu)
    if b.get(0, F(0)) != -3 * mu * r * r:
        return None
    c2 = sum(c * comb(j, 2) * r ** (j - 2) for j, c in a.items() if j >= 2)
    lin = {1: F(1), 0: -r}
    G = TR.add({(0, j): a[4] * c for j, c in _upow(lin, 3).items()},
               {(0, j): c2 * c for j, c in lin.items()},
               {(1, j): mu * c for j, c in lin.items()})
    return G


def detect(H, l):
    """Recognise K1, K2, K3 for a pure top with root form l. Returns None or a dict with the
    family, the generators (polynomials in q, p) and the conjectured core."""
    Ht = TR.coords(H, l)
    s = max(j for _, j in Ht)
    col = lambda j: {i: c for (i, jj), c in Ht.items() if jj == j}
    phi = col(s)
    k = max(phi)
    c0 = phi[k]
    out = None
    if k == 0:
        w = _usc(col(s - 1), 1 / (s * c0))
        h = untri(Ht, w)
        if not w or max(w) < 2:
            return None
        e = max(w)
        quad = [tri({m: F(1)}, w) for m in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))]
        tower = all(i == 0 or (i, j) == (1, 0) for (i, j) in h)      # h in K[P] + K Q
        if s == 2 and all(i + j <= 2 for (i, j) in h):
            if e == 2 and tower:
                out = {'family': 'K1+K2', 'core': 'K[P] + tau*K[Q,P]_{<=2}',
                       'gens': quad + [tri({(0, n): F(1)}, w) for n in range(3, NMAX + 1)],
                       'degrees': [0, 1, 2, 2, 3, 4], 'tower_step': 2, 'tower_from': 3}
            else:
                out = {'family': 'K2', 'core': 'tau*K[Q,P]_{<=2}', 'gens': quad,
                       'degrees': sorted([0, 1, 2, e, e + 1, 2 * e])}
        elif e == 2 and tower:
            out = {'family': 'K1', 'core': 'K[P] + K Q', 'gens': [{(0, 0): F(1)}, {(1, 0): F(1)}] +
                   [tri({(0, n): F(1)}, w) for n in range(1, NMAX + 1)],
                   'degrees': [0, 1], 'tower_step': 2, 'tower_from': 1,
                   'proved': True}                      # equality: Theorem A + Lemma C (check_gauge.py)
        elif e == 2 and s == 4 and all(i <= 1 for (i, j) in h) and _k4(h) is not None:
            # K4 (check_cubic_phase.py): h = A P^4 + (deg <= 2) + mu Q (P - r)(P + 3r)
            gens = [{(0, 0): F(1)}, tri(_k4(h), w), Ht]
            out = {'family': 'K4', 'core': 'span{1, G, H}', 'gens': gens, 'degrees': [0, 6, TR.degree(Ht)]}
        elif e == 2 and all(i == 0 or (i, j) in ((1, 0), (1, 1)) for (i, j) in h):
            # K1': h = F(P) + lam Q + mu Q P with mu != 0 (s >= 3, so P^(s-1) is absent)
            lam = h.get((1, 0), F(0))
            gens = [{(0, 0): F(1)}] + [tri({(0, n): F(1)}, w) for n in (1, 2)] + [Ht]
            core = 'span{1, P, P^2, H}'
            if s == 3:
                gens.append({(1, 0): F(1)})
                core = 'span{1, Q, P, P^2, H}'
                if lam == 0:
                    gens.append(TR.mul(tri({(0, 1): F(1)}, w), Ht))
                    core = 'span{1, Q, P, P^2, H, P H}'
            d = TR.degree(Ht)
            out = {'family': "K1'", 'core': core, 'gens': gens,
                   'degrees': sorted([0, 2, 4, d] + ([1] if s == 3 else []) + ([d + 2] if len(gens) == 6 else []))}
        if out:
            out['w'] = {str(i): str(c) for i, c in sorted(w.items())}
    elif s == 2:
        gam = -phi.get(k - 1, F(0)) / (k * c0)
        Qu = {1: F(1), 0: -gam}
        if phi != _usc(_upow(Qu, k), c0):
            return None
        v = _udiv(col(1), _usc(_upow(Qu, k - 1), 2 * c0))
        if v is None:
            return None
        h0 = col(0)
        Gx = TR.add({(1, 1): F(1), (0, 1): -gam}, U(v))
        if k >= 2:
            r = _uadd(h0, _usc(_umul(_upow(Qu, k - 2), _umul(v, v)), -c0))
            basis = [{0: F(1)}, _upow(Qu, k - 2)]
            rows = [[b.get(e, F(0)) for b in basis] + [r.get(e, F(0))] for e in set(r) | {0, k - 2}]
            if L.rank([x[:-1] for x in rows], 2) != L.rank(rows, 3):
                return None
            gens = [{(0, 0): F(1)}, Gx, Ht]
            out = {'family': 'K3', 'core': 'span{1, G, H}', 'gens': gens}
        else:
            Qr = _uadd(_umul(Qu, h0), _usc(_umul(v, v), -c0))
            if Qr and max(Qr) > 2:
                return None
            gens = [{(0, 0): F(1)}, {(1, 0): F(1), (0, 0): -gam}, Gx, Ht]
            out = {'family': 'K3', 'core': 'span{1, Q, G, H}', 'gens': gens}
        out['G'] = TR.ser(_to_qp(Gx, l))
        out['degrees'] = sorted(TR.degree(_to_qp(g, l)) for g in out['gens'])
    if out is None:
        return None
    out['gens'] = [_to_qp(g, l) for g in out['gens']]
    return out


def cubic_phase(H, l):
    """'affine' or 'general' when the transverse top is constant and the completed power w has degree 2
    (h affine in Q or not), else False. In this case the
    triangular map is then the cubic phase exp(i c q^3 / hbar), where the families are not known
    to be exhaustive (e.g. (q^2 + p)^4 + q (q^2 + p)^2 has a third core element)."""
    Ht = TR.coords(H, l)
    s = max(j for _, j in Ht)
    phi = {i: c for (i, j), c in Ht.items() if j == s}
    if max(phi) != 0:
        return False
    w = {i: c for (i, j), c in Ht.items() if j == s - 1}
    if not (w and max(w) == 2):
        return False
    h = untri(Ht, _usc(w, 1 / (s * phi[0])))
    return 'affine' if all(i <= 1 for (i, j) in h) else 'general'


def affine_data(H, l):
    """For a constant transverse top: (deg w, deg_P a, deg_P b) of the normal form h = a + Q b when h is
    affine in Q (deg b = -1 for b = 0); else None."""
    Ht = TR.coords(H, l)
    s = max(j for _, j in Ht)
    phi = {i: c for (i, j), c in Ht.items() if j == s}
    if max(phi) != 0:
        return None
    w = _usc({i: c for (i, j), c in Ht.items() if j == s - 1}, 1 / (s * phi[0]))
    if not w:
        return None
    h = untri(Ht, w)
    if any(i > 1 for (i, j) in h):
        return None
    bdeg = max((j for (i, j) in h if i == 1), default=-1)
    return max(w), s, bdeg


def first_edge(H, l):
    """(e, s, alpha, edge) for a constant transverse top: e = deg w, s = deg_P h, alpha the slope of the
    first Newton edge of h from P^s (min (s - j)/i over monomials Q^i P^j with i >= 1), edge = those
    monomials; None if the transverse top is not constant or h has no Q-dependence."""
    Ht = TR.coords(H, l)
    s = max(j for _, j in Ht)
    phi = {i: c for (i, j), c in Ht.items() if j == s}
    if max(phi) != 0:
        return None
    w = _usc({i: c for (i, j), c in Ht.items() if j == s - 1}, 1 / (s * phi[0]))
    h = untri(Ht, w)
    qm = [(i, j) for (i, j) in h if i >= 1]
    if not qm:
        return None
    alpha = min(F(s - j, i) for (i, j) in qm)
    return (max(w) if w else -1), s, alpha, sorted(m for m in qm if F(s - m[1], m[0]) == alpha)


def na_applies(H, l):
    """Theorem NA (check_gauge.py): binomial first edge P^s + c Q^d with d >= 2 (s >= 3) or d >= 3 (s = 2),
    slope s/d above the threshold."""
    fe = first_edge(H, l)
    if fe is None:
        return False
    e, s, alpha, edge = fe
    if e < 2 or s < 2 or len(edge) != 1 or edge[0][1] != 0 or edge[0][0] < (2 if s >= 3 else 3):
        return False
    return alpha > (F(1, 2) if e == 2 else F(1, e))


def edge_route(H, l):
    """'NA' (binomial edge), 'NE' (general first edge) or 'NB' (boundary edge P^2 + c Q^(2e)) when the
    corresponding theorem of check_gauge.py applies; else None."""
    fe = first_edge(H, l)
    if fe is None:
        return None
    e, s, alpha, edge = fe
    if e < 2:
        return None
    thr = F(1, 2) if e == 2 else F(1, e)
    if na_applies(H, l):
        return 'NA'
    if s == 2 and edge == [(2 * e, 0)] and alpha == F(1, e):
        return 'NB'
    if s >= 3 and alpha > thr and alpha < s - 1 and (e >= 3 or any(i >= 2 for i, _ in edge)):
        return 'NE'
    return None


def higher_shear(H, l):
    """Constant transverse top, completed power w of degree >= 3 and h affine in Q with deg_P h >= 3:
    'const' if the Q-coefficient b is constant (D_inf = span{1, H}: Theorem AE + Lemma C), 'affine'
    otherwise (span{1, H} proved inside tau*(K[P] + Q K[P])); else None."""
    Ht = TR.coords(H, l)
    s = max(j for _, j in Ht)
    phi = {i: c for (i, j), c in Ht.items() if j == s}
    if max(phi) != 0 or s < 3:
        return None
    w = _usc({i: c for (i, j), c in Ht.items() if j == s - 1}, 1 / (s * phi[0]))
    if not w or max(w) < 3:
        return None
    h = untri(Ht, w)
    if any(i > 1 for (i, j) in h):
        return None
    return 'const' if all(j == 0 for (i, j) in h if i == 1) else 'affine'


def core_dim(res, N):
    """dimension in degrees <= N of the span recorded by detect (tower included)."""
    n = sum(1 for e in res['degrees'] if e <= N)
    if 'tower_step' in res:
        n += sum(1 for t in range(res['tower_from'], N + 1) if t * res['tower_step'] <= N)
    return n


# ---- certificates -------------------------------------------------------------------------


def certify(H):
    H = TR.tidy(H)
    res = TR.classify(H)
    if res.get('route') not in ('K1', "K1'", 'K2', 'K1+K2', 'K3', 'K4'):
        raise ValueError('not a triangular family')
    cert = {'format': FORMAT, 'hamiltonian': TR.ser(H), 'family': res['route'], 'core': res['core'],
            'generators': res['generators']}
    cert['result'] = check(cert)
    return cert


def identities():
    res = {'X1': grid_X()}
    res.update(grid_K())
    return res


def check(cert=None):
    if cert is not None and cert.get('format') != FORMAT:
        raise ValueError('not a triangular-pure-v1 certificate')
    if cert is None or 'hamiltonian' not in cert:
        res = identities()
        bad = [k for k, v in res.items() if not v]
        if bad:
            raise ValueError(f'identities fail: {bad}')
        if cert is not None and cert.get('identities') != sorted(res):
            raise ValueError('certificate lists other identities')
        return {'status': 'passed', 'identities': sorted(res),
                'theorem': 'triangular transvectant formula; containments K1, K2, K3'}
    H = {tuple(map(int, k.split(','))): F(v) for k, v in cert['hamiltonian'].items()}
    gens = [{tuple(map(int, k.split(','))): F(v) for k, v in g.items()} for g in cert['generators']]
    res = TR.classify(H)
    if res.get('route') != cert.get('family') or res.get('core') != cert.get('core'):
        raise ValueError('declared family differs from the recomputed one')
    if not span_ok(H, gens):
        raise ValueError('generators are not an invariant span killed by the gates')
    rank = L.rank([[g.get(m, F(0)) for g in gens] for m in sorted({m for g in gens for m in g})], len(gens))
    if rank != len(gens):
        raise ValueError('generators are dependent')
    if rank <= 2:
        raise ValueError('span does not exceed span{1, H}')
    return {'status': 'passed', 'family': res['route'], 'core': res['core'],
            'verified_dimension': len(gens), 'claim': 'contained in D_inf(H) (exact)'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
