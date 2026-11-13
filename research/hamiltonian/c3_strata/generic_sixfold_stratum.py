"""Generic stratum of the sixfold-leading family: H = q^6 + R, deg R <= 5, p^5-coefficient y != 0.

With wt(q)=5, wt(p)=6 the leading form is q^6 + y p^5 and every other monomial
of degree <= 5 has lower weight.  By GENERIC_SIXFOLD_STRATUM_THEOREM.md every
static partner has weight <= 30, hence ordinary degree <= 6, so the degree-6
window below is exact for every polynomial degree.
"""
from __future__ import annotations
from fractions import Fraction as Fr
from weighted_cubic_form import gate_system

LOWER = [(i, j) for i in range(6) for j in range(6) if i + j <= 5 and (i, j) != (0, 5)]
WINDOW = [(i, dd - i) for dd in range(7) for i in range(dd + 1)]


def hamiltonian(y, lower=None):
    if Fr(y) == 0:
        raise ValueError("the stratum requires a nonzero p^5 coefficient")
    h = {(6, 0): Fr(1), (0, 5): Fr(y)}
    for key, c in (lower or {}).items():
        if key not in LOWER:
            raise ValueError("not a lower monomial: %r" % (key,))
        if Fr(c) != 0:
            h[key] = Fr(c)
    return h


def refinement(h, depth):
    """Exact basis of S^depth(H) in all of Q[q,p]."""
    return WINDOW, gate_system(h, WINDOW, depth).witnesses()


def dims(h):
    return [len(refinement(h, r)[1]) for r in (0, 1, 2)]
