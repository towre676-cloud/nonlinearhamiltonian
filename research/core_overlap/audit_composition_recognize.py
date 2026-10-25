#!/usr/bin/env python3
"""Exact recognizer for the balanced-transverse nonlinear-composition family.

Input coordinates must have pure total top c*q^d.  A successful recognition
proves H=P((q+gamma)*p+u(q+gamma)), deg(u)>=3, deg(P)>=2.  Failure returns
None and makes no claim about the Hamiltonian's core.  No optional symbolic
or numerical library is used.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import random
import sys


def tidy(p): return {e:F(c) for e,c in p.items() if c}


def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items(): out[e]=out.get(e,F(0))+c
    return tidy(out)


def scale(p,c): return tidy({e:v*c for e,v in p.items()})


def mul(a,b):
    out={}
    for (i,j),c in a.items():
        for (k,l),d in b.items(): out[(i+k,j+l)]=out.get((i+k,j+l),F(0))+c*d
    return tidy(out)


def power(a,n):
    out={(0,0):F(1)}
    for _ in range(n): out=mul(out,a)
    return out


def shift_q(H,gamma):
    out={}
    for (i,j),c in H.items():
        for k in range(i+1):
            out[(k,j)]=out.get((k,j),F(0))+c*comb(i,k)*gamma**(i-k)
    return tidy(out)


def ser(p): return {f'{i},{j}':str(c) for (i,j),c in sorted(p.items())}


def parse(p): return {tuple(map(int,e.split(','))):F(c) for e,c in p.items()}


def recognize(H):
    """Return an exact SC theorem result, or None. H keys are (q_exp,p_exp)."""
    H=tidy(H)
    if not H: return None
    d=max(i+j for i,j in H)
    if d<3 or {(i,j) for i,j in H if i+j==d}!={(d,0)}:
        return None
    mu=max(j for i,j in H)
    if mu<2: return None
    phi={i:c for (i,j),c in H.items() if j==mu}
    if max(phi)!=mu: return None
    c=phi[mu]
    gamma=phi.get(mu-1,F(0))/(mu*c)
    if any(phi.get(i,F(0))!=c*comb(mu,i)*gamma**(mu-i) for i in range(mu+1)):
        return None
    # In the new coordinate t=q+gamma, substitute q=t-gamma.
    Ht=shift_q(H,-gamma)
    B={i:v for (i,j),v in Ht.items() if j==mu-1}
    if any(i<mu-1 for i in B): return None
    u={i-mu+1:v/(mu*c) for i,v in B.items()}
    u.pop(0,None)  # This constant is absorbed by the coefficients of P.
    u={i:v for i,v in u.items() if v}
    if not u or max(u)<3: return None
    Jt=add({(1,1):F(1)},{(i,0):v for i,v in u.items()})
    residual=Ht
    coefficients=[F(0)]*(mu+1)
    for j in range(mu,-1,-1):
        part={i:v for (i,k),v in residual.items() if k==j}
        if any(i!=j for i in part): return None
        a=part.get(j,F(0))
        coefficients[j]=a
        residual=add(residual,scale(power(Jt,j),-a))
    if residual: return None
    J=shift_q(Jt,gamma)
    return {'route':'SC','proved':True,
            'core':'span{1, H, J}' if mu==2 else 'span{1, H}',
            'core_dimension':3 if mu==2 else 2,
            'active_part':'0 (all stationary)',
            'J':ser(J),'J_is_core':mu==2,
            'composition_coefficients':[str(a) for a in coefficients],
            'gamma':str(gamma),'u':{str(i):str(v) for i,v in sorted(u.items())},
            'degree_composition':mu,'degree_shear':max(u)}


def check_witness(H,result):
    """Independently replay the finite composition identity from a result."""
    if result is None: return False
    J=parse(result['J'])
    rebuilt={}
    for j,a in enumerate(result['composition_coefficients']):
        rebuilt=add(rebuilt,scale(power(J,j),F(a)))
    return rebuilt==tidy(H)


def self_test():
    root=Path(__file__).resolve().parents[2]
    sys.path.insert(0,str(root/'extensions'/'hamiltonian'))
    import weyl_receipts as W
    rng=random.Random(238901)
    successful=rejected=stationary_gate_cases=0
    for mu in range(2,6):
        for n in range(3,7):
            gamma=F(rng.randint(-3,3),rng.choice((1,2,3)))
            u={(i,0):F(rng.randint(-2,2)) for i in range(n)}
            u[(n,0)]=F(rng.choice((-2,-1,1,2)))
            J0=add({(1,1):F(1)},u)
            J=shift_q(J0,gamma)
            coefficients=[F(rng.randint(-2,2)) for _ in range(mu)]
            coefficients.append(F(rng.choice((-2,-1,1,2))))
            H={}
            for j,a in enumerate(coefficients): H=add(H,scale(power(J,j),a))
            result=recognize(H)
            assert result and result['degree_composition']==mu,(mu,n,result)
            assert result['degree_shear']==n and check_witness(H,result)
            Jr=parse(result['J'])
            assert W.act(W.derivation(H),Jr)=={}
            if mu==2:
                for k in range(3,max(i+j for i,j in H)+1,2):
                    assert W.act(W.gate(H,k),Jr)=={}
                    stationary_gate_cases+=1
            else:
                assert W.act(W.gate(H,3),Jr)!={}
            successful+=1
            # A nonconstant p-free perturbation leaves the prospective shear
            # coefficient unchanged, so failure is certified by reconstruction.
            bad=add(H,{(1,0):F(7)})
            assert recognize(bad) is None
            rejected+=1
    for H in ({(2,2):1,(6,0):1}, # balanced transverse, not a composition
              {(2,2):1,(4,1):2,(6,0):1,(1,0):1},
              {(2,2):1,(3,1):2,(4,0):1}, # quadratic shear excluded
              {(3,1):1,(7,0):1},         # unequal transverse excluded
              {(7,0):1}):
        assert recognize(H) is None
        rejected+=1
    return {'status':'passed','random_compositions':successful,
            'nonmatching_or_excluded_cases':rejected,
            'stationary_quadratic_gate_checks':stationary_gate_cases}


if __name__=='__main__':
    print(json.dumps(self_test(),indent=2))
