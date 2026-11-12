"""Independent replay of schema hamiltonian-sextic-core/2.

Schema 2 is opt-in (sextic_core.classify_sextic_v2, or `--schema 2` on the
CLI).  This checker does not generate classifications.  It validates a
supplied report by the defining star product and by kernels on all inputs of
bounded total degree with untruncated gate outputs.  Those kernel
comparisons are bounded evidence; completeness rests on the cited theorems.

    python research/hamiltonian/c3_strata/verify_sextic_core_v2.py
"""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import verify_sextic_core as V            # noqa: E402
import verify_quadratic_sixfold as Q      # noqa: E402
import partner_lab                        # noqa: E402

E, C = V.E, V.C
ONE = {(0, 0): F(1)}
SCHEMA = "hamiltonian-sextic-core/2"
KINDS = ("finite_basis", "polynomial_family", "module_plus_finite")


def space_samples(space, degree, powers=(0, 1, 2, 4)):
    """(samples for gate checks, spanning set inside total degree <= degree)."""
    V.require(space.get("kind") in KINDS, "Unknown space kind")
    if space["kind"] == "finite_basis":
        basis = V.space_basis(space)
        return basis, [G for G in basis if V.total_degree(G) <= degree]
    V.require(space.get("dimension") is None, "Infinite space must have null dimension")
    generators = [V.polynomial(G) for G in space["coefficient_generators"]]
    V.require(len(generators) == 1 and V.total_degree(generators[0]) == 1,
              "Schema-2 modules are over Q[L] for one linear form L")
    L = generators[0]
    module = [V.polynomial(G) for G in space["module_basis"]]
    finite = [V.polynomial(G) for G in space.get("finite_span", [])]
    V.require(bool(module) and all(module), "Module basis must contain nonzero polynomials")
    V.require((space["kind"] == "module_plus_finite") == bool(finite),
              "finite_span must be present exactly for module_plus_finite")
    samples = finite + [E.multiply(E.power(L, e), base) for e in powers for base in module]
    inside = [G for G in finite if V.total_degree(G) <= degree]
    for base in module:
        power = dict(ONE)
        while V.total_degree(E.multiply(power, base)) <= degree:
            inside.append(E.multiply(power, base))
            power = E.multiply(power, L)
    return samples, inside


def first_failure(H, G, limit=12):
    current = G
    for iterate in range(limit + 1):
        if E.defects(H, current):
            return iterate
        current = E.poisson(H, current)
    return None


def quadratic_complement_type(H, leading):
    """Independently recognize the degree-two branch and whether S0 is known."""
    if leading["geometric_root_pattern"] != [6]:
        return None
    q6 = H.get((6, 0), 0)
    a, b = (1, H.get((5, 1), 0) / (6 * q6)) if q6 else (0, 1)

    def transverse(G):
        return E.add(E.scale(E.derivative(G, q=1), -b),
                     E.scale(E.derivative(G, p=1), a))

    squared = transverse(transverse(H))
    if not squared or transverse(squared):
        return None
    return "constant" if V.total_degree(squared) == 0 else "variable"


