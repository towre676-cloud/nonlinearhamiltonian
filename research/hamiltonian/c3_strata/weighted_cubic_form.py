"""Exact engine for H = q^6 + a q^4 p + b q^2 p^2 + x p^3 + R, wt(R) < 6.

Weights are wt(q)=1, wt(p)=2.  The transvectant T_k lowers weight by 3k, so
the Moyal gates of the weighted-homogeneous leading form are graded and each
weight is a finite exact observation problem (see `exact_observation.py`).
The all-degree statements are in WEIGHTED_CUBIC_FORM_THEOREM.md; this module
computes, it does not extrapolate.
"""
from __future__ import annotations
from fractions import Fraction as Fr
from math import comb
from exact_observation import ObservationSystem, kernel as _kernel

LOWER = [(i, j) for j in range(3) for i in range(6 - 2 * j) if i + 2 * j <= 5]


def _ff(n, k):
    r = 1
    for t in range(k):
        r *= n - t
    return r


def _d(f, a, b):
    return {(i - a, j - b): c * _ff(i, a) * _ff(j, b) for (i, j), c in f.items() if i >= a and j >= b}


def _mul(f, g):
    out = {}
    for (i, j), c in f.items():
        for (k, l), e in g.items():
            v = out.get((i + k, j + l), 0) + c * e
            if v == 0:
                out.pop((i + k, j + l), None)
            else:
                out[(i + k, j + l)] = v
    return out


def _add(f, g, s=1):
    out = dict(f)
    for k, e in g.items():
        v = out.get(k, 0) + s * e
        if v == 0:
            out.pop(k, None)
        else:
            out[k] = v
    return out


def transvectant(h, g, k):
    out = {}
    for j in range(k + 1):
        out = _add(out, _mul(_d(h, k - j, j), _d(g, j, k - j)), (-1) ** j * comb(k, j))
    return out


def hamiltonian(a, b, x, lower=None):
    h = {(6, 0): Fr(1)}
    for key, c in (((4, 1), a), ((2, 2), b), ((0, 3), x)):
        if Fr(c) != 0:
            h[key] = Fr(c)
    for key, c in (lower or {}).items():
        if key not in LOWER:
            raise ValueError("lower term %r does not have weight < 6" % (key,))
        if Fr(c) != 0:
            h[key] = Fr(c)
    return h


def weight_basis(w):
    return [(w - 2 * j, j) for j in range(w // 2 + 1)]


def window_basis(max_weight):
    return [m for w in range(max_weight + 1) for m in weight_basis(w)]


def gate_system(h, basis, depth):
    """Observation system whose rows are the coefficients of T3, T5 on D^i G, i <= depth."""
    cols = []
    for m in basis:
        ent, cur = {}, {m: Fr(1)}
        for i in range(depth + 1):
            for k in (3, 5):
                for mono, c in transvectant(h, cur, k).items():
                    ent[(i, k) + mono] = c
            if i < depth:
                cur = transvectant(h, cur, 1)
        cols.append(ent)
    labels = sorted({r for c in cols for r in c})
    return ObservationSystem(basis, [(lab, 1, [c.get(lab, Fr(0)) for c in cols]) for lab in labels])


def refinement(h, depth, max_weight=12):
    """Kernel of the depth-`depth` gates on all monomials of weight <= max_weight."""
    basis = window_basis(max_weight)
    return basis, gate_system(h, basis, depth).witnesses()


def dims(a, b, x, lower=None, depths=(0, 1, 2), max_weight=12):
    h = hamiltonian(a, b, x, lower)
    return [len(refinement(h, r, max_weight)[1]) for r in depths]


def is_cube(a, b, x):
    a, b, x = Fr(a), Fr(b), Fr(x)
    return 3 * b == a * a and 27 * x == a ** 3


def invariants(a, b, x):
    """The four exceptional polynomials of the leading form (weights 1, 3, 4, 8)."""
    a, b, x = Fr(a), Fr(b), Fr(x)
    return {
        "alpha": a,
        "E12": 4 * a ** 3 - 9 * a * b - 27 * x,
        "Delta_w": b * b - 3 * a * x,
        "Gamma2": 12 * a * a * x * x + 4 * a * b * b * x - b ** 4 - 45 * b * x * x,
    }


def predicted_dims(a, b, x):
    """Theorem 2 for the weighted-homogeneous form, x != 0, not a cube, off the two weight-4 points."""
    inv = invariants(a, b, x)
    s0 = 14 + int(inv["alpha"] == 0) + int(inv["E12"] == 0)
    s1 = 2 + int(inv["Delta_w"] == 0) + int(inv["Gamma2"] == 0)
    return [s0, s1, 2]


def q_survival_conditions(h):
    """Coefficients of T3(H, H_p), T5(H, H_p): q lies in S^1(H) iff all vanish."""
    hp = _d(h, 0, 1)
    out = {}
    for k in (3, 5):
        for mono, c in transvectant(h, hp, k).items():
            out[(k,) + mono] = c
    return out
