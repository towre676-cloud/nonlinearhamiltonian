"""Compile and check small common classical polynomial observable modules."""
from fractions import Fraction
from math import comb, factorial

try:
    from .polynomial import (LinearBasis, ONE, P, Q, add, clean, decode, derivative,
                             encode, evaluate, monomial, multiply, physical_lie,
                             power, scale, substitute, weighted_degree)
except ImportError:
    from polynomial import (LinearBasis, ONE, P, Q, add, clean, decode, derivative,
                            encode, evaluate, monomial, multiply, physical_lie,
                            power, scale, substitute, weighted_degree)


def physical_outputs(shear):
    c = Fraction(shear)
    physical_p = add(P, scale(power(Q, 2), -c))
    return {'one': ONE, 'q': Q, 'p': physical_p, 'q2': power(Q, 2),
            'qp': multiply(Q, physical_p), 'p2': power(physical_p, 2)}


def controlled_generators():
    return {'cubic_transport': scale(power(P, 3), Fraction(1, 3)),
            'lambda': Q, 'mu': multiply(Q, P)}


def discover(outputs, generators, maximum_dimension=100, maximum_weight=64):
    """Exact reachable-span construction; resource exhaustion never means closure."""
    basis = LinearBasis()
    for seed in outputs.values():
        basis.insert(seed)
    rank_history = [len(basis.rows)]
    while True:
        additions = []
        for row in list(basis.rows):
            for name, hamiltonian in generators.items():
                image = physical_lie(hamiltonian, row)
                if weighted_degree(image) > maximum_weight:
                    return basis, {'closed': False, 'reason': 'weight_limit',
                        'generator': name, 'image': encode(image), 'rank_history': rank_history}
                if basis.insert(image):
                    additions.append(name)
                    if len(basis.rows) >= maximum_dimension:
                        return basis, {'closed': False, 'reason': 'dimension_limit',
                            'rank_history': rank_history+[len(basis.rows)]}
        rank_history.append(len(basis.rows))
        if not additions:
            return basis, {'closed': True, 'rank_history': rank_history}


def compile_family(shear=Fraction(1)):
    c = Fraction(shear)
    outputs, generators = physical_outputs(c), controlled_generators()
    basis, discovery = discover(outputs, generators)
    if not discovery['closed']:
        raise ValueError('intended finite family did not close')
    actions = {}
    for name, hamiltonian in generators.items():
        actions[name] = [[str(value) for value in basis.coordinates(physical_lie(hamiltonian, row))]
                         for row in basis.rows]
    return {'schema': 'classical-common-observable-v1', 'shear': str(c),
        'coordinate_map': 'Q=q, P=p+c*q**2',
        'generator_convention': 'L(F)=H_P*F_Q-H_Q*F_P; minus repository D={H,F}',
        'dimension': len(basis.rows), 'maximum_weight': max(map(weighted_degree, basis.rows)),
        'basis': [encode(row) for row in basis.rows],
        'generators': {name: encode(h) for name, h in generators.items()},
        'outputs': {name: encode(poly) for name, poly in outputs.items()},
        'output_coordinates': {name: [str(value) for value in basis.coordinates(poly)]
                               for name, poly in outputs.items()},
        'actions': actions, 'discovery': discovery,
        'scope': 'Prescribed classical Hamiltonians sharing this fixed shear. No self-consistent space-charge closure, global flow/domain or speedup claim.'}


def linear_combination(coefficients, rows):
    if len(coefficients) != len(rows):
        raise ValueError('coordinate dimension mismatch')
    return add(*(scale(row, Fraction(value)) for value, row in zip(coefficients, rows)))