def check_report_v2(H, report, *, degree=6):
    """Check supplied schema-2 claims.  Returns the bounded stage dimensions."""
    H = {key: F(value) for key, value in H.items() if value}
    V.require(report.get("schema") == SCHEMA, "Unexpected classifier schema")
    V.require(json.loads(json.dumps(report)) == report, "Report is not exact JSON")
    V.require(V.polynomial(report.get("input")) == H, "Input polynomial was not preserved")
    spaces = report["classification"]
    first = C.classify_sextic(H)
    complement = quadratic_complement_type(H, first["leading"])
    supported = first["status"] == "classified" or complement is not None
    V.require((report["status"] == "classified") == supported,
              "Report status disagrees with the supported family")
    if report["status"] != "classified":
        V.require(report["status"] == "unsupported" and report.get("unsupported_reason"),
                  "Unclassified report must be unsupported with a reason")
        V.require(all(spaces.get(name) is None for name in ("stages", "Dinf", "depth")),
                  "Unsupported result contains space claims")
        return None
    stages, depth = spaces["stages"], spaces["depth"]
    V.require([stage["index"] for stage in stages] == list(range(len(stages))),
              "Stages must be indexed consecutively from zero")
    V.require(depth["kind"] in ("least", "sufficient") and type(depth["value"]) is int,
              "Malformed depth")
    for stage in stages:
        V.require(stage["status"] in ("classified", "unknown"), "Malformed stage status")
        V.require((stage["status"] == "unknown") == (stage["space"] is None),
                  "An unknown stage must carry no space, and a classified stage must carry one")
        V.require(stage["status"] == "classified" or stage.get("reason"),
                  "An unknown stage needs a reason")

    if spaces.get("derived_from") == "hamiltonian-sextic-core/1":
        first = V.check_report(H, first)
        old = first["classification"]
        V.require(len(stages) == 3 and stages[0]["status"] == "unknown",
                  "Schema-1 results expose S1 and S2 only")
        V.require(stages[1]["space"] == old["S1"] and stages[2]["space"] == old["S2"]
                  and spaces["Dinf"] == old["Dinf"], "Schema-2 spaces differ from schema 1")
        V.require(depth == {"value": old["sufficient_refinement_depth"], "kind": "sufficient"},
                  "Depth differs from schema 1")
        V.require(spaces["obstruction"] == first["obstruction"]
                  and spaces["quadratic_lift"] == first["quadratic_lift"],
                  "Certificates differ from schema 1")
        return None

    V.require(spaces["method"] == "sixfold_quadratic_complement" and depth["kind"] == "least",
              "Unexpected schema-2 method")
    V.require(first["status"] == "unsupported" and complement is not None,
              "Quadratic report does not match its input family")
    d = depth["value"]
    V.require(d >= 1 and len(stages) == d + 1, "Stages must run from S0 to the least depth")
    V.require(all(stage["status"] == "classified" for stage in stages[1:]),
              "Only S0 may be unknown")
    V.require((stages[0]["status"] == "classified") == (complement == "constant"),
              "S0 status disagrees with the squared-complement coefficient")
    kernels = Q.kernels(H, degree, d + 1)
    dims, previous = [], None
    for stage, kernel in zip(stages, kernels):
        if stage["status"] == "unknown":
            dims.append(None)
            continue
        samples, inside = space_samples(stage["space"], degree)
        for G in samples:
            V.gates_through(H, G, stage["index"])
        V.require(V.same_span(kernel, inside),
                  f"S^{stage['index']} differs from the bounded kernel")
        if previous is not None and stage["space"]["kind"] == "finite_basis":
            V.require(V.span_rank(previous + inside) == V.span_rank(previous),
                      "Stages are not nested")
        previous = inside
        dims.append(len(kernel))
    core, core_inside = space_samples(spaces["Dinf"], degree)
    V.require(spaces["Dinf"]["kind"] == "finite_basis" and stages[d]["space"] == spaces["Dinf"],
              "The stage at the least depth must equal the core")
    V.require(V.span_rank(core + [dict(ONE), H]) == len(core), "Core must contain 1 and H")
    for G in core:
        V.require(V.span_rank(core + [E.poisson(H, G)]) == len(core),
                  "Core is not closed under the classical derivation")
        V.gates_through(H, G, d + 2)
    V.require(V.same_span(kernels[d + 1], core_inside), "Core differs from the next bounded kernel")
    witness = spaces["sharpness_witness"]
    V.require(witness["first_failing_iterate"] == d
              and first_failure(H, V.polynomial(witness["G"])) == d,
              "Sharpness witness does not fail first at the least depth")
    integral = spaces.get("square_first_integral")
    V.require((integral is not None) == (complement == "variable" and len(core) == 3),
              "Square first integral is required exactly for the three-dimensional variable core")
    if integral is not None:
        G = V.polynomial(integral)
        V.require(not E.poisson(H, G) and not E.defects(H, G)
                  and V.span_rank(core + [G]) == len(core) == 3,
                  "Square first integral must be a Poisson-commuting core element")
        square = E.power(G, 2)
        pivot = next((key for key in square if key != (0, 0)), None)
        V.require(pivot is not None and H.get(pivot)
                  and V.total_degree(E.add(H, E.scale(square, -H[pivot] / square[pivot]))) <= 0,
                  "Hamiltonian must be a nonzero multiple of the reported integral squared plus a constant")
    return dims


