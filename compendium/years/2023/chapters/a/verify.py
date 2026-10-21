"""Independent stdlib calculations for entries M001--M018.

Finite checks illustrate stated proofs; the entries say which general claims
are proved analytically and which identities are checked by all coefficients.
"""
from fractions import Fraction as F
import json, math
from pathlib import Path

checks=[]
def check(ids,name,ok,detail):
    assert ok,name
    checks.append({'id':ids[0],'ids':ids,'name':name,'status':'passed','passed':True,'detail':detail})

def vp(n,p):
    if n==0:return math.inf
    n=abs(n);v=0
    while n%p==0:n//=p;v+=1
    return v

# Simple-root Hensel lift, independently choosing the unique next digit.
x=3;digits=[];roots=[3]
for n in range(1,6):
    candidates=[x+t*7**n for t in range(7) if ((x+t*7**n)**2-2)%7**(n+1)==0]
    assert len(candidates)==1
    digits.append((candidates[0]-x)//7**n);x=candidates[0];roots.append(x)
check(['M002'],'Hensel simple-root lift',roots[:3]==[3,10,108] and all((r*r-2)%7**(i+1)==0 for i,r in enumerate(roots)),{'prime':7,'roots_mod_successive_powers':roots,'new_digits':digits})

# All affine maps modulo small prime powers: test fixed-point divisibility criterion.
for p in [2,3,5]:
    for n in [1,2,3]:
        mod=p**n
        for a in range(mod):
            for b in range(mod):
                roots_mod=[x for x in range(mod) if ((1-a)*x-b)%mod==0]
                d=math.gcd(1-a,mod)
                assert bool(roots_mod)==(b%d==0)
                if roots_mod:assert len(roots_mod)==d
check(['M003'],'Finite affine fixed-point classification',True,'Exhaustive modulo p^n for p=2,3,5 and n=1,2,3 agrees with gcd divisibility and the predicted count of fixed residues.')
check(['M004'],'Probability range counterexample',(1+1)*(1-0)==2,'P(1,0)=2, so the toy formula is not a probability throughout the unit square.')
logits=[0,math.log(3),-math.log(3)]
ps=[1/(1+math.exp(-z)) for z in logits]
check(['M004'],'Logistic three-design example',max(abs(a-b) for a,b in zip(ps,[.5,.75,.25]))<1e-15,{'probabilities':ps,'design_rows':[[1,0,0],[1,1,0],[1,0,1]],'design_determinant':1})
check(['M005'],'Toy linear inversion attack',pow(7,-1,101)*35%101==5,{'public_modulus':101,'public_multiplier':7,'ciphertext':35,'recovered_x':pow(7,-1,101)*35%101})
for n in range(1,30):assert sum(F(1,2**k) for k in range(1,n+1))==1-F(1,2**n)
check(['M006'],'Exact geometric partial sums',True,'For N=1,...,29 exact rational sums equal 1−2^(-N); the general identity follows by multiplying the finite sum by two.')

def qconj(a):return (a[0],-a[1],-a[2],-a[3])
def qmul(a,b):
    w,x,y,z=a;v,r,s,t=b
    return (w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,w*s-x*t+y*v+z*r,w*t+x*s-y*r+z*v)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def octmul(a,b):
    x,y=a[:4],a[4:];u,v=b[:4],b[4:]
    return sub(qmul(x,u),qmul(qconj(v),y))+add(qmul(v,x),qmul(y,qconj(u)))
def assoc(a,b,c):return sub(octmul(octmul(a,b),c),octmul(a,octmul(b,c)))
def norm2(a):return sum(x*x for x in a)
E=[tuple(int(i==j) for i in range(8)) for j in range(8)]
zero=(0,)*8
assert assoc(E[1],E[2],E[4])==(0,0,0,0,0,0,0,2)
# Since the associator is trilinear, these coefficient identities prove alternation over R.
for a in E:
 for b in E:
  for c in E:
   assert add(assoc(a,b,c),assoc(b,a,c))==zero
   assert add(assoc(a,b,c),assoc(a,c,b))==zero
check(['M007','M008'],'Octonion associator and all alternation coefficients',True,{'convention':'(a,b)(c,d)=(ac−conj(d)b, da+b conj(c)) on quaternion pairs','associator_e1_e2_e4':list(assoc(E[1],E[2],E[4])),'basis_triples_checked':512})
# A is quadratic, b,c linear in this Moufang expression. Basis and pair sums
# determine every a_i^2 and a_i*a_j coefficient, hence the full polynomial identity.
As=E+[add(E[i],E[j]) for i in range(8) for j in range(i)]
for a in As:
 for b in E:
  for c in E:
   assert octmul(octmul(a,b),octmul(c,a))==octmul(a,octmul(octmul(b,c),a))
check(['M007'],'Moufang identity checked by complete coefficient polarization',True,{'evaluations':len(As)*64,'identity':'(ab)(ca)=a((bc)a)','scope':'All real octonions, because the tested homogeneous polynomial is quadratic in a and linear in b,c.'})
check(['M008'],'Sharp unit associator bound attained',norm2(assoc(E[1],E[2],E[4]))==4 and all(norm2(E[j])==1 for j in [1,2,4]),'The normalized triple (e1,e2,e4) has defect 2; therefore the proved upper bound 2 is sharp.')

def pa(a,b):
 c=a.copy()
 for i,v in b.items():c[i]=c.get(i,0)+v
 return {i:v for i,v in c.items() if v}
def pm(a,b):
 c={}
 for i,v in a.items():
  for j,w in b.items():c[i+j]=c.get(i+j,0)+v*w
 return {i:v for i,v in c.items() if v}
def ps(a,s):return {i:v*s for i,v in a.items() if v*s}
def dz(a):return pm({i-1:i*v for i,v in a.items() if i},{0:1,2:-1})
u={0:2,2:-2};uz=dz(u);uzzz=dz(dz(uz))
res=pa(pa(ps(uz,-4),ps(pm(u,uz),6)),uzzz)
check(['M009','M011'],'KdV residual polynomial identity',res=={},'For u=2(1−T²), d/dz=(1−T²)d/dT, −4u_z+6u*u_z+u_zzz is the zero polynomial. Scaling proves the stated κ-family.')
for x in [-8,-2,-.3,0,.3,2,8]:
 theta=math.atan(math.sinh(x))
 assert abs(math.sin(theta)-math.tanh(x))<1e-14
 assert abs(math.cos(theta)-1/math.cosh(x))<1e-14
 assert abs(math.asinh(math.tan(theta))-x)<1e-11
check(['M010'],'Gudermannian identities and inverse',True,'Seven sample points verify circular/hyperbolic identities and inverse; the entry derives them for all real x.')

for k1,k2 in [(F(1),F(2)),(F(2),F(3)),(F(1),F(4))]:
 a=((k1-k2)/(k1+k2))**2
 terms=[((0,0),F(1)),((1,0),F(1)),((0,1),F(1)),((1,1),a)]
 coefficients={}
 for (i,j),c in terms:
  for (l,m),d in terms:
   dx=(i-l)*k1+(j-m)*k2
   dt=-(i-l)*k1**3-(j-m)*k2**3
   key=(i+l,j+m)
   coefficients[key]=coefficients.get(key,0)+c*d*(dx*dt+dx**4)
 assert all(v==0 for v in coefficients.values())
k1,k2=F(1),F(2);a=F(1,9)
tau=3+a;tx=k1+k2+a*(k1+k2);txx=k1*k1+k2*k2+a*(k1+k2)**2
u0=2*(tau*txx-tx*tx)/(tau*tau)
check(['M012'],'Two-soliton Hirota identity',True,{'exact_parameter_pairs':[[1,2],[2,3],[1,4]],'u_at_zero_for_k_1_2_delta_0':str(u0),'linear_superposition_at_zero':str((k1*k1+k2*k2)/2),'bilinear_form':'(D_x D_t+D_x^4)tau·tau=0'})

def gd(x):return math.atan(math.sinh(x))
qgd=[]
for q,x in [(.5,2),(2,2),(.5,-2),(1.001,.3)]:
 val=(gd(q*x)-gd(x))/((q-1)*x)
 low=1/math.cosh(max(1,q)*abs(x));high=1/math.cosh(min(1,q)*abs(x))
 assert low-1e-14<=val<=high+1e-14
 qgd.append({'q':q,'x':x,'difference_quotient':val,'bounds':[low,high]})
check(['M014'],'q-Gudermannian secant bounds',True,qgd)
h=0.;logderivative=0.
for n in range(20):
 z=h+2;logderivative-=math.log(math.cosh(z));h=gd(z)
gradient=math.exp(logderivative);bound=(1/math.cosh(2))**20
check(['M015'],'Twenty saturated scalar layers',0<gradient<=bound,{'architecture':'h_(l+1)=gd(h_l+2), h_0=0','depth':20,'actual_input_derivative':gradient,'proved_upper_bound':bound})

def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def rank(m):
 a=[[F(v) for v in row] for row in m];i=0
 for j in range(len(a[0])):
  pivot=next((k for k in range(i,len(a)) if a[k][j]),None)
  if pivot is None:continue
  a[i],a[pivot]=a[pivot],a[i];d=a[i][j];a[i]=[x/d for x in a[i]]
  for k in range(len(a)):
   if k!=i:
    d=a[k][j];a[k]=[x-d*y for x,y in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i
A=[[1,0,0],[0,2,0],[0,0,3]];C=[[1,1,0]];obs=[];power=[[1,0,0],[0,1,0],[0,0,1]]
for _ in range(3):obs+=mm(C,power);power=mm(power,A)
assert rank(obs)==2
for x in [[1,0,0],[0,1,0],[0,0,1],[2,3,5]]:
 seq=[x[0]*1**n+x[1]*2**n for n in range(15)]
 assert all(seq[n+2]-3*seq[n+1]+2*seq[n]==0 for n in range(13))
check(['M016'],'Observable universal recurrence',True,{'A':'diag(1,2,3)','C':[1,1,0],'observable_rank':2,'universal_polynomial':'z²−3z+2','full_characteristic_polynomial':'(z−1)(z−2)(z−3)'})
A=[[-1,0,0],[0,-2,0],[0,0,3]];B=[[1],[0],[1]];C=[[1,1,0]]
AB=mm(A,B);AAB=mm(A,AB);reach=[list(z) for z in zip(*(B[i]+AB[i]+AAB[i] for i in range(3)))]
# Columns are B, AB, A²B; the transpose above does not affect rank.
obs=C+mm(C,A)+mm(mm(C,A),A)
assert rank(reach)==2 and rank(obs)==2
check(['M017'],'Reachable-visible quotient example',True,{'A':'diag(−1,−2,3)','B':[1,0,1],'C':[1,1,0],'reachable_rank':2,'observable_rank':2,'zero_initial_minimal_dimension':1,'transfer_function':'1/(s+1)','hidden_unstable_mode':3})

def compose(p,f):
 out={};power={0:1}
 for k in range(max(p,default=0)+1):
  if k in p:out=pa(out,ps(power,p[k]))
  power=pm(power,f)
 return out
f={1:2,2:-2};iterate={1:1};degrees=[]
for n in range(7):
 degrees.append(max(iterate));iterate=compose(iterate,f)
check(['M018'],'Polynomial Koopman degree-growth obstruction',degrees==[1,2,4,8,16,32,64],{'map':'2x(1−x)','iterated_degrees':degrees,'scope':'These exact calculations illustrate the analytic degree argument, which proves impossibility of every finite polynomial invariant space containing x on an interval.'})

output={'chapter':'a','entries':[f'M{i:03d}' for i in range(1,19)],'checks':checks,'passed':all(x['passed'] for x in checks)}
Path(__file__).resolve().with_name('checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2))
print(json.dumps({'checks':len(checks),'passed':output['passed'],'gradient':gradient,'gradient_bound':bound}))
