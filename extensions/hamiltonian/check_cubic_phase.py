#!/usr/bin/env python3
"""The cubic-phase case of pure tops (cubic-phase-v1). See DYNAMIC_CORE_RESULTS.md section 6.9.

Setting: P = p + w(q) with deg w = 2, c = w''/2, Q = q; tilde = pullback to (q, p). Notation as in
check_triangular.py (Theorem X).

Theorem G (gauge form). Let S_s = exp(s d_P^3) and s = c t^2 / 3. Then
    sum_k t^k/k! T_k(h~, g~) o tau^-1 = S_s[ sum_a t^a/a! T^flat_a(S_-s h, S_-s g) ],
where T^flat are the flat transvectants in (Q, P).
Proof: in Theorem X only j = 2 survives, c t^2 (dP1 dP2^2 + dP1^2 dP2), and
x y (x + y) = ((x + y)^3 - x^3 - y^3)/3 makes exp(c t^2 dP1 dP2 (dP1 + dP2)) = S_s o mult o (S_-s x S_-s)
on the diagonal; the flat operator has constant coefficients and commutes with all of it.  [G1]

Since S_s is even in t, the odd part of the series is S_s applied to the flat odd part. Hence
G is killed by every gate of H~ iff, as series in t, flat-odd(S_-s h, S_-s g) = t S_-s {h, g}.

Theorem A (affine sector). If h = a(P) + Q b(P) and g = alpha(P) + Q beta(P) are affine in Q, the
flat odd part is t {.,.}, so  T_k(h~, g~) = 0 for all odd k >= 3  iff
    S_s {S_-s h, S_-s g} = {h, g}  for all s  iff  Delta(S_s h, S_s g) = 0 for all s,
where Delta(X, Y) = d^3{X, Y} - {d^3 X, Y} - {X, d^3 Y} (d = d_P). For X = (a, b), Y = (alpha, beta)
the bracket is {X, Y} = (b alpha' - a' beta) + Q (b beta' - b' beta) (a vector field b d_P acting on
functions, the Witt algebra), and                                                        [G2], [G3]
    Delta_Witt = 3 (b' beta''' - b''' beta')            (Gelfand-Fuchs cocycle density),
    Delta_fun  = 3 (b' alpha''' + b'' alpha'' - a''' beta' - a'' beta'').

Lemma W (Witt obstruction). If deg b >= 3, every element of D_inf(H~) affine in Q lies in
span{1, H~}. Proof: Delta_Witt = 0 forces beta' = lambda b' (b' beta'' - b'' beta' = kappa gives
beta' = b'(lambda + kappa int b'^-2), which is a polynomial only for kappa = 0, since b'^-2 decays at
infinity faster than 1/P); subtract lambda h. Then Delta_fun = 3 (b' alpha'')' forces b' alpha'' = const,
so alpha'' = 0 and g in span{1, P, Q}. {H, P} = b and {H, Q} = -a' - Q b' leave that span unless
their coefficients vanish.                                                              [W: grid]

Theorem K4 (twisted quartic). Let b = mu (P - r)(P - r') and
a = A (P - r)^3 (P - r') + c2 (P - r)^2 + c1 (P - r) + c0 with A mu != 0, h = a + Q b. Then
G = A (P - r)^3 + c2 (P - r) + mu Q (P - r) satisfies {H, G} = -mu (H + (r' - r) G) + const, and
span{1, G, H} lies in D_inf(H~). In the normal form (no P^3 term) the condition reads r' = -3r:
h = A P^4 + (deg <= 2) + mu Q (P - r)(P + 3r).
Proof: centre at r. b and beta = mu (P - r) lie in sl2, so Delta_Witt = 0. Delta_fun reduces to
d/dP [b' alpha'' - beta' a''], and b' alpha'' - beta' a'' = -2 mu c2 is constant for the stated
alpha; S_s adds to h and G only terms of degree <= 1 in P (and Delta_fun of those vanishes),
so Delta(S_s h, S_s G) = 0 for all s. The bracket is a direct computation.            [K4: grid]

Theorem A (affine sector inside tau* V, V = K[P] + Q K[P]). For h = a + Q b with deg a = f >= 3,
D_inf(H~) restricted to pullbacks of V is:
  b constant:          K[P] + K Q                                   (K1)
  b linear:            span{1, P, P^2, H}, with Q if f = 3, and with a further element (P H for
                       r = 0) if f = 3 and a = A (P - r)^3 + O(P - r) at the root r of b    (K1')
  b quadratic:         span{1, G, H} if K4 holds, else span{1, H}
  deg b >= 3:          span{1, H}                                   (Lemma W)
Proof (b in sl2): with beta in sl2 the all-order condition is b' alpha'' - beta' a'' in K and
deg(b'' alpha - beta'' a) <= 4; elements with beta = 0 are constants (b quadratic) or span{1, P, P^2}
(b linear); the Witt projection is an ad_b-invariant subspace of sl2 containing b, and each
invariant subspace is solved explicitly (DYNAMIC_CORE_RESULTS.md section 6.9).          [A: grid]

Usage: check_cubic_phase.py [CERT.json]
"""
from __future__ import annotations
import json
import random
import sys
from fractions import Fraction as F
from math import factorial
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)]
import weyl_receipts as W            # noqa: E402
import check_two_root as TR          # noqa: E402
import check_triangular as CT        # noqa: E402
import qlinalg as L                  # noqa: E402

