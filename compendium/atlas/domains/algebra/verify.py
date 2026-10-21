#!/usr/bin/env python3
"""Exact finite worked-model checks for the algebra/quantum atlas (stdlib only).
These checks certify their stated finite models; they do not replay missing historical matrices.
"""
import itertools as it
import json, math
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent
checks=[]
def report(family,name,details):checks.append({'family_id':family,'name':name,'status':'pass','method':'exact finite arithmetic','details':details})
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(k,a):return [[k*x for x in row] for row in a]
def transpose(a):return list(map(list,zip(*a)))
def mv(a,v):return [sum(x*y for x,y in zip(r,v)) for r in a]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def rank(a,p=None):
 a=[[x%p if p else Q(x) for x in r] for r in a];r=0
 for c in range(len(a[0])):
  q=next((j for j in range(r,len(a)) if a[j][c]),None)
  if q is None:continue
  a[r],a[q]=a[q],a[r];z=pow(a[r][c],-1,p) if p else 1/a[r][c];a[r]=[(x*z)%p if p else x*z for x in a[r]]
  for j in range(len(a)):
   if j!=r:
    z=a[j][c];a[j]=[(x-z*y)%p if p else x-z*y for x,y in zip(a[j],a[r])]
  r+=1
  if r==len(a):break
 return r
# D03-F01: exhaustive monoid identities and ideal lattice.
E=list(it.product(range(2),range(3)))
def mul(x,y):return ((x[0]+y[0])%2,min(x[1]+y[1],2))
assert all(mul(mul(a,b),c)==mul(a,mul(b,c)) for a,b,c in it.product(E,repeat=3))
ideals=[]
for mask in range(1,1<<len(E)):
 J={E[i] for i in range(len(E)) if mask>>i&1}
 if all(mul(x,y) in J and mul(y,x) in J for x in E for y in J):ideals.append(J)
K=set.intersection(*ideals);assert K=={(0,2),(1,2)}
assert [x for x in E if mul(x,x)==x]==[(0,0),(0,2)]
report('D03-F01','C₂ × capped counter: complete multiplication and ideal check',{'elements':6,'associative_triples':216,'nonempty_two_sided_ideals':len(ideals),'minimal_ideal':sorted(K)})
# D03-F02: Boolean projector identities plus rank factorization/lower witness.
PP=[[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]];QQ=[[1,0,0,0],[0,0,0,0],[0,0,1,0],[0,0,0,0]];I=eye(4)
blocks=[mm(PP if a else add(I,scale(-1,PP)),QQ if b else add(I,scale(-1,QQ))) for a,b in it.product(range(2),repeat=2)]
assert sum(tr(e) for e in blocks)==4
assert all(mm(e,e)==e for e in blocks)
assert all(mm(e,f)==[[0]*4 for _ in range(4)] for i,e in enumerate(blocks) for j,f in enumerate(blocks) if i!=j)
T=add(scale(2,PP),scale(-1,QQ));poly=I
for lam in [0,1,2,-1]:poly=mm(poly,add(T,scale(-lam,I)))
assert poly==[[0]*4 for _ in range(4)]
A=[[1,2,3],[2,4,6],[0,1,1]];U=[[1,2],[2,4],[0,1]];V=[[1,0,1],[0,1,1]]
assert mm(U,V)==A and rank(A)==2 and rank(A,7)==2
report('D03-F02','Boolean decomposition, supported spectrum and independent rank bounds',{'blocks':4,'supported_eigenvalues':[-1,0,1,2],'rational_rank':2,'mod_7_rank':2})
# D03-F03: enumerate signed-permutation action, independently compare orbit formula.
vec=list(it.product(range(3),repeat=4));perms=list(it.permutations(range(4)));signs=list(it.product([1,-1],repeat=4))
def orbit(v):return {tuple((s[i]*v[p[i]])%3 for i in range(4)) for p in perms for s in signs}
remaining=set(vec);orbs=[]
while remaining:
 o=orbit(min(remaining));orbs.append(o);remaining-=o
