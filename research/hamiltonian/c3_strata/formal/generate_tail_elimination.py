#!/usr/bin/env python3
"""Translate the sextic elimination tree into Lean field identities."""
from fractions import Fraction
from functools import reduce
import json
import sys
from math import gcd, lcm
from pathlib import Path

from generate_tail_degree_factors import INPUTS, checker, degree_factors

FORMAL = Path(__file__).resolve().parent
VARS = ("z", "a", "b", "c", "d")
NV = len(VARS)


def expression(poly, variables=VARS):
    terms = []
    for exponents, coef in sorted(poly.items()):
        parts = [v if e == 1 else f"{v}^{e}" for v, e in zip(variables, exponents) if e]
        magnitude = abs(coef)
        if magnitude != 1 or not parts:
            scalar = str(magnitude.numerator)
            if magnitude.denominator != 1:
                scalar = f"({scalar}/{magnitude.denominator})"
            parts.insert(0, scalar)
        terms.append((coef < 0, "*".join(parts)))
    if not terms:
        return "0"
    negative, term = terms[0]
    return ("-" if negative else "") + term + "".join(
        (" - " if negative else " + ") + term for negative, term in terms[1:]
    )


def primitive(poly):
    uni = checker.uni(poly)
    denominator = lcm(*(c.denominator for c in uni.values()))
    entries = [int(denominator * uni.get(i, 0)) for i in range(max(uni) + 1)]
    content = reduce(gcd, entries)
    if entries[-1] < 0:
        content = -content
    return tuple(c // content for c in entries), Fraction(content, denominator)


def horner(entries):
    value = str(entries[-1])
    for c in reversed(entries[:-1]):
        value = f"({c} + z * {value})"
    return value


def scalar_text(value):
    return expression(checker.const(value, NV))


class Generator:
    def __init__(self, factors):
        self.factor_index = {p: i for i, p in enumerate(factors)}
        self.lines = []
        self.identities = []
        self.degree_polys = {}

    def emit(self, indent, line):
        self.lines.append(" " * indent + line)

    def nonzero(self, poly):
        coefs, scale = primitive(poly)
        idx = self.factor_index[coefs]
        key = (idx, scale)
        if key not in self.identities:
            self.identities.append(key)
        self.degree_polys[key] = poly
        return f"degree_{self.identities.index(key)} n hn"

    def branches(self, steps, polys, names, indent):
        for step in steps:
            op = step["op"]
            if op == "derive":
                poly = checker.parse(step["poly"], NV)
                name = f"h{len(polys)}"
                combo = []
                for idx, multiplier in step["combo"]:
                    mult = expression(checker.parse(multiplier, NV))
                    combo.append(f"({mult}) * {names[idx]}")
                self.emit(indent, f"have {name} : ({expression(poly)} : K) = 0 := by")
                self.emit(indent + 2, "linear_combination " + " + ".join(combo))
                polys = [*polys, poly]
                names = [*names, name]
            elif op == "contradiction":
                idx = step["idx"]
                self.emit(indent, f"exact ({self.nonzero(polys[idx])} {names[idx]}).elim")
            elif op == "target":
                self.emit(indent, "refine ⟨?_, ?_, ?_⟩")
                for idx, scale, target in zip(step["idx"], step["const"], targets(), strict=True):
                    factor = checker.parse(scale, NV)
                    self.emit(indent, "· apply (mul_eq_zero.mp ?_).resolve_left (" + self.nonzero(factor) + ")")
                    self.emit(indent + 2, f"show ({expression(factor)}) * ({expression(target)}) = 0")
                    self.emit(indent + 2, f"linear_combination {names[idx]}")
            elif op == "split":
                idx = step["idx"]
                factor = checker.parse(step["const"], NV)
                factors = [(checker.parse(poly, NV), power) for poly, power in step["factors"]]
                product = " * ".join([f"({expression(factor)})"] + [
                    f"({expression(poly)})^{power}" for poly, power in factors
                ])
                self.emit(indent, f"have factored : {product} = 0 := by")
                self.emit(indent + 2, f"linear_combination {names[idx]}")
                self.emit(indent, "have branchZero := (mul_eq_zero.mp (by")
                self.emit(indent + 2, f"linear_combination factored : ({expression(factor)}) * (" +
                          " * ".join(f"({expression(poly)})^{power}" for poly, power in factors) + ") = 0)).resolve_left (" + self.nonzero(factor) + ")")
                self.emit(indent, "norm_num [mul_eq_zero, pow_eq_zero_iff'] at branchZero")
                zero_names = [f"h{len(polys)}_{i}" for i in range(len(factors))]
                if len(factors) > 1:
                    pattern = zero_names[0]
                    for h in zero_names[1:]:
                        pattern = f"({pattern} | {h})"
                    self.emit(indent, f"rcases branchZero with {pattern}")
                for k, (poly, _) in enumerate(factors):
                    if len(factors) > 1:
                        self.emit(indent, "·")
                    self.branches(step["branches"][k], [*polys, poly],
                                  [*names, zero_names[k] if len(factors) > 1 else "branchZero"],
                                  indent + (2 if len(factors) > 1 else 0))
            else:
                raise ValueError(op)


def targets():
    return [{(0, *es): c for es, c in p.items()} for p in checker.J_EXPECTED[6]]


def systems(cert):
    for s in cert["systems"]:
        case, chart = s["case"], s["chart"]
        polys = []
        for row in cert["rows"]:
            a, b = (checker.parse(row[key], NV) for key in ("A", "B"))
            p = {"A": a, "B": b, "one": checker.padd(a, b)}[case]
            if chart is not None:
                for i in range(1, chart + 1):
                    p = checker.subs_var(p, i, 0)
                p = checker.subs_var(p, chart + 1, 1)
            polys.append(p)
        yield s, polys


def main():
    cert = json.loads((INPUTS / "binary_static_d6.json").read_bytes())
    factors = degree_factors(cert)
    g = Generator(factors)
    mode = sys.argv[1:] or ["--all"]
    if mode not in (["--all"], ["--scales"], ["--axes"], ["--mixed"]):
        raise ValueError("expected --all, --scales, --axes, or --mixed")
    scales_only = mode == ["--scales"]
    selected = ((s, ps) for s, ps in systems(cert)
                if mode == ["--all"] or (mode == ["--mixed"] and s["case"] == "one")
                or (mode == ["--axes"] and s["case"] != "one"))
    for s, polys in selected:
        case, chart = s["case"], s["chart"]
        name = "mixed" if case == "one" else f"axis{case}{chart}"
        g.emit(0, "set_option maxRecDepth 8192 in")
        g.emit(0, "set_option maxHeartbeats 30000000 in")
        g.emit(0, f"theorem {name} (n : ℕ) (hn : 17 ≤ n) (a b c d : K)")
        g.emit(4, " : (let z := (n : K); " + " → ".join(
            [f"({expression(p)} : K) = 0" for p in polys] +
            ([" ∧ ".join(f"({expression(p)} : K) = 0" for p in targets())] if case == "one" else ["False"])
        ) + ") := by")
        names = [f"h{i}" for i in range(len(polys))]
        g.emit(2, "let z : K := n")
        g.emit(2, "dsimp only")
        g.emit(2, "intro " + " ".join(names))
        g.branches(s["steps"], polys, names, 2)
        g.emit(0, "")
    for t, row in enumerate(cert["rows"] if scales_only else []):
        key = checker.parse(row["scale"], NV)
        proof = g.nonzero(key)
        g.emit(0, f"theorem rowScale{t} (n : ℕ) (hn : 17 ≤ n) :")
        g.emit(2, f"(let z : K := n; ({expression(key)} : K)) ≠ 0 := {proof}")
        g.emit(0, "")
    print("import SexticC3.TailDegreeFactorData")
    print()
    namespace = "SexticC3.TailScales" if scales_only else "SexticC3.TailElimination"
    print(f"namespace {namespace}")
    print("open SexticC3.TailDegreeFactors")
    print("variable {K : Type*} [Field K] [CharZero K]")
    print()
    for i, (idx, scale) in enumerate(g.identities):
        cs = factors[idx]
        v = scalar_text(scale)
        print("set_option maxRecDepth 4096 in")
        print("set_option maxHeartbeats 3000000 in")
        print(f"private theorem degree_{i} (n : ℕ) (hn : 17 ≤ n) :")
        print(f"    (let z : K := n; ({expression(g.degree_polys[idx, scale])} : K)) ≠ 0 := by")
        print("  let z : K := n")
        print(f"  change ({expression(g.degree_polys[idx, scale])} : K) ≠ 0")
        print(f"  have hp : ({expression(g.degree_polys[idx, scale])} : K) = ({v}) * {horner(cs)} := by ring")
        print("  rw [hp]")
        print(f"  have h : eval (n : K) {list(cs)} ≠ 0 := eval_ne_zero _ (by decide +kernel) n hn")
        print("  apply mul_ne_zero (by norm_num)")
        print("  simpa only [eval, Int.cast_ofNat, Int.cast_neg, Int.cast_zero, Int.cast_one, z, mul_zero, add_zero] using h")
        print()
    print("\n".join(g.lines))
    print(f"end {namespace}")


if __name__ == "__main__":
    main()
