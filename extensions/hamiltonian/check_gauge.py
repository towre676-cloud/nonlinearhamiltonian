#!/usr/bin/env python3
"""Gauge form of the triangular gates for every shear (gauge-shear-v1).
See DYNAMIC_CORE_RESULTS.md section 6.10.

Notation as in check_triangular.py: tau(q, p) = (q, p + w(q)), Q = q, P = p + w(q), and M^tau_t(h, g)
= sum_k t^k/k! T_k(h~, g~) o tau^-1, M^flat_t(h, g) = sum_a t^a/a! T^flat_a(h, g) in (Q, P).

Theorem GG (gauge form, every w). With
    S_t = exp( sum_{n>=1} t^(2n) w^(2n)(Q) d_P^(2n+1) / (2n+1)! )
(a P-differential operator whose coefficients depend on Q),
    M^tau_t = S_t o M^flat_t o (S_t^-1 x S_t^-1).
Proof: conjugation by exp(i U(q^)/hbar), U' = w, multiplies the Weyl kernel K(x, y) by
exp(i (U(x) - U(y))/hbar). Expanding about the midpoint, the linear term is the shift p -> p + w(q) and
the odd higher terms give S_t. Conjugation is an algebra automorphism, so the pulled-back product
is the gauge transform of the flat one.                                           [GG: grid against Theorem X]
S_t has constant coefficients exactly when deg w <= 2 (Theorem G), and S_t fixes every function of
P-degree <= 2.

Third-gate formula (order t^3):
    T_3(h~, g~) o tau^-1 = T^flat_3(h, g) + w'' Delta(h, g) + w''' Lambda(h, g),
    Delta(h, g) = d^3{h, g} - {d^3 h, g} - {h, d^3 g},   Lambda(h, g) = h_P g_PPP - h_PPP g_P,  d = d_P.
The w'' Delta term is the coboundary part (removable when w'' is constant); w''' Lambda is the
genuine remainder.                                                                [T3: grid]

Theorem AE (higher shears, affine sector). If deg w >= 3, h = a(P) + Q b(P) with deg a >= 3 and
deg b < deg a, then D_inf(H~) restricted to pullbacks of V = K[P] + Q K[P] is span{1, H~}.
Proof (only T_3, at depth <= 2): for g = alpha + Q beta both terms are affine in Q, so
T^flat_3 = 0 and T_3 = omega (Delta_f + Q Delta_W) + omega' (L0 + Q L1 + Q^2 L2), omega = w'',
L0 = a' alpha''' - a''' alpha', L1 = a' beta''' + b' alpha''' - a''' beta' - b''' alpha', L2 = Delta_W/3.
The coefficient of the top power of Q gives Delta_W = 0; the next ones give Delta_f + m L1 = 0
(m = deg omega) and, centring Q at the root of omega when omega is a perfect power and otherwise
also L1 = 0, L0 = 0. L0 = 0 forces alpha = lambda a + const (a Wronskian argument, deg a' >= 2);
after subtracting lambda h, the remaining equations force beta constant, and {H, Q} = -a' - Q b'
leaves the span.                                                                  [AE: instances]

Lemma C (Q-degree containment, b constant). If h = a(P) + lambda Q with deg a >= 3 and deg w >= 2,
every element of D_inf(H~) has Q-degree <= 1 in (Q, P).
Proof: let g have Q-degree j >= 2 and top coefficient gamma(P). In T_3 the flat part lowers the
Q-degree by at least 2. With omega = w'' of degree m >= 0, the coefficient of Q^(j+m-1) reads
    m a' gamma''' - 3j a'' gamma'' - (3j + m) a''' gamma' = 0    (times the leading coefficient of omega).
For m = 0 this is (a'' gamma')' = 0, so gamma is constant. For m >= 1 the polynomial solutions
are gamma' = a'^(1 + 3j/m). Either way {H, g} has Q-degree j - 1 >= 1 and top coefficient
-j a' gamma (+ lambda gamma' Q^j, which for m >= 1 must itself satisfy the equation, forcing
lambda = 0), whose derivative is too large to solve the equation at level j - 1. So the top
vanishes.

Lemma C2 (containment for other b). Let G_j be the space of Q^j-coefficients of core elements of
Q-degree <= j. It is invariant under L_j: gamma -> b gamma' - j b' gamma (the Q-degree-preserving part
of D), and by T_3 it lies in the polynomial solutions of
    (3 + m) b' gamma''' + 3(1 - j) b'' gamma'' - (3j + m) b''' gamma' = 0.
 - b quadratic (vertex form b = mu (u^2 - delta), u = P - p0): solutions span{1, u, u^(j+1)}; L_j u^(j+1)
   has leading coefficient (1 - j) mu != 0 for j >= 2, and L_j 1 = -2 j mu u, L_j u = mu((1 - 2j) u^2 - delta),
   so G_j = 0 (the m >= 1 case is the same with u^(3(j-1)/(3+m) + 2)).
 - deg b = n >= 3: polynomial solutions are at most one-dimensional, gamma' = b'^k with
   k = (3j + m)/(3 + m) (the other indicial root at infinity is 2 - n < 0); L_j raises the degree of
   int b'^k because (n - 1) k + 1 - j n != 0 for j >= 2, and L_j 1 = -j b'. So G_j = 0.
 - b linear, cubic phase, deg a = f >= 4: tops are u^k, k <= 2, eigenvectors of L_j; the ladder
   (D - mu(k - j)) g excludes k = 0, 2; for k = 1 the Q^(j-2) equation requires
   e^{sX}[(e^{-sX} a')(e^{-sX} gamma_1)] - a' gamma_1 (X = d_P^3, gamma_1 = (j/mu) a + quadratic) to be
   linear in s, but its s^2 coefficient has leading term (j/mu) a_f^2 9 f^2 (f-3)(f-2)(f-1)^2 (2f-5)
   P^(2f-7).                                                                       [C2: instances, identity]
Hence every core element is affine in Q, except possibly for b linear with f = 3 (cubic phase) or
b linear (higher shears).

Theorem NA (non-affine binomial edges). Let deg w = e >= 2 and let the normal form h have P-degree s >= 3
(or s = 2 with d >= 3 below).
Suppose the first Newton edge of h from the vertex P^s (Q-exponent i, P-exponent j; slope
alpha = min (s - j)/i over monomials with i >= 1) contains exactly one other monomial, c Q^d with d >= 2,
and alpha = s/d > 1/2 (e = 2) or alpha > 1/e (e >= 3). Then D_inf(H~) = span{1, H~}.
Proof: give Q weight alpha and P weight 1. By Theorem X the odd gates are sums of products of A
(weight -(alpha + 1) per factor of t) and the corrections; the corrections win exactly when
alpha > 1/2 (e = 2), respectively alpha e > 1, so the top of T_3 is w''Delta + w'''Lambda with w = Q^e, and
the top of H is E = P^s + c Q^d. The Q^d part contributes nothing, and on monomials
    C3^top(Q^i P^j) = e(e-1)s j(j + s - 3)[(e-2)(j - s) - 3(s-1) i] Q^(i+e-3) P^(j+s-4)
(for e = 2: -6 s (s-1) i j (j + s - 3) Q^(i-1) P^(j+s-4)). The kernel is spanned by monomials: K[P] + K[Q]
for e = 2; K[Q], P^s and Q^i P^(s + 3(s-1)i/(e-2)) for e >= 3. Then {E, Q^i P^j} = d j Q^(i+d-1) P^(j-1)
- s i Q^(i-1) P^(j+s-1). Monomials of the third kind, and all others except 1 and E, produce images
outside the kernel that nothing else can cancel. So the top core is span{1, E}, and the top-weight
lemma gives dim D_inf(H~) <= 2. For s = 2 (d >= 3) the kernel also contains Q^i P; its images
d Q^(i+d-1) - 2i Q^(i-1) P^2 leave the kernel for i >= 2, and the remaining chains
(P -> Q^(d-1), Q -> P, Q^2 -> QP -> d Q^d - 2P^2) are followed to the end.        [NA: formula, instances]

Theorem NE (general first edges). Let s >= 3, let the first edge E of h from P^s have slope alpha above
the threshold (alpha > 1/2 for e = 2, alpha e > 1 for e >= 3) and kappa = s - 1 - alpha > 0, and for e = 2 let E
contain a monomial of Q-exponent >= 2. Then D_inf(H~) = span{1, H~}.
Proof. (1) Top gates in closed form. On the diagonal B^m(a (x) b) = d^m(a^(m) b^(m)) and
(d2 - d1) B^m(a (x) b) = d^m(a^(m) b^(m+1) - a^(m+1) b^(m)) (d = d_P). Hence the top gates vanish on g
iff for every m >= 1
    e = 2:  {E^(m), g^(m)} has P-degree < m;
    e >= 3: 3Q {E^(m), g^(m)} + m(e-2)(E^(m) g^(m+1) - E^(m+1) g^(m)) has P-degree < m.
(2) Finiteness. The normal form has no P^(s-1) term, so E^(s-1) = s! c0 P. At m = s - 1 this bounds the
Q-dependent monomials of a top-core element by P-degree 2s - 3 (e = 2), respectively excludes every
monomial of P-degree >= 2s - 2 except along one ray, which D then excludes (e >= 3). Tracking the
P-top of D g and D^2 g (it is -s i Q^(i-1) P^(j+s-1), uncancelled) kills all weights >= 3s - 2 (e = 2;
here a monomial of Q-exponent >= 2 in E removes the pure P-part), respectively > 2s - 3 (e >= 3).
(3) The top core V is finite-dimensional and D raises the weight by kappa > 0, so D is nilpotent on V.
ker D is the Poisson centralizer K[G] of E (E = c G^k); the m = 1 condition on G^m gives
(k - m) k m G^(k+m-3) G_P {G, G_P} (e = 2), respectively (k - m) k m G^(k+m-3) G_P [3Q{G, G_P} - (e-2) G_P^2],
of positive P-degree for m not in {0, k}. A longer chain would need g of weight alpha + 1 with
{E, g} = lambda E, lambda != 0: the eigen-equations force alpha in Z and E = P^m (P^alpha + k Q)^a, g = P (P^alpha + k Q)
(excluded by the m = 1 condition), or alpha = 1 with g quadratic (excluded by the Q^0 part of the m = 1
condition, since E has no Q P^(s-1) term). So V = span{1, E}.                [TG, GE: identities, instances]

Theorem NB (boundary edge). If s = 2 and h = c0 P^2 + c Q^(2e) + lower with deg w = e >= 2 (slope 1/e), then
D_inf(H~) = span{1, H~}. At this slope all terms of Theorem X are top: the top problem is the flat core of
F = (p + q^e)^2 + c q^(2e). T_3 is the first-order equation [2(e-2)p + 4g(2e-1)q^e] u_p = 6 q u_q for u = g_pp
(g = 1 + c), so u = q^a L^nu with L = 2p + 2g q^e, nu = 3(W - 2e)/(4e - 2), a = nu(e - 2)/3. T_5 then needs
(nu - 2)(e - 4) = 5a and (nu - 2) K(e) = 0 with K(e) = (2e)_5 - 2(e)_5 - 10 e (e)_4 = 20 e^2 (e-1)^2 (e-2), leaving
nu in {0, 1} for e >= 3; closure under D removes everything except 1 and F. For e = 2 every nu passes
(L is a quadratic-shear coordinate); D removes all weights >= 6, and weights <= 7 are solved exactly
(maximal minors vanish only at c = 0).                                       [BE: identity, instances]

Corollary K1c. (i) deg w = 2, H = F(P) + lambda Q, deg F >= 3: D_inf(H~) = K[P] + K Q exactly.
(ii) deg w >= 3, H = F(P) + lambda Q, deg F >= 3: D_inf(H~) = span{1, H~}.     [K1c: instances]

Usage: check_gauge.py [CERT.json]
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
import check_triangular as CT        # noqa: E402
import check_cubic_phase as CP       # noqa: E402
import qlinalg as L                  # noqa: E402

FORMAT = 'gauge-shear-v1'


def S_series(f, w, sign, kmax):
    """coefficients of t^m, m <= kmax, in S_t^sign f."""
    def X(n, g):
        c = CT.U(CT.uderiv(w, 2 * n))
        return TR.sc(TR.mul(c, W.pder(g, 0, 2 * n + 1)), F(sign, factorial(2 * n + 1))) if c else {}
    E = [dict(f)]
    for m in range(1, kmax + 1):
        acc = {}
        for j in range(2, m + 1, 2):
            acc = TR.add(acc, TR.sc(X(j // 2, E[m - j]), F(j)))
        E.append(TR.sc(acc, F(1, m)))
    return E


def gauge_T(h, g, w, k):
    """k! [t^k] S_t M^flat_t(S_t^-1 h, S_t^-1 g)."""
    Hs, Gs = S_series(h, w, -1, k), S_series(g, w, -1, k)
    out = {}
    for m in range(k + 1):
        acc = {}
        for a in range(m + 1):
            for i in range(m - a + 1):
                x, y = Hs[i], Gs[m - a - i]
                if x and y:
                    acc = TR.add(acc, TR.sc(CP.flat(x, y, a), F(1, factorial(a))))
        out = TR.add(out, S_series(acc, w, 1, k - m)[k - m])
    return TR.sc(out, F(factorial(k)))


def grid_GG(n=14, seed=1):
    rng = random.Random(seed)
    for _ in range(n):
        w = {e: F(rng.randint(-2, 2)) for e in range(rng.randint(3, 6) + 1)}
        h, g = CT.rand_poly(rng, rng.randint(1, 4)), CT.rand_poly(rng, rng.randint(1, 4))
        E = CT.tau_series(w, 7)
        for k in range(1, 8):
            if gauge_T(h, g, w, k) != CT.tau_T(h, g, w, k, E):
                return False
    return True


def third(h, g, w):
    br = lambda f, u: W.act(W.derivation(f), u)
    d3 = lambda f: W.pder(f, 0, 3)
    om, om1 = CT.U(CT.uderiv(w, 2)), CT.U(CT.uderiv(w, 3))
    delta = TR.add(d3(br(h, g)), TR.sc(br(d3(h), g), -1), TR.sc(br(h, d3(g)), -1))
    lam = TR.add(TR.mul(W.pder(h, 0, 1), W.pder(g, 0, 3)), TR.sc(TR.mul(W.pder(h, 0, 3), W.pder(g, 0, 1)), -1))
    return TR.add(W.act(W.gate(h, 3), g), TR.mul(om, delta), TR.mul(om1, lam))


def grid_T3(n=30, seed=5):
    rng = random.Random(seed)
    for _ in range(n):
        w = {e: F(rng.randint(-2, 2)) for e in range(rng.randint(2, 6) + 1)}
        h, g = CT.rand_poly(rng, rng.randint(1, 5)), CT.rand_poly(rng, rng.randint(1, 5))
        if third(h, g, w) != CT.tau_T(h, g, w, 3):
            return False
    return True


def grid_AE(n=8, seed=8):
    rng = random.Random(seed)
    for _ in range(n):
        e, f = rng.choice([3, 4]), rng.choice([3, 4])
        a = {f: F(1), **{i: F(rng.randint(-2, 2)) for i in range(f - 1)}}
        b = {i: F(rng.randint(-2, 2)) for i in range(rng.randint(0, f - 1))}
        w = {e: F(1), **{i: F(rng.randint(-1, 1)) for i in range(e)}}
        H = TR.tidy(CT.tri(CP.to_poly((a, b)), w))
        if CP.affine_core_dim(H, w, f + 2) != 2:
            return False
    return True


def full_dim(H, N, R=8):
    D, gates = W.derivation(H), W.gates(H)
    mons = [(i, s - i) for s in range(N + 1) for i in range(s + 1)]
    cols = []
    for m in mons:
        g, img = {m: F(1)}, {}
        for r in range(R + 1):
            for k, Ck in gates.items():
                for e, v in W.act(Ck, g).items():
                    img[(r, k, e)] = v
            g = W.act(D, g)
        cols.append(img)
    keys = sorted({k for c in cols for k in c})
    M = [[c.get(k, F(0)) for c in cols] for k in keys]
    return len(mons) - L.rank(M, len(mons))


def grid_K1c():
    """(i) deg w = 2: dim in degrees <= N is 2 + #{n >= 1: 2n <= N}; (ii) deg w >= 3: span{1, H}."""
    cases = [({(0, 3): F(1), (1, 0): F(1)}, {2: F(1)}, 8), ({(0, 3): F(1), (0, 1): F(-2)}, {2: F(1), 1: F(1)}, 8),
             ({(0, 3): F(1), (1, 0): F(1)}, {3: F(1)}, 10), ({(0, 3): F(1), (0, 1): F(1)}, {3: F(1), 1: F(-1)}, 10)]
    for h, w, N in cases:
        H = TR.tidy(CT.tri(h, w))
        want = 2 + N // 2 if max(w) == 2 else 1 + (N >= TR.degree(H))
        if full_dim(H, N) != want:
            return False
    return True


