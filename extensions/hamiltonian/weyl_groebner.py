#!/usr/bin/env python3
"""Fixed-H discovery backend: left Groebner closure of the iterated correction ideal.

For a polynomial Hamiltonian H over Q, with D = {H,.} = H_q dp - H_p dq and the
nonzero higher odd gates C_k = T_k(H,.) (k = 3, 5, ...), this computes a finite
generating set P_1..P_m of the left ideal

    I_inf = sum_{k, s >= 0} W_2 (C_k D^s)   in   W_2 = Q[q,p]<dq,dp>

by alternating left Buchberger completion with reduction of the right products
P_i D, and exports the three receipt families of weyl-invariant-kernel-v1:

    C_k   = sum_i U_ki P_i                (correction containment)
    P_i   = sum_{k,s} V_iks C_k D^s       (iterated-gate provenance)
    P_i D = sum_l A_il P_l                (right-D closure)

The exported certificate is replayed by weyl_receipts.verify_certificate, which
recomputes H, D and every gate itself and does not trust this backend. A budget
exhaustion returns status "unknown"; it never returns a partial certificate as
a classification. Nothing here classifies the polynomial solutions of the ideal;
`bounded_kernel` is a labelled finite-degree diagnostic only.

Usage:
  weyl_groebner.py discover "q*p^3 + q^2" [--output CERT.json] [--max-generators N] [--max-steps N]
                    [--kernel-degree N]
Hamiltonians are written as sums of terms c*q^a*p^b with integer/rational c.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import weyl_receipts as W  # noqa: E402  (exact PBW arithmetic, gate and derivation definitions)


class Budget(Exception):
    pass


# ---------- parsing ----------------------------------------------------------

_TERM = re.compile(r'^([+-]?)(\d+(?:/\d+)?)?\*?((?:[qp](?:\^\d+)?\*?)*)$')


def parse_poly(text):
    """Parse a restricted exact polynomial syntax: sums of [c*]q^a*p^b; no floats."""
    s = text.replace(' ', '')
    if not s or re.search(r'[^0-9qp+\-*/^]', s):
        raise ValueError('unsupported characters in polynomial ' + repr(text))
    terms = re.findall(r'[+-]?[^+-]+', s)
    out = {}
    for t in terms:
        m = _TERM.match(t)
        if not m or (not m.group(2) and not m.group(3)):
            raise ValueError('cannot parse term ' + repr(t))
        c = F(m.group(2) or 1) * (-1 if m.group(1) == '-' else 1)
        a = b = 0
        for var, exp in re.findall(r'([qp])(?:\^(\d+))?', m.group(3)):
            e = int(exp or 1)
            if var == 'q':
                a += e
            else:
                b += e
        out[(a, b)] = out.get((a, b), F(0)) + c
    return W.tidy(out)


def show_poly(G):
    if not G:
        return '0'
    parts = []
    for (a, b), c in sorted(G.items(), key=lambda t: (-(t[0][0] + t[0][1]), -t[0][0])):
        mono = '*'.join(x for x in (f'q^{a}' if a > 1 else 'q' if a else '', f'p^{b}' if b > 1 else 'p' if b else '') if x)
        parts.append(f'{c}*{mono}' if mono and c != 1 else (mono or str(c)))
    return ' + '.join(parts).replace('+ -', '- ')


def show_op(A):
    if not A:
        return '0'
    names = ('q', 'p', 'dq', 'dp')
    parts = []
    for k in sorted(A, key=key, reverse=True):
        mono = '*'.join(f'{n}^{e}' if e > 1 else n for n, e in zip(names, k) if e)
        parts.append(f'({A[k]})*{mono}' if mono else f'({A[k]})')
    return ' + '.join(parts)


# ---------- term order -------------------------------------------------------
# Weight (0,0,1,1) on the derivatives, refined by total degree and then reverse
# lexicographic order. The weight is nonnegative and refined by a graded order, so
# this is a well-order compatible with multiplication; in W_2 the normal-ordering
# corrections are divisors of the leading monomial, hence lm(m*f) = m*lm(f).

def key(e):
    a, b, c, d = e
    return (c + d, a + b + c + d, -d, -c, -b, -a)


def lead(A):
    m = max(A, key=key)
    return m, A[m]


def divides(u, v):
    return all(x <= y for x, y in zip(u, v))


def mono_op(e, c):
    return {tuple(e): F(c)}


def sub_exp(v, u):
    return tuple(y - x for x, y in zip(u, v))


def lcm(u, v):
    return tuple(max(x, y) for x, y in zip(u, v))


# ---------- cofactor bookkeeping ----------------------------------------------
# A tracked element is (op, cof) with op = sum_{src} cof[src] * S_src, where the
# sources are S_(k,s) = C_k D^s. Cofactors are left multipliers in W_2.

def cof_add(*xs):
    out = {}
    for x, c in xs:
        for src, L in x.items():
            out[src] = W.add(out.get(src, {}), W.scale(L, c))
            if not out[src]:
                del out[src]
    return out


def cof_left(M, cof):
    out = {}
    for src, L in cof.items():
        z = W.compose(M, L)
        if z:
            out[src] = z
    return out


def cof_shift(cof):
    """P = sum V S_(k,s)  ==>  P D = sum V S_(k,s+1)."""
    return {(k, s + 1): L for (k, s), L in cof.items()}


class Engine:
    def __init__(self, H, max_generators=60, max_steps=20000, max_degree=60):
        self.H = W.tidy(H)
        self.D = W.derivation(self.H)
        self.C = W.gates(self.H)
        self.max_generators, self.max_steps, self.max_degree = max_generators, max_steps, max_degree
        self.steps = 0
        self.basis = []                     # list of (op, cof)

    def tick(self):
        self.steps += 1
        if self.steps > self.max_steps:
            raise Budget(f'step budget {self.max_steps} exhausted')

    def reduce(self, f, basis, track=True):
        """Full left reduction. Returns (remainder, quotients{i: left multiplier})."""
        quot = {}
        f = dict(f)
        rem = {}
        while f:
            self.tick()
            m, c = lead(f)
            for i, (g, _) in enumerate(basis):
                gm, gc = lead(g)
                if divides(gm, m):
                    t = mono_op(sub_exp(m, gm), c / gc)
                    f = W.add(f, W.scale(W.compose(t, g), -1))
                    if track:
                        quot[i] = W.add(quot.get(i, {}), t)
                    break
            else:
                rem[m] = c
                del f[m]
        return W.tidy(rem), quot

    def insert(self, op, cof, pairs):
        if len(self.basis) >= self.max_generators:
            raise Budget(f'generator budget {self.max_generators} exhausted')
        if max(sum(e) for e in op) > self.max_degree:
            raise Budget(f'operator degree budget {self.max_degree} exhausted')
        m, c = lead(op)
        op, cof = W.scale(op, 1 / c), cof_add((cof, 1 / c))
        j = len(self.basis)
        self.basis.append((op, cof))
        pairs.extend((i, j) for i in range(j))

    def reduce_tracked(self, op, cof):
        rem, quot = self.reduce(op, self.basis)
        if not rem:
            return rem, {}
        new_cof = cof_add((cof, 1), *((cof_left(L, self.basis[i][1]), -1) for i, L in quot.items()))
        return rem, new_cof

    def complete(self, pairs):
        while pairs:
            i, j = pairs.pop(0)
            (f, fc), (g, gc) = self.basis[i], self.basis[j]
            fm, _ = lead(f)
            gm, _ = lead(g)
            l = lcm(fm, gm)
            tf, tg = mono_op(sub_exp(l, fm), 1), mono_op(sub_exp(l, gm), 1)
            s = W.add(W.compose(tf, f), W.scale(W.compose(tg, g), -1))
            rem, quot = self.reduce(s, self.basis)
            if rem:
                # Cofactors are expanded only for S-polynomials that survive reduction.
                rcof = cof_add((cof_left(tf, fc), 1), (cof_left(tg, gc), -1),
                               *((cof_left(L, self.basis[k][1]), -1) for k, L in quot.items()))
                self.insert(rem, rcof, pairs)

    def interreduce(self):
        """Minimal, interreduced basis with cofactors carried along."""
        changed = True
        while changed:
            changed = False
            for i in range(len(self.basis)):
                op, cof = self.basis[i]
                others = self.basis[:i] + self.basis[i + 1:]
                m, _ = lead(op)
                if any(divides(lead(g)[0], m) for g, _ in others):
                    del self.basis[i]
                    changed = True
                    break
                rem, quot = self.reduce(op, others)
                if rem != op:
                    idx = [k for k in range(len(self.basis)) if k != i]
                    cof = cof_add((cof, 1), *((cof_left(L, self.basis[idx[k]][1]), -1) for k, L in quot.items()))
                    c = lead(rem)[1]
                    self.basis[i] = (W.scale(rem, 1 / c), cof_add((cof, 1 / c)))
                    changed = True
                    break

    def run(self):
        pairs = []
        for k, Ck in sorted(self.C.items()):
            rem, cof = self.reduce_tracked(Ck, {(k, 0): {(0, 0, 0, 0): F(1)}})
            if rem:
                self.insert(rem, cof, pairs)
        rounds = 0
        while True:
            self.complete(pairs)
            self.interreduce()
            rounds += 1
            added = False
            for op, cof in list(self.basis):
                rem, rcof = self.reduce_tracked(W.compose(op, self.D), cof_shift(cof))
                if rem:
                    self.insert(rem, rcof, pairs)
                    added = True
            if not added:
                return rounds

    def certificate(self):
        P = [op for op, _ in self.basis]
        cc = {}
        for k, Ck in self.C.items():
            rem, quot = self.reduce(Ck, self.basis)
            if rem:
                raise AssertionError('correction gate not reduced to zero by final basis')
            cc[str(k)] = [{'generator': i, 'left_multiplier': W.dump_terms(L)} for i, L in sorted(quot.items())]
        prov = [[{'gate_order': k, 'iterate': s, 'left_multiplier': W.dump_terms(L)}
                 for (k, s), L in sorted(cof.items())] for _, cof in self.basis]
        clo = []
        for op in P:
            rem, quot = self.reduce(W.compose(op, self.D), self.basis)
            if rem:
                raise AssertionError('right-D product not reduced to zero by final basis')
            clo.append([{'generator': i, 'left_multiplier': W.dump_terms(L)} for i, L in sorted(quot.items())])
        return {'schema': 'weyl-invariant-kernel-v1', 'field': 'Q',
                'hamiltonian': [[a, b, str(c)] for (a, b), c in sorted(self.H.items())],
                'generators': [W.dump_terms(op) for op in P],
                'correction_containment': cc, 'provenance': prov, 'closure': clo}


def discover(H, **budget):
    e = Engine(H, **budget)
    try:
        rounds = e.run()
    except Budget as b:
        return {'status': 'unknown', 'reason': str(b), 'steps': e.steps, 'generators_so_far': len(e.basis)}, None
    cert = e.certificate()
    replay = W.verify_certificate(cert)
    meta = {'status': 'certified', 'closure_rounds': rounds, 'reduction_steps': e.steps,
            'generators': [show_op(op) for op, _ in e.basis],
            'max_iterate_used': max((s for _, cof in e.basis for (_, s) in cof), default=0),
            'term_order': 'weight (0,0,1,1) on (q,p,dq,dp), then total degree, then reverse lex',
            'replay': replay}
    return meta, cert


def bounded_kernel(generators, degree):
    """Basis (exact) of polynomials of total degree <= degree killed by all generators.

    Diagnostic only: a bounded window, labelled as such. Operators in W_2 do not
    increase degree beyond their own q,p-degree minus derivative order, so the
    images are computed exactly with no projection.
    """
    monos = [(a, n - a) for n in range(degree + 1) for a in range(n + 1)]
    rows = {}
    cols = []
    for j, m in enumerate(monos):
        img = {}
        for gi, P in enumerate(generators):
            for e, c in W.act(P, {m: F(1)}).items():
                img[(gi, e)] = c
        cols.append(img)
        for k in img:
            rows.setdefault(k, len(rows))
    # Solve sum_j x_j cols[j] = 0 exactly.
    M = [[F(0)] * len(monos) for _ in rows]
    for j, img in enumerate(cols):
        for k, c in img.items():
            M[rows[k]][j] = c
    sys.path.insert(0, str(HERE.parent))
    import qlinalg
    basis = qlinalg.null_basis(M, len(monos)) if M else [[F(int(i == j)) for i in range(len(monos))] for j in range(len(monos))]
    return [W.tidy({monos[i]: v[i] for i in range(len(monos))}) for v in basis]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('discover')
    d.add_argument('hamiltonian')
    d.add_argument('--output', type=Path)
    d.add_argument('--max-generators', type=int, default=60)
    d.add_argument('--max-steps', type=int, default=20000)
    d.add_argument('--max-degree', type=int, default=60)
    d.add_argument('--kernel-degree', type=int)
    a = ap.parse_args()
    H = parse_poly(a.hamiltonian)
    meta, cert = discover(H, max_generators=a.max_generators, max_steps=a.max_steps, max_degree=a.max_degree)
    meta['hamiltonian'] = show_poly(H)
    if cert and a.kernel_degree is not None:
        ker = bounded_kernel([W.read_terms(g, 4) for g in cert['generators']], a.kernel_degree)
        meta['bounded_kernel'] = {'degree_window': a.kernel_degree, 'dimension': len(ker),
                                  'basis': [show_poly(g) for g in ker],
                                  'scope': 'finite-degree diagnostic; not an all-degree solution classification'}
    if cert and a.output:
        a.output.write_text(json.dumps(cert, indent=1) + '\n')
        meta['certificate'] = str(a.output)
    print(json.dumps(meta, indent=2))
    if meta['status'] != 'certified':
        sys.exit(3)


if __name__ == '__main__':
    main()
