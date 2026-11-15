"""Closed-form first-refinement jump loci on the three branches of the
sixfold-leading family where the global depth theorem left the choice between
least depth 1 and 2 to a finite-window computation (Theorem J of
SIXFOLD_JUMP_LOCI_THEOREM.md).

Each function takes a normalised member (leading coefficient 1, dictionary
{(i, j): Fraction} for q^i p^j) of the stated branch and returns the list of
surviving first-refinement partners beyond span{1, H}, as polynomials.  The
least depth is 2 if the list is nonempty and 1 otherwise, and
dim S^1 = 2 + len(list).
"""
from fractions import Fraction as Fr


def _c(h):
    return lambda i, j: h.get((i, j), Fr(0))


def _poly(terms):
    return {k: Fr(v) for k, v in terms.items() if v != 0}


def quartic_edge_partners(h):
    """Branch c04 != 0 (c05 = c14 = c23 = 0):  H = q^6 + g q^3 p^2 + y p^4 + R."""
    r = _c(h)
    g, y = r(3, 2), r(0, 4)
    if g*g != -40*y:
        return []
    mu = r(1, 3)/(4*y)
    equations = [
        2*y*r(4, 1) - g*r(1, 3),
        -g*mu*r(1, 3) + 2*g*r(2, 2) - 6*r(1, 3)*r(4, 1) + 40*r(5, 0)*y,
        6*g*mu*r(2, 2) + 3*g*r(3, 1) - 10*mu*r(1, 3)*r(4, 1) + 40*mu*r(5, 0)*y + 60*r(0, 3)
        + 10*r(1, 3)*r(5, 0) - 4*r(2, 2)*r(4, 1),
        3*g*mu*r(1, 2) + 3*g*r(2, 1) - 6*mu*r(0, 3)*r(4, 1) - 6*mu*r(1, 3)*r(3, 1) + 2*mu*r(2, 2)**2
        + 24*mu*r(4, 0)*y + 30*r(0, 3)*r(5, 0) - 6*r(1, 2)*r(4, 1),
        -3*g*mu*r(0, 3) - 3*g*r(1, 2) + 6*r(0, 3)*r(4, 1) - 6*r(1, 3)*r(3, 1) + 2*r(2, 2)**2 + 24*r(4, 0)*y,
        -3*mu*r(0, 3)*r(3, 1) + 2*mu*r(1, 2)*r(2, 2) - 3*mu*r(1, 3)*r(2, 1) + 12*mu*r(3, 0)*y
        + 12*r(0, 3)*r(4, 0) - 3*r(1, 2)*r(3, 1) - 3*r(1, 3)*r(3, 0) + 2*r(2, 1)*r(2, 2),
    ]
    if any(e != 0 for e in equations):
        return []
    return [_poly({(0, 1): 1, (1, 0): mu})]


def cubic_coefficient_partners(h):
    """Branch c32 != 0 (c05 = c14 = c23 = c04 = 0):  H = f + A p + B p^2 + (c03 + c13 q) p^3."""
    r = _c(h)
    b = [r(i, 2) for i in range(4)]
    if r(0, 3) != 0 or r(1, 3) != 0 or b[2]**2 != 3*b[3]*b[1]:
        return []
    s = -b[2]/(3*b[3])
    delta = b[0] + b[1]*s + b[2]*s**2 + b[3]*s**3          # B = b3 (q - s)^3 + delta
    # A in powers of x = q - s
    a = [r(i, 1) for i in range(5)]
    from math import comb
    ax = [sum(a[i]*comb(i, k)*s**(i - k) for i in range(k, 5)) for k in range(5)]
    # x A' - 2 A = sum (k - 2) ax_k x^k ; quotient by 2 B = 2 b3 x^3 + 2 delta
    q1, q0 = 2*ax[4]/(2*b[3]), ax[3]/(2*b[3])              # phi' = q1 x + q0
    # phi = q1 x^2/2 + q0 x, rewritten in q
    partner = {(1, 1): Fr(1), (0, 1): -s,
               (2, 0): q1/2, (1, 0): -q1*s + q0, (0, 0): q1*s*s/2 - q0*s}
    return [_poly(partner)]


def cubic_form_partners(h):
    """Branch c03 != 0 off the cube locus:  H = q^6 + a q^4 p + b q^2 p^2 + x p^3 + R, wt R < 6."""
    r = _c(h)
    a, b, x = r(4, 1), r(2, 2), r(0, 3)
    assert x != 0 and not (3*b == a*a and 27*x == a**3)
    out = []
    delta_w = b*b - 3*a*x
    gamma2 = 12*a*a*x*x + 4*a*b*b*x - b**4 - 45*b*x*x
    if delta_w == 0 and 3*x*r(3, 1) == 2*b*r(1, 2):
        out.append(_poly({(1, 0): 1}))
    if gamma2 == 0:
        if b != 0:
            lam = (3*a*x + b*b)/(6*b*x)
            mu = (-6*a*r(1, 2) + 10*b*lam*r(1, 2) - 21*lam*r(3, 1)*x + 30*r(5, 0)*x)/(-2*delta_w)
            xi = (-2*b*mu*r(1, 2) - 2*b*r(2, 1) - 4*lam*r(1, 2)**2 + 12*lam*r(2, 1)*x
                  + 3*mu*r(3, 1)*x + 3*r(1, 2)*r(3, 1) - 12*r(4, 0)*x)
            if xi == 0:
                out.append(_poly({(0, 1): 1, (2, 0): lam, (1, 0): mu}))
        elif r(3, 1) == 0 and r(1, 2)**2 == 3*x*r(2, 1):          # a = b = 0
            out.append(_poly({(2, 0): 1}))
    # the two weight-4 points have no rational representative (their coordinate
    # beta^3/x^2 is a root of 2842 t^2 - 53565 t - 245025); see the theorem note.
    return out
