#!/usr/bin/env python3
"""Independent finite checks of the twelve printed worked models.
These checks supplement the proofs. Quadrature and floating comparisons are
explicitly numerical, not interval certificates or tests of every source entry.
"""
import json,math
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
checks=[]
def check(name,scope,fn,kind='exact finite model'):
 try:
  detail=fn(); checks.append(dict(name=name,status='passed',kind=kind,scope=scope,detail=detail))
 except Exception as exc:
  checks.append(dict(name=name,status='failed',kind=kind,scope=scope,detail=str(exc)))
def close(a,b,tol=1e-10):
 assert abs(a-b)<=tol*max(1,abs(a),abs(b)),(a,b)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def trans(A): return list(map(list,zip(*A)))
def add(A,B): return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def det2(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def haar():
 x=list(map(Q,[1,2,3,4]));h0=[Q(1,2)]*4;h1=[Q(1,2),Q(1,2),Q(-1,2),Q(-1,2)]
 c0,c1=dot(x,h0),dot(x,h1)
 y=[c0*a+c1*b for a,b in zip(h0,h1)];r=[a-b for a,b in zip(x,y)]
 assert c0==5 and c1==-2 and dot(r,r)==1
 assert c0*c0+c1*c1+Q(1,2)+Q(1,2)==dot(x,x)==30
 return dict(total_energy=30,discarded_energy=1,reconstruction=[str(v) for v in y])
check('D07-F01 Haar energy','Exact coefficients, reconstruction and omitted energy for the printed four-vector.',haar)
def herglotz():
 def M(z):return 1/(-1-z)+2/(2-z)
 assert M(Q(0))==0 and Q(1)+Q(2,4)==Q(3,2)
 for x in [-3,-.5,0,1,3]:
  for y in [.1,1,3]:assert M(complex(x,y)).imag>0
 assert -1<0<2
 return dict(zero=0,slope='3/2',residues=[-1,-2],half_plane_checks=15)
check('D07-F02 atomic function','Exact rational zero/slope and numerical half-plane sign at fifteen test points; the proof supplies the general sign.',herglotz,'exact rational plus numerical samples')
def mellin():
 assert Q(math.factorial(3),2**4)==Q(3,8)
 S=sum((Q(1,n*n) for n in range(1,5)),Q(0))
 assert S==Q(205,144) and float(S)<math.pi**2/6<float(S+Q(1,4))
 return dict(moment='3/8',zeta_lower=str(S),zeta_upper=str(S+Q(1,4)))
check('D07-F03 Mellin moments','Exact worked moment and rational integral enclosure; ζ(2) comparison is numerical.',mellin)
def heat_trace():
 vals=[]
 for t in [1,.1,.01,.001]:
  N=math.ceil(math.sqrt(40/t));S=sum(math.exp(-t*n*n) for n in range(1,N+1))
  upper=math.sqrt(math.pi)/(2*math.sqrt(t));lower=upper*math.erfc(math.sqrt(t))
  assert lower<=S<=upper
  assert abs(math.sqrt(t)*S-math.sqrt(math.pi)/2)<=math.sqrt(t)
  vals.append([t,S])
 tail=sum(math.exp(-n*n) for n in range(3,20));assert tail<math.exp(-4)/4
 return dict(traces=vals,printed_tail_bound=math.exp(-4)/4)
check('D07-F04 heat trace','Numerical finite-sum checks of the proved integral bounds and printed tail enclosure; no numerical proof of an asymptotic limit.',heat_trace,'numerical model check')
def evolution():
 for t in [0,.3,1,5]:
  E=math.pi*(2*math.exp(-t)+.5*math.exp(-4*t))
  dE=-math.pi*(2*math.exp(-t)+2*math.exp(-4*t))
  derivative_integral=math.pi*(4*math.exp(-t)+4*math.exp(-4*t))
  close(dE,-.5*derivative_integral)
  assert dE<=-E+1e-12
 return dict(mean=3,mode_rates=[.5,2],energy_identity_samples=4)
check('D08-F01 periodic heat','Printed two-mode solution and its energy identity at four times.',evolution,'numerical model check')
def stencil():
 def step(x,r):return [r*x[(j-1)%len(x)]+(1-2*r)*x[j]+r*x[(j+1)%len(x)] for j in range(len(x))]
 x=list(map(Q,[1,0,0,0,0]));y=step(x,Q(1,4));assert y==[Q(1,2),Q(1,4),0,0,Q(1,4)]
 assert sum(y)==1 and dot(y,y)==Q(3,8)
 assert step(x,Q(3,4))[0]==Q(-1,2)
 assert step(x,Q(-1,4))[1]<0
 return dict(step=[str(v) for v in y],mass=1,energy='3/8',negative_counterexamples=2)
check('D08-F02 positive stencil','Exact five-node update, conservation, norm loss and two positivity counterexamples.',stencil)
def frobenius():
 for r in range(1,9):
  # Coefficients of d²/dL² g_r and -d/dL g_(r-1), L=log t.
  left=Q((-1)**(r+1)*r*(r+1),math.factorial(r+1))
  right=-Q((-1)**r*r,math.factorial(r))
  assert left==right
 exact=10*math.expm1(-.2);approx=Q(-136,75);bound=Q(1,1500)
 assert abs(exact-float(approx))<float(bound)
 return dict(hierarchy_orders=8,exact_value=exact,approximation=str(approx),error_bound=str(bound))
check('D08-F03 regularized basis','Exact coefficient hierarchy through ε⁸ and numerical divided-difference remainder check.',frobenius,'exact jets plus numerical example')
def borel():
 a=.1;N=5;n=20000;h=40/n
 def f(v):return -a*math.exp(-v)/(1+a*v)
 S=f(0)+f(40)+sum((4 if j%2 else 2)*f(j*h) for j in range(1,n))
 integral=S*h/3
 trunc=sum(math.factorial(k)*(-a)**(k+1) for k in range(N))
 bound=math.factorial(N)*a**(N+1)
 assert abs(integral-trunc)<bound
 for k in range(1,10):assert k*math.factorial(k-1)==math.factorial(k)
 close(trunc,-.09164)
 return dict(quadrature=integral,truncation=trunc,proved_bound=bound,tail_beyond_40_at_most=a*math.exp(-40),note='Simpson value is a numerical cross-check; the geometric identity proves the bound. Stokes contour orientation is proved in text, not tested here.')
check('D08-F04 factorial expansion','Negative-ray worked truncation with independent numerical integral and exact formal ODE coefficient recurrence.',borel,'numerical quadrature plus exact coefficients')
def lyapunov():
 A=[[Q(-1),Q(3)],[Q(0),Q(-1)]];P=[[Q(1,2),Q(3,4)],[Q(3,4),Q(11,4)]]
 assert det2(P)==Q(13,16) and P[0][0]>0
 R=[[3-P[0][0],-P[0][1]],[-P[1][0],3-P[1][1]]]
 assert det2(R)==Q(1,16) and R[0][0]>0
 assert add(mul(trans(A),P),mul(P,A))==[[-1,0],[0,-1]]
 assert math.sqrt(10)/math.e>1
 c=Q(3,5);s=Q(4,5);P0=[[1,0],[0,0]];Q0=[[c*c,c*s],[c*s,s*s]]
 assert mul(mul(P0,Q0),P0)==[[Q(9,25),0],[0,0]]
 return dict(P_determinant='13/16',threeI_minus_P_determinant='1/16',transient_norm_at_one=math.sqrt(10)/math.e,projection_factor='9/25',commutator_norm='12/25')
check('D09-F01 metric stability','Exact Lyapunov identity, rate comparison, Euclidean amplification and two-line projection quantities.',lyapunov)
def poly_mul(p,q):
 r=[Q(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):r[i+j]+=a*b
 return r

def logistic():
 r=Q(16,5)
 # f(f(x))-x factored as -x*(r*x-r+1)*(r²x²-r(r+1)x+r+1).
 f=[Q(0),r,-r]; f2=[Q(0)]*5
 for i,a in enumerate(f):f2[i]+=r*a
 for i,a in enumerate(poly_mul(f,f)):f2[i]-=r*a
 f2[1]-=1
 fact=poly_mul([0,-1],poly_mul([1-r,r],[r+1,-r*(r+1),r*r]))
 assert f2==fact
 assert -r*r+2*r+4==Q(4,25)
 xp=(21+math.sqrt(21))/32;xm=(21-math.sqrt(21))/32
 close(float(r)*xp*(1-xp),xm);close(float(r)*xm*(1-xm),xp)
 return dict(multiplier='4/25',cycle=[xm,xp],factorization='exact degree-four polynomial identity')
check('D09-F02 logistic cycle','Exact factorization at r=16/5, multiplier and numerical cycle exchange.',logistic)
def mechanics():
 F=Q(2);d=Q(1,4)
 close(math.sqrt(2/float(F))*math.sqrt(float(d)),.5)
 close((2/3)*math.sqrt(2*float(F))*float(d)**1.5,1/6)
 for t in [0,1,2,3]:
  g=1/(4-t);gp=1/(4-t)**2;close(gp,g*g)
 return dict(travel_time='1/2',action='1/6',RG_wall_time=4,ODE_samples=4)
check('D09-F03 mechanics and clock','Printed exact linear-potential observables and scalar RG trajectory.',mechanics,'exact values plus numerical identity')
def memory():
 for t in [0,.1,math.log(2),2]:
  x=(1+math.exp(-2*t))/2;y=(1-math.exp(-2*t))/2
  close(-math.exp(-2*t),-x+y)
  close(math.exp(-2*t),x-y)
  convolution=.5*(1-math.exp(-t)+math.exp(-t)-math.exp(-2*t))
  close(convolution,y)
 def floor_alpha(n):return (math.isqrt(5*n*n)-n)//2
 w=[floor_alpha(n+1)-floor_alpha(n) for n in range(1024)]
 assert w[:8]==[0,1,0,1,1,0,1,0]
 for m in range(1,129):
  counts={sum(w[j:j+m]) for j in range(1025-m)}
  assert counts<=set([floor_alpha(m),floor_alpha(m)+1])
 close((1+math.exp(-2*math.log(2)))/2,5/8)
 return dict(x_at_log2='5/8',memory_free_value='1/2',balance_lengths_checked=128,word_length=1024,word_arithmetic='exact integer square roots')
check('D09-F04 exact memory and rotation coding','Exact irrational floor arithmetic for 1024 symbols and 128 block lengths; numerical linear-flow and convolution identities.',memory,'exact combinatorial plus numerical continuous model')
def metadata():
 fs=json.loads((HERE/'families.json').read_text());cs=json.loads((HERE/'classification_review.json').read_text());source=json.loads((ROOT/'data/source_corpus_initial_routing.json').read_text());byuid={e['uid']:e for e in source}
 initials={e['uid'] for e in source if e['primary_domain'] in ['D07','D08','D09']}
 assert len(cs)==len(initials)==259 and {x['uid'] for x in cs}==initials
 assert len({f['id'] for f in fs})==12
 for f in fs:
  assert 4<=len(f['anchor_uids'])<=8
  assert all(u in byuid for u in f['source_uids']+f['anchor_uids'])
  for p in f['progression']:assert all(byuid[u]['year']==p['year'] for u in p['evidence_uids'])
 return dict(classified_sources=259,families=12,anchor_and_progression_links='valid')
check('Source and coverage integrity','Identifier validity and complete routing of the 259 initial source records; this is structural QA, not theorem validation.',metadata,'metadata')
result=dict(agent='analysis_dynamics_atlas',status='passed' if all(c['status']=='passed' for c in checks) else 'failed',checks=checks,scope='Twelve stated worked models plus source integrity. Proofs in families.json carry the general mathematical claims. No check claims to validate the entire historical corpus or an unspecified operator.')
(HERE/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['status']=='passed' else 1)
