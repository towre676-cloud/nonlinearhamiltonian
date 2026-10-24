"""Small independent exact-integer polynomial replay; no third-party packages."""
import json
from math import comb, prod
from pathlib import Path


def add(*polys):
    out = {}
    for poly in polys:
        for power, coefficient in poly.items():
            out[power] = out.get(power, 0) + coefficient
    return {power: coefficient for power, coefficient in out.items() if coefficient}


def scale(poly, coefficient):
    return {power: coefficient * value for power, value in poly.items() if coefficient * value}


def multiply(left, right):
    out = {}
    for (a, b), value in left.items():
        for (c, d), factor in right.items():
            out[(a+c, b+d)] = out.get((a+c, b+d), 0) + value * factor
    return {power: coefficient for power, coefficient in out.items() if coefficient}


def derivative(poly, q_order, p_order):
    return {
        (a-q_order, b-p_order): value * prod(range(a-q_order+1, a+1)) * prod(range(b-p_order+1, b+1))
        for (a, b), value in poly.items() if a >= q_order and b >= p_order
    }


H = {(1, 3): 1}


def poisson(poly):
    return add(multiply(derivative(H, 1, 0), derivative(poly, 0, 1)),
               scale(multiply(derivative(H, 0, 1), derivative(poly, 1, 0)), -1))


def transvectant(order, poly):
    return add(*(scale(multiply(derivative(H, order-j, j),
                               derivative(poly, j, order-j)), (-1)**j * comb(order, j))
                 for j in range(order+1)))


def replay():
    poly = {(1, 0): 1}
    rows = []
    for r in range(13):
        coefficient = prod(2*j-3 for j in range(r))
        assert poly == {(1, 2*r): coefficient}
        assert transvectant(3, poly) == {}
        assert transvectant(5, poly) == {}
        rows.append({'r': r, 'coefficient': str(coefficient), 'q_degree': 1,
                     'p_degree': 2*r, 'T3_residual': 0, 'T5_residual': 0,
                     'recurrence_formula_residual': 0})
        poly = poisson(poly)
    return {
        'status': 'passed',
        'arithmetic': 'Python arbitrary-precision integers, generic sparse-polynomial derivatives/products',
        'hamiltonian': 'q*p**3', 'seed_observable': 'q',
        'poisson_convention': 'D(f)=H_q*f_p-H_p*f_q',
        'transvectant_convention': 'sum_j (-1)^j binomial(k,j) d_q^(k-j)d_p^j(H) d_q^j d_p^(k-j)(f)',
        'iterates_tested': 'r=0 through 12', 'rows': rows,
        'all_degree_proof': {
            'T3_operator': '18*p*d_q^2*d_p - 6*q*d_q^3',
            'higher_odd_gates': 'All T_k for k>=5 vanish identically since total degree(H)=4.',
            'recurrence': 'D(q*p**m)=(m-3)*q*p**(m+2)',
            'orbit': 'D^r(q)=product_{j=0}^{r-1}(2*j-3)*q*p**(2*r)',
            'nonzero': '2*j-3 is nonzero for every integer j; distinct p degrees give Q-linear independence.',
            'conclusion': 'q is in the formal polynomial dynamic core, but its polynomial Poisson orbit has infinite dimension.'
        },
        'scope': 'Formal polynomial algebra only. No global operator flow, selfadjointness, expectation complexity or speedup claim.'
    }


if __name__ == '__main__':
    result = replay()
    output = Path(__file__).with_name('core_vs_tractability_exact_replay.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'iterates': len(result['rows']),
                      'output': str(output), 'last_coefficient': result['rows'][-1]['coefficient']}))
