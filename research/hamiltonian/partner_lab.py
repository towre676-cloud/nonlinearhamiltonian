#!/usr/bin/env python3
"""Exact polynomial partner CLI. Python 3.10+, standard library only."""
import argparse,ast,json,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'independent'));import engine as E
sys.path.insert(0,str(ROOT/'monomial'));import classification as M

def parse(text):
    tree=ast.parse(text.replace('^','**'),mode='eval')
    def f(n):
        if isinstance(n,ast.Expression):return f(n.body)
        if isinstance(n,ast.Constant) and type(n.value) is int:return E.monomial(0,0,n.value)
        if isinstance(n,ast.Name) and n.id in ['q','p']:return E.monomial(int(n.id=='q'),int(n.id=='p'))
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):return E.scale(f(n.operand),-1 if isinstance(n.op,ast.USub) else 1)
        if isinstance(n,ast.BinOp):
            if isinstance(n.op,ast.Add):return E.add(f(n.left),f(n.right))
            if isinstance(n.op,ast.Sub):return E.add(f(n.left),E.scale(f(n.right),-1))
            if isinstance(n.op,ast.Mult):return E.multiply(f(n.left),f(n.right))
            if isinstance(n.op,ast.Div):
                den=f(n.right)
                if set(den)!={(0,0)}:raise ValueError('Denominator must be a nonzero rational constant')
                return E.scale(f(n.left),1/den[(0,0)])
            if isinstance(n.op,ast.Pow) and isinstance(n.right,ast.Constant) and type(n.right.value) is int and 0<=n.right.value<=100:return E.power(f(n.left),n.right.value)
        raise ValueError('Use integers, rational constants, q,p,+,-,*,/ and nonnegative integer powers up to100')
    return f(tree)

def classify(a,b):
    if min(a,b)<0:raise ValueError('Exponents must be nonnegative')
    if a+b<=2:return {'hamiltonian':[a,b],'scope':'complete','exact_basis':'all monomials','active_quotient':'zero for constant H; infinite for nonconstant H'}
    if a==0 or b==0:return {'hamiltonian':[a,b],'scope':'complete','exact_basis':'all q^c p^d with '+('c<=2' if a==0 else 'd<=2'),'active_quotient':'infinite dimensional'}
    if min(a,b)==1:
        m=max(a,b);swap=b==1
        condition='c<=1, any d; and '
        if m==2:condition+='d=0, any c>=2'
        elif m==3:condition+='c=3d+2, d>=0'
        else:condition+='(c,d)=(2,0)'+('; plus(3,'+str((m-2)//3)+')' if (m-2)%3==0 else '')
        return {'hamiltonian':[a,b],'scope':'complete','exact_basis_condition':condition,'exchange_c_d':swap,'active_quotient':'infinite dimensional','dynamic_core':'polynomials affine in '+('p' if swap else 'q')}
    if a==b:
        m=a
        desc='c=0 or d=0 or c=d' if m==2 else 'c=d or c+d<=2'+(' or(c,d)=(1,11),(11,1)' if m==3 else '')
        return {'hamiltonian':[a,b],'scope':'complete','exact_basis_condition':desc,'active_quotient_dimension':'infinite' if m==2 else 6 if m==3 else 4}
    return M.classify_unequal(a,b)

def core_demo():
    H=parse('q*p^3+q^2');Y=parse('q+p^3/2')
    basis=[parse('1'),parse('p'),parse('p^2'),Y,E.multiply(parse('p'),Y),H];stages=[]
    while True:
        stages.append({'dimension':len(basis),'basis':[E.serialize(E.primitive(x)) for x in basis]})
        images=[E.poisson(H,x) for x in basis];keys=sorted({k for x in basis+images for k in x});m=len(basis)
        matrix=[[x.get(k,Fraction(0)) for x in images]+[-x.get(k,Fraction(0)) for x in basis] for k in keys]
        relations=E.nullspace(matrix,2*m);new=[E.add(*(E.scale(B,v) for B,v in zip(basis,x[:m]))) for x in relations]
        new=[x for x in new if x]
        if len(new)==len(basis):break
        basis=new
    assert [x['dimension'] for x in stages]==[6,4,2]
    assert all(not E.defects(H,x) for x in basis)
    return {'scope':'global dynamical core, using the proved all-degree E2 reduction; no projection of the Poisson action','stages':stages,'stable':True,'answer':'span{1,H}'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    for name in ['bracket','kernel']:
        p=sub.add_parser(name);p.add_argument('--H',required=True)
        if name=='bracket':p.add_argument('--G',required=True)
        else:p.add_argument('--degree',required=True,type=int)
    p=sub.add_parser('monomial');p.add_argument('--a',type=int,required=True);p.add_argument('--b',type=int,required=True)
    p=sub.add_parser('flow');p.add_argument('--r',type=int,default=0);p.add_argument('--steps',type=int,default=4)
    sub.add_parser('core-demo')
    args=ap.parse_args()
    try:
        if args.command=='core-demo':out=core_demo()
        elif args.command=='monomial':out=classify(args.a,args.b)
        elif args.command=='bracket':
            H,G=parse(args.H),parse(args.G);out={'H':E.serialize(H),'G':E.serialize(G),'poisson':E.serialize(E.poisson(H,G)),'moyal':E.serialize_series(E.moyal(H,G)),'exact':E.exact_partner(H,G)}
        elif args.command=='kernel':
            if not 0<=args.degree<=60:raise ValueError('Degree must be between0and60')
            H=parse(args.H);basis=E.homogeneous_kernel(H,args.degree);out={'H':E.serialize(H),'degree':args.degree,'scope':'all homogeneous partners of the requested degree; not a complete arbitrary-degree classification','dimension':len(basis),'basis':[E.serialize(E.primitive(x)) for x in basis]}
        else:
            if not 0<=args.r<=8 or not 0<=args.steps<=40:raise ValueError('Use0<=r<=8 and0<=steps<=40')
            H=E.monomial(1,3);G=E.monomial(3*args.r+2,args.r);quantum={0:G};classical=G;out=[]
            for n in range(args.steps+1):
                out.append({'action':n,'classical':E.serialize(classical),'quantum':E.serialize_series(quantum),'agree':quantum==({0:classical} if classical else {})});quantum=E.formal_action(H,quantum);classical=E.poisson(H,classical)
        print(json.dumps(out,ensure_ascii=False,indent=2))
    except (ValueError,SyntaxError,ZeroDivisionError) as e:ap.error(str(e))
if __name__=='__main__':main()
