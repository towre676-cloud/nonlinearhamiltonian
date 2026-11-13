"""Finite experiments on the binomial strata below the generic one (not theorems).

For each leading form q^6 + q^a p^b on a Newton edge without interior lattice points, counts
static partners chain by chain up to a weight bound and reports refinement dimensions for the
leading form and for one random member of the stratum.  See GENERIC_SIXFOLD_STRATUM_THEOREM.md.
"""
import random
from fractions import Fraction as Fr
from weighted_cubic_form import gate_system
def run(name,mono,wq,wp,maxw=360):
    W=6*wq; assert wq*mono[0]+wp*mono[1]==W
    h={(6,0):Fr(1),mono:Fr(1)}
    supp=[];tot=0
    for w in range(maxw+1):
        chain=[(a,(w-wq*a)//wp) for a in range(w//wq+1) if (w-wq*a)%wp==0]
        if not chain: continue
        ker=gate_system(h,chain,0).witnesses()
        if ker: tot+=len(ker); supp.append((w,len(ker)))
    top=max(w for w,_ in supp)
    B=[(a,b) for a in range(top//wq+2) for b in range(top//wp+2) if wq*a+wp*b<=top]
    d=[len(gate_system(h,B,r).witnesses()) for r in (0,1,2)]
    # random member of the stratum: all lower-weight monomials of degree<=5
    rnd=random.Random(4); low={(a,b):Fr(rnd.randint(-3,3)) for a in range(6) for b in range(6) if a+b<=5 and wq*a+wp*b<W}
    h2=dict(h); h2.update({k:v for k,v in low.items() if v})
    d2=[len(gate_system(h2,B,r).witnesses()) for r in (0,1,2)]
    print(f'{name}: lead q^6 + q^{mono[0]}p^{mono[1]}, weights ({wq},{wp}); static partners in weights <= {maxw}: {tot}, top weight {top}; dims S^0,S^1,S^2 = {d}; random member with {len(low)} lower terms: {d2}')
run('Sigma2',(1,4),4,5); run('Sigma3',(2,3),3,4); run('Sigma5',(1,3),3,5); run('Sigma1 (regression)',(0,5),5,6)
