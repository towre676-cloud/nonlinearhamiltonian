"""Independent exact Bareiss/cofactor and decoder-interval peer checks.

Finite replay checks corroborate implementation; the separately reviewed
lattice proof is the universal all-state certificate. Standard library only.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import json,random,importlib.util
H=Path(__file__).resolve().parent
def determinant(A):
    A=[r[:] for r in A];n=len(A);sign=1;previous=1
    for k in range(n-1):
        if A[k][k]==0:
            j=next(j for j in range(k+1,n) if A[j][k]);A[k],A[j]=A[j],A[k];sign=-sign
        pivot=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=A[i][j]*pivot-A[i][k]*A[k][j]
                assert v%previous==0;A[i][j]=v//previous
            A[i][k]=0
        previous=pivot
    return sign*A[-1][-1]
def cofactor(A,i,j):return (-1)**(i+j)*determinant([[x for jj,x in enumerate(r) if jj!=j] for ii,r in enumerate(A) if ii!=i])
data=json.loads((H/'freelip_certificate.json').read_text());M,A,B,D=(data[k] for k in ('M','A','output_modulus','difference_bound'))
assert D==2**81-1
allmax=Q(0);bases={}
for row in data['records']:
    basis=row['basis'];det=determinant(basis);assert abs(det)==M**4
    inverse=[[Q(cofactor(basis,j,i),det) for j in range(5)]for i in range(5)]
    bounds=[D*sum(abs(inverse[i][j])for i in range(5))for j in range(5)]
    assert [str(b)for b in bounds]==row['dual_box_bounds'];assert max(bounds)<Q(3,8)
    allmax=max(allmax,*bounds);bases[tuple(row['positions'])]=(basis,inverse)
assert set(bases)==set(combinations(range(9),5))
spec=importlib.util.spec_from_file_location('vf',H/'verify_freelip.py');vf=importlib.util.module_from_spec(spec);spec.loader.exec_module(vf)
_,cache,_=vf.prepare();rng=random.Random(72859)
states=[0,1,B-1,B,B+1,M-B-1,M-B,M-2,M-1]+[rng.randrange(M)for _ in range(41)]
fixtures=0
for state in states:
    values=[(pow(A,p,M)*state%M)%B for p in range(9)]
    for positions,(basis,I)in bases.items():
        y=[values[p]for p in positions]
        v=[0]+[(pow(B,-1,M)*(pow(A,positions[j]-positions[0],M)*y[0]-y[j]))%M for j in range(1,5)]
        q=[]
        for j in range(5):
            vals=[I[i][j]for i in range(5)];a=-sum(v[i]*vals[i]for i in range(5))
            lo=a+D*sum(x for x in vals if x<0);hi=a+D*sum(x for x in vals if x>0)
            # Independent endpoint enumeration uses math.floor/ceil on exact Fractions.
            import math
            assert math.ceil(lo)==math.floor(hi)
            q.append(math.ceil(lo))
        z=[v[j]+sum(q[i]*basis[i][j]for i in range(5))for j in range(5)]
        assert all(0<=x<=D for x in z)
        original=pow(pow(A,positions[0],M),-1,M)*(y[0]+B*z[0])%M
        assert original==state==vf.decode(y,positions,data,cache);fixtures+=1
# Endpoint formulas include negative rationals and exact integers.
for numerator in range(-50,51):
 for denominator in range(1,20):
  x=Q(numerator,denominator)
  assert -((-x.numerator)//x.denominator)==math.ceil(x)
report={
 'status':'approved','reviewer':'representations_and_dynamics',
 'reviewed_files':['year_2026/build_freelip_certificate.py','year_2026/verify_freelip.py','year_2026/freelip_certificate.json','year_2026/months/10/catalog_entries.json'],
 'scope':['Read and independently checked all-state lattice proof, cardinality obstruction, exact affine decoder, Singleton distance equality and length-optimal error correction.','Inspected the complete generator/checker code and both catalog entries901/902. Independently replayed supplied verifier.','Recomputed all126 determinant and all630 inverse-column bounds using fraction-free Bareiss determinants and cofactor adjugates, independent of the supplied Gauss-Jordan inverse.','Additional50 states times126 patterns=6300 exact round/reconstruct fixtures, including state/alphabet boundaries and deterministically sampled states; these corroborate code but are not the all-state proof.','Checked1919 positive/negative/integer rational ceil endpoint cases against Python exact Fraction ceil.'],
 'all_state_reasoning':{'lattice':'Congruence kernel has indexM^4 by an onto map to(Z/MZ)^4; checked row membership plus exact determinant proves full row lattice.','collision':'Same raw symbols imply differences b*d with |d_i|<=D, invertibility of b puts d in the lattice, and c=d*inverse_basis is an integer vector with each |c_j|<3/8<1. Therefore c=d=0; invertible A reverses the first selected time.','decoder':'y+b*z congruences give z in v+Lambda with the sign used in code. Multiplying z-v by the inverse basis gives exact coefficient intervals of width<3/8<1. A valid trajectory therefore produces exactly one integer in each interval; bound/congruence replay rejects invalid reconstructed candidates.','coding':'Any5 selected symbols identify state, so d_min>=n-4. Puncturing bound M<=b^(n-d+1), together with M>b^4, gives reverse inequality for5<=n<=9. The same argument yields n>=5+2t for arbitrary-word correction.'},
 'checks':{'supplied_verifier':'passed:126 all-state certificates,630 fixtures,2 error correction fixtures','independent_bareiss_patterns':126,'independent_dual_columns':630,'additional_decoder_fixtures':fixtures,'maximum_dual_bound_exact':str(allmax),'maximum_dual_bound_approx':float(allmax),'interval_endpoint_cases':101*19},
 'findings':[],
 'approved_scope':'Universal theorem for exact known raw-step positions0..8, every state0<=x<M, specified recurrence/output alphabet; accepted outputs with hidden rejected steps, cryptographic quality and empirical historical repository validation remain outside the proof.',
 'comments':['No primality assumption for M is needed: the index proof uses a finite abelian quotient, while invertibility of A and b follows from gcd(3,M)=1 and M odd.','The builder LLL has no trusted role; basis membership, determinant, rational inverse and dual bounds suffice independently.','The small fixture set in the supplied verifier is correctly distinguished from the all-state certificate in the catalog.','No blocking mathematical or implementation issue found within the declared raw-output scope.']}
(H/'independent_freelip_review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['checks']))
