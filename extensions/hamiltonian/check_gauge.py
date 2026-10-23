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

Theorem NT (threshold edges, e >= 3). If s >= 3, deg w = e >= 3 and the first edge E of h from P^s has slope exactly
1/e, then D_inf(H~) = span{1, H~}. With weights (1, e) the top problem is the flat core of the weighted binary form
F = E(p + w_e q^e, q^e) = sum_k c_k q^(ek) p^(s-k), and c1 = s w_e c0 != 0 (normal form). For weight-homogeneous
g = sum_j x_j q^(i+ej) p^(N-j) the leading output of T_3 is -(s)_3 (i)_3 x0, so i <= 2, and once x0 = 0 the next
term (q-exponent >= e >= 3) dies as well; it suffices that x0 = 0 unless (i, N) in {(0, 0), (0, s)}. At the next
p-degree T3 g, T3 D g, T3 D^2 g, T5 g are linear in (x1, c1 x0) with closed-form rows (nt_rows); their 2x2 minors
(i = 0: a multiple of N(s - N)(N + s - 3)(b-3); i = 1: (N-1)(N+s-1)(N+2s-4) and N(N+s-3)((2-b)N+bs+s-3); i = 2:
two cubics with resultant 4(b-3)(b+1)(s-2)(s-1)^3 B(b, s), B(4+x, 3+y) > 0 coefficientwise) leave no N for b >= 4.
For e = 3 types 1, 2 close at step 1 and type 0 at step 2: after x1 = lambda x0, the T3 D g / T3 D^2 g pair removes
x2 and c2 together, leaving N(s-N)(N+s-3)(3N^2 + 6(s-3)N - 10(s-2)) x0 = 0.          [NT: rows, minors, resultant, instances]

Theorem NV (vertex-adjacent rigidity). Let F be weight-homogeneous with vertex p^s (s >= 3) and vertex-adjacent
monomial c q^B p^(s-K), c != 0, B >= 4, K >= 1 (every other monomial of lower p-degree). Then the flat core of F is
span{1, F}. At output level K only p^s (x) x1 q^(i+B) p^(N-K) and c q^B p^(s-K) (x) x0 q^i p^N contribute, so each of
T3 D^r g gives a row in (x1, c x0) (nv_rows); the minors are K-free: i = 0, (T3g, T3Dg): N(s-N)(N+s-3)(B-3)...;
i = 1, (T3Dg, T3D^2g): (N-1)(N+s-1)(N+2s-4)(B-3)..., and at N = 1 (T3g, T3D^2g): (B+K)(s-1)(s-2)...;
i = 2, (T3D^2g, T3D^3g): (N+s-2)(N+2s-2)(N+3s-5)(B-3).... So x0 = 0 unless (i, N) in {(0, 0), (0, s)}; the next
term either dies (q-exponent >= 3) or is again of type 1 or 2. Consequences (top-weight lemma): every first edge
below the slope threshold (there K >= 2 by the normal form, so B > eK >= 4) and, for deg w <= 1, every first edge
with B >= 4 gives D_inf(H~) = span{1, H~}. With K = 1 this re-proves NT for e >= 4.        [NV: rows, minors, instances]
Case B = 3, K = 2 (the only other flat-lower-terms case: a pure top forces slope K/B < 1, the normal form K >= 2):
F = p^s + q^3 p^(s-2) + c q^6 p^(s-4) + ..., lattice step (3, 2). Types 1, 2 close at level 2 (minors with factors
f1, f2 of fixed sign); type 0 at level 4 by the T3 D g / T3 D^2 g eliminant, free of c, with factor f0
(negative at N = 1, positive for N >= 2). So every flat-lower-terms pure top (deg w <= 1, s >= 3) collapses.
                                                                                  [NV32: rows, eliminants, signs, instances]

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


class Pz:
    """Integer polynomials in (N, b, s, K), exponent 4-tuples -> int; enough algebra for exact identities."""
    def __init__(self, d=None):
        self.d = {k: v for k, v in (d or {}).items() if v}

    @staticmethod
    def of(x):
        return x if isinstance(x, Pz) else Pz({(0, 0, 0, 0): x})

    def __add__(self, o):
        o, d = Pz.of(o), dict(self.d)
        for k, v in o.d.items():
            d[k] = d.get(k, 0) + v
        return Pz(d)
    __radd__ = __add__

    def __neg__(self):
        return Pz({k: -v for k, v in self.d.items()})

    def __sub__(self, o):
        return self + (-Pz.of(o))

    def __rsub__(self, o):
        return Pz.of(o) - self

    def __mul__(self, o):
        o, d = Pz.of(o), {}
        for k, v in self.d.items():
            for l, w in o.d.items():
                m = tuple(u + v for u, v in zip(k, l))
                d[m] = d.get(m, 0) + v * w
        return Pz(d)
    __rmul__ = __mul__

    def __pow__(self, n):
        out = Pz.of(1)
        for _ in range(n):
            out = out * self
        return out

    def __eq__(self, o):
        return self.d == Pz.of(o).d

    def deg(self, i):
        return max((k[i] for k in self.d), default=0)

    def coeffs_in(self, i):
        """coefficients of powers of variable i, as polynomials in the others."""
        out = {}
        for k, v in self.d.items():
            kk = list(k)
            e, kk[i] = kk[i], 0
            out.setdefault(e, {})[tuple(kk)] = v
        return {e: Pz(d) for e, d in out.items()}

    def at(self, N=0, b=0, s=0, K=0):
        return sum(v * N ** k[0] * b ** k[1] * s ** k[2] * K ** k[3] for k, v in self.d.items())


