"""Step 2: explicit chain decomposition at a = eps*2.

Chain r = indices c = r (mod 3) in the monomial basis q^c p^(n-c).

Operators in coefficient form (derived by hand; cross-checked against
sextic_lib's transvectant):
  Dtilde = T_3(F,.)/6 : (Dg)_C = (n-C)_3 g_C - eps (C+3)_3 g_{C+3},  C in [0, n-3]
  L      = T_2(F,.)/6 : (Ly)_C = (m-C+1)_2 y_{C-1} + eps (C+2)_2 y_{C+2},
                        C in [0, m-1], Y in V_m
  Phi    = T_3(F^2, .) via the verified identity
           6 T_2(F, T_1(F,G)) + 2 F T_3(F,G) + 216 eps Chat(G)
           (applied through sextic_lib operators for extraction).

ker L on V_m (m >= 2): chain 2 always killed by the C=0 equation;
chain r in {0,1} survives iff no right singleton: r=0 iff m%3 != 2,
r=1 iff m%3 != 0.  Surviving chain basis: y_r = 1 at the bottom and
  y_{c+3} = -eps y_c (m-c)_2/(c+3)_2.
ker Dtilde per chain: 1-dim, g_{c+3} = eps g_c (n-c)_3/(c+3)_3.

W_n basis per chain r: kappa^(r) (ker Dtilde, top coeff 1) and, when
chain r of V_{n-3} survives in ker L, pi^(r) with Dtilde pi = Y^(r)
(Y^(r) normalised to top coeff 1, pi top coeff 0).
"""
import sys, json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sextic_lib.py lives in this directory
import sextic_lib as S
from fractions import Fraction

def fall(x, k):
    r = 1
    for i in range(k):
        r *= x - i
    return r

def chain_indices(r, n):
    return list(range(r, n + 1, 3))

def kerL_survives(r, m):
    if m < 2:
        return r <= m  # L = 0 on V_0, V_1: every chain present survives
    if r == 2:
        return False
    if r == 0:
        return m % 3 != 2
    if r == 1:
        return m % 3 != 0
    return False

def kerL_basis(r, m, eps):
    """Dict {c: y_c} on chain r of V_m, normalised y_r = 1 (bottom)."""
    idx = chain_indices(r, m)
    y = {idx[0]: Fraction(1)}
    for c in idx[:-1]:
        y[c + 3] = -eps * y[c] * Fraction(fall(m - c, 2), fall(c + 3, 2))
    return y

def kerDtilde_basis(r, n, eps):
    """Dict {c: g_c} on chain r of V_n with Dtilde g = 0, top coeff 1."""
    idx = chain_indices(r, n)
    g = {idx[-1]: Fraction(1)}
    for c in reversed(idx[:-1]):
        # (n-c)_3 g_c = eps (c+3)_3 g_{c+3}
        g[c] = eps * Fraction(fall(c + 3, 3), fall(n - c, 3)) * g[c + 3]
    return g

def Dtilde_apply(g, n, eps):
    out = {}
    for C in range(0, n - 2):
        v = fall(n - C, 3) * g.get(C, Fraction(0)) - eps * fall(C + 3, 3) * g.get(C + 3, Fraction(0))
        if v:
            out[C] = v
    return out

def preimage_of_Y(r, n, eps, Ytop):
    """Solve Dtilde pi = Y on chain r of V_n, pi_top = 0, where Y is a
    dict on chain r of V_{n-3} normalised with top coefficient Ytop."""
    idx = chain_indices(r, n)          # unknowns, top = idx[-1]
    eqs = chain_indices(r, n - 3)      # equation indices C
    pi = {idx[-1]: Fraction(0)}
    for C in reversed(eqs):
        # (n-C)_3 pi_C - eps (C+3)_3 pi_{C+3} = Y_C
        pi[C] = (Ytop.get(C, Fraction(0)) + eps * fall(C + 3, 3) * pi.get(C + 3, Fraction(0))) / fall(n - C, 3)
    return pi

