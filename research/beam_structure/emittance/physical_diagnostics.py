"""Retrospective residual-force diagnostics from compact physical-reference data.

Only NumPy is needed. These floating-point values are not validated enclosures
and the force correlations were acquired by a completed PIC solve.
"""
from pathlib import Path
import argparse,hashlib,json,math,time
import numpy as np


def transport(k,length):
    matrix=np.zeros((4,4))
    for start,kk in [(0,k),(2,-k)]:
        if kk==0:block=[[1,length],[0,1]]
        elif kk>0:
            root=math.sqrt(kk);c=math.cos(root*length);s=math.sin(root*length)
            block=[[c,s/root],[-root*s,c]]
        else:
            root=math.sqrt(-kk);c=math.cosh(root*length);s=math.sinh(root*length)
            block=[[c,s/root],[root*s,c]]
        matrix[start:start+2,start:start+2]=block
    return matrix


def diagnose(row):
    data=row['last_kick'];h=data['kick_length_m']
    back=transport(row['last_external_slice']['k_m_minus_2'],-h)
    covariance=back@np.array(row['exit_covariance'])@back.T
    mean=back@np.array(row['exit_centroid'])
    qi=[0,2];pi=[1,3];mq=mean[qi];mf=np.array(data['force_mean_per_m'])
    mp=mean[pi]-h*mf
    A=covariance[np.ix_(qi,qi)]
    M=np.array(data['qF'])-np.outer(mq,mf)
    N=np.array(data['pF'])-np.outer(mp,mf)
    L=np.array(data['FF'])-np.outer(mf,mf)
    S=covariance[np.ix_(qi,pi)]-h*M
    P=covariance[np.ix_(pi,pi)]-h*(N+N.T)-h*h*L
    covariance_before=np.block([[A,S],[S.T,P]])
    inv=np.linalg.inv(A)
    U=P-S.T@inv@S
    G=L-M.T@inv@M
    C=N-S.T@inv@M
    Unew=(covariance[np.ix_(pi,pi)]
          -covariance[np.ix_(pi,qi)]@inv@covariance[np.ix_(qi,pi)])
    predicted=U+h*(C+C.T)+h*h*G
    gram=np.block([[U,C],[C.T,G]])
    # Normalize each coordinate before reporting a PSD diagnostic. No clipping
    # of a failed matrix eigenvalue is used as mathematical certification.
    scales=np.sqrt(np.maximum(np.diag(gram),np.finfo(float).tiny))
    normalized=gram/np.outer(scales,scales)
    eig=np.linalg.eigvalsh((normalized+normalized.T)/2)
    planes=[]
    for i in range(2):
        a=A[i,i];b=S[i,i];c=P[i,i];m=M[i,i];n=N[i,i];ell=L[i,i]
        u=c-b*b/a;g=ell-m*m/a;cross=n-b*m/a
        before=a*c-b*b
        after=a*covariance[pi[i],pi[i]]-covariance[qi[i],pi[i]]**2
        rhs=before+2*h*a*cross+h*h*a*g
        scale=max(abs(before),abs(after),1e-300)
        # Tiny negative numbers are recorded as failure rather than interpreted
        # as zero nonlinear force. No calibrated floating-point error bound.
        if min(before,after,g,u,ell)<0:
            raise ValueError('negative reconstructed variance: '+row['case_id'])
        radius=abs(h)*math.sqrt(a*g)
        full_radius=abs(h)*math.sqrt(a*ell)
        delta=math.sqrt(after)-math.sqrt(before)
        planes.append({'plane':['x','y'][i],'position_variance_m2':float(a),
                       'unexplained_momentum_variance':float(u),
                       'full_force_variance_per_m2':float(ell),
                       'own_plane_residual_force_variance_per_m2':float(g),
                       'signed_ug_per_m':float(cross),
                       'emittance_before_m':math.sqrt(before),'emittance_after_m':math.sqrt(after),
                       'emittance_change_m':delta,'norm_radius_m':radius,
                       'full_force_radius_m':full_radius,
                       'radius_reduction_factor':None if radius==0 else full_radius/radius,
                       'identity_relative_residual':float(abs(after-rhs)/scale),
                       'norm_bound_numerically_satisfied':abs(delta)<=radius+1e-11*max(math.sqrt(before),radius)})
    return {'case_id':row['case_id'],'family':row['family'],'role':row['role'],
            'split':row['split'],'space_charge':row['space_charge'],
            'planes':planes,'U':U.tolist(),'G':G.tolist(),'C':C.tolist(),
            'schur_update_relative_residual':float(np.linalg.norm(Unew-predicted)/max(np.linalg.norm(Unew),1e-300)),
            'joint_gram_scaled_min_eigenvalue':float(eig[0]),
            'determinant_factorization_relative_residual':float(abs(np.linalg.det(covariance_before)-np.linalg.det(A)*np.linalg.det(U))/max(abs(np.linalg.det(covariance_before)),1e-300))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    parser.add_argument('--inputs',type=Path,default=here/'physical_inputs.json')
    parser.add_argument('--output',type=Path,default=here/'physical_receipt.json')
    args=parser.parse_args();start=time.perf_counter()
    source=json.loads(args.inputs.read_text())
    rows=[diagnose(row)for row in source['rows']]
    if not all(p['norm_bound_numerically_satisfied'] for row in rows for p in row['planes']):
        raise ValueError('numerical norm bound check failed')
    if any(row['joint_gram_scaled_min_eigenvalue'] < -1e-7 for row in rows):
        raise ValueError('reconstructed joint covariance is numerically non-PSD')
    selected=[row for row in rows if row['role']=='production' and row['space_charge']]
    summary={}
    for family in sorted({row['family']for row in selected}):
        subset=[row for row in selected if row['family']==family]
        factors=[p['radius_reduction_factor']for row in subset for p in row['planes']]
        summary[family]={'cases':len(subset),'min_radius_reduction_factor':min(factors),
                         'max_radius_reduction_factor':max(factors)}
    result={'status':'passed','schema':'retrospective-emittance-replay-v1',
            'input_sha256':hashlib.sha256(args.inputs.read_bytes()).hexdigest(),
            'cases':len(rows),'plane_kicks':2*len(rows),'production_sc_summary':summary,
            'identity_max_relative_residual':max(p['identity_relative_residual']for row in rows for p in row['planes']),
            'schur_max_relative_residual':max(row['schur_update_relative_residual']for row in rows),
            'new_particle_solver_calls':0,'diagnostic_elapsed_seconds':time.perf_counter()-start,
            'scope':'Floating-point retrospective diagnostics at the last sampled PIC kick only; not a continuum or trajectory certificate and not a computational speedup.',
            'rows':rows}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key]for key in ['status','cases','plane_kicks','production_sc_summary','identity_max_relative_residual','schur_max_relative_residual','new_particle_solver_calls']},indent=2))


if __name__=='__main__':main()
