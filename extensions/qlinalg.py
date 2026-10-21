"""Exact rational linear algebra shared by the machinery *compilers* (not by checkers).

Matrices are lists of rows of fractions.Fraction. Every function is exact; there is
no tolerance anywhere. Independent checkers deliberately carry their own arithmetic.
"""
from __future__ import annotations
from fractions import Fraction as F


def rat(x):
    if type(x) not in (int, str) and not isinstance(x, F):
        raise ValueError('use exact integers or rational strings, never floats/bools')
    return F(x)


def mat(rows, cols, nrows=None):
    if not isinstance(rows, list) or (nrows is not None and len(rows) != nrows):
        raise ValueError('wrong matrix row count')
    if any(not isinstance(r, list) or len(r) != cols for r in rows):
        raise ValueError('wrong matrix column count')
    return [[rat(x) for x in r] for r in rows]


def strs(rows):
    return [[str(x) for x in r] for r in rows]


def vstr(v):
    return [str(x) for x in v]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def zeros(r, c):
    return [[F(0)] * c for _ in range(r)]


def transpose(a, cols=None):
    if not a:
        return [[] for _ in range(cols or 0)]
    return [list(c) for c in zip(*a)]


def mul(a, b, cols=None):
    c = len(b[0]) if b else (cols or 0)
    return [[sum((x * b[k][j] for k, x in enumerate(r)), F(0)) for j in range(c)] for r in a]


def add(a, b, s=1):
    return [[x + s * y for x, y in zip(r, t)] for r, t in zip(a, b)]


def scale(a, c):
    return [[c * x for x in r] for r in a]


def row_times(row, a):
    return [sum((row[i] * a[i][j] for i in range(len(row))), F(0)) for j in range(len(a[0]))] if a else []


def dot(u, v):
    return sum((x * y for x, y in zip(u, v)), F(0))


def rref(rows, cols):
    a = [r[:] for r in rows]
    piv = []
    for c in range(cols):
        p = next((i for i in range(len(piv), len(a)) if a[i][c]), None)
        if p is None:
            continue
        k = len(piv)
        a[k], a[p] = a[p], a[k]
        v = a[k][c]
        a[k] = [x / v for x in a[k]]
        for i in range(len(a)):
            if i != k and a[i][c]:
                v = a[i][c]
                a[i] = [x - v * y for x, y in zip(a[i], a[k])]
        piv.append(c)
        if len(piv) == len(a):
            break
    return a, piv


def rank(rows, cols):
    return len(rref(rows, cols)[1])


def null_basis(rows, n):
    red, piv = rref(rows, n)
    out = []
    for free in range(n):
        if free not in piv:
            v = [F(0)] * n
            v[free] = F(1)
            for i, p in enumerate(piv):
                v[p] = -red[i][free]
            out.append(v)
    return out


def left_solve(rows, target, n):
    """Return c with c * rows = target (free coefficients zero), or None."""
    m = len(rows)
    aug = [[rows[j][i] for j in range(m)] + [target[i]] for i in range(n)]
    red, piv = rref(aug, m + 1)
    if m in piv:
        return None
    c = [F(0)] * m
    for i, p in enumerate(piv):
        c[p] = red[i][-1]
    assert row_times(c, rows) == list(target) if rows else not any(target)
    return c


def inverse(a):
    n = len(a)
    red, piv = rref([r + e for r, e in zip(a, eye(n))], 2 * n)
    if piv[:n] != list(range(n)):
        raise ValueError('singular matrix')
    return [r[n:] for r in red]


def ldl_psd(m):
    """Exact symmetric PSD decision.

    Returns ('psd', L, d) with M = L diag(d) L^T, L unit lower triangular up to a
    permutation-free elimination, d >= 0; or ('not_psd', v) with v^T M v < 0.
    """
    n = len(m)
    if any(m[i][j] != m[j][i] for i in range(n) for j in range(n)):
        raise ValueError('matrix is not symmetric')
    s = [r[:] for r in m]          # running Schur complement (in place)
    lower = eye(n)                  # M = lower * S * lower^T throughout
    d = [F(0)] * n
    for k in range(n):
        if s[k][k] < 0:
            return ('not_psd', _pull_back(lower, [F(int(i == k)) for i in range(n)]))
        if s[k][k] == 0:
            j = next((j for j in range(k + 1, n) if s[k][j]), None)
            if j is not None:
                # w = t e_k + e_j gives w^T S w = 2 t S_kj + S_jj; choose it equal to -1.
                w = [F(0)] * n
                w[k], w[j] = (-1 - s[j][j]) / (2 * s[k][j]), F(1)
                return ('not_psd', _pull_back(lower, w))
            continue
        d[k] = s[k][k]
        for i in range(k + 1, n):
            f = s[i][k] / s[k][k]
            if f:
                lower[i][k] = f
                for j in range(k, n):
                    s[i][j] -= f * s[k][j]
        for i in range(k + 1, n):
            s[k][i] = F(0)
            # keep symmetry of the trailing block
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                s[j][i] = s[i][j]
    return ('psd', lower, d)


def _pull_back(lower, w):
    """Solve lower^T v = w, so v^T M v = w^T S w."""
    n = len(w)
    v = [F(0)] * n
    for i in reversed(range(n)):
        v[i] = w[i] - sum((lower[j][i] * v[j] for j in range(i + 1, n)), F(0))
    return v


def quad(m, v):
    return dot(v, [dot(r, v) for r in m])
