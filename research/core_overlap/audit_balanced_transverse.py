#!/usr/bin/env python3
"""Symbolic and direct-operator checks for nonlinear shear compositions.

The symbolic ring below is independent of the branch's symbolic checker.
Direct PBW fixtures subsequently use the branch's established operator engine.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import sys


def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items(): out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}


def scale(p,c): return {e:v*c for e,v in p.items() if v*c}


def mul(*ps):
    out={(0,0,0):F(1)}
    for p in ps:
        nxt={}
        for e,c in out.items():
            for f,d in p.items():
                k=tuple(a+b for a,b in zip(e,f))
                nxt[k]=nxt.get(k,F(0))+c*d
        out={e:c for e,c in nxt.items() if c}
    return out


def const(c): return {} if not c else {(0,0,0):F(c)}
def var(i): return {tuple(int(i==j) for j in range(3)):F(1)}


def fall(p,r):
    return mul(*(add(p,const(-j)) for j in range(r)))


def t3(a,b,c,d):
    return add(*(scale(mul(fall(a,3-j),fall(b,j),fall(c,j),fall(d,3-j)),
                        (-1)**j*comb(3,j)) for j in range(4)))


def symbolic():
    mu,s,n=(var(i) for i in range(3))
    sm1=add(s,const(-1)); mm1=add(mu,const(-1))
    lhs=add(mul(s,t3(mu,mu,add(sm1,n),sm1)),
            mul(mu,t3(add(mm1,n),mm1,s,s)))
    rhs=mul(mu,s,add(s,scale(mu,-1)),add(s,mu,const(-3)),fall(n,3))
    assert lhs==rhs
    return {'identity':'mu*s*(s-mu)*(s+mu-3)*(n)_3',
            'expanded_nonzero_terms':len(lhs),'status':'passed'}


def operator_checks():
    root=Path(__file__).resolve().parents[2]
    sys.path.insert(0,str(root/'extensions'/'hamiltonian'))
    import weyl_receipts as W
    import check_two_root as T
    u={(0,0):F(2),(1,0):F(-1),(2,0):F(3),(3,0):F(2),(5,0):F(-1)}
    J=T.add({(1,1):1},u)
    n=0
    for mu in range(2,9):
        for s in range(1,9):
            H=T.add(T.power(J,mu),T.sc(T.power(J,mu-1),F(3)))
            v=T.add(u,{(0,0):F(3,mu)})
            A=T.add({(s,s):1},T.sc(T.mul({(s-1,s-1):1},v),s))
            image=W.act(W.gate(H,3),A)
            got={(q,p):c for(q,p),c in image.items() if p==mu+s-4}
            want={}
            if mu+s>=4:
                want=T.sc(T.mul({(mu+s-1,mu+s-4):1},T.dq(T.dq(T.dq(u)))),
                          mu*s*(s-mu)*(s+mu-3))
            assert got==want,(mu,s,got,want)
            n+=1
    # The complete quadratic sector, plus the first escaping stationary power.
    H=T.power(J,2)
    for A in ({(0,0):F(1)},J,H):
        assert W.act(W.derivation(H),A)=={}
        for k in range(3,T.degree(H)+1,2):
            assert W.act(W.gate(H,k),A)=={}
    first_escape=W.act(W.gate(H,3),T.power(J,3))
    assert first_escape
    composition_pairs=0
    u3=T.dq(T.dq(T.dq(u)))
    for mu in range(1,6):
        for s in range(1,6):
            got=W.act(W.gate(T.power(J,mu),3),T.power(J,s))
            coefficient=mu*s*(s-mu)*(s+mu-3)
            want={}
            if mu+s>=4:
                want=T.sc(T.mul(T.mul({(3,0):1},u3),T.power(J,mu+s-4)),coefficient)
            assert got==want,(mu,s)
            composition_pairs+=1
    return {'status':'passed','direct_coefficient_cases':n,
            'quadratic_sector_all_gates':True,'cubic_stationary_power_fails_T3':True,
            'composition_identity_pairs':composition_pairs}


if __name__=='__main__':
    print(json.dumps({'symbolic':symbolic(),'operators':operator_checks()},indent=2))