ZN, ZB, ZS, ZK = (Pz({tuple(int(i == j) for j in range(4)): 1}) for i in range(4))


def nt_rows(i, N, b, s):
    """Step-1 top-end rows (coefficient of x1, coefficient of c1 x0) of T3 g, T3 D g, T3 D^2 g, T5 g for the flat
    form F = p^s + c1 q^b p^(s-1) + ... and g = x0 q^i p^N + x1 q^(i+b) p^(N-1) + ... (closed forms, Theorem NT)."""
    k = b * (s - 2) * (s - 1)
    if i == 0:
        return {'T3g': (-s * k * (b - 2) * (b - 1), N * b * (N - 2) * (N - 1) * (b - 2) * (b - 1)),
                'T3Dg': (s ** 2 * k * (b - 3) * (b - 2) * (b - 1), -N * s * k * (b - 3) * (b - 2) * (b - 1)),
                'T3DDg': (-s ** 3 * k * (b - 4) * (b - 3) * (b - 2) * (b - 1), N * s ** 2 * k * (b - 4) * (b - 3) * (b - 2) * (b - 1)),
                'T5g': (-s * k * (b - 4) * (b - 3) * (b - 2) * (b - 1) * (s - 4) * (s - 3),
                        N * b * (N - 4) * (N - 3) * (N - 2) * (N - 1) * (b - 4) * (b - 3) * (b - 2) * (b - 1))}
    if i == 1:
        return {'T3g': (-s * k * (b - 1) * (b + 1), -N * b * (N - 1) * (b - 1) * (-N * b + 2 * N + 2 * b + 3 * s - 7)),
                'T3Dg': (s ** 2 * k * (b - 2) * (b - 1) * (b + 1),
                         -b * s * (b - 2) * (b - 1) * (N ** 3 + 3 * N ** 2 * s - 6 * N ** 2 + N * b * s ** 2 - 3 * N * b * s + 2 * N * b
                                                       + 3 * N * s ** 2 - 12 * N * s + 11 * N - 2 * s ** 2 + 6 * s - 4)),
                'T3DDg': (-s ** 3 * k * (b - 3) * (b - 2) * (b - 1) * (b + 1), N * s ** 2 * k * (b - 3) * (b - 2) * (b - 1) * (b + 1)),
                'T5g': (-s * k * (b - 3) * (b - 2) * (b - 1) * (b + 1) * (s - 4) * (s - 3),
                        -N * b * (N - 3) * (N - 2) * (N - 1) * (b - 3) * (b - 2) * (b - 1) * (-N * b + 4 * N + 4 * b + 5 * s - 21))}
    return {'T3g': (-s * k * (b + 1) * (b + 2),
                    N * b * (N ** 2 * b ** 2 - 3 * N ** 2 * b + 2 * N ** 2 - 3 * N * b ** 2 - 6 * N * b * s + 15 * N * b + 6 * N * s
                             - 12 * N + 2 * b ** 2 + 6 * b * s - 12 * b + 6 * s ** 2 - 24 * s + 22)),
            'T3Dg': (s ** 2 * k * (b - 1) * (b + 1) * (b + 2),
                     b * s * (b - 1) * (-2 * N ** 3 * b + 4 * N ** 3 - 6 * N ** 2 * b * s + 12 * N ** 2 * b + 18 * N ** 2 * s - 30 * N ** 2
                                        - N * b ** 2 * s ** 2 + 3 * N * b ** 2 * s - 2 * N * b ** 2 - 7 * N * b * s ** 2 + 27 * N * b * s
                                        - 24 * N * b + 24 * N * s ** 2 - 78 * N * s + 62 * N + 4 * b * s ** 2 - 12 * b * s + 8 * b
                                        + 12 * s ** 3 - 56 * s ** 2 + 84 * s - 40)),
            'T3DDg': (-s ** 3 * k * (b - 2) * (b - 1) * (b + 1) * (b + 2),
                      b * s ** 2 * (b - 2) * (b - 1) * (2 * N ** 3 + 12 * N ** 2 * s - 18 * N ** 2 + N * b ** 2 * s ** 2 - 3 * N * b ** 2 * s
                                                        + 2 * N * b ** 2 + 3 * N * b * s ** 2 - 9 * N * b * s + 6 * N * b + 24 * N * s ** 2
                                                        - 72 * N * s + 52 * N + 12 * s ** 3 - 56 * s ** 2 + 84 * s - 40)),
            'T5g': (-s * k * (b - 2) * (b - 1) * (b + 1) * (b + 2) * (s - 4) * (s - 3),
                    N * b * (N - 2) * (N - 1) * (b - 2) * (b - 1) * (N ** 2 * b ** 2 - 7 * N ** 2 * b + 12 * N ** 2 - 7 * N * b ** 2
                                                                     - 10 * N * b * s + 59 * N * b + 30 * N * s - 114 * N + 12 * b ** 2
                                                                     + 30 * b * s - 114 * b + 20 * s ** 2 - 150 * s + 274))}


