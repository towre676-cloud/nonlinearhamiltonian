#!/usr/bin/env python3
"""Produce binary-static-v1 certificates (static finiteness at a simple root, d = 5, 6).

The producer searches for elimination trees with sympy (an optional dependency used only
here); every step it emits is an explicit polynomial identity that check_binary_static.py
replays with its own arithmetic. See the checker for the statement and proof structure.

Usage: binary_static.py DEGREE [--output CERT.json] [--N0 N]
"""
from __future__ import annotations
import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_binary_static as C  # noqa: E402


class Ctx:
    def __init__(self, d):
        self.d = d
        self.nv = d - 1
        self.n = sp.Symbol('n')
        self.hs = sp.symbols(' '.join(f'h{j}' for j in range(3, d + 1)))
        self.gens = (self.n,) + tuple(self.hs)
        self.npolys = []          # every n-only polynomial that must be nonzero for n >= N0

    def to_sp(self, p):
        return sp.Add(*[sp.Rational(v.numerator, v.denominator) * sp.Mul(*[g ** e for g, e in zip(self.gens, k)])
                        for k, v in p.items()]) if p else sp.Integer(0)

    def ser(self, e):
        e = sp.expand(e)
        if e == 0:
            return []
        P = sp.Poly(e, *self.gens)
        return [[[int(x) for x in m], str(sp.Rational(c))] for m, c in P.terms()]

    def is_n_only(self, e):
        return e.free_symbols <= {self.n}

    def hvars(self, e):
        return [h for h in self.hs if h in e.free_symbols]


def strip_rows(ctx, rows):
    out = []
    for A, B, den in rows:
        a, b = ctx.to_sp(A), ctx.to_sp(B)
        parts = [x for x in (a, b) if x != 0]
        g = parts[0]
        for x in parts[1:]:
            g = sp.gcd(g, x)
        # keep only the part of the gcd that depends on n alone
        cont = sp.Integer(1)
        for fac, m in sp.factor_list(g)[1]:
            if ctx.is_n_only(fac):
                cont *= fac ** m
        cont *= sp.factor_list(g)[0]
        a2, b2 = sp.cancel(a / cont), sp.cancel(b / cont)
        ctx.npolys.append(cont)
        ctx.npolys.append(ctx.to_sp(den))
        out.append({'A': ctx.ser(a2), 'B': ctx.ser(b2), 'scale': ctx.ser(cont), '_a': sp.expand(a2), '_b': sp.expand(b2)})
    return out


