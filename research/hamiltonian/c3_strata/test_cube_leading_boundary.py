import unittest

import sympy as S

import cube_leading_boundary as M

q, P, p, mu, lam, eps = M.q, M.P, M.p, M.mu, M.lam, M.eps


class Transport(unittest.TestCase):
    def test_chart_operators_are_the_flat_transvectants(self):
        B = 2 - q + 3*q**2 + 5*q**3
        C = 1 + 4*q - 2*q**2 + 7*q**3 + 3*q**4 - 6*q**5
        D, T3, T5 = M.chart_operators(B, C)
        H = S.expand((P**3 + B*P + C).subs(P, p + q**2))
        for G in (q**3*P**2, q*P**5, P**6 + q**4*P, q**5):
            flat = S.expand(G.subs(P, p + q**2))
            for order, op in ((1, D), (3, T3), (5, T5)):
                self.assertEqual(S.expand(M.flat_transvectant(H, flat, order) - op(G).subs(P, p + q**2)), 0)

    def test_gate_symbol_on_functions_of_P(self):
        B, C = q + 2*q**2, 3*q**3 - q**4
        _, T3, T5 = M.chart_operators(B, C)
        E = M.gate_symbol(B, C)
        self.assertEqual(S.expand(E - (4 + 0*q)), 0)
        for m in range(3, 9):
            self.assertEqual(S.expand(T3(P**m) - 6*E*S.diff(P**m, P, 3)), 0)
            self.assertEqual(T5(P**m), 0)


class StaticSector(unittest.TestCase):
    def test_dimension_law(self):
        self.assertEqual(M.window_dimensions(M.reduced_hamiltonian((0, 0, 0, 10), (0, 0, 0, 0, 0, -6)), 12, (0,)), [15])
        self.assertEqual(M.window_dimensions(M.reduced_hamiltonian((0, 0, 0, 10), (0, 0, 0, 0, 0, -9)), 12, (0,)), [14])
        h = M.reduced_hamiltonian((2, -1, 3, 5), (1, 4, -2, 7, 3, -6))
        self.assertEqual(M.window_dimensions(h, 9, (0,)), [13])
        self.assertEqual(M.window_dimensions(h, 10, (0,)), [14])

    def test_vanishing_symbol_gives_all_powers_of_P(self):
        _, T3, T5 = M.chart_operators(q + 2*q**2, 5*q**2 - q**3 - q**4)
        for m in range(12):
            self.assertEqual((T3(P**m), T5(P**m)), (0, 0))


class CoupledFamily(unittest.TestCase):
    def setUp(self):
        self.B, self.C = mu*q, eps*q + lam*q**2
        self.D, self.T3, self.T5 = M.chart_operators(self.B, self.C)

    def test_static_basis(self):
        basis = M.static_basis()
        self.assertEqual(len(basis), 15)
        self.assertTrue(all(self.T3(g) == 0 and self.T5(g) == 0 for g in basis))
        self.assertEqual(len({S.Poly(g, P, q).monoms()[0] for g in basis}), 15)

    def test_exact_obstructions(self):
        d2q = self.D(self.D(q))
        d3P = self.D(self.D(self.D(P)))
        self.assertEqual(self.T3(d2q), 432*lam)
        self.assertEqual(self.T3(d3P), 864*lam**2)
        self.assertEqual(self.T3(self.D(q)), 0)
        self.assertEqual(self.T3(self.D(self.D(P))), 0)

    def test_chain_at_a_rational_point(self):
        h = M.reduced_hamiltonian((0, 2, 0, 0), (0, 3, 5, 0, 0, 0))
        self.assertEqual(M.window_dimensions(h, 12, (0, 1, 2, 3, 4)), [15, 4, 3, 2, 2])


class ExistingFamilyOverlap(unittest.TestCase):
    def test_quadratic_cubic_phase_has_two_dimensional_core(self):
        # P^3 + q P^2 depresses to Y^3 - (q^2/3)Y + 2q^3/27.
        # This refutes the original novelty argument's premise that every
        # F(P)+qG(P) has core dimension at least five.
        h = M.reduced_hamiltonian((0, 0, -S.Rational(1, 3), 0),
                                  (0, 0, 0, S.Rational(2, 27), 0, 0))
        self.assertEqual(M.window_dimensions(h, 12, (0, 1, 2, 3)), [15, 3, 2, 2])


if __name__ == "__main__":
    unittest.main()
