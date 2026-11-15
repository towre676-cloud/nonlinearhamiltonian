"""Trajectory-only Hamiltonian identification and numerical locus tests.

The public measurement model assumes qdot = H_p, pdot = -H_q and a
normalised q^6 leading term. The constant coefficient is unobservable.
"""
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss, legfit, legint, legval, legvander
from scipy.integrate import solve_ivp
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter


TERMS = tuple((i, degree - i) for degree in range(1, 6) for i in range(degree + 1))
LEADING = (6, 0)
HIGH = ((0, 5), (1, 4), (2, 3), (0, 4), (3, 2), (1, 3), (0, 3))
FAMILIES = ('quartic', 'c32', 'delta', 'gamma', 'origin', 'depth-six')


def field_features(states, terms):
    """Return the canonical vector field of each monomial at each state."""
    q, p = np.moveaxis(states, -1, 0)
    return np.stack([
        np.stack([j*q**i*p**(j-1) if j else np.zeros_like(q),
                  -i*q**(i-1)*p**j if i else np.zeros_like(p)], axis=-1)
        for i, j in terms
    ], axis=-1)


@dataclass(frozen=True)
class Fit:
    coefficients: np.ndarray
    inverse_information: np.ndarray
    residual_scale: float
    condition: float


def fit_field(times, states, sigma, method):
    if method == 'local':
        # Local cubic fits estimate both position and velocity on the sample grid.
        dt = times[1] - times[0]
        smooth = savgol_filter(states, 9, 3, axis=1)
        moments = savgol_filter(states, 9, 3, deriv=1, delta=dt, axis=1)
        library = field_features(smooth, TERMS + (LEADING,))
        floor = sigma / (times[-1] - times[0])
    elif method == 'weak':
        # Integration by parts against primitives of P_1,...,P_6. The
        # primitives vanish at both endpoints, avoiding noisy endpoint differences.
        half_span = (times[-1] - times[0]) / 2
        grid = (times - times[0]) / half_span - 1
        nodes, weights = leggauss(5)
        left, right = grid[:-1], grid[1:]
        widths = (right - left)/2
        sample = ((right + left)[:, None]/2 + widths[:, None]*nodes).ravel()
        weights = (widths[:, None]*weights/2).ravel()
        if sigma:
            series = legfit(grid, states.transpose(1, 0, 2).reshape(len(times), -1), 6)
            smooth = legval(sample, series).T.reshape(len(sample), len(states), 2).transpose(1, 0, 2)
        else:
            smooth = make_interp_spline(grid, states, k=5, axis=1)(sample)
        basis = legvander(sample, 6)[:, 1:]
        primitive = legval(sample, legint(np.eye(7), lbnd=-1)).T[:, 1:]
        normalizer = np.sqrt(2*np.arange(1, 7)+1)
        moments = -np.einsum('t,tk,stc->skc', weights, basis*normalizer, smooth)
        library = np.einsum('t,tk,stcm->skcm', weights,
                            half_span*primitive*normalizer,
                            field_features(smooth, TERMS + (LEADING,)))
        floor = sigma / np.sqrt(len(times))
    else:
        raise ValueError(f'unknown field estimator {method}')

    matrix = library[..., :-1].reshape(-1, len(TERMS))
    target = (moments - library[..., -1]).ravel()
    # Column scaling changes conditioning but leaves the least-squares solution
    # unchanged. Retain the SVD to propagate coefficient uncertainty.
    scale = np.maximum(np.linalg.norm(matrix, axis=0), 1e-30)
    u, singular, vt = np.linalg.svd(matrix/scale, full_matrices=False)
    stable = np.maximum(singular, singular[0]*1e-12)
    inverse = (vt.T/scale[:, None])/stable
    coefficients = inverse @ (u.T @ target)
    rms = np.linalg.norm(matrix @ coefficients - target)/np.sqrt(len(target)-len(TERMS))
    return Fit(coefficients, inverse, max(float(rms), floor, 1e-13),
               float(singular[0]/max(singular[-1], 1e-30)))



