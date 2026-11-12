#!/usr/bin/env python3
"""Compare the coefficient-model rows with the stored elimination inputs."""
import json
import sys

from generate_tail_elimination import NV, expression
from generate_tail_degree_factors import INPUTS, checker


def mul(*ps):
    result = checker.const(1, NV)
    for p in ps:
        result = checker.pmul(result, p)
    return result


def form(a, b, x="g 0", y="g 1"):
    return f"({expression(a)}) * ({x}) + ({expression(b)}) * ({y})"


def row(order, t):
    out = []
    for i in (1, 3, 4, 5, 6):
        j = t + order - i
        if j < 0:
            continue
        coefficient = checker.mono_poly(order, 6 - i, i, j, NV)
        if i != 1:
            coefficient = mul(checker.var(i - 2, NV), coefficient)
        if coefficient:
            out.append((j, coefficient))
    return sorted(out)


def raw(order, t):
    return " + ".join(f"({expression(c)}) * g {j}" for j, c in row(order, t))


def generate(cert, raw_only):
    coefficients = {
        0: (checker.const(1, NV), checker.const(0, NV), checker.const(1, NV)),
        1: (checker.const(0, NV), checker.const(1, NV), checker.const(1, NV)),
    }
    if not raw_only:
        print("import SexticC3.TailScales")
    print("import SexticC3.TailRows")
    print("namespace SexticC3.StaticTail")
    if raw_only:
        print("set_option linter.unusedTactic false")
    else:
        print("open SexticC3.TailDegreeFactors")
    print("variable {K : Type*} [Field K]" + ("" if raw_only else " [CharZero K]"))
    print()
    for order, count in ((3, 8), (5, 6)):
        for t in range(count):
            j = t + order - 1
            u = f"n - {j} + 2" if order == 3 else f"n - {j}"
            print(f"{'' if raw_only else 'private '}theorem raw{order}_{t} (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)")
            print(f"    (h : rowValue a b c d n ⟨false, {order}, {t}, {u}⟩ g = 0) :")
            print(f"    (let z : K := n; {raw(order, t)}) = 0 := by")
            print(f"  have he := rowValue_top_split a b c d n {j} {order} g (by omega) (by omega) (by omega)")
            print(f"  have hv : 5 + (n - {j}) - {order} = {u} := by omega")
            print("  dsimp only at he")
            print("  norm_num at he")
            if order == 5:
                print("  rw [h] at he")
            else:
                print("  rw [hv, h] at he")
            casts = ", ".join(f"Nat.cast_sub (show {i} ≤ n by omega)" for i in range(1, j + 1))
            print(f"  norm_num [List.range_succ, staticColumn, monomialRow, weight, intCast_falling, fallingPoly, {casts}] at he")
            print("  simp (discharger := omega) only [if_pos, if_neg] at he")
            print(f"  norm_num [weight, List.range_succ, intCast_falling, fallingPoly, {casts}] at he")
            if order == 5:
                print("  norm_num [show Nat.choose 5 2 = 10 by decide, show Nat.choose 5 3 = 10 by decide] at he")
            print("  dsimp only")
            print("  linear_combination he")
            print()
    if raw_only:
        print("end SexticC3.StaticTail")
        return
    rows = [
        tuple(checker.parse(item[key], NV) for key in ("A", "B", "scale"))
        for item in cert["rows"]
    ]
    print("set_option maxHeartbeats 10000000 in")
    print("theorem stored_rows (n : ℕ) (hn : 17 ≤ n) (a b c d : K) (g : ℕ → K)")
    print("    (h : ∀ k u v, (k = 3 ∨ k = 5) → rowValue a b c d n ⟨false, k, u, v⟩ g = 0) :")
    print("    (let z : K := n;")
    print("      " + " ∧\n      ".join(f"({form(a,b)}) = 0" for a,b,_ in rows) + ") := by")
    print("  let z : K := n")
    print("  have e0 : g 0 - (1 * g 0 + 0 * g 1) = 0 := by ring")
    print("  have e1 : g 1 - (0 * g 0 + 1 * g 1) = 0 := by ring")
    for t in range(8):
        j = t + 2
        terms = row(3, t)
        assert terms[-1][0] == j
        previous = terms[:-1]
        denominator = mul(*(coefficients[i][2] for i, _ in previous))
        lhs = mul(denominator, terms[-1][1])
        basis = [checker.const(0, NV), checker.const(0, NV)]
        multipliers = []
        for idx, (i, c) in enumerate(previous):
            m = mul(c, *(coefficients[k][2] for k, _ in previous[:idx] + previous[idx+1:]))
            multipliers.append((i, m))
            for axis in (0, 1):
                basis[axis] = checker.padd(basis[axis], checker.psc(mul(m, coefficients[i][axis]), -1))
        coefficients[j] = (*basis, lhs)
        print(f"  have e{j} : ({expression(lhs)}) * g {j} - ({form(*basis)}) = 0 := by")
        print(f"    have hr := raw3_{t} n hn a b c d g (h 3 {t} (n - {j} + 2) (Or.inl rfl))")
        combo = "".join(f" - ({expression(m)}) * e{i}" for i, m in multipliers)
        print(f"    linear_combination ({expression(denominator)}) * hr{combo}")
    for t, (a, b, scale) in enumerate(rows):
        j = t + 4
        terms = row(5, t)
        denom = mul(*(coefficients[i][2] for i, _ in terms))
        comp = []
        for idx, (i, c) in enumerate(terms):
            others = terms[:idx] + terms[idx+1:]
            comp.append((i, mul(c, *(coefficients[k][2] for k, _ in others))))
        print(f"  have f{t} : ({form(a,b)}) = 0 := by")
        print(f"    apply (mul_eq_zero.mp ?_).resolve_left (TailScales.rowScale{t} n hn)")
        print(f"    show ({expression(scale)}) * ({form(a,b)}) = 0")
        print(f"    have hr := raw5_{t} n hn a b c d g (h 5 {t} (n - {j} + 0) (Or.inr rfl))")
        combo = "".join(f" - ({expression(m)}) * e{i}" for i, m in comp)
        print(f"    linear_combination ({expression(denom)}) * hr{combo}")
    print("  exact ⟨f0, f1, f2, f3, f4, f5⟩")
    print("end SexticC3.StaticTail")


if __name__ == "__main__":
    generate(json.loads((INPUTS / "binary_static_d6.json").read_bytes()), sys.argv[1:] == ["--raw"])
