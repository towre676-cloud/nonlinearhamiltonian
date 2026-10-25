"""Step 3: symbolic closed forms.

(a) Verify the coefficient formula for Phi_K = (T_3(F^2,.))_K:
    Phi_K = 120 (n-K+3)_3 g_{K-3} + eps Bt(n,K) g_K - 120 (K+3)_3 g_{K+3},
    Bt(n,K) = 108[-K(n-K+2)_2 + (n-K)(K+2)_2] + 12[(n-K)_3 - K_3] + 216(2K-n)
against sextic_lib on random G.

(b) Closed forms at the chain top (t = n - delta, delta = (n-r) mod 3):
    Phi_t(kappa) = 108 eps P_delta(n),
      P_0 = n(n-1)(n-2), P_1 = (n-1)(n-2)^2, P_2 = (n-1)(n-2)(n-4);
    Phi_t(pi) = 120.
    Verify against step2_results.json for all n = 15..63.

(c) For the 2-dimensional chains (delta in {0,1} only) compute
    det(n) = Phi_t(kappa) Phi_{t-3}(pi) - Phi_t(pi) Phi_{t-3}(kappa)
    symbolically, factor it, and verify against step2_results.json.
"""
import sys, json, random
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sextic_lib.py lives in this directory
import sextic_lib as S
from fractions import Fraction
import sympy as sp

random.seed(999)

def fall(x, k):
    r = 1
    for i in range(k):
        r *= x - i
    return r

def Bt(n, K):
    return (108 * (-K * fall(n - K + 2, 2) + (n - K) * fall(K + 2, 2))
            + 12 * (fall(n - K, 3) - fall(K, 3)) + 216 * (2 * K - n))

def Phi_formula(G, n, eps):
    g = {c: G.get((c, n - c), Fraction(0)) for c in range(n + 1)}
    out = {}
    for K in range(n + 1):
        v = (120 * fall(n - K + 3, 3) * g.get(K - 3, Fraction(0))
             + eps * Bt(n, K) * g[K]
             - 120 * fall(K + 3, 3) * g.get(K + 3, Fraction(0)))
        if v:
            out[(K, n - K)] = v
    return out

# (a)
ok_a = True
for eps in (1, -1):
    F = S.add(S.mono(3, 0), S.scale(S.mono(0, 3), eps))
    H = S.mul(F, F)
    for n in range(0, 26):
        for _ in range(3):
            G = {}
            for c in range(n + 1):
                v = Fraction(random.randint(-4, 4), random.choice([1, 2]))
                if v:
                    G[(c, n - c)] = v
            if S.transvectant(H, G, 3) != Phi_formula(G, n, eps):
                ok_a = False
                print(f"FAIL formula eps={eps} n={n}")
print("(a) Phi coefficient formula verified:", ok_a)

# (b) + (c) numeric comparison with step 2 data, then symbolic det
n = sp.symbols('n', integer=True, positive=True)

def Bt_sym(nn, K):
    def fl(x, k):
        r = 1
        for i in range(k):
            r *= x - i
        return sp.expand(r)
    return (108 * (-K * fl(nn - K + 2, 2) + (nn - K) * fl(K + 2, 2))
            + 12 * (fl(nn - K, 3) - fl(K, 3)) + 216 * (2 * K - nn))

P = {0: n * (n - 1) * (n - 2), 1: (n - 1) * (n - 2) ** 2, 2: (n - 1) * (n - 2) * (n - 4)}

def fl2(x, k):
    r = 1
    for i in range(k):
        r *= x - i
    return sp.expand(r)

det_sym = {}
for delta in (0, 1):
    t = n - delta
    D = fall(delta + 3, 3)
    E = fall(delta + 3, 2)
    Bt_t3 = Bt_sym(n, t - 3)
    Phi_t3_kappa = (120 * fl2(t, 3) * fl2(t - 3, 3) + Bt_t3 * fl2(t, 3)) / D - 120 * fl2(t, 3)
    Phi_t3_pi_brace = 120 * (-fl2(t - 3, 2) / E + fl2(t - 3, 3) / D) + Bt_t3 / D
    det = 108 * P[delta] * Phi_t3_pi_brace - 120 * Phi_t3_kappa
    det_sym[delta] = sp.factor(sp.together(det))
    print(f"delta={delta}: det(n) = {sp.factor(sp.together(det).as_numer_denom()[0])} / {sp.together(det).as_numer_denom()[1]}")

d2 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "step2_results.json")))
tv = d2["top_values"]
ok_b = True
ok_c = True
det_numeric = {}
for eps in (1, -1):
    for key, rows in tv[str(eps)].items():
        nn = int(key.split(',')[0][2:]); r = int(key.split(',')[1][2:])
        delta = (nn - r) % 3
        t = nn - delta
        # (b): Phi_t(kappa) closed form
        pred = 108 * eps * int(P[delta].subs(n, nn))
        got = int(Fraction(rows['kappa']['Phi_t']))
        if pred != got:
            ok_b = False
            print(f"FAIL (b) eps={eps} {key}: pred {pred} got {got}")
        if 'pi' in rows:
            if int(Fraction(rows['pi']['Phi_t'])) != 120:
                ok_b = False
                print(f"FAIL (b) pi Phi_t eps={eps} {key}")
            a = Fraction(rows['kappa']['Phi_t']); b = Fraction(rows['pi']['Phi_t'])
            c = Fraction(rows['kappa']['Phi_t-3']); e = Fraction(rows['pi']['Phi_t-3'])
            detv = a * e - b * c
            det_numeric[(eps, nn, r)] = detv
            pred_det = sp.nsimplify(det_sym[delta].subs(n, nn), rational=True)
            if Fraction(pred_det.p, pred_det.q) != detv:
                ok_c = False
                print(f"FAIL (c) eps={eps} {key}: det pred {pred_det} got {detv}")
print("(b) top closed forms verified against step2 (n=15..63, both eps):", ok_b)
print("(c) determinant closed forms verified against step2 (all 2-dim chains):", ok_c)

out = {
    "phi_formula_verified": ok_a,
    "top_closed_forms_verified": ok_b,
    "det_closed_forms_verified": ok_c,
    "P_delta": {str(k): str(v) for k, v in P.items()},
    "det_delta_factored": {str(k): str(v) for k, v in det_sym.items()},
}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "step3_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print("wrote step3_results.json")
