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


class CoreClosure(unittest.TestCase):
    def test_euler_cramer_identity(self):
        c = S.Symbol("c")
        s = S.Function("s")(q, P)
        for h, (wq, wP), d in ((P**3 + c*q**5, (3, 5), 15), (P**3 + c*q**3*P, (2, 3), 9), (P**3 + c*q**4, (3, 4), 12)):
            bracket = S.diff(h, q)*S.diff(s, P) - S.diff(h, P)*S.diff(s, q)
            euler = wq*q*S.diff(s, q) + wP*P*S.diff(s, P)
            self.assertEqual(S.expand(wq*q*bracket - (d*h*S.diff(s, P) - euler*S.diff(h, P))), 0)
            self.assertNotEqual(S.resultant(h, S.diff(h, P), P), 0)

    def test_adversarial_loci_have_two_dimensional_core(self):
        for b, c in (((1, -2, 3, 5), (0, 2, 1, -1, 4, -3)),      # 3 b3 + 5 c5 = 0
                     ((2, 1, -9, 0), (0, 1, -2, 3, 5, 0)),       # 5 b2 + 9 c4 = 0
                     ((1, 3, -4, 0), (0, 2, 1, -3, 2, 0))):      # E = 0
            self.assertEqual(M.window_dimensions(M.reduced_hamiltonian(b, c), 12, (5,)), [2])

    def test_first_refinement_partner(self):
        gam, b0 = S.symbols("gamma b0")
        B, C = b0 + q**2, eps*q + lam*q**2 + gam*q**3
        D, T3, T5 = M.chart_operators(B, C)
        J = 3*P**2 + 2*q**2 + (2 - 6*lam)*P
        self.assertEqual((T3(J), T5(J), T5(D(J))), (0, 0, 0))
        self.assertEqual(S.expand(T3(D(J)) + 1296*gam*q), 0)
        self.assertEqual(M.window_dimensions(M.reduced_hamiltonian((2, 0, 1, 0), (0, 3, 5, 0, 0, 0)), 12, (1, 2)), [4, 2])
        self.assertEqual(M.window_dimensions(M.reduced_hamiltonian((2, 0, 1, 0), (0, 3, 5, 7, 0, 0)), 12, (1, 2)), [3, 2])


class Refinement(unittest.TestCase):
    def setUp(self):
        self.bs, self.cs = S.symbols("b0:4"), S.symbols("c0:6")
        self.B = sum(self.bs[i]*q**i for i in range(4))
        self.C = sum(self.cs[i]*q**i for i in range(6))

    def test_universal_partner_identities(self):
        D, T3, T5 = M.chart_operators(self.B, self.C)
        a = S.Symbol("alpha")
        self.assertEqual(S.expand(T3(D(q)) - 36*self.bs[3]), 0)
        self.assertEqual(S.expand(T3(D(P + a*q)) - (36*a*self.bs[3] - 72*self.bs[2] - 144*self.cs[4]
                                                   - (216*self.bs[3] + 720*self.cs[5])*q)), 0)
        self.assertEqual((T5(D(q)), T5(D(P + a*q))), (0, 0))

    def test_quadratic_partner_on_case_two_locus(self):
        b0, b1, b2, b3 = self.bs
        c = self.cs
        z = {c[5]: 0, c[4]: S.Rational(5, 4)*b3**2}
        D, T3, T5 = M.chart_operators(self.B.subs(z), self.C.subs(z))
        J2 = (54*b3**2*P**2 + (168*b2*b3**2 + 245*b3**4 - 36*b3**3*q - 108*b3*c[3])*P + 36*b3**3*q**3
              + (36*b2*b3**2 + 15*b3**4)*q**2
              + (-216*b1*b3**2 + 264*b2**2*b3 + 1270*b2*b3**3 - 216*b2*c[3] + 1225*b3**5
                 - 756*b3**2*c[3] + 216*b3*c[2])*q)
        self.assertEqual((T3(J2), T5(J2), T3(D(J2)), T5(D(J2))), (0, 0, 0, 0))

    def test_jump_loci_at_rational_members(self):
        for b, c, expected in (((2, -1, 3, 2), (0, 1, -2, 4, 3, 5), [2, 2]),
                               ((2, -1, 3, 0), (0, 1, -2, 4, 3, 5), [3, 2]),
                               ((2, -1, 3, 10), (0, 1, -2, 4, 3, -3), [3, 2]),
                               ((2, -1, 3, 2), (0, 1, -2, 4, 5, 0), [3, 2]),
                               ((2, -1, 3, 2), (0, 1, -2, 4, 3, 0), [2, 2]),
                               ((2, -1, -6, 0), (0, 1, -2, 4, 3, 0), [4, 2]),
                               ((2, -1, 3, 0), (0, 1, -2, 4, 3, 0), [3, 2])):
            self.assertEqual(M.window_dimensions(M.reduced_hamiltonian(b, c), 12, (1, 2)), expected)


if __name__ == "__main__":
    unittest.main()