# text, regime, least depth, core dimension
QUADRATIC = [
    ("q^6+p^2", "affine_shift", 5, 2),
    ("q^6+q+p+p^2", "affine_shift", 5, 2),
    ("2*q^6-3*q^5+q^4+5*q^3-q^2+7*q+1+(3*q-2)*p+p^2", "affine_shift", 5, 2),
    ("q^6+q^2*p+p^2", "generic_nonlinear", 4, 2),
    ("2*q^6-3*q^5+q^4+5*q^3-q^2+7*q+1+(3*q^4-q^3+2*q+1)*p+3*p^2", "generic_nonlinear", 4, 2),
    ("(p+q^3)^2+q^3", "cubic_potential", 6, 2),
    ("(p+q^3+q^2-3*q+1)^2+3*q^2-q", "hidden_quadratic", 2, 6),
    ("(p+q^3)^2", "hidden_quadratic", 2, 6),
    ("q^6+q*p^2", "variable_top_coefficient", 3, 2),
    ("2*q^6-q^5+q^3+7*q+(q-2)*p^2+(q^4-q+1)*p", "variable_top_coefficient", 3, 2),
    ("2*q^6-q^5+q^3+7*q+(q^2-2*q+3)*p^2+(q^4-q+1)*p", "variable_top_coefficient", 2, 2),
    ("q^6+(q^3+q+1)*p^2", "variable_top_coefficient", 1, 2),
    # Theorem E: the criterion holds
    ("q^6+q^2*p^2+2*q^4*p", "variable_top_coefficient", 1, 3),
    ("3*((q-3)*p+2*(q-3)^3+q+2)^2-7", "variable_top_coefficient", 1, 3),
    # Theorem E: each condition broken separately, still on the discriminant locus
    ("((q-3)*p+2*(q-3)^3+q+2)^2+p^2", "variable_top_coefficient", 2, 2),      # c not a square
    ("((q-3)*p+2*(q-3)^3+q+2)^2+p", "variable_top_coefficient", 2, 2),        # u does not divide b
    ("((q-3)*p+2*(q-3)^3+q+2)^2+q^2", "variable_top_coefficient", 2, 2),      # residual not constant
]
TRANSFORMS = {
    4: (((2, 1), (1, 3)), (1, -2), F(3, 2)),
    5: (((1, 2), (-1, 3)), (F(1, 2), 1), F(-2)),
    7: (((0, 2), (1, 1)), (2, F(-1, 3)), F(5)),
    9: (((3, 1), (2, 2)), (-1, 2), F(2, 3)),
    13: (((1, 1), (0, 2)), (1, 0), F(3)),
    15: (((2, -1), (1, 1)), (0, 1), F(-1, 2)),
}
UNSUPPORTED = ["q^6+p^5", "q^6+q*p^3+p^2", "q^5*p+p^2", "q^3*p^3+q"]


