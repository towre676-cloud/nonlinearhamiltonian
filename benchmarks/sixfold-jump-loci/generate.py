"""Generate the rational sixfold benchmark from the pinned theorem implementation."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import sys

import numpy as np
from scipy.integrate import solve_ivp
import sympy as S

SOURCE = Path(__file__).resolve().parent / 'sources'
sys.path.insert(0, str(SOURCE))
import sixfold_global_depth as G
import sixfold_jump_loci as J

SEED = 20261115
EPS = [F(1, 10), F(1, 1000), F(1, 100000)]
NOISE = np.array([0., 1e-5, 1e-3, 1e-2])
WINDOW = {'quartic': (2, 3, 20), 'c32': (2, 3, 26),
          'delta': (1, 2, 12), 'gamma': (1, 2, 12), 'origin': (1, 2, 12)}


def terms(h):
    return [[i, j, str(c)] for (i, j), c in sorted(h.items()) if c]


def read_terms(rows):
    return {(i, j): F(c) for i, j, c in rows}


def polynomial(expr, q, p):
    return {(i, j): F(str(c)) for (i, j), c in S.Poly(expr, q, p).terms() if c}


def instance(kind, rng, index):
    def small():
        return F(rng.randint(-5, 5), 20)
    h = {(6, 0): F(1), (1, 0): small(), (2, 0): small(),
         (3, 0): small(), (0, 1): small(), (1, 1): small()}
    if kind == 'quartic':
        gamma = F(rng.randint(4, 14), 10)
        y = -gamma**2 / 40
        r13, r22, r31, r12 = (small() for _ in range(4))
        h.update({(0, 4): y, (3, 2): gamma, (1, 3): r13,
                  (2, 2): r22, (3, 1): r31, (1, 2): r12})
        h[4, 1] = gamma*r13/(2*y)
        h[5, 0] = -gamma*(-13*r13**2 + 8*r22*y)/(160*y**2)
        h[0, 3] = -gamma*(r13**3 - 4*r13*r22*y + 8*r31*y**2)/(160*y**2)
        h[4, 0] = (9*gamma**2*r13**4 - 36*gamma**2*r13**2*r22*y
                   + 72*gamma**2*r13*r31*y**2 + 1920*gamma*r12*y**3
                   + 3840*r13*r31*y**3 - 1280*r22**2*y**3)/(15360*y**4)
        h[2, 1] = (3*gamma*r13**5 - 16*gamma*r13**3*r22*y + 24*gamma*r13**2*r31*y**2
                   + 16*gamma*r13*r22**2*y**2 - 32*gamma*r22*r31*y**3
                   + 640*r12*r13*y**3)/(1280*y**4)
        axis = ((4,1), (5,0), (0,3), (4,0), (2,1), (3,2))[index % 6]
        return h, axis, J.quartic_edge_partners(h)
    if kind == 'c32':
        s, b3 = small(), F(rng.randint(4, 14), 10)
        h.update({(0,2): F(1)-b3*s**3, (1,2): 3*b3*s**2,
                  (2,2): -3*b3*s, (3,2): b3, (3,1): small(), (4,1): small()})
        return h, ((0,3), (1,3), (1,2))[index % 3], J.cubic_coefficient_partners(h)
    x = F(1)
    if kind == 'delta':
        beta = F(rng.randint(3, 15), 10)
        alpha = beta**2 / (3*x)
        r12 = small()
        h.update({(1, 2): r12, (3, 1): 2*beta*r12/(3*x)})
        axis = (3, 1)
    elif kind == 'gamma':
        alpha, beta, x = [(F(1),F(-4),F(1)), (F(-6),F(3),F(1)),
                          (F(51,32),F(3,4),F(1))][index % 3]
        r12, r31, r21, r50 = (small() for _ in range(4))
        lam = (3*alpha*x+beta**2)/(6*beta*x)
        mu = (-6*alpha*r12+10*beta*lam*r12-21*lam*r31*x+30*r50*x)/(-2*(beta**2-3*alpha*x))
        r40 = (-2*beta*mu*r12-2*beta*r21-4*lam*r12**2+12*lam*r21*x
               +3*mu*r31*x+3*r12*r31)/(12*x)
        h.update({(1,2):r12,(3,1):r31,(2,1):r21,(5,0):r50,(4,0):r40})
        axis = (4, 0)
    else:
        alpha=beta=F(0)
        r12 = small()
        h.update({(1,2):r12,(2,1):r12**2/(3*x)})
        axis = (3, 1)
    h.update({(0,3):x,(4,1):alpha,(2,2):beta})
    return h, axis, J.cubic_form_partners(h)


def obstruction(h, partner, depth):
    current = partner
    for n in range(depth + 1):
        rows = [terms(G.transvectant(h, current, k)) for k in (3, 5)]
        if any(rows):
            return {'iterate': n, 'T3': rows[0], 'T5': rows[1]}
        current = G.transvectant(h, current, 1)
    raise ValueError("expected nonzero gate")


def record(h, kind, group, split, change, partners, expected_depth, rng):
    h = {m: c for m, c in h.items() if c}
    info = G.classify(h)
    depth = info['depth']
    assert depth == expected_depth, (kind, change, info)
    window = (G.weight_window(*WINDOW[kind]) if kind in WINDOW else G.degree_window(12))
    dims = G.chain(h, window, depth+1)
    assert dims[depth:] == [2, 2] and dims[depth-1] > 2
    obs = [{'polynomial': terms(partner), 'first_failure': obstruction(h, partner, depth)}
           for partner in partners]
    expected_failure = 1 if depth == 1 else depth
    assert obs and obs[0]['first_failure']['iterate'] == expected_failure
    if kind in WINDOW:
        if depth == 2:
            assert dims[1] == 2+len(partners)
            # Independence modulo 1,H via sparse exact coefficient rows.
            basis = [{(0,0): F(1)}, h, *partners]
            support = sorted(set().union(*basis))
            assert S.Matrix([[b.get(m,0) for b in basis] for m in support]).rank() == len(basis)
        else:
            assert dims[1] == 2 and all(x['first_failure']['iterate'] == 1 for x in obs)
    return {'id': f'{rng.getrandbits(96):024x}', 'group': group, 'split': split,
            'stratum': kind, 'branch': info['branch'], 'coefficients': terms(h),
            'least_depth': depth, 'core_dimension': 2, 'perturbation': change,
            'window': list(WINDOW[kind]) if kind in WINDOW else {'total_degree':12},
            'window_dimensions': dims, 'probe_certificates': obs}


def states_for(h, initial, t):
    def rhs(_, state):
        q, p = state
        return (sum(float(c)*j*q**i*p**(j-1) for (i,j),c in h.items() if j),
                -sum(float(c)*i*q**(i-1)*p**j for (i,j),c in h.items() if i))
    def energy(a):
        q,p = a.T
        return sum(float(c)*q**i*p**j for (i,j),c in h.items())
    tracks = []
    drift = 0.
    for y in initial:
        sol = solve_ivp(rhs, (0., float(t[-1])), y, t_eval=t, method='DOP853',
                        atol=1e-12, rtol=1e-11)
        if not sol.success or sol.y.shape != (2,len(t)) or not np.isfinite(sol.y).all():
            raise RuntimeError(sol.message)
        traj = sol.y.T
        e = energy(traj)
        drift = max(drift, float(np.max(np.abs(e-e[0])))/(1+abs(e[0])))
        tracks.append(traj)
    assert drift < 1e-8, drift
    return np.stack(tracks), drift


def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(r,sort_keys=True,allow_nan=False)+'\n' for r in rows))


def generate(out):
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    rows = []
    for kind in WINDOW:
        for index in range(12):
            group = f'{rng.getrandbits(96):024x}'
            split = ('train','train','validation','test')[index%4]
            h, axis, partners = instance(kind,rng,index)
            assert partners
            rows.append(record(h,kind,group,split,None,partners,2,rng))
            sign = rng.choice([-1,1])
            for eps in EPS:
                perturbed = dict(h)
                perturbed[axis] = h.get(axis,F(0))+sign*eps
                rows.append(record(perturbed,kind,group,split,
                                   {'monomial':list(axis),'delta':str(sign*eps)},
                                   partners,1,rng))
    q,p = S.symbols('q p')
    for index in range(12):
        beta = q**3 + S.Rational(index-6,20)*q**2 + S.Rational(index+1,30)*q
        potential = S.Rational(index+1,20)*q**3 + q**2/2
        h = polynomial((p+beta)**2+potential,q,p)
        rows.append(record(h,'depth-six',f'{rng.getrandbits(96):024x}',
                           ('train','train','validation','test')[index%4],None,
                           [{(1,0):F(1)},polynomial(p+beta,q,p)],6,rng))
    rng.shuffle(rows)
    assert len({json.dumps(r['coefficients']) for r in rows}) == len(rows)
    write_jsonl(out/'exact.jsonl',rows)
    initial = np.array([[-.38,-.31],[-.28,.19],[-.08,-.37],[.12,.33],[.31,-.15],[.39,.26]])
    t = np.linspace(0.,.18,49)
    max_drift = 0.
    for split in ('train','validation','test'):
        cases=[r for r in rows if r['split']==split]
        measurements=[]
        for r in cases:
            clean,drift=states_for(read_terms(r['coefficients']),initial,t)
            max_drift=max(max_drift,drift)
            noise_rng=np.random.default_rng(int(r['id'],16))
            measurements.append(clean[None]+NOISE[:,None,None,None]
                                *noise_rng.standard_normal((len(NOISE),*clean.shape)))
        np.savez_compressed(out/f'trajectories_{split}.npz',
                            ids=np.array([r['id'] for r in cases]),t=t,noise_sigma=NOISE,
                            qp=np.stack(measurements))
    import scipy
    manifest={'seed':SEED,'published_source_commit':'9695137deed389d619938c02216c4e8daa73ca20',
              'dependencies':{'numpy':np.__version__,'scipy':scipy.__version__,'sympy':S.__version__},
              'models':len(rows),'groups':len({r['group'] for r in rows}),
              'split_counts':{s:sum(r['split']==s for r in rows) for s in ('train','validation','test')},
              'noise_sigma':NOISE.tolist(),'initial_states':initial.tolist(),'max_scaled_energy_drift':max_drift,
              'sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.iterdir())
                        if f.is_file() and f.name!='manifest.json'}}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out',type=Path)
    generate(parser.parse_args().out)
