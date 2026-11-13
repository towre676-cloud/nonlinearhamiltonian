"""Exact engine for the quartic Newton edge H = q^6 + g q^3 p^2 + y p^4 + R.

Weights wt(q)=2, wt(p)=3, so the leading form has weight 12 and wt(R) < 12.
Same observation engine and gate construction as `weighted_cubic_form.py`;
only the grading differs.  Statements: Theorem 5 of WEIGHTED_CUBIC_FORM_THEOREM.md.
"""
from __future__ import annotations
from fractions import Fraction as Fr
from weighted_cubic_form import gate_system

TAIL_BOUND = 33  # no static partner of the leading form in weight >= 33 (>= 18 if g = 0)


def weight_basis(w):
    return [((w - 3 * j) // 2, j) for j in range(w // 3 + 1) if (w - 3 * j) % 2 == 0]


def hamiltonian(g, y, lower=None):
    h = {(6, 0): Fr(1)}
    for key, c in (((3, 2), g), ((0, 4), y)):
        if Fr(c) != 0:
            h[key] = Fr(c)
    for (i, j), c in (lower or {}).items():
        if 2 * i + 3 * j >= 12 or i + j > 5:
            raise ValueError("lower term q^%d p^%d must have weight < 12 and degree <= 5" % (i, j))
        if Fr(c) != 0:
            h[(i, j)] = Fr(c)
    return h


def dims(g, y, lower=None, depths=(0, 1, 2), max_weight=TAIL_BOUND + 1):
    h = hamiltonian(g, y, lower)
    basis = [m for w in range(max_weight + 1) for m in weight_basis(w)]
    return [len(gate_system(h, basis, r).witnesses()) for r in depths]


def predicted_dims(g, y):
    """Theorem 5 for the leading form, y != 0."""
    g, y = Fr(g), Fr(y)
    s0 = 10 + 2 * int(g == 0) + int(3 * g * g + 80 * y == 0) + int(3 * g * g == 32 * y) \
        + int(g * g + 6 * y == 0) + int(g * g == 24 * y)
    return [s0, 2 + int(g * g + 40 * y == 0), 2]
