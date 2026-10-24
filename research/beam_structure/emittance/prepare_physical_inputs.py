"""Extract compact last-kick inputs from the earlier local physical reference.

No new solver runs. The output is standalone and avoids bundling large particle
snapshots. Upstream source hashes and complete case IDs remain recorded.
"""
from pathlib import Path
import argparse,hashlib,json


def main():
    here=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',type=Path,default=here.parents[1]/'beam_reference'/'results')
    parser.add_argument('--output',type=Path,default=here/'physical_inputs.json')
    args=parser.parse_args()
    paths={name:args.reference/name for name in ['results.jsonl','cases.jsonl']}
    cases={r['case_id']:r for r in map(json.loads,paths['cases.jsonl'].read_text().splitlines())}
    rows=[]
    for r in map(json.loads,paths['results.jsonl'].read_text().splitlines()):
        case=cases[r['case_id']];kick=r['force_correlations'][-1];last=case['lattice'][-1]
        if kick['element']!=last['name']:
            raise ValueError('last kick/external element mismatch')
        h=last['length_m']/case['numerical']['nslice_per_element']
        if abs(h-kick['kick_length_m'])>1e-15:
            raise ValueError('slice length mismatch')
        rows.append({'case_id':r['case_id'],'family':case['distribution']['family'],
                     'role':case['role'],'split':case['split'],
                     'space_charge':case['numerical']['space_charge'],
                     'distribution':case['distribution'],
                     'last_external_slice':{'k_m_minus_2':last['k_m_minus_2'],'length_m':h},
                     'exit_centroid':r['derived_outputs']['centroid'],
                     'exit_covariance':r['derived_outputs']['covariance'],
                     'last_kick':kick})
    result={'schema':'retrospective-emittance-inputs-v1',
            'source_paths':{name:str(path.relative_to(here.parents[2])) for name,path in paths.items()},
            'source_sha256':{name:hashlib.sha256(path.read_bytes()).hexdigest()for name,path in paths.items()},
            'coordinate_order':['x','px','y','py'],'coordinate_units':['m','1','m','1'],
            'moment_convention':'qF,pF,FF are uncentered moments before the kick; force mean is explicit; exit covariance is centered.',
            'scope':'Last sampled self-force kick per completed run, reconstructed from the known final external map; not every slice and not a continuum enclosure.',
            'rows':rows}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'prepared','cases':len(rows),'output':str(args.output)}))


if __name__=='__main__':main()
