"""Exact classifier for sextics quadratic in a coordinate complementary to a sixfold root.

Scope: H in Q[q,p] of total degree six with H6 = a*L^6 and

    H = c(L) M^2 + b(L) M + f(L),    c != 0,

for a rational linear form L and the complement M chosen below.  The proofs
are in c3_strata/QUADRATIC_SIXFOLD_THEOREM.md.

* c constant: Theorems A, B, C give every refinement space in closed form.
* c nonconstant: Theorem D confines S^1 to an explicit finite weighted box,
  so S^r (r >= 1) and the core are obtained by exact linear algebra in that
  box.  This is complete for all polynomial degrees because of the theorem,
  not because of the finite computation alone.  Theorem E gives the core
  dimension in closed form; the box computation must agree with it.

Schema hamiltonian-sextic-core/1 cannot express these results (it requires
S1, S2 and Dinf of one kind and a depth of at most two).  They are exposed to
consumers through sextic_core.classify_sextic_v2.  Standard library only.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "independent"))
import engine as E  # noqa: E402

SCHEMA = "hamiltonian-quadratic-sixfold/1"
_ONE = {(0, 0): F(1)}
_X = {(1, 0): F(1)}
_Y = {(0, 1): F(1)}


def _substitute(poly, first, second):
    """poly(first, second) for polynomials first, second."""
    out = {}
    for (i, j), value in poly.items():
        out = E.add(out, E.scale(E.multiply(E.power(first, i), E.power(second, j)), value))
    return out


def _coefficient(poly, j):
    """Coefficient of M^j as a polynomial in L (stored as (i, 0))."""
    return {(i, 0): v for (i, jj), v in poly.items() if jj == j}


def _deg(poly):
    return max((i for i, _ in poly), default=-1)


def _d(poly, order=1):
    return E.derivative(poly, q=order)


def adapted_coordinates(H):
    """Return (L, M, forward, inverse) or None when H6 is not a sixth power.

    L, M are linear forms in (q, p); `inverse` gives (q, p) as forms in (L, M).
    The linear map has determinant +1 or -1.
    """
    H6 = {k: v for k, v in H.items() if sum(k) == 6}
    a6 = H6.get((6, 0), F(0))
    if a6:
        s = H6.get((5, 1), F(0)) / (6 * a6)
        L = E.add(_X, E.scale(_Y, s))
        M = dict(_Y)
        inverse = (E.add(_X, E.scale(_Y, -s)), dict(_Y))      # q = L - sM, p = M
        lead = a6
    else:
        L, M = dict(_Y), dict(_X)
        inverse = (dict(_Y), dict(_X))                         # q = M, p = L
        lead = H6.get((0, 6), F(0))
    if not lead or H6 != E.scale(E.power(L, 6), lead):
        return None
    return L, M, inverse


def _space(ring=None, module=(), finite=()):
    """K[L]*module + span(finite).  dimension is None when infinite."""
    return {"module_over_K[L]": [E.serialize(G) for G in module],
            "finite_span": [E.serialize(G) for G in finite],
            "dimension": None if module else len(finite)}


def _weighted_kernels(H, wx, wy, bound, max_depth=8):
    """S^1, S^2, ... inside weighted degree <= bound, until stable and D-invariant."""
    exponents = [(a, j) for j in range(bound // wy + 1)
                 for a in range((bound - wy * j) // wx + 1)]
    current = [{e: F(1)} for e in exponents]
    images = [{} for _ in exponents]
    stages = []
    for iterate in range(max_depth + 1):
        for image, poly in zip(images, current):
            for hbar, defect in E.defects(H, poly).items():
                for (a, j), value in defect.items():
                    image[iterate, hbar, a, j] = value
        keys = sorted({key for image in images for key in image})
        rows = [[image.get(key, F(0)) for image in images] for key in keys]
        basis = [E.tidy(dict(zip(exponents, v))) for v in E.nullspace(rows, len(exponents))]
        if iterate >= 1:
            stages.append(basis)
            if len(stages) >= 2 and len(stages[-1]) == len(stages[-2]):
                stages.pop()
                return stages
        current = [E.poisson(H, poly) for poly in current]
    raise RuntimeError("Refinement did not stabilize inside the proved depth bound")


def _divide_linear(poly, root):
    """Quotient and remainder of a polynomial in L by (L - root)."""
    degree = _deg(poly)
    quotient, carry = {}, F(0)
    for i in range(degree, -1, -1):
        carry = poly.get((i, 0), F(0)) + carry * root
        if i:
            quotient[(i - 1, 0)] = carry
    return E.tidy(quotient), carry


def square_first_integral(c, b, f):
    """Theorem E.  Return Q with H = c2*Q^2 + const, or None.

    Q exists exactly when c = c2*u^2 for a monic linear u, u divides b, and
    f - b^2/(4c) is constant; then Q = u*M + b/(2*c2*u).
    """
    if _deg(c) != 2:
        return None
    c2, c1, c0 = (c.get((i, 0), F(0)) for i in (2, 1, 0))
    if c1 * c1 != 4 * c0 * c2:
        return None
    root = -c1 / (2 * c2)
    w, remainder = _divide_linear(b, root)
    if remainder:
        return None
    residual = E.add(f, E.scale(E.multiply(w, w), -1 / (4 * c2)))
    if _deg(residual) > 0:
        return None
    u = {(1, 0): F(1), (0, 0): -root}
    return E.add(E.multiply(u, _Y), E.scale(w, 1 / (2 * c2)))


def _first_failure(H, G, limit=12):
    current = G
    for iterate in range(limit + 1):
        if E.defects(H, current):
            return iterate
        current = E.poisson(H, current)
    raise RuntimeError("Expected a failing iterate")


def _witness(H, G, back, expected):
    """A polynomial in S^(expected-1) that fails S^expected, checked exactly."""
    if _first_failure(H, G) != expected:
        raise RuntimeError("Sharpness witness fails at the wrong iterate")
    return {"G": E.serialize(back(G)), "first_failing_iterate": expected}


def _rank(polys):
    keys = sorted({k for G in polys for k in G})
    rows = [[G.get(k, F(0)) for k in keys] for G in polys]
    return len(keys) - len(E.nullspace(rows, len(keys))) if keys else 0


def _in_span(basis, G):
    return _rank(basis + [G]) == _rank(basis)


def classify_quadratic_sixfold(H):
    """Exact classification, or status=out_of_scope with the reason."""
    H = E.tidy(H)
    report = {"schema": SCHEMA, "input": E.serialize(H), "status": "out_of_scope"}
    if max((sum(k) for k in H), default=-1) != 6:
        report["reason"] = "Total degree must be six"
        return report
    coordinates = adapted_coordinates(H)
    if coordinates is None:
        report["reason"] = "Leading form is not a rational multiple of a sixth power"
        return report
    L, M, inverse = coordinates
    Ht = _substitute(H, *inverse)                      # H as a polynomial in (L, M)
    m_degree = max(j for _, j in Ht)
    if m_degree != 2:
        report["reason"] = ("Affine in the complement: use sextic_core.py" if m_degree <= 1 else
                            "Degree three or more in the complement is outside the proved family")
        return report
    c, b, f = (_coefficient(Ht, j) for j in (2, 1, 0))
    k, m = _deg(c), _deg(b)
    back = lambda G: _substitute(G, L, M)              # (L, M) chart -> (q, p)
    report.update({"status": "classified", "L": E.serialize(L), "M": E.serialize(M),
                   "deg_c": k, "deg_b": m})
    if _deg(f) != 6 or m > 4 or k > 3:
        raise RuntimeError("Degree bookkeeping violated for a sixfold leading form")

    if k >= 1:
        if k == 1:
            wx, wy, bound = (1, 3, 13) if m == 4 else (2, 5, 22)
        elif k == 2:
            wx, wy, bound = (2, 4, 18) if m == 4 else (2, 4, 24)
        else:
            wx, wy, bound = 2, 3, 26
        stages = _weighted_kernels(Ht, wx, wy, bound)
        core = stages[-1]
        if not all(_in_span(core, E.poisson(Ht, G)) for G in core):
            raise RuntimeError("Stable stage is not invariant")
        if not (_in_span(core, _ONE) and _in_span(core, Ht)):
            raise RuntimeError("Core must contain 1 and H")
        degenerate = (k == 2 and m == 4 and
                      b[(4, 0)] ** 2 == 4 * f[(6, 0)] * c[(2, 0)])
        Q = square_first_integral(c, b, f)
        if Q is not None and not degenerate:
            raise RuntimeError("A square first integral forces the discriminant locus")
        if len(core) != (3 if Q is not None else 2):
            raise RuntimeError("Box computation disagrees with Theorem E")
        if Q is not None:
            if E.poisson(Ht, Q) or E.defects(Ht, Q):
                raise RuntimeError("Q must Poisson-commute with H and pass the static gates")
            if len(stages) != 1 or _rank(core + [Q]) != 3:
                raise RuntimeError("Theorem E predicts S^1 = core = span(1, Q, H)")
        depth = len(stages)
        # q^2 passes the static gates and T3(H, D_H q^2) = -24 c' (q c)'' != 0.
        if depth == 1:
            probe = E.power(_X, 2)
        else:
            probe = next(G for G in stages[depth - 2] if not _in_span(core, G))
        report.update({
            "regime": "variable_top_coefficient",
            "weights": {"L": wx, "M": wy, "bound": bound},
            "degenerate_discriminant": degenerate,
            "square_first_integral": None if Q is None else E.serialize(back(Q)),
            "least_depth": depth,
            "stages": {f"S{r + 1}": _space(finite=[back(G) for G in stage])
                       for r, stage in enumerate(stages)},
            "Dinf": _space(finite=[back(G) for G in core]),
            "S0": None,
            "sharpness_witness": _witness(Ht, probe, back, depth),
        })
        return report

    c0 = c[(0, 0)]
    bn, fn = E.scale(b, 1 / c0), E.scale(f, 1 / c0)
    P = E.add(_Y, E.scale(bn, F(1, 2)))                # in the (L, M) chart
    Fn = E.add(fn, E.scale(E.multiply(bn, bn), F(-1, 4)))
    N = _deg(Fn)
    low = [_ONE, _X, E.power(_X, 2)]
    xP, YY = E.multiply(_X, P), E.power(_Y, 2)
    six = low + [P, xP, Ht]
    fin = lambda *polys: _space(finite=[back(G) for G in polys])
    if m <= 1:
        regime, depth, witness = "affine_shift", 5, _X
        stages = [
            _space(module=[back(G) for G in (_ONE, _Y, YY)]),
            _space(module=[back(G) for G in (_ONE, _Y)], finite=[back(YY)]),
            _space(module=[back(_ONE)], finite=[back(G) for G in (_Y, E.multiply(_X, _Y), YY)]),
            fin(*six), fin(*low, Ht), fin(_ONE, Ht)]
    else:
        extra = []
        if m == 2:
            xi = E.add(_Y, E.scale(_d(fn, 2), 1 / (3 * _d(bn, 2)[(0, 0)])))
            for power in (1, 2):
                U = E.power(xi, power)
                extra.append({(a, j + 2): v / ((j + 1) * (j + 2)) for (a, j), v in U.items()})
        stages = [
            _space(module=[back(G) for G in (_ONE, _Y)], finite=[back(G) for G in [YY] + extra]),
            _space(module=[back(_ONE)], finite=[back(G) for G in (_Y, E.multiply(_X, _Y), Ht)]),
            fin(*six)]
        if N >= 4:
            regime, depth, witness = "generic_nonlinear", 4, _X
            stages += [fin(*low, Ht), fin(_ONE, Ht)]
        elif N == 3:
            regime, depth, witness = "cubic_potential", 6, _X
            stages += [fin(*low, P, Ht), fin(_ONE, _X, P, Ht), fin(_ONE, _X, Ht), fin(_ONE, Ht)]
        else:
            regime, depth, witness = "hidden_quadratic", 2, E.power(_X, 3)
    report.update({
        "regime": regime, "deg_F": N, "least_depth": depth,
        "stages": {f"S{r}": stage for r, stage in enumerate(stages)},
        "Dinf": stages[-1],
        "sharpness_witness": _witness(Ht, witness, back, depth),
    })
    return report


if __name__ == "__main__":
    import argparse
    import json
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import partner_lab
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--H", required=True)
    print(json.dumps(classify_quadratic_sixfold(partner_lab.parse(parser.parse_args().H)),
                     indent=1, sort_keys=True))
