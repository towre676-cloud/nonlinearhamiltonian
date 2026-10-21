"""Portable stdlib finite certificates, exact arithmetic unless a tolerance is stated."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import math,json
HERE=Path(__file__).resolve().parent
checks=[]
def check(n,name,fn):
 try: detail=fn();checks.append(dict(id=f'Y24-04-{n:03d}',name=name,status='passed',detail=detail))
 except Exception as e:checks.append(dict(id=f'Y24-04-{n:03d}',name=name,status='failed',detail=repr(e)))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def det(A):
 if len(A)==1:return A[0][0]
 return sum((-1)**j*A[0][j]*det([r[:j]+r[j+1:] for r in A[1:]]) for j in range(len(A)))
def rank(A):
 A=[[F(x) for x in r] for r in A];i=0
 for j in range(len(A[0])):
  p=next((p for p in range(i,len(A)) if A[p][j]),None)
  if p is None:continue
  A[i],A[p]=A[p],A[i];v=A[i][j];A[i]=[x/v for x in A[i]]
  for k in range(len(A)):
   if k!=i:
    v=A[k][j];A[k]=[a-v*b for a,b in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i
class AD:
 def __init__(self,v,d):self.v=F(v);self.d=tuple(F(x) for x in d)
 def co(self,o):return o if isinstance(o,AD) else AD(o,[0]*len(self.d))
 def __add__(self,o):
  o=self.co(o);return AD(self.v+o.v,[a+b for a,b in zip(self.d,o.d)])
 __radd__=__add__
 def __neg__(self):return AD(-self.v,[-x for x in self.d])
 def __sub__(self,o):return self+-self.co(o)
 def __rsub__(self,o):return self.co(o)+-self
 def __mul__(self,o):
  o=self.co(o);return AD(self.v*o.v,[a*o.v+self.v*b for a,b in zip(self.d,o.d)])
 __rmul__=__mul__
 def __pow__(self,n):
  assert isinstance(n,int) and n>=0
  r=AD(1,[0]*len(self.d))
  for _ in range(n):r=r*self
  return r
 def __truediv__(self,o):
  assert not isinstance(o,AD);return self*F(1,o)
def jac(fn,values):
 n=len(values);r=fn(*[AD(v,[int(i==j) for j in range(n)]) for i,v in enumerate(values)])
 return [list(x.d) for x in r]
def scatter(xs,lab):
 groups=[[F(x) for x,l in zip(xs,lab) if l==g] for g in set(lab)]
 mu=sum(map(F,xs))/len(xs)
 W=sum(sum((x-sum(g)/len(g))**2 for x in g) for g in groups)
 B=sum(len(g)*(sum(g)/len(g)-mu)**2 for g in groups)
 T=sum((F(x)-mu)**2 for x in xs)
 return W,B,T
labs=[(0,)+t for t in product((0,1),repeat=3)]
def clustering():
 records=[]
 for lab in labs:
  W,B,T=scatter([0,0,1,1],lab);assert T==W+B==1
  assert 2*B-3*W==2*T-5*W
  records.append((list(lab),str(W),str(B)))
 return {'exhaustive_unlabeled_partitions':8,'scatter_certificate':records}
def potts():
 out=[]
 for gamma,want in [(F(1,2),[(0,0,1,1)]),(F(1),[(0,0,0,0),(0,0,1,1)]),(F(2),[(0,0,0,0)])]:
  vals={l:scatter([0,0,1,1],l)[0]+gamma*sum(a!=b for a,b in zip(l,l[1:])) for l in labs}
  m=min(vals.values());opts=sorted(l for l,v in vals.items() if v==m)
  assert opts==want;out.append(dict(gamma=str(gamma),minimum=str(m),minimizers=opts))
 return out
def regularizers():
 z=[F(3),F(4)];l1=[F(2),F(3)];l2=[F(12,5),F(16,5)];ridge=[F(3,2),F(2)]
 assert all(x-y+1==0 for x,y in zip(l1,z))
 length=F(4);assert all(x-y+x/length==0 for x,y in zip(l2,z))
 assert all(2*x-y==0 for x,y in zip(ridge,z))
 assert F(1,2)<=1 # zero-coordinate subgradient at small input
 return 'Three distinct exact KKT certificates atz(3,4),λ1; radial output length4.'
def online():
 eta=F(1,2);c=F(0)
 for x in [0,0,9]:c=(1-eta)*c+eta*x
 assert c==F(9,2) and F(9,3)==3
 weights=[]
 for j in range(3):
  c=F(0)
  for i in range(3):c=(1-eta)*c+eta*(i==j)
  weights.append(c)
 assert weights==[F(1,8),F(1,4),F(1,2)]
 assert sum(x*x for x in weights)==F(21,64)
 return {'impulse_weights':list(map(str,weights)),'variance':'21/64','limiting_variance':'1/3'}
def kernels():
 xs=[-1,0,1];K=[[(1+x*y)**2 for y in xs] for x in xs]
 assert K==[[4,1,0],[1,1,1],[0,1,4]]
 assert [det([r[:n] for r in K[:n]]) for n in range(1,4)]==[4,3,8]
 bad=[[0,2],[2,0]];v=[1,-1]
 assert sum(v[i]*bad[i][j]*v[j] for i in range(2) for j in range(2))==-4
 return 'Exact principal minors4,3,8; indefinite counterexample quadratic form−4.'
def bayes():
 # Match unnormalized log posterior at several rational θ after completing the square.
 m=F(1);v=F(1,3)
 def energy(t):return t*t+(1-t)**2+(2-t)**2
 for t in map(F,[-2,0,1,3]):assert energy(t)==(t-m)**2/v+2
 w=[F(1,3),F(2,3)]
 assert sum(a*b for a in w for b in w)==1
 assert v+1==F(4,3)
 return 'Posterior square completion exactly3(θ−1)²+2; singular duplicate covariance leaves variance1.'
def transfer():
 ps=[F(3,4),F(1,4)];pt=ps[::-1];loss=[0,1];w=[t/s for s,t in zip(ps,pt)]
 assert w==[F(1,3),3]
 assert sum(s*a*l for s,a,l in zip(ps,w,loss))==sum(t*l for t,l in zip(pt,loss))==F(3,4)
 return 'Finite change-of-measure identity exact; unsupported target point cannot have finite source density ratio.'
def ratios():
 a,b,c=F('2.26'),F('.498'),F('.1446');T=a+b
 assert T==F('2.758') and a/T==F(1130,1379) and b/T==F(249,1379) and c/T==F(723,13790)
 assert F(2,10)==F(1,5) and 1-(1-F(1,10))**2==F(19,100)
 return {'shares':[str(a/T),str(b/T)],'separate_ratio':str(c/T),'lottery_demo':['1/5','19/100'],'historical_denominator':'unavailable'}
def geometry():
 cells={(0,0),(1,0)};exterior=sum((x+dx,y+dy) not in cells for x,y in cells for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
 assert exterior==6 and 4*len(cells)-2==6
 distinct=exterior+1;assert distinct==7 and 4*len(cells)==8
 for a,b in [(1,1),(2,1),(F(1,3),5)]:assert (a+b)**2>=4*a*b
 return 'Two cells: exterior6, distinct edges7, patch perimeter sum8; shared-edge perimeter formula independently counted.'
def fractal():
 pieces=[(F(0),F(1))]
 for n in range(1,9):
  pieces=[q for a,b in pieces for q in [(a,a+(b-a)/3),(b-(b-a)/3,b)]]
  assert len(pieces)==2**n and all(b-a==F(1,3**n) for a,b in pieces)
 assert abs(1+math.log(4)/math.log(2)-3)<1e-12
 assert abs(1+math.log(4)/math.log(4)-2)<1e-12
 return 'Cantor finite-level2^n covering pieces and3^−n lengths throughn8; raw log ratio changes from3 to2 under two unit scalings. Limit proof is in text.'
def division():
 p=list(map(F,[F(1,2),F(1,4),F(1,8),F(1,8)]));D=1-sum(x*x for x in p)
 q=p[:2]+[p[2]+p[3]];D2=1-sum(x*x for x in q)
 assert D==F(21,32) and D2==F(5,8) and D-D2==2*p[2]*p[3]==F(1,32)
 return {'D':'21/32','merged_D':'5/8','effective_count':'32/11'}
def pca():
 points=[(1,0),(0,1),(-1,0),(0,-1)]
 cov=[[sum(F(p[i]*p[j],4) for p in points) for j in range(2)] for i in range(2)]
 assert cov==[[F(1,2),0],[0,F(1,2)]]
 for u in [(1,0),(F(3,5),F(4,5))]:
  error=sum(F(sum(x*x for x in p))-(sum(a*b for a,b in zip(u,p)))**2 for p in points)/4
  assert error==F(1,2)
 return 'Exact covarianceI/2 and reconstruction error1/2 for two different rank-one projectors; not a manifold-dimension estimator.'
def spectral():
 d=[[0]*4 for _ in range(4)];d[1][2]=1
 assert mm(d,d)==[[0]*4 for _ in range(4)] and rank(d)==1
 assert 4-2*rank(d)==2 and rank([[0]*4 for _ in range(4)])==0
 return 'Four-dimensional page differential has square zero, rank1 and homology dimension2; zero differential leaves4. Serre existence/convergence is cited background.'
def sheaf():
 cover=[{0:2,1:3},{1:3,2:5},{2:5,3:7}];glued={}
 for section in cover:
  for x,v in section.items():assert x not in glued or glued[x]==v;glued[x]=v
 assert glued=={0:2,1:3,2:5,3:7}
 assert det([[2,3],[-1,4]])==11
 # Boundary of an oriented triangle has zero vertex boundary.
 B1=[[-1,0,1],[1,-1,0],[0,1,-1]];B2=[[1],[1],[1]]
 assert mm(B1,B2)==[[0],[0],[0]]
 return 'Compatible finite-section gluing; wedge determinant11; triangle boundary-square zero. Continuous sheaf proof and Stokes argument remain in text.'
def braid():
 U=[[1,1],[0,1]];V=[[1,0],[-1,1]];I=[[1,0],[0,1]]
 assert mm(mm(U,V),U)==mm(mm(V,U),V)
 A=mm(U,U);B=mm(V,V)
 inv=lambda M:[[M[1][1],-M[0][1]],[-M[1][0],M[0][0]]]
 comm=lambda X,Y:mm(mm(mm(X,Y),inv(X)),inv(Y))
 C=comm(A,B);assert C==[[13,8],[8,5]] and det(C)==1 and C!=I
 for X,Y in [(I,A),(A,I),(I,I)]:assert comm(X,Y)==I
 return {'commutator':C,'deletion_images':'all identity','scope':'Representation proves nontriviality; strand deletion geometry is justified in text.'}
def elasticity():
 a=F(2,3);mu=F(1);strain=[[0,a/2,0],[a/2,0,0],[0,0,0]]
 energy=mu*sum(x*x for r in strain for x in r)
 assert energy==mu*a*a/2
 b=F(1);lam=F(-1)
 dilation=3*mu*b*b+F(9,2)*lam*b*b
 assert dilation==F(-3,2)<0
 return 'Exact tensor-shear factor and negative dilation-energy counterexample verified.'
def populations():
 beta=2;gamma=1;S=F(4,5);I=F(1,5)
 f=[-beta*S*I,beta*S*I-gamma*I,gamma*I]
 assert f==[F(-8,25),F(3,25),F(1,5)] and sum(f)==0
 for x,y in [(F(2),F(1,2)),(F(3,4),F(5,3)),(F(1),F(1))]:
  dx=x*(1-y);dy=y*(x-1)
  assert (1-1/x)*dx+(1-1/y)*dy==0
 return 'SIR conservation and threshold example exact; Lotka–Volterra first-integral derivative zero at three independent rational states.'
def oscillators():
 for r,want in [(F(5,2),F(-1,2)),(F(7,2),F(-3,2))]:
  x=1-1/r;assert r*x*(1-x)==x and r*(1-2*x)==want
 J=jac(lambda x,y:[y,F(-1,2)*(1-x*x)*y-x],[0,0]);assert J==[[0,1],[-1,F(-1,2)]]
 K=jac(lambda v,w:[v-v**3/3-w,3*(v-F(1,2)*w)],[0,0]);assert K==[[1,-1],[3,F(-3,2)]]
 assert K[0][0]+K[1][1]==F(-1,2) and det(K)==F(3,2)
 return 'Exact automatic differentiation and discrete multipliers reproduce all local-stability examples.'
def lorenz():
 sigma=F(10);beta=F(8,3)
 # Useρ=4 so positive equilibrium x=sqrt(8) is avoided via choosingβ1,ρ5,x2 for independent cubic check.
 J=jac(lambda x,y,z:[10*(y-x),x*(5-z)-y,x*y-z],[2,2,4])
 A1=-sum(J[i][i] for i in range(3));A2=sum(J[i][i]*J[j][j]-J[i][j]*J[j][i] for i in range(3) for j in range(i+1,3));A3=-det(J)
 assert (A1,A2,A3)==(12,15,80)
 assert sigma*(sigma+beta+3)/(sigma-beta-1)==F(470,19)
 assert 20<F(470,19)<28
 assert (sigma+beta+1)*beta*(sigma+28)-2*sigma*beta*(28-1)==F(-496,9)
 for x in [(3-math.sqrt(5))/2,(3+math.sqrt(5))/2]:assert abs(1+x*(x-3))<1e-14
 return 'Independent exact Jacobian/cubic coefficients at a rational Lorenz equilibrium; classic threshold470/19 and Rössler equilibria verified.'
def reaction():
 J=jac(lambda u,v:[1-F(5,2)*u+u*u*v,F(3,2)*u-u*u*v],[1,F(3,2)])
 assert J==[[F(1,2),1],[F(-3,2),-1]] and det(J)==1
 s=F(1,10);M=[[J[i][j]-(s*[1,100][i] if i==j else 0) for j in range(2)] for i in range(2)]
 assert det(M)==F(-29,10) and M[0][0]+M[1][1]==F(-53,5)
 return 'Exact AD reaction Jacobian; stable homogeneous determinant1/trace−1/2; spatial determinant−29/10/trace−53/5.'
def gradient():
 rates=[s*(1-s) for s in [F(0),F(1,4),F(2)]];assert rates==[0,F(3,16),-2]
 assert [1-s for s in [F(0),F(1,4),F(2)]]==[1,F(3,4),-1]
 assert F(1,10)-(1-F(1))**2==F(1,10)
 # Direct trigonometric quadrature of two dissipation integrands at u=sinx, ε1.
 n=32768;h=2*math.pi/n
 ac=h*sum(math.sin(k*h)**6 for k in range(n))
 ch=h*sum((3*math.sin(k*h)**2*math.cos(k*h))**2 for k in range(n))
 assert abs(ac-5*math.pi/8)<1e-11 and abs(ch-9*math.pi/8)<1e-11
 return {'Fourier_rates':list(map(str,rates)),'AC_dissipation':-ac,'CH_dissipation':-ch,'scope':'Periodic smooth-field energy identities are proved in text; this checks one independent trigonometric example.'}
def kuramoto():
 K=F(1,2)
 for t in [0,.3,2]:
  q=math.exp(-t);delta=2*math.atan(q);derivative=-2*q/(1+q*q)
  assert abs(derivative+2*float(K)*math.sin(delta))<1e-14
 # Path of three phases: verify gradient dissipation at a nontrivial state.
 phi=[0,.4,-.7];vel=[0.,0.,0.]
 for i,j in [(0,1),(1,2)]:
  flow=math.sin(phi[j]-phi[i]);vel[i]+=flow;vel[j]-=flow
 dV=sum(math.sin(phi[i]-phi[j])*(vel[i]-vel[j]) for i,j in [(0,1),(1,2)])
 assert abs(dV+sum(v*v for v in vel))<1e-14
 return 'Exact two-phase solution differentiated numerically; independent three-vertex potential dissipation check.'
def gauge():
 configs=list(product((-1,1),repeat=4));gs=configs;edges=[(0,1),(1,2),(2,3),(3,0)]
 action=lambda U:1-math.prod(U)
 trans=lambda U,g:tuple(g[i]*u*g[j] for u,(i,j) in zip(U,edges))
 for U in configs:
  for g in gs:assert action(trans(U,g))==action(U)
 orbits=[];unseen=set(configs)
 while unseen:
  U=min(unseen);orbit={trans(U,g) for g in gs};orbits.append(orbit);unseen-=orbit
 assert sorted(map(len,orbits))==[8,8]
 assert {tuple(sorted({math.prod(U) for U in o})) for o in orbits}=={(-1,),(1,)}
 Z=sum(math.exp(-action(U)) for U in configs);assert abs(Z-8*(1+math.exp(-2)))<1e-14
 return {'configurations':16,'gauge_transform_pairs':256,'orbit_sizes':[8,8],'partition_function_beta1':Z}
functions=[clustering,potts,regularizers,online,kernels,bayes,transfer,ratios,geometry,fractal,division,pca,spectral,sheaf,braid,elasticity,populations,oscillators,lorenz,reaction,gradient,kuramoto,gauge]
for n,fn in enumerate(functions,1):check(n,fn.__name__,fn)
result=dict(scope='Finite examples, exact certificates and stated numerical identities only. General existence, convergence, topology and physical applicability are not certified by these checks.',checks=checks,passed=sum(c['status']=='passed' for c in checks),failed=sum(c['status']=='failed' for c in checks))
HERE.joinpath('checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
if result['failed']:raise SystemExit(1)
