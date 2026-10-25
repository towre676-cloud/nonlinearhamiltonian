#!/usr/bin/env python3
"""Quartic dynamic cores, extended: degree 24, the equianharmonic case,
and a seventh homogeneous representative.

Extends ~/workspace/research/improvements_next/quartic_cores/
quartic_cores.py (wave one, degrees <= 16).  Same definition, quoted
from the repository (programmes/DYNAMIC_CORE_RESULTS.md):

    D_inf(H) = { G in Q[q,p] : C_k D^r G = 0 for all odd k >= 3 and
                 all r >= 0 },   D = {H,.},  C_k = T_k(H,.).

For deg H = 4 the only nonzero gate is C_3 = T_3(H, .), with T_k in
the explicit form of research/hamiltonian/quartic/proofs.md.  What is
computed, in exact arithmetic:

  * For seven homogeneous quartic representatives (the six of wave one
    plus H = q^4 - q^2 p^2 + p^4, lambda = -1, from the repository's
    sec.3c table), the refinement spaces
        S^R_n(H) = { G in V_n : T_3(H, D^r G) = 0, r = 0..R }
    for every n <= 24 and R <= 8.  D_inf(H)_n subseteq S^R_n always, so
    dim S^R_n is a rigorous upper bound on the core dimension; where it
    meets the repository's proved core the degree is determined.
  * The equianharmonic class lambda^2 = -12 (j = 0) of the distinct-
    root family H_l = q^4 + l q^2 p^2 + p^4, in BOTH readings:
      (A) the repository's rational representative H = q^4 + q p^3
          over Q (DYNAMIC_CORE_RESULTS.md sec.3c and
          extensions/hamiltonian/test_quartic_rigidity.py, which calls
          q^4 + q p^3 "a rational representative" of lambda^2 = -12);
      (B) H_l itself with l^2 = -12, computed over the quadratic field
          Q(sqrt(-3)) (l = 2 sqrt(-3)) with exact arithmetic in the
          basis {1, sqrt(-3)}.
    GL_2(Qbar)-covariance of D and T_3 predicts identical refinement
    dimension tables for (A) and (B); the script verifies this.

Cross-checks: wave-one JSON agreement in degrees <= 16; partner spaces
vs improvements/moyal_partner_checker.py and the repository engine
research/hamiltonian/independent/engine.py (spans in degrees <= 12,
dimensions in degrees <= 24); the repository's own Weyl-operator
machinery (extensions/hamiltonian/weyl_receipts.py, the truncated
kernel of its test_quartic_rigidity.py) on samples; the static
Hilbert formula dim E_n = 2 + 1_{e | (n-2)} of quartic/proofs.md.

Standard library only.  Paths are relative to this file.
"""

from fractions import Fraction
from math import comb, gcd, lcm
from functools import reduce
from pathlib import Path
import importlib.util
import json
import sys
import time

HERE = Path(__file__).resolve().parent

NMAX = 24           # highest homogeneous degree tabulated
RMAX = 8            # highest refinement depth
XC_MAX = 12         # span cross-checks up to this degree
WAVE1_NMAX = 16

# ------------------------------------------------------- Q(sqrt(-3))

