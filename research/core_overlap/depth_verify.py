#!/usr/bin/env python3
"""Independent exact checks for the analytic three-equation core theorem.

Only the Python standard library is needed. Fractional p exponents are
stored exactly. Direct mixed differentiation is compared with the
independently assembled sector formula.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb
import json
from pathlib import Path


def clean(p):
    return {k: v for k, v in p.items() if v}


def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Q(0)) + v
    return clean(out)


def scale(p, c):
    return clean({k: v * c for k, v in p.items()})


def mul(p, r):
    out = {}
    for (i, a), x in p.items():
        for (j, b), y in r.items():
            k = (i + j, a + b)
            out[k] = out.get(k, Q(0)) + x * y
    return clean(out)


def mono(i, a, coef=1):
    return clean({(i, Q(a)): Q(coef)})


def falling(x, n):
    out = Q(1)
    for j in range(n):
        out *= x - j
    return out


def diff(p, nq=0, np=0):
    out = {}
    for (i, a), v in p.items():
        c = v * falling(i, nq) * falling(a, np)
        if c:
            assert i >= nq
            out[(i - nq, a - np)] = c
    return out


def transvectant(h, g, n):
    return add(*(scale(mul(diff(h, n - j, j), diff(g, j, n - j)),
                       (-1) ** j * comb(n, j))
                 for j in range(n + 1)))


def sector(f, g, c, n):
    ff = falling(c, n - 1)
    if not ff:
        return {}
    inner = add(scale(mul(diff(f, np=n - 1), diff(g, np=1)), n),
                scale(mul(diff(f, np=n), g), -(c - n + 1)))
    if not inner:
        return {}
    assert c - n + 1 >= 0
    return scale(mul(mono(c - n + 1, 0), inner), ff)


def poly_add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Q(0)) + v
    return clean(out)


def poly_mul(p, r):
    out = {}
    for i, x in p.items():
        for j, y in r.items():
            out[i + j] = out.get(i + j, Q(0)) + x * y
    return clean(out)


def check():
    fcases = [mono(0, 2), mono(0, Q(-2, 5)), mono(0, Q(8, 7)),
              add(mono(0, 3), mono(0, 1, 2), mono(0, 0, -3)),
              add(mono(0, -2, 3), mono(0, Q(1, 2), -4))]
    gcases = [mono(0, 0), mono(0, Q(-8, 5)), mono(0, 4),
              add(mono(0, Q(-1, 3), 2), mono(0, Q(7, 4), -5))]
    count = 0
    for f in fcases:
        h = mul(mono(1, 0), f)
        for g in gcases:
            for c in range(14):
                fullg = mul(mono(c, 0), g)
                for n in (1, 3, 5, 7, 9):
                    direct = transvectant(h, fullg, n)
                    expected = sector(f, g, c, n)
                    assert direct == expected, (f, g, c, n, direct, expected)
                    count += 1

    examples = {}
    h = mono(1, 2)
    g = mono(2, 0)
    assert not transvectant(h, g, 3)
    assert not transvectant(h, g, 5)
    assert transvectant(h, transvectant(h, g, 1), 3) == mono(0, 0, -48)
    examples['first_derivation_necessary'] = '-48'

    g = mono(2, 4)
    assert not transvectant(h, g, 1)
    assert not transvectant(h, g, 5)
    assert transvectant(h, g, 3) == mono(0, 3, 48)
    examples['initial_third_gate_necessary'] = '48*p^3'

    h, g = mono(1, Q(-2, 5)), mono(4, Q(-8, 5))
    assert not transvectant(h, g, 1)
    assert not transvectant(h, g, 3)
    assert transvectant(h, g, 5) == mono(0, -7, Q(-548352, 625))
    examples['fifth_gate_necessary'] = '-548352/625*p^-7'

    h, g = mono(1, Q(8, 7)), mono(6, Q(-8, 7))
    assert not transvectant(h, g, 3)
    assert not transvectant(h, g, 5)
    assert transvectant(h, g, 7) == mono(0, -7, Q(-1940889600, 117649))
    examples['seventh_gate_necessary_for_static_space'] = '-1940889600/117649*p^-7'

    h = add(mono(1, Q(-1, 4)), mono(0, Q(7, 4)))
    g = add(mono(3, Q(-3, 4)), mono(2, Q(5, 4), Q(-21, 25)))
    dg = transvectant(h, g, 1)
    assert dg == add(mono(2, 0, Q(-168, 25)), mono(1, 2, Q(147, 50)))
    assert not transvectant(h, g, 3)
    assert not transvectant(h, g, 5)
    assert not transvectant(h, dg, 3)
    assert transvectant(h, transvectant(h, dg, 1), 3) == mono(0, Q(-9, 2), Q(63, 8))
    examples['second_derivation_necessary_with_additive_potential'] = '63/8*p^(-9/2)'

    # Cross-multiplied polynomial identity in c, not a sampled check:
    # 1+a(beta-2)=8(c+1)/((c-4)(c-2)).
    cm2, cm4, c = {1: Q(1), 0: Q(-2)}, {1: Q(1), 0: Q(-4)}, {1: Q(1)}
    lhs = poly_add(poly_mul(cm2, cm4),
                   poly_mul({1: Q(5)}, cm2),
                   poly_mul({1: Q(-6)}, cm4))
    assert lhs == {1: Q(8), 0: Q(8)}

    for c in range(5, 10005):
        a, beta = Q(3 * c, c - 2), Q(5 * (c - 2), 3 * (c - 4))
        assert beta > 1 and a > 0
        assert 1 + a * (beta - 2) == Q(8 * (c + 1), (c - 4) * (c - 2)) > 0
        aa, dd = (3 * a - 1) * (1 - beta), a * (beta - 4) + 3
        assert (beta + 1) * dd - 2 * aa == (beta + 5) * (1 + a * (beta - 2))

    # The pole argument does not need a fifth-order test. Check its
    # leading coefficient directly against fractional-power derivatives.
    pole_count = 0
    for t in range(1, 41):
        f = mono(0, -t)
        b = diff(f, np=2)
        # B'/B=-(t+2)/p for this monomial; its nonzero constant factor
        # cancels, so Kc can be assembled without roots.
        for c in range(2, 102):
            kc = add(scale(mul(f, mono(0, -1)), -Q(c - 2, 3) * (t + 2)),
                     scale(diff(f, np=1), -c))
            expected = Q(2, 3) * ((c + 1) * t - c + 2)
            assert expected > 0
            assert kc == mono(0, -t - 1, expected)
            assert (c + 1) * t - c + 2 == (c + 1) * (t - 1) + 3
            pole_count += 1

    return {'status': 'passed', 'format': 'analytic-qF-three-equation-v1',
            'sector_operator_comparisons': count,
            'exact_sharpness_examples': examples,
            'symbolic_parameter_identity': 'passed',
            'parameter_grid': {'c_min': 5, 'c_max': 10004, 'count': 10000},
            'pole_leading_coefficient_comparisons': pole_count,
            'scope': 'A[q], real-analytic F,V on a connected interval; proofs localize where F double-prime is nonzero and treat the affine case separately',
            'claim': 'D_infinity(qF)=ker C3 intersect ker(C3 D) intersect ker C5',
            'gamma_polygamma_refinement': 'ker C3 intersect ker(C3 D)=A direct-sum qA',
            'additive_potential_refinement': 'D_infinity(qF+V)=ker C3 intersect ker C5 intersect ker(C3 D) intersect ker(C3 D^2)',
            'limits': 'The all-degree conclusion uses the supplied proof, not the finite grid.'}


if __name__ == '__main__':
    result = check()
    target = Path(__file__).with_name('depth_results.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