sizes={sum(bool(x) for x in next(iter(o))):len(o) for o in orbs}
assert [sizes[j] for j in range(5)]==[1,8,24,32,16]
assert all(sizes[j]==2**j*math.comb(4,j) for j in range(5))
report('D03-F03','B₄ action on F₃⁴: full orbit reconstruction',{'vectors':81,'group_elements':384,'orbit_sizes_by_weight':[sizes[j] for j in range(5)]})
# D03-F04: exact Cayley-Dickson basis multiplication and E8 roots (doubled integral coordinates).
def qmul(a,b):
 a0,a1,a2,a3=a;b0,b1,b2,b3=b
 return (a0*b0-a1*b1-a2*b2-a3*b3,a0*b1+a1*b0+a2*b3-a3*b2,a0*b2-a1*b3+a2*b0+a3*b1,a0*b3+a1*b2-a2*b1+a3*b0)
def conj(a):return (a[0],-a[1],-a[2],-a[3])
def va(a,b,k=1):return tuple(x+k*y for x,y in zip(a,b))
def omul(x,y):
 a,b=x[:4],x[4:];c,d=y[:4],y[4:]
 return va(qmul(a,c),qmul(conj(d),b),-1)+va(qmul(d,a),qmul(b,conj(c)))
basis=[tuple(int(i==j) for j in range(8)) for i in range(8)]
def assoc(a,b,c):return va(omul(omul(a,b),c),omul(a,omul(b,c)),-1)
assert assoc(basis[1],basis[2],basis[4])==tuple(2*x for x in basis[7])
assert assoc(basis[1],basis[2],basis[3])==(0,)*8
for a,b,c in it.product(basis,repeat=3):
 assert va(assoc(a,b,c),assoc(b,a,c))==(0,)*8
 assert va(assoc(a,b,c),assoc(a,c,b))==(0,)*8
roots=set()
for i,j in it.combinations(range(8),2):
 for s,t in it.product([-2,2],repeat=2):
  v=[0]*8;v[i]=s;v[j]=t;roots.add(tuple(v))
for v in it.product([-1,1],repeat=8):
 if sum(x<0 for x in v)%2==0:roots.add(v)
assert len(roots)==240 and all(sum(x*x for x in v)==8 for v in roots)
# Verify root reflection closure using doubled coordinates: r_v(w)=w-(w.v)/4 v.
for v,w in it.product(roots,repeat=2):
 dot=sum(a*b for a,b in zip(v,w));r=tuple(Q(a)-Q(dot,4)*b for a,b in zip(w,v));assert all(x.denominator==1 for x in r) and tuple(map(int,r)) in roots
report('D03-F04','Octonion convention and E₈ root-system finite certificate',{'basis_associator_triples':512,'roots':240,'reflection_pairs':57600,'squared_length':2,'exceptional_bracket_constructed':False})
# D03-F05: standard monomials, full multiplication, radical and socle; path enumeration.
B=[(0,0),(1,0),(0,1),(0,2)]
def jet(a,b):
 c=(a[0]+b[0],a[1]+b[1]);return c if c in B else None
for a,b,c in it.product(B,repeat=3):
 ab=jet(a,b);bc=jet(b,c);assert (jet(ab,c) if ab is not None else None)==(jet(a,bc) if bc is not None else None)
soc=[b for b in B if all(jet(b,g) is None for g in [(1,0),(0,1)])];assert soc==[(1,0),(0,2)]
arrows={'a':(0,1),'g':(1,1),'b':(1,2),'c':(1,2)};paths=[(i,i,'') for i in range(3)]
for length in range(1,5):
 for w in it.product(arrows,repeat=length):
  if any(arrows[w[i]][1]!=arrows[w[i+1]][0] for i in range(length-1)):continue
  if any(w[i]==w[i+1]=='g' for i in range(length-1)):continue
  paths.append((arrows[w[0]][0],arrows[w[-1]][1],''.join(w)))
