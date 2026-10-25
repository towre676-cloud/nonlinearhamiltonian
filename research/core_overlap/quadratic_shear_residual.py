#!/usr/bin/env python3
"""Complete nonlinear-residual cores for quadratic shears, exact standard library.

For H=A(p+u(q))^2+V(q), deg u=2 and deg V>=3, the full core is
span{1,H}. The sharp third-gate depth is six for cubic V and four for
higher V. The cubic all-degree proof uses a 16-dimensional weighted bound
and an exact parameter-polynomial determinant identity of degree at most32.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT/'extensions'/'hamiltonian')]
import pure_transverse as U
import weyl_receipts as W

ROWS = [(0,0,0),(0,1,0),(1,0,0),(1,1,0),(1,2,0),
        (2,0,0),(2,1,0),(2,2,0),(2,3,0),(3,0,0),(3,1,0),
        (4,0,0),(5,0,0),(6,0,0)]
MONOMIALS = [(i,j) for j in range(4) for i in range(7-2*j)
             if (i,j) not in [(0,0),(0,2)]]
DETERMINANT = -2489071056189074244411853807879968522240000000


def determinant(rows):
    """Exact fraction elimination with no compiler rank dependency."""
    matrix = [list(row) for row in rows]
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError('square matrix required')
    value = F(1)
    for col in range(n):
        pivot = next((i for i in range(col,n) if matrix[i][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            matrix[col],matrix[pivot] = matrix[pivot],matrix[col]
            value = -value
        p = matrix[col][col]
        value *= p
        for i in range(col+1,n):
            factor = matrix[i][col]/p
            for j in range(col+1,n):
                matrix[i][j] -= factor*matrix[col][j]
    return value


def transformed_D(g, lam):
    return U.add(U.scale(U.mul({(0,1):F(1)},U.deriv(g,1)),-2),
                 U.mul({(2,0):F(3),(0,0):F(lam)},U.deriv(g,0,1)))


def transformed_C(g):
    return U.add(U.scale(U.deriv(g,0,3),6),U.scale(U.deriv(g,1,2),-12))


def parameter_matrix(lam, monomials=MONOMIALS, rows=ROWS):
    columns = []
    for e in monomials:
        g = {e:F(1)}
        col = {}
        for r in range(7):
            col.update({(r,*k):v for k,v in transformed_C(g).items()})
            g = transformed_D(g,lam)
        columns.append(col)
    return [[col.get(tuple(key),F(0)) for col in columns] for key in rows]


def determinant_certificate():
    return {'format':'quadratic-shear-cubic-minor-v1',
            'normal_form':'(p+q^2)^2+q^3+lambda*q',
            'monomials':[list(e) for e in MONOMIALS],
            'rows':[list(k) for k in ROWS],
            'parameter_degree_bound':sum(row[0] for row in ROWS),
            'determinant':str(DETERMINANT),
            'evaluation_points':list(range(33)),
            'identity_reason':'Each depth-r row has lambda degree at most r. A degree<=32 determinant agreeing with its stated constant at33 distinct exact points is identically that constant.'}


def check_determinant_certificate(cert):
    if cert.get('format')!='quadratic-shear-cubic-minor-v1':
        raise ValueError('unknown determinant certificate')
    monomials = [tuple(e) for e in cert['monomials']]
    rows = [tuple(e) for e in cert['rows']]
    if monomials != MONOMIALS or rows != ROWS:
        raise ValueError('minor populations altered')
    bound = sum(r for r,i,j in rows)
    if cert['parameter_degree_bound'] != bound:
        raise ValueError('parameter degree bound mismatch')
    points = cert['evaluation_points']
    if (any(type(x) is not int for x in points) or len(set(points))!=len(points)
            or len(points)<=bound):
        raise ValueError('insufficient distinct exact interpolation points')
    stated = F(cert['determinant'])
    if not stated:
        raise ValueError('minor must be nonzero')
    for lam in points:
        if determinant(parameter_matrix(lam,monomials,rows)) != stated:
            raise ValueError('parameter polynomial identity failed')
    return {'status':'passed','minor_size':len(monomials),
            'parameter_degree_bound':bound,'exact_evaluations':len(points),
            'determinant':str(stated)}


@lru_cache(maxsize=1)
def generic_cubic_certificate_checked():
    return check_determinant_certificate(determinant_certificate())


def recognize(H):
    H=U.tidy(H)
    if max((j for i,j in H),default=-1)!=2:
        return None
    a={(i,j):v for (i,j),v in H.items() if j==2}
    if set(a)!={(0,2)}:
        return None
    A=a[(0,2)]
    u={(i,0):v/(2*A) for (i,j),v in H.items() if j==1}
    if max((i for i,j in u),default=-1)!=2:
        return None
    Q=U.add({(0,1):F(1)},u)
    V=U.add(H,U.scale(U.power(Q,2),-A))
    n=max((i for i,j in V),default=-1)
    if n<3:
        return None
    return A,u,Q,V,n


def classify(H):
    H=U.tidy(H)
    shape=recognize(H)
    if shape is None:
        return None
    A,u,Q,V,n=shape
    result={'proved':True,'route':'QR','scope':'constant quadratic momentum coefficient; quadratic shear and nonlinear polynomial residual',
            'dimension':2,'core':'span{1,H}','basis':[U.terms({(0,0):F(1)}),U.terms(H)],
            'closure':[['0','0'],['0','0']], 'third_gate_depth':6 if n==3 else 4,
            'A':str(A),'u':U.terms(u),'V':U.terms(V),
            'proof':'quadratic_shear_residual.md','active_part':'0'}
    if n==3:
        generic_cubic_certificate_checked()
        v=V[(3,0)];v2=V.get((2,0),F(0));v1=V.get((1,0),F(0));b=u[(2,0)]
        h=-v2/(3*v);e=v1-v2*v2/(3*v)
        s=v/(A*b*b);t=b*s*s
        lam=e*A*A*b**4/v**3
        result['normalization']={'q_translation':str(h),'q_scale':str(s),'p_scale':str(t),
                                 'lambda':str(lam)}
        uq1=u.get((1,0),F(0));uq0=u.get((0,0),F(0))
        oldq=U.tidy({(1,0):s,(0,0):h})
        oldp=U.tidy({(0,1):t,(1,0):-(2*b*h+uq1)*s,
                       (0,0):-(b*h*h+uq1*h+uq0)})
        pulled=U.add(*(U.scale(U.mul(U.power(oldq,i),U.power(oldp,j)),c)
                       for (i,j),c in H.items()))
        pulled=U.add(pulled,{(0,0):-pulled.get((0,0),F(0))})
        normalized=U.scale(pulled,1/(A*t*t))
        expected=U.add(U.power({(0,1):F(1),(2,0):F(1)},2),
                       {(3,0):F(1),(1,0):lam})
        assert normalized==U.tidy(expected), 'affine normalization failed'
        result['normalization']['exact_pullback_verified']=True
        result['certificate']=determinant_certificate()
    for f in ({(0,0):F(1)},H):
        assert not U.bracket(H,f)
        assert not U.transvectant(H,f,3)
    return result


def make(u,V,A=1):
    u={(i,0):F(v) for i,v in u.items() if v}
    Q=U.add({(0,1):F(1)},u)
    H=U.add(U.scale(U.power(Q,2),F(A)),{(i,0):F(v) for i,v in V.items() if v})
    return H,Q


def self_test():
    determinant_result=generic_cubic_certificate_checked()
    counts={'instances':0,'operator_identities':0,'sharp_depth_checks':0,'forgeries':0,'scope_rejections':0,'exact_affine_normalizations':0}
    records=[]
    for u,A in (({2:1},F(1)),({2:F(-2,3),1:2,0:-1},F(-3,2)),({2:2,1:-1},F(2))):
        for V in ({3:1},{3:F(-2,3),2:2,1:-1,0:3},{3:1,1:-2},
                  {4:1},{5:-2,2:3},{8:F(1,2),3:2}):
            H,Q=make(u,V,A)
            ans=classify(H);assert ans and ans['dimension']==2
            counts['instances']+=1
            if max(V)==3:counts['exact_affine_normalizations']+=1
            D,C=W.derivation(H),W.gate(H,3)
            g={(1,0):F(1)}
            for r in range(ans['third_gate_depth']):
                assert not W.act(C,g),(u,V,A,r)
                g=W.act(D,g)
            obstruction=W.act(C,g)
            up={(i,0):F(v) for i,v in u.items()}
            vp={(i,0):F(v) for i,v in V.items()}
            expected=(U.scale(U.mul(U.deriv(up,2),U.power(U.deriv(vp,3),2)),-960*A**5)
                      if ans['third_gate_depth']==6 else
                      U.scale(U.mul(U.deriv(up,2),U.deriv(vp,4)),96*A**4))
            assert obstruction==expected and obstruction
            counts['sharp_depth_checks']+=1
            # Independently verify the transformed differential operator on monomials.
            from pure_quadratic_composition import comp
            for i,j in ((0,3),(1,2),(3,4),(4,1),(2,5)):
                f={(i,j):F(1)}
                transformed=U.add(U.mul(U.deriv(vp,3),U.deriv(f,0,3)),
                                  U.scale(U.mul(U.deriv(up,2),U.deriv(f,1,2)),-6*A))
                assert W.act(C,comp(f,Q))==comp(transformed,Q)
                counts['operator_identities']+=1
            records.append({'A':str(A),'u':[[i,str(v)]for i,v in sorted(u.items())],
                            'V':[[i,str(v)]for i,v in sorted(V.items())],
                            'dimension':2,'sharp_third_gate_depth':ans['third_gate_depth']})
    cert=determinant_certificate()
    for mutate in (lambda c:c.update(parameter_degree_bound=31),
                   lambda c:c.update(determinant='1'),
                   lambda c:c.update(evaluation_points=list(range(32))),
                   lambda c:c['rows'][0].__setitem__(0,1)):
        bad=copy.deepcopy(cert);mutate(bad)
        try:check_determinant_certificate(bad)
        except ValueError:counts['forgeries']+=1
        else:raise AssertionError('forged determinant certificate accepted')
    for u,V in (({3:1},{3:1}),({2:1},{2:1}),({1:1},{3:1})):
        assert classify(make(u,V)[0]) is None;counts['scope_rejections']+=1
    return {'status':'passed','checks':counts,'instances':records,
            'cubic_parameter_certificate':cert,'determinant_replay':determinant_result,
            'scope':'All polynomial nonlinear residual potentials for quadratic shears; combined with QC and oscillator theorems completes constant-quadratic families with deg u>=2.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',nargs='?')
    ap.add_argument('--classify',type=Path)
    ap.add_argument('--check-certificate',type=Path)
    args=ap.parse_args()
    if args.classify:
        from quadratic_frontier import decode
        rows=json.loads(args.classify.read_text())
        H=decode(rows['hamiltonian']if isinstance(rows,dict)else rows)
        result=classify(H)or{'proved':False,'status':'outside scope'}
    elif args.check_certificate:
        result=check_determinant_certificate(json.loads(args.check_certificate.read_text()))
    else:result=self_test()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