def s2_lead(f):
    """leading coefficient of the s^2 term of e^{sX}[(e^{-sX} a')(e^{-sX} a)] - a' a for a = P^f."""
    a = {(0, f): F(1)}
    A1 = W.pder(a, 0, 1)
    X = lambda u, n=1: W.pder(u, 0, 3 * n)
    c2 = TR.sc(TR.add(X(TR.mul(A1, a), 2), TR.sc(X(TR.add(TR.mul(X(A1), a), TR.mul(A1, X(a)))), -2),
                      TR.mul(X(A1, 2), a), TR.sc(TR.mul(X(A1), X(a)), 2), TR.mul(A1, X(a, 2))), F(1, 2))
    return c2.get((0, 2 * f - 7), F(0))


def grid_C2():
    # identity in f: the leading coefficient is a polynomial in f of degree <= 8; 13 values determine it
    for f in range(4, 17):
        if s2_lead(f) != 9 * f * f * (f - 3) * (f - 2) * (f - 1) ** 2 * (2 * f - 5):
            return False
    # full cores (no affine restriction) for b quadratic and deg b >= 3, cubic and higher shears
    w2, w3 = {2: F(1)}, {3: F(1)}
    cases = [(({4: F(1), 1: F(-1)}, {2: F(1), 1: F(2), 0: F(-3)}), w2, 8, 3),    # K4: 1, G, H
             (({4: F(1)}, {2: F(1), 0: F(-1)}), w2, 8, 2),                          # quadratic b, not K4
             (({5: F(1), 1: F(1)}, {3: F(1)}), w2, 10, 2),                          # deg b = 3
             (({4: F(1), 1: F(1)}, {1: F(1), 0: F(1)}), w2, 8, 4),                  # K1', f = 4: 1, P, P^2, H
             (({3: F(1)}, {2: F(1), 0: F(1)}), w3, 9, 2)]                           # higher shear, quadratic b
    for X, w, N, want in cases:
        H = TR.tidy(CT.tri(CP.to_poly(X), w))
        if full_dim(H, N) != want:
            return False
    return True


