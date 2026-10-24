"""Conditional emittance predictor using only unexplained-force kick radii.

This module proves arithmetic consequences of supplied moment bounds. It never
certifies that a model, sampled cloud or continuum field satisfies those bounds.
Each kick needs its own valid premise; no stationarity or closure is assumed.
"""
from fractions import Fraction
from exact import rational,sqrt_upper,determinant,is_psd


def residual_radius_squared(h,position_variance_upper,force_variance_upper,q_force_interval):
    """Bound h²(a E[F_c²]−E[x_c F_c]²) from valid centered-moment bounds."""
    h,a,ell=map(rational,(h,position_variance_upper,force_variance_upper))
    lo,hi=map(rational,q_force_interval)
    if a<0 or ell<0 or lo>hi:
        raise ValueError('invalid moment-bound premises')
    magnitude=Fraction(0) if lo<=0<=hi else min(abs(lo),abs(hi))
    residual=a*ell-magnitude*magnitude
    if residual<0:
        raise ValueError('inconsistent moment premises: negative residual upper bound')
    return {'radius_squared':h*h*residual,'full_force_radius_squared':h*h*a*ell,
            'cancelled_squared_correlation':magnitude*magnitude,
            'scope':'conditional centered-moment enclosure; premise coverage not established'}


def round_profile_radius_squared(h,kappa,radial_mean,radial_force_factor_upper):
    """Ideal round-continuum specialization.

    t=r²/R², mu=E[t], B>=E[M(t)²/t], M(t)=Pr(T<=t), and
    F=kappa*q*M(t)/r². Per plane a*E[g²]<=kappa²/4*(mu*B−1/4).
    Validity requires the actual round continuum profile and a true B bound;
    quadrupoles, PIC field error, boundaries and empirical particles are extra.
    """
    h,kappa,mu,b=map(rational,(h,kappa,radial_mean,radial_force_factor_upper))
    if mu<=0 or b<0 or mu*b<Fraction(1,4):
        raise ValueError('inconsistent round-profile upper-bound premises')
    return h*h*kappa*kappa/Fraction(4)*(mu*b-Fraction(1,4))


def propagate(initial_covariance,word,bits=80):
    """Return a conditional rational interval after uncoupled maps and kicks.

    Initial covariance is centered in one plane. Supported external maps are
    exact 2 by 2 determinant-one matrices. A kick supplies a nonnegative upper
    bound on h²*a*E[g²], already including its own h. No cross-plane map is
    silently accepted and no missing force premise is filled by a heuristic.
    """
    sigma=[[rational(v) for v in row]for row in initial_covariance]
    if len(sigma)!=2 or any(len(row)!=2 for row in sigma)or not is_psd(sigma):
        raise ValueError('centered PSD two-by-two initial covariance required')
    eps2=determinant(sigma);eps_hi=sqrt_upper(eps2,bits)
    step=Fraction(1,1<<bits)
    eps_lo=eps_hi if eps_hi*eps_hi==eps2 else max(Fraction(0),eps_hi-step)
    total=Fraction(0);premises=[]
    for index,action in enumerate(word):
        kind=action.get('kind')
        if kind=='uncoupled_symplectic':
            matrix=action['matrix']
            if len(matrix)!=2 or any(len(row)!=2 for row in matrix)or determinant(matrix)!=1:
                raise ValueError('external map must be an exact two-by-two determinant-one matrix')
        elif kind=='residual_force_kick':
            radius2=rational(action['radius_squared_upper'])
            if radius2<0 or not action.get('premise_id'):
                raise ValueError('each kick needs a nonnegative bound and explicit premise identifier')
            radius=sqrt_upper(radius2,bits);total+=radius
            premises.append({'action':index,'premise_id':action['premise_id'],
                             'radius_squared_upper':radius2,'radius_upper':radius})
        else:
            raise ValueError('unsupported action; coupling/loss/resampling requires a separate theorem')
    return {'lower':max(Fraction(0),eps_lo-total),'upper':eps_hi+total,
            'initial_eps_squared':eps2,'total_radius_upper':total,'kick_premises':premises,
            'status':'conditional','force_premises_verified':False,
            'scope':'Exact algebra conditional on every stated force-moment premise; not a physical coverage or speedup certificate.'}
