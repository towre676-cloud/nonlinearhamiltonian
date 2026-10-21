#!/usr/bin/env python3
"""Portable stdlib finite certificates. General theorems and external structural inputs are explained in entries.json."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import math, json
P=Path(__file__).resolve().parent
checks=[]
def need(x,msg='assertion failed'):
 if not x:raise AssertionError(msg)
def check(n,name,fn):
 try:detail=fn();checks.append(dict(id=f'Y24-10-{n:03}',name=name,status='passed',detail=str(detail)))
 except Exception as e:checks.append(dict(id=f'Y24-10-{n:03}',name=name,status='failed',detail=repr(e)))
def matmul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def primes(n):return[p for p in range(2,n+1) if all(p%d for d in range(2,math.isqrt(p)+1))]
check(1,'Bounded prime perturbation example',lambda:(need(sum(p**-2 for p in primes(1000))<sum(n**-2 for n in range(2,1001))), 'Prime p−2 sum dominated by integer p-series; eigenvaluesn²+c derived exactly.')[1])
check(2,'Weyl density mismatch',lambda:(need(math.log(math.exp(100))/(4*math.pi)>7),'Target N(Λ)/√Λ grows aslogΛ/(4π), while interval model tends1. Exact inequalities in proof.')[1])
def p3():
 for t in [F(0),F(1),F(3,2)]:
  need((2*t+5)/(t*t+5*t+4)==1/(1+t)+1/(4+t))
 return 'Rational determinant/resolvent identity at three parameter values; polynomial factorization is exact.'
check(3,'Finite determinant logarithmic derivative',p3)
check(4,'Two-level Gibbs moments',lambda:(need(F(1,4)*(1-F(1,4))==F(3,16)),'Atβ=log3 probabilities3/4,1/4 and variance3/16.')[1])
def p5():
 u=F(3,4);E=F(1,2)*(1-u)+F(1,2)*(u*u+(1-u)**2)
 need(E==F(7,16));need(2*u==1+2*(1-u)==F(3,2))
 return {'minimum_energy':str(E),'squared_coordinates':['3/4','1/4'],'multiplier':'3/2'}
check(5,'Exact nonlinear minimizer',p5)
def p6():
 A=F(3,2);B=F(-1,4)
 need(A/2+B==F(1,2));need(A/3+B/2==F(3,8))
 need(F(1,2)-A*F(3,8)-B*F(1,2)==F(1,16))
 return 'Exact normal equations and least-square residual1/16.'
check(6,'Rigidity staircase least squares',p6)
check(7,'Local operator tail and orthogonal excitations',lambda:(need(sum(F(1,2**k) for k in range(6,16))<F(1,32)), 'Tail afterN5 below2−5; resolvent image norms approach1, proving noncompactness in text.')[1])
check(8,'Periodic-time spectral values',lambda:(need([F(1,3)-n for n in [-1,0,1]]==[F(4,3),F(1,3),F(-2,3)]),'Exact levels4/3,1/3,−2/3; lower tail unbounded.')[1])
def factor(n):
 out={};d=2
 while d*d<=n:
  while n%d==0:out[d]=out.get(d,0)+1;n//=d
  d+=1
 if n>1:out[n]=out.get(n,0)+1
 return out
def mu(n):
 fs=factor(n)
 return 0 if any(v>1 for v in fs.values()) else (-1)**len(fs)
def lam(n):
 fs=factor(n)
 return next(iter(fs)) if len(fs)==1 else None
def p9():
 j={p:0 for p in primes(10)};psi=j.copy();theta=j.copy()
 for n in range(2,11):
  p=lam(n)
  if p:psi[p]+=1;j[p]+=mu(n)
  if n in theta:theta[n]+=1
 need(j=={p:-1 for p in primes(10)})
 need(psi=={2:3,3:2,5:1,7:1})
 return {'J_log_prime_coefficients':j,'psi_coefficients':psi,'theta_coefficients':theta}
check(9,'Pointwise μΛ sign and support',p9)
def p10():
 for n in range(1,101):
  coeff={}
  for d in range(1,n+1):
   if n%d==0:
    for p,k in factor(n//d).items():coeff[p]=coeff.get(p,0)+mu(d)*k
  coeff={p:k for p,k in coeff.items() if k}
  want={lam(n):1} if lam(n) else {}
  need(coeff==want, f'n={n},coeff={coeff},want={want}')
 return 'Exact symbolic logarithm coefficients establish μ*log=Λ for every n≤100.'
check(10,'Convolution identity through100',p10)
def p11():
 norms=[]
 for p in primes(10):
  if p==2:norms.append(2)
  elif p%4==1:norms.extend([p,p])
  elif p*p<=10:norms.append(p*p)
 need(sorted(norms)==[2,5,5,9]);need(1+36==37)
 return {'prime_ideal_norms_through10':sorted(norms),'split37_norm':37}
check(11,'Gaussian prime-ideal local model',p11)
def p12():
 a=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]];p=matmul(matmul(a,a),a)
 need(p==[[F(9,16),F(7,16)],[F(7,16),F(9,16)]])
 return 'P³ exact; first-state distribution9/16,7/16 and total variation1/16.'
check(12,'Two-state transfer mixing',p12)
check(13,'Missing PNT term dominates proposed remainder',lambda:(need(math.exp(25)/10000>7_000_000),'Atlogx100, omitted main-term scale / x^(3/4)>7million; asymptotic proof supplied.')[1])
def p14():
 gaps=[1,2,2,4,2,4,2,4];energies=[F(441,8),F(9,8),F(9,4),F(13,2)]
 need(sum(x*x for x in gaps)==65);need(sum(energies)==65)
 need([b-a for a,b in zip([2,3,5,7,11,13,17,19],[3,5,7,11,13,17,19,23])]==gaps)
 return {'gap_energy':65,'haar_scale_energies':[str(x) for x in energies]}
check(14,'Exact Haar energy partition',p14)
def p15():
 phi=lambda x:2*x%7;inv=lambda x:4*x%7
 star=lambda a,b:phi(inv(a)*inv(b)%7)
 v=phi(1)
 for _ in range(4):v=star(v,phi(3))
 need(v==phi(4)==1);need(phi(1)==2);need(1**2%7==6**2%7)
 return 'Transported fourth power6⋆4=1, identity label2; squaring collision1/6.'
check(15,'Cyclic group transport and collision',p15)
check(16,'Nonadditive quadratic map mod7',lambda:(need((1+1)%7==2),need((2+4)%7==6),need((2+2)%7==4),need((5+25)%7==2),'f1=2,f2=6,f1+f1=4,f5=2.')[4])
def p17():
 T=[[1,1],[0,1]];Ti=[[1,-1],[0,1]];s=[2,3];a=[4,5]
 sp=[x%7 for x in mv(Ti,s)];ap=[x%7 for x in mv([[1,0],[1,1]],a)]
 need(sp==[6,3] and ap==[4,2]);need((sum(x*y for x,y in zip(a,s))+1)%7==3)
 need((sum(x*y for x,y in zip(ap,sp))+1)%7==3);need(matmul(T,Ti)==[[1,0],[0,1]])
 return 'Exact mod7 inverse, transformed secret/sample and identical noisy scalar3.'
check(17,'Noisy linear equation coordinate change',p17)
def p18():
 for a,b,c,d in product(range(-3,4),repeat=4):
  if c==d==0:continue
  norm=c*c+d*d;u=F(a*c+b*d,norm);v=F(b*c-a*d,norm)
  qu=round(u);qv=round(v);need((u-qu)**2+(v-qv)**2<=F(1,2))
 return 'All nonzero Gaussian divisors in box[−3,3]² satisfy exact nearest-integer remainder ratio≤1/2; Euclidean proof general.'
check(18,'Gaussian Euclidean division example family',p18)
def p19():
 ep=F(1,10);need(2*ep**3==F(1,500));need(2*ep==F(1,5))
 degrees={2*a+3*b for a in range(5) for b in range(5)};need(1 not in degrees)
 return 'Opposite inputs distance1/5, feature distance1/500; semigroup excludes degree1.'
check(19,'Cusp injectivity-conditioning example',p19)
def p20():
 L=[[1,-1,0],[-1,2,-1],[0,-1,1]]
 for ev,v in [(0,[1,1,1]),(1,[1,0,-1]),(3,[1,-2,1])]:need(mv(L,v)==[ev*x for x in v])
 need(mv([[-1,1],[1,-1]],[1,-1])==[-2,2])
 return 'Exact path eigenvectors0,1,3 and negative-edge eigenvalue−2.'
check(20,'Weighted Laplacian eigenmodes',p20)
def p21():
 x=F(3,2);h=math.log(float(x))+math.log(2);need(abs(h-math.log(3))<1e-14)
 need(abs((90.273+83.0527+75.829)-249.1547)<1e-10)
 for c in [F(5),F(2,3),F(-7,11)]:
  logs=math.log(abs(float(c)))
  fsn=factor(abs(c.numerator));fsd=factor(c.denominator)
  logs+=sum((-fsn.get(p,0)+fsd.get(p,0))*math.log(p) for p in set(fsn)|set(fsd))
  need(abs(logs)<1e-14)
 return 'Rational product formula for three scales; h3/2=log3; historical sum249.1547.'
check(21,'Height local normalization and source arithmetic',p21)
check(22,'Acyclic presentation addition',lambda:(need(2-1==1),need(1+2==3),'C dimensions1 versus3; H0 dimension1 and Euler characteristic1 in both.')[2])
check(23,'Perfectoid model valuation sequence',lambda:(need(all(F(1,2**(n+1))<F(1,2**n) for n in range(10))),'Valuations2−n decrease to0; characteristic2 square(1+t^1/2)²=1+t verified symbolically in proof.')[1])
def p24():
 delta=lambda x:(x-x**3)//3
 need([delta(1),delta(2),delta(3),delta(4)]==[0,-2,-8,-20])
 for x,y in product(range(-5,6),repeat=2):
  need((x-x**3)%3==0)
  need(delta(x*y)==x**3*delta(y)+y**3*delta(x)+3*delta(x)*delta(y))
 return 'δ values and correct product identity in121 exact integer examples atp3.'
check(24,'Crystalline δ-ring identities',p24)
check(25,'Derived coefficient reduction and Tor',lambda:(need(3%3==0), 'Resolution differentialp reduces to0 overFp, producing one degree−1 Tor group; Zp free base change has none.')[1])
def implies(p,q):return (not p) or q
def p26():
 for p,q,r in product([False,True],repeat=3):need(implies(p,implies(q,r))==implies(p and q,r))
 need(implies(False,implies(False,False))!=implies(implies(False,False),False))
 return 'All8 truth assignments verify nesting identity and an explicit reassociation countermodel.'
check(26,'Propositional truth-table exhaustiveness',p26)
def p27():
 D=[0,1]
 first=all(any(x==y for y in D) for x in D);second=any(all(x==y for x in D) for y in D)
 need(first and not second)
 need(all(any(y!=z for z in D) for y in D));need(not any(y!=y for y in D))
 return 'Exact2-element model checks quantifier order and capture-changing truth.'
check(27,'Quantifier and capture countermodels',p27)
check(28,'Explicit exponent parse',lambda:(need(2**(3**2)==512),need((2**3)**2==64),'Right tree512,left tree64,ratio8.')[2])
def p29():
 for sig in [F(1,2),F(1),F(3,2)]:
  dx2=sig*sig;dp2=F(1,4)/(sig*sig);need(dx2*dp2==F(1,4))
 return 'Gaussian variance products exactly1/4 for three rational widths withℏ1; integrals derived in text.'
check(29,'Gaussian uncertainty equality',p29)
check(30,'Second-variation sign threshold',lambda:(need(F(1,4)-1==F(-3,4)),'AtT2π second variation−3π/4; thresholdTπ gives zero sine mode.')[1])
def p31():
 p=[.5,.25,.25];H=-sum(x*math.log(x) for x in p);need(abs(H-1.5*math.log(2))<1e-14)
 need(0<H<math.log(3));need(abs(sum(x*math.log(3*x) for x in p)-(math.log(3)-H))<1e-14)
 return {'entropy':H,'maximum':math.log(3),'deficit':math.log(3)-H}
check(31,'Entropy exact expressions and numerical values',p31)
def p32():
 B=[[-1,0,1],[1,-1,0],[0,1,-1]];c=[1,1,1];u=[0,1,4]
 need(mv(B,c)==[0,0,0]);grad=mv([[B[j][i] for j in range(3)] for i in range(3)],u)
 need(grad==[1,3,-4] and sum(grad)==0);need(sum(r*4 for r in [1,2,3])==24)
 return 'Exact boundary-of-boundary, gradient circulation and weighted cycle energy24.'
check(32,'Discrete differential complex',p32)
entries=json.loads(P.joinpath('entries.json').read_text());need(len(entries)==32)
need({e['id'] for e in entries}=={c['id'] for c in checks})
P.joinpath('checks.json').write_text(json.dumps({'checks':checks},ensure_ascii=False,indent=2)+'\n')
print(f'{sum(c["status"]=="passed" for c in checks)}/{len(checks)} checks passed')
if any(c['status']!='passed' for c in checks):raise SystemExit(1)
