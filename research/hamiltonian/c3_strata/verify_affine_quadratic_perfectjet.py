"""Run with Python 3 and SymPy 1.14: python verify.py /path/to/PerfectJet/src/perfectjet/moyal.py."""
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

import sympy as s

q, p = s.symbols("q p")
h_coeffs = s.symbols("c0:7")
a0, a1, b0, b1 = s.symbols("a0 a1 b0 b1")
params = (*h_coeffs, a0, a1, b0, b1)
h = sum(c * q**j for j, c in enumerate(h_coeffs))
A, B = a0 + a1*q, b0 + b1*q
H = h + A*p + B*p**2


def transvectant(F, G, n):
    return s.expand(sum(
        (-1)**k * comb(n, k) * s.diff(F, q, n-k, p, k)
        * s.diff(G, q, k, p, n-k) for k in range(n+1)
    ))


def load_engine(path):
    spec = importlib.util.spec_from_file_location("pr38_perfectjet_moyal", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def verify(engine):
    def pack(expr, spectators):
        n = 1 + len(spectators)
        return engine.PolyH(n, {
            (0, (powers[0], *powers[2:], powers[1], *((0,) * (n-1)))): Fraction(coeff)
            for powers, coeff in s.Poly(expr, q, p, *spectators).terms()
        })

    def unpack(poly, order, spectators):
        n = 1 + len(spectators)
        terms = []
        for (hp, exps), coeff in poly.terms.items():
            if hp == order:
                assert coeff.im == 0 and not any(exps[n+1:])
                powers = (exps[0], exps[n], *exps[1:n])
                terms.append(s.Rational(coeff.re) * s.prod(
                    x**degree for x, degree in zip((q, p, *spectators), powers)
                ))
        return s.Add(*terms)

    def compare(F, G, spectators=()):
        bracket = engine.scaled_moyal_bracket(pack(F, spectators), pack(G, spectators))
        assert all(hp in (0, 2, 4) for hp, _ in bracket.terms)
        actual = tuple(unpack(bracket, hp, spectators)*scale
                       for hp, scale in [(0, 1), (2, -24), (4, 1920)])
        assert actual == tuple(transvectant(F, G, n) for n in (1, 3, 5))
        return actual

    probe = (1+q+q**3+q**8)*(1+p+p**2+p**4+p**7)
    _, third, fifth = compare(H, probe, params)
    assert s.expand(third - s.diff(h, q, 3)*s.diff(probe, p, 3)
                    - 6*b1*s.diff(probe, q, 2, p)) == 0
    assert s.expand(fifth - s.diff(h, q, 5)*s.diff(probe, p, 5)) == 0

    def coefficient(expr, q_degree, p_degree=0):
        return s.expand(expr).coeff(p, p_degree).coeff(q, q_degree)

    print("symbolic gate comparison passed", file=sys.stderr)
    rows = {}
    for G, iterations in [(s.S.One, 3), (q, 3), (p, 2), (q*p, 2), (H, 3)]:
        label = "H" if G == H else str(G)
        for k in range(iterations+1):
            D, t3, t5 = compare(H, G, params)
            if label in ("1", "H") or k < iterations:
                assert t3 == t5 == 0
            rows[label, k] = (t3, t5)
            G = D

    c6 = h_coeffs[-1]
    obstructions = [(("p*q", 2), 4, -15120*b1**2*c6),
                    (("p", 2), 3, -4320*b1**2*c6),
                    (("q", 3), 4, 30240*b1**3*c6)]
    for key, degree, expected in obstructions:
        third, fifth = rows[key]
        assert fifth == 0 and coefficient(third, degree) == expected
        assert all(coefficient(third, j) == 0 for j in range(degree+1, 10))
        assert s.degree(third, p) == 0

    print("symbolic original pivots passed", file=sys.stderr)
    # Translate q so B=b1*q. The translation is symplectic.
    centered = H.subs(b0, 0)
    extra = b1*p**2 + 2*sum(j*h_coeffs[j]*q**(j-1)/s.Integer(j-1)
                              for j in range(2, 7))
    G = extra
    for k in range(3):
        G, t3, t5 = compare(centered, G, params)
        assert t5 == 0
        if k < 2:
            assert t3 == 0
        else:
            assert coefficient(t3, 3, 1) == 51840*b1**3*c6
            assert s.degree(t3, p) == 1

    u, v = s.symbols("u v")
    g3 = u + v*q
    g1 = s.integrate(s.integrate(-s.diff(h, q, 3)*g3/b1, q), q)
    D = transvectant(centered, g3*p**3 + g1*p, 1)
    static_residual = s.expand(s.diff(D.coeff(p, 2), q, 2)
                               + 2*s.diff(h, q, 3)*D.coeff(p, 4)/b1)
    assert static_residual.coeff(q, 4) == 2100*v*c6
    assert static_residual.subs(v, 0).coeff(q, 3) == 2160*u*c6

    counterexample = p**2 + s.Rational(12, 5)*q**5
    F = q**6 + q*p**2
    D, t3, t5 = compare(F, counterexample)
    assert (t3, t5) == (0, 0)
    assert D == 2*p**3 - 12*q**5*p
    D2, t3, t5 = compare(F, D)
    assert (t3, t5) == (0, 0)
    assert compare(F, D2)[1:] == (51840*p*q**3, 0)

    print("symbolic extra pivot and minimal witness passed", file=sys.stderr)
    def dimensions(F, degree):
        columns = []
        for i in range(degree+1):
            for j in range(degree+1-i):
                G = q**i*p**j
                column = {}
                for k in range(4):
                    G, t3, t5 = compare(F, G)
                    for n, expr in [(3, t3), (5, t5)]:
                        for powers, value in s.Poly(expr, q, p).terms():
                            if value:
                                column[k, n, powers] = value
                columns.append(column)
        keys = sorted(set().union(*columns))
        return [len(columns)-s.Matrix([
            [column.get(key, 0) for column in columns] for key in keys if key[0] <= k
        ]).rank() for k in range(4)]

    cases = {
        "generic": 2*q**6-3*q**5+7*q**4-q**3+q**2-8*q+9+(2-3*q)*p+(5+2*q)*p**2,
        "A_and_B_intercept_zero": q**6+q*p**2,
        "A_constant": -q**6+q**2+2*p+(-3+q)*p**2,
        "A_intercept_zero": q**6+q**3-q*p+(1-q)*p**2,
        "B_constant": q**6+(1+q)*p+2*p**2,
        "B_zero": q**6+(1+q)*p,
        "A_and_B_zero": q**6,
    }
    ranks = {name: dimensions(F, 8) for name, F in cases.items()}
    for name in list(cases)[:4]:
        assert ranks[name] == [17, 6, 3, 2]
    for name in list(cases)[4:]:
        assert ranks[name][0] == 24
    return {
        "total_degree": 8,
        "dimensions_S0_to_S3": ranks,
        "symbolic_obstructions": {str(key): str(expected) for key, _, expected in obstructions},
        "extra_p_q3_obstruction": "51840*b1**3*c6",
        "counterexample": str(counterexample),
        "engine_sha256": hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(verify(load_engine(sys.argv[1])), indent=2))