def nt_direct(i, N, b, s):
    """the same rows computed with weyl_receipts on F = p^s + q^b p^(s-1) (c1 = 1) and single monomials of g."""
    Fh = {(0, s): F(1), (b, s - 1): F(1)}
    D, C3, C5 = W.derivation(Fh), W.gate(Fh, 3), W.gate(Fh, 5)
    wt = i + b * N
    ops = {'T3g': (lambda g: W.act(C3, g), s + N - 4, b * s - 3 * (b + 1)),
           'T3Dg': (lambda g: W.act(C3, W.act(D, g)), 2 * s + N - 5, 2 * b * s - 4 * (b + 1)),
           'T3DDg': (lambda g: W.act(C3, W.act(D, W.act(D, g))), 3 * s + N - 6, 3 * b * s - 5 * (b + 1)),
           'T5g': (lambda g: W.act(C5, g), s + N - 6, b * s - 5 * (b + 1))}
    out = {}
    for name, (op, pe, dw) in ops.items():
        mon = (wt + dw - b * pe, pe)
        out[name] = (op({(i + b, N - 1): F(1)}).get(mon, 0), op({(i, N): F(1)}).get(mon, 0))
    return out


def nt_rows30(N, s, c):
    """e = 3, top type 0: (x0, x1, x2) coefficients of the step-1 row of T3 g and the step-2 rows of T3 D g and
    T3 D^2 g, for F = p^s + q^3 p^(s-1) + c q^6 p^(s-2) and g = x0 p^N + x1 q^3 p^(N-1) + x2 q^6 p^(N-2)."""
    k = (s - 2) * (s - 1)
    return {'T3g1': (6 * N * (N - 2) * (N - 1), -6 * s * k, 0),
            'T3Dg2': (-18 * N * (-N ** 3 + 3 * N ** 2 * s + 3 * N ** 2 + 6 * N * s ** 2 - 15 * N * s - 2 * N + 20 * c * s ** 3
                                 - 60 * c * s ** 2 + 40 * c * s + 2 * s ** 3 - 12 * s ** 2 + 16 * s),
                      18 * s * (-N ** 3 + 3 * N ** 2 * s + 3 * N ** 2 - 4 * N * s ** 2 + 15 * N * s - 22 * N + 12 * s ** 3
                                - 42 * s ** 2 + 36 * s), 360 * s ** 2 * k),
            'T3DDg2': (36 * N * s * (-N ** 3 - 3 * N ** 2 * s + 9 * N ** 2 - 6 * N * s ** 2 + 33 * N * s - 38 * N + 20 * c * s ** 3
                                     - 60 * c * s ** 2 + 40 * c * s + 2 * s ** 3 + 8 * s ** 2 - 44 * s + 40),
                       -36 * s ** 2 * (-N ** 3 - 3 * N ** 2 * s + 9 * N ** 2 - 16 * N * s ** 2 + 63 * N * s - 58 * N + 12 * s ** 3
                                       - 22 * s ** 2 - 24 * s + 40), -720 * s ** 3 * k)}


def nt_direct2(N, s, c, b=3, i=0):
    """the rows of nt_rows30 from weyl_receipts."""
    Fh = TR.tidy({(0, s): F(1), (b, s - 1): F(1), (2 * b, s - 2): F(c)})
    D, C3 = W.derivation(Fh), W.gate(Fh, 3)
    wt = i + b * N
    ops = {'T3g1': (lambda g: W.act(C3, g), s + N - 4, b * s - 3 * (b + 1)),
           'T3Dg2': (lambda g: W.act(C3, W.act(D, g)), 2 * s + N - 6, 2 * b * s - 4 * (b + 1)),
           'T3DDg2': (lambda g: W.act(C3, W.act(D, W.act(D, g))), 3 * s + N - 7, 3 * b * s - 5 * (b + 1))}
    out = {}
    for name, (op, pe, dw) in ops.items():
        mon = (wt + dw - b * pe, pe)
        out[name] = tuple(op({(i + b * j, N - j): F(1)}).get(mon, 0) for j in range(3))
    return out


def minor(r, a, c):
    return r[a][0] * r[c][1] - r[a][1] * r[c][0]


