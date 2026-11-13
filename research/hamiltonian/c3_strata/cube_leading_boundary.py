"""Cube-leading boundary H = P^3 + B(q) P + C(q) in the chart P = p + q^2.

The chart substitution is not linear, so the flat transvectants of the
original coordinates (q, p) are transported explicitly: with p-derivative
d/dP and q-derivative delta = d/dq + 2 q d/dP one obtains the closed operators
returned by :func:`chart_operators`.  The flat engine of
``weighted_cubic_form`` is kept as the independent reference.
"""
from fractions import Fraction

import sympy as S

from weighted_cubic_form import _add, _mul, gate_system

q, P, p = S.symbols("q P p")
mu, lam, eps = S.symbols("mu lambda epsilon")

STATIC_BASIS_SOURCE = [
    "P**3 + mu*q**3",
    "-q*(-140*P**3 + 1260*P**2*q**2 - 1512*P*q**4 - 35*mu*q**3 + 216*q**6)/140",
    "-q**2*(-70*P**3 + 315*P**2*q**2 - 252*P*q**4 - 7*mu*q**3 + 27*q**6)/70",
    "P**2",
    "q*(5*P**2 - 20*P*q**2 + 6*q**4)/5",
    "q**2*(5*P**2 - 10*P*q**2 + 2*q**4)/5",
    "P",
    "-q*(-P + q**2)",
    "-q**2*(-2*P + q**2)/2",
    "1",
    "q",
    "q**2",
    "-(-5*P**4 - 20*P*mu*q**3 + 6*mu*q**5)/5",
    "(7*P**5 + 70*P**2*mu*q**3 - 84*P*mu*q**5 + 12*mu*q**7)/7",
    "-(-7*P**6 - 140*P**3*mu*q**3 + 378*P**2*mu*q**5 - 216*P*mu*q**7 - 7*mu**2*q**6 + 18*mu*q**9)/7"
]


def static_basis(mu_value=mu):
    """The 15 static partners of P^3 + mu q P + (quadratic in q), mu != 0."""
    env = {"q": q, "P": P, "mu": mu}
    return [S.sympify(text, locals=env).subs(mu, mu_value) for text in STATIC_BASIS_SOURCE]


def coefficients(B, C):
    b = [S.Poly(B, q).coeff_monomial(q**i) for i in range(4)]
    c = [S.Poly(C, q).coeff_monomial(q**i) for i in range(6)]
    return b, c


def gate_symbol(B, C):
    """E(q, P), characterised by T_3(H, g(P)) = 6 E d^3 g / dP^3."""
    b, c = coefficients(B, C)
    return b[3]*P + (b[1] + c[3]) + (2*b[2] + 4*c[4])*q + (3*b[3] + 10*c[5])*q**2


def chart_operators(B, C):
    """Transported D = T_1(H,-), T_3(H,-), T_5(H,-) acting on polynomials in (q, P)."""
    b, c = coefficients(B, C)
    beta = b[3] + c[5]
    E = gate_symbol(B, C)

    def D(G):
        return S.expand((S.diff(B, q)*P + S.diff(C, q))*S.diff(G, P) - (3*P**2 + B)*S.diff(G, q))

    def T3(G):
        return S.expand(-6*S.diff(G, q, 3) - 36*S.diff(G, q, 1, P, 1)
                        - 6*(6*P + b[2] + 3*b[3]*q)*S.diff(G, q, 1, P, 2)
                        + 6*E*S.diff(G, P, 3))

    def T5(G):
        return S.expand(-360*S.diff(G, q, 1, P, 4) + 120*beta*S.diff(G, P, 5))

    return D, T3, T5


def flat_transvectant(F, G, k):
    """The flat transvectant in the original coordinates (q, p), by definition."""
    return S.expand(sum((-1)**t*S.binomial(k, t)*S.diff(F, q, k - t, p, t)*S.diff(G, q, t, p, k - t)
                        for t in range(k + 1)))


def depth_matrix(B, C, basis, first, last):
    """Rows: coefficients of T_3, T_5 on D^i g for first <= i <= last; columns: basis."""
    D, T3, T5 = chart_operators(B, C)
    columns = []
    for g in basis:
        entry, current = {}, g
        for i in range(last + 1):
            if i >= first:
                for name, op in (("3", T3), ("5", T5)):
                    value = op(current)
                    if value != 0:
                        for mon, cf in S.Poly(value, q, P).terms():
                            entry[(i, name) + mon] = cf
            if i < last:
                current = D(current)
        columns.append(entry)
    rows = sorted({r for col in columns for r in col}, key=str)
    return S.Matrix([[col.get(r, 0) for col in columns] for r in rows])


def chart_window(max_p_degree=6, weight=12, q_divisible=False):
    """Monomials q^i P^k of weight i + 2k <= weight in the chart."""
    start = 1 if q_divisible else 0
    return [q**i*P**k for k in range(max_p_degree + 1) for i in range(start, weight - 2*k + 1)]


def static_window_basis(B, C, monomials):
    """Exact basis of the static elements supported on the given chart monomials."""
    _, T3, T5 = chart_operators(B, C)
    unknowns = S.symbols("x0:%d" % len(monomials))
    G = sum(c*m for c, m in zip(unknowns, monomials))
    equations = S.Poly(T3(G), q, P).coeffs() + S.Poly(T5(G), q, P).coeffs()
    matrix, _ = S.linear_eq_to_matrix(equations, unknowns)
    return [S.expand(S.cancel(sum(c*m for c, m in zip(v, monomials)))) for v in matrix.nullspace()]


# Flat exact engine in the original coordinates -------------------------------

def reduced_hamiltonian(b=(0, 0, 0, 0), c=(0, 0, 0, 0, 0, 0)):
    """P^3 + B(q) P + C(q) as a dictionary polynomial in the original (q, p)."""
    terms = {(0, 3): Fraction(1)}
    for i, v in enumerate(b):
        if v:
            terms[(i, 1)] = Fraction(v)
    for i, v in enumerate(c):
        if v:
            terms[(i, 0)] = terms.get((i, 0), Fraction(0)) + Fraction(v)
    out = {}
    for (i, k), cf in terms.items():
        t = {(i, 0): cf}
        for _ in range(k):
            t = _mul(t, {(0, 1): Fraction(1), (2, 0): Fraction(1)})
        out = _add(out, t)
    return out


def window(weight):
    return [(i, j) for j in range(weight//2 + 1) for i in range(weight - 2*j + 1)]


def window_dimensions(h, weight, depths=(0, 1, 2, 3)):
    basis = window(weight)
    return [len(gate_system(h, basis, r).witnesses()) for r in depths]
