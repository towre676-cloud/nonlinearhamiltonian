"""Step 1: kernel dimensions of single gates at a = +-2, and exact
verification of the star-product identities

  T_1(F^2, G) = 2 F T_1(F, G)
  T_3(F^2, G) = 6 T_2(F, T_1(F,G)) + 2 F T_3(F,G) + 216 eps * Chat(G)
  T_5(F^2, G) = 20 T_2(F, T_3(F,G))

for F = q^3 + eps p^3, eps = +-1, Chat = q d/dq - p d/dp (charge op).
"""
import sys, json, random
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sextic_lib.py lives in this directory
import sextic_lib as S
from fractions import Fraction

random.seed(12345)

def H_of(eps):
    F = S.add(S.mono(3, 0), S.scale(S.mono(0, 3), eps))
    return F, S.mul(F, F)

def charge_op(G):
    return S.clean({(c, e): v * (c - e) for (c, e), v in G.items()})

def rand_G(n, bound=5):
    G = {}
    for c in range(n + 1):
        v = Fraction(random.randint(-bound, bound), random.choice([1, 1, 2, 3]))
        if v:
            G[(c, n - c)] = v
    return G

def gate_rows(H, n, ks):
    mons = S.homogeneous_mons(n)
    rows = []
    for k in ks:
        cols = [S.transvectant(H, S.mono(c, e), k) for (c, e) in mons]
        keys = sorted({key for col in cols for key in col})
        for key in keys:
            rows.append([col.get(key, Fraction(0)) for col in cols])
    return mons, rows

def dim_ker(H, n, ks):
    mons, rows = gate_rows(H, n, ks)
    return len(mons) - S.rank_of(rows)

out = {"dims": {}, "identity_checks": {}}
for eps in (1, -1):
    F, H = H_of(eps)
    assert H == S.add(S.mono(6, 0), S.scale(S.mono(3, 3), 2 * eps), S.mono(0, 6)), H
    dims = {}
    for n in range(0, 41):
        dims[n] = {
            "kerT3": dim_ker(H, n, (3,)),
            "kerT5": dim_ker(H, n, (5,)),
            "E": dim_ker(H, n, (3, 5)),
        }
    out["dims"][str(eps)] = dims
    # identity checks on random G
    checks = {"T1": True, "T3": True, "T5": True, "trials": 0}
    for n in list(range(0, 21)) + [25, 30, 37]:
        for _ in range(4):
            G = rand_G(n)
            if not G:
                continue
            checks["trials"] += 1
            if S.transvectant(H, G, 1) != S.scale(S.mul(F, S.transvectant(F, G, 1)), 2):
                checks["T1"] = False
            lhs3 = S.transvectant(H, G, 3)
            rhs3 = S.add(
                S.scale(S.transvectant(F, S.transvectant(F, G, 1), 2), 6),
                S.scale(S.mul(F, S.transvectant(F, G, 3)), 2),
                S.scale(charge_op(G), 216 * eps))
            if lhs3 != rhs3:
                checks["T3"] = False
            lhs5 = S.transvectant(H, G, 5)
            rhs5 = S.scale(S.transvectant(F, S.transvectant(F, G, 3), 2), 20)
            if lhs5 != rhs5:
                checks["T5"] = False
    out["identity_checks"][str(eps)] = checks
    print(f"eps={eps}: identities {checks}")
    print(" n: kerT3 kerT5 E")
    for n in range(0, 41):
        d = dims[n]
        print(f"  {n:2d}: {d['kerT3']:3d} {d['kerT5']:3d} {d['E']:3d}")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "step1_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print("wrote step1_results.json")
