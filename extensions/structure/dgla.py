#!/usr/bin/env python3
"""Finite DGLA Maurer-Cartan lifting through the rational contraction (S2 producer).

Given a dgla-v1 model and a first-order term x_1 in L^1 with d x_1 = 0, solve
d x_n = -ob_n, ob_n = (1/2) sum_{i+j=n} [x_i, x_j], order by order with the S1
obstruction compiler on the complex of graded pieces. A vanishing class gives the
explicit correction x_n = h(-ob_n) (complement/gauge choice: the contraction's h;
adding any cocycle of L^1 gives another lift). A nonzero class gives a functional on
L^2 that vanishes on d(L^1) and detects ob_n. Certificates are replayed by
check_dgla.py, which re-verifies the DGLA axioms itself.

Also provides `lie_deformation_dgla(n, structure)`: the Chevalley-Eilenberg DGLA
L^k = Hom(Lambda^(k+1) g, g) with the Nijenhuis-Richardson bracket and d = [mu, .],
whose Maurer-Cartan elements are the deformations mu + x of a Lie bracket mu.

Usage: dgla.py lift MODEL.json --x1 '[...]' --order N [--output CERT.json]
       dgla.py lie --structure '{"0,1": {"2": 1}}' --dim 3 --output MODEL.json
"""
from __future__ import annotations
import argparse
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_dgla as C      # noqa: E402
import obstruction as O     # noqa: E402


def graded_complex(A):
    """Model of the cochain complex of graded pieces, with index maps."""
    degs = sorted(set(A.deg))
    lo, hi = degs[0], degs[-1]
    pieces = {k: [i for i in range(A.N) if A.deg[i] == k] for k in range(lo, hi + 1)}
    dims = [len(pieces[k]) for k in range(lo, hi + 1)]
    diffs = []
    for k in range(lo, hi):
        src, dst = pieces[k], pieces[k + 1]
        diffs.append([[str(A.d[i][j]) for j in src] for i in dst] if dst else [])
        if not src:
            diffs[-1] = [[] for _ in dst]
    return {'field': 'Q', 'dimensions': dims, 'differentials': diffs}, pieces, lo


def lift(model, x1, order):
    A = C.Algebra(model)
    A.verify_structure()
    x1 = [F(c) for c in x1]
    cx, pieces, lo = graded_complex(A)
    if 1 not in pieces or 2 not in pieces:
        raise ValueError('need nonempty degrees 1 and 2')
    xs = [x1]
    cert = {'format': C.FORMAT, 'coefficient_domain': 'Q', 'model_sha256': C.digest(model)}
    if any(A.dif(x1)):
        raise ValueError('x1 is not a cocycle')
    for n in range(2, order + 1):
        ob = [F(0)] * A.N
        for i in range(1, n):
            ob = [u + v / 2 for u, v in zip(ob, A.bracket(xs[i - 1], xs[n - i - 1]))]
        rhs = [str(-ob[i]) for i in pieces[2]]
        ans = O.solve(cx, 2 - lo, rhs, max_size=10 ** 6)
        if ans['status'] == 'solved':
            u = [F(r[0]) for r in ans['primitive']['entries']]
            xn = [F(0)] * A.N
            for idx, val in zip(pieces[1], u):
                xn[idx] = val
            xs.append(xn)
        elif ans['status'] == 'obstructed':
            f = [F(0)] * A.N
            for idx, val in zip(pieces[2], ans['functional']['entries'][0]):
                f[idx] = F(val)
            cert.update(status='obstructed', jet=[[str(c) for c in x] for x in xs],
                        functional=[str(c) for c in f], order=n)
            cert['result'] = C.check(cert, model)
            return cert
        else:
            raise ValueError('unexpected answer ' + ans['status'])
    cert.update(status='lifted', jet=[[str(c) for c in x] for x in xs], order=order,
                complement_choice='x_n = h(-ob_n) with h from the rational contraction; any cocycle may be added')
    cert['result'] = C.check(cert, model)
    return cert


# ---- Chevalley-Eilenberg / Nijenhuis-Richardson model ------------------------

def _eval(P, args, n):
    """Alternating P (dict sorted-tuple -> vector) on basis-vector arguments (list of dict index->coef)."""
    out = [F(0)] * n
    for choice in itertools.product(*[list(a.items()) for a in args]):
        idx = [i for i, _ in choice]
        if len(set(idx)) < len(idx):
            continue
        coef = F(1)
        for _, c in choice:
            coef *= c
        perm = sorted(range(len(idx)), key=lambda t: idx[t])
        sign = 1
        seen = list(perm)
        for i in range(len(seen)):          # parity of the sorting permutation
            while seen[i] != i:
                j = seen[i]
                seen[i], seen[j] = seen[j], seen[i]
                sign = -sign
        v = P.get(tuple(sorted(idx)))
        if v:
            for m, c in enumerate(v):
                out[m] += sign * coef * c
    return out