def c3top(E, g, e):
    """top part of T_3 for the monomial shear w = Q^e (e >= 2): w'' Delta + w''' Lambda."""
    br = lambda f, u: W.act(W.derivation(f), u)
    d3 = lambda u: W.pder(u, 0, 3)
    om = {(e - 2, 0): F(e * (e - 1))}
    om1 = {(e - 3, 0): F(e * (e - 1) * (e - 2))} if e >= 3 else {}
    delta = TR.add(d3(br(E, g)), TR.sc(br(d3(E), g), -1), TR.sc(br(E, d3(g)), -1))
    lam = TR.add(TR.mul(W.pder(E, 0, 1), W.pder(g, 0, 3)), TR.sc(TR.mul(W.pder(E, 0, 3), W.pder(g, 0, 1)), -1))
    return TR.add(TR.mul(om, delta), TR.mul(om1, lam))


def grid_NA():
    for e in (2, 3, 4, 5):
        for s_ in (2, 3, 4, 5):
            for d in (2, 3, 4):
                E = {(0, s_): F(1), (d, 0): F(1)}
                for i in range(5):
                    for j in range(7):
                        got = c3top(E, {(i, j): F(1)}, e)
                        coef = e * (e - 1) * s_ * j * (j + s_ - 3) * ((e - 2) * (j - s_) - 3 * (s_ - 1) * i)
                        want = {(i + e - 3, j + s_ - 4): F(coef)} if coef else {}
                        if got != want:
                            return False
    cases = [({(0, 3): F(1), (2, 0): F(1)}, {2: F(1)}, 7), ({(0, 4): F(1), (3, 0): F(1), (0, 1): F(1)}, {2: F(1)}, 8),
             ({(0, 3): F(1), (2, 0): F(1)}, {3: F(1)}, 9),
             ({(0, 2): F(1), (3, 0): F(1)}, {2: F(1)}, 6), ({(0, 2): F(1), (4, 0): F(1)}, {3: F(1)}, 7)]
    for h, w, N in cases:
        H = TR.tidy(CT.tri(h, w))
        if full_dim(H, N) != 1 + (N >= TR.degree(H)):
            return False
    return True


