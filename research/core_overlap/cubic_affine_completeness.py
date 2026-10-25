#!/usr/bin/env python3
"""Full cubic-phase affine cores for deg b>=2; exact standard-library checks."""
from __future__ import annotations
import argparse
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT/'extensions/hamiltonian'), str(ROOT/'extensions')]
import check_two_root as T
import check_triangular as CT
import weyl_receipts as W
import qlinalg as L

FORMAT = 'cubic-affine-complete-v1'
ONE = {(0, 0): F(1)}
Q = {(1, 0): F(1)}
P = {(0, 1): F(1)}


def up(u):
    return {(0, int(j)): F(c) for j, c in u.items() if F(c)}


def exact_poly(h):
    out = {}
    try:
        for (i, j), c in h.items():
            if any(isinstance(v, float) for v in (i, j, c)):
                return None
            i, j, c = F(i), F(j), F(c)
            if min(i, j) < 0 or i.denominator != 1 or j.denominator != 1:
                return None
            if c:
                out[int(i), int(j)] = c
    except (TypeError, ValueError, AttributeError, ZeroDivisionError):
        return None
    return out


def classify_affine(h):
    """Classify h in (Q,P), for arbitrary a and deg b>=2.

    Return None outside the declared polynomial scope. Basis entries are
    polynomials in (Q,P); transport by the given quadratic shear afterward.
    """
    h = exact_poly(h)
    if not h or any(i > 1 for i, j in h):
        return None
    a = {j: c for (i, j), c in h.items() if i == 0}
    b = {j: c for (i, j), c in h.items() if i == 1}
    m, f = max(b, default=-1), max(a, default=-1)
    if m < 2:
        return None
    basis = [ONE, h]
    case = 'nonlinear vector-field coefficient'
    extra = {}
    if m == 2:
        mu, b1, b0 = b[2], b.get(1, F(0)), b.get(0, F(0))
        if f <= 2:
            shift = a.get(2, F(0))/mu
            X = T.add(Q, T.sc(ONE, shift))
            basis = [ONE, X, T.mul(X, P), h]
            case = 'quadratic coefficient with low density'
            extra = {'shift_Q': str(shift)}
        elif f == 4:
            A = a[4]
            r = (b1/mu-a.get(3, F(0))/A)/2
            rp = -b1/mu-r
            if sum(c*r**j for j, c in b.items()) == 0:
                c2 = a.get(2, F(0))-3*A*r*(r+rp)
                x = T.add(P, T.sc(ONE, -r))
                G = T.add(T.sc(T.power(x, 3), A), T.sc(x, c2),
                          T.sc(T.mul(Q, x), mu))
                basis = [ONE, G, h]
                case = 'K4 full core'
                extra = {'r': str(r), 'r_prime': str(rp), 'c2': str(c2),
                         'G': T.ser(G)}
            else:
                case = 'quadratic coefficient outside K4'
        else:
            case = 'quadratic coefficient outside K4'
    return {'format': FORMAT, 'degree_a': f, 'degree_b': m,
            'dimension': len(basis), 'case': case, 'proved': True,
            'basis': basis,
            'third_gate_depth_for_Q_degree_bound': 2 if m == 2 else 1,
            'third_gate_depth': 2 if m == 2 else 1,
            'finite_stopping_equality': 'intersection of ker(C3 D^r) through the declared depth',
            'proof': 'cubic_affine_completeness.md', **extra}


def decode(p):
    return {tuple(map(int, k.split(','))): F(c) for k, c in p.items()}


def serialize_classification(result):
    out = dict(result)
    out['basis'] = [T.ser(g) for g in result['basis']]
    return out


def check_application(cert):
    if cert.get('format') != FORMAT or 'hamiltonian_QP' not in cert:
        raise ValueError('not a cubic-affine theorem application')
    result = classify_affine(decode(cert['hamiltonian_QP']))
    if result is None or cert.get('classification') != serialize_classification(result):
        raise ValueError('theorem application mismatch')
    return {'status': 'passed', 'dimension': result['dimension']}


def D(g, a, b):
    return T.add(T.mul(b, W.pder(g, 0, 1)),
                 T.sc(T.mul(T.add(W.pder(a, 0, 1),
                                 T.mul(Q, W.pder(b, 0, 1))),
                            W.pder(g, 1, 0)), -1))


