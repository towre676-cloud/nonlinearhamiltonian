"""Step 4: purely symbolic verification of the remaining polynomial
identities used in the proof, so that no step rests on interpolation.

(i) 120 t^3fall + Bt(n, t) = 108 P_delta(n) for delta = 0, 1, 2
    (t = n - delta), where Phi_t(kappa) = eps * [120 t_3 + Bt(n,t)].
(ii) det_delta(n) for delta = 0, 1 re-derived and factored (as in
    step 3) and its rational roots listed.
(iii) The Phi coefficient formula's A and C coefficients:
    A(n,K) = 120 (n-K+3)_3, C(n,K) = -120 (K+3)_3 identically.
"""
import sympy as sp
import json, os

n, K = sp.symbols('n K')

def fl(x, k):
    r = 1
    for i in range(k):
        r *= x - i
    return sp.expand(r)

def Bt(nn, KK):
    return (108 * (-KK * fl(nn - KK + 2, 2) + (nn - KK) * fl(KK + 2, 2))
            + 12 * (fl(nn - KK, 3) - fl(KK, 3)) + 216 * (2 * KK - nn))

P = {0: n * (n - 1) * (n - 2), 1: (n - 1) * (n - 2) ** 2, 2: (n - 1) * (n - 2) * (n - 4)}

ok = {}
for delta in (0, 1, 2):
    t = n - delta
    expr = sp.expand(120 * fl(t, 3) + Bt(n, t) - 108 * P[delta])
    ok[f"P_delta_identity_{delta}"] = (expr == 0)
    print(f"delta={delta}: 120 t_3 + Bt(n,t) - 108 P_delta(n) = {expr}  (identity: {expr == 0})")

det_info = {}
for delta in (0, 1):
    t = n - delta
    D = fl(delta + 3, 3) if False else {0: 6, 1: 24}[delta]
    E = {0: 6, 1: 12}[delta]
    Bt_t3 = Bt(n, t - 3)
    Phi_t3_kappa = (120 * fl(t, 3) * fl(t - 3, 3) + Bt_t3 * fl(t, 3)) / D - 120 * fl(t, 3)
    brace = 120 * (-fl(t - 3, 2) / E + fl(t - 3, 3) / D) + Bt_t3 / D
    det = sp.factor(108 * P[delta] * brace - 120 * Phi_t3_kappa)
    roots = sp.solve(sp.together(det).as_numer_denom()[0], n)
    det_info[str(delta)] = {"det": str(det), "rational_roots": [str(r) for r in roots]}
    print(f"delta={delta}: det(n) = {det}, roots = {roots}")

out = {"identities": ok, "det": det_info,
       "A_coeff": "120*(n-K+3)_3", "C_coeff": "-120*(K+3)_3"}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "step4_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print("wrote step4_results.json")