def regularize(fit, center, prior_root):
    """Gaussian shrinkage in the weak moment metric, with a train-only prior."""
    centered = np.linalg.solve(fit.inverse_information, fit.coefficients-center)
    matrix = np.linalg.solve(fit.inverse_information, prior_root)/fit.residual_scale
    u, singular, vt = np.linalg.svd(matrix, full_matrices=False)
    precision = 1+singular**2
    root = prior_root @ vt.T
    updated = center + root @ (singular/precision*(u.T @ centered))/fit.residual_scale
    # Fold the fitted noise scale in here to preserve the Fit convention.
    uncertainty = (root/np.sqrt(precision))/fit.residual_scale
    return Fit(updated, uncertainty, fit.residual_scale, fit.condition)

def equations(coefficients, family):
    """Polynomial constraints obtained from Theorems G and J.

    These numerical tests use closures of branches. A zero residual by itself
    cannot establish branch membership or prove a refinement depth.
    """
    terms = dict(zip(TERMS, coefficients))
    c = lambda i, j: terms[i, j]
    a, b, x = c(4, 1), c(2, 2), c(0, 3)
    y, g = c(0, 4), c(3, 2)
    r13, r31, r12, r21, r50, r40 = (c(i, j) for i, j in
                                    ((1, 3), (3, 1), (1, 2), (2, 1), (5, 0), (4, 0)))
    if family == 'quartic':
        return np.array([*(c(*m) for m in HIGH[:3]),
                         g*g+40*y, 2*y*a-g*r13,
                         160*y*y*r50-g*(13*r13*r13-8*y*b),
                         160*y*y*x+g*(r13**3-4*y*r13*b+8*y*y*r31),
                         384*y**3*r40+9*r13**4-36*y*r13*r13*b-24*y*y*r13*r31
                         -48*g*y*y*r12+32*y*y*b*b,
                         1280*y**4*r21-3*g*r13**5+16*g*y*r13**3*b
                         -24*g*y*y*r13*r13*r31-16*g*y*y*r13*b*b
                         +32*g*y**3*b*r31-640*y**3*r12*r13])
    if family == 'c32':
        return np.array([*(c(*m) for m in HIGH if m != (3, 2)), b*b-3*g*r12])
    if family == 'depth-six':
        k = 4*c(0, 2)
        return np.array([*(c(*m) for m in HIGH), r12, b, a,
                         r31*r31-k, k*r50-2*r31*r21,
                         k*r40-r21*r21-2*r31*c(1, 1)])
    prefix = [c(*m) for m in HIGH[:-1]]
    if family == 'delta':
        return np.array([*prefix, b*b-3*a*x, 3*x*r31-2*b*r12])
    if family == 'origin':
        # This sublocus has both the q and q^2 partners. The delta test
        # already includes the larger q-only locus at a=b=0.
        return np.array([*prefix, a, b, r31, r12*r12-3*x*r21])
    if family != 'gamma':
        raise ValueError(f'unknown locus {family}')
    delta = b*b-3*a*x
    lambda_num, lambda_den = 3*a*x+b*b, 6*b*x
    mu_num = ((6*a*r12-30*x*r50)*lambda_den
              + (-10*b*r12+21*x*r31)*lambda_num)
    mu_den = 2*delta*lambda_den
    xi_num = ((-2*b*r12+3*x*r31)*mu_num
              + (-2*b*r21+3*r12*r31-12*x*r40)*mu_den
              + (-4*r12*r12+12*x*r21)*lambda_num*2*delta)
    return np.array([*prefix, 12*a*a*x*x+4*a*b*b*x-b**4-45*b*x*x, xi_num])