def sylvester_det(f, g):
    """resultant of two polynomials given as coefficient lists (highest first), exact Fractions."""
    m, n = len(f) - 1, len(g) - 1
    M = [[F(0)] * (m + n) for _ in range(m + n)]
    for r in range(n):
        for j, x in enumerate(f):
            M[r][r + j] = F(x)
    for r in range(m):
        for j, x in enumerate(g):
            M[n + r][r + j] = F(x)
    det, M = F(1), [row[:] for row in M]
    for c in range(m + n):
        piv = next((r for r in range(c, m + n) if M[r][c]), None)
        if piv is None:
            return F(0)
        if piv != c:
            M[c], M[piv], det = M[piv], M[c], -det
        det *= M[c][c]
        for r in range(c + 1, m + n):
            if M[r][c]:
                t = M[r][c] / M[c][c]
                M[r] = [x - t * y for x, y in zip(M[r], M[c])]
    return det


def nt_big(b, s):
    return (6*b**7*s**3 - 23*b**7*s**2 + 26*b**7*s - 8*b**7 + 36*b**6*s**4 - 216*b**6*s**3 + 488*b**6*s**2 - 440*b**6*s
            + 116*b**6 - 36*b**5*s**4 + 480*b**5*s**3 - 1451*b**5*s**2 + 1388*b**5*s - 272*b**5 - 144*b**4*s**4
            - 228*b**4*s**3 + 1942*b**4*s**2 - 1804*b**4*s - 176*b**4 + 252*b**3*s**4 + 126*b**3*s**3 - 2104*b**3*s**2
            + 982*b**3*s + 1664*b**3 - 108*b**2*s**4 - 636*b**2*s**3 + 2392*b**2*s**2 + 20*b**2*s - 2900*b**2
            + 684*b*s**3 - 1824*b*s**2 - 228*b*s + 2280*b - 216*s**3 + 576*s**2 + 72*s - 720)