def coeffs_to_poly(gdict, n):
    return S.clean({(c, n - c): v for c, v in gdict.items() if v})

def top_normalised_kerL(r, m, eps):
    """ker L basis on chain r of V_m normalised to TOP coefficient 1."""
    y = kerL_basis(r, m, eps)
    idx = chain_indices(r, m)
    top = y[idx[-1]]
    return {c: v / top for c, v in y.items()}

def W_chain_basis(r, n, eps):
    """Basis of W_n^(r) = {g on chain r : T_5(F^2, g) = 0} as coeff dicts.
    Returns list of (name, dict)."""
    basis = [("kappa", kerDtilde_basis(r, n, eps))]
    m = n - 3
    if kerL_survives(r, m):
        Y = top_normalised_kerL(r, m, eps)
        pi = preimage_of_Y(r, n, eps, Y)
        basis.append(("pi", pi))
    return basis

def Phi(G, F, eps):
    return S.add(
        S.scale(S.transvectant(F, S.transvectant(F, G, 1), 2), 6),
        S.scale(S.mul(F, S.transvectant(F, G, 3)), 2),
        S.scale(S.clean({(c, e): v * (c - e) for (c, e), v in G.items()}), 216 * eps))

results = {"checks": [], "top_values": {}}
for eps in (1, -1):
    F = S.add(S.mono(3, 0), S.scale(S.mono(0, 3), eps))
    H = S.mul(F, F)
    ok = True
    for n in range(5, 64):
        total = 0
        for r in range(3):
            if r > n:
                continue
            basis = W_chain_basis(r, n, eps)
            total += len(basis)
            polys = [coeffs_to_poly(g, n) for _, g in basis]
            # each basis element must lie in ker T_5(H, .)
            for P in polys:
                if S.transvectant(H, P, 5) != {}:
                    ok = False
                    print(f"FAIL eps={eps} n={n} r={r}: basis element not in ker T5")
            # independence across the whole W_n: stack coefficient vectors
            vecs = []
            for P in polys:
                vecs.append([P.get((c, n - c), Fraction(0)) for c in range(n + 1)])
            if vecs and S.rank_of(vecs) != len(vecs):
                ok = False
                print(f"FAIL eps={eps} n={n} r={r}: basis not independent")
        # total dimension must equal dim ker T_5
        mons, rows = None, None
        mons = S.homogeneous_mons(n)
        rows = []
        cols = [S.transvectant(H, S.mono(c, e), 5) for (c, e) in mons]
        keys = sorted({k for col in cols for k in col})
        for key in keys:
            rows.append([col.get(key, Fraction(0)) for col in cols])
        dimker = len(mons) - S.rank_of(rows)
        if dimker != total:
            ok = False
            print(f"FAIL eps={eps} n={n}: sum of chain basis dims {total} != dim kerT5 {dimker}")
    results["checks"].append({"eps": eps, "W_basis_verified_up_to_63": ok})
    print(f"eps={eps}: W_n chain basis verified for n=5..63: {ok}")

    # Extract top output coefficients of Phi (= T_3(H,.)) on each chain basis
    tv = {}
    for n in range(15, 64):
        for r in range(3):
            basis = W_chain_basis(r, n, eps)
            idx = chain_indices(r, n)
            t = idx[-1]
            rows_out = {}
            for name, g in basis:
                P = coeffs_to_poly(g, n)
                out = Phi(P, F, eps)
                rows_out[name] = {
                    "Phi_t": str(out.get((t, n - t), Fraction(0))),
                    "Phi_t-3": str(out.get((t - 3, n - t + 3), Fraction(0))) if t >= 3 else None,
                    "Phi_t-6": str(out.get((t - 6, n - t + 6), Fraction(0))) if t >= 6 else None,
                    "allzero": out == {},
                }
            tv[f"n={n},r={r}"] = rows_out
    results["top_values"][str(eps)] = tv

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "step2_results.json"), "w") as f:
    json.dump(results, f, indent=1)
print("wrote step2_results.json")
