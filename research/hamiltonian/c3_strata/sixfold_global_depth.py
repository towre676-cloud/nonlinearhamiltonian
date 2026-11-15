"""Global stopping depth for the sixfold-leading family

    H = q^6 + sum_{i+j<=5} c_ij q^i p^j        (characteristic zero, flat gates).

`classify(h)` assigns every member to exactly one Newton branch by an
exhaustive decision chain on its coefficients, and returns the persistent-core
dimension, the proved upper bound on the least stopping depth, the exact least
depth, and the theorems used.  Where a closed formula for the exact depth is
proved it is used: this now covers every branch except the two with
nonconstant quadratic coefficient of degree 1 or 2, where the core dimension
on the square locus is still read from a proved finite box.  The jump loci of
`sixfold_jump_loci` replace the earlier finite-window decisions on the
branches c04, c32 and c03 off the cube locus.

`chain(h, monomials, max_depth)` is the exact engine: it returns
dim(S^r intersected with span(monomials)) for r = 0..max_depth.  Gate outputs
are never truncated, so these intersections are exact.

Polynomials are dictionaries {(i, j): Fraction} for q^i p^j.
"""
from fractions import Fraction as Fr
from math import comb, gcd, perm

import sympy as S
from sympy.polys.matrices import DomainMatrix

import sixfold_jump_loci as J

INF = float("inf")
P_HIGH = ((0, 5), (1, 4), (2, 3), (0, 4), (3, 2), (1, 3), (0, 3))


# ---------------------------------------------------------------- arithmetic

def _deriv(f, a, b):
    return {(i - a, j - b): c*perm(i, a)*perm(j, b) for (i, j), c in f.items() if i >= a and j >= b}


def _mul(f, g):
    out = {}
    for (a, b), c in f.items():
        for (i, j), d in g.items():
            key = (a + i, b + j)
            out[key] = out.get(key, 0) + c*d
    return {k: v for k, v in out.items() if v}


def _add(f, g, s=1):
    out = dict(f)
    for k, v in g.items():
        out[k] = out.get(k, 0) + s*v
    return {k: v for k, v in out.items() if v}


def transvectant(h, g, k):
    """Unnormalised flat transvectant T_k(h, g) in the original coordinates."""
    out = {}
    for t in range(k + 1):
        hd = _deriv(h, k - t, t)
        gd = _deriv(g, t, k - t)
        if hd and gd:
            out = _add(out, _mul(hd, gd), (-1)**t*comb(k, t))
    return out


def integer_form(h):
    """A nonzero integer multiple of h (the refinement spaces are unchanged)."""
    den = 1
    for v in h.values():
        d = Fr(v).denominator
        den = den*d//gcd(den, d)
    return {k: int(Fr(v)*den) for k, v in h.items() if v}


def _nullspace(rows, ncols):
    if not rows:
        return [[int(i == j) for i in range(ncols)] for j in range(ncols)]
    dm = DomainMatrix([[S.ZZ(x) for x in row] for row in rows], (len(rows), ncols), S.ZZ).to_field()
    basis = dm.nullspace().to_Matrix()
    out = []
    for r in range(basis.rows):
        vec = [S.Rational(x) for x in basis.row(r)]
        den = S.ilcm(*[x.q for x in vec]) if vec else 1
        out.append([int(x*den) for x in vec])
    return out


def _combine(polys, vec):
    out = {}
    for c, g in zip(vec, polys):
        if c:
            out = _add(out, {k: c*v for k, v in g.items()})
    return out


def chain(h, monomials, max_depth, return_basis=False):
    """dim(S^r(h) ∩ span(monomials)) for r = 0..max_depth, exactly."""
    h = integer_form(h)
    vecs = [{m: 1} for m in monomials]
    imgs = list(vecs)
    dims = []
    for r in range(max_depth + 1):
        if r:
            imgs = [transvectant(h, g, 1) for g in imgs]
        rows = {}
        for col, g in enumerate(imgs):
            for k in (3, 5):
                for mon, c in transvectant(h, g, k).items():
                    rows.setdefault((k,) + mon, {})[col] = c
        n = len(vecs)
        null = _nullspace([[row.get(c, 0) for c in range(n)] for row in rows.values()], n)
        vecs = [_combine(vecs, v) for v in null]
        imgs = [_combine(imgs, v) for v in null]
        dims.append(len(vecs))
        if not vecs:
            dims += [0]*(max_depth - r)
            break
    return (dims, vecs) if return_basis else dims


