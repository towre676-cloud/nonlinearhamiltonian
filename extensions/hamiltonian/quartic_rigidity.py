#!/usr/bin/env python3
"""Produce quartic-rigidity-v1 certificates: for each degree n, the one-step space S_n(l) of
H_l = q^4 + l q^2 p^2 + p^4 over all l in Qbar (see check_quartic_rigidity.py).

Minor polynomials come from integer Bareiss determinants at integer points and Newton
interpolation; the gcd is split into squarefree parts (Yun) and further by dynamic evaluation
whenever a zero divisor appears while computing the rank over Q[x]/(f).

Usage: quartic_rigidity.py N [--output CERT.json]   (degrees 1..N)
"""
from __future__ import annotations
import argparse
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import check_quartic_rigidity as C  # noqa: E402  (matrix family and polynomial helpers)
import qlinalg as L                 # noqa: E402


def idet(M):
    M = [r[:] for r in M]
    n, sign, prev = len(M), 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            p = next((i for i in range(k + 1, n) if M[i][k]), None)
            if p is None:
                return 0
            M[k], M[p] = M[p], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[-1][-1] if n else 1


def newton(xs, ys):
    n, coef = len(xs), [F(y) for y in ys]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (xs[i] - xs[i - j])
    res = [F(0)]
    for i in range(n - 1, -1, -1):
        new = [F(0)] * (len(res) + 1)
        for k, c in enumerate(res):
            new[k + 1] += c
            new[k] -= xs[i] * c
        new[0] += coef[i]
        res = new
    return C.pnorm(res)


def derivative(p):
    return C.pnorm([k * c for k, c in enumerate(p)][1:] or [F(0)])


def yun(g):
    """Squarefree decomposition: list of (factor, multiplicity)."""
    out, i = [], 1
    a = C.pgcd(g, derivative(g)) if len(g) > 2 else [F(1)]
    b = C.pdivmod(g, a)[0]
    while len(b) > 1:
        c = C.pgcd(a, b)
        f = C.pdivmod(b, c)[0]
        if len(f) > 1:
            out.append(([x / f[-1] for x in f], i))
        a, b, i = C.pdivmod(a, c)[0], c, i + 1
    return out


def split_rank(mats, f):
    """[(factor, rank)] covering f, splitting on zero divisors."""
    try:
        return [(f, C.nf_rank(mats, f))]
    except ValueError:
        pass
    # find a nontrivial factor: retry elimination tracking the offending element
    K = C.NF(f)
    M = [[K.red([m[i][j] for m in mats]) for j in range(len(mats[0][0]))] for i in range(len(mats[0]))]
    for row in M:
        for e in row:
            if any(e):
                g = C.pgcd(f, e)
                if 1 < len(g) < len(f):
                    h = C.pdivmod(f, g)[0]
                    return split_rank(mats, g) + split_rank(mats, [x / h[-1] for x in h])
    # fall back: entries were fine but pivot products were not; try leading-principal-like products
    raise ValueError('could not split a reducible factor; increase effort')


def degree_entry(n, depth, subsets=3, seed=0):
    rng = random.Random(seed + n)
    keys, mats = C.family_matrix_parts(n, depth)
    M0 = C.evaluate(mats, F(1, 3))
    generic = L.rank(M0, n + 1)
    red, piv = L.rref(L.transpose(M0, n + 1), len(M0))      # independent rows of M0 = pivots of M0^T
    _, colpiv = L.rref(M0, n + 1)
    cols = colpiv[:generic]
    entry = {'n': n, 'depth': depth, 'generic_rank': generic, 'column_subset': cols, 'row_subsets': [], 'minors': []}
    g = None
    cache = {}
    for _ in range(subsets):
        order = list(range(len(M0)))
        rng.shuffle(order)
        rows, cur = [], []
        for i in order:
            cand = cur + [[M0[i][j] for j in cols]]
            if L.rank(cand, generic) > len(cur):
                cur, rows = cand, rows + [i]
            if len(rows) == generic:
                break
        deg = sum(C.row_degree(keys[i]) for i in rows)
        xs = list(range(-(deg // 2) - 1, deg + 2))[:deg + 1]
        ys = []
        for x in xs:
            if x not in cache:
                cache[x] = [[int(v) for v in r] for r in C.evaluate(mats, F(x))]
            ys.append(idet([[cache[x][i][j] for j in cols] for i in rows]))
        poly = newton([F(x) for x in xs], ys)
        entry['row_subsets'].append(rows)
        entry['minors'].append([str(c) for c in poly])
        g = poly if g is None else C.pgcd(g, poly)
    g = [c / g[-1] for c in g]
    entry['gcd'] = [str(c) for c in g]
    factors = []
    for f, mult in yun(g):
        for piece, r in split_rank(mats, f):
            factors.append({'poly': [str(c) for c in piece], 'multiplicity': mult, 'rank': r})
    entry['factors'] = factors
    if generic < n + 1:
        if n != 4 or generic != 4:
            raise ValueError(f'unexpected generic corank in degree {n}')
        entry['kernel_vectors'] = [[['1'], ['0'], ['0', '1'], ['0'], ['1']]]      # H_l itself
    return entry


SQUARE = ['-4', '0', '1']          # l^2 = 4: the square stratum (q^2 +- p^2)^2, not distinct roots


def adaptive_entry(n, max_depth=6):
    """Smallest depth after which every exceptional factor other than l^2 - 4 has full rank."""
    for depth in range(1, max_depth + 1):
        e = degree_entry(n, depth)
        target = e['generic_rank']
        bad = [f for f in e['factors'] if f['rank'] < target and f['poly'] != SQUARE]
        if not bad:
            return e
    return e


def build(N, max_depth=6):
    cert = {'format': C.FORMAT, 'family': 'q^4 + l*q^2*p^2 + p^4',
            'degrees': [adaptive_entry(n, max_depth) for n in range(1, N + 1)]}
    cert['result'] = C.check(cert)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('N', type=int)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    cert = build(a.N)
    if a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
    summary = [(d['n'], d['depth'], d['generic_kernel_dimension'], [(e['factor'], e['kernel_dimension']) for e in d['exceptions']])
               for d in cert['result']['degrees']]
    print(json.dumps({'status': cert['result']['status'], 'summary': summary}))


if __name__ == '__main__':
    main()
