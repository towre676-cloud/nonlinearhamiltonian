"""Replay sharp binomial Newton proofs and exact rank certificates.

python verify_binomial_newton_sharp.py --perfectjet --write CERTIFICATE.json
python verify_binomial_newton_sharp.py --perfectjet --check CERTIFICATE.json

Requires SymPy 1.14.0. --perfectjet additionally requires the pinned PerfectJet
source/package. No search beyond the analytically proved windows is performed.
"""
from __future__ import annotations
import argparse
import copy
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path
import sympy as s
from binomial_newton_sharp import (
    FAMILIES, classify, hamiltonian, lower_monomials, static_basis,
    transvectant, weight_monomials, window,
)
from weighted_cubic_form import gate_system

q, p, c, a, j = s.symbols("q p c a j")
HERE = Path(__file__).resolve().parent


def ff(n, k):
    return s.prod(n-t for t in range(k))


def sym_trans(h, g, order):
    """Independent differentiation, without the sparse engine's helpers."""
    return s.expand(sum((-1)**t * comb(order, t) * s.diff(h, q, order-t, p, t)
                        * s.diff(g, q, t, p, order-t) for t in range(order+1)))


def expr(poly):
    return sum(s.Rational(v.numerator, v.denominator)*q**i*p**j
               for (i, j), v in poly.items())


def sparse(expression):
    return {m: F(v) for m, v in s.Poly(s.expand(expression), q, p).terms() if v}


def encode(poly):
    return [[i, j, str(v)] for (i, j), v in sorted(poly.items()) if v]


def mat_certificate(matrix, columns, labels):
    """Rank sandwich: nonzero minor plus independent nullspace vectors."""
    rr, piv = matrix.rref()
    row_ids = list(matrix.T.rref()[1])
    col_ids = list(piv)
    null = matrix.nullspace()
    cert = {
        "columns": columns, "row_labels": labels,
        "shape": list(matrix.shape),
        "entries": [[i, j, str(matrix[i, j])] for i in range(matrix.rows)
                    for j in range(matrix.cols) if matrix[i, j]],
        "rank": len(piv), "minor_rows": row_ids, "minor_columns": col_ids,
        "minor_determinant": str(matrix.extract(row_ids, col_ids).det()),
        "kernel": [[str(v) for v in vec] for vec in null],
    }
    verify_rank_certificate(cert)
    return cert


def verify_rank_certificate(cert):
    nr, nc = cert["shape"]
    m = s.zeros(nr, nc)
    seen = set()
    for i, j, v in cert["entries"]:
        assert 0 <= i < nr and 0 <= j < nc and (i, j) not in seen
        seen.add((i, j))
        m[i, j] = s.Rational(v)
    r = cert["rank"]
    assert len(cert["columns"]) == nc and len(cert["row_labels"]) == nr
    assert len(cert["minor_rows"]) == len(cert["minor_columns"]) == r
    determinant = m.extract(cert["minor_rows"], cert["minor_columns"]).det()
    assert determinant == s.Rational(cert["minor_determinant"]) != 0
    vectors = [s.Matrix([s.Rational(v) for v in vec]) for vec in cert["kernel"]]
    assert len(vectors) == nc-r
    assert all(len(vec) == nc and m*vec == s.zeros(nr, 1) for vec in vectors)
    assert (s.Matrix.hstack(*vectors).rank() if vectors else 0) == nc-r
    return m


def operator_certificate(h, monomials, depth=0):
    system = gate_system(h, monomials, depth)
    matrix = s.Matrix(len(system.rows), len(monomials), lambda i, j: system.rows[i][j])
    return mat_certificate(matrix, [list(m) for m in monomials],
                           [list(l) for l in system.labels])