def distances(fit, guard_branches=False):
    """Local distances to constraint surfaces in the field-fit metric.

    These are first-order diagnostics, not calibrated chi-square statistics.
    Project in whitened coefficient coordinates and count all restrictions,
    including branch support. No true stratum or perturbation axis is supplied.
    """
    c = fit.coefficients
    if guard_branches:
        # Degenerate closures can spuriously accept a different branch (for
        # instance the cleared gamma equation when beta is zero). Resolve
        # leading support in theorem order when distinguishable from zero.
        se = fit.residual_scale*np.linalg.norm(fit.inverse_information, axis=1)
        detected = dict(zip(TERMS, abs(c) > 4*se))
        if detected[0, 4]:
            eligible = {'quartic'}
        elif detected[3, 2]:
            eligible = {'c32'}
        elif detected[0, 3]:
            eligible = {'delta', 'origin'}
            if detected[2, 2]:
                eligible.add('gamma')
        else:
            eligible = {'depth-six'}
    else:
        eligible = set(FAMILIES)
    result = []
    for family in FAMILIES:
        if family not in eligible:
            result.append(1e30)
            continue
        residual = equations(c, family)
        jacobian = np.stack([equations(c + 1e-24j*e, family).imag/1e-24
                             for e in np.eye(len(c))], axis=1)
        design = jacobian @ fit.inverse_information
        scale = np.maximum(np.linalg.norm(design, axis=1), 1e-24)
        direction, _, _, _ = np.linalg.lstsq(design/scale[:, None], residual/scale, rcond=1e-10)
        remainder = (design @ direction-residual)/scale
        distance = np.hypot(np.linalg.norm(direction), np.linalg.norm(remainder))
        result.append(distance/(np.sqrt(len(residual))*fit.residual_scale))
    return np.asarray(result)


def rational_candidate(fit, times, states):
    """Propose one rational model from noiseless tracks and replay it.

    Fit and replay tolerances are numerical heuristics. Only replayed
    models are passed to the exact theorem code, with no depth guarantee
    about the unknown generating system.
    """
    coefficients = {LEADING: Fraction(1)}
    for term, value in zip(TERMS, fit.coefficients):
        # Pick the simplest approximant found by the fixed denominator ladder.
        for bound in (20, 100, 1_000, 10_000, 1_000_000):
            candidate = Fraction(float(value)).limit_denominator(bound)
            if abs(candidate-value) <= 2e-7:
                if candidate:
                    coefficients[term] = candidate
                break
        else:
            return None
    terms, values = zip(*coefficients.items())
    values = np.asarray(values, dtype=float)

    def rhs(_, state):
        return field_features(state, terms) @ values

    for track in states:
        sol = solve_ivp(rhs, (times[0], times[-1]), track[0], t_eval=times,
                        method='DOP853', rtol=1e-11, atol=1e-12)
        if not sol.success or np.max(np.abs(sol.y.T-track)) > 2e-8:
            return None
    source = exact_source()
    result = source.classify(coefficients)
    partner = {(1, 0): Fraction(1)} if result['depth'] == 6 else None
    if result.get('partners'):
        partner = result['partners'][0]
    witness = replay_witness(source, coefficients, partner, result['depth']) if partner else None
    return {'coefficients': [[i, j, str(c)] for (i, j), c in sorted(coefficients.items())],
            'candidate_depth': result['depth'], 'branch': result['branch'],
            'theorems': result['sources'], 'witness': witness}


def replay_witness(source, coefficients, partner, depth):
    def serialize(poly):
        return [[i, j, str(c)] for (i, j), c in sorted(poly.items()) if c]

    current = partner
    for iterate in range(depth+1):
        t3 = source.transvectant(coefficients, current, 3)
        t5 = source.transvectant(coefficients, current, 5)
        if t3 or t5:
            assert iterate == depth
            return {'probe': serialize(partner), 'first_failure_iterate': iterate,
                    'T3': serialize(t3), 'T5': serialize(t5)}
        current = source.transvectant(coefficients, current, 1)
    raise AssertionError('expected a nonzero exact obstruction')


def classify_exact(coefficients):
    return exact_source().classify(coefficients)


def exact_source():
    source = Path(__file__).resolve().parent / 'sources'
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))
    import sixfold_global_depth

    return sixfold_global_depth