class Quad:
    """Exact element a + b*sqrt(-3) of Q(sqrt(-3)), a, b in Q."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    @staticmethod
    def coerce(x):
        if isinstance(x, Quad):
            return x
        return Quad(x, 0)

    def __add__(self, other):
        o = Quad.coerce(other)
        return Quad(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, other):
        o = Quad.coerce(other)
        return Quad(self.a - o.a, self.b - o.b)

    def __rsub__(self, other):
        return Quad.coerce(other) - self

    def __neg__(self):
        return Quad(-self.a, -self.b)

    def __mul__(self, other):
        o = Quad.coerce(other)
        # (a + b s)(c + d s) with s^2 = -3
        return Quad(self.a * o.a - 3 * self.b * o.b,
                    self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def inverse(self):
        n = self.a * self.a + 3 * self.b * self.b
        if n == 0:
            raise ZeroDivisionError("Quad zero has no inverse")
        return Quad(self.a / n, -self.b / n)

    def __truediv__(self, other):
        return self * Quad.coerce(other).inverse()

    def __rtruediv__(self, other):
        return Quad.coerce(other) * self.inverse()

    def __eq__(self, other):
        if other == 0 and not isinstance(other, (Quad, Fraction)):
            return self.a == 0 and self.b == 0
        try:
            o = Quad.coerce(other)
        except (TypeError, ValueError):
            return NotImplemented
        return self.a == o.a and self.b == o.b

    def __repr__(self):
        return f"Quad({self.a}, {self.b})"

SQRT_NEG3 = Quad(0, 1)          # sqrt(-3)
LAM_EQ = Quad(0, 2)             # lambda = 2 sqrt(-3), lambda^2 = -12

# ------------------------------------------------------------- polys
# Polynomial: dict (a, b) -> coeff (Fraction or Quad), term q^a p^b.

def clean(p):
    return {k: v for k, v in p.items() if v != 0}

def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            nv = v if k not in out else out[k] + v
            if nv != 0:
                out[k] = nv
            elif k in out:
                del out[k]
    return out

def scale(p, s):
    if s == 0:
        return {}
    return clean({k: v * s for k, v in p.items()})

def mul(a, b):
    out = {}
    for (a1, b1), c1 in a.items():
        for (a2, b2), c2 in b.items():
            k = (a1 + a2, b1 + b2)
            nv = c1 * c2 if k not in out else out[k] + c1 * c2
            if nv != 0:
                out[k] = nv
            elif k in out:
                del out[k]
    return out

def mono(a, b, c=1):
    return {(a, b): c} if c != 0 else {}

def falling(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r *= n - i
    return r

def deriv(p, dq, dp):
    out = {}
    for (a, b), c in p.items():
        if a < dq or b < dp:
            continue
        k = (a - dq, b - dp)
        out[k] = out.get(k, 0) + c * (falling(a, dq) * falling(b, dp))
    return clean(out)

def poisson(H, G):
    """D_H G = {H, G} = H_q G_p - H_p G_q."""
    return add(mul(deriv(H, 1, 0), deriv(G, 0, 1)),
               scale(mul(deriv(H, 0, 1), deriv(G, 1, 0)), -1))

def transvectant(F, G, k):
    """T_k(F,G) = sum_j (-1)^j C(k,j) (dq^{k-j} dp^j F)(dq^j dp^{k-j} G),
    as in research/hamiltonian/quartic/proofs.md."""
    out = {}
    for j in range(k + 1):
        left = deriv(F, k - j, j)
        right = deriv(G, j, k - j)
        if left and right:
            out = add(out, scale(mul(left, right),
                                 ((-1) ** j) * comb(k, j)))
    return out

def gate(H, G):
    """The only nonzero correction gate for deg H = 4: C_3 = T_3(H, .)."""
    return transvectant(H, G, 3)

# ------------------------------------------------------- linear algebra

def field_zero(H):
    return Quad(0) if any(isinstance(v, Quad) for v in H.values()) \
        else Fraction(0)

def nullspace(rows, ncols, zero=Fraction(0)):
    mat = [list(r) for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] != 0), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        mat[r] = [x / pv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[r])]
        pivots.append(c)
        r += 1
        if r >= len(mat):
            break
    basis = []
    for fc in (c for c in range(ncols) if c not in pivots):
        vec = [zero] * ncols
        vec[fc] = zero + 1
        for i, pc in enumerate(pivots):
            vec[pc] = -mat[i][fc]
        basis.append(vec)
    return basis

def rank(vecs):
    if not vecs:
        return 0
    mat = [list(v) for v in vecs]
    ncols = len(mat[0])
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] != 0), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        mat[r] = [x / pv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[r])]
        r += 1
        if r >= len(mat):
            break
    return r

def in_span(vec, basis_vecs):
    if not basis_vecs:
        return all(v == 0 for v in vec)
    return rank(basis_vecs + [vec]) == rank(basis_vecs)

def spans_equal(basis_a, basis_b):
    va = [list(v) for v in basis_a]
    vb = [list(v) for v in basis_b]
    if not va and not vb:
        return True
    return rank(va) == rank(vb) == rank(va + vb)

# ------------------------------------------------------------ formatting

def fmt_frac(c):
    return str(c)

def fmt_quad(c):
    a, b = c.a, c.b
    if b == 0:
        return str(a)
    if a == 0:
        return f"({b})*sqrt(-3)"
    sgn = "+" if b > 0 else "-"
    return f"({a} {sgn} {abs(b)}*sqrt(-3))"

def is_quad_poly(p):
    return any(isinstance(v, Quad) for v in p.values())

def fmt(p):
    if not p:
        return "0"
    quad = is_quad_poly(p)
    fc = fmt_quad if quad else fmt_frac
    def keyf(kv):
        (a, b), _ = kv
        return (-(a + b), -a, b)
    parts = []
    for (a, b), c in sorted(p.items(), key=keyf):
        t = ""
        if a:
            t += f"q^{a}" if a > 1 else "q"
        if b:
            t += f"p^{b}" if b > 1 else "p"
        if not t:
            t = "1"
        if not quad and c == 1:
            parts.append(t)
        elif not quad and c == -1:
            parts.append("-" + t)
        else:
            parts.append(f"{fc(c)}*{t}")
    return " + ".join(parts).replace("+ -", "- ")

def vec_to_poly(vec, mons):
    return clean({m: c for c, m in zip(vec, mons) if c != 0})

def poly_to_vec(p, mons):
    zero = Quad(0) if is_quad_poly(p) else Fraction(0)
    return [p.get(m, zero) for m in mons]

# ------------------------------------------------------- core machinery

def refinement(H, mons, rmax, want_bases_at=()):
    """Stacked conditions T_3(H, D^r G) = 0 for r = 0..rmax on the span
    of `mons`, D^r images kept as full polynomials (no projection).
    Returns (dims_by_R, {R: basis_polys for R in want_bases_at})."""
    zero = field_zero(H)
    one = zero + 1
    images = [mono(a, b, one) for (a, b) in mons]
    rows = []
    dims = []
    bases = {}
    for r in range(rmax + 1):
        gated = [gate(H, im) for im in images]
        keys = sorted({k for g in gated for k in g})
        for k in keys:
            rows.append([g.get(k, zero) for g in gated])
        vecs = nullspace(rows, len(mons), zero)
        dims.append(len(vecs))
        if r in want_bases_at:
            bases[r] = [vec_to_poly(v, mons) for v in vecs]
        images = [poisson(H, im) for im in images]
    return dims, bases

def homogeneous_mons(n):
    return [(a, n - a) for a in range(n + 1)]

# ------------------------------------------------- external cross-check

def load_module(name, candidates):
    for cand in candidates:
        p = cand.resolve()
        if p.is_file():
            spec = importlib.util.spec_from_file_location(name, p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod, p
    return None, None

REPO = HERE.parents[2]  # repository root, from research/hamiltonian/independent/

def find_checkers():
    moyal, mp = load_module(
        "moyal_partner_checker_x",
        [HERE / "moyal_partner_checker.py"]  # added by the Moyal checker change, same directory)
    engine, ep = load_module(
        "repo_engine_x",
        [REPO / "research" / "hamiltonian" / "independent" / "engine.py"])
    return moyal, mp, engine, ep

def weyl_truncated_kernel_dim(W, H, n, depth):
    """Copied verbatim in spirit from the repository's
    extensions/hamiltonian/test_quartic_rigidity.py: an independent
    computation of dim {G in V_n : C_3 D^r G = 0, r <= depth} via the
    repository's Weyl-algebra operator action."""
    import qlinalg as L
    D, C3 = W.derivation(H), W.gates(H)[3]
    cols = []
    for a in range(n + 1):
        g, img = {(a, n - a): Fraction(1)}, {}
        for r in range(depth + 1):
            img.update({(r, e): c for e, c in W.act(C3, g).items()})
            g = W.act(D, g)
        cols.append(img)
    keys = sorted({k for c in cols for k in c})
    M = [[c.get(k, Fraction(0)) for c in cols] for k in keys]
    return n + 1 - (L.rank(M, n + 1) if M else 0)