def dP(u, n=1):
    return W.pder(u, 0, n) if n else u


def pb(f, g):
    return W.act(W.derivation(f), g)


def B_pow(a, b, m, twist=False):
    """[(d2 - d1)?] B^m (a (x) b) on the diagonal, from the expansion B^m = sum_i C(m,i) d1^(m+i) d2^(2m-i)."""
    out = {}
    for i in range(m + 1):
        c = F(comb(m, i))
        x, y = dP(a, m + i), dP(b, 2 * m - i)
        if not twist:
            out = TR.add(out, TR.sc(TR.mul(x, y), c))
        else:
            out = TR.add(out, TR.sc(TR.mul(x, dP(y)), c), TR.sc(TR.mul(dP(x), y), -c))
    return out


def grid_TG(seed=29):
    rng = random.Random(seed)
    for _ in range(12):
        a, b = CT.rand_poly(rng, rng.randint(2, 7)), CT.rand_poly(rng, rng.randint(2, 7))
        for m in (1, 2, 3):
            if B_pow(a, b, m) != dP(TR.mul(dP(a, m), dP(b, m)), m):
                return False
            if B_pow(a, b, m, True) != dP(TR.add(TR.mul(dP(a, m), dP(b, m + 1)), TR.sc(TR.mul(dP(a, m + 1), dP(b, m)), -1)), m):
                return False
            # cubic-phase top gate A B^m (E (x) g) = d^m {E^(m), g^(m)}
            lhs = TR.add(B_pow(W.pder(a, 1, 0), dP(b), m), TR.sc(B_pow(dP(a), W.pder(b, 1, 0), m), -1))
            if lhs != dP(pb(dP(a, m), dP(b, m)), m):
                return False
    return True


