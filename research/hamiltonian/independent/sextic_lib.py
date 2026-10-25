"""Shared exact library for the sextic-family computations.

Conventions (the repository's, programmes/DYNAMIC_CORE_RESULTS.md):
  - Polynomials in q, p over Q, stored as dict (c, e) -> Fraction
    for the monomial q^c p^e.  Zero terms omitted.
  - Flat Weyl-Moyal convention.  The correction gates are the odd
    transvectants C_k = T_k(H, .), k >= 3, with
        T_k(F, G) = sum_j (-1)^j C(k, j) (dq^{k-j} dp^j F)(dq^j dp^{k-j} G).
    This T_k is exactly the bidifferential operator D^k of
    improvements/moyal_partner_checker.py (reindex j -> k-j there).
  - For deg H = 6 the only nonzero gates are T_3 and T_5
    (T_k differentiates H k times, so T_k = 0 for k > 6).
  - One-step (static) partner space E_n(H) = {G in V_n : T_3(H,G) =
    T_5(H,G) = 0}.  G is a correction-free partner iff it lies in E.
  - Dynamic core D_inf(H) = {G : C_k D^r G = 0 for all odd k >= 3 and
    all r >= 0}, D = {H, .} the Poisson operator.
  - Charge of q^c p^e is c - e.  T_k and D are charge-additive:
    charge(T_k(F,G)) = charge(F-part) + charge(G-part) termwise.
    Every monomial of H_a = q^6 + a q^3 p^3 + p^6 has charge in
    {6, 0, -6} == 0 (mod 6), so for the family both the partner
    system and the refinement system split by charge mod 6.

Exact rational arithmetic only (fractions.Fraction).  The parametric
work represents scalars in Q(a) as reduced pairs of polynomials in a,
and scalars in a number field Q[t]/(f) as polynomials mod f.
"""

from fractions import Fraction
from math import comb, gcd as _igcd, lcm as _ilcm
from functools import reduce

# ------------------------------------------------------------ polynomials

def clean(p):
    return {k: v for k, v in p.items() if v != 0}

def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Fraction(0)) + v
    return clean(out)

def scale(p, s):
    return clean({k: v * s for k, v in p.items()})

def mul(a, b):
    out = {}
    for (c1, e1), v1 in a.items():
        for (c2, e2), v2 in b.items():
            k = (c1 + c2, e1 + e2)
            out[k] = out.get(k, Fraction(0)) + v1 * v2
    return clean(out)

def mono(c, e, coeff=1):
    return {(c, e): Fraction(coeff)} if coeff else {}

