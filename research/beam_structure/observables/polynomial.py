"""Two-variable exact polynomial operations; coordinates are always (Q, P)."""
from fractions import Fraction
from math import comb


def clean(poly):
    return {tuple(k): Fraction(v) for k, v in poly.items() if v}


def monomial(q, p, coefficient=1):
    if not isinstance(q, int) or not isinstance(p, int) or min(q, p) < 0:
        raise ValueError('nonnegative integral powers required')
    return clean({(q, p): coefficient})


ONE = monomial(0, 0)
Q = monomial(1, 0)
P = monomial(0, 1)


def add(*polys):
    result = {}
    for poly in polys:
        for key, value in poly.items():
            result[key] = result.get(key, 0) + value
    return clean(result)


def scale(poly, coefficient):
    return clean({key: value * coefficient for key, value in poly.items()})


def multiply(left, right):
    result = {}
    for (a, b), coefficient in left.items():
        for (c, d), factor in right.items():
            key = (a+c, b+d)
            result[key] = result.get(key, 0) + coefficient * factor
    return clean(result)


def power(poly, exponent):
    if not isinstance(exponent, int) or exponent < 0:
        raise ValueError('nonnegative integral exponent required')
    result = ONE
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def derivative(poly, axis):
    if axis not in (0, 1):
        raise ValueError('axis must be zero or one')
    result = {}
    for powers, coefficient in poly.items():
        if powers[axis]:
            new = list(powers)
            new[axis] -= 1
            result[tuple(new)] = coefficient * powers[axis]
    return clean(result)


def physical_lie(hamiltonian, observable):
    """H_P*d_Q(F)-H_Q*d_P(F): minus the repo's D={H,F}."""
    return add(multiply(derivative(hamiltonian, 1), derivative(observable, 0)),
               scale(multiply(derivative(hamiltonian, 0), derivative(observable, 1)), -1))


def substitute(poly, q_image, p_image):
    return add(*(scale(multiply(power(q_image, a), power(p_image, b)), value)
                 for (a, b), value in poly.items()))


def evaluate(poly, q, p):
    q, p = Fraction(q), Fraction(p)
    return sum((value * q**a * p**b for (a, b), value in poly.items()), Fraction(0))


def weighted_degree(poly):
    return max((2*a+b for a, b in poly), default=-1)


def total_degree(poly):
    return max((a+b for a, b in poly), default=-1)


def key_order(key):
    a, b = key
    return (2*a+b, a, b)


def encode(poly):
    return [{'q': a, 'p': b, 'coefficient': str(poly[a, b])}
            for a, b in sorted(poly, key=key_order)]


def decode(rows):
    result = {}
    for row in rows:
        powers = row['q'], row['p']
        if (not all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in powers)
                or powers in result):
            raise ValueError('invalid or duplicate monomial')
        coefficient = Fraction(row['coefficient'])
        if not coefficient:
            raise ValueError('zero coefficient is not canonical')
        result[powers] = coefficient
    return result


class LinearBasis:
    """Exact reduced row basis in the finite span encountered by the compiler."""

    def __init__(self):
        self.rows = []

    def reduce(self, poly):
        residual = clean(poly)
        coordinates = []
        for row in self.rows:
            pivot = min(row, key=key_order)
            coefficient = residual.get(pivot, Fraction(0))
            coordinates.append(coefficient)
            residual = add(residual, scale(row, -coefficient))
        return coordinates, residual

    def insert(self, poly):
        _, residual = self.reduce(poly)
        if not residual:
            return False
        pivot = min(residual, key=key_order)
        row = scale(residual, 1/residual[pivot])
        self.rows = [add(old, scale(row, -old.get(pivot, Fraction(0)))) for old in self.rows]
        self.rows.append(row)
        self.rows.sort(key=lambda item: key_order(min(item, key=key_order)))
        return True

    def coordinates(self, poly):
        coordinates, residual = self.reduce(poly)
        if residual:
            raise ValueError('observable outside certified space')
        return coordinates
