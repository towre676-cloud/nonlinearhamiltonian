#!/usr/bin/env python3
"""Exact check of the rms-emittance kick identity and its 4D Schur form.

For a centered cloud with a = E[x^2], b = E[xp], c = E[p^2], eps^2 = ac - b^2,
a thin kick p -> p + h F (F centered too) gives

    (eps+)^2 = eps^2 + 2 h a E[u g] + h^2 a E[g^2],
    u = p - (b/a) x,   g = F - (E[xF]/a) x,

and |eps+ - eps| <= |h| sqrt(a E[g^2]), because eps = sqrt(a)|u| and
eps+ = sqrt(a)|u + h g| in L2 of the cloud.

In 4D with z = (x, p), x and p in R^2 and Sigma = [[A, B], [B^T, C]], a kick
p -> p + h F leaves A fixed, so det Sigma+ = det A * det(S+), where
S = C - B^T A^-1 B = Cov(U), U = p - B^T A^-1 x, and U+ = U + h G with
G = F - Cov(F, x) A^-1 x. Hence
    det Sigma+ = det A * det(S + h (Cov(U,G) + Cov(G,U)) + h^2 Cov(G)).

Everything is checked with Fractions on random rational clouds, including
uncentered input centered by the checker. Standard algebra; recorded as an
executable check of the formulas quoted in the beam memo.
"""
from fractions import Fraction as Fr
import json
import random


def mean(v):
    return sum(v, Fr(0)) / len(v)


def center(v):
    m = mean(v)
    return [t - m for t in v]


def E(a, b):
    return mean([s * t for s, t in zip(a, b)])


def det(M):
    M = [row[:] for row in M]
    n, d = len(M), Fr(1)
    for i in range(n):
        piv = next((r for r in range(i, n) if M[r][i] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != i:
            M[i], M[piv] = M[piv], M[i]
            d = -d
        d *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] -= f * M[i][c]
    return d


def inv2(A):
    (p, q), (r, s) = A
    D = p * s - q * r
    return [[s / D, -q / D], [-r / D, p / D]]


def cov(X, Y):
    return [[E(x, y) for y in Y] for x in X]


def check_2d(rng):
    n = rng.randint(3, 9)
    x = center([Fr(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)])
    p = center([Fr(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)])
    if E(x, x) == 0:
        return False
    k2, k3 = Fr(rng.randint(-3, 3)), Fr(rng.randint(-3, 3), 2)
    F = center([k2 * t * t + k3 * t ** 3 + Fr(rng.randint(-2, 2)) for t in x])
    h = Fr(rng.randint(-5, 5), rng.randint(1, 5))
    a, b, c = E(x, x), E(x, p), E(p, p)
    e2 = a * c - b * b
    q = [s + h * f for s, f in zip(p, F)]
    e2p = E(x, x) * E(q, q) - E(x, q) ** 2
    u = [s - b / a * t for s, t in zip(p, x)]
    g = [f - E(x, F) / a * t for f, t in zip(F, x)]
    assert e2p == e2 + 2 * h * a * E(u, g) + h * h * a * E(g, g)
    # |eps+ - eps| <= |h| sqrt(a E[g^2])  <=>  e2p + e2 - R <= 2 sqrt(e2 e2p)
    R = h * h * a * E(g, g)
    L = e2p + e2 - R
    assert L <= 0 or L * L <= 4 * e2 * e2p
    return True


def check_4d(rng):
    n = rng.randint(5, 10)
    cols = [center([Fr(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(n)])
            for _ in range(4)]
    x, y, px, py = cols
    X, P = [x, y], [px, py]
    A = cov(X, X)
    if det(A) == 0:
        return False
    # sextupole-like kick plus an arbitrary nonlinear term
    s, o = Fr(rng.randint(-3, 3)), Fr(rng.randint(-2, 2), 3)
    Fx = center([s * (u * u - v * v) + o * u ** 3 for u, v in zip(x, y)])
    Fy = center([-2 * s * u * v + o * v ** 3 for u, v in zip(x, y)])
    F = [Fx, Fy]
    h = Fr(rng.randint(-4, 4), rng.randint(1, 4))
    Ai = inv2(A)
    B = cov(X, P)
    M = [[sum(B[k][i] * Ai[k][j] for k in range(2)) for j in range(2)] for i in range(2)]  # B^T A^-1
    U = [[P[i][m] - sum(M[i][j] * X[j][m] for j in range(2)) for m in range(n)] for i in range(2)]
    CFX = cov(F, X)
    N = [[sum(CFX[i][k] * Ai[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    G = [[F[i][m] - sum(N[i][j] * X[j][m] for j in range(2)) for m in range(n)] for i in range(2)]
    Sig = cov(X + P, X + P)
    S = cov(U, U)
    assert det(Sig) == det(A) * det(S)                       # Schur complement
    Pp = [[P[i][m] + h * F[i][m] for m in range(n)] for i in range(2)]
    Sigp = cov(X + Pp, X + Pp)
    CUG, CGG = cov(U, G), cov(G, G)
    Sp = [[S[i][j] + h * (CUG[i][j] + CUG[j][i]) + h * h * CGG[i][j] for j in range(2)]
          for i in range(2)]
    assert det(Sigp) == det(A) * det(Sp)
    Up = [[U[i][m] + h * G[i][m] for m in range(n)] for i in range(2)]
    assert cov(Up, Up) == Sp
    # G is uncorrelated with x, which is what makes A unchanged and the split exact
    assert cov(G, X) == [[0, 0], [0, 0]] and cov(U, X) == [[0, 0], [0, 0]]
    return True


def main(trials=400, seed=1):
    rng = random.Random(seed)
    n2 = sum(check_2d(rng) for _ in range(trials))
    n4 = sum(check_4d(rng) for _ in range(trials))
    print(json.dumps({'status': 'passed', 'exact_2d_clouds': n2, 'exact_4d_schur_clouds': n4,
                      'seed': seed, 'trials': trials}))


if __name__ == '__main__':
    main()