assert len(paths)==14 and all(len(w)<=3 for _,_,w in paths)
assert (0,2,'agb') in paths and (0,2,'ab') in paths
for u,v in [(1,0),(1,1),(0,1)]:assert rank([[u,-v]])==1
report('D03-F05','Jet socle and complete pre-relation quiver path count',{'jet_basis':4,'socle_dimension':2,'quiver_paths_before_relation':14,'fibre_dimension_after_nonzero_relation':13})
# D03-F06: KMS identity independently on all matrix units with rational population ratios.
rho=[[Q(3,4),0],[0,Q(1,4)]];D=[[1,0],[0,Q(1,3)]];Di=[[1,0],[0,3]]
units=[]
for i,j in it.product(range(2),repeat=2):
 E=[[0,0],[0,0]];E[i][j]=1;units.append(E)
for A,Bb in it.product(units,repeat=2):
 assert tr(mm(rho,mm(A,mm(mm(D,Bb),Di))))==tr(mm(rho,mm(Bb,A)))
report('D03-F06','Finite Gibbs KMS boundary on a spanning basis',{'matrix_unit_pairs':16,'populations':['3/4','1/4'],'thermal_ratio':'1/3','modular_ratios':['1','3','1/3','1']})
# D16-F01: exact Bell/mixture collision, dephasing positivity, instrument completeness.
bell=[[Q(1,2) if i in [0,3] and j in [0,3] else 0 for j in range(4)] for i in range(4)]
mix=[[Q(1,2) if i==j and i in [0,3] else 0 for j in range(4)] for i in range(4)]
XX=[[int(j==(i^3)) for j in range(4)] for i in range(4)];ZZ=[[((-1)**((i>>1)+(i&1))) if i==j else 0 for j in range(4)] for i in range(4)]
assert [bell[i][i] for i in range(4)]==[mix[i][i] for i in range(4)]
assert tr(mm(bell,XX))==1 and tr(mm(mix,XX))==0 and tr(mm(bell,ZZ))==tr(mm(mix,ZZ))==1
q=Q(1,3);out=[[bell[i][j]*(q if i!=j else 1) for j in range(4)] for i in range(4)]
assert tr(mm(out,XX))==q and (1+q)/2==Q(2,3)
# Two sequential projective instruments: every composed branch included.
K=[[[1,0],[0,0]],[[0,0],[0,1]]];total=[[0,0],[0,0]]
for a,b in it.product(K,repeat=2):
 C=mm(b,a);total=add(total,mm(transpose(C),C))
assert total==eye(2)
# Knill-Laflamme scalar test on repetition basis, error labels are xor flips.
code=[0,7];errors=[0,1,2,4]
for a,b in it.product(errors,repeat=2):
 restricted=[[int((j^a^b)==i) for j in code] for i in code];assert restricted==scale(int(a==b),eye(2))
report('D16-F01','Coherence collision, dephasing and complete branch probabilities',{'dephasing_q':'1/3','XX_Bell':1,'XX_mixture':0,'KL_error_pairs':16,'quantum_distance':1})
# D16-F02: Pauli centralizer and exact q=i clock/shift relation using Gaussian integers.
U=[[1,0,0,0],[0,1j,0,0],[0,0,-1,0],[0,0,0,-1j]];V=[[int(i==(j+1)%4) for j in range(4)] for i in range(4)]
assert mm(U,V)==scale(1j,mm(V,U))
paulis=list(it.product(range(2),repeat=4))
def omega(a,b):return sum(a[i]*b[i+2]+a[i+2]*b[i] for i in range(2))%2
support=[(0,0,1,0),(0,0,0,1)];central=[v for v in paulis if all(omega(v,s)==0 for s in support)]
assert len(central)==4 and all(v[:2]==(0,0) for v in central)
report('D16-F02','Exact root-of-unity pair and symplectic support kernel',{'conductor':4,'Weyl_relation':'UV=iVU','Pauli_centralizer_labels':4,'binary_dimension':2,'full_operator_commutant_claimed':False})
# D16-F03: independent coefficient and direct-star algorithms on the complete sextic universe.
def falling(a,k):return math.factorial(a)//math.factorial(a-k) if 0<=k<=a else 0
def S(a,b,c,d,k):return sum((-1)**r*math.comb(k,r)*falling(a,k-r)*falling(b,r)*falling(c,r)*falling(d,k-r) for r in range(k+1))
def direct_star(a,b,c,d):
 # dictionary (i-exponent mod4, hbar-power, q-degree,p-degree)->real rational coefficient
 out={}
 for x in range(min(a,d)+1):
  for y in range(min(b,c)+1):
   k=x+y;key=(k%4,k,a+c-k,b+d-k)
   val=Q((-1)**y*falling(a,x)*falling(b,y)*falling(c,y)*falling(d,x),2**k*math.factorial(x)*math.factorial(y))
   out[key]=out.get(key,Q(0))+val
 return {k:v for k,v in out.items() if v}
