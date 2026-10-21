"""Build exact reduced-lattice certificates; standard-library LLL, no trusted LLL claim.

The verifier checks the returned bases, determinants and inverse bounds directly.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import json
ROOT=Path(__file__).resolve().parent
M=2**107-1;A=pow(3,121,M);D=(M-1)//2**26
def gs(B):
    stars=[];norm=[];mu=[[Q(0)for _ in B]for _ in B]
    for i,row in enumerate(B):
        v=list(map(Q,row))
        for j in range(i):
            mu[i][j]=sum(Q(row[t])*stars[j][t]for t in range(len(row)))/norm[j]
            v=[v[t]-mu[i][j]*stars[j][t]for t in range(len(row))]
        stars.append(v);norm.append(sum(x*x for x in v))
    return mu,norm
def lll(B):
    B=[r[:]for r in B];k=1;steps=0;mu,norm=gs(B)
    while k<len(B):
        steps+=1
        if steps>100000:raise RuntimeError('LLL step cap')
        for j in range(k-1,-1,-1):
            v=mu[k][j];q=(2*v.numerator+v.denominator)//(2*v.denominator)
            if q:B[k]=[a-q*b for a,b in zip(B[k],B[j])];mu,norm=gs(B)
        if norm[k]>=(Q(99,100)-mu[k][k-1]**2)*norm[k-1]:k+=1
        else:B[k],B[k-1]=B[k-1],B[k];mu,norm=gs(B);k=max(k-1,1)
    return B,steps
def inverse(B):
    n=len(B);a=[[Q(x)for x in row]+[Q(i==j)for j in range(n)]for i,row in enumerate(B)]
    for k in range(n):
        pivot=next(i for i in range(k,n)if a[i][k]);a[k],a[pivot]=a[pivot],a[k]
        v=a[k][k];a[k]=[x/v for x in a[k]]
        for i in range(n):
            if i!=k:
                v=a[i][k];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
    return[row[n:]for row in a]
def make(positions):
    gaps=[p-positions[0]for p in positions]
    B=[[1]+[pow(A,p,M)for p in gaps[1:]]]+[[0]+[M if i==j else 0 for j in range(4)]for i in range(4)]
    reduced,steps=lll(B);I=inverse(reduced)
    bounds=[D*sum(abs(I[i][j])for i in range(5))for j in range(5)]
    return dict(positions=list(positions),gaps=gaps,basis=reduced,dual_box_bounds=[str(v)for v in bounds],passed=all(v<1 for v in bounds),lll_steps=steps)
def main():
    rows=[]
    for positions in combinations(range(9),5):rows.append(make(positions))
    report=dict(M=M,A=A,output_modulus=2**26,difference_bound=D,records=rows,all_passed=all(r['passed']for r in rows))
    (ROOT/'freelip_certificate.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dict(patterns=len(rows),passed=sum(r['passed']for r in rows),failed=[r['positions']for r in rows if not r['passed']],max_bound=max(float(Q(v))for r in rows for v in r['dual_box_bounds']))))
if __name__=='__main__':main()
