#!/usr/bin/env python3
"""Independent direct mixed-derivative audit of the three 2026-10-22 extensions.

This checker has its own sparse rational arithmetic and imports no producer.
Finite checks calibrate the universal proofs in extension_proof_review.md;
they do not substitute a bounded matrix for an all-degree theorem.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json


def tidy(a):
    return {k: v for k, v in a.items() if v}


def mon(q=0, p=0, c=1):
    return tidy({(q, F(p)): F(c)})


def add(*aa):
    z = {}
    for a in aa:
        for k, v in a.items():
            z[k] = z.get(k, F(0)) + v
    return tidy(z)


def times(a, b):
    z = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            key = (i+k, j+l)
            z[key] = z.get(key, F(0)) + v*w
    return tidy(z)


def scale(a, s):
    return tidy({k: v*s for k, v in a.items()})


def power(a, n):
    z = mon()
    for _ in range(n):
        z = times(z, a)
    return z


def partial(a, nq=0, np=0):
    z = {}
    for (i, j), v in a.items():
        c = v
        for k in range(nq):
            c *= i-k
        for k in range(np):
            c *= j-k
        if c:
            z[(i-nq, j-np)] = c
    return z


def gate(h, g, k):
    return add(*(scale(times(partial(h, k-j, j), partial(g, j, k-j)),
                       (-1)**j*comb(k,j)) for j in range(k+1)))


def substitute_Q(g, u):
    Q = add(mon(0,1), u)
    return add(*(scale(times(mon(i), power(Q, int(j))), c)
                 for (i,j), c in g.items()))


def eval_P(P, Q, derivative=0):
    ans = {}
    for n, c in enumerate(P):
        if n < derivative:
            continue
        for k in range(derivative):
            c *= n-k
        ans = add(ans, scale(power(Q, n-derivative), c))
    return ans


def rank_columns(columns):
    pivots = {}
    for source in columns:
        col = dict(source)
        while col:
            lead = min(col)
            value = col[lead]
            if lead not in pivots:
                pivots[lead] = {k: v/value for k,v in col.items()}
                break
            for k,v in pivots[lead].items():
                col[k] = col.get(k,F(0))-value*v
                if not col[k]:
                    del col[k]
    return len(pivots)


def kernel_dimension(h, u, bound, depth):
    columns = []
    for n in range(bound+1):
        for a in range(n+1):
            g = substitute_Q(mon(a,n-a),u)
            col = {}
            for r in range(depth+1):
                for key, value in gate(h,g,3).items():
                    col[(r,*key)] = value
                g = gate(h,g,1)
            columns.append(col)
    return len(columns)-rank_columns(columns)


def check():
    operator_checks = 0
    composition_dimensions = []
    for m,mu,A,eps in [(3,3,1,0),(3,4,-2,3),(4,3,2,-1),(5,5,1,2)]:
        u = add(mon(m,0,A),mon(2,0,2),mon(1,0,-1),mon(0,0,3))
        Q = add(mon(0,1),u)
        P = [F(2), F(-3)] + [F(1)]*(mu-2) + [F(A)]
        h = add(eval_P(P,Q),mon(1,0,eps))
        for n in range(6):
            for a in range(n+1):
                g_new = mon(a,n-a)
                g = substitute_Q(g_new,u)
                gq = substitute_Q(partial(g_new,1),u)
                gQ = substitute_Q(partial(g_new,0,1),u)
                expected_D = add(scale(times(eval_P(P,Q,1),gq),-1),scale(gQ,eps))
                assert gate(h,g,1) == expected_D
                expected_C = add(
                    times(partial(u,3),add(
                        times(eval_P(P,Q,1),substitute_Q(partial(g_new,0,3),u)),
                        scale(times(eval_P(P,Q,3),gQ),-1))),
                    scale(times(partial(u,2),add(
                        times(eval_P(P,Q,2),substitute_Q(partial(g_new,1,2),u)),
                        times(eval_P(P,Q,3),substitute_Q(partial(g_new,1,1),u)))), -3),
                    scale(times(eval_P(P,Q,3),substitute_Q(partial(g_new,3),u)),-1))
                assert gate(h,g,3) == expected_C
                operator_checks += 1
        assert gate(h,Q,3)
        assert not gate(h,gate(h,Q,1),3)
        assert not gate(h,mon(1),3)
        assert gate(h,gate(h,mon(1),1),3)
        if mu <= 4:
            dim = kernel_dimension(h,u,mu,1)
            assert dim == 2
            composition_dimensions.append({'m':m,'mu':mu,'bound':mu,'dimension':dim})

    oscillator_dimensions = []
    for m,kappa,depth in [(2,3,3),(3,0,2),(3,-2,2),(4,3,2)]:
        A,B,eps,b = F(2),F(-3),F(5),F(-1)
        u = add(mon(m,0,b),mon(1,0,2),mon(0,0,-1))
        Q = add(mon(0,1),u)
        h = add(scale(power(Q,2),A),scale(Q,B),mon(2,0,F(kappa,2)),mon(1,0,eps),mon(0,0,7))
        dim = kernel_dimension(h,u,4,depth)
        assert dim == 6
        oscillator_dimensions.append({'m':m,'kappa':kappa,'depth':depth,'bound':4,'dimension':dim})
        q3 = mon(3)
        assert not gate(h,q3,3)
        assert not gate(h,gate(h,q3,1),3)
        assert gate(h,gate(h,gate(h,q3,1),1),3) == scale(partial(u,2),-288*A**3)

    A,b,kappa = F(2),F(-3),F(5)
    u = mon(2,0,b)
    Q = add(mon(0,1),u)
    h = add(scale(power(Q,2),A),mon(2,0,kappa/2))
    witness = add(scale(times(mon(2),Q),3*kappa),scale(power(Q,3),4*A))
    g = witness
    for r in range(3):
        assert not gate(h,g,3)
        g = gate(h,g,1)
    assert gate(h,g,3) == mon(0,0,-1728*A**3*b*kappa**2)
    assert kernel_dimension(h,u,4,2) == 7
    assert kernel_dimension(h,u,4,3) == 6

    # The complete quadratic-transverse theorem is calibrated beyond the
    # former weighted boundary, with its sharp third-gate depth witnesses.
    frontier_depths = []
    for m,n in [(2,3),(2,4),(3,3),(4,3),(3,4),(3,6),(3,8)]:
        A = F(2)
        u = add(mon(m,0,-1),mon(2,0,2),mon(1,0,-3))
        Q = add(mon(0,1),u)
        V = add(mon(n,0,F(3,2)),mon(2,0,-2),mon(1,0,3))
        h = add(scale(power(Q,2),A),V)
        depth = 6 if n == 3 else 4
        g = mon(1)
        for r in range(depth):
            assert not gate(h,g,3), (m,n,r)
            g = gate(h,g,1)
        expected = (scale(times(partial(u,2),power(partial(V,3),2)),-960*A**5)
                    if n == 3 else
                    scale(times(partial(u,2),partial(V,4)),96*A**4))
        assert gate(h,g,3) == expected and expected
        frontier_depths.append({'shear_degree':m,'potential_degree':n,'sharp_depth':depth})

    # Parameter polynomials are coefficient dictionaries of independently
    # computed original-chart observables, with no discarded outputs.
    def param_gate(hs,gs,k):
        result = {}
        for i,h in hs.items():
            for j,g in gs.items():
                result[i+j] = add(result.get(i+j,{}),gate(h,g,k))
        return {i:g for i,g in result.items() if g}
    u = mon(2)
    Q = add(mon(0,1),u)
    family = {0:power(Q,2),1:mon(2,0,F(1,2))}
    lifted = {0:power(Q,3),1:scale(times(mon(2),Q),F(3,4))}
    iterated = lifted
    for r in range(3):
        assert not param_gate(family,iterated,3)
        iterated = param_gate(family,iterated,1)
    assert param_gate(family,iterated,3) == {2:mon(0,0,-432)}

    affine_depths = []
    for degree in (0,1):
        for n in (3,4,6):
            A = F(-2,3)
            u = mon(0,0,2) if degree == 0 else add(mon(1,0,-3),mon(0,0,2))
            Q = add(mon(0,1),u)
            V = add(mon(n,0,F(3,2)),mon(2,0,-2),mon(1,0,3))
            h = add(scale(power(Q,2),A),V)
            depth = 7 if n == 3 else 5
            g = mon(1)
            for r in range(depth):
                assert not gate(h,g,3), (degree,n,r)
                g = gate(h,g,1)
            expected = (scale(power(partial(V,3),3),-960*A**5)
                        if n == 3 else
                        scale(times(partial(V,3),partial(V,4)),96*A**4))
            assert gate(h,g,3) == expected and expected
            affine_depths.append({'shear_degree':degree,'potential_degree':n,'sharp_depth':depth})

    # Independent replay of the cubic quadratic-shear universal minor.
    # Every selected row has parameter degree <= its depth, so 33 exact
    # agreements prove the degree<=32 determinant identity for all lambda.
    minor_rows = [(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,2,0),
                  (2,0,0),(2,1,0),(2,2,0),(2,3,0),(3,0,0),(3,1,0),
                  (4,0,0),(5,0,0),(6,0,0)]
    minor_monomials = [(i,j) for j in range(4) for i in range(7-2*j)
                       if (i,j) not in [(0,0),(0,2)]]
    def determinant(matrix):
        mat = [list(row) for row in matrix]
        answer = F(1)
        for k in range(len(mat)):
            pivot = next((i for i in range(k,len(mat)) if mat[i][k]),None)
            if pivot is None:
                return F(0)
            if pivot != k:
                mat[k],mat[pivot] = mat[pivot],mat[k]
                answer = -answer
            value = mat[k][k]
            answer *= value
            for i in range(k+1,len(mat)):
                factor = mat[i][k]/value
                for j in range(k+1,len(mat)):
                    mat[i][j] -= factor*mat[k][j]
        return answer
    minor_values = []
    for lam in range(33):
        h_new = add(mon(0,2),mon(3),mon(1,0,lam))
        cols = []
        for i,j in minor_monomials:
            g = mon(i,j)
            output = {}
            for r in range(7):
                correction = add(scale(partial(g,0,3),6),scale(partial(g,1,2),-12))
                output.update({(r,*key):value for key,value in correction.items()})
                g = gate(h_new,g,1)
            cols.append(output)
        matrix = [[col.get(row,F(0)) for col in cols] for row in minor_rows]
        minor_values.append(determinant(matrix))
    assert sum(row[0] for row in minor_rows) == 32
    assert set(minor_values) == {F(-2489071056189074244411853807879968522240000000)}

    exponents = [F(0),F(-1,4),F(3,4),F(5,2)]
    def indicial(nu):
        return nu*(nu-1)*(nu-2)*(nu-3)+3*nu*(nu-1)*(nu-2)-F(15,16)*nu*(nu-1)-F(15,32)*nu
    for nu in exponents+[F(7,4),F(1),F(1,2),F(-2)]:
        assert indicial(nu) == nu*(4*nu+1)*(4*nu-3)*(2*nu-5)/32
    potential_cases = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(7,2,-3,4)]
    for c0,a,b,c in potential_cases:
        V = add(*(mon(0,nu,v) for nu,v in zip(exponents,[c0,a,b,c])))
        h = add(mon(1,F(-1,4)),V)
        K = add(h,mon(0,0,-c0))
        cubic = power(K,3)
        assert not gate(h,cubic,1)
        assert not gate(h,cubic,3)
        assert not gate(h,cubic,5)
        # An unremoved constant generically creates a forbidden quadratic term.
        if c0 and (a or b or c):
            assert gate(h,power(h,3),3)
    rejected = add(mon(1,F(-1,4)),mon(0,F(7,4)))
    assert gate(rejected,power(rejected,3),3)

    return {
        'status':'passed','format':'core-extension-independent-audit-v1',
        'direct_operator_comparisons':operator_checks,
        'composition_joint_kernel_dimensions':composition_dimensions,
        'oscillator_joint_kernel_dimensions':oscillator_dimensions,
        'quadratic_shear_depth_two_dimension':7,
        'quadratic_shear_depth_three_dimension':6,
        'quartic_resonance_witness':'C3 D^3 G = -1728 A^3 b kappa^2',
        'analytic_potential_cases':len(potential_cases),
        'quadratic_frontier_sharp_depths':frontier_depths,
        'affine_shear_sharp_depths':affine_depths,
        'quadratic_shear_cubic_minor':{'size':14,'parameter_degree_bound':32,'exact_evaluations':33,'constant_determinant':str(minor_values[0])},
        'formal_cubic_lift_residual':'C3 D_t^3 (Q^3+3tq^2Q/4) = -432t^2',
        'euler_indicial_identity':'nu(4nu+1)(4nu-3)(2nu-5)/32',
        'constant_shift_warning':'(H-c0)^3 is exact; H^3 generally is not',
        'scope':'Independent exact finite calibrations; universal conclusions rest on the reviewed proofs.'}


if __name__ == '__main__':
    result = check()
    Path(__file__).with_name('extension_proof_review_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