mons=[(a,b) for a in range(7) for b in range(7-a)];exact=defect=cubicblind=0;sixexact=0
for a,b in mons:
 for c,d in mons:
  star=direct_star(a,b,c,d);rev=direct_star(c,d,a,b)
  # odd-order commutator divided by i hbar; exact signs use i^(k-1).
  terms={}
  for key in set(star)|set(rev):
   ip,k,qdeg,pdeg=key;coeff=star.get(key,0)-rev.get(key,0)
   if coeff:
    assert k%2==1;terms[k]=((-1)**((k-1)//2))*coeff
  for k in [1,3,5]:
   expect=Q((-1)**((k-1)//2)*S(a,b,c,d,k),2**(k-1)*math.factorial(k));assert terms.get(k,0)==expect
  e=S(a,b,c,d,3)==S(a,b,c,d,5)==0
  exact+=e;defect+=not e;cubicblind+=S(a,b,c,d,3)==0 and S(a,b,c,d,5)!=0
  if a+b==c+d==6:sixexact+=e
assert (exact,defect,cubicblind,sixexact)==(504,280,4,15)
assert S(1,5,4,2,3)==0 and S(1,5,4,2,5)==28800
assert S(1,5,5,3,3)==0 and S(1,5,5,3,5)==201600
for r in range(1,41):
 assert all(S(1,3,3*r+2,r,k)==0 for k in range(3,2*r+6,2))
report('D16-F03','Complete bounded sextic monomial atlas with independent star replay',{'monomials':28,'ordered_pairs':784,'exact':exact,'defect':defect,'cubic_blind_defects':cubicblind,'homogeneous_sextic_exact':sixexact,'uniform_family_samples':40,'sample_checks_not_uniform_proof':True})
# D16-F04: all finite coherence and Verlinde equations; exact Hecke and braid at q=1/2.
G=list(it.product(range(2),repeat=2));plus=lambda a,b:tuple(x^y for x,y in zip(a,b));R=lambda a,b:(-1)**(a[0]*b[1]);BB=lambda a,b:R(a,b)*R(b,a)
for a,b,c in it.product(G,repeat=3):
 assert R(a,plus(b,c))==R(a,b)*R(a,c) and R(plus(a,b),c)==R(a,c)*R(b,c)
 assert sum(Q(BB(a,x)*BB(b,x)*BB(c,x),4) for x in G)==int(c==plus(a,b))
SS=[[Q(BB(a,b),2) for b in G] for a in G];assert mm(SS,SS)==eye(4)
q=Q(1,2);RR=[[q,0,0,0],[0,0,1,0],[0,1,q-1/q,0],[0,0,0,q]]
assert mm(add(RR,scale(-q,eye(4))),add(RR,scale(1/q,eye(4))))==[[0]*4 for _ in range(4)]
def kron(a,b):return [[x*y for x in rowa for y in rowb] for rowa in a for rowb in b]
R12=kron(RR,eye(2));R23=kron(eye(2),RR);assert mm(mm(R12,R23),R12)==mm(mm(R23,R12),R23)
report('D16-F04','Finite pointed coherence, exact Verlinde and rational braid matrices',{'hexagon_triples':64,'Verlinde_triples':64,'pointed_rank':4,'Hecke_q':'1/2','braid_matrix_dimension':8,'unitarity_claimed':False})
# D16-F05: four independent eigenvectors and every KdV exponential coefficient.
H=[[2 if i==j else -1 if (i-j)%4 in [1,3] else 0 for j in range(4)] for i in range(4)]
vecs=[([1,1,1,1],0),([1,0,-1,0],2),([0,1,0,-1],2),([1,-1,1,-1],4)]
assert all(mv(H,v)==[e*x for x in v] for v,e in vecs) and rank([v for v,e in vecs])==4
for k1,k2 in [(Q(2),Q(1)),(Q(3),Q(1)),(Q(5,2),Q(1,2))]:
 aa=((k1-k2)/(k1+k2))**2;expo={(0,0):1,(1,0):1,(0,1):1,(1,1):aa};res={}
 for a,ca in expo.items():
  for b,cb in expo.items():
   dx=(a[0]-b[0])*k1+(a[1]-b[1])*k2;dt=-(a[0]-b[0])*k1**3-(a[1]-b[1])*k2**3
   key=(a[0]+b[0],a[1]+b[1]);res[key]=res.get(key,0)+ca*cb*(dx*dt+dx**4)
 assert all(v==0 for v in res.values())
report('D16-F05','XXX full one-magnon basis and KdV tau exponential residuals',{'XXX_sector_dimension':4,'energies':[0,2,2,4],'rational_soliton_parameter_pairs':3,'arbitrary_Bethe_completeness_claimed':False})
# D16-F06: exhaustive characteristic-two lift failure, family associativity and first-order cocycle.
def pmul(a,b,p,n):
 c=[0]*n
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<n:c[i+j]=(c[i+j]+x*y)%p
 return c
assert pmul([1,1],[1,1],2,2)==[1,0]
assert all(pmul([1,1,b],[1,1,b],2,3)==[1,0,1] for b in range(2))
# A_t over Q: pairs a+bx, x²=t, tested on basis implies all associativity by trilinearity.
def dual(a,b,t):return (a[0]*b[0]+t*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
for t in [Q(0),Q(1),Q(-2)]:
 for a,b,c in it.product([(1,0),(0,1)],repeat=3):assert dual(dual(a,b,t),c,t)==dual(a,dual(b,c,t),t)
# Positive cochain maps at special fibre alternate zero and multiplication by 2x.
m2x=[[0,0],[2,0]];assert rank(m2x)==1 and 2-rank(m2x)==1
report('D16-F06','Obstructed character lift and flat dual-number comparison',{'characteristic':2,'second_order_lift_candidates':2,'lifts':0,'flat_basis_rank':2,'positive_HH_dimension_special_fibre':1,'order_12_implies_all_orders':False})
# Metadata integrity is additional to the model checks, never their replacement.
families=json.load(open(P/'families.json'));reviews=json.load(open(P/'classification_review.json'));corpus=json.load(open(P.parents[1]/'data/source_corpus_initial_routing.json'));known={x['uid'] for x in corpus}
assert len(families)==12 and len(reviews)==184
for f in families:
 assert set(f['source_uids'])<=known and set(f['anchor_uids'])<=set(f['source_uids'])
 assert 4<=len(f['anchor_uids'])<=8
assert {x['uid'] for x in reviews}=={x['uid'] for x in corpus if x['primary_domain'] in ['D03','D16']}
result={'status':'pass','verifier':'verify.py','stdlib_only':True,'family_count':12,'reviewed_source_count':184,'checks':checks,'scope':'Finite exact model certificates. Statements proved symbolically in the prose are not inferred solely from tested samples. Missing historical objects are not reconstructed.'}
(P/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','checks':len(checks),'families':len(families),'reviewed_sources':len(reviews)}))
