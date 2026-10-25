"""Independent, stdlib-only checker for correction-free Moyal partners.

Scope, stated plainly:
- Formal polynomials in q, p over the rationals, flat Weyl-Moyal convention.
- The Moyal bracket is (H star G - G star H) / (i*hbar).
- Its hbar expansion is sum_{m>=0} (-1)^m * hbar^(2m) * D^(2m+1)(H,G)
  / (2^(2m) * (2m+1)!), where D is the bidifferential operator
  D(f,g) = (dq f)(dp g) - (dp f)(dq g).
  Hence m=0 is the Poisson bracket, and correction-free means
  D^(2m+1)(H,G) = 0 for every m>=1.
- This file does NOT prove a general classification. It computes
  finite, exact instances and homogeneous kernels, so a later
  comparison with the repository classifier is a genuine independent check.
- Dynamic cores, analytic operator domains and global flows are
  outside this checker.
"""

from fractions import Fraction
from itertools import product
from math import comb, factorial

# Polynomial: dict[(a, b)] -> Fraction, for q^a p^b. Zero terms omitted.


def clean(poly):
    return {k: v for k, v in poly.items() if v != 0}


def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Fraction(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def scale(poly, s):
    return clean({k: v * s for k, v in poly.items()})


def falling(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r *= n - i
    return r


def deriv(poly, dq, dp):
    out = {}
    for (a, b), c in poly.items():
        if a < dq or b < dp:
            continue
        out[(a - dq, b - dp)] = out.get((a - dq, b - dp), Fraction(0)) + c * falling(a, dq) * falling(b, dp)
    return clean(out)


def mul(a, b):
    out = {}
    for (a1, b1), c1 in a.items():
        for (a2, b2), c2 in b.items():
            k = (a1 + a2, b1 + b2)
            out[k] = out.get(k, Fraction(0)) + c1 * c2
    return clean(out)


def d_power(f, g, k):
    """D^k(f, g) with D = dq<- dp-> - dp<- dq->."""
    out = {}
    for j in range(k + 1):
        # (dq^j dp^(k-j) f) * (dp^j dq^(k-j) g), sign (-1)^(k-j)
        left = deriv(f, j, k - j)
        right = deriv(g, k - j, j)
        term = mul(left, right)
        sign = -1 if (k - j) % 2 else 1
        out = add(out, scale(term, Fraction(sign * comb(k, j))))
    return out


def moyal_bracket_series(f, g):
    """Return {hbar-power: polynomial} for the Moyal bracket, up to the
    highest odd D-power that can be nonzero for these degrees."""
    max_deg = max((a + b for a, b in f), default=0) + max((a + b for a, b in g), default=0)
    series = {}
    m = 0
    while True:
        k = 2 * m + 1
        if k > max_deg + 1 and m > 0:
            break
        term = d_power(f, g, k)
        if term:
            coeff = Fraction((-1) ** m, (2 ** (2 * m)) * factorial(k))
            series[2 * m] = scale(term, coeff)
        if k > max_deg:
            break
        m += 1
    return series


def is_correction_free(f, g):
    series = moyal_bracket_series(f, g)
    return all(v == {} for power, v in series.items() if power > 0), series


def monomial(a, b, coeff=1):
    return {(a, b): Fraction(coeff)}


def fmt(poly):
    if not poly:
        return "0"
    parts = []
    for (a, b), c in sorted(poly.items()):
        term = ""
        if a:
            term += f"q^{a}" if a > 1 else "q"
        if b:
            term += f"p^{b}" if b > 1 else "p"
        if not term:
            term = "1"
        parts.append(f"{c}*{term}" if c != 1 else term)
    return " + ".join(parts)


def nullspace(rows, ncols):
    """Exact rational nullspace of a list of rows (each length ncols).
    Returns a list of basis vectors (lists of Fractions)."""
    mat = [list(r) for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(mat)):
            if mat[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        mat[r] = [x / pv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                factor = mat[i][c]
                mat[i] = [x - factor * y for x, y in zip(mat[i], mat[r])]
        pivots.append(c)
        r += 1
        if r >= len(mat):
            break
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        vec = [Fraction(0)] * ncols
        vec[fc] = Fraction(1)
        for i, pc in enumerate(pivots):
            vec[pc] = -mat[i][fc]
        basis.append(vec)
    return basis


def homogeneous_kernel(h, degree):
    """Basis for homogeneous polynomials G of total degree `degree` with
    D^(2m+1)(h, G) = 0 for all m>=1. Each basis vector is returned as a
    polynomial dict. Works for homogeneous h; for inhomogeneous h the
    separate degree components of each D-term are separate equations,
    which is what the row construction below does."""
    mons = [(a, degree - a) for a in range(degree + 1)]
    # Collect equations: for each odd k>=3, for each monomial in D^k(h, G),
    # the coefficient must be 0. Coefficient is linear in G's coefficients.
    rows = []
    # Build D^k(h, basis monomial) for each basis monomial, then read off.
    max_k = max((a + b for a, b in h), default=0) + degree
    for k in range(3, max_k + 1, 2):
        col_polys = [d_power(h, monomial(a, b), k) for (a, b) in mons]
        keys = sorted({key for poly in col_polys for key in poly})
        for key in keys:
            rows.append([poly.get(key, Fraction(0)) for poly in col_polys])
    basis_vecs = nullspace(rows, len(mons))
    out = []
    for vec in basis_vecs:
        poly = {}
        for coeff, (a, b) in zip(vec, mons):
            if coeff:
                poly[(a, b)] = coeff
        out.append(poly)
    return out


if __name__ == "__main__":
    print("=== 1. Poisson and corrections for H = q*p^3, G = q^2 ===")
    h = monomial(1, 3)
    g = monomial(2, 0)
    series = moyal_bracket_series(h, g)
    for power in sorted(series):
        print(f"hbar^{power}: {fmt(series[power])}")
    print("correction-free:", all(v == {} for p, v in series.items() if p > 0))

    print("\n=== 2. Monomial partners of H = q*p^3, G = q^c p^d, c+d <= 6 ===")
    for c, d in product(range(7), repeat=2):
        if c + d == 0:
            continue
        free, _ = is_correction_free(h, monomial(c, d))
        if free:
            print(f"  G = q^{c} p^{d}  correction-free")

    print("\n=== 3. Homogeneous kernel, H = q^4 + p^4, degree 6 ===")
    h4 = add(monomial(4, 0), monomial(0, 4))
    basis = homogeneous_kernel(h4, 6)
    print(f"dimension: {len(basis)}")
    for poly in basis:
        print(f"  {fmt(poly)}")

    print("\n=== 4. Homogeneous kernel, H = q^3, degree 4 (sanity / monomial sector) ===")
    basis3 = homogeneous_kernel(monomial(3, 0), 4)
    print(f"dimension: {len(basis3)}")
    for poly in basis3:
        print(f"  {fmt(poly)}")