FORMAT = 'cubic-phase-v1'


def S(f, s):
    """exp(s d_P^3) f."""
    out, term, n = dict(f), dict(f), 0
    while term:
        n += 1
        term = TR.sc(W.pder(term, 0, 3), s / n)
        out = TR.add(out, term)
    return out


def flat(x, y, a):
    return TR.mul(x, y) if a == 0 else W.act(W.gate(x, a), y)


def gauge_T(h, g, c, k):
    """k! [t^k] S_s(flat_t(S_-s h, S_-s g)), s = c t^2/3, expanded order by order in t."""
    def Spow(f, n, sign):            # coefficient of t^(2n) in S_(sign c t^2/3) f
        return TR.sc(W.pder(f, 0, 3 * n), (sign * c / 3) ** n / factorial(n))
    out = {}
    for n0 in range(k // 2 + 1):
        for n1 in range(k // 2 + 1 - n0):
            for n2 in range(k // 2 + 1 - n0 - n1):
                a = k - 2 * (n0 + n1 + n2)
                if a < 0:
                    continue
                x, y = Spow(h, n1, -1), Spow(g, n2, -1)
                if not x or not y:
                    continue
                inner = TR.sc(flat(x, y, a), F(1, factorial(a)))
                out = TR.add(out, Spow(inner, n0, 1))
    return TR.sc(out, F(factorial(k)))


def grid_G1(n=25, seed=11):
    rng = random.Random(seed)
    for _ in range(n):
        c = F(rng.choice([1, -2, 3]))
        w = {2: c, 1: F(rng.randint(-2, 2))}
        h, g = CT.rand_poly(rng, rng.randint(1, 5)), CT.rand_poly(rng, rng.randint(1, 5))
        E = CT.tau_series(w, 7)
        for k in range(1, 8):
            if gauge_T(h, g, c, k) != CT.tau_T(h, g, w, k, E):
                return False
    return True


# ---- the affine sector ---------------------------------------------------------------------


def ud(u, j=1):
    return CT.uderiv(u, j)


def bracket(X, Y):
    (a, b), (al, be) = X, Y
    return (CT._uadd(CT._umul(b, ud(al)), CT._usc(CT._umul(ud(a), be), -1)),
            CT._uadd(CT._umul(b, ud(be)), CT._usc(CT._umul(ud(b), be), -1)))


def d3(X):
    return (ud(X[0], 3), ud(X[1], 3))


def delta(X, Y):
    B = bracket(X, Y)
    t1, t2 = bracket(d3(X), Y), bracket(X, d3(Y))
    return tuple(CT._uadd(ud(B[i], 3), CT._usc(t1[i], -1), CT._usc(t2[i], -1)) for i in range(2))


def delta_formula(X, Y):
    (a, b), (al, be) = X, Y
    m = CT._umul
    fun = CT._usc(CT._uadd(m(ud(b), ud(al, 3)), m(ud(b, 2), ud(al, 2)),
                           CT._usc(m(ud(a, 3), ud(be)), -1), CT._usc(m(ud(a, 2), ud(be, 2)), -1)), 3)
    witt = CT._usc(CT._uadd(m(ud(b), ud(be, 3)), CT._usc(m(ud(b, 3), ud(be)), -1)), 3)
    return fun, witt


def to_poly(X):
    """(a, b) -> a(P) + Q b(P) as {(i, j): c} for Q^i P^j."""
    return TR.tidy({**{(0, j): c for j, c in X[0].items()}, **{(1, j): c for j, c in X[1].items()}})


def grid_G2(nmax=8):
    """Delta formulas on the monomial basis (bilinear, so this proves them up to degree nmax)."""
    mono = [{i: F(1)} for i in range(nmax + 1)]
    zero = {}
    for x in mono:
        for y in mono:
            for X, Y in (((x, zero), (y, zero)), ((x, zero), (zero, y)), ((zero, x), (y, zero)), ((zero, x), (zero, y))):
                if delta(X, Y) != delta_formula(X, Y):
                    return False
    return True


def grid_G3(n=30, seed=13):
    """For pairs affine in Q: odd gates of the pullbacks = k! [t^k] t S_s{S_-s h, S_-s g}."""
    rng = random.Random(seed)
    for _ in range(n):
        c = F(rng.choice([1, 2, -1]))
        w = {2: c, 0: F(rng.randint(-1, 1))}
        X = ({i: F(rng.randint(-2, 2)) for i in range(rng.randint(3, 6))}, {i: F(rng.randint(-2, 2)) for i in range(rng.randint(1, 4))})
        Y = ({i: F(rng.randint(-2, 2)) for i in range(rng.randint(3, 6))}, {i: F(rng.randint(-2, 2)) for i in range(rng.randint(1, 4))})
        h, g = TR.tidy(to_poly(X)), TR.tidy(to_poly(Y))
        for k in (3, 5, 7):
            lhs = CT.untri(W.act(W.gate(CT.tri(h, w), k), CT.tri(g, w)), w)
            # t S_s {S_-s h, S_-s g}: coefficient of t^k needs s^((k-1)/2)
            m = (k - 1) // 2
            rhs = {}
            for n0 in range(m + 1):
                for n1 in range(m + 1 - n0):
                    n2 = m - n0 - n1
                    x = TR.sc(W.pder(h, 0, 3 * n1), (-c / 3) ** n1 / factorial(n1))
                    y = TR.sc(W.pder(g, 0, 3 * n2), (-c / 3) ** n2 / factorial(n2))
                    br = W.act(W.derivation(x), y) if x and y else {}
                    rhs = TR.add(rhs, TR.sc(W.pder(br, 0, 3 * n0), (c / 3) ** n0 / factorial(n0)))
            if lhs != TR.sc(rhs, F(factorial(k))):
                return False
    return True


def affine_core_dim(H, w, pdeg, R=8):
    """dim of {g = alpha(P) + Q beta(P), deg_P <= pdeg} in D_inf(H) at depth R (pullbacks)."""
    cands = [CT.tri({(i, j): F(1)}, w) for i in (0, 1) for j in range(pdeg + 1)]
    D, gates = W.derivation(H), W.gates(H)
    cols = []
    for g in cands:
        img = {}
        for r in range(R + 1):
            for k, Ck in gates.items():
                for e, v in W.act(Ck, g).items():
                    img[(r, k, e)] = v
            g = W.act(D, g)
        cols.append(img)
    keys = sorted({k for col in cols for k in col})
    M = [[col.get(k, F(0)) for col in cols] for k in keys]
    return len(cands) - (L.rank(M, len(cands)) if M else 0)


def grid_W(n=6, seed=17):
    """Lemma W instances: deg b >= 3 gives an affine core of dimension 2 (1 and H)."""
    rng = random.Random(seed)
    for _ in range(n):
        f = rng.choice([5, 6])
        bdeg = rng.randint(3, f - 2)
        a = {f: F(1), **{i: F(rng.randint(-2, 2)) for i in range(f - 1)}}
        b = {bdeg: F(rng.choice([1, -1, 2])), **{i: F(rng.randint(-2, 2)) for i in range(bdeg)}}
        w = {2: F(1)}
        H = TR.tidy(CT.tri(to_poly((a, b)), w))
        if affine_core_dim(H, w, f + 1) != 2:
            return False
    return True


def k4_h_G(A, mu, r, rp, c2, c1, c0, w):
    lin = {1: F(1), 0: -r}
    a = CT._uadd(CT._usc(CT._umul(CT._upow(lin, 3), {1: F(1), 0: -rp}), A), CT._usc(CT._upow(lin, 2), c2),
                 CT._usc(lin, c1), {0: c0})
    b = CT._usc(CT._umul(lin, {1: F(1), 0: -rp}), mu)
    h = to_poly((a, b))
    G = to_poly((CT._uadd(CT._usc(CT._upow(lin, 3), A), CT._usc(lin, c2)), CT._usc(lin, mu)))
    return TR.tidy(CT.tri(h, w)), TR.tidy(CT.tri(G, w))


def grid_K4(n=10, seed=19):
    rng = random.Random(seed)
    for _ in range(n):
        A, mu = F(rng.choice([1, 2, -1])), F(rng.choice([1, -3, 2]))
        r, rp = F(rng.randint(-2, 2)), F(rng.randint(-2, 2))
        c2, c1, c0 = (F(rng.randint(-2, 2)) for _ in range(3))
        w = {2: F(rng.choice([1, 2, -1])), 1: F(rng.randint(-2, 2)), 0: F(rng.randint(-1, 1))}
        H, G = k4_h_G(A, mu, r, rp, c2, c1, c0, w)
        if not CT.span_ok(H, [{(0, 0): F(1)}, G, H]):
            return False
        DG = W.act(W.derivation(H), G)
        rest = TR.add(DG, TR.sc(H, mu), TR.sc(G, mu * (rp - r)))
        if any(k != (0, 0) for k in rest):
            return False
    return True


def grid_A(seed=23):
    """Theorem A instances: affine core dimension against the table (P-degree box f + 2)."""
    rng = random.Random(seed)
    w = {2: F(1)}
    cases = []
    for f in (3, 4, 5):
        a = {f: F(1), **{i: F(rng.randint(-2, 2)) for i in range(f - 1)}}
        cases.append(((a, {0: F(1)}), None))                                   # K1: infinite tower
        cases.append(((a, {1: F(1), 0: F(rng.randint(-2, 2))}), 4 + (f == 3)))  # K1' generic
        cases.append(((a, {2: F(1), 1: F(1)}), 2))                             # quadratic, not K4
    cases.append((({3: F(1), 1: F(1)}, {1: F(1)}), 6))                        # K1' with the extra element
    cases.append((({4: F(1), 1: F(-1)}, {2: F(1), 1: F(2), 0: F(-3)}), 3))    # K4, r = 1, r' = -3
    for (X, want) in cases:
        H = TR.tidy(CT.tri(to_poly(X), w))
        f = max(X[0])
        got = affine_core_dim(H, w, f + 2)
        if want is None:
            if got < f + 4:                     # K[P]_{<= f+2} + K Q + H has at least f + 4 elements
                return False
        elif got != want:
            return False
    return True


def identities():
    return {'G1': grid_G1(), 'G2': grid_G2(), 'G3': grid_G3(), 'W': grid_W(), 'K4': grid_K4(), 'A': grid_A()}


def check(cert=None):
    if cert is not None and cert.get('format') != FORMAT:
        raise ValueError('not a cubic-phase-v1 certificate')
    res = identities()
    bad = [k for k, v in res.items() if not v]
    if bad:
        raise ValueError(f'identities fail: {bad}')
    if cert is not None and cert.get('identities') != sorted(res):
        raise ValueError('certificate lists other identities')
    return {'status': 'passed', 'identities': sorted(res),
            'theorem': 'cubic-phase gauge form; affine-sector criterion with the Witt cocycle; Lemma W; family K4; Theorem A instances'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