def C3(g, a, b, c):
    a2, a3 = W.pder(a, 0, 2), W.pder(a, 0, 3)
    b1, b2, b3 = (W.pder(b, 0, j) for j in (1, 2, 3))
    inside = T.add(T.mul(b1, W.pder(g, 0, 3)),
                   T.mul(b2, W.pder(g, 0, 2)),
                   T.sc(T.mul(T.add(a2, T.mul(Q, b2)), W.pder(g, 1, 2)), -1),
                   T.sc(T.mul(T.add(a3, T.mul(Q, b3)), W.pder(g, 1, 1)), -1))
    return T.add(T.sc(inside, 6*c), T.sc(T.mul(b2, W.pder(g, 2, 1)), 3),
                 T.sc(T.mul(T.add(a3, T.mul(Q, b3)), W.pder(g, 3, 0)), -1))


def LN(f, b, n):
    return T.add(T.mul(b, W.pder(f, 0, 1)),
                 T.sc(T.mul(W.pder(b, 0, 1), f), -n))


def MN(f, b, n):
    return T.add(T.mul(W.pder(b, 0, 1), W.pder(f, 0, 3)),
                 T.sc(T.mul(W.pder(b, 0, 2), W.pder(f, 0, 2)), 1-n),
                 T.sc(T.mul(W.pder(b, 0, 3), W.pder(f, 0, 1)), -n))


def qcol(g, n):
    return {(0, j): c for (i, j), c in g.items() if i == n}


def pdeg(f):
    return max((j for i, j in f), default=-1)


def rank(gens):
    keys = sorted({k for g in gens for k in g})
    return L.rank([[g.get(k, F(0)) for g in gens] for k in keys], len(gens))


def quadratic_static_basis(a, b):
    """The proved five-dimensional affine static third-gate kernel."""
    mu = b[(0, 2)]
    rho = -b.get((0, 1), F(0))/(2*mu)
    out = [ONE, P]
    for beta in (ONE, P, T.power(P, 2)):
        numerator = T.mul(W.pder(beta, 0, 1), W.pder(a, 0, 2))
        value = sum(v*rho**j for (_, j), v in numerator.items())
        numerator = T.add(numerator, T.sc(ONE, -value))
        quotient = {}
        while pdeg(numerator) >= 1:
            d = pdeg(numerator)
            v = numerator[(0, d)]/(2*mu)
            term = up({d-1: v})
            quotient = T.add(quotient, term)
            numerator = T.add(numerator, T.sc(T.mul(term, W.pder(b, 0, 1)), -1))
        assert not numerator
        alpha = {(0, j+2): v/F((j+1)*(j+2)) for (_, j), v in quotient.items()}
        out.append(T.add(alpha, T.mul(Q, beta)))
    assert rank(out) == 5
    assert all(not C3(g, a, b, F(1)) for g in out)
    return out


def finite_static_kernel(a, b, depth=2):
    """All-output matrix on the proved static five-space, no output projection."""
    columns = []
    for g in quadratic_static_basis(a, b):
        col = {}
        for r in range(depth+1):
            for (i, j), v in C3(g, a, b, F(1)).items():
                col[r, i, j] = v
            g = D(g, a, b)
        columns.append(col)
    keys = sorted({k for col in columns for k in col})
    matrix = [[col.get(k, F(0)) for col in columns] for k in keys]
    return 5-L.rank(matrix, 5)


def formal_factor_identity():
    # Sparse formal polynomials in independent variables (n,N,m).
    def add(*xs):
        z = {}
        for x in xs:
            for e, c in x.items():
                z[e] = z.get(e, F(0))+c
        return {e: c for e, c in z.items() if c}
    def scale(x, c):
        return {e: c*v for e, v in x.items() if c*v}
    def mul(x, y):
        z = {}
        for e, c in x.items():
            for f, d in y.items():
                k = tuple(u+v for u, v in zip(e, f))
                z[k] = z.get(k, F(0))+c*d
        return {e: c for e, c in z.items() if c}
    one = {(0, 0, 0): F(1)}
    n, N, m = ({tuple(int(i == j) for i in range(3)): F(1)} for j in range(3))
    nm1, nm2, mm1, mm2 = (add(x, scale(one, -j)) for x, j in ((n, 1), (n, 2), (m, 1), (m, 2)))
    raw = add(mul(nm1, nm2), mul(mul(add(one, scale(N, -1)), mm1), nm1),
              scale(mul(mul(N, mm1), mm2), -1))
    factored = mul(add(n, m, scale(one, -3)), add(nm1, scale(mul(N, mm1), -1)))
    assert raw == factored
    return len(raw)