def grid_GE():
    cases = [({(0, 3): F(1), (2, 1): F(1)}, {2: F(1)}, 7),                  # cubic, edge P^3 + Q^2 P
             ({(0, 4): F(1), (1, 2): F(1), (2, 0): F(1)}, {2: F(1)}, 8),    # cubic, edge P^4 + Q P^2 + Q^2
             ({(0, 3): F(1), (2, 1): F(1), (2, 0): F(1)}, {3: F(1)}, 9)]    # e = 3, edge P^3 + Q^2 P
    for h, w, N in cases:
        H = TR.tidy(CT.tri(h, w))
        if full_dim(H, N) != 1 + (N >= TR.degree(H)):
            return False
    return True


def ff_(x, k):
    out = 1
    for i in range(k):
        out *= (x - i)
    return out


def flat_core_dims(Fh, e, Wmax, R=5):
    D, gates = W.derivation(Fh), {k: W.gate(Fh, k) for k in (3, 5, 7, 9)}
    out = []
    for Wt in range(Wmax + 1):
        mons = [(Wt - e * j, j) for j in range(Wt // e + 1)]
        cols = []
        for mm in mons:
            g, img = {mm: F(1)}, {}
            for r in range(R + 1):
                for k, C in gates.items():
                    for ee, v in W.act(C, g).items():
                        img[(r, k, ee)] = v
                g = W.act(D, g)
            cols.append(img)
        keys = sorted({k for c in cols for k in c})
        M = [[c.get(k, F(0)) for c in cols] for k in keys]
        dm = len(mons) - (L.rank(M, len(mons)) if M else 0)
        if dm:
            out.append((Wt, dm))
    return out


def grid_BE():
    # K(e) is a polynomial of degree 5 in e: 9 values determine it
    for e in range(2, 11):
        if ff_(2 * e, 5) - 2 * ff_(e, 5) - 10 * e * ff_(e, 4) != 20 * e * e * (e - 1) ** 2 * (e - 2):
            return False
    for e, c, Wmax in [(2, F(1), 9), (2, F(-3), 9), (2, F(1, 2), 9), (3, F(1), 14), (4, F(-2), 18)]:
        Fh = TR.tidy({(0, 2): F(1), (e, 1): F(2), (2 * e, 0): 1 + c})
        if flat_core_dims(Fh, e, Wmax) != [(0, 1), (2 * e, 1)]:
            return False
    return True


def identities():
    return {'GG': grid_GG(), 'T3': grid_T3(), 'AE': grid_AE(), 'K1c': grid_K1c(), 'C2': grid_C2(),
            'NA': grid_NA(), 'TG': grid_TG(), 'GE': grid_GE(), 'BE': grid_BE()}


def check(cert=None):
    if cert is not None and cert.get('format') != FORMAT:
        raise ValueError('not a gauge-shear-v1 certificate')
    res = identities()
    bad = [k for k, v in res.items() if not v]
    if bad:
        raise ValueError(f'identities fail: {bad}')
    if cert is not None and cert.get('identities') != sorted(res):
        raise ValueError('certificate lists other identities')
    return {'status': 'passed', 'identities': sorted(res),
            'theorem': 'gauge form for every shear; third-gate formula; higher-shear affine rigidity; '
                       'Q-degree containment (b constant, quadratic, degree >= 3; b linear with f >= 4 in the '
                       'cubic phase); K1, K1\' (f >= 4) and K4 exact; '
                       'non-affine binomial edges collapse (Theorem NA), general first edges (NE) and the boundary edge (NB)'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
