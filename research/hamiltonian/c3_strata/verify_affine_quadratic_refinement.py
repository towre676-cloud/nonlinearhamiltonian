"""Exact symbolic replay for the affine quadratic-momentum sextic classification."""
from math import comb

import sympy as s

q, p = s.symbols("q p")
coeffs = s.symbols("c0:7")
c6 = coeffs[-1]
a0, a1, b1, u, v = s.symbols("a0 a1 b1 u v")
h = sum(c * q**j for j, c in enumerate(coeffs))
A = a0 + a1*q
# Translation by b0/b1 centers B at its unique root when b1 != 0.
H = h + A*p + b1*q*p**2


def gate(F, G, order):
    return s.expand(sum(
        (-1)**k * comb(order, k) * s.diff(F, q, order-k, p, k)
        * s.diff(G, q, k, p, order-k)
        for k in range(order+1)
    ))


def orbit(F, G, steps):
    for _ in range(steps+1):
        yield gate(F, G, 3), gate(F, G, 5)
        G = gate(F, G, 1)


def coefficient(expr, q_degree, p_degree=0):
    return s.expand(expr).coeff(p, p_degree).coeff(q, q_degree)


g3 = u + v*q
g1 = s.integrate(s.integrate(-s.diff(h, q, 3)*g3/b1, q), q)
DG = gate(H, g3*p**3 + g1*p, 1)
residual = s.expand(s.diff(DG.coeff(p, 2), q, 2)
                    + 2*s.diff(h, q, 3)*DG.coeff(p, 4)/b1)
assert coefficient(residual, 4) == 2100*v*c6
assert coefficient(residual.subs(v, 0), 3) == 2160*u*c6

E = b1*p**2 + 2*sum(j*coeffs[j]*q**(j-1)/s.Integer(j-1) for j in range(2, 7))
for G in (s.S.One, H):
    assert list(orbit(H, G, 3)) == [(0, 0)]*4

for G, p_degree, q_degree, pivot in (
    (E, 1, 3, 51840*b1**3*c6),
    (q*p, 0, 4, -15120*b1**2*c6),
    (p, 0, 3, -4320*b1**2*c6),
):
    initial, first, second = orbit(H, G, 2)
    assert initial == first == (0, 0)
    third, fifth = second
    assert fifth == 0
    assert s.degree(third, p) == p_degree
    assert s.degree(third.coeff(p, p_degree), q) == q_degree
    assert coefficient(third, q_degree, p_degree) == pivot

initial, first, second, last = orbit(H, q, 3)
assert initial == first == second == (0, 0)
assert coefficient(last[0], 4) == 30240*b1**3*c6

F = q**6 + q*p**2
witness = p**2 + s.Rational(12, 5)*q**5
assert gate(F, witness, 1) == 2*p**3 - 12*q**5*p
assert list(orbit(F, witness, 2)) == [(0, 0), (0, 0), (51840*p*q**3, 0)]
print("PASS affine quadratic sextic obstructions and degree-five witness")