def run():
    rng = random.Random(2941)
    counts = {'formal_factor_terms': formal_factor_identity(),
              'operator_checks': 0, 'top_Q_checks': 0,
              'leading_degree_obstructions': 0, 'classified_instances': 0,
              'full_basis_gate_and_closure_checks': 0,
              'forgery_rejections': 0, 'invalid_input_rejections': 0,
              'sl2_exclusion_checks': 0, 'low_density_constraint_checks': 0,
              'sharp_depth_checks': 0, 'proved_static_space_rank_checks': 0}
    for k in range(18):
        c = F(rng.choice([1, -2, 3]))
        w = {2: c, 1: F(rng.randint(-2, 2)), 0: F(rng.randint(-2, 2))}
        fa, mb = rng.randint(0, 6), rng.randint(2, 5)
        a = up({j: F(rng.randint(-2, 2)) for j in range(fa+1)})
        b = T.add(up({j: F(rng.randint(-2, 2)) for j in range(mb)}), up({mb: F(1)}))
        g = T.tidy({(i, j): F(rng.randint(-2, 2)) for i in range(4) for j in range(5)})
        h = T.add(a, T.mul(Q, b))
        H, G = CT.tri(h, w), CT.tri(g, w)
        assert CT.untri(W.act(W.derivation(H), G), w) == D(g, a, b)
        assert CT.untri(W.act(W.gate(H, 3), G), w) == C3(g, a, b, c)
        counts['operator_checks'] += 2
        N = max(i for i, j in g)
        f = qcol(g, N)
        assert qcol(D(g, a, b), N) == LN(f, b, N)
        assert qcol(C3(g, a, b, c), N) == T.sc(MN(f, b, N), 6*c)
        counts['top_Q_checks'] += 2
    for k in range(12):
        c = F(rng.choice([1, -2]))
        a = up({3: F(rng.choice([1, 2, -1])), 2: F(rng.randint(-2, 2)),
                1: F(rng.randint(-2, 2)), 0: F(rng.randint(-2, 2))})
        b = up({2: F(rng.choice([1, -2])), 1: F(rng.randint(-2, 2)),
                0: F(rng.randint(-2, 2))})
        actual = C3(D(D(Q, a, b), a, b), a, b, c)
        expected = T.sc(T.mul(T.mul(W.pder(b, 0, 1), W.pder(b, 0, 2)),
                              W.pder(a, 0, 3)), -12*c)
        assert actual == expected != {}
        counts['sl2_exclusion_checks'] += 1
        low_a = up({1: F(rng.randint(-2, 2)), 0: F(rng.randint(-2, 2))})
        alpha1, beta2 = F(rng.randint(-2, 2)), F(rng.randint(-2, 2))
        g = T.add(T.sc(P, alpha1), T.mul(Q, up({2: beta2, 1: F(2), 0: F(-1)})))
        scalar = 24*c*b[(0, 2)]*(b[(0, 2)]*alpha1-low_a.get((0, 1), F(0))*beta2)
        assert C3(D(g, low_a, b), low_a, b, c) == T.sc(ONE, scalar)
        counts['low_density_constraint_checks'] += 1
    for m in range(2, 7):
        b = up({m: F(2), m-1: F(-1), 0: F(3)})
        for N in range(2, 7):
            allowed = (0, 1, N+1) if m == 2 else (0, 1+N*(m-1))
            for n in allowed:
                f = up({n: F(3)})
                steps = 2 if m == 2 and n == 0 else 1
                for _ in range(steps):
                    f = LN(f, b, N)
                failure = MN(f, b, N)
                assert failure
                d = pdeg(f)
                expected = 2*f[(0, d)]*m*d*(d+m-3)*(d-1-N*(m-1))
                assert failure.get((0, d+m-4)) == expected != 0
                counts['leading_degree_obstructions'] += 1
    instances = []
    # The low-density four-dimensional branch, including roots that do not split over Q.
    for k in range(12):
        a = up({j: F(rng.randint(-2, 2)) for j in range(3)})
        b = up({2: F(rng.choice([1, -2])), 1: F(rng.randint(-2, 2)), 0: F(rng.randint(-2, 2))})
        instances.append((T.add(a, T.mul(Q, b)), 4))
    # General K4, including repeated roots and nonzero cubic coefficients.
    for k in range(10):
        mu, A = F(rng.choice([1, -2])), F(rng.choice([1, 2, -1]))
        r, rp = F(rng.randint(-2, 2)), F(rng.randint(-2, 2))
        x, y = T.add(P, T.sc(ONE, -r)), T.add(P, T.sc(ONE, -rp))
        b = T.sc(T.mul(x, y), mu)
        a = T.add(T.sc(T.mul(T.power(x, 3), y), A),
                  T.sc(T.power(x, 2), F(rng.randint(-2, 2))),
                  T.sc(x, F(rng.randint(-2, 2))), T.sc(ONE, F(rng.randint(-2, 2))))
        instances.append((T.add(a, T.mul(Q, b)), 3))
    for f in (3, 5, 6, 8):
        instances.append((T.add(up({f: F(1)}), T.mul(Q, up({2: F(1), 0: F(1)}))), 2))
    for m in (3, 4, 6):
        for f in (0, 2, 5):
            instances.append((T.add(up({f: F(1)}), T.mul(Q, up({m: F(1), 1: F(-1)}))), 2))
    for h, want in instances:
        result = classify_affine(h)
        assert result and result['dimension'] == want
        basis = result['basis']
        assert rank(basis) == want
        w = {2: F(rng.choice([1, -2])), 1: F(rng.randint(-2, 2)), 0: F(rng.randint(-2, 2))}
        H, gs = CT.tri(h, w), [CT.tri(g, w) for g in basis]
        assert CT.span_ok(H, gs)
        if result['degree_b'] == 2:
            a = {(0, j): v for (i, j), v in h.items() if i == 0}
            b = {(0, j): v for (i, j), v in h.items() if i == 1}
            assert finite_static_kernel(a, b, 2) == want
            counts['proved_static_space_rank_checks'] += 1
        counts['classified_instances'] += 1
        counts['full_basis_gate_and_closure_checks'] += len(gs)
        cert = {'format': FORMAT, 'hamiltonian_QP': T.ser(h), 'classification': serialize_classification(result)}
        assert check_application(cert)['dimension'] == want
        if len(instances) and counts['classified_instances'] <= 3:
            for field in ('dimension', 'proved'):
                bad = copy.deepcopy(cert)
                bad['classification'][field] = 19 if field == 'dimension' else False
                try:
                    check_application(bad)
                except ValueError:
                    counts['forgery_rejections'] += 1
                else:
                    raise AssertionError('forged classification accepted')
    for c in (F(1), F(-2), F(3)):
        a, b = {}, T.power(P, 2)
        witness = T.add(T.power(Q, 2), T.sc(P, 2/c))
        assert not C3(witness, a, b, c)
        assert not C3(D(witness, a, b), a, b, c)
        failure = C3(D(D(witness, a, b), a, b), a, b, c)
        assert failure.get((2, 0)) == -288*c
        counts['sharp_depth_checks'] += 3
    for m in (3, 4, 6):
        b = up({m: F(1), 1: F(2), 0: F(-1)})
        assert not C3(P, {}, b, F(1))
        assert C3(D(P, {}, b), {}, b, F(1))
        counts['sharp_depth_checks'] += 2
    for h in ({(2, 0): F(1), (1, 2): F(1)}, {(1, 1): F(1)},
              {(1, 2): 1.0}, {(-1, 2): 1}, {(1, F(3, 2)): 1}):
        assert classify_affine(h) is None
        counts['invalid_input_rejections'] += 1
    return {'format': FORMAT, 'status': 'passed', 'checks': counts,
            'theorems': ['all-degree Q-affine containment for deg b>=2',
                         'full span{1,H} for deg b>=3, arbitrary a',
                         'complete quadratic-b core classification in every density degree',
                         'four-dimensional low-density quadratic-b branch',
                         'K4 necessity without bounded symbolic casework'],
            'scope': 'Exact rational checks supplement written all-degree proofs over characteristic-zero fields; historical priority unestablished.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
