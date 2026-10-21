"""Reproduce scoped checks for S001-S006. Uses only Python's standard library."""
import json, math
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
checks=[]
def check(id,name,ok,detail):
 if not ok:raise AssertionError(name)
 checks.append(dict(id=id,name=name,status='passed',detail=detail))
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def tr(a):return list(map(list,zip(*a)))
def eye(n):return [[float(i==j) for j in range(n)] for i in range(n)]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,s):return [[s*x for x in r] for r in a]
def eig_sym(a):
 n=len(a);a=[list(map(float,r)) for r in a];v=eye(n)
 for _ in range(500):
  if n<2:break
  p,q=max(((i,j) for i in range(n) for j in range(i+1,n)),key=lambda z:abs(a[z[0]][z[1]]))
  if abs(a[p][q])<1e-14:break
  theta=.5*math.atan2(2*a[p][q],a[q][q]-a[p][p]);c=math.cos(theta);s=math.sin(theta)
  app,aqq,apq=a[p][p],a[q][q],a[p][q]
  for k in range(n):
   if k not in (p,q):
    x,y=a[k][p],a[k][q];a[k][p]=a[p][k]=c*x-s*y;a[k][q]=a[q][k]=s*x+c*y
  a[p][p]=c*c*app-2*c*s*apq+s*s*aqq;a[q][q]=s*s*app+2*c*s*apq+c*c*aqq;a[p][q]=a[q][p]=0
  for k in range(n):x,y=v[k][p],v[k][q];v[k][p]=c*x-s*y;v[k][q]=s*x+c*y
 return [a[i][i] for i in range(n)],v
def fun_sym(a,fun):
 vals,v=eig_sym(a);return mm([[x*fun(lam) for x,lam in zip(row,vals)] for row in v],tr(v))
def norm(a):return math.sqrt(max(0,max(eig_sym(mm(tr(a),a))[0])))
def det2(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]

seq=[2**n+3**n for n in range(12)]
check('S001','Exact second-order recurrence',all(seq[n+2]==5*seq[n+1]-6*seq[n] for n in range(10)),{'prefix':seq,'scope':'Arithmetic check of the explicitly proved exponential example'})
check('S001','Minimality witness',det2([[seq[0],seq[1]],[seq[1],seq[2]]])==1,{'leading_Hankel_determinant':1})
alias=[2**(2*k)+(-2)**(2*k) for k in range(8)]
check('S001','Subsampling alias',all(alias[k+1]==4*alias[k] for k in range(7)),{'subsequence':alias,'new_order':1})

normal_cdf=lambda z:0.5*(1+math.erf(z/math.sqrt(2)))
normal_pdf=lambda z:0 if not math.isfinite(z) else math.exp(-z*z/2)/math.sqrt(2*math.pi)
def binned_information(mu,sigma,bins):
 edges=[-math.inf]+[math.atanh(math.sin(-math.pi/2+math.pi*j/bins)) for j in range(1,bins)]+[math.inf]
 result=0;total=0
 for a,b in zip(edges,edges[1:]):
  za=(a-mu)/sigma;zb=(b-mu)/sigma;prob=normal_cdf(zb)-normal_cdf(za);der=(normal_pdf(za)-normal_pdf(zb))/sigma
  total+=prob
  if prob>0:result+=der*der/prob
 return result,total
info=[]
for mu in [0.,.3,1.7]:
 for bins in [4,8,16,32]:
  v,total=binned_information(mu,1.2,bins);info.append(dict(mu=mu,bins=bins,information=v))
  assert v<=1/1.2**2+1e-12 and abs(total-1)<1e-14
check('S002','Finite-bin Fisher information after Gudermannian quantization',True,{'unquantized_information':1/1.2**2,'calculations':info,'scope':'Floating-point Gaussian CDF example, not a proof of the general inequality'})
for x in [-4,-1.2,0.,.8,4.]:
 y=math.atan(math.sinh(x));back=math.atanh(math.sin(y))
 assert abs(back-x)<1e-12
 assert abs(1/math.cos(y)-math.cosh(x))<1e-12*math.cosh(x)
check('S002','Gudermannian chart and Jacobian identities',True,{'sample_points':[-4,-1.2,0,.8,4],'scope':'Numerical identities accompanying the analytic proof'})

