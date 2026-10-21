"""Calculated figures for the2025 mathematical developments; no external data."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
                     'axes.spines.right':False,'figure.facecolor':'white'})
blue='#23536f';teal='#238c83';orange='#c97935';meta=[]

t=np.linspace(0,2*np.pi,12001)
x=np.cos(t)+.5*np.cos(2*t)+.5*np.cos(4*t)+.375*np.cos(8*t)
y=2*np.sin(t)-np.sin(2*t)+np.sin(4*t)-.75*np.sin(8*t)
dx=-np.sin(t)-np.sin(2*t)-2*np.sin(4*t)-3*np.sin(8*t)
dy=2*np.cos(t)-2*np.cos(2*t)+4*np.cos(4*t)-6*np.cos(8*t)
z=x+1j*y;dz=dx+1j*dy;w=z+1j*dz
fig,axs=plt.subplots(1,3,figsize=(13,4.4),layout='constrained')
for ax,v,title,color in zip(axs,[z,dz,w],['Recovered oscillator curve','Tangent: exact winding -2','z + i z-prime: exact winding -6'],[blue,teal,orange]):
    ax.plot(v.real,v.imag,lw=1.05,color=color)
    ax.scatter([v.real[0]],[v.imag[0]],s=26,c=color,zorder=5)
    ax.scatter([0],[0],marker='+',s=65,c='#222222',zorder=5)
    ax.set_aspect('equal',adjustable='datalim');ax.set_title(title,fontsize=11)
    ax.set_xlabel('Real coordinate');ax.set_ylabel('Imaginary coordinate');ax.grid(alpha=.15)
fig.savefig(OUT/'december_oscillator.png',dpi=180);plt.close(fig)
with (OUT/'december_oscillator.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['t','x','y','dx','dy','w_real','w_imag'])
    writer.writerows(zip(t,x,y,dx,dy,w.real,w.imag))
meta.append(dict(file='december_oscillator.png',caption='The exact trigonometric curve recovered from22December2025, its tangent, and w=z+i z-prime. Samples draw the curves; the nonvanishing and winding claims are certified separately by integer-polynomial Rouche reduction in independent_audit.py. The scalar x coordinate already requires an8-dimensional linear realization.'))

r=np.linspace(.15,1.28,600);a,q=1.1,.74;ar,qr=1.05,.51
b=a/(1-q*r);br=ar/(1-qr*r)
fig,axs=plt.subplots(1,2,figsize=(12,4.3),layout='constrained')
axs[0].plot(r,b,color=blue,label='A=1.10, q=0.74')
axs[0].plot(r,br,color=teal,label='A=1.05, q=0.51')
axs[0].set_ylabel('Exact weighted operator norm B(R)');axs[0].set_xlabel('Weight R')
axs[0].legend(frameon=False);axs[0].grid(alpha=.15)
axs[1].plot(r,80*np.log10(b),color=blue,label='First kernel')
axs[1].plot(r,80*np.log10(br),color=teal,label='Second kernel')
axs[1].set_ylabel('log10 of norm after80 compositions');axs[1].set_xlabel('Weight R')
axs[1].grid(alpha=.15)
fig.savefig(OUT/'december_weighted_operator.png',dpi=180);plt.close(fig)
with (OUT/'december_weighted_operator.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['R','B','B_second','log10_B80','log10_Bsecond80'])
    writer.writerows(zip(r,b,br,80*np.log10(b),80*np.log10(br)))
meta.append(dict(file='december_weighted_operator.png',caption='Explicit positive convolution models T_ij=A q^(i-j) for i>=j on weighted ell-one, with norm sum |f_i|R^i. Their exact norms are B(R)=A/(1-qR), and their80-fold composition norms are B(R)^80. Constants define these illustrative mathematical models; the plots do not reproduce or establish a measured machine-learning advantage.'))

m=np.linspace(-1.5,1.5,1200);u=m**4/4-m*m/2
fig,axs=plt.subplots(1,2,figsize=(12,4.3),layout='constrained')
axs[0].plot(m,u,color=blue);axs[0].scatter([-1,0,1],[-.25,0,-.25],c=[teal,orange,teal])
axs[0].annotate('Barrier =1/4',xy=(0,-.125),xytext=(.25,.10),arrowprops={'arrowstyle':'->','color':orange})
axs[0].set_xlabel('State m');axs[0].set_ylabel('U(m)=m^4/4-m^2/2');axs[0].grid(alpha=.15)
d=np.linspace(.015,.15,600)
logtime=np.log10(np.sqrt(2)*np.pi)+(.25/d)/np.log(10)
axs[1].plot(1/d,logtime,color=teal)
axs[1].set_xlabel('Inverse noise scale1/D');axs[1].set_ylabel('log10 of Kramers approximation');axs[1].grid(alpha=.15)
fig.savefig(OUT/'december_pitchfork.png',dpi=180);plt.close(fig)
with (OUT/'december_pitchfork.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['D','log10_Kramers_approximation']);writer.writerows(zip(d,logtime))
meta.append(dict(file='december_pitchfork.png',caption='A fully specified symmetric double-well model U(m)=m^4/4-m^2/2. For dM=-U-prime(M)dt+sqrt(2D)dW, the barrier is1/4 and the small-noise Kramers approximation for transition to the other well is sqrt(2)*pi*exp(1/(4D)). The right panel displays that asymptotic formula, not simulated or measured escape times.'))

(OUT/'figures.json').write_text(json.dumps(meta,indent=2))
(OUT/'figure_scope.json').write_text(json.dumps({'data':'Analytic formulas, source curve and stipulated models only','numerical_samples':'For rendering and CSV export; exact certificate supplied for oscillator topology','external_measurements':False},indent=2))
print(json.dumps({'figures':len(meta),'directory':str(OUT)}))
