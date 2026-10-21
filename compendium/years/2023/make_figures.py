"""Regenerate the two scientific figures. Optional build dependency: matplotlib."""
from pathlib import Path
import math,csv,cmath
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
F=P/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#243b50','axes.edgecolor':'#879bad','xtick.color':'#4a6072','ytick.color':'#4a6072','figure.facecolor':'white','axes.facecolor':'white'})
def phi(z):return 0 if not math.isfinite(z) else math.exp(-z*z/2)/math.sqrt(2*math.pi)
def Phi(z):return .5*(1+math.erf(z/math.sqrt(2)))
def info(mu,bins,sigma=1):
 edges=[-math.inf]+[math.atanh(math.sin(-math.pi/2+math.pi*j/bins)) for j in range(1,bins)]+[math.inf]
 total=0
 for a,b in zip(edges,edges[1:]):
  za=(a-mu)/sigma;zb=(b-mu)/sigma;p=Phi(zb)-Phi(za);dp=(phi(za)-phi(zb))/sigma
  if p>1e-300:total+=dp*dp/p
 return total
mus=[-3+6*j/240 for j in range(241)];colors=['#a55132','#3b7b99','#294f6c']
fig,ax=plt.subplots(figsize=(7.2,3.8),layout='constrained')
records=[]
for bins,col in zip([4,8,16],colors):
 ys=[info(mu,bins) for mu in mus]
 assert max(ys)<=1+1e-11
 ax.plot(mus,ys,label=f'{bins} equal angle bins',color=col,lw=2)
 records.extend((mu,bins,y) for mu,y in zip(mus,ys))
ax.axhline(1,color='#658174',ls='--',lw=1.7,label='Exact reversible observation')
ax.set(xlabel='Gaussian location μ with known σ = 1',ylabel='Retained Fisher information',ylim=(0,1.07),xlim=(-3,3))
ax.grid(axis='y',alpha=.16);ax.legend(fontsize=8.7,loc='lower center',ncol=2,frameon=False)
fig.savefig(F/'gudermannian_information.png',dpi=220);plt.close(fig)
with (F/'gudermannian_information.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['mu','angle_bins','Fisher_information']);w.writerows(records)

times=[.001+.799*j/400 for j in range(401)]
margin=[(math.exp(-4*t)-math.exp(-8*t))/4 for t in times]
condition=[math.exp(8*t)/(8*t) for t in times]
tstar=math.log(2)/4
fig,(ax,bx)=plt.subplots(1,2,figsize=(8.6,3.5),layout='constrained')
ax.plot(times,margin,color='#225e86',lw=2);ax.axvline(tstar,ls='--',color='#9a643d',lw=1);ax.scatter([tstar],[1/16],color='#9a643d',zorder=5,s=22)
ax.set(xlabel='Heat time t',ylabel='Aligned heat-entry difference',title='Distinguishing the two labeled graphs',xlim=(0,.8),ylim=(0,.068));ax.annotate('maximum 1/16\nat t = log(2)/4',(tstar,1/16),xytext=(.32,.051),fontsize=8.5,arrowprops=dict(arrowstyle='-',color='#879bad'))
bx.plot(times,condition,color='#386b57',lw=2);bx.axvline(1/8,ls='--',color='#9a643d',lw=1);bx.scatter([1/8],[math.e],color='#9a643d',s=22,zorder=5)
bx.set(xlabel='Heat time t with generator bound Λ = 8',ylabel='Normalized inverse bound e^(8t)/(8t)',title='Bounding full-kernel reconstruction error',xlim=(0,.8),ylim=(2,30));bx.annotate('minimum e\nat t = 1/8',(1/8,math.e),xytext=(.27,8),fontsize=8.5,arrowprops=dict(arrowstyle='-',color='#879bad'))
for a in [ax,bx]:a.grid(axis='y',alpha=.16)
fig.savefig(F/'heat_observation_tradeoff.png',dpi=220);plt.close(fig)
with (F/'heat_observation_tradeoff.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['t','aligned_entry_gap','normalized_inverse_bound']);w.writerows(zip(times,margin,condition))
print('Created two scientific figures and their numerical tables')

# This is analytic continuation of algebraic eigenlabels, not KZ connection holonomy.
t0=complex(.5,math.sqrt(3)/2);radius=.13
ts=[t0+radius*cmath.exp(2j*math.pi*k/600) for k in range(601)]
roots=[];last=None
for t in ts:
 d=t*t-t+1;s=cmath.sqrt(d)
 if last is not None and abs(-s-last)<abs(s-last):s=-s
 last=s;w=(1+t+s)/3;v=(1+t-s)/3
 assert abs(3*w*w-2*(1+t)*w+t)<1e-12
 roots.append((w,v))
assert abs(roots[-1][0]-roots[0][1])<1e-12
assert abs(roots[-1][1]-roots[0][0])<1e-12
fig,(ax,bx)=plt.subplots(1,2,figsize=(8.6,3.7),layout='constrained')
ax.plot([z.real for z in ts],[z.imag for z in ts],color='#516f86',lw=1.8);ax.scatter([t0.real],[t0.imag],marker='x',s=45,color='#9a4c38');ax.scatter([ts[0].real],[ts[0].imag],s=28,color='#516f86');ax.set(xlabel='Re t',ylabel='Im t',title='One loop around t² − t + 1 = 0');ax.set_aspect('equal',adjustable='datalim')
for j,col in [(0,'#245d88'),(1,'#ab6538')]:
 z=[pair[j] for pair in roots];bx.plot([x.real for x in z],[x.imag for x in z],color=col,lw=2,label='Continued branch '+('A' if j==0 else 'B'));bx.scatter([z[0].real],[z[0].imag],s=30,color=col,zorder=5)
 k=290;bx.annotate('',xy=(z[k+15].real,z[k+15].imag),xytext=(z[k].real,z[k].imag),arrowprops=dict(arrowstyle='->',color=col,lw=1.5))
bx.set(xlabel='Re w',ylabel='Im w',title='The two Bethe-root labels exchange');bx.set_aspect('equal',adjustable='datalim');bx.legend(frameon=False,fontsize=8,loc='best')
for a in [ax,bx]:a.grid(alpha=.14)
fig.savefig(F/'gaudin_spectral_cover.png',dpi=220);plt.close(fig)
with (F/'gaudin_spectral_cover.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['t_real','t_imag','A_real','A_imag','B_real','B_imag']);w.writerows((t.real,t.imag,a.real,a.imag,b.real,b.imag) for t,(a,b) in zip(ts,roots))
print('Created spectral-cover figure; continuation swaps both roots within 1e-12')