def static_locus_matrix(family):
    """Formula (M), with all parameter-independent row slots retained."""
    info = FAMILIES[family]
    wq, wp = info["weights"]
    h = {(6,0):s.Integer(1), info["edge"]:c}
    h.update({m:s.Symbol("h_%d_%d" % m) for m in lower_monomials(family)})
    cols = window(family)
    labels = [(k,)+m for k in (3,5)
              for w in range(info["bound"]+info["degree"]-k*(wq+wp)+1)
              for m in weight_monomials(family,w)]
    lookup = {label:i for i,label in enumerate(labels)}
    entries = {}
    for col,(aa,jj) in enumerate(cols):
        for (u,v),value in h.items():
            for k in (3,5):
                row_label = k,u+aa-k,v+jj-k
                if row_label not in lookup:
                    continue
                factor = sum((-1)**t*comb(k,t)*ff(u,k-t)*ff(v,t)*ff(aa,t)*ff(jj,k-t)
                             for t in range(k+1))
                if factor:
                    key = lookup[row_label],col
                    entries[key] = entries.get(key,0)+factor*value
    # Direct symbolic differentiation verifies every generated matrix column.
    he = sum(value*q**u*p**v for (u,v),value in h.items())
    for col,(aa,jj) in enumerate(cols):
        for k in (3,5):
            expected = s.Poly(sym_trans(he,q**aa*p**jj,k),q,p)
            for row,(kk,r,t) in enumerate(labels):
                if kk == k:
                    assert s.expand(entries.get((row,col),0)-expected.coeff_monomial(q**r*p**t)) == 0
    return {"shape":[len(labels),len(cols)], "columns":[list(m) for m in cols],
            "row_labels":[list(m) for m in labels],
            "entries":[[i,j,str(s.expand(v))] for (i,j),v in sorted(entries.items()) if v],
            "dimension_at_least_minor_sizes":{str(d):len(cols)-d+1 for d in (8,9,10)},
            "nonzero_parameter":"c"}


def resonance_proof():
    """Symbolic identities and finite endpoint lists; no weight cutoff input."""
    P4 = 5*a*a+6*a*j-19*a-9*j*j-21*j+18
    Q = (a-1)*(a-2)-6*(a-1)*j+3*j*(j-1)
    P3 = 7*a*a+18*a*j-21*a-9*j*j-9*j+14
    assert s.expand(P4-(5*(a-2)*(a-3)-3*(j+1)*(3*j-2*a+4))) == 0
    assert s.expand(P3-(10*(a-1)*(a-2)-3*Q)) == 0
    assert s.expand(P4-P4.subs({a:a-5, j:j+4}, simultaneous=True)) == 2*(13*a+51*j+64)
    assert s.expand(P3-P3.subs({a:a-4, j:j+3}, simultaneous=True)) == 2*(a+63*j+64)
    # Monomial derivative coefficients derived from the defining contraction.
    for (u, v), expected3, expected5 in [
        ((1, 4), 12*a*(a-1)*(3*j-2*a+4), 120*ff(a, 4)*j),
        ((2, 3), -6*a*Q, -120*ff(a, 3)*j*(j-1)),
    ]:
        for k, expected in [(3, expected3), (5, expected5)]:
            actual = sum((-1)**t*comb(k,t)*ff(u,k-t)*ff(v,t)*ff(a,t)*ff(j,k-t)
                         for t in range(k+1))
            assert s.expand(actual-expected) == 0
    # These factorizations prove the terminal lists for all nonnegative integers.
    assert s.factor(Q.subs(a,1)) == 3*j*(j-1)
    assert s.factor(Q.subs(a,2)) == 3*j*(j-3)
    assert s.factor(Q.subs(j,0)) == (a-2)*(a-1)
    assert s.factor(Q.subs(j,1)) == (a-8)*(a-1)
    patterns = {}
    for family, u, v, P, allowed in [
        ("qp4", 1, 4, P4, [(0,0,0),(1,0,0),(2,0,0),(0,1,0),(1,1,0),
                           (0,2,0),(1,2,0),(5,0,1),(6,0,1),(11,0,2)]),
        ("q2p3", 2, 3, P3, [(0,0,0),(1,0,0),(2,0,0),(0,1,0),(1,1,0),
                             (8,1,0),(0,2,0),(4,0,1),(6,0,1),(4,1,1)]),
    ]:
        actual = []
        cases = []
        for j0 in range(3):
            max_links = (2 if j0 == 0 else 1) if family == "qp4" else (2 if j0 < 2 else 1)
            for m in range(max_links+1):
                jt = j0+v*m
                # Exhaustive terminal a values follow from the identities above.
                terminal = ([0,1]+([2] if jt == 0 else [])) if family == "qp4" else (
                    [0]+([1] if jt in (0,1) else [])+([2] if jt in (0,3) else [])
                    +([8] if jt == 1 else []))
                for at in terminal:
                    a0 = at+(6-u)*m
                    failures = []
                    for t in range(m):
                        aa, jj = a0-(6-u)*t, j0+v*t
                        B3 = (12*aa*(aa-1)*(3*jj-2*aa+4) if family == "qp4"
                              else -6*aa*Q.subs({a:aa,j:jj}))
                        active5 = jj >= (1 if family == "qp4" else 2)
                        if B3 == 0:
                            failures.append([t, "zero third-gate propagation"])
                        if active5 and P.subs({a:aa,j:jj}) != 0:
                            failures.append([t, str(P.subs({a:aa,j:jj}))])
                    cases.append({"start":[a0,j0], "links":m, "failures":failures})
                    if not failures:
                        actual.append((a0,j0,m))
        assert sorted(actual) == sorted(allowed), (family,actual)
        wq, wp = FAMILIES[family]["weights"]
        assert max(wq*aa+wp*jj for aa,jj,_ in actual) == FAMILIES[family]["bound"]
        patterns[family] = {"surviving_patterns": sorted(actual), "endpoint_cases": cases}
    return patterns