def grid_NT():
    N, b, s = ZN, ZB, ZS
    # (a) the closed-form rows agree with the gates; they have degree <= 6 in each variable, checked on a 7^3 box
    for i in (0, 1, 2):
        for bb in range(2, 11):
            for ss in range(3, 10):
                for NN in range(1, 8):
                    cf, dr = nt_rows(i, NN, bb, ss), nt_direct(i, NN, bb, ss)
                    if any(F(cf[k][0]) != dr[k][0] or F(cf[k][1]) != dr[k][1] for k in cf):
                        return False
    # (a') e = 3, top type 0, steps 1-2: degree <= 5 in N and s, linear in c
    for NN in range(2, 9):
        for ss in range(3, 10):
            for cc in (0, 1):
                cf, dr = nt_rows30(NN, ss, cc), nt_direct2(NN, ss, cc)
                if any(F(x) != y for k in cf for x, y in zip(cf[k], dr[k])):
                    return False
    # x1 = lambda x0 from T3g1 (lambda = N(N-1)(N-2)/(s(s-1)(s-2))); the T3 D g / T3 D^2 g pair then gives a
    # c-free equation for x0
    r3 = nt_rows30(N, s, ZB)            # c carried in the b-slot
    A = {k: s * (s - 1) * (s - 2) * r3[k][0] + N * (N - 1) * (N - 2) * r3[k][1] for k in ('T3Dg2', 'T3DDg2')}
    m30 = A['T3Dg2'] * r3['T3DDg2'][2] - A['T3DDg2'] * r3['T3Dg2'][2]
    if m30 != 25920 * N * s ** 4 * (s - N) * (s - 1) ** 2 * (s - 2) * (N + s - 3) * (3 * N ** 2 + 6 * N * s - 18 * N - 10 * s + 20):
        return False
    q1 = lambda N, s: 3 * N ** 2 + 3 * N * s - 9 * N - s + 2
    q2 = lambda N, s: 3 * N ** 2 + 9 * N * s - 15 * N + 6 * s ** 2 - 19 * s + 14
    q0 = lambda N, s: 3 * N ** 2 + 6 * N * s - 18 * N - 10 * s + 20
    if not (positive_shift(q1, 1, 3) and positive_shift(q2, 0, 3) and positive_shift(q0, 2, 3)):
        return False
    if q1(0, s) != 2 - s or q0(1, s) != 5 - 4 * s:
        return False
    # (b) the minors, exactly
    k0 = b ** 2 * (b - 2) * (b - 1) * (s - 2) * (s - 1)
    r0, r1, r2 = (nt_rows(i, N, b, s) for i in (0, 1, 2))
    if minor(r0, 'T3g', 'T3Dg') != k0 * N * s ** 2 * (s - N) * (b - 3) * (b - 2) * (b - 1) * (N + s - 3):
        return False
    if minor(r1, 'T3Dg', 'T3DDg') != -k0 * s ** 4 * (N - 1) * (b - 3) * (b - 2) * (b - 1) * (b + 1) * (N + s - 1) * (N + 2 * s - 4):
        return False
    if minor(r1, 'T3g', 'T3DDg') != -k0 * N * s ** 3 * (b - 3) * (b - 1) * (b + 1) * (N + s - 3) * (-N * b + 2 * N + b * s + s - 3):
        return False
    # e = 3, top types 1 and 2: step 1 suffices
    r31, r32 = nt_rows(1, N, 3, s), nt_rows(2, N, 3, s)
    if minor(r31, 'T3g', 'T3Dg') != 288 * s ** 2 * (s - 2) * (s - 1) ** 2 * (3 * N ** 2 + 3 * N * s - 9 * N - s + 2):
        return False
    if minor(r32, 'T3Dg', 'T3DDg') != 2880 * s ** 4 * (s - 2) * (s - 1) ** 2 * (3 * N ** 2 + 9 * N * s - 15 * N + 6 * s ** 2 - 19 * s + 14):
        return False
    f13 = (-N**3*b**2 + 3*N**3*b + 3*N**2*b**2 + 6*N**2*b*s - 15*N**2*b + 6*N**2*s - 6*N**2 + N*b**2*s**2 - 3*N*b**2*s
           + 3*N*b*s**2 - 15*N*b*s + 18*N*b + 18*N*s**2 - 48*N*s + 30*N + 12*s**3 - 56*s**2 + 84*s - 40)
    f23 = (-N**3*b + 3*N**3 - 3*N**2*b*s + 6*N**2*b + 15*N**2*s - 24*N**2 - 2*N*b*s**2 + 9*N*b*s - 9*N*b + 24*N*s**2
           - 75*N*s + 57*N + 2*b*s**2 - 6*b*s + 4*b + 12*s**3 - 56*s**2 + 84*s - 40)
    k2 = b ** 2 * (b - 2) * (b - 1) * (b + 1) * (b + 2) * (s - 2) * (s - 1)
    if minor(r2, 'T3g', 'T3DDg') != -k2 * s ** 3 * f13 or minor(r2, 'T3Dg', 'T3DDg') != 2 * k2 * s ** 4 * (b - 1) * f23:
        return False
    # (c) Res_N(f13, f23) = 4 (b-3)(b+1)(s-2)(s-1)^3 big(b, s): degree <= 12 in b and <= 18 in s, checked on that box
    c13, c23 = f13.coeffs_in(0), f23.coeffs_in(0)
    for bb in range(13):
        for ss in range(19):
            lhs = sylvester_det([c13.get(e, Pz()).at(b=bb, s=ss) for e in (3, 2, 1, 0)],
                                [c23.get(e, Pz()).at(b=bb, s=ss) for e in (3, 2, 1, 0)])
            if lhs != 4 * (bb - 3) * (bb + 1) * (ss - 2) * (ss - 1) ** 3 * nt_big(bb, ss):
                return False
    # (d) big(4 + x, 3 + y) has positive coefficients (x, y >= 0)
    sh = nt_big(4 + b, 3 + s)
    if any(v <= 0 for v in sh.d.values()):
        return False
    # (e) instances: threshold forms F = E(p + q^e, q^e) with E = P^s + sum_{k>=2} c_k Q^(ek) P^(s-k)
    for e, cs, Wmax in [(4, [1, 0, 0, 0], 18), (4, [1, 0, 2, -1], 18), (5, [1, 0, -1, 3], 21), (4, [1, 0, 1, 0, -2], 22),
                         (3, [1, 0, 0, 0], 14), (3, [1, 0, 2, -1], 14), (3, [1, 0, -1, 0, 3], 17)]:
        sd, Fh = len(cs) - 1, {}
        for kk, c in enumerate(cs):
            for t in range(sd - kk + 1):
                if c:
                    m = (e * kk + e * (sd - kk - t), t)
                    Fh[m] = Fh.get(m, F(0)) + c * comb(sd - kk, t)
        if flat_core_dims(TR.tidy(Fh), e, Wmax, R=4) != [(0, 1), (e * sd, 1)]:
            return False
    return True