def verify(degree=6):
    derived = 0
    for name, pattern, H, dimensions in V.fixtures():
        for poly in (H, V.sparse_add(H, {(0, 0): F(7, 3)})):
            check_report_v2(poly, C.classify_sextic_v2(poly))
            derived += 1
    for text in ("q^4*p^2+q^3", "q^6+q^3*p+q", "p^6+p^3*q", "q^6+p^6+q*p"):
        H = partner_lab.parse(text)
        check_report_v2(H, C.classify_sextic_v2(H))
        derived += 1
    check_report_v2({}, C.classify_sextic_v2({}))
    derived += 1

    records = []
    for index, (text, regime, depth, core) in enumerate(QUADRATIC):
        for transform in [None] + ([TRANSFORMS[index]] if index in TRANSFORMS else []):
            H = partner_lab.parse(text)
            if transform is not None:
                matrix, shift, scalar = transform
                H = V.sparse_add(V.affine_substitute(H, matrix, shift, scalar),
                                 {(0, 0): F(7, 3)})
            report = C.classify_sextic_v2(H)
            V.require(C.classify_sextic(H)["status"] == "unsupported",
                      f"{text}: schema 1 must keep its unsupported status")
            spaces = report["classification"]
            V.require(report["status"] == "classified" and spaces["regime"] == regime
                      and spaces["depth"]["value"] == depth
                      and spaces["Dinf"]["dimension"] == core, f"{text}: unexpected result")
            dims = check_report_v2(H, report, degree=degree)
            records.append({"H": text, "rational_affine_change": transform is not None,
                            "regime": regime, "least_depth": depth, "core_dimension": core,
                            "stage_kinds": [None if s["space"] is None else s["space"]["kind"]
                                            for s in spaces["stages"]],
                            "bounded_dimensions": dims,
                            "square_first_integral": spaces["square_first_integral"] is not None})
    for text in UNSUPPORTED:
        H = partner_lab.parse(text)
        check_report_v2(H, C.classify_sextic_v2(H))

    rejected = 0
    for corrupt, expression in (
        ("depth", "q^6+q*p^2"), ("witness", "q^6+q*p^2"),
        ("stage", "q^6+q*p^2"), ("unknown", "q^6+q*p^2"),
        ("omitted_static", "q^6+p^2"), ("omitted_integral", "(q*p+q^3)^2"),
        ("false_unsupported", "q^6+p^2"), ("zero_module", "q^6+p^2"),
    ):
        H = partner_lab.parse(expression)
        report = C.classify_sextic_v2(H)
        spaces = report["classification"]
        if corrupt == "depth":
            spaces["depth"]["value"] -= 1
        elif corrupt == "witness":
            spaces["sharpness_witness"]["G"] = [{"q": 2, "p": 0, "coefficient": "1"}]
        elif corrupt == "stage":
            spaces["stages"][2]["space"] = spaces["stages"][1]["space"]
        elif corrupt == "unknown":
            spaces["stages"][0]["space"] = spaces["Dinf"]
        elif corrupt == "omitted_static":
            spaces["stages"][0] = {"index": 0, "status": "unknown",
                                   "space": None, "reason": "omitted"}
        elif corrupt == "omitted_integral":
            spaces["square_first_integral"] = None
        elif corrupt == "false_unsupported":
            report.update(status="unsupported", unsupported_reason="omitted")
            spaces.update(stages=None, Dinf=None, depth=None)
        else:
            spaces["stages"][0]["space"]["module_basis"][0] = []
        try:
            check_report_v2(H, report)
        except V.VerificationError:
            rejected += 1
        else:
            raise V.VerificationError(f"Corrupted schema-2 report accepted: {corrupt}")

    receipt = {
        "schema": "hamiltonian-sextic-core-independent-replay/2",
        "status": "PASS",
        "schema_1_derived_checks": derived,
        "quadratic_complement_checks": records,
        "unsupported_checks": UNSUPPORTED,
        "corrupted_reports_rejected": rejected,
        "input_degree": degree,
        "source_sha256": Q.source_hashes(Path(__file__).resolve(), HERE.parent / "quadratic_sixfold.py"),
        "proof_boundary": {
            "finite_checks": "Direct defining-star expansion, exact span checks, bounded kernels.",
            "all_degree_dependencies": "Schema-1 dependencies and QUADRATIC_SIXFOLD_THEOREM.md.",
            "formalization": "This Python replay is not a Lean proof.",
        },
    }
    return receipt


if __name__ == "__main__":
    print(json.dumps(verify(), indent=1, sort_keys=True))