class Builder:
    def __init__(self, ctx, J):
        self.ctx, self.J = ctx, J

    def derive(self, L, P, combo, steps):
        steps.append({'op': 'derive', 'poly': self.ctx.ser(P), 'combo': [[i, self.ctx.ser(m)] for i, m in combo]})
        L.append(sp.expand(P))
        return len(L) - 1

    def factor_split(self, L, idx):
        """Return (const, [(q, m)]) for L[idx] with n-only part folded into const."""
        c0, facs = sp.factor_list(L[idx])
        const, rest = sp.Integer(c0), []
        for f, m in facs:
            if self.ctx.is_n_only(f):
                const *= f ** m
            else:
                rest.append((f, m))
        return const, rest

    def build(self, L, active, subs, depth=0):
        """L: all known polynomials (sympy); active: indices of the current system;
        subs: list of (index of linear polynomial, variable, coefficient c(n))."""
        ctx = self.ctx
        steps = []
        if depth > 40:
            raise RuntimeError('tree too deep')
        active = [i for i in active if L[i] != 0]
        # leaf: an n-only nonzero polynomial
        for i in active:
            if ctx.is_n_only(L[i]):
                ctx.npolys.append(L[i])
                steps.append({'op': 'contradiction', 'idx': i})
                return steps
        if not active or all(not ctx.hvars(L[i]) for i in active):
            return steps + self.target(L, subs)
        # split reducible polynomials
        for i in active:
            const, rest = self.factor_split(L, i)
            if len(rest) > 1 or (rest and rest[0][1] > 1):
                ctx.npolys.append(const)
                branches = []
                for q, m in rest:
                    L2 = L + [sp.expand(q)]
                    branches.append(self.build(L2, [j for j in active if j != i] + [len(L2) - 1], subs, depth + 1))
                steps.append({'op': 'split', 'idx': i, 'const': ctx.ser(const),
                              'factors': [[ctx.ser(q), int(m)] for q, m in rest], 'branches': branches})
                return steps
        # linear substitution with a coefficient in n alone
        best = None
        for i in active:
            for v in ctx.hvars(L[i]):
                P = sp.Poly(L[i], v)
                if P.degree() == 1 and ctx.is_n_only(P.coeffs()[0]):
                    size = len(sp.Poly(L[i], *ctx.gens).terms())
                    if best is None or size < best[0]:
                        best = (size, i, v, P.coeffs()[0], P.coeffs()[1] if len(P.coeffs()) > 1 else 0)
        if best:
            _, i, v, c, r = best
            r = sp.expand(L[i] - c * v)
            ctx.npolys.append(c)
            new = []
            for j in active:
                if j == i:
                    continue
                if v not in L[j].free_symbols:
                    new.append(j)
                    continue
                red, Q, k = psubst(ctx, L[j], v, r, c, L[i])
                new.append(self.derive(L, red, [(j, c ** k), (i, -Q)], steps))
            return steps + self.build(L, new, subs + [(i, v, c)], depth + 1)
        # resultant of two polynomials in a common variable of least degree
        cands = []
        for a in active:
            for b in active:
                if a >= b:
                    continue
                for v in set(ctx.hvars(L[a])) & set(ctx.hvars(L[b])):
                    da, db = sp.Poly(L[a], v).degree(), sp.Poly(L[b], v).degree()
                    cands.append((da * db, len(str(L[a])) + len(str(L[b])), a, b, v))
        for _, _, a, b, v in sorted(cands, key=lambda x: (x[0], x[1])):
            r, A, B = resultant_cofactors(L[a], L[b], v)
            if r == 0:
                continue
            k = self.derive(L, r, [(a, A), (b, B)], steps)
            return steps + self.build(L, active + [k], subs, depth + 1)
        raise RuntimeError('no elimination step applies')

    def target(self, L, subs):
        """All h variables are eliminated by linear substitutions: reduce every J_j."""
        ctx = self.ctx
        steps, idxs, consts = [], [], []
        for Jj in self.J:
            cur, mults, C = sp.expand(Jj), {}, sp.Integer(1)
            # cur = C * J - sum mults[i] L[i] at every stage
            for i, v, c in subs:
                if v not in cur.free_symbols:
                    continue
                r = sp.expand(L[i] - c * v)
                red, Q, k = psubst(ctx, cur, v, r, c, L[i])
                mults = {j: c ** k * m for j, m in mults.items()}
                mults[i] = mults.get(i, 0) + Q
                C, cur = C * c ** k, red
            if cur != 0:
                raise RuntimeError(f'J generator does not vanish on a branch: {cur}')
            ctx.npolys.append(C)
            idx = self.derive(L, C * Jj, [(i, m) for i, m in mults.items()], steps)
            idxs.append(idx)
            consts.append(ctx.ser(C))
        steps.append({'op': 'target', 'idx': idxs, 'const': consts})
        return steps