def nv_rows(i, N, B, K, s):
    """Theorem NV: level-K rows (coefficient of x1, coefficient of c x0) for F = p^s + c q^B p^(s-K) + ... and
    g = x0 q^i p^N + x1 q^(i+B) p^(N-K) + ...; only the pairs used in the proof."""
    k = B * (s - 2) * (s - 1)
    if i == 0:
        return {'T3g': (-s * k * (B - 2) * (B - 1), N * B * (N - 2) * (N - 1) * (B - 2) * (B - 1)),
                'T3Dg': (s ** 2 * k * (B - 3) * (B - 2) * (B - 1), -N * s * k * (B - 3) * (B - 2) * (B - 1))}
    if i == 1:
        return {'T3g': (-s * k * (B - 1) * (B + 1), -B * N * (B - 1) * (N - 1) * (-B * N + 2 * B - 3 * K + 2 * N + 3 * s - 4)),
                'T3Dg': (s ** 2 * k * (B - 2) * (B - 1) * (B + 1),
                         -B * s * (B - 2) * (B - 1) * (B * N * s ** 2 - 3 * B * N * s + 2 * B * N + K * s ** 2 - 3 * K * s + 2 * K
                                                       + N ** 3 + 3 * N ** 2 * s - 6 * N ** 2 + 3 * N * s ** 2 - 12 * N * s + 11 * N
                                                       - 3 * s ** 2 + 9 * s - 6)),
                'T3DDg': (-s ** 3 * k * (B - 3) * (B - 2) * (B - 1) * (B + 1), s ** 2 * k * (B - 3) * (B - 2) * (B - 1) * (B * N + K + N - 1))}
    return {'T3DDg': (-s ** 3 * k * (B - 2) * (B - 1) * (B + 1) * (B + 2),
                      B * s ** 2 * (B - 2) * (B - 1) * (B ** 2 * N * s ** 2 - 3 * B ** 2 * N * s + 2 * B ** 2 * N + 2 * B * K * s ** 2
                                                        - 6 * B * K * s + 4 * B * K + 3 * B * N * s ** 2 - 9 * B * N * s + 6 * B * N
                                                        - 2 * B * s ** 2 + 6 * B * s - 4 * B + 4 * K * s ** 2 - 12 * K * s + 8 * K
                                                        + 2 * N ** 3 + 12 * N ** 2 * s - 18 * N ** 2 + 24 * N * s ** 2 - 72 * N * s
                                                        + 52 * N + 12 * s ** 3 - 60 * s ** 2 + 96 * s - 48)),
            'T3D3g': (s ** 4 * k * (B - 3) * (B - 2) * (B - 1) * (B + 1) * (B + 2),
                      -s ** 3 * k * (B - 3) * (B - 2) * (B - 1) * (B + 2) * (B * N + 2 * K + N - 2))}


def nv_direct(i, N, B, K, s):
    """the rows of nv_rows from weyl_receipts, with c = 1."""
    Fh = {(0, s): F(1), (B, s - K): F(1)}
    D, C3 = W.derivation(Fh), W.gate(Fh, 3)
    out = {}
    for name in nv_rows(i, 0, B, K, s):
        r = {'T3g': 0, 'T3Dg': 1, 'T3DDg': 2, 'T3D3g': 3}[name]

        def op(g):
            for _ in range(r):
                g = W.act(D, g)
            return W.act(C3, g)
        mon = (i + B - r - 3, N - K + r * (s - 1) + s - 3)
        out[name] = (op({(i + B, N - K): F(1)}).get(mon, 0), op({(i, N): F(1)}).get(mon, 0))
    return out


def grid_NV():
    N, B, s, K = ZN, ZB, ZS, ZK
    # (a) closed-form rows against the gates: degree <= 5 in B, s, N and <= 2 in K
    for i in (0, 1, 2):
        for BB in range(4, 10):
            for KK in range(1, 4):
                for ss in range(3, 9):
                    for NN in range(KK, KK + 6):
                        cf, dr = nv_rows(i, NN, BB, KK, ss), nv_direct(i, NN, BB, KK, ss)
                        if any(F(cf[k][0]) != dr[k][0] or F(cf[k][1]) != dr[k][1] for k in cf):
                            return False
    # (b) the minors
    k0 = B ** 2 * (B - 2) * (B - 1) * (s - 2) * (s - 1)
    r0, r1, r2 = (nv_rows(i, N, B, K, s) for i in (0, 1, 2))
    if minor(r0, 'T3g', 'T3Dg') != k0 * N * s ** 2 * (s - N) * (B - 3) * (B - 2) * (B - 1) * (N + s - 3):
        return False
    if minor(r1, 'T3Dg', 'T3DDg') != -k0 * s ** 4 * (N - 1) * (B - 3) * (B - 2) * (B - 1) * (B + 1) * (N + s - 1) * (N + 2 * s - 4):
        return False
    m1, sub = minor(r1, 'T3g', 'T3DDg'), Pz()
    for kk, v in m1.d.items():                       # N = 1
        sub = sub + Pz({(0,) + kk[1:]: v})
    if sub != -k0 * s ** 3 * (B - 3) * (B - 1) * (B + 1) * (B + K) * (s - 1) * (s - 2):
        return False
    if minor(r2, 'T3DDg', 'T3D3g') != -2 * k0 * s ** 6 * (B - 3) * (B - 2) * (B - 1) * (B + 1) * (B + 2) * (N + s - 2) * (N + 2 * s - 2) * (N + 3 * s - 5):
        return False
    # (c) instances: flat cores of weighted forms with vertex p^s and adjacent monomial q^B p^(s-K), B >= 4
    for Fh, (a, b), Wmax in [({(0, 3): F(1), (5, 1): F(1)}, (2, 5), 20), ({(0, 4): F(1), (7, 2): F(2), (14, 0): F(-1)}, (2, 7), 30),
                             ({(0, 3): F(1), (4, 1): F(1), (6, 0): F(3)}, (1, 2), 16), ({(0, 4): F(1), (4, 2): F(-1)}, (1, 2), 14)]:
        if flat_core_dims_w(Fh, a, b, Wmax) != [(0, 1), (max(i * a + j * b for i, j in Fh), 1)]:
            return False
    return True