def falling(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r *= n - i
    return r

def deriv(p, dq, dp):
    out = {}
    for (c, e), v in p.items():
        if c < dq or e < dp:
            continue
        k = (c - dq, e - dp)
        out[k] = out.get(k, Fraction(0)) + v * falling(c, dq) * falling(e, dp)
    return clean(out)

def transvectant(F, G, k):
    out = {}
    for j in range(k + 1):
        left = deriv(F, k - j, j)
        right = deriv(G, j, k - j)
        if left and right:
            out = add(out, scale(mul(left, right),
                                 Fraction((-1) ** j * comb(k, j))))
    return out

def poisson(H, G):
    """D_H G = {H, G} = H_q G_p - H_p G_q."""
    return add(mul(deriv(H, 1, 0), deriv(G, 0, 1)),
               scale(mul(deriv(H, 0, 1), deriv(G, 1, 0)), -1))

GATES = (3, 5)          # the nonzero odd gates for deg H = 6

def gates_of(H, G):
    return [transvectant(H, G, k) for k in GATES]

# ------------------------------------------------------- linear algebra/Q

def nullspace(rows, ncols):
    """Exact rational nullspace basis (list of vectors of Fractions)."""
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
        vec = [Fraction(0)] * ncols
        vec[fc] = Fraction(1)
        for i, pc in enumerate(pivots):
            vec[pc] = -mat[i][fc]
        basis.append(vec)
    return basis

def rank_of(vecs):
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

def spans_equal(vecs_a, vecs_b):
    va = [list(v) for v in vecs_a]
    vb = [list(v) for v in vecs_b]
    return rank_of(va) == rank_of(vb) == rank_of(va + vb)

def in_span(vec, basis_vecs):
    if not basis_vecs:
        return all(v == 0 for v in vec)
    return rank_of(list(basis_vecs) + [list(vec)]) == rank_of(basis_vecs)

# ------------------------------------------------------------ formatting

def primitive(p):
    if not p:
        return {}
    den = reduce(_ilcm, (v.denominator for v in p.values()), 1)
    ints = {k: int(v * den) for k, v in p.items()}
    g = reduce(_igcd, (abs(v) for v in ints.values()))
    first = sorted(ints)[0]
    sgn = 1 if ints[first] > 0 else -1
    return {k: Fraction(v * sgn, g) for k, v in ints.items()}

def fmt(p):
    if not p:
        return "0"
    parts = []
    for (c, e), v in sorted(p.items()):
        t = ""
        if c:
            t += f"q^{c}" if c > 1 else "q"
        if e:
            t += f"p^{e}" if e > 1 else "p"
        if not t:
            t = "1"
        if v == 1:
            parts.append(t)
        elif v == -1:
            parts.append("-" + t)
        else:
            parts.append(f"({v})*{t}")
    return " + ".join(parts).replace("+ -", "- ")

def poly_json(p):
    return [{"q": c, "p": e, "coefficient": str(v)}
            for (c, e), v in sorted(p.items())]

def homogeneous_mons(n):
    return [(c, n - c) for c in range(n + 1)]

def vec_to_poly(vec, mons):
    return clean({m: v for v, m in zip(vec, mons) if v})

def poly_to_vec(p, mons):
    return [p.get(m, Fraction(0)) for m in mons]

# ------------------------------------------------- partner systems over Q

def partner_rows(H, n):
    """Rows of the stacked gate system on V_n for a specialized H."""
    mons = homogeneous_mons(n)
    rows = []
    for k in GATES:
        cols = [transvectant(H, mono(c, e), k) for (c, e) in mons]
        keys = sorted({key for col in cols for key in col})
        for key in keys:
            rows.append([col.get(key, Fraction(0)) for col in cols])
    return mons, rows

def partner_kernel(H, n):
    mons, rows = partner_rows(H, n)
    return [vec_to_poly(v, mons) for v in nullspace(rows, len(mons))]

def partner_dim(H, n):
    mons, rows = partner_rows(H, n)
    return len(mons) - rank_of(rows)

# ------------------------------------------------- refinement (cores)

def refinement(H, n, rmax):
    """S^R_n dims for R = 0..rmax and the final basis (polys in V_n).
    S^R_n = {G in V_n : T_k(H, D^r G) = 0, k in {3,5}, r = 0..R}.
    D_inf(H)_n is contained in every S^R_n."""
    mons = homogeneous_mons(n)
    images = [mono(c, e) for (c, e) in mons]
    rows = []
    dims = []
    basis = []
    for r in range(rmax + 1):
        for k in GATES:
            gated = [transvectant(H, im, k) for im in images]
            keys = sorted({key for g in gated for key in g})
            for key in keys:
                rows.append([g.get(key, Fraction(0)) for g in gated])
        vecs = nullspace(rows, len(mons))
        dims.append(len(vecs))
        basis = [vec_to_poly(v, mons) for v in vecs]
        images = [poisson(H, im) for im in images]
    return dims, basis

# ============================================ polynomials in the parameter a
# A polynomial in a is a tuple of Fractions, ascending powers, trimmed
# (no trailing zeros); the zero polynomial is ().

def p_trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return tuple(p)

def p_add(a, b):
    n = max(len(a), len(b))
    return p_trim(tuple((a[i] if i < len(a) else Fraction(0)) +
                        (b[i] if i < len(b) else Fraction(0))
                        for i in range(n)))

def p_neg(a):
    return tuple(-x for x in a)

def p_sub(a, b):
    return p_add(a, p_neg(b))

def p_scale(a, s):
    if s == 0:
        return ()
    return tuple(x * s for x in a)

def p_mul(a, b):
    if not a or not b:
        return ()
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] += x * y
    return p_trim(out)

def p_divmod(a, b):
    if not b:
        raise ZeroDivisionError("polynomial division by zero")
    a = list(a)
    q = [Fraction(0)] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        i = len(a) - len(b)
        coef = a[-1] / b[-1]
        q[i] = coef
        for j in range(len(b)):
            a[i + j] -= coef * b[j]
        while a and a[-1] == 0:
            a.pop()
    return p_trim(q), p_trim(a)

def p_gcd(a, b):
    a, b = p_trim(a), p_trim(b)
    while b:
        _, r = p_divmod(a, b)
        a, b = b, r
    if a:
        a = p_scale(a, 1 / a[-1])
    return a

def p_eval(a, x):
    out = Fraction(0)
    for coef in reversed(a):
        out = out * x + coef
    return out

def p_str(a):
    if not a:
        return "0"
    parts = []
    for i, coef in enumerate(a):
        if coef == 0:
            continue
        t = "a" if i == 1 else (f"a^{i}" if i > 1 else "")
        if not t:
            parts.append(str(coef))
        elif coef == 1:
            parts.append(t)
        elif coef == -1:
            parts.append("-" + t)
        else:
            parts.append(f"({coef})*{t}")
    return " + ".join(parts).replace("+ -", "- ") if parts else "0"

# Rational functions in a: pair (num, den), coprime, den monic-ish
# (leading coefficient 1) unless num is zero, when the pair is ((), (1,)).

