#!/usr/bin/env python3
"""Exact tree-flow/phasor certificates and bounded floating checks for S009."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import math,json

checks=[]
def record(name,test,detail):
    assert test,(name,detail)
    checks.append(dict(id='S009',name=name,status='pass',detail=detail))
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a):return [list(c) for c in zip(*a)]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def rank(a):
    a=[list(map(F,row)) for row in a];r=0
    for j in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];d=a[r][j];a[r]=[x/d for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r
def determinant(a):
    a=[list(map(F,row)) for row in a];d=F(1)
    for j in range(len(a)):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None:return F(0)
        if p!=j:a[j],a[p]=a[p],a[j];d=-d
        pivot=a[j][j];d*=pivot
        for i in range(j+1,len(a)):
            z=a[i][j]/pivot
            for k in range(j+1,len(a)):a[i][k]-=z*a[j][k]
            a[i][j]=F(0)
    return d
def incidence(n,edges):
    B=[[F(0) for _ in edges] for _ in range(n)]
    for j,(u,v) in enumerate(edges):B[u][j]=-1;B[v][j]=1
    return B
def cut_component(n,edges,omit):
    head=edges[omit][1];adj=[[] for _ in range(n)]
    for j,(u,v) in enumerate(edges):
        if j!=omit:adj[u].append(v);adj[v].append(u)
    seen={head};todo=[head]
    while todo:
        i=todo.pop()
        for j in adj[i]:
            if j not in seen:seen.add(j);todo.append(j)
    return seen
def lap(B,w):return [[sum(B[i][e]*w[e]*B[j][e] for e in range(len(w))) for j in range(len(B))] for i in range(len(B))]
def c_mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def c_conj(z):return(z[0],-z[1])
def phasors(n,edges,edge_z):
    z=[None]*n;z[0]=(F(1),F(0));todo=[0]
    while todo:
        i=todo.pop()
        for e,(u,v) in enumerate(edges):
            if i==u and z[v] is None:z[v]=c_mul(z[u],edge_z[e]);todo.append(v)
            if i==v and z[u] is None:z[u]=c_mul(z[v],c_conj(edge_z[e]));todo.append(u)
    assert all(v is not None for v in z)
    return z
def eigenvalues_symmetric(a):
    a=[[float(x) for x in row] for row in a];n=len(a)
    for _ in range(200):
        p,q=max(((i,j) for i in range(n) for j in range(i+1,n)),key=lambda ij:abs(a[ij[0]][ij[1]]))
        if abs(a[p][q])<1e-14:break
        angle=.5*math.atan2(2*a[p][q],a[q][q]-a[p][p]);c=math.cos(angle);s=math.sin(angle)
        app,aqq,apq=a[p][p],a[q][q],a[p][q]
        for k in range(n):
            if k not in [p,q]:
                akp,akq=a[k][p],a[k][q]
                a[k][p]=a[p][k]=c*akp-s*akq
                a[k][q]=a[q][k]=s*akp+c*akq
        a[p][p]=c*c*app-2*c*s*apq+s*s*aqq
        a[q][q]=s*s*app+2*c*s*apq+c*c*aqq
        a[p][q]=a[q][p]=0
    return sorted(a[i][i] for i in range(n))

edges=[(0,1),(1,2),(1,3)];B=incidence(4,edges)
K=[F(5,6),F(13,15),F(1,2)];f=[F(1,2),F(1,3),F(0)];b=[F(-1,2),F(1,6),F(1,3),F(0)]
s=[F(3,5),F(5,13),F(0)];c=[F(4,5),F(12,13),F(1)]
record('Rational incidence and cut-flow certificate',mv(B,f)==b and sum(b)==0 and all(sum(b[i] for i in cut_component(4,edges,e))==f[e] for e in range(3)),{'flows':list(map(str,f)),'frequencies_centered':list(map(str,b))})
record('Exact sine-cosine feasibility',all(K[e]*s[e]==f[e] and s[e]**2+c[e]**2==1 and c[e]>0 and abs(s[e])<F(4,5) for e in range(3)),{'sines':list(map(str,s)),'cosines':list(map(str,c)),'cohesive_sine_bound':'4/5'})
z=phasors(4,edges,list(zip(c,s)))
z_expected=[(F(1),F(0)),(F(4,5),F(3,5)),(F(33,65),F(56,65)),(F(4,5),F(3,5))]
record('Exact rational node phasors',z==z_expected and all(x*x+y*y==1 for x,y in z),{'phasors':[[str(x),str(y)] for x,y in z]})
w=[K[e]*c[e] for e in range(3)];L=lap(B,w)
cofactors=[]
for delete in range(4):cofactors.append(determinant([[L[i][j] for j in range(4) if j!=delete] for i in range(4) if i!=delete]))
eigs=eigenvalues_symmetric(L)
record('Positive tree Hessian certificate',rank(L)==3 and mv(L,[1,1,1,1])==[0]*4 and all(x==F(4,15) for x in cofactors) and .5-1e-12<=eigs[1]<=2/3+1e-12,{'weights':list(map(str,w)),'principal_cofactors':list(map(str,cofactors)),'floating_eigenvalues':eigs,'exact_rate_bounds':['1/2','2/3']})

# Every sign pattern produces a different rational phase assignment and the correct Hessian inertia.
V=[[-1,-1,-1],[1,0,0],[0,1,0],[0,0,1]];T=mm(tr(B),V)
assert determinant(T)!=0
seen=set();index_counts={q:0 for q in range(4)};branches=[]
for signs in product([-1,1],repeat=3):
    cc=[signs[e]*c[e] for e in range(3)]
    zz=phasors(4,edges,list(zip(cc,s)));seen.add(tuple(zz))
    ee=[c_mul(zz[v],c_conj(zz[u])) for u,v in edges]
    assert all(ee[e]==(cc[e],s[e]) and K[e]*ee[e][1]==f[e] for e in range(3))
    ww=[K[e]*cc[e] for e in range(3)];H=lap(B,ww)
    restricted=mm(mm(tr(V),H),V)
    diagonal=[[ww[i] if i==j else F(0) for j in range(3)] for i in range(3)]
    assert restricted==mm(mm(tr(T),diagonal),T)
    ev=eigenvalues_symmetric(H);q=sum(x<0 for x in signs)
    assert sum(x<-1e-9 for x in ev)==q and sum(x>1e-9 for x in ev)==3-q and rank(H)==3
    index_counts[q]+=1;branches.append({'cosine_signs':list(signs),'unstable_index':q})
record('Complete eight-branch Morse classification',len(seen)==8 and index_counts=={0:1,1:3,2:3,3:1},{'branch_count':len(seen),'index_counts':index_counts,'branches':branches,'scope':'Exact phase/flow and congruence identities; floating eigenvalues independently confirm the analytic inertia proof.'})

# Rational Pythagorean parametrization approaches flow capacity without irrational certificate data.
boundary=[]
for t in [F(0),F(1,2),F(3,4),F(9,10),F(99,100),F(999,1000)]:
    q=t/(1+t*t);a=(1-t*t)/(2*(1+t*t))
    assert q*q+a*a==F(1,4) and a>0
    ww=[F(2,3),F(4,5),a];H=lap(B,ww);ev=eigenvalues_symmetric(H);rate=ev[1]
    v=[F(-1,4),F(-1,4),F(-1,4),F(3,4)]
    norm=sum(x*x for x in v);energy=sum(x*y for x,y in zip(v,mv(H,v)))
    assert energy==a and norm==F(3,4) and all(x>=a for x in ww)
    assert float(a)-1e-11<=rate<=float(F(4,3)*a)+1e-11
    assert 1-1e-9<=rate/float(a)<=4/3+1e-9
    boundary.append({'t':str(t),'flow_q':str(q),'restoring_weight':str(a),'edge_sensitivity':str(1/a),'lambda2_float':rate,'lambda2_times_sensitivity':rate/float(a)})
record('Capacity sensitivity and critical-slowing bounds',True,{'samples':boundary,'proof_scope':'The exact Rayleigh certificate and coefficient lower bound prove the stated bounds; the eigenvalue calculation is a separate numerical check.'})

# Relative-output kernel and an absolute-center sensor with additional invisible modes.
L0=lap(B,[F(1)]*3);A=[[-x for x in row] for row in L0]
C=tr(B);O=[];block=C
for k in range(4):O+=block;block=mm(block,A)
anchor=[F(0),F(1),F(0),F(0)];Ocenter=[];row=[anchor]
for k in range(4):Ocenter+=row;row=mm(row,A)
v=[1,0,-1,0]
record('Exact relative and center-only observability ranks',rank(C)==rank(O)==3 and rank(C+[anchor])==4 and rank(Ocenter)==2 and mv(L0,v)==v and sum(x*y for x,y in zip(anchor,v))==0,{'all_edge_rank':rank(O),'edges_plus_anchor_rank':rank(C+[anchor]),'center_only_rank':rank(Ocenter),'center_only_unobservable_dimension':2})

errors=[]
for a0 in [.2,math.pi/6,math.pi/3]:
    for t in [0,.2,1,3,10]:
        q0=math.tan(a0/2)*math.exp(-t);a=2*math.atan(q0);adot=-2*q0/(1+q0*q0)
        theta=[a,0,-a,0];rhs=[0.0]*4
        for u,v in edges:
            flow=math.sin(theta[v]-theta[u]);rhs[u]+=flow;rhs[v]-=flow
        expected=[adot,0,-adot,0];errors.append(max(abs(x-y) for x,y in zip(rhs,expected)))
        assert rhs[1]==0 and theta[1]==0
record('Exact-form nonlinear center blindness replay',max(errors)<1e-14,{'maximum_ODE_residual_float':max(errors),'trajectory':'(a(t),0,−a(t),0), a(t)=2 atan(tan(a0/2)e^(−t))','center_output':'identically zero, equal to the synchronized equilibrium output','scope':'Residual samples replay the closed-form solution whose all-time identity is proved in text.'})

# All labeled trees through five nodes: independently recover known edge flows from cut sums.
def decode_prufer(n,seq):
    degree=[1]*n
    for x in seq:degree[x]+=1
    edges=[]
    for x in seq:
        leaf=next(i for i,d in enumerate(degree) if d==1)
        edges.append((leaf,x));degree[leaf]-=1;degree[x]-=1
    left=[i for i,d in enumerate(degree) if d==1];edges.append(tuple(left));return edges
tree_count=0;case_count=0
for n in range(2,6):
    for seq in product(range(n),repeat=n-2):
        ee=decode_prufer(n,seq);BB=incidence(n,ee);assert rank(BB)==n-1;tree_count+=1
        for shift in [0,1]:
            ff=[F(((e+shift)%3)-1,5) for e in range(n-1)];bb=mv(BB,ff)
            recovered=[sum(bb[i] for i in cut_component(n,ee,e)) for e in range(n-1)]
            assert recovered==ff and sum(bb)==0;case_count+=1
record('Finite exhaustive cut-flow replay',tree_count==145 and case_count==290,{'labeled_trees_n2_through_n5':tree_count,'rational_flow_cases':case_count,'scope':'Finite independent combinatorial replay; the proof in the text covers arbitrary finite trees.'})

out={'supplement':'S009','checks':checks,'summary':{'check_count':len(checks),'all_passed':True,'method':'Exact Fraction arithmetic for phasors flows Laplacians ranks and congruences; explicitly scoped floating eigenvalue and ODE residual checks.'}}
Path(__file__).resolve().parent.joinpath('supplement_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out['summary']))