def flat_core_dims_w(Fh, a, b, Wmax, R=4):
    """flat core dimensions by weight, q of weight a and p of weight b."""
    D, gates = W.derivation(Fh), {k: W.gate(Fh, k) for k in (3, 5, 7)}
    out = []
    for Wt in range(Wmax + 1):
        mons = [(i, (Wt - a * i) // b) for i in range(Wt // a + 1) if (Wt - a * i) % b == 0]
        if not mons:
            continue
        cols = []
        for mm in mons:
            g, img = {mm: F(1)}, {}
            for r in range(R + 1):
                for kk, C in gates.items():
                    for ee, v in W.act(C, g).items():
                        img[(r, kk, ee)] = v
                g = W.act(D, g)
            cols.append(img)
        keys = sorted({kk for c in cols for kk in c})
        M = [[c.get(kk, F(0)) for c in cols] for kk in keys]
        dm = len(mons) - (L.rank(M, len(mons)) if M else 0)
        if dm:
            out.append((Wt, dm))
    return out


def positive_shift(f, n0, s0):
    """every coefficient of f(n0 + N, s0 + s) is positive, so f > 0 for N >= n0, s >= s0."""
    return all(v > 0 for v in f(n0 + ZN, s0 + ZS).d.values())


def nv32_rows(N, s, c):
    """B = 3, K = 2: (x0, x1, x2) coefficients for F = p^s + q^3 p^(s-2) + c q^6 p^(s-4) and
    g = x0 q^i p^N + x1 q^(i+3) p^(N-2) + x2 q^(i+6) p^(N-4); keys (i, row, level/2)."""
    k = (s - 2) * (s - 1)
    return {(0, 'T3g', 1): (6 * N * (N - 2) * (N - 1), -6 * s * k, 0),
            (0, 'T3Dg', 2): (-18 * N * (-N ** 3 + 3 * N ** 2 * s + 6 * N * s ** 2 - 27 * N * s + 19 * N + 20 * c * s ** 3 - 60 * c * s ** 2
                                        + 40 * c * s + 2 * s ** 3 - 18 * s ** 2 + 46 * s - 30),
                             18 * s * (-N + 3 * s - 3) * (N ** 2 - 3 * N + 4 * s ** 2 - 12 * s + 10), 360 * s ** 2 * k),
            (0, 'T3DDg', 2): (36 * N * s * (-N ** 3 - 3 * N ** 2 * s + 9 * N ** 2 - 6 * N * s ** 2 + 27 * N * s - 32 * N + 20 * c * s ** 3
                                            - 60 * c * s ** 2 + 40 * c * s + 2 * s ** 3 - 2 * s ** 2 - 14 * s + 20),
                              -36 * s ** 2 * (-N ** 3 - 3 * N ** 2 * s + 9 * N ** 2 - 16 * N * s ** 2 + 57 * N * s - 52 * N + 12 * s ** 3
                                              - 32 * s ** 2 + 6 * s + 20), -720 * s ** 3 * k),
            (1, 'T3g', 1): (-6 * N * (N - 1) * (-N + 3 * s - 4), -24 * s * k, 0),
            (1, 'T3Dg', 1): (-6 * s * (N ** 3 + 3 * N ** 2 * s - 6 * N ** 2 + 6 * N * s ** 2 - 21 * N * s + 17 * N - s ** 2 + 3 * s - 2),
                             24 * s ** 2 * k, 0),
            (2, 'T3Dg', 1): (12 * s * (-N ** 3 - 3 * N * s ** 2 + 9 * N * s - 5 * N + 6 * s ** 3 - 29 * s ** 2 + 45 * s - 22), 120 * s ** 2 * k, 0),
            (2, 'T3DDg', 1): (12 * s ** 2 * (N ** 3 + 6 * N ** 2 * s - 9 * N ** 2 + 21 * N * s ** 2 - 63 * N * s + 44 * N + 6 * s ** 3
                                             - 23 * s ** 2 + 27 * s - 10), -120 * s ** 3 * k, 0)}


def nv32_direct(N, s, c):
    Fh = TR.tidy({(0, s): F(1), (3, s - 2): F(1), (6, s - 4): F(c)})
    D, C3 = W.derivation(Fh), W.gate(Fh, 3)
    out = {}
    for (i, name, lev) in nv32_rows(0, 3, 0):
        r = {'T3g': 0, 'T3Dg': 1, 'T3DDg': 2}[name]

        def op(g):
            for _ in range(r):
                g = W.act(D, g)
            return W.act(C3, g)
        pe = N + r * (s - 1) + s - 3 - 2 * lev
        wt = 3 * s * (r + 1) + 2 * i + 3 * N - 5 * (r + 3)
        mon = ((wt - 3 * pe) // 2, pe)
        out[(i, name, lev)] = tuple(op({(i + 3 * j, N - 2 * j): F(1)}).get(mon, 0) for j in range(3))
    return out


def grid_NV32():
    """flat lower terms with vertex-adjacent monomial q^3 p^(s-2) (the case B = 3, which forces K = 2)."""
    for NN in range(4, 11):
        for ss in range(4, 11):
            for cc in (0, 1):
                cf, dr = nv32_rows(NN, ss, cc), nv32_direct(NN, ss, cc)
                if any(F(x) != y for k in cf for x, y in zip(cf[k], dr[k])):
                    return False
    N, s = ZN, ZS
    r = nv32_rows(N, s, ZB)                                      # c in the b-slot
    A = {k: s * (s - 1) * (s - 2) * r[(0, k, 2)][0] + N * (N - 1) * (N - 2) * r[(0, k, 2)][1] for k in ('T3Dg', 'T3DDg')}
    e0 = A['T3Dg'] * r[(0, 'T3DDg', 2)][2] - A['T3DDg'] * r[(0, 'T3Dg', 2)][2]
    if e0 != 12960 * N * s ** 4 * (s - N) * (s - 2) * (s - 1) * (N + s - 3) * (6 * N ** 2 * s - 9 * N ** 2 + 12 * N * s ** 2 - 54 * N * s
                                                                               + 51 * N - 16 * s ** 2 + 60 * s - 50):
        return False
    m1 = r[(1, 'T3g', 1)][0] * r[(1, 'T3Dg', 1)][1] - r[(1, 'T3g', 1)][1] * r[(1, 'T3Dg', 1)][0]
    if m1 != -144 * s ** 2 * (s - 2) * (s - 1) * (6 * N ** 2 * s - 9 * N ** 2 + 6 * N * s ** 2 - 24 * N * s + 21 * N - s ** 2 + 3 * s - 2):
        return False
    m2 = r[(2, 'T3Dg', 1)][0] * r[(2, 'T3DDg', 1)][1] - r[(2, 'T3Dg', 1)][1] * r[(2, 'T3DDg', 1)][0]
    if m2 != -1440 * s ** 4 * (s - 2) * (s - 1) * (6 * N ** 2 * s - 9 * N ** 2 + 18 * N * s ** 2 - 54 * N * s + 39 * N
                                                    + 4 * (s - 1) * (s - 2) * (3 * s - 4)):
        return False
    # signs: f0 < 0 at N = 1 and > 0 for N >= 2; f1 < 0 at N = 0 and > 0 for N >= 1; f2 > 0 (all for s >= 3)
    f0 = lambda N, s: 6 * N ** 2 * s - 9 * N ** 2 + 12 * N * s ** 2 - 54 * N * s + 51 * N - 16 * s ** 2 + 60 * s - 50
    f1 = lambda N, s: 6 * N ** 2 * s - 9 * N ** 2 + 6 * N * s ** 2 - 24 * N * s + 21 * N - s ** 2 + 3 * s - 2
    f2 = lambda N, s: 6 * N ** 2 * s - 9 * N ** 2 + 18 * N * s ** 2 - 54 * N * s + 39 * N + 4 * (s - 1) * (s - 2) * (3 * s - 4)
    if not (positive_shift(f0, 2, 3) and positive_shift(f1, 1, 3) and positive_shift(f2, 0, 3)):
        return False
    if f0(1, s) != -4 * (s - 2) * (s - 1) or f1(0, s) != -(s - 2) * (s - 1):
        return False
    for Fh, Wmax in [({(0, 4): F(1), (3, 2): F(1)}, 22), ({(0, 4): F(1), (3, 2): F(1), (6, 0): F(-2)}, 22),
                     ({(0, 5): F(1), (3, 3): F(2), (6, 1): F(1)}, 25)]:
        if flat_core_dims_w(Fh, 2, 3, Wmax) != [(0, 1), (max(2 * i + 3 * j for i, j in Fh), 1)]:
            return False
    return True


def identities():
    return {'GG': grid_GG(), 'T3': grid_T3(), 'AE': grid_AE(), 'K1c': grid_K1c(), 'C2': grid_C2(),
            'NA': grid_NA(), 'TG': grid_TG(), 'GE': grid_GE(), 'BE': grid_BE(), 'NT': grid_NT(), 'NV': grid_NV(), 'NV32': grid_NV32()}


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
                       'non-affine binomial edges collapse (Theorem NA), general first edges (NE), the boundary edge (NB), '
                       'threshold edges with deg w >= 3 (NT), edges below the threshold and flat lower terms (NV)'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