# ------------------------------------------------------------- the data

def H_parse(*terms):
    out = {}
    for a, b, c in terms:
        out = add(out, mono(a, b, Fraction(c)))
    return out

CASES = [
    {"id": "q4", "H_str": "q^4", "H": H_parse((4, 0, 1)),
     "root_type": "(4)", "e": 1,
     "repo_proved_core": "Q[q] + p*Q[q] + p^2*Q[q]",
     "family": "monomials q^n, q^(n-1) p, q^(n-2) p^2"},
    {"id": "q3p", "H_str": "q^3 p", "H": H_parse((3, 1, 1)),
     "root_type": "(3,1)", "e": 4,
     "repo_proved_core": "Q[q] + p*Q[q]",
     "family": "monomials q^n, q^(n-1) p"},
    {"id": "qp3", "H_str": "q p^3", "H": H_parse((1, 3, 1)),
     "root_type": "(3,1) with q and p exchanged", "e": 4,
     "repo_proved_core": "Q[p] + q*Q[p]",
     "family": "monomials p^n, q p^(n-1)"},
    {"id": "q2p2", "H_str": "q^2 p^2", "H": H_parse((2, 2, 1)),
     "root_type": "(2,2)", "e": 2,
     "repo_proved_core": "Q[qp]",
     "family": "monomial (qp)^(n/2) in even degree n, nothing in odd degree"},
    {"id": "q4_p4", "H_str": "q^4 + p^4",
     "H": H_parse((4, 0, 1), (0, 4, 1)),
     "root_type": "distinct roots, lambda = 0", "e": 4,
     "repo_proved_core": "span{1, H}",
     "family": "1 in degree 0, H in degree 4, nothing else"},
    {"id": "q4_q2p2_p4", "H_str": "q^4 + q^2 p^2 + p^4",
     "H": H_parse((4, 0, 1), (2, 2, 1), (0, 4, 1)),
     "root_type": "distinct roots, lambda = 1", "e": 4,
     "repo_proved_core": "span{1, H}",
     "family": "1 in degree 0, H in degree 4, nothing else"},
    {"id": "q4_mq2p2_p4", "H_str": "q^4 - q^2 p^2 + p^4",
     "H": H_parse((4, 0, 1), (2, 2, -1), (0, 4, 1)),
     "root_type": "distinct roots, lambda = -1", "e": 4,
     "repo_proved_core": "span{1, H}",
     "family": "1 in degree 0, H in degree 4, nothing else"},
]