states=[(0,0),(1,0),(0,1),(1,1)]
observed=[x+y for x,y in states];h=[x+y+2*x for x,y in states]
check('S003','Observation class counts',len(set(observed))==3 and len(set(h))==4,{'single_probe':observed,'separating_combination':h})
indicator=[]
for i,hi in enumerate(h):
 vals=[]
 for hv in h:
  v=F(1)
  for j,hj in enumerate(h):
   if i!=j:v*=F(hv-hj,hi-hj)
  vals.append(v)
 indicator.append(vals)
check('S003','Exact Lagrange indicator basis',indicator==[[F(i==j) for j in range(4)] for i in range(4)],{'indicator_table':[[str(x) for x in row] for row in indicator]})

L=[[1,-1,0],[-1,2,-1],[0,-1,1]]
M=[[1.4,-1.4,0],[-1.4,2.1,-.7],[0,-.7,.7]]
Lam=max(max(eig_sym(L)[0]),max(eig_sym(M)[0]));values=[]
assert norm(sub(mm(L,M),mm(M,L)))>.1
for t in [.05,.2,.7,1.5]:
 KL=fun_sym(L,lambda x:math.exp(-t*x));KM=fun_sym(M,lambda x:math.exp(-t*x));delta=norm(sub(KL,KM));ld=norm(sub(L,M))
 recovered=scale(fun_sym(KL,math.log),-1/t)
 assert norm(sub(recovered,L))<1e-10
 assert delta<=t*ld+1e-12
 assert ld<=math.exp(t*Lam)*delta/t+1e-12
 values.append(dict(t=t,kernel_distance=delta,generator_distance=ld,forward_bound=t*ld,inverse_bound=math.exp(t*Lam)*delta/t,reconstruction_error=norm(sub(recovered,L))))
check('S004','Noncommuting symmetric generators satisfy forward and inverse example bounds',True,{'Lambda':Lam,'calculations':values,'scope':'Numerical spot checks; the written Duhamel/resolvent proof provides the general result'})

cycle=[[F(0) for _ in range(4)] for _ in range(4)]
for i in range(4):cycle[i][i]=F(2);cycle[i][(i-1)%4]=cycle[i][(i+1)%4]=F(-1)
p=[F(1),F(0),F(0),F(0)]
def entropy(p):return -sum(float(x)*math.log(float(x)) for x in p if x)
for step in [F(1,8),F(1,4),F(1,2)]:
 K=[[F(i==j)-step*cycle[i][j] for j in range(4)] for i in range(4)]
 assert all(x>=0 for row in K for x in row)
 assert all(sum(row)==1 for row in K) and all(sum(col)==1 for col in zip(*K))
 pn=mm([p],K)[0]
 assert sum(pn)==1 and entropy(pn)>=entropy(p)-1e-14
check('S005','Exact stochasticity and entropy example on a four-cycle',True,{'steps':['1/8','1/4','1/2'],'scope':'Exact rational update properties and numerical entropy values'})
K=[[F(i==j)-F(1,2)*cycle[i][j] for j in range(4)] for i in range(4)]
alternating=[F(1),F(-1),F(1),F(-1)]
check('S005','Positivity endpoint can retain a periodic mode',mm(K,[[v] for v in alternating])==[[-v] for v in alternating],{'alternating_mode_multiplier':-1})

Projection=[[1,0,0],[0,1,0],[0,0,0]]
square=lambda v:sum(x*x for x in v)
project=lambda v:[sum(a*b for a,b in zip(row,v)) for row in Projection]
d1=[F(3),F(4),F(0)];d2=[F(0),F(0),F(5)]
check('S006','Retained and invisible Gaussian shifts',square(project(d1))==25 and square(project(d2))==0 and square(d2)==25,{'retained_shift':[3,4,0],'invisible_shift':[0,0,5],'full_noncentralities':[25,25],'panel_noncentralities':[25,0]})
e=[F(-6,5),F(-8,5),F(0)];perturbed=[x+y for x,y in zip(d1,e)]
check('S006','Worst-case robust noncentrality is attained',square(e)==4 and square(project(perturbed))==9,{'epsilon':2,'perturbation':[str(x) for x in e],'retained_noncentrality':9})

result={'checks':checks,'count':len(checks),'status':'passed','scope':'Exact checks are marked as such. Floating-point examples do not replace the written proofs.'}
(P/'synthesis_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'checks':len(checks),'status':'passed'}))