def _compose(P, p, Q, q, n):
    """(P o Q)(x_0..x_(p+q)) = sum over (q+1,p)-shuffles sgn * P(Q(x_S), x_rest)."""
    out = {}
    for tup in itertools.combinations(range(n), p + q + 1):
        total = [F(0)] * n
        for S in itertools.combinations(range(p + q + 1), q + 1):
            rest = [t for t in range(p + q + 1) if t not in S]
            perm = list(S) + rest
            inv = sum(1 for a in range(len(perm)) for b in range(a + 1, len(perm)) if perm[a] > perm[b])
            sgn = -1 if inv % 2 else 1
            qv = _eval(Q, [{tup[s]: F(1)} for s in S], n)
            if not any(qv):
                continue
            arg0 = {m: c for m, c in enumerate(qv) if c}
            pv = _eval(P, [arg0] + [{tup[r]: F(1)} for r in rest], n)
            total = [a + sgn * b for a, b in zip(total, pv)]
        if any(total):
            out[tup] = total
    return out


def nr_bracket(P, p, Q, q, n):
    a, b = _compose(P, p, Q, q, n), _compose(Q, q, P, p, n)
    s = (-1) ** (p * q)
    keys = set(a) | set(b)
    out = {}
    for k in keys:
        v = [x - s * y for x, y in zip(a.get(k, [F(0)] * n), b.get(k, [F(0)] * n))]
        if any(v):
            out[k] = v
    return out


def lie_deformation_dgla(n, structure, max_degree=2):
    """structure: {(i,j): {k: c}} for i<j, the bracket mu of an n-dim Lie algebra."""
    basis = []                       # (degree, sorted tuple, output index)
    for k in range(0, max_degree + 1):
        for tup in itertools.combinations(range(n), k + 1):
            for m in range(n):
                basis.append((k, tup, m))
    pos = {b: i for i, b in enumerate(basis)}
    N = len(basis)
    mu = {}
    for (i, j), out in structure.items():
        v = [F(0)] * n
        for k, c in out.items():
            v[k] += F(c)
        mu[(i, j)] = v

    def cochain(b):
        k, tup, m = b
        return {tup: [F(int(t == m)) for t in range(n)]}

    def expand(cc, k):
        vec = [F(0)] * N
        for tup, v in cc.items():
            for m, c in enumerate(v):
                if c:
                    vec[pos[(k, tup, m)]] += c
        return vec
    if nr_bracket(mu, 1, mu, 1, n):
        raise ValueError('structure constants do not satisfy Jacobi')
    bracket = []
    for i in range(N):
        for j in range(i, N):
            (ki, _, _), (kj, _, _) = basis[i], basis[j]
            if ki + kj > max_degree:
                continue
            v = expand(nr_bracket(cochain(basis[i]), ki, cochain(basis[j]), kj, n), ki + kj)
            terms = [[k, str(c)] for k, c in enumerate(v) if c]
            if terms:
                bracket.append([i, j, terms])
    d = [[F(0)] * N for _ in range(N)]
    for j in range(N):
        kj = basis[j][0]
        if kj + 1 > max_degree:
            continue
        v = expand(nr_bracket(mu, 1, cochain(basis[j]), kj, n), kj + 1)
        for i, c in enumerate(v):
            d[i][j] = c
    return {'schema': 'dgla-v1', 'field': 'Q',
            'basis': [{'degree': k, 'name': 'e' + ''.join(map(str, tup)) + '->' + str(m)} for k, tup, m in basis],
            'differential': [[str(c) for c in r] for r in d], 'bracket': bracket,
            'truncation': f'degrees 0..{max_degree}; brackets landing above degree {max_degree} are dropped'}


def two_cochain(n, structure, model):
    """Vector in L^1 of the dgla model for a 2-cochain given as {(i,j): {k: c}}."""
    names = {b['name']: i for i, b in enumerate(model['basis'])}
    v = [F(0)] * len(model['basis'])
    for (i, j), out in structure.items():
        for k, c in out.items():
            v[names[f'e{i}{j}->{k}']] += F(c)
    return v


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    l = sub.add_parser('lift')
    l.add_argument('model', type=Path)
    l.add_argument('--x1', required=True)
    l.add_argument('--order', type=int, default=4)
    l.add_argument('--output', type=Path)
    g = sub.add_parser('lie')
    g.add_argument('--dim', type=int, required=True)
    g.add_argument('--structure', required=True, help='JSON {"i,j": {"k": c}}')
    g.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == 'lie':
        st = {tuple(map(int, k.split(','))): {int(m): c for m, c in v.items()} for k, v in json.loads(a.structure).items()}
        a.output.write_text(json.dumps(lie_deformation_dgla(a.dim, st), indent=1) + '\n')
        print(json.dumps({'status': 'written', 'path': str(a.output)}))
        return
    model = json.loads(a.model.read_text())
    cert = lift(model, json.loads(a.x1), a.order)
    if a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    print(json.dumps(cert['result'], indent=2))


if __name__ == '__main__':
    main()
