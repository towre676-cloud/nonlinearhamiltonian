"""Symbolic audit of the displayed identities in QUADRATIC_SIXFOLD_THEOREM.md.

This is not a formalization.  It checks, with SymPy, each coefficient
identity that the hand proofs rely on, with symbolic coefficients for f, b,
c and with arbitrary *functions* of q as the coefficients of the partner G,
so the checks are not restricted to a degree in q.  The degree in the
complement is symbolic where SymPy allows it and otherwise ranges over
2..7.  The contractions are expanded from their definition and share no
code with the star engine or with the verifiers.

    python research/hamiltonian/c3_strata/audit_quadratic_sixfold_steps.py
"""
from math import comb
import json

import sympy as sp

x, y, P = sp.symbols("x y P")
n, d = sp.symbols("n d", positive=True)
gamma = sp.Symbol("gamma")


def T(k, H, G, u=x, v=y):
    return sum((-1) ** j * comb(k, j) * sp.diff(H, u, k - j, v, j) * sp.diff(G, u, j, v, k - j)
               for j in range(k + 1))


def zero(expr):
    return sp.simplify(sp.expand(expr)) == 0


def poly(name, degree):
    return sum(sp.Symbol(f"{name}{i}") * x**i for i in range(degree + 1))


def run():
    done = []
    f, b = poly("f", 6), poly("b", 4)
    F = f - b**2 / 4
    a = [sp.Function(f"a{j}")(x) for j in range(8)]

    # Lemma 1: gates and derivation in the shifted chart, P-degree <= 6.
    Gc = sum(a[j] * P**j for j in range(7))
    H = y**2 + b * y + f
    Gy = Gc.subs(P, y + b / 2)
    to_y = lambda expr: expr.subs(P, y + b / 2)
    t3 = (sp.diff(F, x, 3) + sp.diff(b, x, 3) * P) * sp.diff(Gc, P, 3) \
        - 3 * sp.diff(b, x, 2) * sp.diff(Gc, x, 1, P, 2)
    t5 = (sp.diff(f, x, 5) - sp.Rational(5, 2) * sp.diff(b, x, 4) * sp.diff(b, x)) \
        * sp.diff(Gc, P, 5) - 5 * sp.diff(b, x, 4) * sp.diff(Gc, x, 1, P, 4)
    dh = sp.diff(F, x) * sp.diff(Gc, P) - 2 * P * sp.diff(Gc, x)
    assert zero(T(3, H, Gy).doit() - to_y(t3).doit())
    assert zero(T(5, H, Gy).doit() - to_y(t5).doit())
    assert zero(T(1, H, Gy).doit() - to_y(dh).doit())
    assert zero(T(7, H, Gy).doit())
    done.append("Lemma 1: (3), (4), (5) and vanishing of T7")

    # (8), (9): top two coefficients of (4) and of the derivation, d = 2..7.
    g, g1 = a[0], a[1]
    for dd in range(2, 8):
        G = g * P**dd + g1 * P ** (dd - 1) + sum(a[j + 2] * P**j for j in range(max(dd - 1, 0)))
        t3 = sp.expand((sp.diff(F, x, 3) + sp.diff(b, x, 3) * P) * sp.diff(G, P, 3)
                       - 3 * sp.diff(b, x, 2) * sp.diff(G, x, 1, P, 2))
        top = dd * (dd - 1) * ((dd - 2) * sp.diff(b, x, 3) * g - 3 * sp.diff(b, x, 2) * sp.diff(g, x))
        assert zero(t3.coeff(P, dd - 2) - top)
        if dd >= 3:
            # with g constant (substituted as 1), coefficient of P^(d-3)
            t3c = sp.expand(t3.subs(g, 1).doit())
            nxt = (dd - 1) * (dd - 2) * (dd * sp.diff(F, x, 3) + (dd - 3) * sp.diff(b, x, 3) * g1
                                         - 3 * sp.diff(b, x, 2) * sp.diff(g1, x))
            assert zero(t3c.coeff(P, dd - 3) - nxt)
        dG = sp.expand(sp.diff(F, x) * sp.diff(G, P) - 2 * P * sp.diff(G, x))
        assert zero(dG.coeff(P, dd + 1) + 2 * sp.diff(g, x))
        assert zero(dG.subs(g, 1).doit().coeff(P, dd) + 2 * sp.diff(g1, x))
    done.append("Lemma 3: (8), (9) and the top coefficients of D_H G, d = 2..7")

    # (6), (7) and the P^2 gate of Lemma 2.
    A, B, Cc = a[2], a[3], a[4]
    G = A + B * P + Cc * P**2
    dG = sp.expand(sp.diff(F, x) * sp.diff(G, P) - 2 * P * sp.diff(G, x))
    want = sp.diff(F, x) * B + (2 * Cc * sp.diff(F, x) - 2 * sp.diff(A, x)) * P \
        - 2 * sp.diff(B, x) * P**2 - 2 * sp.diff(Cc, x) * P**3
    assert zero(dG - want)
    t3 = (sp.diff(F, x, 3) + sp.diff(b, x, 3) * P) * sp.diff(G, P, 3) \
        - 3 * sp.diff(b, x, 2) * sp.diff(G, x, 1, P, 2)
    assert zero(t3 + 6 * sp.diff(b, x, 2) * sp.diff(Cc, x))
    done.append("Lemma 2 and formulas (6), (7)")

    # Theorem B(a): the static extras for deg b = 2, symbolic f and b.
    b2 = poly("b", 2)
    beta = sp.diff(b2, x, 2)
    H2 = y**2 + b2 * y + f
    xi = y + sp.diff(f, x, 2) / (3 * beta)
    assert zero(sp.diff(f, x, 3) * sp.diff(xi, y) - 3 * beta * sp.diff(xi, x))
    for power in (0, 1, 2):
        G = sp.integrate(sp.integrate(sp.expand(xi**power), y), y)
        assert zero(T(3, H2, G)) and zero(T(5, H2, G))
    G = sp.integrate(sp.integrate(sp.expand(xi**3), y), y)
    assert zero(T(3, H2, G)) and not zero(T(5, H2, G))
    done.append("Theorem B(a): first integral xi, extras xi and xi^2, failure of xi^3")

    # Theorem D: gates for H = c y^2 + b y + f and the top-coefficient laws.
    c = poly("c", 3)
    Hc = c * y**2 + b * y + f
    Gf = sp.Function("G")(x, y)
    t3 = (sp.diff(f, x, 3) + sp.diff(b, x, 3) * y + sp.diff(c, x, 3) * y**2) * sp.diff(Gf, y, 3) \
        - 3 * (sp.diff(b, x, 2) + 2 * sp.diff(c, x, 2) * y) * sp.diff(Gf, x, 1, y, 2) \
        + 6 * sp.diff(c, x) * sp.diff(Gf, x, 2, y, 1)
    t5 = sp.diff(f, x, 5) * sp.diff(Gf, y, 5) - 5 * sp.diff(b, x, 4) * sp.diff(Gf, x, 1, y, 4) \
        + 20 * sp.diff(c, x, 3) * sp.diff(Gf, x, 2, y, 3)
    assert zero(T(3, Hc, Gf).doit() - t3) and zero(T(5, Hc, Gf).doit() - t5)
    mono = gamma * x**n * y**d
    for k in (1, 2, 3):
        ck = x**k
        bracket = sp.diff(ck, x, 3) * y**2 * sp.diff(mono, y, 3) \
            - 6 * sp.diff(ck, x, 2) * y * sp.diff(mono, x, 1, y, 2) \
            + 6 * sp.diff(ck, x) * sp.diff(mono, x, 2, y, 1)
        lam = (k - 1) * (k - 2) * (d - 1) * (d - 2) - 6 * (k - 1) * (d - 1) * n + 6 * n * (n - 1)
        assert zero(bracket - gamma * k * d * lam * x ** (n + k - 3) * y ** (d - 1))
        top = sp.diff(ck, x) * y**2 * sp.diff(mono, y) - 2 * ck * y * sp.diff(mono, x)
        assert zero(top - gamma * (k * d - 2 * n) * x ** (n + k - 1) * y ** (d + 1))
    assert zero(20 * 6 * sp.diff(mono, x, 2, y, 3)
                - 120 * gamma * d * (d - 1) * (d - 2) * n * (n - 1) * x ** (n - 2) * y ** (d - 3))
    done.append("Theorem D: gate formulas (13), (14), laws (15), (16), the T5 top for deg c = 3")

    # Theorem D, model x^4 y + x y^2: the second coefficient under a top y^d.
    Hb = x**4 * y + x * y**2
    G = y**d + gamma * x**3 * y ** (d - 1)
    t3 = sp.expand(T(3, Hb, G))
    coefficient = sp.simplify(t3.coeff(x, 1) / y ** (d - 2))
    solution = sp.solve(coefficient, gamma)
    assert len(solution) == 1 and zero(solution[0] + sp.Rational(2, 3) * d * (d - 2))
    done.append("Theorem D: second coefficient -2 d (d-2)/3 in the quartic-b, linear-c model")

    # Theorem E: coefficients of D_H(u p + v) for H = c p^2 + b p + f, and the
    # converse identity H = c2 Q^2 + const with D_H Q = 0.
    r, c2, av, dv = sp.symbols("r c2 a_ d_")
    u = x - r
    v = sp.Function("v")(x)
    cg, bg, fg = sp.Function("c")(x), sp.Function("b")(x), sp.Function("f")(x)
    Hg = cg * y**2 + bg * y + fg
    DG = sp.expand(T(1, Hg, u * y + v).doit())
    assert zero(DG.coeff(y, 2) - (sp.diff(cg, x) * u - 2 * cg))
    assert zero(DG.coeff(y, 1) - (sp.diff(bg, x) * u - bg - 2 * cg * sp.diff(v, x)))
    assert zero(DG.coeff(y, 0) - (sp.diff(fg, x) * u - bg * sp.diff(v, x)))
    w = sp.Function("w")(x)
    # with c = c2 u^2 and b = u w the p-coefficient is u^2 (w' - 2 c2 v')
    mid = (sp.diff(u * w, x) * u - u * w - 2 * c2 * u**2 * sp.diff(v, x))
    assert zero(mid - u**2 * (sp.diff(w, x) - 2 * c2 * sp.diff(v, x)))
    w3 = poly("w", 3)
    Qe = u * y + w3 / (2 * c2)
    He = c2 * u**2 * y**2 + u * w3 * y + w3**2 / (4 * c2) + sp.Symbol("k0")
    assert zero(He - c2 * Qe**2 - sp.Symbol("k0"))
    assert zero(T(1, He, Qe)) and zero(T(3, He, Qe)) and zero(T(5, He, Qe))
    done.append("Theorem E: coefficients of D_H(up+v), the divisibility step, and the converse")

    # Sharpness witness for a nonconstant top coefficient.
    assert zero(T(3, Hc, x**2)) and zero(T(5, Hc, x**2))
    step = T(1, Hc, x**2)
    assert zero(T(3, Hc, step) + 24 * sp.diff(c, x) * sp.diff(x * c, x, 2))
    done.append("Witness: q^2 is static and T3(H, D_H q^2) = -24 c' (q c)''")
    return done


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "sympy": sp.__version__, "checked": run()}, indent=1))
