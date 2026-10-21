#!/usr/bin/env python3
"""Independent checker for finite DGLA Maurer-Cartan lifting certificates (dgla-lift-v1).

Model (dgla-v1, over Q): a graded basis b_0..b_(N-1) with integer degrees, a differential
matrix d (column j = d b_j, degree +1) and structure constants [b_i, b_j] for i <= j; the
other order follows from graded antisymmetry [x,y] = -(-1)^{|x||y|} [y,x].

The checker verifies, on basis elements, that the data form a DGLA:
  degrees      d raises degree by 1, [L^i, L^j] lands in L^(i+j);
  d^2 = 0;     Leibniz d[x,y] = [dx,y] + (-1)^{|x|} [x,dy];
  Jacobi       [x,[y,z]] = [[x,y],z] + (-1)^{|x||y|} [y,[x,z]];
then checks the lifting claim for x = sum_{n>=1} x_n t^n with x_n in L^1:
  every order m <= M:  d x_m + (1/2) sum_{i+j=m} [x_i, x_j] = 0;
  obstruction at order n (if claimed): a functional f on L^2 with f(d y) = 0 for every
  y in L^1 and f(ob_n) != 0, where ob_n = (1/2) sum_{i+j=n} [x_i, x_j]. Then no x_n in L^1
  solves d x_n = -ob_n, so the declared jet x_1..x_(n-1) does not extend to order n.
At order 2 the obstruction class [ob_2] = (1/2)[[x_1, x_1]] depends only on the class of x_1
(x_1 + dy changes [x_1,x_1] by a coboundary), so an order-2 witness obstructs every jet with
first-order class [x_1]; at higher orders the witness is relative to the declared jet.
No convergence or moduli statement is made.

Usage: check_dgla.py CERT.json --input MODEL.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

FORMAT = 'dgla-lift-v1'


def _rat(x):
    if type(x) not in (int, str) and not isinstance(x, F):
        raise ValueError('coefficients must be exact')
    return F(x)


def digest(model):
    return hashlib.sha256(json.dumps(model, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read(model):
    if model.get('field') != 'Q' or model.get('schema') != 'dgla-v1':
        raise ValueError('need a dgla-v1 model over Q')
    deg = [b['degree'] for b in model['basis']]
    if any(type(x) is not int for x in deg):
        raise ValueError('degrees must be integers')
    N = len(deg)
    d = [[_rat(x) for x in r] for r in model['differential']]
    if len(d) != N or any(len(r) != N for r in d):
        raise ValueError('differential must be N x N')
    br = {}
    for i, j, terms in model['bracket']:
        if not (type(i) is int and type(j) is int and 0 <= i <= j < N) or (i, j) in br:
            raise ValueError('bracket entries need 0 <= i <= j < N, each pair once')
        v = [F(0)] * N
        for k, c in terms:
            v[k] += _rat(c)
        br[(i, j)] = v
    return deg, d, br


class Algebra:
    def __init__(self, model):
        self.deg, self.d, self.br = read(model)
        self.N = len(self.deg)
        N, deg = self.N, self.deg
        for j in range(N):
            for i in range(N):
                if self.d[i][j] and deg[i] != deg[j] + 1:
                    raise ValueError('d must raise degree by one')
        for (i, j), v in self.br.items():
            if any(c and deg[k] != deg[i] + deg[j] for k, c in enumerate(v)):
                raise ValueError('bracket must be additive in degree')
            if i == j and deg[i] % 2 == 0 and any(v):
                raise ValueError('[x,x] must vanish for even x')

    def basis_bracket(self, i, j):
        if i <= j:
            return self.br.get((i, j), [F(0)] * self.N)
        s = -(-1) ** (self.deg[i] * self.deg[j])
        return [s * c for c in self.br.get((j, i), [F(0)] * self.N)]

    def bracket(self, x, y):
        out = [F(0)] * self.N
        for i, a in enumerate(x):
            if a:
                for j, b in enumerate(y):
                    if b:
                        for k, c in enumerate(self.basis_bracket(i, j)):
                            if c:
                                out[k] += a * b * c
        return out

    def dif(self, x):
        return [sum((self.d[i][j] * x[j] for j in range(self.N)), F(0)) for i in range(self.N)]

    def e(self, i):
        return [F(int(k == i)) for k in range(self.N)]

    def verify_structure(self):
        N, deg = self.N, self.deg
        for j in range(N):
            if any(self.dif(self.dif(self.e(j)))):
                raise ValueError('d^2 != 0')
        for i in range(N):
            for j in range(N):
                x, y = self.e(i), self.e(j)
                lhs = self.dif(self.bracket(x, y))
                r1, r2 = self.bracket(self.dif(x), y), self.bracket(x, self.dif(y))
                if lhs != [a + (-1) ** deg[i] * b for a, b in zip(r1, r2)]:
                    raise ValueError(f'Leibniz fails on ({i},{j})')
        for i in range(N):
            for j in range(N):
                xy = self.bracket(self.e(i), self.e(j))
                for k in range(N):
                    lhs = self.bracket(self.e(i), self.bracket(self.e(j), self.e(k)))
                    a = self.bracket(xy, self.e(k))
                    b = self.bracket(self.e(j), self.bracket(self.e(i), self.e(k)))
                    if lhs != [u + (-1) ** (deg[i] * deg[j]) * v for u, v in zip(a, b)]:
                        raise ValueError(f'Jacobi fails on ({i},{j},{k})')
        return N


def check(cert, model):
    if cert.get('format') != FORMAT or cert.get('coefficient_domain') != 'Q':
        raise ValueError('not a dgla-lift-v1 certificate over Q')
    if cert.get('model_sha256') != digest(model):
        raise ValueError('certificate belongs to another model')
    A = Algebra(model)
    A.verify_structure()
    xs = [[_rat(c) for c in x] for x in cert['jet']]
    if not xs or any(len(x) != A.N or any(c and A.deg[k] != 1 for k, c in enumerate(x)) for x in xs):
        raise ValueError('jet terms must lie in L^1')

    def ob(n):
        out = [F(0)] * A.N
        for i in range(1, n):
            out = [u + v / 2 for u, v in zip(out, A.bracket(xs[i - 1], xs[n - i - 1]))]
        return out
    for m in range(1, len(xs) + 1):
        if any(u + v for u, v in zip(A.dif(xs[m - 1]), ob(m))):
            raise ValueError(f'Maurer-Cartan equation fails at order {m}')
    status = cert['status']
    if status == 'lifted':
        return {'status': 'passed', 'claim': 'lifted', 'order': len(xs),
                'scope': 'x = sum x_n t^n solves dx + [x,x]/2 = 0 modulo t^(order+1); no convergence claim'}
    if status == 'obstructed':
        n = len(xs) + 1
        f = [_rat(c) for c in cert['functional']]
        if len(f) != A.N or any(c and A.deg[k] != 2 for k, c in enumerate(f)):
            raise ValueError('functional must live on L^2')
        for j in range(A.N):
            if A.deg[j] == 1 and sum((a * b for a, b in zip(f, A.dif(A.e(j)))), F(0)):
                raise ValueError('functional does not vanish on d(L^1)')
        if not sum((a * b for a, b in zip(f, ob(n))), F(0)):
            raise ValueError('functional does not detect the obstruction')
        return {'status': 'passed', 'claim': 'obstructed', 'order': n,
                'intrinsic': n == 2,
                'scope': ('no extension to order 2 for any jet with this first-order class' if n == 2 else
                          f'the declared jet does not extend to order {n}; other jets with the same '
                          'first-order class are not covered')}
    raise ValueError('unknown status')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--input', type=Path, required=True)
    a = ap.parse_args()
    try:
        print(json.dumps(check(json.loads(a.certificate.read_text()), json.loads(a.input.read_text())), indent=2))
    except (ValueError, KeyError, TypeError, IndexError) as e:
        print(json.dumps({'status': 'rejected', 'reason': str(e)}))
        sys.exit(2)


if __name__ == '__main__':
    main()
