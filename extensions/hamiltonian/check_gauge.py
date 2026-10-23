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

Upper bounds (section 6.14). K2U: for h = alpha P^2 + gamma Q^2 + lam Q + c the third gate is
-6 alpha w'' g_PPQ + 2 alpha w''' P g_PPP; with the degree-preserving top part of D this confines the core to
total degree <= 2 (K[P] + quadratics for deg w = 2, gamma = 0).                       [K2U: identity, instances]
LB (higher shears, b linear): the top core of E = P^f + Q P (Q of weight f - 1) is span{1, E}: D0 = {E, .} has the
eigenvectors P^r (Q + P^(f-1))^j with distinct eigenvalues r - j, and the order-1 top gate kills all but 1 and E.
                                                                       [LB: C1 formula, eigenvectors, instances]
K1P (cubic phase, f = 3): the top core of a P^3 + mu Q P is span{1, P, Q, P^2, E, P E}; P H is in the core iff
lam = 0.                                                                   [K1P: top cores, obstruction values]
TP (transverse top l^k, 2 <= k != s): span{1, H} for s >= 3; for s = 2 span{1, H} or, on the extended K3
H = c Q^(k-2) G^2 + beta G + r, span{1, G, H}.                         [TP: instances, extended K3 identities]
TE (transverse top l^k, k in {1, s}): reduce to the first Newton edge E from Q^k m^s; level-K rows of T_j D^r g in
(x1, c x0) (computed symbolically here); for k = s the rows with r >= 1 are proportional and the rank drops only on
X = X5 = X7 = 0, excluded by an elimination (transverse_edge.json) with a positivity certificate; for k = 1 a chain
argument and nonzero leading N-coefficients; s = 2 leaves exactly K3.        [TE: rows, elimination, instances]
NT for deg w = 2 (cubic-phase threshold): twisted top problem exp(tA + t^2 B), weights (1, 2); the vertex forces the
coefficients below the first deviation level k0 to vanish, and level k0 (levels 2-3 when k0 = 2) forces the top
coefficient to vanish.                                                   [CT: twisted rows, minors, instances]

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


def topgate(E, g, e, m):
    """closed-form top gate of order m (Theorem NE (1)) for the monomial shear of degree e."""
    a, b = dP(E, m), dP(g, m)
    if e == 2:
        return pb(a, b)
    return TR.add(TR.mul({(1, 0): F(3)}, pb(a, b)),
                  TR.sc(TR.add(TR.mul(a, dP(b)), TR.sc(TR.mul(dP(a), b), -1)), F(m * (e - 2))))


def top_core(E, wq, e, nmax):
    """[(weight, dim)] of the top core of E (Q of weight wq, P of weight 1): the largest {E, .}-invariant
    space of weight-homogeneous g on which every top gate of order m has P-degree < m."""
    dE = max(j for _, j in E)
    out = []
    for n in range(nmax + 1):
        mons = [(j, n - wq * j) for j in range(n // wq + 1)]
        cols = []
        for mm in mons:
            img = {}
            for m in range(1, dE + 2):
                for (i, j), v in topgate(E, {mm: F(1)}, e, m).items():
                    if j >= m:
                        img[(m, i, j)] = v
            cols.append(img)
        keys = sorted({k for c in cols for k in c})
        M = [[c.get(k, F(0)) for c in cols] for k in keys]
        V = L.null_basis(M, len(mons)) if M else [[F(int(a == b)) for a in range(len(mons))] for b in range(len(mons))]
        while V:                                  # largest D0-invariant subspace
            imgs = [pb(E, TR.tidy({mons[a]: v[a] for a in range(len(mons))})) for v in V]
            nv = len(V)
            rk = sorted({k for g in imgs for k in g} | set(mons))
            A = [[im.get(k, F(0)) for im in imgs] + [-(V[b][mons.index(k)] if k in mons else F(0)) for b in range(nv)]
                 for k in rk]
            sol = L.null_basis(A, 2 * nv)
            W2 = [[sum(z[b] * V[b][a] for b in range(nv)) for a in range(len(mons))] for z in sol]
            r = L.rank(W2, len(mons)) if W2 else 0
            if r == nv:
                break
            V = [list(v) for v in L.rref(W2, len(mons))[0][:r]] if r else []
        if V:
            out.append((n, len(V)))
    return out


def _pow(f, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = TR.mul(out, f)
    return out


def grid_K2U(seed=41):
    """K2 and K1+K2 upper bounds: for h = alpha P^2 + r(Q), deg r <= 2,
    T_3 = -6 alpha w'' g_PPQ + 2 alpha w''' P g_PPP."""
    rng = random.Random(seed)
    for _ in range(12):
        al = F(rng.choice([1, -2, 3]))
        h = TR.tidy({(0, 2): al, (2, 0): F(rng.randint(-2, 2)), (1, 0): F(rng.randint(-2, 2)), (0, 0): F(1)})
        w = {e: F(rng.randint(-2, 2)) for e in range(rng.randint(2, 6) + 1)}
        g = CT.rand_poly(rng, rng.randint(2, 6))
        om, om1 = CT.U(CT.uderiv(w, 2)), CT.U(CT.uderiv(w, 3))
        want = TR.add(TR.mul(TR.sc(om, -6 * al), W.pder(g, 1, 2)),
                      TR.mul(TR.sc(om1, 2 * al), TR.mul({(0, 1): F(1)}, W.pder(g, 0, 3))))
        if third(h, g, w) != want:
            return False
    for H, N, want in [(CT.tri({(0, 2): F(1), (2, 0): F(1)}, {3: F(1)}), 9, 6),
                       (CT.tri({(0, 2): F(1), (2, 0): F(-1), (1, 0): F(2)}, {2: F(1)}), 8, 6)]:
        if full_dim(TR.tidy(H), N) != want:
            return False
    return True


def grid_LB():
    """linear b, higher shears: E = P^f + Q P with e >= 3."""
    for f in range(3, 8):
        E = {(0, f): F(1), (1, 1): F(1)}
        R = {(1, 0): F(1), (0, f - 1): F(1)}
        for e in range(3, 7):
            for i in range(4):
                for r in range(9):
                    want = TR.tidy({(i + 1, r - 2): F((e + 1) * r * (r - 1)) if r >= 2 else F(0),
                                    (i, r + f - 3): F(f * r * ((e - 2) * (r - f) - 3 * (f - 1) * i))})
                    if topgate(E, {(i, r): F(1)}, e, 1) != want:
                        return False
        for r in range(6):
            for j in range(5):
                g = TR.mul({(0, r): F(1)}, _pow(R, j))
                if pb(E, g) != TR.sc(g, F(r - j)):
                    return False
    for f, e in [(3, 3), (4, 3), (3, 4), (5, 5)]:
        if top_core({(0, f): F(1), (1, 1): F(1)}, f - 1, e, 2 * f + 3) != [(0, 1), (f, 1)]:
            return False
    for h, w, N in [({(0, 3): F(1), (1, 1): F(1)}, {3: F(1), 1: F(1)}, 9),
                    ({(0, 3): F(2), (1, 1): F(-1), (1, 0): F(1), (0, 1): F(1)}, {3: F(1)}, 9)]:
        if full_dim(TR.tidy(CT.tri(h, w)), N) != 2:
            return False
    return True


def grid_K1P(seed=43):
    """K1 prime with f = 3: the top core of a P^3 + mu Q P (cubic phase) is span{1, P, Q, P^2, E, P E}, and
    P H leaves the core exactly when lam != 0."""
    for a, mu in [(1, 1), (2, -3)]:
        if top_core({(0, 3): F(a), (1, 1): F(mu)}, 2, 2, 16) != [(0, 1), (1, 1), (2, 2), (3, 1), (4, 1)]:
            return False
    rng = random.Random(seed)
    for _ in range(6):
        a, b, lam, mu = (F(rng.choice([1, -1, 2, 3])) for _ in range(4))
        h = {(0, 3): a, (0, 1): b, (1, 0): lam, (1, 1): mu}
        w = {2: F(1), 1: F(rng.randint(-2, 2))}
        Ph = TR.mul({(0, 1): F(1)}, h)
        if third(h, Ph, w) != {(0, 0): -36 * a * lam} or third(h, {(0, 3): F(1)}, w) != {(0, 0): 36 * mu}:
            return False
        g = TR.add(Ph, {(0, 3): a * lam / mu})
        if third(h, g, w) or third(h, pb(h, g), w) != {(0, 0): 72 * a * lam * mu}:
            return False
    return True


def grid_TP():
    """perfect-power transverse tops phi = l^k, 2 <= k != s, s >= 3 (coordinates (l, m) = (q, p))."""
    for H, N in [({(2, 3): F(1), (6, 0): F(1)}, 8), ({(3, 4): F(1), (8, 0): F(1), (1, 2): F(2), (0, 1): F(1)}, 9),
                 ({(4, 3): F(1), (8, 0): F(-1), (3, 2): F(1), (2, 0): F(1)}, 9),
                 ({(3, 2): F(1), (8, 0): F(1), (1, 1): F(1)}, 9),                          # s = 2, k = 3
                 ({(3, 2): F(1), (5, 1): F(2), (7, 0): F(1), (1, 1): F(1), (1, 0): F(1)}, 8)]:   # near the K3 family
        if full_dim(TR.tidy(H), N) != 2:
            return False
    # s = 2, k >= 3: the extended family K3, H = c Q^(k-2) G^2 + beta G + r, r in span{1, Q^(k-2)}:
    # {H, G} = (k-2) H - (k-2) beta G + (Q r' - (k-2) r), so span{1, G, H} is D-invariant and gate-free.
    rng = random.Random(47)
    for _ in range(6):
        k = rng.randint(3, 5)
        v = {(i, 0): F(rng.randint(-2, 2)) for i in range(rng.randint(3, 4) + 1)}
        v[(max(i for i, _ in v), 0)] = F(1)
        G = TR.tidy(TR.add({(1, 1): F(1)}, v))
        c, beta = F(rng.choice([1, 2, -1])), F(rng.choice([1, -2, 3]))
        r = TR.tidy({(0, 0): F(rng.randint(-2, 2)), (k - 2, 0): F(rng.randint(-2, 2))})
        H = TR.tidy(TR.add(TR.sc(TR.mul({(k - 2, 0): F(1)}, TR.mul(G, G)), c), TR.sc(G, beta), r))
        rhs = TR.add(TR.sc(H, F(k - 2)), TR.sc(G, -(k - 2) * beta),
                     TR.mul({(1, 0): F(1)}, W.pder(r, 1, 0)), TR.sc(r, F(2 - k)))
        if pb(H, G) != TR.tidy(rhs) or not CT.span_ok(H, [{(0, 0): F(1)}, G, H]):
            return False
        res = TR.classify(H)
        if res['route'] != 'K3' or not res['proved']:
            return False
    H = TR.tidy(TR.add(TR.mul({(1, 0): F(1)}, TR.mul({(1, 1): F(1), (3, 0): F(1)}, {(1, 1): F(1), (3, 0): F(1)})),
                       {(1, 1): F(1), (3, 0): F(1), (0, 0): F(1)}))             # Q (Qm + Q^3)^2 + (Qm + Q^3) + 1
    return full_dim(H, 9) == 3

# ---- Theorem TE: transverse tops l^k with k in {1, s} ----------------------------------------


def _ffz(x, n):
    out = Pz.of(1)
    for i in range(n):
        out = out * (x - i)
    return out


def _tcz(k, P, Q, x, z):
    return sum((_ffz(P, k - l) * _ffz(Q, l) * _ffz(x, l) * _ffz(z, k - l) * ((-1) ** l * comb(k, l)) for l in range(k + 1)), Pz())


def te_rows(kv, itop, ntop, ops):
    """level-K rows (coefficient of x1, coefficient of c x0) of T_k D^r g for the edge with vertex q^kv p^s and
    adjacent monomial c q^(kv+B) p^(s-K), g = x0 q^itop p^ntop + x1 q^(itop+B) p^(ntop-K) + ...; symbolic in N, B, s, K.
    Terms are (q-exponent, p-exponent, coefficient, level, which x)."""
    N, B, s, K = ZN, ZB, ZS, ZK
    Fm = [(Pz.of(kv) if not isinstance(kv, Pz) else kv, s, Pz.of(1), 0)]
    Fm.append((Fm[0][0] + B, s - K, Pz.of(1), 1))
    G = [(itop, ntop, Pz.of(1), 0, 0), (itop + B, ntop - K, Pz.of(1), 1, 1)]
    chains = [G]
    for _ in range(max(r for _, r in ops)):
        nxt = []
        for (a, b, cf, lf) in Fm:
            for (x, z, cg, lg, w) in chains[-1]:
                if lf + lg <= 1:
                    nxt.append((a + x - 1, b + z - 1, cf * cg * (a * z - b * x), lf + lg, w))
        chains.append(nxt)
    out = {}
    for k, r in ops:
        x1, cx0 = Pz(), Pz()
        for (a, b, cf, lf) in Fm:
            for (x, z, cg, lg, w) in chains[r]:
                if lf + lg == 1:
                    v = cf * cg * _tcz(k, a, b, x, z)
                    if w == 1:
                        x1 = x1 + v
                    else:
                        cx0 = cx0 + v
        out[(k, r)] = (x1, cx0)
    return out


def _te_data():
    d = json.loads((Path(__file__).resolve().parent / 'transverse_edge.json').read_text())
    return d


def _pz_from(terms, slots):
    """terms [[exponents], 'coeff'] over variables mapped to Pz slots (indices into (N, b, s, K))."""
    out = {}
    for ex, c in terms:
        key = [0, 0, 0, 0]
        for e, sl in zip(ex, slots):
            key[sl] += e
        out[tuple(key)] = out.get(tuple(key), 0) + int(c)
    return Pz(out)


def _upoly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def _upoly_add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def _upoly_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def _upoly_gcd(a, b):
    a, b = _upoly_trim(a), _upoly_trim(b)
    while b:
        r = list(a)
        while len(r) >= len(b) and r:
            c = r[-1] / b[-1]
            sh = len(r) - len(b)
            for i, y in enumerate(b):
                r[sh + i] -= c * y
            r = _upoly_trim(r)
        a, b = b, r
    return a


def _reduce_ud(P, Mv, sv):
    """P(N, B, K, s) at N = M - s, s = sv, B = (u - d)/2, K = (u + d)/2, with u^2 -> U(d) = (-6Md + 8M + 3d^2 + 6d - 12)/(2M - 3);
    returns (polynomial in d times (2M - 3)^e, e), or None if an odd power of u occurs."""
    Nv = Mv - sv
    biv = {}                                         # (u-power, d-power) -> coeff
    for (eN, eB, es, eK), c in P.d.items():
        base = F(c) * Nv ** eN * sv ** es
        # ((u - d)/2)^eB ((u + d)/2)^eK
        for i in range(eB + 1):
            for j in range(eK + 1):
                cc = base * comb(eB, i) * comb(eK, j) * (-1) ** (eB - i) / F(2) ** (eB + eK)
                key = (i + j, eB - i + eK - j)
                biv[key] = biv.get(key, F(0)) + cc
    biv = {k: v for k, v in biv.items() if v}
    if any(k[0] % 2 for k in biv):
        return None
    top = max((k[0] // 2 for k in biv), default=0)
    Unum = [F(8 * Mv - 12), F(-6 * Mv + 6), F(3)]   # numerator of U in powers of d; denominator 2M - 3
    den = F(2 * Mv - 3)
    out = [F(0)]
    for (ue, de), v in biv.items():
        j = ue // 2
        term = [F(0)] * de + [v]
        for _ in range(j):
            term = _upoly_mul(term, Unum)
        term = [x * den ** (top - j) for x in term]
        out = _upoly_add(out, term)
    return _upoly_trim(out), top


def grid_TE():
    N, B, s, K = ZN, ZB, ZS, ZK
    dat = _te_data()
    X = _pz_from(dat['X'], (0, 1, 3, 2))
    X5 = _pz_from(dat['X5'], (0, 1, 3, 2))
    X7 = _pz_from(dat['X7'], (0, 1, 3, 2))
    # --- vertex (q p)^s: rows with r >= 1 are proportional to (-s, N); the T3 scales cannot all vanish
    R = te_rows(s, N, N, [(3, 0), (5, 0), (7, 0), (3, 1), (3, 2), (3, 3), (5, 1), (5, 2), (5, 3)])
    for k in (3, 5):
        for r in (1, 2, 3):
            if R[(k, r)][0] * N + R[(k, r)][1] * s != Pz():
                return False
    Y = {1: -B ** 2 * s + 2 * B ** 2 - 2 * B * K * s - 2 * B * K + 6 * B * N + 9 * B * s - 12 * B - K ** 2 * s + 2 * K ** 2
            - 6 * K * N - 9 * K * s + 12 * K + 6 * N ** 2 + 18 * N * s - 24 * N + 12 * s ** 2 - 32 * s + 22}
    Y[2] = Y[1] + 6 * (s - 1) * (B - K + 2 * N + 4 * s - 5)
    Y[3] = Y[2] + 6 * (s - 1) * (B - K + 2 * N + 6 * s - 7)
    for r in (1, 2, 3):
        if R[(3, r)][0] != (-1) ** r * s ** (r + 1) * (s - 1) * (B + K) ** (r + 1) * Y[r]:
            return False
    pre = -N * s * (B + K) * (s - N)
    for k, Xk in ((3, X), (5, X5), (7, X7)):
        if R[(k, 0)][0] * N + R[(k, 0)][1] * s != pre * Xk:
            return False
    # --- elimination: U solves X; X5, X7 reduce to f5, f7; Res_d(f5, f7) = 38400 (2M-3)^4 big(M, s)
    f5 = _pz_from(dat['f5'], (0, 1, 2))            # (M, d, s) in slots (N, b, s)
    f7 = _pz_from(dat['f7'], (0, 1, 2))
    big = _pz_from(dat['big'], (0, 2))
    ucoef = lambda P, Mv, sv: [sum(F(c) * Mv ** k[0] * sv ** k[2] for k, c in P.d.items() if k[1] == j)
                               for j in range(P.deg(1) + 1)]
    for Mv in range(0, 12):                            # the relations have degree <= 9 in M and <= 4 in s
        for sv in range(0, 7):
            rx = _reduce_ud(X, Mv, sv)
            r5, r7 = _reduce_ud(X5, Mv, sv), _reduce_ud(X7, Mv, sv)
            if rx is None or r5 is None or r7 is None or rx[0]:
                return False
            want5 = _upoly_mul([F(0), F(3), F(-3)], ucoef(f5, Mv, sv))
            want7 = _upoly_mul([x * (2 * Mv - 3) for x in [F(0), F(3), F(-3)]], ucoef(f7, Mv, sv))
            # normalize the powers of (2M - 3): r5 carries (2M-3)^e5, the relation is stated with (2M-3)^2, (2M-3)^4
            got5 = [x * F(2 * Mv - 3) ** (2 - r5[1]) for x in r5[0]] if r5[1] <= 2 else None
            got7 = [x * F(2 * Mv - 3) ** (4 - r7[1]) for x in r7[0]] if r7[1] <= 4 else None
            if got5 is None or got7 is None or _upoly_trim(got5) != _upoly_trim(want5) or _upoly_trim(got7) != _upoly_trim(want7):
                return False
    dM = 4 * f5.deg(0) + 2 * f7.deg(0)
    dS = 4 * f5.deg(2) + 2 * f7.deg(2)
    for Mv in range(dM + 1):
        for sv in range(dS + 1):
            a, b = ucoef(f5, Mv, sv), ucoef(f7, Mv, sv)       # formal degrees 2 and 4 in d
            a, b = (a + [F(0)] * 3)[:3], (b + [F(0)] * 5)[:5]
            lhs = sylvester_det(list(reversed(a)), list(reversed(b)))
            if lhs != 38400 * (2 * Mv - 3) ** 4 * big.at(N=Mv, s=sv):
                return False
    # positivity for s >= 15 (M = N + s >= s + 1)
    sh = Pz()
    for k, c in big.d.items():
        sh = sh + Pz.of(c) * (N + s + 16) ** k[0] * (s + 15) ** k[2]
    if any(v <= 0 for v in sh.d.values()):
        return False
    # 2 <= s <= 14: integer roots M >= s + 1 of big, then common roots of f5, f7 in d
    admissible = []
    for sv in range(2, 15):
        M0 = sv + 1
        while True:                                     # big(M0 + x, s) > 0 coefficientwise from some M0 on
            shc = {}
            for k, c in big.d.items():
                for i in range(k[0] + 1):
                    shc[i] = shc.get(i, 0) + c * sv ** k[2] * comb(k[0], i) * M0 ** (k[0] - i)
            if all(v > 0 for v in shc.values()):
                break
            M0 += 1
        for Mv in range(sv + 1, M0 + 1):
            if big.at(N=Mv, s=sv) != 0:
                continue
            a, b = ucoef(f5, Mv, sv), ucoef(f7, Mv, sv)
            if not _upoly_trim(a) and not _upoly_trim(b):
                admissible.append((sv, Mv, 'all d'))
                continue
            g = _upoly_gcd(a, b)
            for dv in range(-200, 0):
                if g and sum(x * dv ** i for i, x in enumerate(g)) == 0:
                    Uv = F(-6 * Mv * dv + 8 * Mv + 3 * dv * dv + 6 * dv - 12, 2 * Mv - 3)
                    uv = int(round(float(Uv) ** 0.5)) if Uv >= 0 else -1
                    if uv >= 0 and uv * uv == Uv and (uv + dv) % 2 == 0 and (uv + dv) // 2 >= 1 and (uv - dv) // 2 > (uv + dv) // 2:
                        admissible.append((sv, Mv, dv))
    if admissible != [(2, 3, 'all d')]:
        return False
    # at s = 2, N = 1: X = 3/2 (u^2 - (d - 2)^2) forces u = 2 - d, i.e. K = 1
    X21 = Pz()
    for k, c in X.d.items():
        X21 = X21 + Pz({(0, k[1], 0, k[3]): c * 1 ** k[0] * 2 ** k[2]})
    if 2 * X21 != 3 * ((B + K) ** 2 - (K - B - 2) ** 2):
        return False
    # --- vertex q p^s (phi linear): leading N-coefficients, and the rows at N = 1
    for itop, lead in ((0, 3 * B ** 2 * s * (B - 1) ** 2 * (B + 1) * (s - 1) * (B * s + K + 2 * s - 2)),
                       (1, 3 * B ** 2 * s * (B - 1) * (B + 1) ** 2 * (s - 1) * (B * s + K + 2 * s - 2))):
        Rk = te_rows(1, Pz.of(itop), N, [(3, 0), (3, 1)])
        m = Rk[(3, 0)][0] * Rk[(3, 1)][1] - Rk[(3, 0)][1] * Rk[(3, 1)][0]
        cN = m.coeffs_in(0)
        if cN[max(cN)] != lead:
            return False
    R1 = te_rows(1, Pz.of(1), Pz.of(1), [(3, 0), (3, 1), (3, 2), (5, 1), (5, 2)])
    L = lambda r: B * s - 2 * B + 3 * K - (3 * r + 1) * s + 3 * r - 1
    if R1[(3, 0)] != (-B * s * (B + 1) * (s - 1) * L(0), Pz()):
        return False
    for key in ((3, 1), (3, 2), (5, 1), (5, 2)):
        if R1[key][0] * (B + K) + R1[key][1] * (B * s + K + s - 1) != Pz():
            return False
    if R1[(3, 1)][0] != B * s * (B + 1) * (s - 1) * (B * s + K + s - 1) * L(1) or \
            R1[(3, 2)][0] != -B * s * (B + 1) * (s - 1) * (B * s + K) * (B * s + K + s - 1) * L(2):
        return False
    # --- instances (coordinates (l, m) = (q, p))
    for H, N_, want in [({(1, 3): F(1), (5, 0): F(1)}, 6, 2), ({(1, 3): F(1), (3, 2): F(1), (6, 0): F(1), (0, 1): F(1)}, 7, 2),
                        ({(3, 3): F(1), (7, 0): F(1)}, 8, 2), ({(3, 3): F(1), (5, 2): F(2), (8, 0): F(1), (1, 1): F(1)}, 9, 2),
                        ({(2, 2): F(1), (5, 0): F(1), (0, 1): F(1)}, 7, 2), ({(1, 2): F(1), (4, 0): F(1), (2, 0): F(1)}, 6, 2)]:
        if full_dim(TR.tidy(H), N_) != want:
            return False
    G = {(1, 1): F(1), (3, 0): F(1)}                                                 # K3, k = 2: G^2 + 1
    if full_dim(TR.tidy(TR.add(TR.mul(G, G), {(0, 0): F(1)})), 8) != 3:
        return False
    return True

# ---- Theorem NT for the cubic phase: threshold edges with deg w = 2 ---------------------------


def _twops(k):
    """k! [t^k] exp(t A + t^2 B), A = dQ1 dP2 - dP1 dQ2, B = dP1 dP2^2 + dP1^2 dP2: (coef, a1, b1, a2, b2, v)."""
    out = {}
    for v in range(k // 2 + 1):
        u = k - 2 * v
        base = factorial(k) // (factorial(u) * factorial(v))
        for i in range(u + 1):
            for j in range(v + 1):
                key = (i, u - i + j + 2 * (v - j), u - i, i + 2 * j + (v - j), v)
                out[key] = out.get(key, 0) + base * comb(u, i) * (-1) ** (u - i) * comb(v, j)
    return [(c,) + key for key, c in out.items() if c]


def tw_rows(Fm, G, targets, R=3, ks=(3, 5, 7)):
    """rows of the twisted (cubic-phase) top gates T_k D^r g at the given levels. Fm, G: lists of
    (q-exponent, p-exponent, coefficient, level, tag) with Pz entries; a level is (units, extra), the extra part
    counting B-factors. Returns {(r, k, level): {(F-tags, g-tag): coefficient}}."""
    top = max(targets)
    keep = lambda lev: lev <= top
    chains = [[(x, z, c, lev, (), t) for (x, z, c, lev, t) in G]]
    for _ in range(R):
        nxt = []
        for (a, b, cf, lf, tf) in Fm:
            for (x, z, cg, lg, fts, t) in chains[-1]:
                lev = (lf[0] + lg[0], lf[1] + lg[1])
                if keep(lev):
                    nxt.append((a + x - 1, b + z - 1, cf * cg * (a * z - b * x), lev,
                                tuple(sorted(fts + ((tf,) if tf else ()))), t))
        chains.append(nxt)
    out = {}
    for r in range(R + 1):
        for k in ks:
            for (a, b, cf, lf, tf) in Fm:
                for (x, z, cg, lg, fts, t) in chains[r]:
                    for c, a1, b1, a2, b2, v in _twops(k):
                        lev = (lf[0] + lg[0], lf[1] + lg[1] + v)
                        if lev in targets:
                            val = cf * cg * _ffz(a, a1) * _ffz(b, b1) * _ffz(x, a2) * _ffz(z, b2) * c
                            key = (tuple(sorted(fts + ((tf,) if tf else ()))), t)
                            d = out.setdefault((r, k, lev), {})
                            d[key] = d.get(key, Pz()) + val
    return out


def grid_CT():
    N, s, k0 = ZN, ZS, ZK
    one = Pz.of(1)
    vertex = [(Pz(), s, one, (0, 0), None)]
    col = lambda rows, key, tags: [rows.get(key, {}).get(t, Pz()) for t in tags]

    def det(M):
        n = len(M)
        if n == 1:
            return M[0][0]
        return sum(((-1) ** j * M[0][j] * det([row[:j] + row[j + 1:] for row in M[1:]]) for j in range(n)), Pz())
    # (1) vertex only, type 0: the top P^N never contributes; level 2 fixes x1, x2
    G0 = [(Pz(), N, one, (0, 0), 'x0'), (Pz.of(2), N - 1, one, (0, 1), 'x1'), (Pz.of(4), N - 2, one, (0, 2), 'x2')]
    R = tw_rows(vertex, G0, {(0, 0), (0, 1), (0, 2)})
    if any(v != Pz() for d in R.values() for (ft, t), v in d.items() if t == 'x0'):
        return False
    A = [col(R, (0, 3, (0, 2)), [((), 'x1'), ((), 'x2')]), col(R, (1, 3, (0, 2)), [((), 'x1'), ((), 'x2')])]
    if det(A) != 576 * s ** 3 * (s - 2) * (s - 1) ** 3 * (N + s - 3):
        return False
    # (2) induction: the flat part of T3 on x_L at its own level is -(s)_3 (2L)_3 (L in the K slot)
    RL = tw_rows(vertex, [(2 * k0, N - k0, one, (1, 0), 'x')], {(1, 0)}, R=0, ks=(3,))
    if RL[(0, 3, (1, 0))][((), 'x')] != -s * (s - 1) * (s - 2) * (2 * k0) * (2 * k0 - 1) * (2 * k0 - 2):
        return False
    # (3) first deviation at level k0 (symbolic): rows in (x_k0, e x0)
    Fk = vertex + [(2 * k0, s - k0, one, (1, 0), 'e')]
    Gk = [(Pz(), N, one, (0, 0), 'x0'), (2 * k0, N - k0, one, (1, 0), 'xk')]
    Rk = tw_rows(Fk, Gk, {(1, 0)}, R=1, ks=(3,))
    tags = [((), 'xk'), (('e',), 'x0')]
    m = det([col(Rk, (0, 3, (1, 0)), tags), col(Rk, (1, 3, (1, 0)), tags)])
    if m != 16 * N * k0 ** 2 * s ** 2 * (s - N) * (k0 - 1) ** 2 * (2 * k0 - 3) * (2 * k0 - 1) ** 2 * (s - 2) * (s - 1) * (N + s - 3):
        return False
    # (4) types 1 and 2 die by level 2 (vertex only)
    for i, keys, want in ((1, [(0, 3, (0, 1)), (0, 3, (0, 2)), (1, 3, (0, 2))], -25920 * N * s ** 4 * (s - 2) * (s - 1) ** 4 * (N + s - 3) ** 2),
                          (2, [(0, 3, (0, 1)), (0, 3, (0, 2)), (1, 3, (0, 1))], 69120 * s ** 4 * (s - 2) ** 2 * (s - 1) ** 4 * (N + s - 2))):
        Gi = [(Pz.of(i), N, one, (0, 0), 'x0'), (Pz.of(i + 2), N - 1, one, (0, 1), 'x1'), (Pz.of(i + 4), N - 2, one, (0, 2), 'x2')]
        Ri = tw_rows(vertex, Gi, {(0, 1), (0, 2)}, R=1, ks=(3,))
        if det([col(Ri, key, [((), 'x0'), ((), 'x1'), ((), 'x2')]) for key in keys]) != want:
            return False
    # (5) k0 = 2: levels 2 and 3 with E = P^s + e2 Q^4 P^(s-2) + e3 Q^6 P^(s-3); extended unknowns
    F2 = vertex + [(Pz.of(4), s - 2, one, (0, 2), 'e2'), (Pz.of(6), s - 3, one, (0, 3), 'e3')]
    G2 = [(Pz(), N, one, (0, 0), 'x0'), (Pz.of(2), N - 1, one, (0, 1), 'x1'), (Pz.of(4), N - 2, one, (0, 2), 'x2'),
          (Pz.of(6), N - 3, one, (0, 3), 'x3')]
    R2 = tw_rows(F2, G2, {(0, 2), (0, 3)}, R=3, ks=(3,))
    ext = [(('e2',), 'x0'), (('e3',), 'x0'), ((), 'x1'), (('e2',), 'x1'), ((), 'x2'), ((), 'x3')]
    allowed = set(ext) | {((), 'x0')}
    if any(v != Pz() and t not in allowed for d in R2.values() for t, v in d.items()) or \
            any(v != Pz() for d in R2.values() for t, v in d.items() if t == ((), 'x0')):
        return False
    keys = [(0, 3, (0, 2)), (1, 3, (0, 2)), (0, 3, (0, 3)), (1, 3, (0, 3)), (2, 3, (0, 3)), (3, 3, (0, 3))]
    q = lambda N, s: 8 * N ** 2 * s - 11 * N ** 2 + 24 * N * s ** 2 - 87 * N * s + 72 * N + 16 * s ** 3 - 94 * s ** 2 + 177 * s - 105
    m6 = det([col(R2, key, ext) for key in keys])
    if m6 != -171992678400 * N ** 2 * s ** 10 * (s - N) ** 2 * (s - 2) * (s - 1) ** 4 * (N + s - 3) ** 2 * (N + s - 2) \
            * (N + 2 * s - 5) * (N + 3 * s - 6) * q(N, s) or not positive_shift(q, 1, 3):
        return False
    # type 1 at k0 = 2: unknowns (x0, e2 x0, x1, x2)
    G21 = [(one, N, one, (0, 0), 'x0'), (Pz.of(3), N - 1, one, (0, 1), 'x1'), (Pz.of(5), N - 2, one, (0, 2), 'x2')]
    R21 = tw_rows(F2[:2], G21, {(0, 1), (0, 2)}, R=2, ks=(3,))
    tags1 = [((), 'x0'), (('e2',), 'x0'), ((), 'x1'), ((), 'x2')]
    kq = lambda N, s: 8 * N ** 2 * s - 11 * N ** 2 + 8 * N * s ** 2 - 33 * N * s + 28 * N - 2 * s ** 2 + 7 * s - 5
    m4 = det([col(R21, key, tags1) for key in [(0, 3, (0, 1)), (0, 3, (0, 2)), (1, 3, (0, 2)), (2, 3, (0, 2))]])
    if m4 != 622080 * N * s ** 6 * (s - 2) * (s - 1) ** 4 * (N + s - 3) * (N + 2 * s - 4) * kq(N, s) or not positive_shift(kq, 1, 3):
        return False
    # type 2 at k0 = 2: the determinant is linear in the x0-column, and the e2 x0-column contributes 0
    G22 = [(Pz.of(2), N, one, (0, 0), 'x0'), (Pz.of(4), N - 1, one, (0, 1), 'x1'), (Pz.of(6), N - 2, one, (0, 2), 'x2')]
    R22 = tw_rows(F2[:2], G22, {(0, 1), (0, 2)}, R=1, ks=(3,))
    keys2 = [(0, 3, (0, 1)), (0, 3, (0, 2)), (1, 3, (0, 1))]
    if det([col(R22, key, [((), 'x0'), ((), 'x1'), ((), 'x2')]) for key in keys2]) != \
            69120 * s ** 4 * (s - 2) ** 2 * (s - 1) ** 4 * (N + s - 2) or \
            det([col(R22, key, [(('e2',), 'x0'), ((), 'x1'), ((), 'x2')]) for key in keys2]) != Pz():
        return False
    # (6) instances
    for h, N_ in [({(0, 3): F(1), (6, 0): F(1)}, 8), ({(0, 3): F(1), (4, 1): F(1)}, 8), ({(0, 3): F(1), (4, 1): F(2), (6, 0): F(-1), (0, 1): F(1)}, 8)]:
        if full_dim(TR.tidy(CT.tri(h, {2: F(1)})), N_) != 2:
            return False
    return True


def identities():
    return {'GG': grid_GG(), 'T3': grid_T3(), 'AE': grid_AE(), 'K1c': grid_K1c(), 'C2': grid_C2(),
            'NA': grid_NA(), 'TG': grid_TG(), 'GE': grid_GE(), 'BE': grid_BE(), 'NT': grid_NT(), 'NV': grid_NV(), 'NV32': grid_NV32(), 'K2U': grid_K2U(), 'LB': grid_LB(), 'K1P': grid_K1P(), 'TP': grid_TP(), 'TE': grid_TE(), 'CT': grid_CT()}


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
                       'threshold edges with deg w >= 3 (NT), edges below the threshold and flat lower terms (NV); '
                       'K2 and K1+K2 exact (K2U), linear b for higher shears (LB), K1\' with f = 3 (K1P), '
                       'perfect-power transverse tops and the extended K3 (TP), transverse tops l^k with k in {1, s} (TE), cubic-phase threshold edges (CT)'}


def main():
    try:
        cert = json.loads(open(sys.argv[1]).read()) if len(sys.argv) > 1 else None
        print(json.dumps(check(cert), indent=1))
    except (ValueError, KeyError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
