#!/usr/bin/env python3
"""Exact PBW arithmetic and all-degree invariant-kernel receipt checker.

This is NOT a Groebner-basis or polynomial-PDE solver. Operators are in
Q[q,p]<dq,dp>, normally ordered q^a p^b dq^c dp^d; products mean composition,
with the right factor acting first. Standard library only, Python 3.10+.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse
import importlib.util
import json
import random


def tidy(x):
    return {tuple(k): F(v) for k, v in x.items() if v}


def add(*xs):
    out = {}
    for x in xs:
        for k, v in x.items():
            out[k] = out.get(k, F(0)) + v
    return tidy(out)


def scale(x, c):
    return tidy({k: v * c for k, v in x.items()})


def fall(n, k):
    return factorial(n) // factorial(n-k) if 0 <= k <= n else 0


def compose(A, B):
    out = {}
    for (a,b,c,d), x in A.items():
        for (e,f,g,h), y in B.items():
            for i in range(min(c,e)+1):
                for j in range(min(d,f)+1):
                    k = (a+e-i,b+f-j,c+g-i,d+h-j)
                    z = x*y*comb(c,i)*fall(e,i)*comb(d,j)*fall(f,j)
                    out[k] = out.get(k,F(0)) + z
    return tidy(out)


def op_power(A, n):
    if type(n) is not int or n < 0:
        raise ValueError('Operator iterate must be a nonnegative integer')
    ans = {(0,0,0,0): F(1)}
    while n:
        if n % 2:
            ans = compose(ans,A)
        n //= 2
        if n:
            A = compose(A,A)
    return ans


def act(A, G):
    out = {}
    for (a,b,c,d), x in A.items():
        for (e,f), y in G.items():
            if e >= c and f >= d:
                k = (a+e-c,b+f-d)
                out[k] = out.get(k,F(0)) + x*y*fall(e,c)*fall(f,d)
    return tidy(out)


def pder(G, c=0, d=0):
    return act({(0,0,c,d):F(1)},G)


def pmul(A,B):
    out = {}
    for (a,b),x in A.items():
        for (c,d),y in B.items():
            k=(a+c,b+d)
            out[k]=out.get(k,F(0))+x*y
    return tidy(out)


def lift(G,c=0,d=0):
    return {(a,b,c,d):v for (a,b),v in G.items()}


def derivation(H):
    return add(lift(pder(H,1),0,1),scale(lift(pder(H,0,1),1,0),-1))


def gate(H,k):
    return add(*(scale(lift(pder(H,k-j,j),j,k-j),(-1)**j*comb(k,j))
                 for j in range(k+1)))


def gates(H):
    return {k:C for k in range(3,max((a+b for a,b in H),default=0)+1,2)
            if (C:=gate(H,k))}


def read_terms(rows, width):
    out = {}
    for row in rows:
        if len(row) != width+1 or any(type(a) is not int or a < 0 for a in row[:-1]):
            raise ValueError('Invalid exponent row')
        if type(row[-1]) not in (int,str):
            raise ValueError('Coefficients must be integer or rational strings, never floats')
        k=tuple(row[:-1]); out[k]=out.get(k,F(0))+F(row[-1])
    return tidy(out)


def dump_terms(A):
    return [list(k)+[str(A[k])] for k in sorted(A)]


def receipt_sum(rows, generators):
    ans = {}
    for row in rows:
        i=row['generator']
        if type(i) is not int or not 0 <= i < len(generators):
            raise ValueError('Invalid generator index')
        ans=add(ans,compose(read_terms(row['left_multiplier'],4),generators[i]))
    return ans


def verify_certificate(cert):
    if cert.get('schema') != 'weyl-invariant-kernel-v1' or cert.get('field') != 'Q':
        raise ValueError('Unsupported certificate schema/field')
    H=read_terms(cert['hamiltonian'],2); D=derivation(H); C=gates(H)
    P=[read_terms(x,4) for x in cert['generators']]
    if len(cert['provenance']) != len(P) or len(cert['closure']) != len(P):
        raise ValueError('Every generator needs provenance and closure receipts')
    if set(cert['correction_containment']) != {str(k) for k in C}:
        raise ValueError('Correction receipt orders do not match all nonzero gates')
    for k,op in C.items():
        if op != receipt_sum(cert['correction_containment'][str(k)],P):
            raise ValueError(f'Failed correction containment for order {k}')
    for i,op in enumerate(P):
        ans={}
        for row in cert['provenance'][i]:
            k=row['gate_order']; n=row['iterate']
            if k not in C:
                raise ValueError('Unknown correction gate')
            ans=add(ans,compose(read_terms(row['left_multiplier'],4),
                                compose(C[k],op_power(D,n))))
        if ans != op:
            raise ValueError(f'Failed provenance for generator {i}')
        if compose(op,D) != receipt_sum(cert['closure'][i],P):
            raise ValueError(f'Failed right-D closure for generator {i}')
    return {'status':'passed','generators':len(P),'nonzero_gates':list(C),
            'claim':'The polynomial common kernel of these generators equals the full dynamic exact core in all degrees.',
            'limits':'This receipt does not compute a basis of that polynomial kernel or establish literature priority.'}


def example():
    # H=q^3, C3=6 dp^3, D=3q^2 dp. The exact core is ker dp^3.
    return {'schema':'weyl-invariant-kernel-v1','field':'Q',
            'hamiltonian':[[3,0,'1']], 'generators':[[[0,0,0,3,'1']]],
            'correction_containment':{'3':[{'generator':0,'left_multiplier':[[0,0,0,0,'6']]}]},
            'provenance':[[{'gate_order':3,'iterate':0,'left_multiplier':[[0,0,0,0,'1/6']]}]],
            'closure':[[{'generator':0,'left_multiplier':[[2,0,0,1,'3']]}]]}


def self_test(existing_engine=None):
    rng=random.Random(20261021)
    q={(1,0,0,0):F(1)};p={(0,1,0,0):F(1)}
    dq={(0,0,1,0):F(1)};dp={(0,0,0,1):F(1)};one={(0,0,0,0):F(1)}
    assert add(compose(dq,q),scale(compose(q,dq),-1))==one
    assert add(compose(dp,p),scale(compose(p,dp),-1))==one
    assert compose(dq,p)==compose(p,dq) and compose(dp,q)==compose(q,dp)
    for _ in range(200):
        A=tidy({tuple(rng.randrange(3) for _ in range(4)):rng.randrange(-3,4) for _ in range(3)})
        B=tidy({tuple(rng.randrange(3) for _ in range(4)):rng.randrange(-3,4) for _ in range(3)})
        G=tidy({(rng.randrange(6),rng.randrange(6)):rng.randrange(-4,5) for _ in range(4)})
        assert act(compose(A,B),G)==act(A,act(B,G))
    fixtures=[]
    for _ in range(40):
        H=tidy({(a:=rng.randrange(8),rng.randrange(8-a)):rng.randrange(-3,4) for _ in range(4)})
        G=tidy({(rng.randrange(7),rng.randrange(7)):rng.randrange(-4,5) for _ in range(4)})
        for k in (1,3,5):
            direct=add(*(scale(pmul(pder(H,k-j,j),pder(G,j,k-j)),(-1)**j*comb(k,j)) for j in range(k+1)))
            assert act(gate(H,k),G)==direct
        assert act(derivation(H),G)==act(gate(H,1),G)
        fixtures.append((H,G))
    assert verify_certificate(example())['status']=='passed'
    zero={'schema':'weyl-invariant-kernel-v1','field':'Q','hamiltonian':[],
          'generators':[],'correction_containment':{},'provenance':[],'closure':[]}
    assert verify_certificate(zero)['status']=='passed'
    mutations=[]
    broken=example();broken['closure'][0][0]['left_multiplier'][0][-1]='2';mutations.append(broken)
    broken=example();broken['provenance'][0][0]['left_multiplier'][0][-1]='1/5';mutations.append(broken)
    broken=example();broken['correction_containment']['3'][0]['left_multiplier'][0][-1]='5';mutations.append(broken)
    for broken in mutations:
        try:
            verify_certificate(broken)
        except ValueError:
            pass
        else:
            raise AssertionError('False operator receipt accepted')
    independent=0
    if existing_engine:
        spec=importlib.util.spec_from_file_location('existing_moyal_engine',existing_engine)
        E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
        for H,G in fixtures:
            expected={}
            for k in range(1,max((a+b for a,b in H),default=0)+1,2):
                z=scale(act(gate(H,k),G),F((-1)**((k-1)//2),2**(k-1)*factorial(k)))
                if z:expected[k-1]=z
            assert E.moyal(H,G)==expected
            independent+=1
    return {'status':'passed','pbw_commutation_checks':4,'composition_action_cases':200,
            'gate_definition_cases':120,'hamiltonian_derivation_cases':40,
            'valid_all_degree_receipts':2,'false_operator_receipts_rejected':3,
            'existing_direct_star_engine_cases':independent,
            'implemented':'Exact operator arithmetic and receipt replay only; no Groebner discovery backend.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',type=Path)
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--existing-engine',type=Path)
    ap.add_argument('--write-example',type=Path)
    args=ap.parse_args();out={}
    if args.write_example:
        args.write_example.write_text(json.dumps(example(),indent=2)+'\n')
        out['example_written']=str(args.write_example)
    if args.self_test:
        out['self_test']=self_test(args.existing_engine)
    if args.check:
        out['certificate']=verify_certificate(json.loads(args.check.read_text()))
    if not out:ap.error('Choose --self-test, --check or --write-example')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
