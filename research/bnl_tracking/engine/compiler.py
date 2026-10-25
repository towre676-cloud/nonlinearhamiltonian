"""Fixed-delta transverse compilation of the PyAT0.9 discrete map.

This is not a six-dimensional equivalence: ct is omitted and must not feed back.
An uncertainty guard loss requires a native rerun; it is never a physical loss.
Floating-point regrouping can alter chaotic boundary labels, requiring validation.
"""
import math
import time
import numpy as np
import at

DRIFT1=.6756035959798286638
DRIFT2=-.1756035959798286639
KICK1=1.351207191959657328
KICK2=-1.702414383919314656


def drift(length,dp):
    m=np.eye(5);m[0,1]=m[2,3]=length/(1+dp)
    return m


def kick(length,dp,a,b,h=0.):
    m=np.eye(5)
    a0=float(a[0])if len(a)else 0.;a1=float(a[1])if len(a)>1 else 0.
    b0=float(b[0])if len(b)else 0.;b1=float(b[1])if len(b)>1 else 0.
    m[1,0]=-length*(b1+h*h);m[1,2]=length*a1
    m[3,0]=length*a1;m[3,2]=length*b1
    m[1,4]=length*(dp*h-b0);m[3,4]=length*a0
    return m


def edge(e,dp,entrance):
    h=e.BendingAngle/e.Length
    name='Entrance'if entrance else'Exit'
    theta=float(getattr(e,name+'Angle'))
    method=int(getattr(e,'FringeBend'+name,1))
    if method==3:raise ValueError('nonlinear bend fringe method3')
    fint=float(getattr(e,'FringeInt1'if entrance else'FringeInt2',0))
    gap=float(getattr(e,'FullGap',0))
    corr=0. if fint==0 or gap==0 or method==0 else h*gap*fint*(1+math.sin(theta)**2)/math.cos(theta)
    fx=h*math.tan(theta);fy=h*math.tan(theta-corr/(1+dp))
    if method==2:fy/=1+dp
    m=np.eye(5);m[1,0]=fx;m[3,2]=-fy
    return m


def admissible(e):
    forbidden=['RApertures','EApertures','T1','T2','R1','R2','KickAngle']
    if any(hasattr(e,k)for k in forbidden):return False
    if float(getattr(e,'FieldScaling',1))!=1:return False
    if e.PassMethod=='DriftPass'and isinstance(e,at.Drift):return True
    if e.PassMethod not in ('StrMPoleSymplectic4Pass','BndMPoleSymplectic4Pass'):return False
    if int(getattr(e,'MaxOrder',99))>1:return False
    if any(float(getattr(e,k,0))!=0 for k in ['FringeQuadEntrance','FringeQuadExit']):return False
    if any(int(getattr(e,k,1))==3 for k in ['FringeBendEntrance','FringeBendExit']):return False
    if any(np.any(np.asarray(getattr(e,k))[2:]!=0)for k in ['PolynomA','PolynomB']):return False
    return isinstance(e,(at.Quadrupole,at.Dipole))


def affine_element(e,dp):
    if not admissible(e):raise ValueError('unsupported/nonlinear element')
    if e.PassMethod=='DriftPass':return drift(e.Length,dp)
    n=int(e.NumIntSteps)
    if n<1:raise ValueError('positive integrator steps required')
    sl=e.Length/n;h=e.BendingAngle/e.Length if isinstance(e,at.Dipole)else 0.
    d1=drift(sl*DRIFT1,dp);d2=drift(sl*DRIFT2,dp)
    k1=kick(sl*KICK1,dp,e.PolynomA,e.PolynomB,h)
    k2=kick(sl*KICK2,dp,e.PolynomA,e.PolynomB,h)
    step=d1@k1@d2@k2@d2@k1@d1
    m=np.linalg.matrix_power(step,n)
    if isinstance(e,at.Dipole):m=edge(e,dp,False)@m@edge(e,dp,True)
    return m