EQ_A = {"id": "equianharmonic_rational_form", "H_str": "q^4 + q p^3",
        "H": H_parse((4, 0, 1), (1, 3, 1)), "e": 4}
EQ_B = {"id": "equianharmonic_lambda_form",
        "H_str": "q^4 + lambda q^2 p^2 + p^4 with lambda^2 = -12",
        "H": {(4, 0): Quad(1), (2, 2): LAM_EQ, (0, 4): Quad(1)},
        "e": 4}

def expected_static_dim(e, n):
    """quartic/proofs.md: dim E_n = 2 + 1_{e | (n-2)} for n >= 2;
    dim E_0 = 1, dim E_1 = 2."""
    if n == 0:
        return 1
    if n == 1:
        return 2
    return 2 + (1 if (n - 2) % e == 0 else 0)

def min_depth(dims):
    """First R at which dims[R] equals the final (R = RMAX) value."""
    fin = dims[-1]
    for r, d in enumerate(dims):
        if d == fin:
            return r
    return None

def run_case_table(H, e, label, xc=None, weyl=None, wave1=None):
    """Full refinement table n <= NMAX, R <= RMAX for one H."""
    entry = {"partner_dims_by_degree": {}, "refinement_dims_by_degree": {},
             "core_dims_by_degree_truncated": {}, "core_bases_by_degree": {},
             "min_depth_by_degree": {}, "static_dim_formula_agrees": True,
             "invariance_in_computed_range": True,
             "stabilisation_depth_overall": 0}
    core_basis_by_n = {}
    for n in range(NMAX + 1):
        mons = homogeneous_mons(n)
        dims, bases = refinement(H, mons, RMAX,
                                 want_bases_at=(0, RMAX))
        entry["partner_dims_by_degree"][str(n)] = dims[0]
        entry["refinement_dims_by_degree"][str(n)] = dims
        entry["core_dims_by_degree_truncated"][str(n)] = dims[-1]
        entry["min_depth_by_degree"][str(n)] = min_depth(dims)
        entry["stabilisation_depth_overall"] = max(
            entry["stabilisation_depth_overall"], min_depth(dims))
        core_basis_by_n[n] = bases[RMAX]
        if dims[0] != expected_static_dim(e, n):
            entry["static_dim_formula_agrees"] = False
        if bases[RMAX]:
            entry["core_bases_by_degree"][str(n)] = [
                fmt(b) for b in bases[RMAX]]
        if wave1 is not None and n <= WAVE1_NMAX:
            w = wave1["refinement_dims_by_degree"][str(n)]
            if list(w) != list(dims):
                xc["details"].append(
                    f"WAVE1 MISMATCH {label} n={n}: wave1={w} ext={dims}")
            else:
                xc["wave1_agree"] += 1
        # partner-space cross-checks against the two Q engines
        if xc is not None and xc.get("moyal") is not None and n <= NMAX:
            mons_n = mons
            mb = xc["moyal"].homogeneous_kernel(H, n)
            mv = [poly_to_vec(b, mons_n) for b in mb]
            ov = [poly_to_vec(b, mons_n) for b in bases[0]]
            if len(mv) != dims[0]:
                xc["partner_dims_agree_all"] = False
                xc["details"].append(
                    f"MOYAL DIM MISMATCH {label} n={n}: moyal={len(mv)} "
                    f"ours={dims[0]}")
            if n <= XC_MAX:
                eb = xc["engine"].homogeneous_kernel(H, n)
                ev = [poly_to_vec(b, mons_n) for b in eb]
                if not (spans_equal(ov, mv) and spans_equal(ov, ev)):
                    xc["partner_spans_agree_all"] = False
                    xc["details"].append(
                        f"SPAN MISMATCH {label} n={n}")
        # repository Weyl-operator spot check of refinement dims
        if weyl is not None:
            W, samples = weyl
            for (nn, depth) in samples:
                if nn == n and depth <= RMAX:
                    got = weyl_truncated_kernel_dim(W, H, nn, depth)
                    if got != dims[depth]:
                        xc["weyl_agree"] = False
                        xc["details"].append(
                            f"WEYL MISMATCH {label} n={nn} depth={depth}: "
                            f"weyl={got} ours={dims[depth]}")
    for n in range(NMAX - 1):
        if not core_basis_by_n[n]:
            continue
        target_mons = homogeneous_mons(n + 2)
        target_vecs = [poly_to_vec(b, target_mons)
                       for b in core_basis_by_n[n + 2]]
        for G in core_basis_by_n[n]:
            DG = poisson(H, G)
            if not in_span(poly_to_vec(DG, target_mons), target_vecs):
                entry["invariance_in_computed_range"] = False
    return entry

