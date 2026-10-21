"""Exact all-state certificate checker and raw-output decoder.

No LLL routine, floating arithmetic, or external package is trusted here.
The accepted-output/rejection process is outside this certificate.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import json
ROOT=Path(__file__).resolve().parent
def inverse_det(B):
    n=len(B);a=[[Q(v)for v in row]+[Q(i==j)for j in range(n)]for i,row in enumerate(B)];det=Q(1)
    for k in range(n):
        pivot=next(i for i in range(k,n)if a[i][k])
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];det=-det
        v=a[k][k];det*=v;a[k]=[v2/v for v2 in a[k]]
        for i in range(n):
            if i!=k:
                v2=a[i][k];a[i]=[x-v2*y for x,y in zip(a[i],a[k])]
    return[row[n:]for row in a],det
def prepare():
    data=json.loads((ROOT/'freelip_certificate.json').read_text());M=data['M'];A=data['A'];B=data['output_modulus'];D=data['difference_bound']
    assert M==2**107-1 and A==pow(3,121,M) and B==2**26 and D==(M-1)//B
    cache={};maximum=Q(0)
    for row in data['records']:
        positions=row['positions'];gaps=row['gaps'];basis=row['basis']
        assert len(positions)==5 and sorted(set(positions))==positions and positions[0]>=0 and positions[-1]<=8
        assert gaps==[p-positions[0]for p in positions]
        assert len(basis)==5 and all(len(r)==5 and all(type(v)is int for v in r)for r in basis)
        for r in basis:
            assert all((r[j]-pow(A,gaps[j],M)*r[0])%M==0 for j in range(1,5))
        I,det=inverse_det(basis);assert abs(det)==M**4
        for i in range(5):
            for j in range(5):assert sum(Q(basis[i][k])*I[k][j]for k in range(5))==int(i==j)
        bounds=[D*sum(abs(I[i][j])for i in range(5))for j in range(5)]
        assert [str(v)for v in bounds]==row['dual_box_bounds']
        assert all(v<Q(3,8)for v in bounds)
        maximum=max(maximum,*bounds);cache[tuple(positions)]=(basis,I,gaps)
    assert set(cache)==set(combinations(range(9),5))
    return data,cache,maximum
def raw(state,n,A,M,B):
    result=[]
    for _ in range(n):result.append(state%B);state=(A*state)%M
    return result
def decode(values,positions,data,cache):
    M,A,B,D=[data[k]for k in ['M','A','output_modulus','difference_bound']]
    if len(values)!=5 or any(type(y)is not int or not 0<=y<B for y in values):return None
    basis,I,gaps=cache[tuple(positions)]
    binv=pow(B,-1,M)
    v=[0]+[(binv*(pow(A,gaps[j],M)*values[0]-values[j]))%M for j in range(1,5)]
    coefficients=[]
    for j in range(5):
        center=-sum(Q(v[i])*I[i][j]for i in range(5))
        lower=center+D*sum(min(Q(0),I[i][j])for i in range(5))
        upper=center+D*sum(max(Q(0),I[i][j])for i in range(5))
        lo=-((-lower.numerator)//lower.denominator);hi=upper.numerator//upper.denominator
        if lo!=hi:return None
        coefficients.append(lo)
    z=[v[j]+sum(coefficients[i]*basis[i][j]for i in range(5))for j in range(5)]
    if any(not 0<=a<=D for a in z):return None
    states=[values[j]+B*z[j]for j in range(5)]
    if any(not 0<=s<M for s in states):return None
    if any(states[j]!=pow(A,gaps[j],M)*states[0]%M for j in range(5)):return None
    return pow(pow(A,positions[0],M),-1,M)*states[0]%M
def correct(values,t,data,cache):
    answers=set();A,M,B=[data[k]for k in ['A','M','output_modulus']]
    for positions in combinations(range(len(values)),5):
        state=decode([values[p]for p in positions],positions,data,cache)
        if state is not None and sum(a!=b for a,b in zip(raw(state,len(values),A,M,B),values))<=t:answers.add(state)
    return next(iter(answers))if len(answers)==1 else None
def main():
    data,cache,maximum=prepare();A,M,B=[data[k]for k in ['A','M','output_modulus']]
    states=[0,1,1234567890123456789,M//3,M-1]
    for state in states:
        ys=raw(state,9,A,M,B)
        for positions in cache:assert decode([ys[p]for p in positions],positions,data,cache)==state
    state=1234567890123456789;ys=raw(state,9,A,M,B)
    noisy7=ys[:7];noisy7[2]=(noisy7[2]+12345)%B
    noisy9=ys[:];noisy9[1]=(noisy9[1]+54321)%B;noisy9[7]=(noisy9[7]+98765)%B
    assert correct(noisy7,1,data,cache)==state and correct(noisy9,2,data,cache)==state
    assert M>B**4 and M<=B**5
    checks=[dict(id='Y26-10-901',name='All126 exact raw-state lattice certificates',status='passed',scope='All states moduloM, proved by integer-lattice membership, determinant equality and exact dual bounds; no enumeration of2^107states is required.',details={'patterns':126,'maximum_dual_bound_exact':str(maximum),'uniform_strict_bound':'3/8','decoder_fixture_states':states,'decoder_pattern_fixtures':len(states)*126}),dict(id='Y26-10-902',name='Exact raw-output decoder and error correction fixtures',status='passed',scope='The distance and length-optimality statements have a separate all-state proof. These are exact replay examples of the certified decoder; no accepted-output theorem is checked.',details={'state':state,'raw9':ys,'one_error7':noisy7,'two_errors9':noisy9,'decoded':state,'cardinality_inequality':'(2^26)^4 <2^107−1≤(2^26)^5'})]
    (ROOT/'freelip_checks.json').write_text(json.dumps(dict(status='passed',checks=checks),indent=2))
    print(json.dumps(dict(status='passed',all_state_patterns=126,decoder_fixtures=630,error_correction_fixtures=2)))
if __name__=='__main__':main()
