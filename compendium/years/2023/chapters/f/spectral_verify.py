#!/usr/bin/env python3
"""Exact exceptional-point identities and illustrative continuation for S013."""
from fractions import Fraction as F
from pathlib import Path
import json,cmath,math
P=Path(__file__).resolve().parent
checks=[]
def check(name,detail):checks.append(dict(id='S013',name=name,status='passed',detail=detail))
class K:
 def __init__(self,a=0,b=0):
  if isinstance(a,K):self.a,self.b=a.a,a.b
  else:self.a,self.b=F(a),F(b)
 def __add__(self,o):o=K(o);return K(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return K(-self.a,-self.b)
 def __sub__(self,o):return self+-K(o)
 def __rsub__(self,o):return K(o)+-self
 def __mul__(self,o):
  o=K(o);return K(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a+self.b*o.b)
 __rmul__=__mul__
 def inv(self):
  d=self.a*self.a+self.a*self.b+self.b*self.b
  if not d:raise ZeroDivisionError
  return K((self.a+self.b)/d,-self.b/d)
 def __truediv__(self,o):return self*K(o).inv()
 def __rtruediv__(self,o):return K(o)*self.inv()
 def __eq__(self,o):o=K(o);return self.a==o.a and self.b==o.b
 def __ne__(self,o):return not self==o
 def __str__(self):return str(self.a)+' + ('+str(self.b)+')tau'
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def ma(a,b):return [[x+y for x,y in zip(row,col)] for row,col in zip(a,b)]
def ms(a,k):return [[x*k for x in row] for row in a]
def minus(a,b):return ma(a,ms(b,-1))
def outer(a,b):return [[x*y for y in b] for x in a]
def zero(n):return [[K(0) for _ in range(n)] for _ in range(n)]
def eye(n):return [[K(i==j) for j in range(n)] for i in range(n)]
def norm(a):return math.sqrt(sum(abs(x)**2 for row in a for x in row))
tau=K(0,1);sites=[K(0),K(1),tau];w=(1+tau)/3
assert tau*tau-tau+1==0
a=[1/(w-z) for z in sites];vp=[-x*x for x in a];u=[K(1)]*3
p0=K(1)
for z in sites:p0*=w-z
assert p0!=0 and sum(a)==0 and sum(x*x for x in a)==0
assert sum(a[i]*vp[i] for i in range(3))==-3/p0
assert sum(x*x for x in vp)==0
Q=minus(eye(3),ms(outer(u,u),F(1,3)))
Qformula=ms(ma(outer(vp,a),outer(a,vp)),-p0/3)
assert Q==Qformula and mm(Q,Q)==Q
C=ms(outer(a,a),-p0/2)
assert C!=zero(3) and mm(C,C)==zero(3)
assert mv(C,u)==[K(0)]*3 and mv(C,a)==[K(0)]*3
assert mv(C,vp)==[F(3,2)*x for x in a]
check('Exceptional Gram and constant-projector identities','In Q(tau), both v and v′ are bilinearly isotropic, vᵀv′=−3/p0, and Q=−p0(v′vᵀ+vv′ᵀ)/3 exactly. Q²=Q; the nonzero leading divergence coefficient C=−p0vvᵀ/2 satisfies C²=0.')

Hs=[];E=[];nilpotents=[]
for i in range(3):
 H=zero(3)
 for j in range(3):
  if j==i:continue
  O=ms(eye(3),F(1,2));O[i][i]=O[j][j]=K(F(-1,2));O[i][j]=O[j][i]=K(1)
  H=ma(H,ms(O,1/(sites[i]-sites[j])))
 E0=sum(F(1,2)/(sites[i]-sites[j]) for j in range(3) if j!=i)
 Ei=E0+a[i]
 assert mv(H,a)==[Ei*x for x in a]
 assert mv(H,vp)==[Ei*vp[j]-a[i]*a[i]*a[j] for j in range(3)]
 N=mm(minus(H,ms(eye(3),Ei)),Q)
 assert N==ms(outer(a,a),p0*a[i]*a[i]/3)
 assert N!=zero(3) and mm(N,N)==zero(3)
 assert mm(N,Q)==N and mm(Q,N)==N
 Hs.append(H);E.append(Ei);nilpotents.append(N)
for H in Hs:
 for J in Hs:assert mm(H,J)==mm(J,H)
check('All three exact nonzero square-zero Jordan parts','Each N_i=(H_i−E_i)Q equals (p0 a_i²/3)vvᵀ, is nonzero, has square zero and is supported on Q. The differentiated generalized-eigenvector identities hold, proving a size-two block for every H_i on the highest-weight plane.')

# Projector asymptotics: finite complex evaluations illustrate the exact derivation.
t0=(1+1j*math.sqrt(3))/2
ascomplex=lambda x:float(x.a)+float(x.b)*t0
Cnum=[[ascomplex(x) for x in row] for row in C]
Qnum=[[ascomplex(x) for x in row] for row in Q]
approaches=[]
for eps in [.1,.03,.01,.003,.001]:
 t=(1+1j*math.sqrt(3-4*eps*eps))/2
 zs=[0,1,t];wp=(1+t+eps)/3;wm=(1+t-eps)/3
 ap=[1/(wp-z) for z in zs];am=[1/(wm-z) for z in zs]
 pp=wp*(wp-1)*(wp-t)
 pm=wm*(wm-1)*(wm-t)
 Pp=ms(outer(ap,ap),-pp/(2*eps));Pm=ms(outer(am,am),pm/(2*eps))
 cancellation=norm(minus(ma(Pp,Pm),Qnum))
 leading_error=norm(minus(ms(Pp,eps),Cnum))
 assert cancellation<1e-8 and leading_error<10*eps
 approaches.append({'epsilon':eps,'projector_norm':norm(Pp),'scaled_norm':eps*norm(Pp),'leading_coefficient_error':leading_error,'sum_projector_error':cancellation})
assert approaches[-1]['leading_coefficient_error']<approaches[0]['leading_coefficient_error']
check('Projector blowup with bounded sum','Complex sample approaches satisfy the exact projector formula, show ε||P+|| tending to a nonzero coefficient and cancellation P++P−=Q to roundoff. This numerical illustration accompanies the analytic |D|^(−1/2) proof.')

# Continue sqrt(D) by choosing at each fine step the root closest to its predecessor.
radius=.01;steps=256
D=lambda t:t*t-t+1
start_t=t0+radius;start_root=cmath.sqrt(D(start_t));root=start_root
for step in range(1,steps+1):
 t=t0+radius*cmath.exp(1j*2*math.pi*step/steps)
 candidate=cmath.sqrt(D(t))
 root=min([candidate,-candidate],key=lambda z:abs(z-root))
assert abs(root+start_root)<1e-12 and abs(root-start_root)>1e-3
start_wp=(1+start_t+start_root)/3;start_wm=(1+start_t-start_root)/3
end_wp=(1+start_t+root)/3
assert abs(end_wp-start_wm)<1e-12
check('Tracked spectral-cover label exchange','A small loop around one discriminant root flips the continued square root and exchanges w+ with w−. This is a label-continuation calculation, not KZ parallel transport; the proof uses the winding of D.')

encode_matrix=lambda A:[[str(x) for x in row] for row in A]
out={'checks':checks,'exact_field':'Q(tau), tau²−tau+1=0','exceptional_root':str(w),'p0':str(p0),'v':[str(x) for x in a],'vprime':[str(x) for x in vp],'Q':encode_matrix(Q),'leading_projector_coefficient_C':encode_matrix(C),'nilpotents':[encode_matrix(N) for N in nilpotents],'approaches':approaches,'continuation':{'radius':radius,'steps':steps,'root_flip_error':abs(root+start_root),'eigenroot_exchange_error':abs(end_wp-start_wm)},'scope':'Algebraic Jordan and projector identities use exact quadratic-field arithmetic. Limit samples and the continuation path use ordinary floating-point complex numbers and accompany written analytic arguments.'}
P.joinpath('spectral_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'id':'S013','checks':len(checks),'exact_Jordan_identities':'passed','projector_limit_and_cover_examples':'passed'}))
