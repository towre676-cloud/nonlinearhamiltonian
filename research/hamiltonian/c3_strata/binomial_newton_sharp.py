"""All-degree finite windows justified by BINOMIAL_NEWTON_SHARP_THEOREM.md.

The bounds 44 and 28 are proved by chain endpoints, not inferred by this code.
Sparse rational operators are shared with the existing weighted engine.
"""
from fractions import Fraction as F
from weighted_cubic_form import transvectant, gate_system

FAMILIES = {
    "qp4": {"edge": (1, 4), "weights": (4, 5), "degree": 24, "bound": 44},
    "q2p3": {"edge": (2, 3), "weights": (3, 4), "degree": 18, "bound": 28},
}


def weight_monomials(family, weight):
    wq, wp = FAMILIES[family]["weights"]
    return [(i, (weight - wq*i)//wp) for i in range(weight//wq + 1)
            if (weight - wq*i) % wp == 0]


def window(family):
    return [m for w in range(FAMILIES[family]["bound"] + 1)
            for m in weight_monomials(family, w)]


def lower_monomials(family):
    return [m for w in range(FAMILIES[family]["degree"])
            for m in weight_monomials(family, w)]


def hamiltonian(family, coefficient=1, lower=None):
    c = F(coefficient)
    if not c:
        raise ValueError("the Newton-edge coefficient must be nonzero")
    data = FAMILIES[family]
    h = {(6, 0): F(1), data["edge"]: c}
    allowed = set(lower_monomials(family))
    for m, value in (lower or {}).items():
        if m not in allowed:
            raise ValueError("perturbation must have strictly lower weight")
        if F(value):
            h[m] = F(value)
    return h


def static_basis(family, coefficient=1):
    c = F(coefficient)
    h = hamiltonian(family, c)
    common = [{m: F(1)} for m in [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]]
    if family == "qp4":
        return common + [
            {(1, 2): F(1)},
            {(5, 0): F(1), (0, 4): c/2}, h,
            {(11, 0): F(1), (6, 4): 33*c/4, (1, 8): -33*c*c/112},
        ]
    return common + [
        {(4, 0): F(1), (0, 3): c/5},
        {(4, 1): F(1), (0, 4): -c/10}, h,
        {(8, 1): F(1)},
    ]


def classify(family, coefficient=1, lower=None):
    """Exact all-degree S0 basis and S^r (r>=1), for rational input."""
    h = hamiltonian(family, coefficient, lower)
    mons = window(family)
    kernel = gate_system(h, mons, 0).witnesses()
    return {
        "static_basis": [{m: c for m, c in zip(mons, v) if c} for v in kernel],
        "first_and_persistent_basis": [{(0, 0): F(1)}, h],
        "support_bound": FAMILIES[family]["bound"],
        "all_degree_dependency": "BINOMIAL_NEWTON_SHARP_THEOREM.md",
    }
