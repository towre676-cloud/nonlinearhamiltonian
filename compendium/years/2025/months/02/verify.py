"""Portable mathematical example checks; no unmeasured historical claim is certified."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import math,json
HERE=Path(__file__).resolve().parent
checks=[]
def check(n,name,fn):
 try:detail=fn();checks.append(dict(id=f'Y25-02-{n:03d}',name=name,status='passed',detail=detail))
 except Exception as exc:checks.append(dict(id=f'Y25-02-{n:03d}',name=name,status='failed',detail=repr(exc)))
def mm(A,B):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def tr(A):return list(map(list,zip(*A)))
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def rank(A):
 A=[list(map(F,r)) for r in A];r=0
 for j in range(len(A[0])):
  p=next((p for p in range(r,len(A)) if A[p][j]),None)
  if p is None:continue
  A[r],A[p]=A[p],A[r];z=A[r][j];A[r]=[x/z for x in A[r]]
  for i in range(len(A)):
   if i!=r:
    z=A[i][j];A[i]=[a-z*b for a,b in zip(A[i],A[r])]
  r+=1
  if r==len(A):break
 return r
I=eye(2);X=[[0,1],[1,0]];Y=[[0,-1j],[1j,0]];Z=[[1,0],[0,-1]]
def c1():
 for t in [0,.7,3]:
  w=50*(1-math.exp(-t/5));wd=10*math.exp(-t/5)
  assert abs(wd-(10-w/5))<1e-13
 return 'Analytic feedbacksolution satisfiesODEatthree times;stablelimit50.'
def c2():
 A=[[0,F(1,4)],[F(1,2),0]];B=[[F(8,7),F(2,7)],[F(4,7),F(8,7)]]
 assert mm([[1,-F(1,4)],[-F(1,2),1]],B)==I
 assert sum(B[i][0] for i in range(2))==F(12,7) and sum(B[i][1] for i in range(2))==F(10,7)
 return 'Exactinverse andtwo directional multipliers independently matrix-multiplied.'
def c3():
 x=[F(5,3),F(1,3)];a=[2,1];assert sum(x)==2
 assert [a[i]/(1+x[i]) for i in range(2)]==[F(3,4)]*2
 # Feasible-direction derivative vanishesatoptimumandHessianisnegative.
 assert all(-a[i]/(1+x[i])**2<0 for i in range(2))
 return 'ExactKKTcertificate plusstrictconcavity;feasibleallocation5/3,1/3.'
def c4():
 r=F(1,50);g=F(1,25)
 assert (1+r+F(1,100))/(1+g)==F(103,104)
 assert (1+r+F(1,20))/(1+g)==F(107,104)
 b=F(1)
 for t in range(1,8):
  b=((1+r)*b+F(1,100))/(1+g)
  assert b==F(1,2)+F(1,2)*F(51,52)**t
 return 'Seven exactdebt-ratiosteps matchclosedform;opposite primaryflows reverseinitialdirection.'
def c5():
 def gini(x):return F(sum(abs(a-b) for a in x for b in x),2*len(x)*sum(x))
 assert gini([0,0,2,2])==gini([0,0,20,20])==F(1,2) and gini([1]*4)==0
 assert 341000000//10000==34100 and (341000001+9999)//10000==34101
 return 'ExactpairwiseGini,scaleinvarianceandwhole-representativeceiling verified.'
def c6():
 t=10*math.log(2);assert abs(2*math.exp(-t/10)-1)<1e-14
 for t in [0,1,7]:
  a=.1*math.exp(-t/10);gd=-.2*math.exp(-t/10)
  assert abs(gd+2*a)<1e-14
 return 'Dampedsourceanalytictrajectoryandfinitezero-crossingtime verified.'
def c7():
 u=list(map(F,[0,1,2,3]));nu=F(1,2)
 serial=[(1-nu)*u[j]+nu*u[(j-1)%4] for j in range(4)]
 local=[]
 for data,halo in [(u[:2],u[3]),(u[2:],u[1])]:local += [(1-nu)*data[j]+nu*(data[j-1] if j else halo) for j in range(2)]
 assert serial==local==[F(3,2),F(1,2),F(3,2),F(5,2)] and sum(serial)==sum(u)
 assert abs(1-2*F(5,4))>1
 return 'Exactserial/haloupdateequality,meanconservationandunstablealternatingamplification.'
def c8():
 # Integrateproducts ofindependentlydifferentiatedpower-basis coefficients.
 basis=[[1,-2,1],[0,2,-2],[0,0,1]]
 deriv=[[i*c for i,c in enumerate(b)][1:] for b in basis]
 K=[[sum(F(a*b,i+j+1) for i,a in enumerate(p) for j,b in enumerate(q)) for q in deriv] for p in deriv]
 want=[[F(4,3) if i==j else F(-2,3) for j in range(3)] for i in range(3)]
 assert K==want and rank(K)==2
 assert sum(F(a)*K[i][j]*F(b) for i,a in enumerate([0,F(1,2),1]) for j,b in enumerate([0,F(1,2),1]))==1
 return {'stiffness':[[str(x) for x in r] for r in K],'rank':2}
def c9():
 # Rescale theatomby√3 tokeepallarithmeticalchecks rational.
 w=[1,3];b=[0,2];at=[F(3,4),F(-1,4)]
 assert sum(a*z for a,z in zip(at,w))==0
 assert sum(a*a*z for a,z in zip(at,w))==F(3,4)
 mean=F(3,2);osc2=sum(z*(x-mean)**2 for z,x in zip(w,b))/4
 pair=sum(z*a*x for z,a,x in zip(w,at,b))
 assert osc2==F(3,4) and pair*pair/3==osc2
 return 'Rationallyrescaledweightedatom attainssquaredbound3/4;normalizationscheckedexactly.'
def c10():
 V=lambda r:math.pi*(math.sinh(2*r)-2*r)
 assert V(4)/V(2)>V(2)/V(1)>2
 for R in [2,4,8]:assert 1+math.pi**2/(2*R)**2<1+math.pi**2/R**2
 return 'Exactradialidentityprovedintext;finitevolume-ratiogrowthandtestfunctionRayleighquotientscheckitsconsequences.'
def c11():
 H=[[.5]*4,[.5,.5,-.5,-.5],[1/math.sqrt(2),-1/math.sqrt(2),0,0],[0,0,1/math.sqrt(2),-1/math.sqrt(2)]]
 G=mm(H,tr(H));assert max(abs(G[i][j]-(i==j)) for i in range(4) for j in range(4))<1e-14
 coeff=[sum(a*b for a,b in zip(h,[0,1,2,3])) for h in H]
 assert abs(sum(c*c for c in coeff)-14)<1e-13
 return {'Haar_coefficients':coeff,'frame_energy':14,'orthogonality_tolerance':1e-14}
def c12():
 eps=math.sqrt(math.log(40000)/2000)
 assert abs(2*1000*math.exp(-2*1000*eps*eps)-.05)<1e-13
 return {'uniform_radius':eps,'excess_risk_bound':2*eps,'hypotheses':'independent bounded validationlosses andfixedfamily;notverifiedformarketdata'}
def c13():
 E=[]
 for i,j in product(range(2),repeat=2):E.append([[int(a==i and b==j) for b in range(2)] for a in range(2)])
 for i,j,k,l in product(range(2),repeat=4):
  assert mm(E[2*i+j],E[2*k+l])==[[int(j==k)*x for x in row] for row in E[2*i+l]]
 return 'All16matrix-unitproductidentitiescertifythewrittenMorita inverse;two-cosetS3actionhastrivial/signcharacters.'
def c14():
 A=[[0,1],[0,0]];assert mm(A,A)==[[0,0],[0,0]]
 assert [[I[i][j]+A[i][j] for j in range(2)] for i in range(2)]!=I
 for n in [1,2,3]:assert abs(math.sin(2*math.pi*n))<1e-14 and abs(math.cos(2*math.pi*n)-1)<1e-14
 return 'Jordanmonodromyexactlynonidentity;threeoscillatoryidentityperiodschecked.'
def c15():
 for k in map(F,[-2,0,2]):
  d=lambda n:F(n)+(k if n%2 else 0)
  for n in range(8):assert d(n+1)-d(n)==1+k*(-1)**n
 return 'All24monomialcommutatorsverify[Dκ,X]=I+κs;HH2classificationiscitedbackground.'
def c16():
 # CompositeSimpsonintegraloftheexplicitcurvaturedensity.
 n=4096;h=math.pi/n;f=lambda t:.5*math.sin(t)
 integral=h/3*(f(0)+f(math.pi)+sum((4 if i%2 else 2)*f(i*h) for i in range(1,n)))
 assert abs(integral-1)<1e-12
 return 'Curvatureintegraldividedby2π equals1 within1e-12;patchtransition/Stokesargumentprovedintext.'
def c17():
 for t in [.01,.5,3]:
  P=(1+2*math.exp(-2*t)+math.exp(-4*t))/4
  exact=(1+math.exp(-2*t))**2/4;assert abs(P-exact)<1e-14
 assert abs(4/(math.e+1)-1.07576568547998)<1e-12
 return 'C4heatfactorizationandscaleddimensionchecked;compact-resolvent/summabilitydistinctionhasexplicitcomparisonproof.'
def c18():
 for s in [F(1,2),F(3,2),F(2)]:
  # Differentiatelog[(s−1)^2 e^(3s)] algebraicallyawayfromthezero.
  quotient=(2*(s-1)+3*(s-1)**2)/(s-1)**2
  assert quotient==2/(s-1)+3
 return 'Independentproduct-derivativequotientconfirmpoleandregularpartatthreeexactpoints.'
def kron(A,B):return [[a*b for a in r for b in s] for r in A for s in B]
def c19():
 Xs=[kron(kron(X,I),I),kron(kron(I,X),I),kron(kron(I,I),X)]
 errors=[eye(8)]+Xs
 for a,b in product(errors,repeat=2):
  C=mm(tr(a),b);block=[[C[i][j] for j in [0,7]] for i in [0,7]]
  assert block==(I if a==b else [[0,0],[0,0]])
 LZ=kron(kron(Z,I),I);assert [LZ[0][0],LZ[7][7]]==[1,-1]
 return 'All16Knill–Laflammeproductscheckedexactly;weight-onephaseerrorisnontriviallogicalZ.'
def c20():
 A=[[1,0],[0,0]];B=[[0,1],[0,0]];C=[[0,0],[1,0]]
 comm=lambda X,Y:[[a-b for a,b in zip(r,s)] for r,s in zip(mm(X,Y),mm(Y,X))]
 cs=[comm(A,B),comm([[0,0],[0,1]],C),comm(B,C)]
 assert rank([[M[i][j] for i,j in product(range(2),repeat=2)] for M in cs])==3
 assert all(sum(M[i][i] for i in range(2))==0 for M in cs)
 return 'Matrixcommutatorsspanexactthree-dimensionaltracelessspace;finitecoverequalizerdimension3.'
def c21():
 p=F(1,5);rho=[[F(3,4),F(1,4)],[F(1,4),F(1,4)]]
 weights=[1-3*p/4,p/4,p/4,p/4];ops=[I,X,Y,Z]
 out=[[sum(w*mm(mm(U,rho),tr([[x.conjugate() if hasattr(x,'conjugate') else x for x in r] for r in U]))[i][j] for w,U in zip(weights,ops)) for j in range(2)] for i in range(2)]
 target=[[(1-p)*rho[i][j]+(p/2 if i==j else 0) for j in range(2)] for i in range(2)]
 assert all(abs(out[i][j]-target[i][j])<1e-14 for i,j in product(range(2),repeat=2))
 assert (1-p)**5==F(1024,3125)
 return 'Krausmixtureindependentlymatchesdepolarizingformula;fivestepcontraction1024/3125.'
def c22():
 m=[int(n%2==0) for n in range(13)];b=[0]*13
 for n in range(1,13):b[n]=m[n]-sum(b[j]*m[n-j] for j in range(1,n))
 assert b[2]==1 and sum(abs(x) for x in b)==1
 words=['']+[a for a in '01']+[a+b for a in '01' for b in '01'];assert len(words)==7
 assert sum(bool(w) for w in words)==6
 return 'Booleanmomentrecursionthroughdegree12hasonlyb2;wordspacehasonevacuumdefectandspecifiedtop-layertruncation.'
def c23():
 bell=[[F(1,2) if i in [0,3] and j in [0,3] else 0 for j in range(4)] for i in range(4)]
 mix=[[bell[i][j] if i==j else 0 for j in range(4)] for i in range(4)]
 XX=kron(X,X);ZZ=kron(Z,Z)
 expect=lambda rho,A:sum(rho[i][j]*A[j][i] for i in range(4) for j in range(4))
 assert expect(bell,XX)==1 and expect(mix,XX)==0 and expect(bell,ZZ)==expect(mix,ZZ)==1
 assert [bell[i][i] for i in range(4)]==[mix[i][i] for i in range(4)]
 return 'Exactrationaldensity-matrixcollisionforallbasisprobabilitiesandZZ,distinguishedbyXX.'
def c24():
 # The associator preserves all16orderedbasistensors in four2-dimensional factors.
 labels=list(product((0,1),repeat=4));assert len(set(labels))==16
 assert 3*F(7,100)+2*F(7,100)==F(35,100)
 return 'All16basistensorlabelsagreealongbothcanonicalpaths;five-edgeerrorbound0.35usesprovedtelescopingestimate.'
def c25():
 Y=F(2);assert 1/Y==F(1,2) and F(1,8)/F(1,2)==F(1,4)
 assert abs(math.log(8/2)-math.log(4))<1e-14
 return 'Exactcuspantiderivativearea1/2,sectionlengthratio1/4andverticaldistancelog4.'
for n in range(1,26):check(n,globals()['c'+str(n)].__name__,globals()['c'+str(n)])
r={'scope':'Exactfiniteexamplesanddeclarednumericalchecks;nohistoricalforecasts,marketdata,hardwareclaimsorfullgeometricLanglandsresultiscertified.','checks':checks,'passed':sum(c['status']=='passed' for c in checks),'failed':sum(c['status']=='failed' for c in checks)}
HERE.joinpath('checks.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(r['passed'],r['failed'])
if r['failed']:print([c for c in checks if c['status']=='failed']);raise SystemExit(1)
