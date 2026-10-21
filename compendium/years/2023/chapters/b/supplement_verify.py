#!/usr/bin/env python3
"""Exact induced-subgraph and heat-margin certificates for supplemental S011."""
from itertools import combinations,permutations
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,math

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('chapter_b_verify',HERE/'verify.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def mask_matrix(mask,n):
    A=[[0]*n for _ in range(n)]
    for bit,(i,j) in enumerate(combinations(range(n),2)):A[i][j]=A[j][i]=(mask>>bit)&1
    return A

def canonical_mask(A):
    n=len(A);edges=list(combinations(range(n),2));best=None
    for p in permutations(range(n)):
        value=sum(A[p[i]][p[j]]<<bit for bit,(i,j) in enumerate(edges))
        if best is None or value<best:best=value
    return best or 0

def induced_pattern_counts(A,k):
    counts={}
    for vertices in combinations(range(len(A)),k):
        M=[[A[i][j] for j in vertices] for i in vertices]
        key=canonical_mask(M);counts[key]=counts.get(key,0)+1
    return counts

def pattern_label(A):
    ds=tuple(sorted(map(sum,A),reverse=True));e=sum(ds)//2
    names={
      (0,(0,0,0,0)):'empty',
      (1,(1,1,0,0)):'one edge and two isolated vertices',
      (2,(1,1,1,1)):'two disjoint edges',
      (2,(2,1,1,0)):'three-vertex path and isolated vertex',
      (3,(2,2,2,0)):'triangle and isolated vertex',
      (3,(3,1,1,1)):'three-leaf star',
      (3,(2,2,1,1)):'four-vertex path',
      (4,(2,2,2,2)):'four-cycle',
      (4,(3,2,2,1)):'triangle with pendant vertex',
      (5,(3,3,2,2)):'diamond',
      (6,(3,3,3,3)):'four-clique',
    }
    return names[e,ds]

def main():
    R=base.rook_adjacency();S=base.shrikhande_adjacency()
    # Independently derive the full set of isomorphism classes of simple 4-vertex graphs.
    keys=sorted({canonical_mask(mask_matrix(m,4)) for m in range(64)})
    assert len(keys)==11
    by_order={}
    for k in range(4):
        r=induced_pattern_counts(R,k);s=induced_pattern_counts(S,k)
        assert r==s
        assert sum(r.values())==math.comb(16,k)
        by_order[str(k)]={'rook':{str(a):b for a,b in r.items()},'shrikhande':{str(a):b for a,b in s.items()}}
    # Direct SRG parameter formulas for the order-three induced distribution.
    v,k,lam,mu=16,6,2,2
    triangles=v*k*lam//6
    paths=v*(math.comb(k,2)-k*lam//2)
    single_edges=(v*k//2)*(v-2*k+lam)
    empty=math.comb(v,3)-triangles-paths-single_edges
    assert [empty,single_edges,paths,triangles]==[96,288,144,32]
    triples=induced_pattern_counts(R,3)
    assert triples=={0:96,1:288,3:144,7:32}
    rc=induced_pattern_counts(R,4);sc=induced_pattern_counts(S,4)
    table=[]
    for key in keys:
        A=mask_matrix(key,4)
        table.append({'canonical_mask':key,'name':pattern_label(A),'edges':sum(map(sum,A))//2,
                      'degrees':sorted(map(sum,A),reverse=True),'rook':rc.get(key,0),'shrikhande':sc.get(key,0)})
    assert sum(x['rook'] for x in table)==sum(x['shrikhande'] for x in table)==1820
    assert rc.get(63,0)==8 and sc.get(63,0)==0
    assert R[0][2]==1 and S[0][2]==0
    # At t=log(2)/4 the exact exponentials are 1/2 and 1/4.
    a,b=F(1,2),F(1,4)
    beta=(a-b)/4;gamma=(1-2*a+b)/16;diagonal=(a+b)/2+gamma
    assert beta==F(1,16) and gamma==F(1,64) and beta+gamma==F(5,64)
    assert diagonal==F(25,64) and diagonal+6*(beta+gamma)+9*gamma==1
    assert beta/2==F(1,32)
    # An unobserved timing interval is a different nuisance-parameter problem.
    r=F(3,2);u=r/2;l=1/(2*r)
    minimum_rook=(1+2*u-3*u*u)/16;maximum_shrikhande=(1-l)**2/16
    assert minimum_rook==F(13,256) and maximum_shrikhande==F(1,36)
    assert minimum_rook-maximum_shrikhande==F(53,2304)
    assert (minimum_rook-maximum_shrikhande)/2==F(53,4608)
    t=math.log(2)/4
    assert abs((math.exp(-4*t)-math.exp(-8*t))/4-float(beta))<1e-15
    # Sharpness of the quadratic maximization, with exact values across the unit interval.
    for j in range(101):
        x=F(j,100)
        assert F(1,16)-x*(1-x)/4==(x-F(1,2))**2/4
    result={'id':'S011','name':'Observation order and sharp aligned heat-entry margin','status':'passed',
            'detail':'Induced graph distributions agree at orders0–3, differ atorder4; all11 four-vertex classes enumerated. Heat margin maximum1/16 at t=log2/4, bounded-error threshold1/32 for the specified aligned pair.',
            'orders_zero_through_three':by_order,
            'srg_triple_formulas':{'empty':empty,'single_edge':single_edges,'path':paths,'triangle':triangles},
            'four_vertex_distributions':table,
            'heat_margin':{'aligned_vertices':[[0,0],[0,2]],'time':'log(2)/4','rook_entry':'5/64','shrikhande_entry':'1/64',
                           'margin':'1/16','strict_bounded_error_threshold':'1/32','midpoint_threshold':'3/64',
                           'scope':'known coordinate labels and one fixed pair of candidate graphs; not uniform unlabeled recovery'},
            'unobserved_time_example':{'time_halfwidth':'log(3/2)/4','minimum_rook':'13/256','maximum_shrikhande':'1/36',
                                      'uniform_gap':'53/2304','strict_error_threshold':'53/4608'}}
    target=HERE/'supplement_checks.json';target.write_text(json.dumps({'checks':[result],'passed':1,'failed':0},ensure_ascii=False,indent=2))
    print(json.dumps({'passed':1,'four_vertex_classes':11,'rook_four_cliques':8,'shrikhande_four_cliques':0,'output':str(target)}))
    print(json.dumps(table,ensure_ascii=False))

if __name__=='__main__':main()