def compile_ring(ring,dp=0.,sext_steps=None,guards=True):
    if not math.isfinite(dp)or dp<=-1:raise ValueError('fixed dp must exceed -1')
    if getattr(ring,'is_6d',False)or getattr(ring,'radiation',False):raise ValueError('disable6D first')
    if sext_steps is not None and(type(sext_steps)is not int or sext_steps<1):raise ValueError('positive sextsteps')
    started=time.perf_counter();out=[];blocks=[];guard_indices=[];native_map=[]
    pending=np.eye(5);prefix=[];indices=[];length=0.;ct_ignored=True
    swap=np.eye(6);swap[:4,:4]=np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
    counts={'linear_magnets':0,'drifts':0,'identity':0,'retained_nonlinear':0}
    def append(e,native_index):out.append(e);native_map.append(native_index)
    def flush():
        nonlocal pending,prefix,indices,length
        if not indices:return
        radius=np.array([.05,.025,.05,.025])
        scale=1.
        for m in prefix:
            v=abs(m[:4,:4])@radius;b=abs(m[:4,4])
            if np.any(b>=.45):raise ValueError('linear offset too large for guarded domain')
            ratio=np.min(np.divide(.45-b,v,out=np.full(4,np.inf),where=v>0))
            scale=min(scale,float(ratio))
        radius*=max(0.,min(1.,scale))
        if guards:
            guard_indices.append(len(out));append(at.Aperture('LinearGuardQ',[-radius[0],radius[0],-radius[2],radius[2]]),None)
            append(at.M66('SwapForGuard',swap),None)
            guard_indices.append(len(out));append(at.Aperture('LinearGuardP',[-radius[1],radius[1],-radius[3],radius[3]]),None)
            append(at.M66('UnswapGuard',swap),None)
        m66=np.eye(6);m66[:4,:4]=pending[:4,:4]
        t2=np.zeros(6);t2[:4]=pending[:4,4]
        append(at.M66('CompiledLinearBlock',m66,T2=t2,Length=length),indices[-1])
        blocks.append({'native_indices':indices,'input_radius':radius.tolist(),
                       'max_prefix_bound':max((abs(m[:4,:4])@radius+abs(m[:4,4])).max()for m in prefix),
                       'matrix':pending.tolist()})
        pending=np.eye(5);prefix=[];indices=[];length=0.
    for i,original in enumerate(ring):
        if original.PassMethod=='IdentityPass'and not any(hasattr(original,k)for k in ['RApertures','EApertures','T1','T2','R1','R2']):
            counts['identity']+=1;continue
        if admissible(original):
            pending=affine_element(original,dp)@pending;prefix.append(pending.copy())
            indices.append(i);length+=original.Length
            counts['drifts'if isinstance(original,at.Drift)else'linear_magnets']+=1
        else:
            flush();e=original.deepcopy()
            if sext_steps is not None and isinstance(e,at.Sextupole):e.NumIntSteps=sext_steps
            append(e,i);counts['retained_nonlinear']+=1
    flush()
    compiled=at.Lattice(out,**vars(ring))
    receipt={'dp':dp,'sext_steps':sext_steps,'guards':guards,'guard_indices':guard_indices,
             'native_index_map':native_map,'blocks':blocks,'counts':counts,
             'native_elements':len(ring),'compiled_elements':len(compiled),
             'construction_seconds':time.perf_counter()-started,
             'scope':'Real-arithmetic4Dfixed-delta map equivalence for unchanged sextsteps; ct not preserved; guards require native fallback; floating regrouping and any changed sextsteps empirically qualified.'}
    return compiled,receipt


def track_with_fallback(native,compiled,receipt,initial,turns):
    if np.any(initial[4]!=receipt['dp']):raise ValueError('compiled dp does not match every particle')
    started=time.perf_counter()
    _,params,diag=compiled.track(np.asfortranarray(initial),nturns=turns,refpts=[],losses=True,omp_num_threads=1,keep_lattice=False)
    loss=diag['loss_map'].copy();rout=np.array(params['rout']);uncertain=loss['islost']&np.isin(loss['elem'],receipt['guard_indices'])
    for j in np.flatnonzero(loss['islost']&~uncertain):
        mapped=receipt['native_index_map'][int(loss['elem'][j])]
        if mapped is None:raise ValueError('unmapped nonphysical loss requires fallback')
        loss['elem'][j]=mapped
    fallback_count=int(uncertain.sum())
    if fallback_count:
        _,p2,d2=native.track(np.asfortranarray(initial[:,uncertain]),nturns=turns,refpts=[],losses=True,omp_num_threads=1,keep_lattice=False)
        rout[:,uncertain]=p2['rout'];loss[uncertain]=d2['loss_map']
    return rout,loss,{'seconds':time.perf_counter()-started,'fallback_particles':fallback_count,
                      'guard_uncertain_indices':np.flatnonzero(uncertain).tolist()}