def rf(num, den=(Fraction(1),)):
    num, den = p_trim(num), p_trim(den)
    if not num:
        return ((), (Fraction(1),))
    if not den:
        raise ZeroDivisionError("zero denominator")
    g = p_gcd(num, den)
    if g:
        num, _ = p_divmod(num, g)
        den, _ = p_divmod(den, g)
    lc = den[-1]
    if lc != 1:
        num = p_scale(num, 1 / lc)
        den = p_scale(den, 1 / lc)
    return (num, den)

def rf_const(c):
    return rf((Fraction(c),))

def rf_a():
    return rf((Fraction(0), Fraction(1)))

def rf_add(x, y):
    return rf(p_add(p_mul(x[0], y[1]), p_mul(y[0], x[1])), p_mul(x[1], y[1]))

def rf_neg(x):
    return (p_neg(x[0]), x[1])

def rf_sub(x, y):
    return rf_add(x, rf_neg(y))

def rf_mul(x, y):
    return rf(p_mul(x[0], y[0]), p_mul(x[1], y[1]))

def rf_inv(x):
    if not x[0]:
        raise ZeroDivisionError("inverse of zero rational function")
    return rf(x[1], x[0])

def rf_div(x, y):
    return rf_mul(x, rf_inv(y))

def rf_is_zero(x):
    return not x[0]

def rf_str(x):
    if not x[0]:
        return "0"
    if x[1] == (Fraction(1),):
        return p_str(x[0])
    return f"({p_str(x[0])}) / ({p_str(x[1])})"

def rf_eval(x, a0):
    """Evaluate at a rational a0 not a pole; returns Fraction."""
    dv = p_eval(x[1], a0)
    if dv == 0:
        raise ZeroDivisionError(f"pole at a = {a0}")
    return p_eval(x[0], a0) / dv

def nullspace_field(rows, ncols, zero, one, add, sub, mul, inv, is_zero):
    """Gauss-Jordan nullspace over an abstract field given by callables.
    Used for Q, Q(a) and number fields with the same code path shape."""
    mat = [list(r) for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(mat)) if not is_zero(mat[i][c])),
                   None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = inv(mat[r][c])
        mat[r] = [mul(x, pv) for x in mat[r]]
        for i in range(len(mat)):
            if i != r and not is_zero(mat[i][c]):
                f = mat[i][c]
                mat[i] = [sub(x, mul(f, y)) for x, y in zip(mat[i], mat[r])]
        pivots.append(c)
        r += 1
        if r >= len(mat):
            break
    rank = len(pivots)
    basis = []
    for fc in (c for c in range(ncols) if c not in pivots):
        vec = [zero] * ncols
        vec[fc] = one
        for i, pc in enumerate(pivots):
            vec[pc] = sub(zero, mat[i][fc])
        basis.append(vec)
    return rank, basis

def nullspace_rf(rows, ncols):
    """Nullspace over Q(a); rows contain rf pairs."""
    return nullspace_field(
        rows, ncols, ((), (Fraction(1),)), rf_const(1),
        rf_add, rf_sub, rf_mul, rf_inv, rf_is_zero)

# ============================================ number fields Q[t]/(f)
# Elements: polynomials in t (tuples of Fractions, ascending), degree
# < deg f, f monic irreducible.  Arithmetic is performed mod f.

class NumberField:
    def __init__(self, f):
        self.f = p_trim(f)
        assert self.f and self.f[-1] == 1, "modulus must be monic"
        self.deg = len(f) - 1

    def reduce(self, p):
        p = p_trim(p)
        while len(p) >= len(self.f):
            coef = p[-1]
            i = len(p) - len(self.f)
            sub = [Fraction(0)] * i + [coef * x for x in self.f]
            p = p_sub(p, tuple(sub))
        return p

    def add(self, x, y):
        return p_add(x, y)

    def sub(self, x, y):
        return p_sub(x, y)

    def neg(self, x):
        return p_neg(x)

    def mul(self, x, y):
        return self.reduce(p_mul(x, y))

    def inv(self, x):
        if not x:
            raise ZeroDivisionError("inverse of zero in number field")
        # extended Euclid in Q[t]
        old_r, r = self.f, p_trim(x)
        old_s, s = (), (Fraction(1),)
        while r:
            q, rem = p_divmod(old_r, r)
            old_r, r = r, rem
            old_s, s = s, p_sub(old_s, p_mul(q, s))
        # old_r is a nonzero constant (f irreducible, x nonzero mod f)
        c = old_r[0]
        return self.reduce(p_scale(old_s, 1 / c))

    def is_zero(self, x):
        return not p_trim(x)

    def nullspace(self, rows, ncols):
        return nullspace_field(rows, ncols, (), (Fraction(1),),
                               self.add, self.sub, self.mul, self.inv,
                               self.is_zero)

    def elem_str(self, x):
        return p_str(x).replace("a", "t")
