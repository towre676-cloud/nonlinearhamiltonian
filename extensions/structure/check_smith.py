#!/usr/bin/env python3
"""Independent checker for integral cochain-complex certificates (integer-smith-v1).

Model: {"field": "Z", "dimensions": [n_0..n_m], "differentials": [d_0..d_(m-1)]}, d_k an
n_(k+1) x n_k integer matrix, d_(k+1) d_k = 0.

Certificate, per differential d_k: integer matrices P, Pinv (n_(k+1) square), Q, Qinv (n_k
square) with P Pinv = I, Q Qinv = I (so P, Q are unimodular) and P d_k Q = S, S diagonal
with positive invariant factors s_1 | s_2 | ... | s_r followed by zeros. The checker then
derives, with no elimination of its own,
    H^k(C; Z) = Z^(n_k - r_k - r_(k-1))  +  sum over s_i > 1 of Z/s_i  (s_i from d_(k-1)),
and replays integer answers for a cocycle b in degree k:
    exact       u with d_(k-1) u = b (integers);
    rational    a functional f with f d_(k-1) = 0 and f b != 0 (b is not exact even over Q);
    torsion     a modulus m > 1 and functional f with f d_(k-1) = 0 mod m, f b != 0 mod m: a
                Z/m-valued cochain functional vanishing on all coboundaries, so b is not an
                integral coboundary although it may be a rational one.
Usage: check_smith.py CERT.json --input MODEL.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

FORMAT = 'integer-smith-v1'


def digest(model):
    return hashlib.sha256(json.dumps(model, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def imat(rows, r, c):
    if not isinstance(rows, list) or len(rows) != r or any(not isinstance(x, list) or len(x) != c for x in rows):
        raise ValueError('matrix shape mismatch')
    if any(type(v) is not int for x in rows for v in x):
        raise ValueError('integer entries required')
    return rows


def mul(a, b, c):
    return [[sum(x * b[k][j] for k, x in enumerate(row)) for j in range(c)] for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def read(model):
    if model.get('field') != 'Z':
        raise ValueError('integer-smith-v1 models declare field Z')
    n = model['dimensions']
    if not n or any(type(x) is not int or x < 0 for x in n) or len(model['differentials']) != len(n) - 1:
        raise ValueError('invalid dimensions or differential count')
    d = [imat(x, n[k + 1], n[k]) for k, x in enumerate(model['differentials'])]
    for k in range(len(d) - 1):
        if any(any(r) for r in mul(d[k + 1], d[k], n[k])):
            raise ValueError(f'd^2 != 0 at degree {k}')
    return n, d


def check_snf(dk, rows, cols, s):
    P, Pi = imat(s['P'], rows, rows), imat(s['Pinv'], rows, rows)
    Q, Qi = imat(s['Q'], cols, cols), imat(s['Qinv'], cols, cols)
    if mul(P, Pi, rows) != eye(rows) or mul(Q, Qi, cols) != eye(cols):
        raise ValueError('transforms are not unimodular (inverse identity fails)')
    S = mul(mul(P, dk, cols), Q, cols)
    inv = s['invariants']
    r = len(inv)
    if any(type(v) is not int or v <= 0 for v in inv) or any(inv[i + 1] % inv[i] for i in range(r - 1)):
        raise ValueError('invariant factors must be positive and successively divisible')
    want = [[inv[i] if i == j and i < r else 0 for j in range(cols)] for i in range(rows)]
    if S != want:
        raise ValueError('P d Q is not the declared Smith form')
    return r, inv


def check(cert, model):
    if cert.get('format') != FORMAT or cert.get('model_sha256') != digest(model):
        raise ValueError('not an integer-smith-v1 certificate for this model')
    n, d = read(model)
    if len(cert['smith']) != len(d):
        raise ValueError('one Smith certificate per differential')
    ranks, invs = [], []
    for k, s in enumerate(cert['smith']):
        r, inv = check_snf(d[k], n[k + 1], n[k], s)
        ranks.append(r)
        invs.append(inv)
    groups = []
    for k in range(len(n)):
        r_out = ranks[k] if k < len(d) else 0
        r_in = ranks[k - 1] if k else 0
        tors = [v for v in invs[k - 1] if v > 1] if k else []
        groups.append({'degree': k, 'rank': n[k] - r_out - r_in, 'torsion': tors})
    if cert['cohomology'] != groups:
        raise ValueError('declared cohomology differs from the certified Smith data')
    answers = []
    for ans in cert.get('answers', []):
        k, b = ans['degree'], ans['cocycle']
        if not 0 <= k < len(n) or len(b) != n[k] or any(type(v) is not int for v in b):
            raise ValueError('malformed cocycle')
        if k < len(d) and any(sum(x * y for x, y in zip(row, b)) for row in d[k]):
            raise ValueError('not a cocycle')
        st = ans['status']
        if st == 'exact':
            u = ans['primitive']
            img = [sum(x * y for x, y in zip(row, u)) for row in d[k - 1]] if k else [0] * n[0]
            if any(type(v) is not int for v in u) or img != b:
                raise ValueError('integer primitive fails')
        elif st in ('rational', 'torsion'):
            f, m = ans['functional'], ans.get('modulus', 0)
            if st == 'torsion' and (type(m) is not int or m < 2):
                raise ValueError('torsion witness needs a modulus >= 2')
            red = (lambda v: v % m) if st == 'torsion' else (lambda v: v)
            if k and any(red(sum(f[i] * d[k - 1][i][j] for i in range(n[k]))) for j in range(n[k - 1])):
                raise ValueError('functional does not vanish on coboundaries')
            if not red(sum(x * y for x, y in zip(f, b))):
                raise ValueError('functional does not detect the cocycle')
        else:
            raise ValueError('unknown answer status')
        answers.append(st)
    return {'status': 'passed', 'cohomology': groups, 'answers': answers,
            'scope': 'integral cohomology of the finite integer cochain complex; answers are exact over Z'}


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