def symbolic_basis(family):
    u, v = FAMILIES[family]["edge"]
    return [sum(s.Rational(value)*q**i*p**j*c**(j//v) for (i,j),value in g.items())
            for g in static_basis(family)]


def refinement_minor(family):
    u,v = FAMILIES[family]["edge"]
    h = q**6+c*q**u*p**v
    basis = symbolic_basis(family)
    columns = []
    rows = []
    for index,g in enumerate(basis):
        assert sym_trans(h,g,3) == sym_trans(h,g,5) == 0
        dg = sym_trans(h,g,1)
        image = sym_trans(h,dg,3)
        if index in (0,8):
            assert dg == image == sym_trans(h,dg,5) == 0
        else:
            mon,value = s.Poly(image,q,p).terms()[0]
            assert value != 0
            rows.append(mon)
            columns.append(index)
    matrix = s.Matrix([[s.Poly(sym_trans(h,sym_trans(h,basis[col],1),3),q,p).coeff_monomial(mon)
                        for col in columns] for mon in rows])
    assert matrix.is_diagonal()
    determinant = s.factor(matrix.det())
    assert s.Poly(determinant,c).length() == 1 and determinant != 0
    return {"basis":[str(g) for g in basis], "columns":columns,
            "T3_output_monomials":[list(m) for m in rows],
            "diagonal":[str(x) for x in matrix.diagonal()],
            "determinant":str(determinant), "surviving_columns":[0,8]}


def independent_checks(family, coefficient, use_perfectjet):
    h = hamiltonian(family, coefficient)
    he = expr(h)
    count = 0
    if use_perfectjet:
        from perfectjet.polynomial import Poly
        from perfectjet.transvectants import transvectant as pt
        from perfectjet.moyal import PolyH, egorov_defect
        hp = Poly(h)
    for m in window(family):
        cur = {m:F(1)}
        ge = expr(cur)
        for depth in range(2):
            for order in (3,5):
                actual = transvectant(h,cur,order)
                assert actual == sparse(sym_trans(he,ge,order))
                if use_perfectjet:
                    assert actual == pt(hp,Poly(cur),order).terms
                count += 1
            if depth == 0:
                cur = transvectant(h,cur,1)
                ge = sym_trans(he,ge,1)
                assert cur == sparse(ge)
    if use_perfectjet:
        hm = PolyH(1,{(0,m):v for m,v in h.items()})
        for g in static_basis(family,coefficient):
            for depth in range(3):
                gm = PolyH(1,{(0,m):v for m,v in g.items()})
                defect = egorov_defect(hm,gm)
                expected = {}
                for order,scale,hpower in [(3,F(-1,24),2),(5,F(1,1920),4)]:
                    for m,value in transvectant(h,g,order).items():
                        expected[(hpower,m)] = scale*value
                assert defect == PolyH(1,expected)
                g = transvectant(h,g,1)
    return {"coefficient":str(coefficient), "matrix_columns":len(window(family)),
            "gate_comparisons":count, "sympy":True, "perfectjet":use_perfectjet,
            "perfectjet_star_defects":30 if use_perfectjet else 0}


def perturbations(family, use_perfectjet):
    examples = ({"seven":{(3,0):1,(2,1):1}, "eight":{(2,1):1},
                 "nine":{(3,0):1}, "ten":{}} if family == "qp4" else
                {"seven":{(3,0):1,(0,4):1}, "eight":{(3,0):1},
                 "nine":{(4,0):1}, "ten":{}})
    out = {}
    for name,lower in examples.items():
        h = hamiltonian(family, lower=lower)
        cert = operator_certificate(h,window(family))
        expected = {"seven":7,"eight":8,"nine":9,"ten":10}[name]
        assert len(cert["kernel"]) == expected
        result = classify(family,lower=lower)
        assert len(result["static_basis"]) == expected
        # Full first-refinement matrix, not testing individual kernel vectors only.
        basis = result["static_basis"]
        images = []
        for g in basis:
            dg = transvectant(h,g,1)
            images.append({(k,)+m:v for k in (3,5) for m,v in transvectant(h,dg,k).items()})
        labels = sorted(set().union(*(set(x) for x in images)))
        mat = s.Matrix(len(labels),len(basis),lambda i,j:images[j].get(labels[i],0))
        assert mat.rank() == expected-2
        if use_perfectjet:
            from perfectjet.polynomial import Poly
            from perfectjet.transvectants import transvectant as pt
            from perfectjet.kernel_tower import polynomial_kernel_tower
            hp = Poly(h)
            tower = polynomial_kernel_tower([Poly({m:1}) for m in window(family)],
                evolution=lambda g:pt(hp,g,1),
                constraints=[lambda g:pt(hp,g,3),lambda g:pt(hp,g,5)],max_depth=2)
            assert [row["kernel_dimension"] for row in tower["history"]] == [expected,2,2]
        out[name] = {"hamiltonian":encode(h), "static_certificate":cert,
                     "first_rank":expected-2, "tower":[expected,2,2]}
    return out


def build(use_perfectjet=False):
    out = {"schema":"binomial-newton-sharp/1", "arithmetic":"exact rational and symbolic",
           "tail_dependency":"endpoint/resonance proof; no degree-360 search",
           "patterns":resonance_proof(), "families":{}}
    for family in FAMILIES:
        h = hamiltonian(family)
        weights = []
        occupied = []
        for w in range(FAMILIES[family]["bound"]+1):
            cert = operator_certificate(h,weight_monomials(family,w))
            weights.append({"weight":w,"certificate":cert})
            occupied.extend([w]*len(cert["kernel"]))
        expected = ([0,4,5,8,9,10,14,20,24,44] if family=="qp4" else
                    [0,3,4,6,7,8,12,16,18,28])
        assert occupied == expected
        out["families"][family] = {
            "metadata":FAMILIES[family], "occupied_weights":occupied,
            "weights":weights, "refinement":refinement_minor(family),
            "static_locus_matrix":static_locus_matrix(family),
            "independent_checks":[independent_checks(family,c,use_perfectjet)
                                  for c in [F(1),F(2),F(-3,2)]],
            "perturbations":perturbations(family,use_perfectjet),
        }
        print("PASS",family,"sharp bound",FAMILIES[family]["bound"],"dimensions 10,2,2",flush=True)
    # Reject an incorrect rank, determinant, or nullspace witness.
    sample = out["families"]["qp4"]["perturbations"]["seven"]["static_certificate"]
    for kind in ["rank","minor_determinant","kernel"]:
        bad = copy.deepcopy(sample)
        if kind == "rank": bad[kind] += 1
        elif kind == "minor_determinant": bad[kind] = "0"
        else: bad[kind][0] = ["0"]*bad["shape"][1]
        try: verify_rank_certificate(bad)
        except AssertionError: pass
        else: raise AssertionError("corruption accepted: "+kind)
    out["certificate_corruption_tests"] = 3
    out["source_sha256"] = {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        for name in ["binomial_newton_sharp.py","verify_binomial_newton_sharp.py",
                     "BINOMIAL_NEWTON_SHARP_THEOREM.md","weighted_cubic_form.py","exact_observation.py"]}
    out["perfectjet_pin"] = (HERE/"BINOMIAL_NEWTON_PERFECTJET_PIN.txt").read_text().strip()
    out["perfectjet_checked"] = use_perfectjet
    if use_perfectjet:
        from importlib import import_module
        out["perfectjet_source_sha256"] = {
            name:hashlib.sha256(Path(import_module("perfectjet."+name).__file__).read_bytes()).hexdigest()
            for name in ["polynomial","transvectants","kernel_tower","exact","moyal"]}
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--perfectjet",action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write",type=Path)
    group.add_argument("--check",type=Path)
    args = parser.parse_args()
    data = build(args.perfectjet)
    if args.check:
        assert json.loads(args.check.read_text()) == json.loads(json.dumps(data)), "receipt differs"
    if args.write:
        args.write.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print("PASS all symbolic identities, endpoint cases, exact rank certificates, perturbations and corruption tests")
