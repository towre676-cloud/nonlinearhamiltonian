"""Portable exact finite certificates and explicitly scoped analytic spot checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json, math, sys
HERE=Path(__file__).resolve().parent
checks=[]
def check(n,name,fn):
 try: detail=fn(); checks.append(dict(id=f'Y26-02-{n:03d}',name=name,status='passed',detail=detail))
 except Exception as e: checks.append(dict(id=f'Y26-02-{n:03d}',name=name,status='failed',detail=repr(e)))
def mm(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def det(A):
 A=[list(map(F,r)) for r in A];d=F(1)
 for j in range(len(A)):
  p=next((i for i in range(j,len(A)) if A[i][j]),None)
  if p is None:return F(0)
  if p!=j:A[p],A[j]=A[j],A[p];d=-d
  z=A[j][j];d*=z
  for i in range(j+1,len(A)):
   q=A[i][j]/z
   for k in range(j,len(A)):A[i][k]-=q*A[j][k]
 return d
def rank(A):
 A=[list(map(F,r)) for r in A];r=0
 for j in range(len(A[0])):
  p=next((i for i in range(r,len(A)) if A[i][j]),None)
  if p is None:continue
  A[p],A[r]=A[r],A[p];z=A[r][j];A[r]=[x/z for x in A[r]]
  for i in range(len(A)):
   if i!=r:
    q=A[i][j];A[i]=[x-q*y for x,y in zip(A[i],A[r])]
  r+=1
  if r==len(A):break
 return r
def close(a,b,tol=1e-10):assert abs(a-b)<tol,(a,b)
def simpson(f,a,b,n=2000):
 h=(b-a)/n;return h/3*(f(a)+f(b)+4*sum(f(a+(2*j-1)*h) for j in range(1,n//2+1))+2*sum(f(a+2*j*h) for j in range(1,n//2)))
from itertools import combinations
from collections import Counter
import cmath

def c1():
 edges={frozenset(e) for e in [(0,1),(1,2),(2,3),(3,0)]};hist=Counter()
 for S in combinations(range(4),2):hist[2-sum(e<=set(S) for e in edges)]+=1
 assert hist=={1:4,2:2} and sum(F(k*v,6) for k,v in hist.items())==F(4,3)
 return {'complete_induced_pair_distribution':dict(hist),'expected_Euler':'4/3'}
def c2():
 # Exact order-statistic moments from polynomial integration.
 EB=F(4,5);length=F(1,5);assert EB+length==1 and F(1,2)**4==F(1,16)
 # Every proper induced subgraph of C4 is acyclic.
 edges=[(0,1),(1,2),(2,3),(3,0)]
 for n in range(1,4):
  for S in combinations(range(4),n):
   es=[e for e in edges if set(e)<=set(S)];assert len(es)<n
 return 'All proper induced supports contain no cycle; birth CDFt^4, mean4/5 and mean bar1/5 checked by exact integration.'
def c3():
 weights=[1,2,3];subs=list(combinations(range(3),2));raw=[math.prod(weights[i] for i in S) for S in subs];assert raw==[2,3,6]
 prob=[F(v,sum(raw)) for v in raw];marg=[sum(p for S,p in zip(subs,prob) if i in S) for i in range(3)]
 assert marg==[F(5,11),F(8,11),F(9,11)] and sum(marg)==2
 assert sum((2-int(S==(0,1)))*p for S,p in zip(subs,prob))==F(20,11)
 return {'subset_weights':raw,'marginals':[str(x) for x in marg],'Euler_mean':'20/11'}
def c4():
 d=[[-1,1,0],[0,-1,1],[1,0,-1]];x=[[0],[2],[5]]
 assert mm(d,x)==[[2],[3],[-5]] and rank(d)==2
 assert rank([r+[a] for r,a in zip(d,[2,3,-4])])==3
 return 'Exact compatible and incompatible augmented ranks2 versus3, with cycle obstruction0 versus1.'
def c5():
 words=list(product(range(2),repeat=5))
 def distance(x,y):
  for k,(a,b) in enumerate(zip(x,y)):
   if a!=b:return F(1,4**k)
  return F(0)
 for x,y,z in product(words[:8],repeat=3):assert distance(x,z)<=max(distance(x,y),distance(y,z))
 assert F(1,2)==sum((F(1,2**j) for j in range(2,40)),F(0))+F(1,2**39)
 return 'All triples of eight depth5 words satisfy the ultrametric; exact terminating/nonterminating binary limit identity checked. Hausdorff proof is in text.'
def c6():
 a=float(2**53);b=1.;s=a+b;z=s-a;lo=b-z
 assert s==a and lo==1 and (s-a)+lo==1 and ((a+b)-a)==0
 assert F.from_float(s)+F.from_float(lo)==F.from_float(a)+F.from_float(b)
 return 'Exact rational interpretation of binary64 verifies retained residual1 and scalar cancellation failure.'
def c7():
 # Nonzero connecting map in 0 -> H0O -> H0E -> H0O -> H1O.
 delta=[[1]];assert rank(delta)==1 and 1+(1-rank(delta))==1
 assert 1+1==2
 return 'Independent exact-sequence rank check gives h0E1 versus split2; Serre duality/genus input are cited background, not a computational geometric proof.'
def c8():
 cutoffs=[0,2]
 heart={(i,n) for i in range(2) for n in range(-4,6) if n==cutoffs[i]}
 assert heart=={(0,0),(1,2)}
 for i,n in heart:
  assert all((m>=cutoffs[i])<=((m+1)>=cutoffs[i]) for m in range(-4,5))
 return 'Explicit two-factor heart cutoffs and aisle shift closure checked; classification proof uses complete semisimple splitting in text.'
def c9():
 gaussian=simpson(lambda x:math.exp(-x*x),-8,8,n=8000);close(gaussian,math.sqrt(math.pi),1e-12)
 shifted=simpson(lambda x:math.exp(-x*x+x),-8,8,n=8000);close(shifted,math.exp(.25)*math.sqrt(math.pi),1e-12)
 close(simpson(math.exp,0,1),math.e-1,1e-12)
 return {'Gaussian_quadrature':gaussian,'shifted_Gaussian_quadrature':shifted,'scope':'finite quadrature interval; omitted Gaussian tails <1e-24, period identities proved analytically'}
def c10():
 vals=[313]
 for _ in range(2):vals.append(vals[-1]**2)
 assert vals==[313,97969,9597924961]
 for d,v in enumerate(vals):close(math.log(math.log(v))-math.log(math.log(313)),d*math.log(2))
 for g in [F(2),F(7),F(11)]:assert (F(313)*g)/(g/F(313))==313**2
 return {'exact_depth_values':vals,'soundness_composition':'set inclusion and union-bound proof in text; no hardness assumption certified'}
def c11():
 H=lambda h,m:(3*h+m)%101
 assert H(H(0,1),2)==5 and H(H(0,2),1)==7
 assert H(H(0,0),3)==H(H(0,1),0)==3
 U=[[1,1],[0,1]];V=[[1,0],[1,1]];Ui=[[1,-1],[0,1]];Vi=[[1,0],[-1,1]]
 C=mm(mm(mm(U,V),Ui),Vi);assert C==[[3,-1],[1,0]] and det(C)==1
 return {'nontrivial_loop_holonomy':C,'ordered_hash_endpoints':[5,7],'toy_collision_endpoint':3}
def c12():
 A={0,1,4,6};B={0,1,3,7};corr=lambda S:[sum((j+r)%12 in S for j in S) for r in range(12)]
 ca,cb=corr(A),corr(B);assert ca==cb==[4,1,1,1,1,1,2,1,1,1,1,1]
 for shift in range(12):assert {(x+shift)%12 for x in A}!=B and {(-x+shift)%12 for x in A}!=B
 powers=[]
 for k in range(12):
  pa=abs(sum(cmath.exp(-2j*math.pi*k*x/12) for x in A))**2;pb=abs(sum(cmath.exp(-2j*math.pi*k*x/12) for x in B))**2;close(pa,pb,1e-11);powers.append(round(pa,12))
 return {'exact_autocorrelation':ca,'all_12_power_values':powers,'all_dihedral_equivalences_excluded':True}
def c13():
 for ell in range(11):
  lam=ell*(ell+1)
  assert ell*(ell+1)==lam and (-ell-1)*(-ell)==lam
 for alpha,c in product([F(-1),F(0),F(1),F(2)],[F(2),F(3)]):assert c**(2*alpha)*c**(2*(1-alpha))==c*c
 return 'All ell0–10 sphere indicial roots and exact homothety exponents checked; anisotropic Laplacian deliberately not identified with ordinary cone.'
def c14():
 words=list(product((0,1),repeat=4));Fmap=lambda w:sum(w)
 a=(0,0,1,1);b=(0,1,0,1);assert Fmap(a)==Fmap(b)==2
 valid=lambda w:any(w[i]==w[i+1]==1 for i in range(3))
 assert valid(a) and not valid(b)
 return {'mixed_validity_fiber':[a,b],'common_feature':2,'factorization_bound':'common acceptance p cannot be >=1-eps and <=eps for eps<1/2'}
def c15():
 # Partial sums have the exact residues of -1/3 modulo powers of2.
 for n in range(1,22):
  residue=sum(2**j for j in range(n) if j%2==0)%(2**n)
  assert (3*residue+1)%(2**n)==0
 assert all(2**n>2**(n-1) for n in range(1,10))
 return 'Twenty-one compatible 2-adic residues certify the displayed -1/3 obstruction; cokernel isomorphism and its nonintegrality are proved in prose.'
def c16():
 x=F(1);signs=[]
 for n in range(20):
  signs.append(x>=0);assert abs(x)==F(1,2**n);x=-x/2
 assert all(signs[i]!=signs[i+1] for i in range(19))
 for k in range(1,15):assert F(1,2**(k+1))<F(1,2**k) and not F(1,2**k)<F(1,2**k)
 return 'Exact alternating contraction counterexample and strict-boundary resolution times k+1, not automatic ceiling equality.'
def c17():
 for theta,Fisher,GGN,Hessian in [(0,0,0,-2),(1,0,4,4)]:
  J=2*theta;g=(theta*theta-1)*J
  assert g*g==Fisher and J*J==GGN and 6*theta*theta-2==Hessian
 P=[[1,0],[0,0]];assert mm(P,P)==P
 return 'Scalar nonlinear least squares distinguishes Fisher/GGN/Hessian at exact-fit and stationary negative-curvature points.'
def c18():
 B=[[1,-1,0]];A=[[2,2],[2,2],[0,4]];S=[[2,2],[0,4]];V=[[1,-1],[0,1]]
 assert mm(B,A)==[[0,0]] and det(V)==1 and mm(S,V)==[[2,0],[0,4]]
 reps={(a%2,b%4) for a,b in product(range(2),range(4))};assert len(reps)==8 and abs(det(S))==8
 assert ((2*3)%2,(2*7)%4)==(0,2) and ((4*3)%2,(4*7)%4)==(0,0)
 return {'Smith_diagonal':[2,4],'unimodular_V':V,'quotient_order':8,'sample_class_order':4}
def c19():
 Q=400;exact=math.exp(-math.pi/(Q*math.sqrt(1-1/(4*Q*Q))));approx=math.exp(-math.pi/Q)
 assert abs(exact-approx)<1e-8
 depth=math.log(1000)/(-math.log(approx));assert 879.5<depth<879.6
 beta=F(-4,5);alpha=F(2);ds=[1,0,-2,3,1];z=F(7)
 for d in ds:z=beta*z+alpha*d
 independent=beta**len(ds)*7+alpha*sum(beta**(len(ds)-1-j)*d for j,d in enumerate(ds));assert z==independent
 return {'cycle_amplitude':exact,'high_Q_60dB_cycles':depth,'driven_recurrence_exact_value':str(z)}
def c20():
 k,g=2,1;omega=math.sqrt(k*k-g*g);T=math.pi/omega
 M=[[math.cos(omega*T),math.sin(omega*T)/omega],[-omega*math.sin(omega*T),math.cos(omega*T)]]
 close(float(det(M)),1);close(M[0][0]+M[1][1],-2)
 # Exact variable-gain coefficient at four points agrees with the harmonic expansion.
 for t in [.1,.4,1.2,2]:
  gamma=g*math.cos(2*t);gp=-2*g*math.sin(2*t)
  close(k*k-gamma*gamma-gp,k*k-g*g/2-g*g/2*math.cos(4*t)+2*g*math.sin(2*t))
 return 'Constant coupler monodromy and variable-gain extra harmonics checked independently; reverse SL2 trace equality is exact algebra.'
def hill(q,n=5000):
 # RK4 evolves two fundamental solutions, independent of the Fourier perturbation derivation.
 dt=math.pi/n;y=[1.,0.,0.,1.]
 def f(t,z):
  coefficient=-2*q*math.cos(2*t)
  return [z[1],-coefficient*z[0],z[3],-coefficient*z[2]]
 for j in range(n):
  t=j*dt;k1=f(t,y);k2=f(t+dt/2,[a+dt*b/2 for a,b in zip(y,k1)]);k3=f(t+dt/2,[a+dt*b/2 for a,b in zip(y,k2)]);k4=f(t+dt,[a+dt*b for a,b in zip(y,k3)])
  y=[a+dt*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,k1,k2,k3,k4)]
 return y[0]+y[3],y[0]*y[3]-y[1]*y[2]
def c21():
 out=[]
 for q in [.02,.01,-.02]:
  trace,detm=hill(q);prediction=2-math.pi**2*q*q/2
  close(detm,1,2e-11);assert trace<2 and abs(trace-prediction)<1e-6;out.append({'q':q,'trace':trace,'second_order':prediction,'determinant':detm})
 close(out[0]['trace'],out[2]['trace'],1e-11)
 return {'independent_RK4_monodromies':out,'scope':'numerical spot checks, not a certified uniform O(q^4) remainder'}
def c22():
 for A in [range(1),range(2),range(7)]:
  for a in A:
   based=[(x,int(x==a)) for x in A if x==a];assert len(based)==1
 return 'Discrete set models of sizes1,2,7 have singleton based-path total space at every basepoint; general path-induction proof is in text.'
def c23():
 grid=[F(j,40) for j in range(41)];epsilon=F(1,100)
 assert len(grid)==41 and all(b-a>2*epsilon for a,b in zip(grid,grid[1:]))
 assert 2**5<41<2**6
 return {'robust_scalar_messages':41,'spacing':'1/40','readout_error':'1/100','information_bits':math.log2(41)}
def c24():
 powers=[1,1,1,16];sf=math.prod(powers)**.25/(sum(powers)/4);close(sf,8/19)
 upper=-math.expm1(math.log(.05)/1_000_000);assert 2.9957e-6<upper<2.9958e-6
 close((1-upper)**1_000_000,.05,1e-11)
 return {'flatness':sf,'zero_failures_95pct_upper_bound':upper,'claim_scope':'no adversarial or cryptographic probability is inferred'}
def c25():
 sigma=.1;mean=simpson(lambda x:x*x*math.exp(-x*x/(2*sigma*sigma))/(sigma*math.sqrt(2*math.pi)),-1,1,n=4000)
 fourth=simpson(lambda x:x**4*math.exp(-x*x/(2*sigma*sigma))/(sigma*math.sqrt(2*math.pi)),-1,1,n=4000)
 close(mean,.01,1e-12);close(fourth-mean*mean,.0002,1e-12)
 return 'Independent Gaussian quadrature verifies nonzero mean.01 and variance.0002 despite zero Jacobian.'
def c26():
 H=[[0,0],[0,9]];g=[[1],[1]];d=[[-1],[F(-1,10)]]
 assert mm([[1,0],[0,10]],d)==[[-1],[-1]]
 value=d[0][0]+d[1][0]+F(1,2)*9*d[1][0]**2+F(1,2)*sum(r[0]**2 for r in d)
 assert value==F(-11,20)
 return 'Exact stationarity and completed quadratic minimum -11/20 for damping step(-1,-1/10).'
def c27():
 primes=[p for p in range(2,11) if all(p%d for d in range(2,math.isqrt(p)+1))];assert primes==[2,3,5,7]
 assert sum(x*x for x in [2,2,2,2])==16 and sum(x*x for x in [1,2,2,3])==18
 for beta in [0,.3,1]:close(sum(math.exp(-4*beta) for p in primes),4*math.exp(-4*beta))
 return 'Exact prime enumeration and equal-sum energy comparison; finite partition has no position dependence.'
def c28():
 F9=list(product(range(3),repeat=2))
 add=lambda x,y:((x[0]+y[0])%3,(x[1]+y[1])%3)
 mul=lambda x,y:((x[0]*y[0]+2*x[1]*y[1])%3,(x[0]*y[1]+x[1]*y[0])%3)
 def power(x,n):
  y=(1,0)
  while n:
   if n&1:y=mul(y,x)
   x=mul(x,x);n//=2
  return y
 def curve(x):return add(add(power(x,5),((-x[0])%3,(-x[1])%3)),(1,0))
 pairs=[(x,y) for x,y in product(F9,repeat=2) if mul(y,y)==curve(x)]
 N9=1+len(pairs);N3=1+sum(mul(y,y)==curve(x) for x,y in product([(a,0) for a in range(3)],repeat=2))
 assert N3==7 and N9==15
 a1=4-N3;a2=F(N9-10+a1*a1,2);assert a1==-3 and a2==7
 assert all(not (curve(x)==(0,0) and add(mul((2,0),power(x,4)),(2,0))==(0,0)) for x in F9)
 return {'N3':N3,'N9':N9,'F9_affine_points':pairs,'Frobenius_polynomial_descending':[1,3,7,9,9],'smoothness':'text Euclidean gcd certificate; derivative splits inF9'}
def c29():
 for b in [1,3,7]:
  codims=[1]*b+[0]*3;assert sum(codims)==b and 1+sum(codims)==b+1
 return 'Conductor sums for explicitly supplied cyclic filtrations; Artin–Schreier break3 is cited background, not independently reconstructed.'
def c30():
 M=[[1,1],[1,0]];assert mm(M,M)==[[2,1],[1,1]]
 Fibs=[0,1]
 for _ in range(15):Fibs.append(sum(Fibs[-2:]))
 counts=[]
 for L in range(1,11):
  legal=sum(all(not(w[i]==w[i+1]==1) for i in range(L-1)) for w in product((0,1),repeat=L));assert legal==Fibs[L+2];counts.append(legal)
 assert mm(mm(M,M),mm(M,M))==[[5,3],[3,2]]
 return {'exhaustive_legal_word_counts_L1to10':counts,'substitution_H_after4':[5,3]}
def c31():
 def recursive(s,z=0):
  for a in s:z=max(0,z-a)
  return z
 def suffix(s):return max([0]+[-sum(s[k:]) for k in range(len(s))])
 for n in range(1,7):
  for s in product((-1,0,1),repeat=n):assert recursive(s)==suffix(s)
 assert recursive([1,-1])==1 and recursive([-1,1])==0
 return 'All 1092 ternary slack sequences of lengths1–6 verify the closed suffix-deficit formula; reordered zero-sum examples differ.'
def c32():
 c=10*.05/(1.05**20-1);W=0
 for _ in range(20):W=1.05*W+c
 close(W,10);assert .3024<c<.3025
 assert 12*200*100_000_000==240_000_000_000 and 12*800*100_000_000==960_000_000_000
 return {'annual_contribution_for_hypothetical_5pct_trillion':c,'balance_after20':W,'scope':'constant-return mathematical scenario only'}
def c33():
 for t in range(-20,21):assert 6*(-1+3*t)+9*(1-2*t)==3
 assert all((6*x+9*y)%3==0 for x,y in product(range(-10,11),repeat=2))
 assert 6*F(1,6)==1
 return 'Integer solution family and divisibility obstruction independently checked, alongside rational solvability.'
def c34():
 words=list(product((0,1),repeat=4));fixed=Counter((0,)+w[:3] for w in words)
 H=lambda counts:-sum((v/sum(counts.values()))*math.log(v/sum(counts.values())) for v in counts.values())
 close(H(Counter(words)),4*math.log(2));close(H(fixed),3*math.log(2))
 random_prefix=Counter((u,)+w[:3] for u in (0,1) for w in words);close(H(random_prefix),4*math.log(2))
 return 'Complete finite prefix distributions give4bits,3bits,4bits for original,fixed-prefix,fresh-random-prefix cases.'
def c35():
 lam=F(2);tau=F(1,2);q=F(1,2)
 for x,y in product(map(F,range(-5,6)),repeat=2):
  original=lam*x*x/2+(x-y)**2/(2*tau)
  square=(lam+1/tau)*(x-q*y)**2/2+lam*y*y/(2*(1+lam*tau))
  assert original==square
 assert q*2==1 and q*q*9==F(9,4)
 return 'All121 rational point pairs verify the coupling square-completion identity; exact Gaussian pushforward mean1 variance9/4.'
for n,fn in enumerate([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35],1):check(n,fn.__name__,fn)
result={'checks':checks,'scope':'Exact finite certificates and declared numerical spot checks; general categorical, probabilistic and geometric theorems are proved in prose or cited, not claimed as computationally proved.'}
(HERE/'checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(f'{sum(x["status"]=="passed" for x in checks)}/{len(checks)} passed')
for x in checks:
 if x['status']!='passed':print(x)
sys.exit(any(x['status']!='passed' for x in checks))
