#!/usr/bin/env python3
"""Exact stdlib replay for S010, including a quadratic-field Jordan point."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import json

HERE=Path(__file__).resolve().parent
checks=[];certificates={}
def check(name,detail):checks.append(dict(id='S010',name=name,status='passed',detail=detail))
def clean(p):
    while len(p)>1 and p[-1]==0:p.pop()
    return p
def pa(a,b):return clean([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def ps(a,k):return clean([x*k for x in a])
def pdiff(a,b):return pa(a,ps(b,-1))
def pm(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return clean(c)
def pder(a):return clean([i*a[i] for i in range(1,len(a))] or [0])
def pval(a,x):
    out=0
    for v in reversed(a):out=out*x+v
    return out
def pprod(items):
    out=[F(1)]
    for p in items:out=pm(out,p)
    return out
def zero(n):return [[F(0) for j in range(n)] for i in range(n)]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def ma(a,b):return [[x+y for x,y in zip(row,col)] for row,col in zip(a,b)]
def ms(a,k):return [[x*k for x in row] for row in a]
def rank(a):
    a=[row[:] for row in a];i=0
    for j in range(len(a[0])):
        pivot=next((k for k in range(i,len(a)) if a[k][j]!=0),None)
        if pivot is None:continue
        a[i],a[pivot]=a[pivot],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i
def one_magnon(sites):
    n=len(sites);Hs=[]
    for i in range(n):
        H=zero(n)
        for j in range(n):
            if i==j:continue
            O=eye(n);O=ms(O,F(1,2))
            O[i][i]=O[j][j]=F(-1,2);O[i][j]=O[j][i]=F(1)
            H=ma(H,ms(O,1/(sites[i]-sites[j])))
        Hs.append(H)
    E0=[sum(F(1,2)/(sites[i]-sites[j]) for j in range(n) if j!=i) for i in range(n)]
    return Hs,E0

def oper_certificate(sites,w,E):
    p=pprod([[-z,1] for z in sites]);h=[-w,1]
    assert pval(pder(p),w)==0 and pval(p,w)!=0
    N=pdiff(ps(pm(pder(p),h),F(1,2)),p);D=pm(p,h)
    actual=pa(pdiff(pm(N,N),pm(pder(N),D)),pm(N,pder(D)))
    expected=[0]
    for i,z in enumerate(sites):
        removed=pprod([[-zz,1] for j,zz in enumerate(sites) if j!=i])
        expected=pa(expected,ps(pm(removed,removed),F(3,4)))
        expected=pa(expected,ps(pm(p,removed),E[i]))
    residual=pdiff(pm(actual,pm(p,p)),pm(expected,pm(D,D)))
    assert residual==[0]
    q1=h;q2=[-pval(p,w)];power=[F(1)];der=p
    for m in range(1,len(p)):
        power=pm(power,h);der=pder(der)
        if m>=2:q2=pa(q2,ps(power,pval(der,w)/(factorial(m)*(m-1))))
    ode_residuals=[]
    for q in [q1,q2]:
        r=pa(pdiff(ps(pm(pm(p,p),pder(pder(q))),4),ps(pm(pm(p,pder(p)),pder(q)),4)),pm(pdiff(pdiff(ps(pm(pder(p),pder(p)),3),ps(pm(p,pder(pder(p))),2)),ps(expected,4)),q))
        assert r==[0];ode_residuals.append([str(x) for x in r])
    wronskian_num=pdiff(pm(q1,pder(q2)),pm(pder(q1),q2))
    assert wronskian_num==p
    return {'potential_residual':[str(x) for x in residual],'ODE_residuals':ode_residuals,'p':[str(x) for x in p],'q1':[str(x) for x in q1],'q2':[str(x) for x in q2],'Wronskian':'1'}

examples=[([F(0),F(1)],[F(1,2)]),([F(0),F(1),F(8,3)],[F(4,9),F(2)]),([F(-7),F(-1),F(1),F(7)],[F(-5),F(0),F(5)])]
for sites,roots in examples:
    n=len(sites);Hs,E0=one_magnon(sites);u=[F(1)]*n
    basis=[u];projectors=[ms([[F(1) for _ in range(n)] for _ in range(n)],F(1,n))]
    spectra=[E0];opers=[]
    for i,H in enumerate(Hs):assert mv(H,u)==[E0[i]]*n
    for w in roots:
        v=[1/(w-z) for z in sites];assert sum(v)==0
        E=[E0[i]+v[i] for i in range(n)]
        for H,lam in zip(Hs,E):assert mv(H,v)==[lam*x for x in v]
        P=pprod([[-z,1] for z in sites]);norm=sum(x*x for x in v)
        assert norm==-pval(pder(pder(P)),w)/pval(P,w) and norm>0
        proj=[[x*y/norm for y in v] for x in v]
        for prev in basis:assert sum(x*y for x,y in zip(prev,v))==0
        basis.append(v);projectors.append(proj);spectra.append(E)
        opers.append(oper_certificate(sites,w,E))
    assert rank(basis)==n
    total=zero(n)
    for P in projectors:total=ma(total,P)
    assert total==eye(n)
    for i,H in enumerate(Hs):
        reconstructed=zero(n)
        for P,E in zip(projectors,spectra):reconstructed=ma(reconstructed,ms(P,E[i]))
        assert reconstructed==H
    certificates['real_sites_'+str(n)]={'sites':[str(x) for x in sites],'critical_roots':[str(x) for x in roots],'joint_spectra':[[str(x) for x in E] for E in spectra],'basis_rank':n,'oper_certificates':opers}
    check('Complete rational '+str(n)+'-site one-magnon sector','Exact matrices, orthogonal eigenbasis, projector resolution of identity and all Hamiltonian reconstructions passed. Every critical-root scalar equation has a zero potential residual, two zero ODE residuals and Wronskian one.')

# Work exactly in Q(tau), tau²−tau+1=0, to certify the exceptional Jordan locus.
class K:
    def __init__(self,a=0,b=0):
        if isinstance(a,K):self.a,self.b=a.a,a.b
        else:self.a,self.b=F(a),F(b)
    def __add__(self,o):
        o=K(o);return K(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return K(-self.a,-self.b)
    def __sub__(self,o):return self+-K(o)
    def __rsub__(self,o):return K(o)+-self
    def __mul__(self,o):
        o=K(o);return K(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a+self.b*o.b)
    __rmul__=__mul__
    def inv(self):
        norm=self.a*self.a+self.a*self.b+self.b*self.b
        if not norm:raise ZeroDivisionError
        return K((self.a+self.b)/norm,-self.b/norm)
    def __truediv__(self,o):return self*K(o).inv()
    def __rtruediv__(self,o):return K(o)*self.inv()
    def __eq__(self,o):
        o=K(o);return self.a==o.a and self.b==o.b
    def __ne__(self,o):return not self==o
    def __str__(self):return str(self.a)+' + ('+str(self.b)+')tau'
    def __repr__(self):return str(self)
tau=K(0,1);assert tau*tau-tau+1==0
sites=[K(0),K(1),tau];w=(1+tau)/3
Hs,E0=one_magnon(sites);a=[1/(w-z) for z in sites];vprime=[-x*x for x in a];u=[K(1)]*3
assert sum(a)==0 and sum(x*x for x in a)==0
E=[E0[i]+a[i] for i in range(3)]
for i,H in enumerate(Hs):
    assert mv(H,a)==[E[i]*x for x in a]
    assert mv(H,vprime)==[E[i]*vprime[j]-a[i]*a[i]*a[j] for j in range(3)]
    assert a[i]*a[i]!=0
    for J in Hs:assert mm(H,J)==mm(J,H)
assert rank([u,a,vprime])==3
exceptional_oper=oper_certificate(sites,w,E)
certificates['exceptional_three_site']={'field':'Q(tau), tau²−tau+1=0','sites':[str(x) for x in sites],'coalesced_root':str(w),'eigenvalues':[str(x) for x in E],'eigenvector':[str(x) for x in a],'generalized_vector':[str(x) for x in vprime],'generalized_equation':'(H_i−E_i)v′=−a_i²v','rank_uniform_eigen_generalized':3,'oper':exceptional_oper}
check('Exact exceptional three-site Jordan point','In Q(tau), tau²−tau+1=0, the two critical roots coalesce. B=B′=0, each generalized-eigenvector equation holds with a nonzero coefficient, and (u,v,v′) has rank3. Hamiltonians commute; the surviving scalar equation retains zero residuals and Wronskian1.')

# Import the complete full-tensor certificate by independently reading and
# verifying the generated matrices/eigenbasis (without running its producer).
full=json.loads(HERE.joinpath('gaudin_three_site_certificate.json').read_text())
Hs=[[[F(x) for x in row] for row in H] for H in full['Hamiltonians']]
basis=[[F(x) for x in row] for row in full['eigenbasis']]
specs=[[F(x) for x in full['vacuum_joint_eigenvalues']]]*4
specs += [[F(x) for x in full['two_spin_half_joint_eigenvalues'][0]]]*2
specs += [[F(x) for x in full['two_spin_half_joint_eigenvalues'][1]]]*2
assert rank(basis)==8
for v,E in zip(basis,specs):
    for H,lam in zip(Hs,E):assert mv(H,v)==[lam*x for x in v]
check('Independent replay of the full eight-dimensional rational example','Read the published rational 8×8 matrices and all eight vectors from the separate certificate, recomputed all joint eigenvector equations, and verified rank8. This independently replays the quartet plus two doublets certificate.')

out={'checks':checks,'certificates':certificates,'scope':'All arithmetic checks in this supplemental verifier are exact rational or exact quadratic-field calculations. The arbitrary-n result is proved in S010, not inferred from finite examples.'}
HERE.joinpath('supplement_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'id':'S010','checks':len(checks),'passed':True,'exact_rational_examples':[2,3,4],'exceptional_field':'Q(tau), tau²−tau+1=0'}))
