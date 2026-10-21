#!/usr/bin/env python3
"""Integral cohomology and integer coboundary decisions via Smith normal form (producer).

For each differential d_k it records unimodular P, Q (with inverses) such that P d_k Q is the
Smith form, derives H^k(C; Z) = free rank + torsion, and for supplied integer cocycles returns
an integer primitive, a rational obstruction functional, or a torsion functional mod s_i.
Every certificate is replayed by check_smith.py. A size budget returns 'unknown'.

Usage: smith.py MODEL.json [--cocycle K '[...]'] [--output CERT.json]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_smith as C  # noqa: E402


class SNF:
    def __init__(self, A):
        self.m, self.n = len(A), (len(A[0]) if A else 0)
        self.A = [r[:] for r in A]
        self.P, self.Pi = C.eye(self.m), C.eye(self.m)
        self.Q, self.Qi = C.eye(self.n), C.eye(self.n)

    # Row ops act as A <- E A, P <- E P, Pinv <- Pinv E^-1; column ops dually.
    def rswap(self, i, j):
        for M in (self.A, self.P):
            M[i], M[j] = M[j], M[i]
        for r in self.Pi:
            r[i], r[j] = r[j], r[i]

    def radd(self, i, j, c):          # row i += c * row j
        for M in (self.A, self.P):
            M[i] = [x + c * y for x, y in zip(M[i], M[j])]
        for r in self.Pi:             # column j of Pinv -= c * column i
            r[j] -= c * r[i]

    def rneg(self, i):
        for M in (self.A, self.P):
            M[i] = [-x for x in M[i]]
        for r in self.Pi:
            r[i] = -r[i]

    def cswap(self, i, j):
        for M in (self.A, self.Q):
            for r in M:
                r[i], r[j] = r[j], r[i]
        self.Qi[i], self.Qi[j] = self.Qi[j], self.Qi[i]

    def cadd(self, i, j, c):          # column i += c * column j
        for M in (self.A, self.Q):
            for r in M:
                r[i] += c * r[j]
        self.Qi[j] = [x - c * y for x, y in zip(self.Qi[j], self.Qi[i])]

    def run(self):
        A, t = self.A, 0
        while t < min(self.m, self.n):
            cells = [(abs(A[i][j]), i, j) for i in range(t, self.m) for j in range(t, self.n) if A[i][j]]
            if not cells:
                break
            _, i, j = min(cells)
            self.rswap(t, i)
            self.cswap(t, j)
            while True:
                done = True
                for i in range(t + 1, self.m):
                    if A[i][t]:
                        self.radd(i, t, -(A[i][t] // A[t][t]))
                        if A[i][t]:
                            self.rswap(t, i)
                            done = False
                for j in range(t + 1, self.n):
                    if A[t][j]:
                        self.cadd(j, t, -(A[t][j] // A[t][t]))
                        if A[t][j]:
                            self.cswap(t, j)
                            done = False
                if not done:
                    continue
                bad = next(((i, j) for i in range(t + 1, self.m) for j in range(t + 1, self.n)
                            if A[i][j] % A[t][t]), None)
                if bad is None:
                    break
                self.radd(t, bad[0], 1)       # brings a non-multiple into row t; repeat
            if A[t][t] < 0:
                self.rneg(t)
            t += 1
        return [A[i][i] for i in range(min(self.m, self.n)) if A[i][i]]


def build(model, cocycles=(), max_size=300):
    n, d = C.read(model)
    if sum(n) > max_size:
        return {'status': 'unknown', 'reason': f'total dimension exceeds budget {max_size}'}
    smith, snfs = [], []
    for k, dk in enumerate(d):
        s = SNF(dk)
        inv = s.run()
        snfs.append(s)
        smith.append({'P': s.P, 'Pinv': s.Pi, 'Q': s.Q, 'Qinv': s.Qi, 'invariants': inv})
    cert = {'format': C.FORMAT, 'model_sha256': C.digest(model), 'smith': smith}
    groups = []
    for k in range(len(n)):
        r_out = len(smith[k]['invariants']) if k < len(d) else 0
        r_in = len(smith[k - 1]['invariants']) if k else 0
        groups.append({'degree': k, 'rank': n[k] - r_out - r_in,
                       'torsion': [v for v in smith[k - 1]['invariants'] if v > 1] if k else []})
    cert['cohomology'] = groups
    answers = []
    for k, b in cocycles:
        if k == 0:
            answers.append({'degree': 0, 'cocycle': b, 'status': 'exact', 'primitive': []} if not any(b) else
                           {'degree': 0, 'cocycle': b, 'status': 'rational',
                            'functional': [int(i == next(i for i, v in enumerate(b) if v)) for i in range(n[0])]})
            continue
        s, inv = snfs[k - 1], smith[k - 1]['invariants']
        y = [sum(x * v for x, v in zip(row, b)) for row in s.P]          # y = P b
        r = len(inv)
        free = next((i for i in range(r, n[k]) if y[i]), None)
        if free is not None:
            answers.append({'degree': k, 'cocycle': b, 'status': 'rational', 'functional': s.P[free]})
            continue
        tor = next((i for i in range(r) if y[i] % inv[i]), None)
        if tor is not None:
            answers.append({'degree': k, 'cocycle': b, 'status': 'torsion', 'modulus': inv[tor],
                            'functional': [v % inv[tor] for v in s.P[tor]]})
            continue
        z = [y[i] // inv[i] for i in range(r)] + [0] * (n[k - 1] - r)
        answers.append({'degree': k, 'cocycle': b, 'status': 'exact',
                        'primitive': [sum(row[j] * z[j] for j in range(n[k - 1])) for row in s.Q]})
    cert['answers'] = answers
    cert['result'] = C.check(cert, model)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('model', type=Path)
    ap.add_argument('--cocycle', nargs=2, action='append', metavar=('K', 'VECTOR'), default=[])
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    try:
        cert = build(json.loads(a.model.read_text()), [(int(k), json.loads(v)) for k, v in a.cocycle])
    except (ValueError, KeyError, TypeError) as e:
        print(json.dumps({'status': 'invalid_model', 'reason': str(e)}))
        sys.exit(2)
    if a.output and 'result' in cert:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    print(json.dumps(cert.get('result', cert), indent=2))


if __name__ == '__main__':
    main()
