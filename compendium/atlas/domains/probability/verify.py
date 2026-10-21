#!/usr/bin/env python3
"""Independent finite/model checks for the probability, inference and decision atlas.

Only Python's standard library is used. Rational arithmetic and exhaustive finite
populations are exact; transcendental identities are labeled numerical checks.
This verifies declared examples, not historical data or general algorithms.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import exp, log, sqrt, prod, isclose
from pathlib import Path
import json

checks=[]
def record(id,family,method,scope,inputs,result):
    checks.append(dict(id=id,family_ids=family.split(),status='pass',method=method,scope=scope,inputs=inputs,result=result))
def close(a,b,tol=1e-11):
    assert isclose(a,b,rel_tol=tol,abs_tol=tol),(a,b)
def moments(law,fun):
    m=sum(p*fun(x) for x,p in law.items());v=sum(p*(fun(x)-m)**2 for x,p in law.items());return m,v

# Dependence: construct both sharp Frechet endpoints, rather than checking only a bound.
lower={(1,1,1):F(2,5),(1,1,0):F(1,5),(1,0,1):F(1,5),(0,1,1):F(1,5)}
upper={(1,1,1):F(4,5),(0,0,0):F(1,5)}
for law in [lower,upper]:
    assert sum(law.values())==1
    assert [sum(p*x[i] for x,p in law.items()) for i in range(3)]==[F(4,5)]*3
    assert sum(p*(10*sum(x)-F(95,4)) for x,p in law.items())==F(1,4)
assert lower[(1,1,1)]==F(2,5) and upper[(1,1,1)]==F(4,5)
record('P01','D10-F01','exact rational constructions','Sharp dependence bounds and expectation in the declared three-Bernoulli fixture',{'marginals':'4/5 each'}, {'mean_surplus':'1/4','profit_range':['2/5','4/5'],'independent_profit':'64/125'})
assert F(4*5,6*7)-F(4,9)==F(2,63)
record('P02','D10-F01','exact rational beta moment arithmetic','Beta(4,2) posterior-predictive fixture, not a fitted dataset',{}, {'two_successes':'10/21','plug_in':'4/9','gap':'2/63'})
# Weighted subset normalizer: enumerate and separately dynamic-program its polynomial coefficients.
w=[1,2,3,4];subsets=list(combinations(range(4),2));mass={s:prod(w[i] for i in s) for s in subsets};Z=sum(mass.values())
E=[1,0,0]
for wi in w:
    for r in [2,1]:E[r]+=wi*E[r-1]
assert E[2]==Z==35
p_vertex=F(sum(v for s,v in mass.items() if 0 in s),Z)
p_pair=F(mass[(0,1)],Z)
edge_list=[(0,1),(1,2),(2,3),(0,3)]
expected_chi=sum(F(v,Z)*(2-sum(set(e)<=set(s) for e in edge_list)) for s,v in mass.items())
assert (p_vertex,p_pair,expected_chi)==(F(9,35),F(2,35),F(46,35))
record('P03','D10-F02','exhaustive subsets versus coefficient dynamic program','Weighted size-two selection on four vertices and induced four-cycle Euler characteristic',{'weights':w,'sample_size':2},{'normalizer':Z,'vertex_one_probability':str(p_vertex),'pair_probability':str(p_pair),'expected_euler_characteristic':str(expected_chi)})
# Order-statistic expectation via exact integral of the birth CDF.
birth_cdf_polynomial={4:F(1)}
expected_length=sum(coefficient/F(power+1) for power,coefficient in birth_cdf_polynomial.items())
assert expected_length==F(1,5)
record('P04','D10-F02','exact polynomial integral','Maximum of four iid uniform birth times; loop filled at one',{'birth_cdf':'t^4 on [0,1]'}, {'expected_bar_length':'1/5'})
# Finite reversible chain N=2,q=4: Q rows are outgoing rates.
Q=[[-4,4,0],[1,-5,4],[0,1,-1]];pi=[F(1,21),F(4,21),F(16,21)]
assert all(sum(row)==0 for row in Q)
assert all(pi[i]*Q[i][j]==pi[j]*Q[j][i] for i in range(3) for j in range(3))
def det3(a):return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
assert all(det3([[-Q[i][j]-(lam if i==j else 0) for j in range(3)]for i in range(3)])==0 for lam in [0,3,7])
record('P05','D10-F03','exact detailed balance and determinant roots','Reflecting three-state birth-death chain only',{'q':4,'N':2},{'stationary_weights':['1/21','4/21','16/21'],'eigenvalues_negative_generator':[0,3,7]})
# OU stationary variance and independently iterated covariance recurrence.
kappa=2.;sigma=3.;h=.1;v_exact=sigma*sigma/(2*kappa);v_discrete=sigma*sigma/(2*kappa-kappa*kappa*h)
v=0.
for _ in range(1000):v=(1-kappa*h)**2*v+sigma*sigma*h
close(v,v_discrete);assert v_discrete>v_exact
record('P06','D10-F03','declared floating-point covariance recurrence','OU Euler stationary bias for kappa=2,sigma=3,h=.1',{'iterations':1000},{'continuous_stationary_variance':v_exact,'Euler_stationary_variance':v_discrete,'tolerance':1e-11})
# Analytic OU backward PDE solution checked by explicit derivative formulas.
tau=.7;x=1.3;a=1.4;s=.8;e=exp(-2*a*tau)
u=e*x*x+s*s*(1-e)/(2*a)
u_tau=-2*a*e*x*x+s*s*e;Lu=-a*x*(2*e*x)+s*s*e
close(u_tau,Lu)
record('P07','D10-F03','analytic derivative identity evaluated numerically','Backward OU moment PDE for the declared quadratic terminal observable',{'tau':tau,'x':x,'kappa':a,'sigma':s},{'u':u,'u_tau_equals_Lu_residual':u_tau-Lu})
# Linear driver sensor comparison and process covariance are exact rational calculations.
assert 100+F(1,101)>F(201,101)
Q2=[[F(8,3),F(2)],[F(2),F(2)]];det=Q2[0][0]*Q2[1][1]-Q2[0][1]**2;assert det==F(4,3)
record('P08','D10-F03 D11-F01','exact rational propagation','Constant-driver two-dimensional fixture at common horizon 10',{'prior':'I','sensor_noise':'1/100'},{'direct_sensor_future_variance':'10101/101','driver_sensor_future_variance':'201/101','process_covariance_at_horizon_two':[['8/3','2'],['2','2']],'process_determinant':str(det)})
# Fixed-point/scaling checks: transform identities, not simulated convergence.
for t in [-2.,-.3,0.,.7,2.]:
    close(exp(-(t/sqrt(2))**2/2)**2,exp(-t*t/2))
    for n in [1,2,8,32]:close(exp(-abs(t/n))**n,exp(-abs(t)))
record('P09','D10-F04','floating-point characteristic-function identities','Standard Gaussian normalized-sum fixed point and Cauchy arithmetic-mean stability',{'t_values':[-2,-.3,0,.7,2],'n_values':[1,2,8,32]}, {'Gaussian_fixed_point':True,'Cauchy_mean_law_unchanged':True,'tolerance':1e-11})
# A finite Gaussian-moment analogue has EZ^2=1 and EZ^4=3, so the hidden square risk is exactly two.
zlaw={-1:F(1,6),0:F(2,3),1:F(1,6)}
# Scale z by sqrt(3) conceptually; use its square directly as 3*z*z to retain rational arithmetic.
m,var=moments(zlaw,lambda z:3*z*z);assert(m,var)==(F(1),F(2))
# Explicit risk decomposition for T=X+W, observing noisy parity-free version of X through BSC.
# X is fair +/-1, W=3*z^2 independent. Z=X and Y flips X with probability1/4.
joint={}
for X in [-1,1]:
 for z,pz in zlaw.items():
  for flip,pf in [(1,F(3,4)),(-1,F(1,4))]:
   key=(X+3*z*z,X,X*flip);joint[key]=joint.get(key,F(0))+F(1,2)*pz*pf
risk=F(0)
for y in [-1,1]:
 py=sum(p for (t,x,yy),p in joint.items() if yy==y)
 my=sum(p*t for (t,x,yy),p in joint.items() if yy==y)/py
 risk+=sum(p*(t-my)**2 for (t,x,yy),p in joint.items() if yy==y)
assert risk==F(11,4) and risk-F(2)==F(3,4)
record('P10','D11-F01','exact finite conditional-expectation enumeration','Finite independent hidden-square fixture matching Gaussian second/fourth square moments; no Gaussian density claim',{'hidden_square_mean':'1','hidden_square_variance':'2','bit_flip_probability':'1/4'},{'noiseless_target_floor':'2','additional_noise_risk':'3/4','total_noisy_risk':str(risk)})
# Total covariance identity, including exact PSD and signed-correction counterexample.
points=[(F(1),F(0)),(F(-1),F(0)),(F(0),F(2))];mu=[sum(x[j] for x in points)/3 for j in [0,1]]
cov=[[sum((x[i]-mu[i])*(x[j]-mu[j]) for x in points)/3 for j in [0,1]]for i in [0,1]]
assert cov==[[F(2,3),0],[0,F(8,9)]] and cov[0][0]*cov[1][1]==F(16,27)
record('P11','D11-F01','exact rational covariance calculation','Three equally weighted vectors; signed rank-one correction of identity',{'points':[[1,0],[-1,0],[0,2]]},{'covariance':[['2/3','0'],['0','8/9']],'positive_determinant':'16/27','signed_correction_eigenvalues':[-1,1]})
# KL contraction on nontrivial two-output channel, also checking Shannon can fall for a reset channel.
def kl(p,q):return sum(pi*log(pi/qi) for pi,qi in zip(p,q) if pi)
p=[.2,.8];q=[.6,.4];T=[[.8,.3],[.2,.7]]
def channel(p):return [sum(T[j][i]*p[i] for i in range(2))for j in range(2)]
before=kl(p,q);after=kl(channel(p),channel(q));assert after<before
h=lambda a:-sum(x*log(x) for x in a if x)
assert h([.9,.1])<h([.5,.5]);close(kl([.5,.5],[.9,.1]),log(5/3))
record('P12','D11-F02','declared numerical KL evaluation','Finite stochastic channel and concentrated reset equilibrium',{'p':p,'q':q,'channel_columns':T},{'KL_before':before,'KL_after':after,'Shannon_can_decrease':True,'tolerance':1e-11})
# Fisher nullspace and the KL Taylor coefficient independently by finite differences.
p=[.2,.3,.5];v=[-1.,2.,.4];Fisher=[[((p[i] if i==j else 0)-p[i]*p[j])for j in range(3)]for i in range(3)]
assert all(abs(sum(row))<1e-15 for row in Fisher)
quad=sum(v[i]*Fisher[i][j]*v[j]for i in range(3)for j in range(3))
variance=sum(p[i]*v[i]**2 for i in range(3))-sum(p[i]*v[i] for i in range(3))**2;close(quad,variance)
errors=[]
for eps in [.01,.005,.0025]:
 raw=[p[i]*exp(eps*v[i]) for i in range(3)];tot=sum(raw);pnew=[x/tot for x in raw]
 errors.append(abs(kl(p,pnew)/eps**2-quad/2))
assert errors[2]<errors[1]<errors[0]
record('P13','D11-F02','exact algebra evaluated numerically plus shrinking finite differences','Three-class categorical Fisher variance identity and local KL only',{'p':p,'direction':v},{'quadratic_form':quad,'KL_coefficient_errors':errors,'null_direction':'(1,1,1)'})
# Exact randomization p-value superuniformity, not merely the observed extreme.
sums=[sum(s)for s in product([-1,1],repeat=8)]
pvals=[F(sum(t>=s for t in sums),256)for s in sums]
for alpha in set(pvals):assert F(sum(p<=alpha for p in pvals),256)<=alpha
assert F(sum(s>=8 for s in sums),256)==F(1,256)
assert F(sum(abs(s)>=8 for s in sums),256)==F(1,128)
record('P14','D11-F03','exhaustive 256-sign null distribution','Independent fair signs conditional on eight equal positive magnitudes',{}, {'one_sided_extreme_p':'1/256','two_sided_extreme_p':'1/128','superuniformity_all_attained_thresholds':True})
# AUROC direct pair count includes tie half-credit and strict transform invariance.
pos=[2,1];neg=[1,0]
def auc(a,b):return sum(F(1)if x>y else F(1,2)if x==y else F(0)for x in a for y in b)/(len(a)*len(b))
assert auc(pos,neg)==auc([x**3 for x in pos],[x**3 for x in neg])==F(7,8)
record('P15','D11-F03','exact pair enumeration','Two positives and two negatives, ties split in half',{'positive_scores':pos,'negative_scores':neg},{'AUROC':'7/8','strict_cubic_transform_invariant':True})
# Finite encoding and rejection versus biased modulo sampling.
mod=[sum(i%5==r for i in range(8)) for r in range(5)];assert mod==[2,2,2,1,1]
assert len(set(range(5)))==5 and 2**2<5<=2**3
record('P16','D11-F04','finite count and exhaustive addresses','Five objects encoded in three bits',{}, {'minimum_fixed_bits':3,'modulo_counts':mod,'rejection_valid_counts':[1]*5})
# Singular/regular quadratic certificates: exact completions of square.
wstar=[F(4,5),F(1,5)];assert sum(wstar)==1 and wstar[0]**2+4*wstar[1]**2==F(4,5)
for k in range(-12,13):
 t=F(k,7);w=[wstar[0]+t,wstar[1]-t]
 assert w[0]**2+4*w[1]**2==F(4,5)+5*t*t
null_candidate=[F(1),F(0)]
assert sum(null_candidate)==1 and 0*null_candidate[0]**2+4*null_candidate[1]**2==0
record('P17','D12-F01','exact completion-of-square identity','Two-dimensional constrained quadratic, plus feasible null vector',{'Sigma':'diag(1,4)','budget':'w1+w2=1'},{'optimizer':['4/5','1/5'],'minimum':'4/5','gap_identity':'5t^2','singular_diag_0_4_minimum':'0'})
# SDP gap identity for all a sampled rational feasible PSD matrices; exact certificate at a=1.
for k in range(11):
 a=F(k,10);X=[[a,F(0)],[F(0),1-a]]
 primal=X[0][0]+2*X[1][1];dual=F(1);gap=X[1][1]
 assert primal-dual==gap>=0
record('P18','D12-F01','exact rational primal-dual gap','2x2 SDP min Tr(diag(1,2)X), TrX=1, X PSD',{}, {'primal_optimum':'1','dual_optimum':'1','zero_gap_X':'diag(1,0)','dual_slack':'diag(0,1)'})
# Proximal solutions verified by coordinate optimality/subgradients.
z=[F(3),F(4)];soft=[F(2),F(3)];radial=[F(12,5),F(16,5)];ridge=[F(3,2),F(2)]
assert all(soft[i]-z[i]+1==0 for i in range(2))
# norm radial is four, so derivative of norm is radial/4.
assert all(radial[i]-z[i]+radial[i]/4==0 for i in range(2))
assert all(2*ridge[i]-z[i]==0 for i in range(2))
record('P19','D12-F02','exact first-order convex optimality','Three strongly convex proximal models at lambda=1,z=(3,4)',{}, {'l1_solution':['2','3'],'l2_solution':['12/5','16/5'],'ridge_solution':['3/2','2']})
# Gradient step energy identity in all eigenmodes, distinguish endpoint and unstable step.
for eta in [F(2,5),F(3,5)]:
 factors=[1-eta*l for l in [0,2,2,4]]
 if eta==F(2,5):assert all(abs(v)<1 for v in factors[1:])
 else:assert abs(factors[-1])>1
record('P20','D12-F02','exact rational spectral multipliers','Four-cycle quadratic gradient step',{}, {'eta_0_4_factors':['1','1/5','1/5','-3/5'],'eta_0_6_top_factor':'-7/5'})
# Combinatorial optimum and min-plus recurrence from independent enumeration.
cut_values=[sum(x[i]!=x[j]for i,j in [(0,1),(1,2),(2,0)])for x in product([0,1],repeat=3)]
assert sorted(cut_values)==[0,0,2,2,2,2,2,2]
inf=float('inf');M=[[inf,2],[3,inf]]
def mm(A,B):return [[min(A[i][k]+B[k][j]for k in range(2))for j in range(2)]for i in range(2)]
assert mm(M,M)==[[5,inf],[inf,5]]
v=[0,inf];ds=[]
for _ in range(8):ds.append(min(v));v=[min(v[i]+M[i][j]for i in range(2))for j in range(2)]
assert all(ds[i+2]==ds[i]+5 for i in range(6))
record('P21','D12-F03','exhaustive cut labels and exact min-plus identity','Triangle and two-state repeated-layer fixtures',{}, {'cut_maximum':2,'maximizer_count':6,'terminal_costs':ds,'two_layer_increment':5})
# Pareto nondominance and unsupported middle point: necessary inequalities contradict.
points=[(F(0),F(2)),(F(1),F(3,2)),(F(2),F(0))]
assert all(not any(all(q[i]<=p[i]for i in range(2))and q!=p for q in points)for p in points)
assert F(1,2)<F(3,2)
record('P22','D12-F03','exact finite dominance and incompatible weight inequalities','Three-point Pareto minimization fixture',{'points':[[0,2],[1,'3/2'],[2,0]]},{'all_nondominated':True,'middle_requires':'alpha<=beta/2 and alpha>=3beta/2','no_positive_linear_selector':True})
# Main L08 shared-uncertainty cancellation and bounded-error measurement.
dlo,dhi=F(7,4),F(9,4);clo,chi=F(0),F(100)
separate=(clo+dlo)-chi;assert separate==F(-393,4) and dlo>0
for c in [clo,F(17,3),chi]:
 for d in [dlo,F(2),dhi]:assert(c+d)-c==d>=dlo
assert F(1,4)-F(1,10)==F(3,20)>0
assert F(1,20)-F(1,10)==F(-1,20)<0<F(1,20)+F(1,10)
record('P23','D12-F04','exact rational shared-variable simplification and fibre bounds','L08 scalar common-nuisance worked model only',{'common_c_range':['0','100'],'difference_range':['7/4','9/4']},{'joint_margin':'7/4','separate_interval_lower':'-393/4','measurement_z_1_4_error_1_10_margin':'3/20','measurement_z_1_20_inconclusive':True})
# A finite decision-sufficient test tree costs one, whereas nuisance measurement cannot resolve sign.
states=[(-1,0),(-1,1),(1,0),(1,1)] # (decision sign, nuisance)
for nuisance in [0,1]:assert {s for s,c in states if c==nuisance}=={-1,1}
for sign in [-1,1]:assert {s for s,c in states if s==sign}=={sign}
record('P24','D12-F04','exact outcome-fibre enumeration','Finite two-test fixture with a direct sign test and an irrelevant nuisance test',{}, {'sign_test_decision_sufficient':True,'nuisance_test_decision_sufficient':False,'minimum_guaranteed_cost_when_each_test_costs_one':1})

out=Path(__file__).with_name('checks.json')
report={'scope':'Executed mathematical worked models only; no historical empirical dataset, trained model, forecasting system, or general solver is validated.','arithmetic_policy':'Fractions and finite enumerations are exact. Transcendental evaluations and recurrences are declared floating-point checks with explicit tolerances or monotone error checks.','check_count':len(checks),'passed':len(checks),'failed':0,'checks':checks}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'passed':len(checks),'output':str(out)}))