def main():
    t0 = time.time()
    moyal, moyal_path, engine, engine_path = find_checkers()
    print(f"moyal checker: {moyal_path}")
    print(f"repo engine:   {engine_path}")
    sys.path.insert(0, str((REPO / "extensions" / "hamiltonian").resolve()))
    sys.path.insert(0, str((REPO / "extensions").resolve()))
    try:
        import weyl_receipts as W
        print("weyl_receipts: loaded (repository operator machinery)")
    except Exception as ex:  # pragma: no cover
        W = None
        print(f"weyl_receipts: FAILED to load ({ex})")

    wave1 = {}
    w1_path = (HERE / ".." / ".." / "improvements_next" / "quartic_cores"
               / "quartic_cores.json")
    if w1_path.is_file():
        w1 = json.loads(w1_path.read_text())
        wave1 = {c["id"]: c for c in w1["cases"]}
        print(f"wave-one table loaded: {sorted(wave1)}")

    xc = {"partner_dims_agree_all": True, "partner_spans_agree_all": True,
          "monomial_verdicts_agree_all": True, "weyl_agree": True,
          "wave1_agree": 0, "details": [],
          "moyal": moyal, "engine": engine}

    results = {
        "definition": (
            "D_inf(H) = { G in Q[q,p] : C_k D^r G = 0 for all odd k >= 3 "
            "and all r >= 0 }, D = {H,.}, C_k = T_k(H,.) "
            "(programmes/DYNAMIC_CORE_RESULTS.md).  For deg H = 4 the "
            "only nonzero gate is T_3."),
        "parameters": {"NMAX": NMAX, "RMAX": RMAX, "XC_MAX": XC_MAX},
        "arithmetic": ("exact rational (fractions.Fraction); "
                       "Q(sqrt(-3)) exact pairs for the lambda-form "
                       "equianharmonic computation"),
        "cross_check_sources": {
            "moyal_partner_checker": str(moyal_path) if moyal_path else None,
            "repo_engine": str(engine_path) if engine_path else None,
            "weyl_receipts": "extensions/hamiltonian/weyl_receipts.py",
            "wave_one_table": str(w1_path) if w1_path.is_file() else None,
        },
        "cases": [], "equianharmonic": {},
    }

    weyl_samples = [(2, 0), (2, 1), (3, 0), (3, 1), (3, 2),
                    (4, 1), (6, 0), (6, 1), (6, 2)]
    for case in CASES:
        H = case["H"]
        print(f"\n=== H = {case['H_str']} ===", flush=True)
        entry = {k: case[k] for k in
                 ("id", "H_str", "root_type", "e", "repo_proved_core",
                  "family")}
        w1 = wave1.get(case["id"])
        table = run_case_table(
            H, case["e"], case["H_str"], xc=xc,
            weyl=(W, weyl_samples) if W is not None else None,
            wave1=w1)
        entry.update(table)
        # monomial verdict spot-check (Q cases, both engines)
        if moyal is not None and engine is not None:
            for a in range(7):
                for b in range(7 - a):
                    g = mono(a, b, Fraction(1))
                    ours_free = (gate(H, g) == {})
                    moyal_free, _ = moyal.is_correction_free(H, g)
                    engine_free = engine.exact_partner(H, g)
                    if not (ours_free == moyal_free == engine_free):
                        xc["monomial_verdicts_agree_all"] = False
                        xc["details"].append(
                            f"MONOMIAL MISMATCH H={case['H_str']} "
                            f"G=q^{a}p^{b}")
        dims_str = " ".join(
            str(entry["core_dims_by_degree_truncated"][str(n)])
            for n in range(NMAX + 1))
        print(f"truncated core dims n=0..{NMAX}: {dims_str}")
        print(f"stabilisation depth overall: "
              f"{entry['stabilisation_depth_overall']}; static formula: "
              f"{entry['static_dim_formula_agrees']}; invariance: "
              f"{entry['invariance_in_computed_range']}")
        results["cases"].append(entry)

    # ------------------------------------------------ equianharmonic
    print("\n=== Equianharmonic, reading A: H = q^4 + q p^3 over Q ===",
          flush=True)
    eq_samples = [(1, 0), (1, 1), (1, 2), (1, 3), (2, 1), (3, 0), (3, 1),
                  (3, 2), (3, 3), (4, 1), (5, 1), (6, 1)]
    eqA = {k: EQ_A[k] for k in ("id", "H_str", "e")}
    tableA = run_case_table(EQ_A["H"], 4, "equianharmonic A", xc=xc,
                            weyl=(W, eq_samples) if W is not None else None)
    eqA.update(tableA)
    # survivors at sub-stabilisation depths in degrees 1 and 3
    surv = {}
    for n in (1, 3):
        mons = homogeneous_mons(n)
        dims, bases = refinement(EQ_A["H"], mons, RMAX,
                                 want_bases_at=tuple(range(RMAX + 1)))
        surv[str(n)] = {str(r): [fmt(b) for b in bases[r]]
                        for r in range(RMAX + 1)}
    eqA["survivor_bases_degrees_1_and_3"] = surv
    print("A core dims:", " ".join(
        str(eqA["core_dims_by_degree_truncated"][str(n)])
        for n in range(NMAX + 1)))
    print("A min depths n=0..12:",
          [eqA["min_depth_by_degree"][str(n)] for n in range(13)])

    print("\n=== Equianharmonic, reading B: H_lambda over Q(sqrt(-3)) "
          "===", flush=True)
    eqB = {k: EQ_B[k] for k in ("id", "H_str", "e")}
    tableB = run_case_table(EQ_B["H"], 4, "equianharmonic B", xc=None)
    eqB.update(tableB)
    survB = {}
    for n in (1, 3):
        mons = homogeneous_mons(n)
        dims, bases = refinement(EQ_B["H"], mons, RMAX,
                                 want_bases_at=tuple(range(RMAX + 1)))
        survB[str(n)] = {str(r): [fmt(b) for b in bases[r]]
                         for r in range(RMAX + 1)}
    eqB["survivor_bases_degrees_1_and_3"] = survB
    print("B core dims:", " ".join(
        str(eqB["core_dims_by_degree_truncated"][str(n)])
        for n in range(NMAX + 1)))
    print("B min depths n=0..12:",
          [eqB["min_depth_by_degree"][str(n)] for n in range(13)])

    agree = all(
        eqA["refinement_dims_by_degree"][str(n)]
        == eqB["refinement_dims_by_degree"][str(n)]
        for n in range(NMAX + 1))
    print(f"\nEquianharmonic readings A and B refinement tables "
          f"identical in every degree <= {NMAX}: {agree}")
    results["equianharmonic"] = {
        "reading_A_rational_form": eqA,
        "reading_B_lambda_form": eqB,
        "tables_identical": agree,
        "repo_claim": (
            "DYNAMIC_CORE_RESULTS.md sec.3c: the equianharmonic class "
            "lambda^2 = -12 (j = 0, rational form q^4 + q p^3) is not "
            "exceptional, but needs depth R = 3 in degree 1 and R = 2 "
            "in degree 3; every other degree needs only R = 1.  "
            "Per-degree certificate covers degrees 1-12."),
    }

    results["cross_checks"] = {
        k: v for k, v in xc.items() if k not in ("moyal", "engine")}
    print("\ncross-checks:",
          {k: v for k, v in results["cross_checks"].items()
           if k != "details"})
    if xc["details"]:
        print("cross-check details:", *xc["details"], sep="\n  ")
    print(f"\nelapsed: {time.time() - t0:.1f}s")
    out = HERE / "quartic_cores_ext.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