def psubst(ctx, g, v, r, c, f):
    """red = c^k g(v = -r/c) and Q with c^k g = Q f + red, where f = c v + r (sparse arithmetic)."""
    gens = ctx.gens
    G = sp.Poly(g, v)
    k = G.degree()
    coeffs = G.all_coeffs()                       # highest first
    R_ = sp.Poly(-r, *gens)
    Cc = sp.Poly(c, *gens)
    red = sp.Poly(0, *gens)
    pw_r = sp.Poly(1, *gens)
    for i in range(k + 1):                        # coefficient of v^i is coeffs[k - i]
        a = sp.Poly(coeffs[k - i], *gens)
        red += a * pw_r * Cc ** (k - i)
        pw_r = pw_r * R_
    lhs = Cc ** k * sp.Poly(g, *gens) - red
    Q, rem = sp.div(lhs, sp.Poly(f, *gens))
    if not rem.is_zero:
        raise RuntimeError('pseudo-division failed')
    return red.as_expr(), Q.as_expr(), k


def resultant_cofactors(f, g, v):
    """r = A f + B g with r = Res_v(f, g), via the last column of the Sylvester matrix."""
    P, Q = sp.Poly(f, v), sp.Poly(g, v)
    a, b = P.degree(), Q.degree()
    pc, qc = P.all_coeffs(), Q.all_coeffs()
    N = a + b
    S = sp.zeros(N, N)
    for i in range(b):
        for j, c in enumerate(pc):
            S[i, i + j] = c
    for i in range(a):
        for j, c in enumerate(qc):
            S[b + i, i + j] = c
    A = sum(S.cofactor(i, N - 1, method='berkowitz') * v ** (b - 1 - i) for i in range(b))
    B = sum(S.cofactor(b + i, N - 1, method='berkowitz') * v ** (a - 1 - i) for i in range(a))
    r = sp.expand(A * f + B * g)
    if r.has(v):
        raise RuntimeError('cofactor identity failed')
    return r, sp.expand(A), sp.expand(B)


def build(d, N0=None):
    ctx = Ctx(d)
    R = C.ROWS[d]
    rows, used_den, tmax = C.derive_rows(d, R)
    for den in used_den:
        ctx.npolys.append(ctx.to_sp(den))
    srows = strip_rows(ctx, rows)
    J = [ctx.to_sp({(0,) + k: v for k, v in Jj.items()}) for Jj in C.J_EXPECTED[d]]
    systems = []
    cases = [('one', None)] + [(c, k) for c in ('A', 'B') for k in range(d - 2)]
    for case, chart in cases:
        base = []
        for r in srows:
            p = {'one': r['_a'] + r['_b'], 'A': r['_a'], 'B': r['_b']}[case]
            Jc = J
            if chart is not None:
                sub = {ctx.hs[i]: 0 for i in range(chart)}
                sub[ctx.hs[chart]] = 1
                p = p.subs(sub)
            base.append(sp.expand(p))
        Jc = [sp.expand(Jj.subs(sub)) if chart is not None else Jj for Jj in J]
        L = list(base)
        print('system', case, chart, file=sys.stderr, flush=True)
        steps = Builder(ctx, Jc).build(L, list(range(len(L))), [])
        systems.append({'case': case, 'chart': chart, 'steps': steps})
    # N0: beyond every integer root of every n-polynomial that must be nonzero
    worst = tmax + 1
    for p in ctx.npolys:
        p = sp.expand(p)
        if p == 0:
            raise RuntimeError('zero polynomial asserted nonzero')
        roots = [r for r in sp.Poly(p, ctx.n).ground_roots() if r.is_integer] if p.free_symbols else []
        if roots:
            worst = max(worst, int(max(roots)) + 1)
    N0 = max(worst, N0 or 0)
    for r in srows:
        r.pop('_a'), r.pop('_b')
    cert = {'format': C.FORMAT, 'degree': d, 'N0': N0, 'rows': srows, 'systems': systems}
    cert['result'] = C.check(cert)
    return cert


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('degree', type=int)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--N0', type=int)
    a = ap.parse_args()
    cert = build(a.degree, a.N0)
    if a.output:
        a.output.write_text(json.dumps(cert) + '\n')
    print(json.dumps(cert['result'], indent=1))


if __name__ == '__main__':
    main()
