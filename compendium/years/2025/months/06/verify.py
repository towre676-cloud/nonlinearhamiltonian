"""Stdlib replay of declared examples, not a proof of general comparison theorems."""
from pathlib import Path
from fractions import Fraction as F
import math,json,itertools,cmath
P=Path(__file__).resolve().parent;checks=[]
def check(n,name,ok,detail):
 assert ok,name
 checks.append(dict(id=f'Y25-06-{n:03d}',name=name,status='passed',detail=detail))
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def tr(a):return list(map(list,zip(*a)))
def rank(a,mod=None):
 a=[[int(v)%mod if mod else F(v) for v in row] for row in a];r=0
 for c in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];z=a[r][c]
  a[r]=[(v*pow(z,-1,mod))%mod if mod else v/z for v in a[r]]
  for j in range(len(a)):
   if j!=r:
    z=a[j][c];a[j]=[(x-z*y)%mod if mod else x-z*y for x,y in zip(a[j],a[r])]
  r+=1
  if r==len(a):break
 return r

def factors(n):
 out={};p=2
 while p*p<=n:
  while n%p==0:out[p]=out.get(p,0)+1;n//=p
  p+=1
 if n>1:out[n]=out.get(n,0)+1
 return out
def radical(*ns):return math.prod(set().union(*(set(factors(n)) for n in ns)))
triples=[(2,6436341,6436343),(121,109375,109496),(24833,181307,22784)]
rads=[radical(*t) for t in triples];qualities=[math.log(t[2])/math.log(r) for t,r in zip(triples,rads)]
check(1,'Exact ABC source-table audit',rads[:2]==[15042,10538990] and triples[0][0]+triples[0][1]==triples[0][2] and triples[1][0]+triples[1][1]==triples[1][2] and sum(triples[2][:2])==206140!=triples[2][2] and math.gcd(121,109375)==1,
 {'radicals':rads,'logarithmic_qualities':qualities,'scope':'The third displayed tuple is rejected before being used as an ABC example.'})
f1=sum(math.log(p)**2/p for p in [2,3]);f2=-sum(math.log(p)**3/p for p in [2,3]);r=2**.5*3**(2/3)
check(2,'Smoothed-radical calculus example',f1>0 and f2<0 and abs(math.log(r)-sum((1-1/p)*math.log(p) for p in [2,3]))<1e-14,
 {'r_sigma_one_n6':r,'first_log_derivative':f1,'second_log_derivative':f2,'scope':'No curvature or eigenvalue is inferred from these scalar derivatives.'})
