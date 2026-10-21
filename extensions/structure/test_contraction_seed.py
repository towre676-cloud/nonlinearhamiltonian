"""Meaningful exact fixtures, coefficient-ring boundary and rejected false certificates."""
import copy
import random
import unittest
from contraction_seed import build, solve
from check_contraction import Matrix, eye, mul, same, unpack, verify


def model(n, d):
    return {'field': 'Q', 'dimensions': n, 'differentials': d}


class Certificates(unittest.TestCase):
    def test_triangle_gluing_and_obstruction(self):
        c = model([3, 3], [[[-1, 1, 0], [0, -1, 1], [1, 0, -1]]])
        cert = build(c)
        self.assertEqual(cert['cohomology_dimensions'], [1, 1])
        answer = solve(c, cert, 1, [1, 2, -3])
        self.assertEqual(answer['status'], 'solved')
        self.assertTrue(same(mul(Matrix(3, 3, c['differentials'][0]), unpack(answer['primitive'])),
                             Matrix(3, 1, [[1], [2], [-3]])))
        no = solve(c, cert, 1, [1, 2, -2])
        self.assertEqual(no['status'], 'obstructed')
        self.assertEqual(mul(unpack(no['separating_functional']), Matrix(3, 3, c['differentials'][0])).a,
                         [[0, 0, 0]])
        self.assertNotEqual(unpack(no['nonzero_pairing']).a[0][0], 0)

    def test_parameter_jump_and_torsion_boundary(self):
        self.assertEqual(build(model([1, 1], [[[1]]]))['cohomology_dimensions'], [0, 0])
        self.assertEqual(build(model([1, 1], [[[0]]]))['cohomology_dimensions'], [1, 1])
        # The same integer matrix has integral H^1 = Z/2; Q-acyclic is deliberately narrower.
        c = model([1, 1], [[[2]]])
        self.assertEqual(verify(c, build(c))['field'], 'Q')
        self.assertEqual(build(c)['cohomology_dimensions'], [0, 0])
        c['field'] = 'Z'
        with self.assertRaises(ValueError):
            build(c)

    def test_invalid_complex_noncycle_and_forgery(self):
        with self.assertRaises(ValueError):
            build(model([1, 1, 1], [[[1]], [[1]]]))
        c = model([1, 2, 1], [[[1], [0]], [[0, 1]]])
        cert = build(c)
        self.assertEqual(solve(c, cert, 1, [1, 1])['status'], 'not_cocycle')
        forged = copy.deepcopy(cert)
        forged['h'][1]['entries'][0][0] = '17'
        with self.assertRaises(ValueError):
            verify(c, forged)
        with self.assertRaises(ValueError):
            solve(c, cert, 1, '11')

    def test_empty_degrees_and_exact_rationals(self):
        c = model([0, 2, 1, 0], [[[], []], [['1/3', '-2/5']], []])
        self.assertEqual(build(c)['cohomology_dimensions'], [0, 1, 0, 0])
        self.assertEqual(solve(c, build(c), 1, ['6/5', 1])['status'], 'obstructed')

    def test_zero_laplacian_does_not_erase_a_class(self):
        c = model([3, 3], [[[-1, 1, 0], [0, -1, 1], [1, 0, -1]]])
        d = Matrix(3, 3, c['differentials'][0])
        transpose = Matrix(3, 3, [[d.a[j][i] for j in range(3)] for i in range(3)])
        harmonic = Matrix(3, 1, [[1], [1], [1]])
        self.assertEqual(mul(mul(d, transpose), harmonic).a, [[0], [0], [0]])
        self.assertEqual(solve(c, build(c), 1, [1, 1, 1])['status'], 'obstructed')

    def test_generated_exact_two_step_complexes(self):
        rng = random.Random(731)
        # Columns all lie in ker[0,0,1]; independent fixed cohomology/rank expectations.
        for _ in range(40):
            a, b = rng.randint(1, 9), rng.randint(-9, 9)
            c = model([1, 3, 1], [[[a], [b], [0]], [[0, 0, 1]]])
            cert = build(c)
            self.assertEqual(cert['cohomology_dimensions'], [0, 1, 0])
            self.assertEqual(verify(c, cert)['status'], 'passed')


if __name__ == '__main__':
    unittest.main()
