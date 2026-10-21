"""Calculated scientific illustrations; regeneration requires numpy/matplotlib."""
from pathlib import Path
from math import gcd
from collections import Counter
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
meta=[]
delta=1e-4;N=np.arange(1,501)
fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
ax.loglog(N,1/(N+1),label='Bias bound 1/(N+1)',color='#23536f',lw=2)
ax.loglog(N,delta*N,label='Noise bound δN',color='#bb7043',lw=2)
ax.loglog(N,1/(N+1)+delta*N,label='Total guaranteed error',color='#367d69',lw=2.4)
ax.axvline(100,color='#7f8b93',ls=':',lw=1.5)
ax.set(xlabel='Cutoff dimension N',ylabel='Deterministic norm-error bound',title='Resolution improves bias and amplifies noise')
ax.legend(frameon=False);ax.grid(alpha=.16)
fig.savefig(OUT/'cutoff-balance.png',dpi=170);plt.close(fig)
meta.append(dict(file='cutoff-balance.png',caption='Calculated bounds for the new diagonal example Ae_k=e_k/k on the ellipsoid Σk²|x_k|²≤1, with δ=10⁻⁴. The choice N=100 has error below0.02; every reconstruction has worst-case error at least0.01. These are deterministic model bounds, not empirical measurements. EntriesY26-08-901–902.'))
G=[(0,3),(0,4),(0,6),(1,2),(1,3),(2,3),(2,4),(3,5)]
H=[(0,1),(0,4),(0,6),(1,5),(1,6),(2,6),(3,6),(4,5)]
angles=np.pi/2+np.arange(7)*2*np.pi/7
pos=np.c_[np.cos(angles),np.sin(angles)]
fig,axes=plt.subplots(1,2,figsize=(9,4.4),layout='constrained')
for ax,E,label in zip(axes,[G,H],['Graph G','Graph H']):
    for u,v in E:ax.plot(pos[[u,v],0],pos[[u,v],1],color='#8aa5b6',lw=1.7,zorder=1)
    ax.scatter(pos[:,0],pos[:,1],s=600,color='#23536f',zorder=2)
    for i,(x,y)in enumerate(pos):ax.text(x,y,str(i),ha='center',va='center',color='white',weight='bold')
    ax.set(aspect='equal',xlim=(-1.3,1.3),ylim=(-1.3,1.3),title=label);ax.axis('off')
fig.suptitle('Equal binary energy censuses; different multilevel populations',fontsize=14)
fig.savefig(OUT/'graph-observation-collision.png',dpi=170);plt.close(fig)
meta.append(dict(file='graph-observation-collision.png',caption='The recovered seven-vertex edge sets have exactly equal(size,energy) counts over all128 binary assignments. Allowing total integer height3 separates them: the difference isq³(1−q)(1−q³)²(1−q⁴)², equal to11025/262144 atq=1/2. The independent exact verifier enumerates both populations.'))
units=[a for a in range(1680)if gcd(a,1680)==1];fibres=Counter(a%30 for a in units)
fig,ax=plt.subplots(figsize=(9,4.2),layout='constrained')
r=sorted(fibres);ax.bar([str(a)for a in r],[fibres[a]for a in r],color='#367d69',width=.65)
ax.set(xlabel='Primitive exponent modulo30',ylabel='Primitive preimages modulo1680',ylim=(0,56),title='The conductor bridge has eight equal fibres')
for i,a in enumerate(r):ax.text(i,49,'48',ha='center',va='bottom',color='#23536f')
fig.savefig(OUT/'conductor-fibres.png',dpi=170);plt.close(fig)
meta.append(dict(file='conductor-fibres.png',caption='Exact residue enumeration: all384 primitive conductor1680 phases map under the56th power to the8 primitive conductor30 phases, with48 preimages each. This is a finite phase/field-degree calculation; it does not alone prove an E8 lattice isometry or KZ monodromy closure.'))
(OUT/'figures.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print(json.dumps(dict(figures=len(meta))))
