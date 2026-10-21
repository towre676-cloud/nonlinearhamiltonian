"""Generate exact-data illustrations for June, September and December mathematics."""
from pathlib import Path
import math,json,csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;F=P/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':180})
figs=[]
roots=[complex(s*math.sqrt(2),t) for s in [-1,1] for t in [-1,1]]
fig,ax=plt.subplots(figsize=(9,4.5))
ax.axhline(0,color='#cbd6de',lw=.8);ax.axvline(0,color='#cbd6de',lw=.8)
ax.plot([z.real for z in roots],[z.imag for z in roots],'o',color='#235c7e',ms=9)
for z in roots:
    sx='−' if z.real<0 else '';sy='−' if z.imag<0 else '+'
    ax.annotate(sx+'√2 '+sy+' i',(z.real,z.imag),xytext=(8,10 if z.imag>0 else -18),textcoords='offset points')
ax.plot([-math.sqrt(2),math.sqrt(2)],[-1,-1],'--',color='#8aafc3',lw=1)
ax.plot([-math.sqrt(2),math.sqrt(2)],[1,1],'--',color='#8aafc3',lw=1)
ax.set(xlim=(-2.4,2.4),ylim=(-1.6,1.6),xlabel='Real coordinate',ylabel='Imaginary coordinate',title='June: roots of x⁴ − 2x² + 9 and independent sign changes')
ax.set_aspect('equal');fig.tight_layout();fig.savefig(F/'june_quartic.png');plt.close(fig)
figs.append(dict(file='june_quartic.png',caption='The roots are ±√2±i. Independent changes of the signs of √2 and i generate the four automorphisms of Q(√2,i)/Q. Thus the splitting group is V₄. The figure is calculated from the corrected factorization; it is not an inference from approximate root geometry alone.'))

def count(p):
    return 1+sum((y*y+y-x*x*x+x)%p==0 for x in range(p) for y in range(p))
rows=[]
for p in [2,3,5,7,11,13,17,19,23,29,31]:
    n=count(p);a=p+1-n;warped=a+(.0334*math.copysign(abs(a)**.673,a) if a else 0)
    rows.append(dict(p=p,points=n,trace=a,warped=warped,difference=warped-a))
with (F/'september_traces.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
fig,(ax,bx)=plt.subplots(1,2,figsize=(10,4.3))
ax.plot([r['p'] for r in rows],[r['trace'] for r in rows],'o-',color='#225a79',label='Exact finite-field trace')
ax.plot([r['p'] for r in rows],[r['warped'] for r in rows],'x',color='#bb6742',label='Numerically warped value')
ax.set(xlabel='Good prime p',ylabel='Trace',title='September: E : y² + y = x³ − x');ax.legend(fontsize=8)
bx.axhline(0,color='#cbd6de',lw=.8);bx.plot([r['p'] for r in rows],[r['difference'] for r in rows],'o-',color='#bb6742')
bx.set(xlabel='Good prime p',ylabel='Warped value minus integer trace',title='The coordinate warp changes arithmetic data')
fig.tight_layout();fig.savefig(F/'september_traces.png');plt.close(fig)
figs.append(dict(file='september_traces.png',caption='Exact point counts determine integer Frobenius traces for y²+y=x³−x at the listed good primes. The displayed warp is a ↦ a+0.0334 sign(a)|a|^0.673, evaluated numerically. A transformed real number is not automatically the trace of another elliptic curve; retaining a numerical range does not establish integrality or an Euler factor of arithmetic origin.'))

eps=[10**(-k/4) for k in range(1,49)]
data=[dict(epsilon=e,operator_perturbation=e,eigenvalue_magnitude=math.sqrt(e),eigenvector_condition=1/math.sqrt(e)) for e in eps]
with (F/'december_jordan.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
fig,(ax,bx)=plt.subplots(1,2,figsize=(10,4.3))
ax.loglog(eps,[math.sqrt(e) for e in eps],color='#235c7e',label='Eigenvalue magnitude √ε')
ax.loglog(eps,eps,'--',color='#9caebb',label='Matrix perturbation norm ε')
ax.set(xlabel='ε > 0',ylabel='Magnitude',title='December: Aε = [[0, 1], [ε, 0]]');ax.legend(fontsize=8)
bx.loglog(eps,[1/math.sqrt(e) for e in eps],color='#bb6742');bx.set(xlabel='ε > 0',ylabel='2-norm condition number',title='An eigenvector basis becomes ill-conditioned')
fig.tight_layout();fig.savefig(F/'december_jordan.png');plt.close(fig)
figs.append(dict(file='december_jordan.png',caption='At ε=0 the matrix has one Jordan block of length two. For 0<ε≤1 its eigenvalues are ±√ε, the perturbation has 2-norm ε, and V=[[1,1],[√ε,−√ε]] has condition number ε^(−1/2). This exact family explains why numerical Jordan-block decisions need more than an arbitrary small threshold.'))
(F/'figures.json').write_text(json.dumps(figs,ensure_ascii=False,indent=2))
(F/'figure_data.json').write_text(json.dumps(dict(roots=[[z.real,z.imag] for z in roots],traces=rows,jordan=data),indent=2))
print(json.dumps(dict(figures=len(figs),point_count_primes=len(rows),jordan_samples=len(data))))