def degree_window(n):
    return [(i, j) for j in range(n + 1) for i in range(n + 1 - j)]


def weight_window(wq, wp, bound):
    return [(i, j) for j in range(bound//wp + 1) for i in range((bound - wp*j)//wq + 1)]


def first_stable(dims):
    """Least r with dims[r] == dims[-1]; meaningful when the tail is constant."""
    return next(r for r, d in enumerate(dims) if d == dims[-1])


# ------------------------------------------------------------ normalisation

def normalise(h):
    h = {k: Fr(v) for k, v in h.items() if Fr(v) != 0}
    lead = h.get((6, 0), Fr(0))
    if lead == 0 or any(i + j > 5 for (i, j) in h if (i, j) != (6, 0)):
        raise ValueError("not of the form f6*q^6 + (terms of total degree <= 5), f6 != 0")
    return {k: v/lead for k, v in h.items()}


def _poly(coeffs):
    """Coefficient list of a polynomial in q -> trimmed list of Fractions."""
    coeffs = [Fr(c) for c in coeffs]
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs


def _deg(coeffs):
    return len(_poly(coeffs)) - 1          # -1 for the zero polynomial


def _pmul(a, b):
    out = [Fr(0)]*(max(len(a) + len(b) - 1, 0))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x*y
    return out


def _gates_vanish(h, g):
    return not transvectant(h, g, 3) and not transvectant(h, g, 5)


# ------------------------------------------------------- the cube sub-branch

def cube_reduced_coefficients(h):
    """On the cube locus: (b0..b3), (c0..c5) of the reduced form P^3 + B(q) P + C(q)."""
    q, Y = S.symbols("q Y")
    kappa = S.Rational(h[(4, 1)])/3
    expr = sum(S.Rational(v.numerator, v.denominator)*q**i*((Y - q**2)/kappa)**j for (i, j), v in h.items())
    poly = S.Poly(S.expand(expr), Y)
    assert poly.degree() == 3 and poly.coeff_monomial(Y**3) == 1
    A, B, C = (poly.coeff_monomial(Y**k) for k in (2, 1, 0))
    Bt = S.Poly(S.expand(B - A**2/3), q)
    Ct = S.Poly(S.expand(C - A*B/3 + 2*A**3/27), q)
    assert Bt.degree() <= 3 and Ct.degree() <= 5
    b = tuple(Fr(str(Bt.coeff_monomial(q**i))) for i in range(4))
    c = tuple(Fr(str(Ct.coeff_monomial(q**i))) for i in range(6))
    return b, c


def cube_reduced_depth(b, c):
    """(core dimension, exact least depth, sources) for P^3 + B P + C, P = p + q^2."""
    b0, b1, b2, b3 = b
    c0, c1, c2, c3, c4, c5 = c
    if b2 == b3 == 0 and c2 == c3 == c4 == c5 == 0:
        if b1 == 0:
            return INF, 1, "cubic-phase table (d<=0, f=3) and Lemma G2"
        return (6 if c1 == 0 else 5), 1, "cubic-phase table (d=1, f=3) and Lemma G2"
    if c5 != 0:
        return 2, (2 if b3 == 0 or 3*b3 + 10*c5 == 0 else 1), "Theorem R, case I"
    if b3 != 0:
        return 2, (2 if 4*c4 == 5*b3*b3 else 1), "Theorem R, case II"
    if c4 != 0:
        return 2, 2, "Theorem R, case III"
    if b2 != 0 or c3 != 0:
        return 2, 2, "cube-leading Theorems E and G"
    return 2, 3, "cube-leading Theorem C / higher-restoring theorem"


# ------------------------------------------------------------------ classify

def _window_depth(h, monomials, core_dimension, bound):
    dims = chain(h, monomials, bound + 1)
    assert dims[bound] == dims[bound + 1] == core_dimension, dims
    return next(r for r in range(bound + 1) if dims[r] == core_dimension)


def classify(h):
    """Branch, persistent-core dimension, proved depth bound and exact least depth."""
    h = normalise(h)
    c = lambda i, j: h.get((i, j), Fr(0))
    out = {"core_dimension": 2}

    def done(branch, bound, exact, sources, **extra):
        out.update(branch=branch, depth_bound=bound, depth=exact, sources=sources, **extra)
        return out

    if c(0, 5) != 0:
        return done("c05", 1, 1, "generic-stratum Theorem 6")
    if c(1, 4) != 0:
        return done("c14", 1, 1, "binomial Newton sharp theorem")
    if c(2, 3) != 0:
        return done("c23", 1, 1, "binomial Newton sharp theorem")
    if c(0, 4) != 0:
        partners = J.quartic_edge_partners(h)
        return done("c04 quartic edge", 2, 2 if partners else 1,
                    "weighted cubic-form Theorem 5; Theorem J", partners=partners)
    if c(3, 2) != 0:
        partners = J.cubic_coefficient_partners(h)
        return done("c32", 2, 2 if partners else 1,
                    "quadratic-sixfold Lemmas 4, 5 and Theorem D; Theorem J", partners=partners)
    if c(1, 3) != 0:
        survives = _gates_vanish(h, _deriv(h, 0, 1))
        return done("c13", 2, 2 if survives else 1, "generic-stratum Theorem 7")
    if c(0, 3) != 0:
        a, b, x = c(4, 1), c(2, 2), c(0, 3)
        if 3*b == a*a and 27*x == a**3:
            rb, rc = cube_reduced_coefficients(h)
            core, depth, source = cube_reduced_depth(rb, rc)
            out["core_dimension"] = core
            return done("c03 cube locus", 3, depth, source, reduced=(rb, rc))
        partners = J.cubic_form_partners(h)
        return done("c03 off the cube locus", 2, 2 if partners else 1,
                    "weighted cubic-form Theorems 1-3; Theorem J", partners=partners)

    # p-degree at most two:  H = f(q) + A(q) p + B(q) p^2,  deg B <= 2
    f = _poly([c(i, 0) for i in range(6)] + [Fr(1)])
    A = _poly([c(i, 1) for i in range(5)])
    B = _poly([c(i, 2) for i in range(3)])
    if not B:
        out["core_dimension"] = INF
        affine = _deg(A) <= 1
        return done("affine in p", 1, 0 if affine else 1, "inhomogeneous theorem, Section 10")
    if len(B) == 1:
        if _deg(A) <= 1:
            return done("constant quadratic coefficient, b''=0", 5, 5, "quadratic-sixfold Theorem A")
        square = [x/(4*B[0]) for x in _pmul(A, A)]
        F = _poly([(f[i] if i < len(f) else 0) - (square[i] if i < len(square) else 0)
                   for i in range(max(len(f), len(square)))])
        n = _deg(F)
        if n >= 4:
            return done("constant quadratic coefficient, N>=4", 4, 4, "quadratic-sixfold Theorem C", N=n)
        if n == 3:
            return done("constant quadratic coefficient, N=3", 6, 6, "quadratic-sixfold Theorem C", N=3)
        out["core_dimension"] = 6
        return done("constant quadratic coefficient, N<=2", 2, 2, "quadratic-sixfold Theorem C", N=n)
    k, db = _deg(B), _deg(A)
    if k == 1:
        box = weight_window(1, 3, 13) if db == 4 else weight_window(2, 5, 22)
        depth = _window_depth(h, box, 2, 3)
        return done("linear quadratic coefficient", 3, max(depth, 1), "quadratic-sixfold Theorem D (box)")
    box = weight_window(2, 4, 18 if db == 4 else 24)
    dims = chain(h, box, 3)
    assert dims[2] == dims[3] and dims[2] in (2, 3)
    out["core_dimension"] = dims[2]
    return done("quadratic quadratic coefficient", 2, 1 if dims[1] == dims[2] else 2,
                "quadratic-sixfold Theorems D and E (box)")


def depth_six_conditions(h):
    """The explicit coefficient test for least depth six (Theorem G, part 2)."""
    h = normalise(h)
    c = lambda i, j: h.get((i, j), Fr(0))
    if any(c(i, j) != 0 for (i, j) in P_HIGH) or c(1, 2) != 0 or c(2, 2) != 0 or c(0, 2) == 0:
        return False
    if c(4, 1) != 0 or c(3, 1) == 0:
        return False
    k = 4*c(0, 2)
    return (c(3, 1)**2 == k
            and k*c(5, 0) == 2*c(3, 1)*c(2, 1)
            and k*c(4, 0) == c(2, 1)**2 + 2*c(3, 1)*c(1, 1)
            and k*c(3, 0) != 2*c(3, 1)*c(0, 1) + 2*c(2, 1)*c(1, 1))


def parse(text):
    q, p = S.symbols("q p")
    poly = S.Poly(S.expand(S.sympify(text.replace("^", "**"), locals={"q": q, "p": p})), q, p)
    return {mon: Fr(str(cf)) for mon, cf in poly.terms()}