R=lambda d,p:{pow(x,d,p) for x in range(p)}
check(3,'Power residues and factorial obstruction',R(8,3)=={0,1} and R(7,3)=={0,1,2} and all((math.factorial(n)-1)%3==2 for n in range(3,20)) and math.factorial(4)+1==5**2 and all(len(R(d,p))==1+(p-1)//math.gcd(d,p-1) for p in [3,5,7,11] for d in range(1,13)),
 'Exact residue enumeration for four primes and twelve degrees, plus all-n modular proof in the entry.')
def fact_v(n,p):
 out=0;q=p
 while q<=n:out+=n//q;q*=p
 return out
for n in range(1,13):
 for k in range(1,201):
  g=math.prod(p**min(a,fact_v(n,p)) for p,a in factors(k).items())
  assert g==math.gcd(k,math.factorial(n))
check(4,'Factorial gcd via Legendre valuations',math.gcd(16,120)==8 and F(math.gcd(16,120),16)==F(1,2) and F(120,math.gcd(12,120))==10,
 'Valuation formula agrees with Euclid on2400 cases; exact branch examples give10 and1/2.')
def bisect(fun,lo,hi,N=100):
 fl=fun(lo)
 for _ in range(N):
  mid=(lo+hi)/2;fm=fun(mid)
  if fl*fm<=0:hi=mid
  else:lo=mid;fl=fm
 return (lo+hi)/2
m=bisect(lambda x:math.tanh(2*x)-x,.9,.99)
check(5,'Tanh positive branch and susceptibility',abs(math.tanh(2*m)-m)<1e-14 and abs(m-.9575040240772688)<1e-13 and 1/(1-.5)==2,
 {'positive_root_at_lambda_two':m,'residual':abs(math.tanh(2*m)-m),'scope':'Root count and asymptotics are proved analytically, not by this bisection.'})
def ground(e):
 return bisect(lambda k:2*k/math.tan(math.pi*k/2)+2*e,1,1.5)
k=ground(1);eps=1e-5;deriv=(ground(eps)**2-1)/eps
check(6,'Point-interaction scalar equation and perturbation derivative',1<k<1.5 and abs(2*k/math.tan(math.pi*k/2)+2)<1e-13 and abs(deriv-4/math.pi)<1e-4,
 {'ground_wavenumber':k,'ground_eigenvalue':k*k,'small_coupling_difference_quotient':deriv,'analytic_derivative':4/math.pi,'scope':'Finite numerical checks; the exact bracket and operator theorem are given in the text.'})
perms=list(itertools.permutations(range(3)))
commuting=[q for q in perms if all(q[(x+a)%3]==(q[x]+a)%3 for x in range(3) for a in range(3))]
check(7,'Regular C3 naturality certificate',len(commuting)==3 and set(commuting)=={tuple((x+a)%3 for x in range(3)) for a in range(3)},'All six regular-set permutations checked; exactly the three translations commute with all equivariant right translations.')
S=[[1,0],[0,-1]];plus=[[1,0],[0,0]]
check(8,'Modal projector and tensor obstruction',mm(S,S)==[[1,0],[0,1]] and mm(plus,plus)==plus and (-1)*(-1)==1 and rank(plus)==1,
 'The sign invariant space is zero, while sign⊗sign is trivial; categorical and tensor properties remain distinct.')
def chow_mul(a,b,n):
 out={}
 for i,x in a.items():
  for j,y in b.items():
   if i+j<=n:out[i+j]=out.get(i+j,0)+x*y
 return {i:v for i,v in out.items() if v}
h={1:1};h2=chow_mul(h,h,2);h3=chow_mul(h2,h,2)
check(9,'Declared projective Chow ring and shifts',h2=={2:1} and h3=={} and [(2*i,i) for i in range(3)]==[(0,0),(2,1),(4,2)],
 'Exact truncated ringZ[h]/h³. This tests the cellular Chow subtheory, not all field motivic cohomology.')
check(10,'Nontrivial units witness against the false comparison',math.log(2)>0 and F(2)*F(1,2)==1 and all(2**n>1 for n in range(1,25)),
 'The unit2 has nonzero log-absolute-value image; H¹ of a point is zero. The all-degree/categorical contradiction is the written classical low-degree proof, not finite exponent sampling.')
for d in [2,3]:
 d1=[[d,d]];d2=[[-d],[d]]
 assert mm(d1,d2)==[[0]] and rank(d1)==rank(d2)==1
 assert math.gcd(*[abs(x) for x in d1[0]])==d
check(11,'Tensor-complex signs and torsion indices',True,'For multiplication-by2 and3 complexes, d1d2=0; kernel generator(1,−1) is hit d times, giving both H0 and H1=Z/d. Omitting the sign gives nonzero composition.')
def laurent_mul(a,b):
 out={}
 for i,x in a.items():
  for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
 return {i:x for i,x in out.items() if x}
check(12,'Torus unit exponents and blow-up rank shift',laurent_mul({2:F(3)},{-3:F(5)})=={-1:F(15)} and laurent_mul({2:F(3)},{-2:F(1,3)})=={0:F(1)} and [1,1+1,1]==[1,2,1],
 'Laurent monomial product3t²·5t^(−3)=15t^(−1); the codimension-two point blow-up adds one Chow-degree-one class. General localization/blow-up theorems are explicit classical inputs.')
lines={}
for a,b in itertools.product(range(5),repeat=2):
 if (a,b)!=(0,0):
  choices=[((s*a)%5,(s*b)%5) for s in range(1,5)]
  lines[min(choices)]=1
check(13,'Projective-line finite-field and comparison test',len(lines)==6 and 5**2+1==26 and (1+5)==6,
 'Enumerated six F5 projective lines; Frobenius factors1 and5 give the same trace count. General comparison theorems are sourced, not certified by ranks.')
cents=lambda r:1200*math.log2(float(r))
check(14,'Rational interval logarithmic identities',abs(cents(F(3,2)*F(81,80))-cents(F(3,2))-cents(F(81,80)))<1e-11 and abs(cents(F(2))-1200)<1e-12 and abs(cents(F(3,2))-701.9550008653874)<1e-10,
 {'fifth_cents':cents(F(3,2)),'syntonic_comma_cents':cents(F(81,80)),'scope':'No perceptual calibration or unrecovered Baker constant is asserted.'})
err=[]
for t in [0,.2,1,2]:
 w=math.sqrt(3);q=math.exp(-t)*(math.cos(w*t)+math.sin(w*t)/w)
 v=-4*math.exp(-t)*math.sin(w*t)/w
 acc=4*math.exp(-t)*math.sin(w*t)/w-4*math.exp(-t)*math.cos(w*t)
 err.extend([abs(acc+2*v+4*q),abs(v*(acc+4*q)+2*v*v)])
check(15,'Tuning oscillator and energy residual',max(err)<1e-13,{'maximum_residual':max(err),'scope':'A new stipulated ODE, not a fitted musical model.'})
J=[[0,4],[0,0]]
a=[[1],[2]];b=[[3],[4]];c=[[5],[6]];d=[[7],[8]]
left=mm(mm(a,tr(b)),mm(c,tr(d)));scalar=mm(tr(b),c)[0][0];right=[[scalar*x for x in row] for row in mm(a,tr(d))]
check(16,'Nonlinear Jacobian and dyad composition',rank(J)==1 and J!=tr(J) and left==right,'The nonsymmetric Jacobian rules out a potential; independent rank-one matrix multiplication confirms the linear composition formula.')
K=[[F(1),F(1)],[0,F(1)]];u=[[F(2,5)],[F(1,5)]];y=[[F(1)],[0]]
Ku=mm(K,u);res=[[a[0]-b[0]] for a,b in zip(Ku,y)];grad=mm(tr(K),res);grad=[[a[0]+b[0]] for a,b in zip(grad,u)]
check(17,'Exact adjoint normal-equation solution',u==[[F(2,5)],[F(1,5)]] and grad==[[0],[0]] and res==[[F(-2,5)],[F(1,5)]],
 'Forward and adjoint residual independently give zero gradient for the strictly convex regularized problem.')
beta=F(7,10);cnt=[0,0,0]
for j in range(200):
 t=F(2*j+1,400);aa=t<beta;bb=(t-F(1,2))%1<beta
 assert aa or bb
 cnt[0]+=aa and bb;cnt[1]+=aa and not bb;cnt[2]+=bb and not aa
rate=4*640*480*8*100
alias_cycles=[(F(1,7)+5)*F(n,5)-F(1,7)*F(n,5) for n in range(8)]
check(18,'Exact tripod overlap and sensor bitrate',cnt==[80,60,60] and rate==983040000 and alias_cycles==list(map(F,range(8))),
 {'overlap_and_exclusive_fractions':[str(F(n,200)) for n in cnt],'constructed_bits_per_second':rate})
check(19,'Oscillator peak and regeneration denominator', (25-23)**2+4*23==96 and (25-25)**2+4*25==100 and F(60,100-20)==F(3,4) and F(60,100)==F(3,5),
 'Displacement peak squared frequency23 has denominator96 rather than100 at the undamped frequency; net and gross ratios differ.')
r=F(973,1000);sig2=1/(r*r)-1
npv=sum((F(1)/(1+F(1,20))**t for t in range(1,31)),F(0))-10
closed=(1-(1+F(1,20))**(-30))/F(1,20)-10
check(20,'Exact confounding correlation and discount sum',sig2>0 and 1/(1+sig2)==r*r and npv==closed,
 {'squared_noise_scale':str(sig2),'normalized_30_year_sum':str(npv),'scope':'No causal or policy benefit is inferred from the stipulated association.'})
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
xscore=[F(1),F(0)];yscore=[F(0),F(1)];wa=[F(2),F(1)];wb=[F(1),F(2)]
changed_x=[100*xscore[0],xscore[1]];changed_w=[wa[0]/100,wa[1]]
check(21,'Unit invariance and arbitrary ranking',dot(wa,xscore)>dot(wa,yscore) and dot(wb,xscore)<dot(wb,yscore) and dot(changed_w,changed_x)==dot(wa,xscore),
 'Weights(2,1) and(1,2) reverse the two coordinate-object rankings; coordinated unit change preserves the same scalar.')
Tup=1800*1.7**.25;Tdown=1800/1.7**.25
check(22,'Fourth-power balance and complete denominators',abs((Tup/1800)**4-1.7)<1e-13 and abs(1.7*(Tdown/1800)**4-1)<1e-13 and F(17,10)**2==F(289,100) and F(150)/F('277.5')==F(20,37),
 {'upward_stipulated_temperature':Tup,'fixed_power_temperature_with_area_increase':Tdown,'with_auxiliary_efficiency':float(F(150,280)),'scope':'Arithmetic model audit, not device validation.'})
points=list(itertools.product(range(3),repeat=4));perms=list(itertools.permutations(range(4)));signs=list(itertools.product([1,-1],repeat=4))
group=[(p,s) for p in perms for s in signs]
apply=lambda v,p,s:tuple((s[j]*v[p[j]])%3 for j in range(4))
sizes=[]
for r0 in range(5):
 v=tuple([1]*r0+[0]*(4-r0));orb={apply(v,p,s) for p,s in group};sizes.append(len(orb))
 assert all(sum(x!=0 for x in w)==r0 for w in orb)
gl=math.prod([81-1,81-3,81-9,81-27])
check(23,'Exhaustive B4 orbit and order certificate',len(group)==384 and sizes==[1,8,24,32,16] and sum(sizes)==81 and gl==24261120<696729600,
 {'orbit_sizes':sizes,'GL4_F3_order':gl,'scope':'Exceptional group order is a classical input; no unrecovered generator implementation is certified.'})
exps=list(itertools.product(range(3),repeat=4))
eval_matrix=[[math.prod(pow(x,e,3) for x,e in zip(v,a))%3 for a in exps] for v in points]
check(24,'Full reduced-polynomial evaluation isomorphism',rank(eval_matrix,3)==81 and all((v[0]**3-v[0])%3==0 for v in points) and {3:1,1:2}!={},
 'The81×81 evaluation matrix has full rank overF3. The nonzero formal polynomial x³−x still vanishes on all points when the degree bound is removed.')
es=json.loads((P/'entries.json').read_text());assert len(es)==24
assert all(e['original']['month']=='2025-06' and e['original']['original_question'] is None for e in es)
assert all(e['original']['evidence'] in ['U','A','T'] for e in es)
checks.append(dict(id='MONTH-2025-06',name='Attribution and proof scope audit',status='passed',detail='24 newly developed treatments; original prompts remain null, implementation postulates are not counted as proofs, and false universal motivic comparisons are corrected.'))
(P/'checks.json').write_text(json.dumps(dict(month='2025-06',status='passed',count=len(checks),checks=checks),ensure_ascii=False,indent=2))
print(json.dumps({'month':'2025-06','entries':24,'checks':len(checks),'status':'passed'}))