def check_certificate(certificate):
    """Check declared action/reconstruction identities, without rerunning discovery."""
    if certificate['schema'] != 'classical-common-observable-v1':
        raise ValueError('unsupported certificate schema')
    c = Fraction(certificate['shear'])
    rows = [decode(row) for row in certificate['basis']]
    expected_weight = 4 if c == 0 else 8
    expected_keys = {(a, b) for a in range(expected_weight//2+1)
                     for b in range(expected_weight-2*a+1)}
    if certificate['dimension'] != len(rows) or certificate['maximum_weight'] != expected_weight:
        raise ValueError('dimension/weight declaration mismatch')
    basis = LinearBasis()
    for row in rows:
        if weighted_degree(row) > expected_weight or not basis.insert(row):
            raise ValueError('basis is dependent or outside weighted space')
    if len(rows) != len(expected_keys):
        raise ValueError('basis does not span complete claimed weighted space')
    outputs, generators = physical_outputs(c), controlled_generators()
    if set(certificate['outputs']) != set(outputs) or set(certificate['generators']) != set(generators):
        raise ValueError('output or generator set mismatch')
    checks = 0
    for name, hamiltonian in generators.items():
        if decode(certificate['generators'][name]) != hamiltonian:
            raise ValueError('generator mismatch')
        matrix = certificate['actions'][name]
        if len(matrix) != len(rows):
            raise ValueError('action row count')
        for row, coefficients in zip(rows, matrix):
            if linear_combination(coefficients, rows) != physical_lie(hamiltonian, row):
                raise ValueError('action identity failed')
            checks += 1
    for name, poly in outputs.items():
        if decode(certificate['outputs'][name]) != poly:
            raise ValueError('physical output mismatch')
        if linear_combination(certificate['output_coordinates'][name], rows) != poly:
            raise ValueError('output reconstruction identity failed')
        checks += 1
    return {'status': 'passed', 'dimension': len(rows), 'action_and_output_identities': checks}


def first_missing_image(certificate, extra_hamiltonian):
    basis = LinearBasis()
    for row in certificate['basis']:
        basis.insert(decode(row))
    for row in basis.rows:
        image = physical_lie(extra_hamiltonian, row)
        _, residual = basis.reduce(image)
        if residual:
            return {'closed': False, 'input': encode(row), 'image': encode(image),
                    'missing_polynomial': encode(residual),
                    'scope': 'Exact failure of this finite module, not by itself a general nonclosure theorem.'}
    return {'closed': True}


def hidden_cloud_witness(kick=Fraction(1, 7), shear=Fraction(1), transport=Fraction(1, 3)):
    """Positive/negative parts of Delta_Q Delta_P^7 give two probability laws."""
    plus, minus = [], []
    for q in range(2):
        for p in range(8):
            weight = (-1)**(8-q-p)*comb(7, p)
            (plus if weight > 0 else minus).append((Fraction(q), Fraction(p), Fraction(abs(weight), 128)))
    def mean(poly, cloud):
        return sum((weight*evaluate(poly, q, p) for q, p, weight in cloud), Fraction(0))
    if not sum(row[2] for row in plus) == sum(row[2] for row in minus) == 1:
        raise ValueError('cloud normalization failed')
    for a in range(5):
        for b in range(9-2*a):
            f = monomial(a, b)
            if mean(f, plus) != mean(f, minus):
                raise ValueError('cloud moment equality failed')
    target = power(P, 8)
    after = substitute(target, Q, add(P, scale(Q, -2*Fraction(kick))))
    difference = mean(after, plus)-mean(after, minus)
    if difference != -630*Fraction(kick):
        raise ValueError('cloud future P**8 difference failed')
    physical_p2 = physical_outputs(shear)['p2']
    physical_after_transport = substitute(physical_p2, add(Q, scale(power(P, 2), Fraction(transport))), P)
    physical_after_word = substitute(physical_after_transport, Q, add(P, scale(Q, -2*Fraction(kick))))
    physical_difference = mean(physical_after_word, plus)-mean(physical_after_word, minus)
    if physical_difference != -630*Fraction(kick)*Fraction(shear)**2*Fraction(transport)**4:
        raise ValueError('cloud future physical p**2 difference failed')
    final_adapted_p = add(P, scale(Q, -2*Fraction(kick)))
    final_q = add(Q, scale(power(final_adapted_p, 2), Fraction(transport)))
    final_physical_p = add(final_adapted_p, scale(power(final_q, 2), -Fraction(shear)))
    covariance_rows = []
    for law in [plus, minus]:
        mq, mp = mean(final_q, law), mean(final_physical_p, law)
        a = mean(power(final_q, 2), law)-mq*mq
        b = mean(multiply(final_q, final_physical_p), law)-mq*mp
        z = mean(power(final_physical_p, 2), law)-mp*mp
        covariance_rows.append((a, b, z, a*z-b*b))
    if covariance_rows[0][:2] != covariance_rows[1][:2]:
        raise ValueError('expected equal position variance/cross covariance')
    emittance_difference = covariance_rows[0][3]-covariance_rows[1][3]
    if emittance_difference != covariance_rows[0][0]*physical_difference:
        raise ValueError('future squared-emittance difference')
    return {'schema': 'finite-cloud-observability-witness-v1',
        'plus': [[str(v) for v in row] for row in plus],
        'minus': [[str(v) for v in row] for row in minus],
        'all_25_weighted_moments_agree': True, 'extra_hamiltonian': 'Q**2',
        'kick_time': str(kick), 'queried_retained_observable': 'P**8',
        'future_expectation_plus_minus_difference': str(difference),
        'physical_readout': 'p**2 after Q**2 kick then P**3/3 transport',
        'fixed_shear': str(shear), 'transport_time': str(transport),
        'future_physical_second_moment_difference': str(physical_difference),
        'future_position_variance': str(covariance_rows[0][0]),
        'future_position_variance_and_cross_covariance_agree': True,
        'future_projected_emittance_squared_difference': str(emittance_difference),
        'scope': 'Finite positive probability laws, not a smooth Vlasov-density or finite phase-cap witness.'}


def quadratic_backbone(a, b, c, d):
    a, b, c, d = map(Fraction, (a, b, c, d))
    if not a:
        raise ValueError('a!=0 required for this completion-of-square route')
    alpha = c/(2*a)
    delta = d-c*c/(4*a)
    original = add(scale(power(P, 2), a), scale(power(Q, 2), b),
                   scale(multiply(power(Q, 2), P), c), scale(power(Q, 4), d))
    transformed = substitute(original, Q, add(P, scale(power(Q, 2), -alpha)))
    target = add(scale(power(P, 2), a), scale(power(Q, 2), b), scale(power(Q, 4), delta))
    if transformed != target:
        raise ValueError('completion-of-square identity failed')
    return {'a': str(a), 'b': str(b), 'c': str(c), 'd': str(d),
            'shear_alpha': str(alpha), 'delta': str(delta), 'quadratic': delta == 0,
            'transformed_hamiltonian': encode(target), 'residual_force': encode(scale(power(Q, 3), -4*delta))}


def shared_backbone(records, alpha):
    """Verify the proposed shared shear; mismatch is not universal nonclosure."""
    alpha = Fraction(alpha)
    routes = []
    for index, row in enumerate(records):
        a, b, c, d = map(Fraction, row)
        cross = c-2*a*alpha
        if cross:
            return {'shared_shear_verified': False, 'failed_generator': index,
                    'remaining_Q2P_coefficient': str(cross),
                    'scope': 'This proposed shared shear fails; no claim that every adapted representation fails.'}
        routes.append({'a': str(a), 'b': str(b), 'remaining_Q4_coefficient': str(d-a*alpha**2)})
    return {'shared_shear_verified': True, 'shear_alpha': str(alpha), 'routes': routes}


def residual_observable_bound(poly, delta, q_radius, p_radius):
    """Conditional sup bound for L_delta(F) on the declared adapted rectangle."""
    delta, r, s = map(Fraction, (delta, q_radius, p_radius))
    if r < 0 or s < 0:
        raise ValueError('nonnegative support radii required')
    defect = scale(multiply(power(Q, 3), derivative(poly, 1)), -4*delta)
    bound = sum((abs(value)*r**a*s**b for (a, b), value in defect.items()), Fraction(0))
    return defect, bound


def finite_word_pullback(outputs, maps):
    """An exact sufficient initial summary for one finite declared map word."""
    pulled = dict(outputs)
    for q_image, p_image in reversed(maps):
        pulled = {name: substitute(poly, q_image, p_image) for name, poly in pulled.items()}
    terms = sorted(set().union(*(set(poly) for poly in pulled.values())))
    return {'pulled_outputs': {name: encode(poly) for name, poly in pulled.items()},
            'initial_monomials': [list(term) for term in terms],
            'monomial_count': len(terms),
            'maximum_weight': max(map(weighted_degree, pulled.values())),
            'scope': 'Exact sufficient monomial summary for this finite word, not a minimal invariant module or a continuous-aperture safety proof.'}
